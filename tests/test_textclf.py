"""Tests for dsls.textclf (CPU only, tiny synthetic data, a few seconds)."""

import numpy as np
import pytest
import scipy.sparse as sp

torch = pytest.importorskip("torch")

from dsls.textclf import (  # noqa: E402
    MLPClassifier,
    make_loader,
    position_features,
    predict_proba,
    train_with_early_stopping,
)


def test_position_features():
    f = position_features([0, 2, 4, 0], [5, 5, 5, 1])
    assert f.shape == (4, 12)
    np.testing.assert_allclose(f[:, 0], [0, 0.5, 1, 0])  # relative position; one-sentence abstract → 0
    assert (f[:, 2:].sum(1) == 1).all()  # exactly one tenth-of-abstract bin
    assert f[2, 2 + 9] == 1 and f[0, 2] == 1
    with pytest.raises(ValueError):
        position_features([5], [5])


def test_make_loader_densifies_sparse_batches_and_appends_extra():
    X = sp.random(10, 7, density=0.3, format="csr", random_state=0)
    extra = np.arange(20, dtype=np.float32).reshape(10, 2)
    batches = list(make_loader(X, y=np.arange(10) % 2, extra=extra, batch_size=4))
    assert [b[0].shape for b in batches] == [(4, 9), (4, 9), (2, 9)]
    np.testing.assert_allclose(batches[0][0][:, :7].numpy(), X[:4].toarray(), rtol=1e-6)
    np.testing.assert_allclose(batches[0][0][:, 7:].numpy(), extra[:4])
    with pytest.raises(ValueError):
        make_loader(X, y=[0, 1])


def _toy(n, seed):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 3, n)
    X = rng.normal(size=(n, 6)).astype(np.float32)
    X[np.arange(n), y] += 3.0  # class k is signalled by feature k
    return X, y


def test_training_learns_and_restores_best_weights():
    X, y = _toy(600, 0)
    Xv, yv = _toy(200, 1)
    model = MLPClassifier(6, 3, hidden=16, dropout=0.0, input_dropout=0.0)
    history = train_with_early_stopping(
        model,
        make_loader(X, y, batch_size=32, shuffle=True),
        make_loader(Xv, yv, batch_size=64),
        score_fn=lambda t, p: (t == p).mean(),
        max_epochs=15,
        patience=2,
        device=torch.device("cpu"),
    )
    proba = predict_proba(model, make_loader(Xv, yv, batch_size=64))
    np.testing.assert_allclose(proba.sum(1), 1, rtol=1e-5)
    accuracy = (proba.argmax(1) == yv).mean()
    assert accuracy > 0.9
    assert accuracy == pytest.approx(max(h["val_score"] for h in history))  # best epoch's weights restored
    assert {"train_loss", "val_loss", "val_score", "seconds"} <= set(history[0])


def test_seed_makes_initial_weights_reproducible():
    a, b, c = (MLPClassifier(6, 3, hidden=8, seed=s) for s in (1, 1, 2))
    for pa, pb, pc in zip(a.parameters(), b.parameters(), c.parameters(), strict=True):
        assert torch.equal(pa, pb)
        assert pa.shape == pc.shape
    assert not torch.equal(a.net[1].weight, c.net[1].weight)
