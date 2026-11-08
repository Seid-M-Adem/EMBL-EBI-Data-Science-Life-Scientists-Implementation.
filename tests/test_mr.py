"""Tests for dsls.mr (pure functions, no network)."""

import pandas as pd
import pytest

from dsls.mr import (
    COURSE_FEATURES,
    POST_MR_FEATURES,
    load_mr_data,
    standard_space_group,
    subsample_prevalence,
)

CSV = """sweep_id,pdb_id_id,MR_success,LLG,mr_sg_no,model_res,totalobservations
1,10,1.00,"2,449.00",2018,1.70,"576,429"
2,10,1.00,"1,000.00",19,0.00,"12,755"
3,11,0.00,55.00,1018,2.50,"8,768"
"""


def test_standard_space_group():
    assert [standard_space_group(n) for n in (1, 19, 1017, 1018, 2018, 230)] == [1, 19, 17, 18, 18, 230]
    for bad in (0, 231, 1000):
        with pytest.raises(ValueError):
            standard_space_group(bad)


def test_load_mr_data_fixes_audit_issues(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text(CSV)
    df = load_mr_data(path)
    assert df["LLG"].tolist() == [2449.0, 1000.0, 55.0]  # thousands separators parsed
    assert df["totalobservations"].tolist() == [576429, 12755, 8768]
    assert df["mr_sg_no"].tolist() == [18, 19, 18]
    assert df["model_res"].isna().tolist() == [False, True, False]  # 0 Å → missing
    assert df["MR_success"].dtype.kind == "i"


def test_feature_lists_do_not_overlap():
    assert len(COURSE_FEATURES) == 27 == len(set(COURSE_FEATURES))
    assert not set(COURSE_FEATURES) & set(POST_MR_FEATURES)


def test_subsample_prevalence_keeps_targets_whole():
    df = pd.DataFrame(
        {"pdb_id_id": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9], "MR_success": [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]}
    )
    sub = subsample_prevalence(df, 0.2, seed=0)
    assert (sub["MR_success"] == 0).sum() == 6  # all negatives kept
    assert sub["MR_success"].mean() >= 0.2
    for target, rows in df.groupby("pdb_id_id"):
        assert len(sub[sub["pdb_id_id"] == target]) in (0, len(rows))  # whole target or nothing
    mixed = pd.DataFrame({"pdb_id_id": [1, 1], "MR_success": [0, 1]})
    with pytest.raises(ValueError):
        subsample_prevalence(mixed, 0.5)
    with pytest.raises(ValueError):
        subsample_prevalence(df, 1.5)
