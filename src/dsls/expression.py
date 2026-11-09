"""Helpers for exploring bulk gene-expression matrices (TCGA-style) and judging low-dimensional embeddings.

Conventions: expression tables are **samples × genes** (rows are samples), labels are a ``pd.Series`` indexed by
sample ID. Nothing here looks at labels unless its name says so, so the unsupervised steps stay label-free.

``GeneSelector`` is a scikit-learn transformer, so gene selection can sit *inside* a pipeline and be re-fitted on each
cross-validation training fold: the only way to select genes without leaking the test labels.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import mannwhitneyu, spearmanr
from sklearn.base import BaseEstimator, TransformerMixin
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


class GeneSelector(BaseEstimator, TransformerMixin):
    """Keep ``k`` genes (columns of a samples × genes DataFrame), chosen on the data passed to ``fit`` only.

    ``method``:

    * ``"mannwhitney"`` – smallest Mann-Whitney U p-value between the two classes (label-aware, a simple
      differential-expression filter); constant genes get p = 1
    * ``"variance"`` – highest variance (label-free)
    * ``"fixed"`` – the first ``k`` of ``genes`` that are present (e.g. a literature list; ignores the data)
    * ``"random"`` – ``k`` random genes, a baseline (seeded by ``seed``)

    The chosen names are in ``genes_``. Ties are broken by column order, so results are reproducible.
    """

    def __init__(self, k: int = 200, method: str = "mannwhitney", genes=None, seed: int = 0):
        self.k = k
        self.method = method
        self.genes = genes
        self.seed = seed

    def fit(self, X: pd.DataFrame, y=None):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("GeneSelector needs a DataFrame with gene names as columns")
        if self.k < 1:
            raise ValueError("k must be at least 1")
        columns = X.columns
        if self.method == "mannwhitney":
            if y is None:
                raise ValueError("method='mannwhitney' needs labels")
            y = np.asarray(y)
            classes = np.unique(y)
            if len(classes) != 2:
                raise ValueError("method='mannwhitney' needs exactly two classes")
            values = X.to_numpy(dtype=float)
            p = mannwhitneyu(values[y == classes[1]], values[y == classes[0]], axis=0).pvalue
            score = -np.nan_to_num(p, nan=1.0)
        elif self.method == "variance":
            score = X.var(axis=0).to_numpy()
        elif self.method == "fixed":
            present = [g for g in dict.fromkeys(self.genes or []) if g in set(columns)]
            if not present:
                raise ValueError("none of the fixed genes is in the data")
            self.genes_ = present[: self.k]
            return self
        elif self.method == "random":
            rng = np.random.default_rng(self.seed)
            self.genes_ = list(rng.choice(columns, size=min(self.k, len(columns)), replace=False))
            return self
        else:
            raise ValueError(f"unknown method {self.method!r}")
        order = np.argsort(-score, kind="stable")[: self.k]
        self.genes_ = list(columns[order])
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X[self.genes_]

    def get_feature_names_out(self, input_features=None):
        return np.asarray(self.genes_, dtype=object)
