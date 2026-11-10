"""Screening images when the positive class is rare, and when training and deployment disagree about how rare.

The protein-crystallisation datasets this module was written for have a tenfold difference in class balance:
the training set is enriched for crystals (60 %), the test set reflects a real plate (6.7 %). A classifier's
*ranking* survives that, but every probability and every threshold-dependent score does not. The helpers here
separate the two concerns:

* ``shift_prior`` – rescale predicted probabilities from the prevalence they were trained on to the prevalence
  expected in deployment. A log-odds shift; no refitting, no new data.
* ``balanced_accuracy`` / ``recall_at`` / ``screen_report`` – the metrics that matter when a missed positive is
  expensive and negatives vastly outnumber positives.
* ``best_threshold`` – choose an operating point on validation data, which is the only honest place to choose it.
* ``image_stats`` – six cheap grey-level and edge statistics per image, the "did we need deep learning?" baseline.

Nothing here imports torch, so it is importable and testable without a deep-learning stack.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

EPS = 1e-12


def shift_prior(proba, train_prior: float, target_prior: float):
    """Correct probabilities for a change in class balance between training and deployment.

    A model trained on data where positives are a fraction ``train_prior`` learns log-odds that embed that
    prevalence. Under the standard assumption that the class-conditional distributions p(x|y) are unchanged and
    only p(y) moved, the correction is a constant shift of the log-odds::

        logit(p') = logit(p) + log(target/(1-target)) - log(train/(1-train))

    So a 0.5 probability from a balanced training set becomes 0.067 when crystals are really 6.7 % of a plate.
    Monotone in ``proba``, so AUC and average precision are unchanged; calibration and any fixed threshold are not.
    """
    proba = np.clip(np.asarray(proba, dtype=float), EPS, 1 - EPS)
    for name, prior in (("train_prior", train_prior), ("target_prior", target_prior)):
        if not 0 < prior < 1:
            raise ValueError(f"{name} must be strictly between 0 and 1, got {prior}")
    offset = np.log(target_prior / (1 - target_prior)) - np.log(train_prior / (1 - train_prior))
    return 1 / (1 + np.exp(-(np.log(proba / (1 - proba)) + offset)))


def _counts(y_true, y_pred) -> tuple[int, int, int, int]:
    y_true = np.asarray(y_true).astype(bool)
    y_pred = np.asarray(y_pred).astype(bool)
    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    tn = int((~y_true & ~y_pred).sum())
    return tp, fp, fn, tn


def balanced_accuracy(y_true, y_pred) -> float:
    """Mean of sensitivity and specificity: the average of per-class recalls, so a 6.7 % positive rate can't be
    gamed by predicting "no crystal" everywhere (that scores 0.5, the same as a coin flip)."""
    tp, fp, fn, tn = _counts(y_true, y_pred)
    sensitivity = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    return float((sensitivity + specificity) / 2)


def recall_at(y_true, score, threshold: float) -> float:
    """Share of true positives caught when everything scoring at or above ``threshold`` is flagged."""
    return float(np.asarray(score)[np.asarray(y_true).astype(bool)].__ge__(threshold).mean())


def screen_report(y_true, score, threshold: float = 0.5) -> dict:
    """The numbers a screening operator actually asks for, at one operating point.

    ``recall`` is how many crystals are found, ``precision`` how much of the flagged pile is worth looking at,
    and ``flagged`` what share of all drops a human would have to inspect.
    """
    y_pred = np.asarray(score) >= threshold
    tp, fp, fn, tn = _counts(y_true, y_pred)
    return {
        "threshold": float(threshold),
        "balanced_accuracy": balanced_accuracy(y_true, y_pred),
        "recall": tp / (tp + fn) if tp + fn else 0.0,
        "specificity": tn / (tn + fp) if tn + fp else 0.0,
        "precision": tp / (tp + fp) if tp + fp else 0.0,
        "flagged": float(y_pred.mean()),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def best_threshold(
    y_true, score, metric: str = "balanced_accuracy", min_recall: float | None = None
) -> float:
    """Threshold maximising ``metric`` over the observed scores, optionally among those reaching ``min_recall``.

    Call this on a *validation* split. Choosing it on the test set and then reporting that test score is a
    textbook optimistic bias: the threshold has then been fitted to the data it is scored on.
    """
    score = np.asarray(score, dtype=float)
    candidates = np.unique(score)
    rows = [screen_report(y_true, score, t) for t in candidates]
    if min_recall is not None:
        eligible = [r for r in rows if r["recall"] >= min_recall]
        if not eligible:
            raise ValueError(f"no threshold reaches recall {min_recall}")
        rows = eligible
    if metric not in rows[0]:
        raise ValueError(f"metric must be one of {sorted(rows[0])}")
    return float(max(rows, key=lambda r: (r[metric], -r["flagged"]))["threshold"])


STAT_NAMES = ("mean", "std", "p05", "p95", "edge_mean", "edge_p99")


def image_stats(grey) -> np.ndarray:
    """Six numbers summarising one greyscale image: brightness, contrast, tails, and edge strength.

    Crystals are bright objects with straight, high-contrast edges, so a gradient magnitude ought to separate them
    from clear drops and amorphous precipitate without any learned features. ``grey`` is a 2-D array scaled to
    [0, 1]; the gradient is the plain forward difference, which needs no SciPy.
    """
    grey = np.asarray(grey, dtype=float)
    if grey.ndim != 2:
        raise ValueError(f"expected a 2-D greyscale image, got shape {grey.shape}")
    gy, gx = np.diff(grey, axis=0), np.diff(grey, axis=1)
    edges = np.hypot(gy[:, : gx.shape[1]], gx[: gy.shape[0], :])
    return np.array(
        [
            grey.mean(),
            grey.std(),
            np.quantile(grey, 0.05),
            np.quantile(grey, 0.95),
            edges.mean(),
            np.quantile(edges, 0.99),
        ],
        dtype=float,
    )


def stats_frame(stats, index=None) -> pd.DataFrame:
    """Stack ``image_stats`` rows into a named DataFrame."""
    return pd.DataFrame(np.asarray(stats, dtype=float), columns=list(STAT_NAMES), index=index)
