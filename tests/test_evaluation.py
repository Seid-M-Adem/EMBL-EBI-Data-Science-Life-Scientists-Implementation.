import numpy as np
import pytest
from scipy.special import log_softmax
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support

from dsls.evaluation import (
    _confusion,
    apply_temperature,
    bootstrap_ci,
    coverage_curve,
    expected_calibration_error,
    fit_temperature,
    metric_from_confusion,
    nearest_neighbours,
    normalise_text,
    paired_bootstrap,
    per_class_report,
    reliability_table,
)

rng = np.random.default_rng(0)
Y = rng.integers(0, 4, 500)
P = np.where(rng.random(500) < 0.7, Y, rng.integers(0, 4, 500))


@pytest.mark.parametrize(
    ("metric", "reference"),
    [
        ("accuracy", accuracy_score),
        ("macro_f1", lambda y, p: f1_score(y, p, average="macro")),
        ("weighted_f1", lambda y, p: f1_score(y, p, average="weighted")),
    ],
)
def test_metrics_match_sklearn(metric, reference):
    assert metric_from_confusion(_confusion(Y, P, 4), metric) == pytest.approx(reference(Y, P))


def test_macro_f1_ignores_classes_absent_from_both_like_sklearn():
    y, p = np.array([0, 0, 1, 1]), np.array([0, 1, 1, 1])  # class 2 never appears
    assert metric_from_confusion(_confusion(y, p, 3), "macro_f1") == pytest.approx(
        f1_score(y, p, average="macro")
    )
    with pytest.raises(ValueError):
        metric_from_confusion(_confusion(y, p, 3), "auc")


def test_per_class_report_matches_sklearn():
    table = per_class_report(Y, P, ["a", "b", "c", "d"])
    prec, rec, f1, sup = precision_recall_fscore_support(Y, P)
    np.testing.assert_allclose(table.loc[["a", "b", "c", "d"], "f1"], f1)
    np.testing.assert_allclose(table.loc[["a", "b", "c", "d"], "precision"], prec)
    assert table.loc["macro avg", "f1"] == pytest.approx(f1_score(Y, P, average="macro"))
    assert table.loc["weighted avg", "recall"] == pytest.approx(rec @ (sup / sup.sum()))
    assert table.loc["macro avg", "support"] == 500


def test_bootstrap_interval_contains_estimate_and_grouping_widens_it():
    # 100 groups of 10 rows; within a group, rows are all right or all wrong (perfectly correlated)
    groups = np.repeat(np.arange(100), 10)
    y = np.zeros(1000, dtype=int)
    right = np.repeat(rng.random(100) < 0.8, 10)
    pred = np.where(right, 0, 1)
    flat = bootstrap_ci(y, pred, "accuracy", n_classes=2, n_boot=500)
    grouped = bootstrap_ci(y, pred, "accuracy", groups=groups, n_classes=2, n_boot=500)
    assert flat["low"] <= flat["estimate"] <= flat["high"]
    assert grouped["estimate"] == pytest.approx(right.mean())
    assert (grouped["high"] - grouped["low"]) > 2 * (flat["high"] - flat["low"])  # ~√10 wider


def test_paired_bootstrap():
    same = paired_bootstrap(Y, P, P, n_boot=200)
    assert same["difference"] == 0 and same["low"] == 0 and same["high"] == 0
    better = paired_bootstrap(Y, Y, P, "accuracy", n_boot=200)
    assert better["difference"] == pytest.approx(1 - accuracy_score(Y, P))
    assert better["low"] > 0 and better["share_a_better"] == 1.0


def test_reliability_and_ece():
    conf = rng.uniform(0.2, 1.0, 20000)
    calibrated = rng.random(20000) < conf  # right with probability equal to the confidence
    assert expected_calibration_error(conf, calibrated) < 0.02
    overconfident = rng.random(20000) < conf - 0.15
    assert expected_calibration_error(conf, overconfident) == pytest.approx(0.15, abs=0.03)
    table = reliability_table(conf, calibrated, n_bins=10)
    assert table["count"].sum() == 20000 and len(table) == 8  # bins below 0.2 are empty
    with pytest.raises(ValueError):
        reliability_table([1.5], [1])


def test_temperature_recovers_overconfidence():
    logits = rng.normal(0, 2, size=(5000, 4))
    y = np.array(
        [rng.choice(4, p=p) for p in np.exp(log_softmax(logits, axis=1))]
    )  # labels drawn from true probs
    T = fit_temperature(3 * logits, y)  # a model 3× too confident
    assert T == pytest.approx(3, rel=0.1)
    probs = apply_temperature(3 * logits, T)
    np.testing.assert_allclose(probs.sum(1), 1)
    assert (probs.argmax(1) == logits.argmax(1)).all()  # temperature never changes the predicted class


def test_coverage_curve():
    conf = np.array([0.9, 0.8, 0.7, 0.6])
    correct = np.array([1, 1, 0, 0])
    curve = coverage_curve(conf, correct, coverages=(1.0, 0.5))
    assert curve["accuracy"].tolist() == [0.5, 1.0]
    assert curve["threshold"].tolist() == [0.6, 0.8]


def test_normalise_text():
    assert normalise_text("RESULTS: Mortality fell (p < 0.05).") == normalise_text("results mortality fell p")
    assert normalise_text("@ %") == ""


def test_nearest_neighbours_finds_copies_and_near_copies():
    refs = ["patients were randomized into two groups", "mortality was lower in the treated group",
            "the study was registered at clinicaltrials gov"]  # fmt: skip
    queries = [
        "mortality was lower in the treated group",
        "the patients were randomized into two groups",
        "zebra",
    ]
    sim, idx = nearest_neighbours(queries, refs, chunk_size=2)
    assert sim[0] == pytest.approx(1.0) and idx[0] == 1
    assert 0.6 < sim[1] < 1.0 and idx[1] == 0
    assert sim[2] == 0.0
    # words never seen in the references are ignored: "all" adds nothing, so this counts as an exact copy
    assert nearest_neighbours(["all patients were randomized into two groups"], refs)[0][0] == pytest.approx(
        1.0
    )
