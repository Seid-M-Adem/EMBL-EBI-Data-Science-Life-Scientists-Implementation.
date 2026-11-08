"""Evaluating classifiers beyond a single score.

* ``per_class_report`` – precision / recall / F1 / support per class, plus macro and weighted averages, as a table
* ``bootstrap_ci`` / ``paired_bootstrap`` – uncertainty of a metric, and of the difference between two models,
  resampling whole *groups* (e.g. abstracts, patients) when rows within a group are not independent
* ``reliability_table`` / ``expected_calibration_error`` – does "90 % confident" mean right 90 % of the time?
* ``fit_temperature`` / ``apply_temperature`` – the standard one-number fix for over- or under-confidence
* ``coverage_curve`` – accuracy if the model only answers when it is confident enough
* ``normalise_text`` / ``nearest_neighbours`` – leakage checks: exact and near-duplicate texts across data splits

Metrics for the bootstrap are computed from confusion matrices, so 1,000 resamples of 30,000 rows take about a second.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.special import log_softmax
from sklearn.feature_extraction.text import TfidfVectorizer

METRICS = ("accuracy", "macro_f1", "weighted_f1")


def _confusion(y_true, y_pred, n_classes: int) -> np.ndarray:
    return np.bincount(np.asarray(y_true) * n_classes + np.asarray(y_pred), minlength=n_classes**2).reshape(
        n_classes, n_classes
    )


def metric_from_confusion(cm: np.ndarray, metric: str) -> float:
    """Accuracy, macro-F1 or weighted-F1 from a confusion matrix (rows = true class, columns = predicted)."""
    if metric not in METRICS:
        raise ValueError(f"metric must be one of {METRICS}")
    cm = np.asarray(cm, dtype=float)
    if metric == "accuracy":
        return float(np.trace(cm) / cm.sum())
    tp, support, predicted = np.diag(cm), cm.sum(1), cm.sum(0)
    denom = support + predicted
    f1 = np.divide(2 * tp, denom, out=np.zeros_like(tp), where=denom > 0)  # F1 = 2TP / (2TP + FP + FN)
    present = (
        support > 0
    )  # like scikit-learn with labels taken from the data: classes absent from y_true and y_pred
    present |= predicted > 0
    if metric == "macro_f1":
        return float(f1[present].mean())
    return float((f1 * support).sum() / support.sum())


def per_class_report(y_true, y_pred, labels: list[str]) -> pd.DataFrame:
    """One row per class (precision, recall, F1, support) plus "macro avg" and "weighted avg" rows."""
    cm = _confusion(y_true, y_pred, len(labels)).astype(float)
    tp, support, predicted = np.diag(cm), cm.sum(1), cm.sum(0)
    precision = np.divide(tp, predicted, out=np.zeros_like(tp), where=predicted > 0)
    recall = np.divide(tp, support, out=np.zeros_like(tp), where=support > 0)
    f1 = np.divide(2 * tp, support + predicted, out=np.zeros_like(tp), where=(support + predicted) > 0)
    table = pd.DataFrame(
        {"precision": precision, "recall": recall, "f1": f1, "support": support.astype(int)}, index=labels
    )
    w = support / support.sum()
    table.loc["macro avg"] = [precision.mean(), recall.mean(), f1.mean(), int(support.sum())]
    table.loc["weighted avg"] = [precision @ w, recall @ w, f1 @ w, int(support.sum())]
    table["support"] = table["support"].astype(int)
    return table


def _group_confusions(y_true, preds: list, groups, n_classes: int):
    """Per-group confusion matrices, shape (n_groups, n_models, K*K), so a bootstrap is a weighted sum."""
    y_true = np.asarray(y_true)
    if groups is None:
        groups = np.arange(len(y_true))
    _, g = np.unique(np.asarray(groups), return_inverse=True)
    n_groups = g.max() + 1
    out = np.zeros((n_groups, len(preds), n_classes * n_classes))
    for m, pred in enumerate(preds):
        cell = y_true * n_classes + np.asarray(pred)
        np.add.at(out[:, m, :], (g, cell), 1)
    return out


def bootstrap_ci(y_true, y_pred, metric: str = "macro_f1", groups=None, n_classes: int | None = None,
                 n_boot: int = 1000, level: float = 0.95, seed: int = 0) -> dict:  # fmt: skip
    """Point estimate and percentile bootstrap interval of a metric.

    With ``groups``, whole groups are resampled (a "cluster bootstrap"): if sentences from one abstract tend to be
    right or wrong together, resampling sentences individually would make the interval too narrow.
    """
    n_classes = n_classes or int(max(np.max(y_true), np.max(y_pred)) + 1)
    per_group = _group_confusions(y_true, [y_pred], groups, n_classes)[:, 0, :]
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(len(per_group), np.full(len(per_group), 1 / len(per_group)), size=n_boot)
    boot = weights @ per_group
    values = np.array([metric_from_confusion(b.reshape(n_classes, n_classes), metric) for b in boot])
    alpha = (1 - level) / 2
    estimate = metric_from_confusion(per_group.sum(0).reshape(n_classes, n_classes), metric)
    return {
        "estimate": estimate,
        "low": float(np.quantile(values, alpha)),
        "high": float(np.quantile(values, 1 - alpha)),
    }


def paired_bootstrap(y_true, pred_a, pred_b, metric: str = "macro_f1", groups=None, n_classes: int | None = None,
                     n_boot: int = 1000, level: float = 0.95, seed: int = 0) -> dict:  # fmt: skip
    """Bootstrap the difference ``metric(A) - metric(B)`` on the *same* resamples (both models see the same data).

    Returns the observed difference, its interval, and the share of resamples in which A scored higher.
    """
    n_classes = n_classes or int(max(np.max(y_true), np.max(pred_a), np.max(pred_b)) + 1)
    per_group = _group_confusions(y_true, [pred_a, pred_b], groups, n_classes)
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(len(per_group), np.full(len(per_group), 1 / len(per_group)), size=n_boot)
    boot = np.einsum("bg,gmc->bmc", weights, per_group)
    k = n_classes
    diffs = np.array([metric_from_confusion(b[0].reshape(k, k), metric) - metric_from_confusion(b[1].reshape(k, k), metric)
                      for b in boot])  # fmt: skip
    total = per_group.sum(0)
    observed = metric_from_confusion(total[0].reshape(k, k), metric) - metric_from_confusion(
        total[1].reshape(k, k), metric
    )
    alpha = (1 - level) / 2
    return {"difference": observed, "low": float(np.quantile(diffs, alpha)), "high": float(np.quantile(diffs, 1 - alpha)),
            "share_a_better": float((diffs > 0).mean())}  # fmt: skip


def reliability_table(confidence, correct, n_bins: int = 10) -> pd.DataFrame:
    """Group predictions into equal-width confidence bins; compare mean confidence with actual accuracy per bin."""
    confidence, correct = np.asarray(confidence, dtype=float), np.asarray(correct, dtype=float)
    if confidence.min() < 0 or confidence.max() > 1:
        raise ValueError("confidence must be in [0, 1]")
    edges = np.linspace(0, 1, n_bins + 1)
    bins = np.clip(np.digitize(confidence, edges[1:-1], right=True), 0, n_bins - 1)
    rows = []
    for b in range(n_bins):
        m = bins == b
        if m.any():
            rows.append({"bin_low": edges[b], "bin_high": edges[b + 1], "count": int(m.sum()),
                         "mean_confidence": confidence[m].mean(), "accuracy": correct[m].mean()})  # fmt: skip
    return pd.DataFrame(rows)


def expected_calibration_error(confidence, correct, n_bins: int = 10) -> float:
    """Average |accuracy − confidence| over bins, weighted by how many predictions fall in each bin (0 = perfect)."""
    t = reliability_table(confidence, correct, n_bins)
    return float((t["count"] * (t["accuracy"] - t["mean_confidence"]).abs()).sum() / t["count"].sum())


def apply_temperature(log_proba, temperature: float) -> np.ndarray:
    """Rescale log-probabilities (or logits) by ``1 / temperature`` and return probabilities.

    T > 1 softens over-confident predictions, T < 1 sharpens under-confident ones; the predicted class never changes.
    """
    return np.exp(log_softmax(np.asarray(log_proba, dtype=float) / temperature, axis=1))


def fit_temperature(log_proba, y_true) -> float:
    """The temperature that minimises cross-entropy on held-out data (fit on validation, never on test)."""
    log_proba, y_true = np.asarray(log_proba, dtype=float), np.asarray(y_true)

    def nll(log_t):
        lp = log_softmax(log_proba / np.exp(log_t), axis=1)
        return -lp[np.arange(len(y_true)), y_true].mean()

    return float(np.exp(minimize_scalar(nll, bounds=(-3, 3), method="bounded").x))


def coverage_curve(confidence, correct, coverages=(1.0, 0.9, 0.8, 0.7, 0.6, 0.5)) -> pd.DataFrame:
    """Accuracy on the most confident fraction of predictions ("only answer when sure"), for each coverage level."""
    confidence, correct = np.asarray(confidence, dtype=float), np.asarray(correct, dtype=float)
    order = np.argsort(-confidence, kind="stable")
    rows = []
    for c in coverages:
        k = max(1, int(round(c * len(order))))
        rows.append(
            {"coverage": c, "threshold": confidence[order[k - 1]], "accuracy": correct[order[:k]].mean()}
        )
    return pd.DataFrame(rows)


def normalise_text(text: str) -> str:
    """Lower-case and keep letters only, so trivially different copies ("Results: X." vs "results x") compare equal."""
    return re.sub(r"[^a-z]+", " ", text.lower()).strip()


def nearest_neighbours(
    queries, references, chunk_size: int = 2000, **tfidf_kwargs
) -> tuple[np.ndarray, np.ndarray]:
    """For every query text, the cosine similarity (TF-IDF, words + word pairs) to its most similar reference text,
    and that reference's index. 1.0 = same words; around 0.9 = the same sentence with a word or two changed.

    The vectoriser is fitted on the references, so words that never occur there are ignored: the score measures
    how much of a query is *covered* by known text. Work is done in chunks so large sets fit in memory.
    """
    vec = TfidfVectorizer(**({"ngram_range": (1, 2), "sublinear_tf": True} | tfidf_kwargs)).fit(references)
    ref, qry = vec.transform(references), vec.transform(queries)
    best, index = np.zeros(qry.shape[0]), np.zeros(qry.shape[0], dtype=int)
    for start in range(0, qry.shape[0], chunk_size):
        sim = (qry[start : start + chunk_size] @ ref.T).tocsr()
        best[start : start + chunk_size] = sim.max(axis=1).toarray().ravel()
        index[start : start + chunk_size] = np.asarray(sim.argmax(axis=1)).ravel()
    return best, index
