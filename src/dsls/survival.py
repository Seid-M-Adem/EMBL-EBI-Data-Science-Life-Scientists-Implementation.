"""Small, dependency-free helpers for time-to-event (survival) analysis.

* ``concordance_index`` – Harrell's C: how well a risk score orders patients by when their event happened
* ``gene_set_score`` – a per-sample score for a predefined gene set (mean of per-gene z-scores); label-free
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def concordance_index(time, event, risk) -> float:
    """Harrell's concordance index for a risk score (higher risk = event expected sooner).

    A pair of patients is *comparable* when the one with the shorter time had the event (a patient censored early
    can't be compared with someone who lived longer). C is the share of comparable pairs in which the earlier event
    has the higher risk; tied risks count one half. 0.5 is chance, 1.0 a perfect ordering. Pairs with equal times
    are skipped.
    """
    time, event, risk = (np.asarray(a, dtype=float) for a in (time, event, risk))
    if not (len(time) == len(event) == len(risk)):
        raise ValueError("time, event and risk must have the same length")
    earlier = time[:, None] < time[None, :]  # i before j
    comparable = earlier & (event[:, None] == 1)
    if not comparable.any():
        raise ValueError("no comparable pairs (are there any events?)")
    higher = risk[:, None] > risk[None, :]
    tied = risk[:, None] == risk[None, :]
    return float((higher[comparable].sum() + 0.5 * tied[comparable].sum()) / comparable.sum())


def gene_set_score(expr: pd.DataFrame, genes) -> pd.Series:
    """Mean z-score of the ``genes`` present in ``expr`` (samples × genes), one value per sample.

    Uses only the expression values, never the outcome, so it can be computed on all samples without leakage.
    Genes that don't vary are ignored.
    """
    present = [g for g in dict.fromkeys(genes) if g in expr.columns]
    sub = expr[present]
    sub = sub.loc[:, sub.std() > 0]
    if sub.shape[1] == 0:
        raise ValueError("none of the genes is present (and variable) in the data")
    z = (sub - sub.mean()) / sub.std()
    return z.mean(axis=1).rename("score")
