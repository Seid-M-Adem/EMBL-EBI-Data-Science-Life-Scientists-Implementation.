import numpy as np
import pandas as pd
import pytest

from dsls.survival import concordance_index, gene_set_score


def test_concordance_perfect_reversed_and_tied():
    time = [1, 2, 3, 4]
    event = [1, 1, 1, 1]
    assert concordance_index(time, event, [4, 3, 2, 1]) == 1.0
    assert concordance_index(time, event, [1, 2, 3, 4]) == 0.0
    assert concordance_index(time, event, [1, 1, 1, 1]) == 0.5


def test_concordance_skips_early_censoring():
    # patient 0 is censored at t=1: not comparable with anyone, so its (wrong) high risk doesn't count
    time, event = [1, 2, 3], [0, 1, 0]
    assert concordance_index(time, event, [9, 2, 1]) == 1.0  # only pair (1, 2) is comparable
    with pytest.raises(ValueError):
        concordance_index([1, 2], [0, 0], [1, 2])


def test_concordance_matches_brute_force():
    rng = np.random.default_rng(0)
    t, e, r = rng.integers(1, 20, 60), rng.integers(0, 2, 60), rng.normal(size=60)
    num = den = 0.0
    for i in range(60):
        for j in range(60):
            if t[i] < t[j] and e[i] == 1:
                den += 1
                num += 1.0 if r[i] > r[j] else 0.5 if r[i] == r[j] else 0.0
    assert concordance_index(t, e, r) == pytest.approx(num / den)


def test_gene_set_score():
    expr = pd.DataFrame(
        {"A": [1.0, 2.0, 3.0], "B": [10.0, 20.0, 30.0], "C": [5.0, 5.0, 5.0], "D": [3.0, 2.0, 1.0]}
    )
    score = gene_set_score(expr, ["A", "B", "C", "MISSING"])
    assert score.tolist() == pytest.approx([-1.0, 0.0, 1.0])  # A and B agree; constant C ignored
    with pytest.raises(ValueError):
        gene_set_score(expr, ["C"])
