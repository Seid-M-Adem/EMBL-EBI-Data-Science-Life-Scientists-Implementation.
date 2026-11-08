"""Small, reusable PyTorch pieces for classifying sentences (or any rows of features).

* ``position_features`` – where a sentence sits in its abstract, as numbers a model can use
* ``make_loader`` – batches from a (sparse) feature matrix, densified one batch at a time to save memory
* ``MLPClassifier`` – a one-hidden-layer network with dropout
* ``train_with_early_stopping`` – the training loop: train, validate each epoch, keep the best weights
* ``predict_proba`` / ``pick_device``

Install with ``pip install -e ".[dl]"`` (PyTorch is an optional dependency).
"""

from __future__ import annotations

import copy
import time
from collections.abc import Callable

import numpy as np
import scipy.sparse as sp
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


def pick_device() -> torch.device:
    """CUDA GPU if present, else Apple-silicon GPU (MPS), else CPU."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def position_features(sentence_id, n_sentences, n_bins: int = 10) -> np.ndarray:
    """Encode a sentence's place in its abstract.

    Columns: relative position (0 = first sentence, 1 = last), abstract length (log-scaled), and a one-hot
    "which tenth of the abstract" indicator, which lets even a linear layer learn non-monotonic patterns.
    """
    sid = np.asarray(sentence_id, dtype=float)
    n = np.asarray(n_sentences, dtype=float)
    if np.any(n < 1) or np.any(sid < 0) or np.any(sid >= n):
        raise ValueError("need 0 <= sentence_id < n_sentences")
    rel = sid / np.maximum(n - 1, 1)
    bins = np.eye(n_bins)[np.minimum((rel * n_bins).astype(int), n_bins - 1)]
    return np.column_stack([rel, np.log(n) / 3, bins]).astype(np.float32)


class _RowIndex(Dataset):
    def __init__(self, n: int):
        self.n = n

    def __len__(self) -> int:
        return self.n

    def __getitem__(self, i: int) -> int:
        return i


def make_loader(
    X, y=None, extra=None, batch_size: int = 256, shuffle: bool = False, seed: int = 0
) -> DataLoader:
    """A ``DataLoader`` of ``(features, labels)`` batches from a dense or sparse matrix ``X``.

    Sparse rows (e.g. TF-IDF) are converted to dense tensors **per batch**, so a 176,000 × 50,000 matrix never has
    to fit in memory as dense numbers. ``extra`` (dense, same number of rows) is appended column-wise.
    """
    X = sp.csr_matrix(X) if sp.issparse(X) else np.asarray(X, dtype=np.float32)
    n = X.shape[0]
    if extra is not None and len(extra) != n:
        raise ValueError("extra must have one row per row of X")
    if y is not None and len(y) != n:
        raise ValueError("y must have one entry per row of X")
    labels = None if y is None else torch.as_tensor(np.asarray(y), dtype=torch.long)

    def collate(idx):
        rows = X[idx]
        x = torch.from_numpy(rows.toarray() if sp.issparse(rows) else rows).float()
        if extra is not None:
            x = torch.cat([x, torch.as_tensor(np.asarray(extra)[idx], dtype=torch.float32)], dim=1)
        return x, (labels[idx] if labels is not None else torch.empty(0))

    generator = torch.Generator().manual_seed(seed)
    return DataLoader(
        _RowIndex(n), batch_size=batch_size, shuffle=shuffle, collate_fn=collate, generator=generator
    )


class MLPClassifier(nn.Module):
    """input → dropout → linear → ReLU → dropout → linear → one score (logit) per class.

    Pass ``seed`` for reproducible starting weights: initial weights are random, and without a seed two otherwise
    identical runs start (and end) in different places. The global random state is left untouched.
    """

    def __init__(self, n_inputs: int, n_classes: int, hidden: int = 256, dropout: float = 0.5,
                 input_dropout: float = 0.2, seed: int | None = None):  # fmt: skip
        super().__init__()
        with torch.random.fork_rng(devices=[]):
            if seed is not None:
                torch.manual_seed(seed)
            self.net = nn.Sequential(
                nn.Dropout(input_dropout),
                nn.Linear(n_inputs, hidden),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden, n_classes),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


@torch.no_grad()
def predict_proba(model: nn.Module, loader: DataLoader, device=None) -> np.ndarray:
    """Class probabilities (softmax of the logits) for every row the loader yields, in order."""
    device = device or next(model.parameters()).device
    model.eval()
    return torch.cat([torch.softmax(model(x.to(device)), dim=1).cpu() for x, _ in loader]).numpy()


def train_with_early_stopping(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    score_fn: Callable[[np.ndarray, np.ndarray], float],
    max_epochs: int = 30,
    patience: int = 3,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    device=None,
    seed: int = 0,
) -> list[dict]:
    """Train with AdamW and cross-entropy; after each epoch score the validation set with ``score_fn(y, pred)``.

    Stops after ``patience`` epochs without improvement and **restores the best weights**. Returns one dict per
    epoch (training loss, validation loss, validation score, seconds), handy for learning curves.
    """
    torch.manual_seed(seed)
    device = device or pick_device()
    model.to(device)
    optimiser = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    loss_fn = nn.CrossEntropyLoss()
    y_val = torch.cat([y for _, y in val_loader]).numpy()

    history, best_score, best_state, waited = [], -np.inf, None, 0
    for epoch in range(1, max_epochs + 1):
        start = time.perf_counter()
        model.train()
        total, count = 0.0, 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimiser.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            optimiser.step()
            total += loss.item() * len(y)
            count += len(y)
        proba = predict_proba(model, val_loader, device)
        val_loss = float(loss_fn(torch.log(torch.as_tensor(proba).clamp_min(1e-12)), torch.as_tensor(y_val)))
        # (CrossEntropyLoss on log-probabilities equals the negative log-likelihood of the true class)
        score = float(score_fn(y_val, proba.argmax(1)))
        history.append({"epoch": epoch, "train_loss": total / count, "val_loss": val_loss, "val_score": score,
                        "seconds": time.perf_counter() - start})  # fmt: skip
        if score > best_score:
            best_score, best_state, waited = score, copy.deepcopy(model.state_dict()), 0
        else:
            waited += 1
            if waited >= patience:
                break
    model.load_state_dict(best_state)
    return history
