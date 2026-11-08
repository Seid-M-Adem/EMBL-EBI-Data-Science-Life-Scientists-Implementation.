"""Tests for dsls.expression (pure functions, no network)."""

import numpy as np
import pandas as pd
import pytest

from dsls.expression import (
    balanced_subsample,
    centroid_distance_correlation,
    knn_label_agreement,
    tcga_sample_type,
    top_variable_genes,
)


def test_tcga_sample_type_short_and_long_barcodes():
    assert tcga_sample_type("TCGA-S9-A7J2-01") == "01"
    assert tcga_sample_type("TCGA-44-6778-11A-01R-1858-07") == "11"
    for bad in ["TCGA-S9-A7J2", "sample_1", "TCGA-S9-A7J2-XX"]:
        with pytest.raises(ValueError):
            tcga_sample_type(bad)


def test_balanced_subsample_caps_each_class_and_is_reproducible():
    labels = pd.Series(["a"] * 10 + ["b"] * 3, index=[f"s{i:02d}" for i in range(13)])
    sub = balanced_subsample(labels, n_per_class=5, seed=1)
    assert sub.value_counts().to_dict() == {"a": 5, "b": 3}  # small class kept whole
    assert sub.index.is_unique and set(sub.index) <= set(labels.index)
    assert sub.index.tolist() == balanced_subsample(labels, 5, seed=1).index.tolist()
    assert list(sub) == sorted(sub)  # grouped by class
    with pytest.raises(ValueError):
        balanced_subsample(labels, 0)


def test_top_variable_genes_orders_by_variance():
    expr = pd.DataFrame({"flat": [1, 1, 1, 1], "mid": [0, 1, 0, 1], "wide": [0, 10, 0, 10]})
    assert top_variable_genes(expr, 2) == ["wide", "mid"]
    assert top_variable_genes(expr, 10) == ["wide", "mid", "flat"]


def test_embedding_scores_separate_good_from_scrambled():
    rng = np.random.default_rng(0)
    centres = np.array([[0, 0], [10, 0], [0, 30], [40, 40]])
    labels = np.repeat(np.arange(4), 25)
    high = centres[labels] + rng.normal(size=(100, 2))
    assert knn_label_agreement(high, labels, k=5) == pytest.approx(1.0)
    assert centroid_distance_correlation(high, high * 3, labels) == pytest.approx(1.0)  # scaling keeps ranks
    shuffled = rng.permutation(labels)
    assert knn_label_agreement(high, shuffled, k=5) < 0.5
    with pytest.raises(ValueError):
        centroid_distance_correlation(high, high, labels % 2)
