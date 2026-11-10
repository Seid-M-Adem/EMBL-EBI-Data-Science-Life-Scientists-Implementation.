"""Offline unit tests for :mod:`dsls.crystals`."""

from __future__ import annotations

import numpy as np
import pytest

from dsls.crystals import (
    STAT_NAMES,
    balanced_accuracy,
    best_threshold,
    image_stats,
    recall_at,
    screen_report,
    shift_prior,
    stats_frame,
)


def test_shift_prior_moves_a_balanced_half_to_the_target_prevalence():
    # A 0.5 probability carries no evidence either way, so it should land exactly on the new prior.
    assert shift_prior([0.5], train_prior=0.5, target_prior=0.067)[0] == pytest.approx(0.067)


def test_shift_prior_is_identity_when_the_priors_match():
    proba = np.array([0.01, 0.3, 0.5, 0.9, 0.999])
    assert shift_prior(proba, 0.4, 0.4) == pytest.approx(proba)


def test_shift_prior_preserves_ranking():
    proba = np.array([0.1, 0.4, 0.45, 0.8])
    shifted = shift_prior(proba, 0.6, 0.067)
    assert np.all(np.diff(shifted) > 0)  # monotone, so AUC is unchanged
    assert np.all(shifted < proba)  # a rarer positive class lowers every probability


def test_shift_prior_rejects_impossible_priors():
    with pytest.raises(ValueError, match="train_prior"):
        shift_prior([0.5], 0.0, 0.1)
    with pytest.raises(ValueError, match="target_prior"):
        shift_prior([0.5], 0.5, 1.0)


def test_balanced_accuracy_scores_the_majority_rule_at_one_half():
    y = np.array([1] * 7 + [0] * 93)
    assert balanced_accuracy(y, np.zeros(100)) == pytest.approx(0.5)
    assert balanced_accuracy(y, y) == pytest.approx(1.0)


def test_balanced_accuracy_averages_the_two_recalls():
    # 8 of 10 positives caught, 90 of 100 negatives rejected  ->  (0.8 + 0.9) / 2
    y = np.array([1] * 10 + [0] * 100)
    pred = np.array([1] * 8 + [0] * 2 + [1] * 10 + [0] * 90)
    assert balanced_accuracy(y, pred) == pytest.approx(0.85)


def test_recall_at_counts_only_positives():
    y = [1, 1, 1, 0, 0]
    score = [0.9, 0.6, 0.2, 0.95, 0.8]
    assert recall_at(y, score, 0.5) == pytest.approx(2 / 3)


def test_screen_report_counts_add_up_and_precision_reflects_rarity():
    y = np.array([1] * 10 + [0] * 990)
    score = np.concatenate([np.full(10, 0.9), np.full(90, 0.9), np.full(900, 0.1)])
    r = screen_report(y, score, 0.5)
    assert r["tp"] + r["fp"] + r["fn"] + r["tn"] == 1000
    assert r["recall"] == pytest.approx(1.0)
    assert r["precision"] == pytest.approx(0.1)  # 10 of 100 flagged
    assert r["flagged"] == pytest.approx(0.1)


def test_best_threshold_finds_the_separating_cut():
    y = np.array([0, 0, 0, 1, 1, 1])
    score = np.array([0.1, 0.2, 0.3, 0.7, 0.8, 0.9])
    assert balanced_accuracy(y, score >= best_threshold(y, score)) == pytest.approx(1.0)


def test_best_threshold_honours_a_recall_floor():
    y = np.array([1, 1, 0, 0, 0, 0])
    score = np.array([0.9, 0.2, 0.5, 0.4, 0.3, 0.1])
    # Maximising balanced accuracy alone would drop the positive scoring 0.2; a 100 % recall floor cannot.
    assert recall_at(y, score, best_threshold(y, score, min_recall=1.0)) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="no threshold"):
        best_threshold(y, score, min_recall=1.01)


def test_image_stats_separates_an_edge_from_a_flat_field():
    flat = np.full((16, 16), 0.5)
    striped = np.tile([0.0, 1.0], (16, 8))
    f, s = image_stats(flat), image_stats(striped)
    assert f[STAT_NAMES.index("std")] == pytest.approx(0.0)
    assert f[STAT_NAMES.index("edge_mean")] == pytest.approx(0.0)
    assert s[STAT_NAMES.index("edge_mean")] > 0.5  # strong edges everywhere
    assert len(f) == len(STAT_NAMES)


def test_image_stats_rejects_colour_images():
    with pytest.raises(ValueError, match="2-D greyscale"):
        image_stats(np.zeros((8, 8, 3)))


def test_stats_frame_is_named():
    frame = stats_frame([image_stats(np.zeros((4, 4))), image_stats(np.ones((4, 4)))], index=["a", "b"])
    assert list(frame.columns) == list(STAT_NAMES)
    assert list(frame.index) == ["a", "b"]
