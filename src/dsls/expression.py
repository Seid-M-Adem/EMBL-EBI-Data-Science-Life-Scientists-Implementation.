"""Helpers for exploring bulk gene-expression matrices (TCGA-style) and judging low-dimensional embeddings.

Conventions: expression tables are **samples × genes** (rows are samples), labels are a ``pd.Series`` indexed by
sample ID. Nothing here looks at labels unless its name says so, so the unsupervised steps stay label-free.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

#: TCGA sample-type codes (barcode characters 14–15) used in this repo.
SAMPLE_TYPES = {
    "01": "Primary Solid Tumor",
    "02": "Recurrent Solid Tumor",
    "03": "Primary Blood Derived Cancer",
    "06": "Metastatic",
    "11": "Solid Tissue Normal",
}


def tcga_sample_type(barcode: str) -> str:
    """Two-digit sample-type code of a TCGA barcode, e.g. ``"TCGA-S9-A7J2-01"`` → ``"01"``.

    Works for both the short (``…-01``) and long (``…-01A-11R-…``) forms.
    """
    parts = barcode.split("-")
    if len(parts) < 4 or len(parts[3]) < 2 or not parts[3][:2].isdigit():
        raise ValueError(f"not a TCGA sample barcode: {barcode!r}")
    return parts[3][:2]


def balanced_subsample(labels: pd.Series, n_per_class: int, seed: int = 0) -> pd.Series:
    """Draw up to ``n_per_class`` samples from every class (all of them if a class is smaller).

    Returns the selected labels, sorted by class then sample ID, so the result is reproducible for a given seed.
    """
    if n_per_class < 1:
        raise ValueError("n_per_class must be at least 1")
    picked = [
        group.sample(n=min(n_per_class, len(group)), random_state=seed)
        for _, group in labels.groupby(labels, sort=True)
    ]
    out = pd.concat(picked)
    return out.loc[sorted(out.index, key=lambda s: (out[s], s))]


def top_variable_genes(expr: pd.DataFrame, n: int) -> list[str]:
    """Names of the ``n`` genes (columns) with the highest variance across samples. Label-free."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return expr.var(axis=0).sort_values(ascending=False, kind="stable").index[:n].tolist()


def knn_label_agreement(embedding: np.ndarray, labels, k: int = 10, cv: int = 5, seed: int = 0) -> float:
    """Cross-validated accuracy of a k-nearest-neighbour classifier *in the embedding*.

    A label-aware score of how well an embedding keeps samples of the same class next to each other. It is used
    only to *judge* embeddings after they are made, never to build them.
    """
    folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
    return float(cross_val_score(KNeighborsClassifier(n_neighbors=k), embedding, labels, cv=folds).mean())


def centroid_distance_correlation(high: np.ndarray, low: np.ndarray, labels) -> float:
    """Spearman correlation between class-centroid distances in the original space and in an embedding.

    Near 1: the embedding keeps the *global* arrangement of classes (which classes are near which). t-SNE and UMAP
    are designed to keep *local* neighbourhoods, so this number tells you how far to trust between-cluster gaps.
    """
    labels = np.asarray(labels)
    classes = np.unique(labels)
    if len(classes) < 3:
        raise ValueError("need at least 3 classes to correlate centroid distances")
    c_high = np.vstack([high[labels == c].mean(axis=0) for c in classes])
    c_low = np.vstack([low[labels == c].mean(axis=0) for c in classes])
    return float(spearmanr(pdist(c_high), pdist(c_low)).statistic)
