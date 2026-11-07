"""Tests for dsls.chembl (offline, synthetic rows shaped like ChEMBL activity records)."""

import pandas as pd
import pytest

from dsls.chembl import aggregate, curate, has_mutation, normalise_variant


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, "WT"),
        (float("nan"), "WT"),
        ("", "WT"),
        ("wild type", "WT"),
        ("L858R", "L858R"),
        ("T790M,L858R", "T790M/L858R"),
        ("L858R, T790M", "T790M/L858R"),
        ("C797S/T790M,L858R", "T790M/C797S/L858R"),
        ("T790M,T790M", "T790M"),
        ("UNDEFINED MUTATION", "undefined mutant"),
    ],
)
def test_normalise_variant(raw, expected):
    assert normalise_variant(raw) == expected


def test_has_mutation_matches_whole_tokens():
    assert has_mutation("T790M/L858R", "T790M")
    assert not has_mutation("L858R", "T790M")
    assert not has_mutation("T790MX", "T790M")


def _row(**kw):
    base = {
        "parent_molecule_chembl_id": "C1",
        "standard_relation": "=",
        "pchembl_value": "7.0",
        "data_validity_comment": None,
        "potential_duplicate": 0,
        "assay_variant_mutation": None,
        "assay_type": "B",
        "document_year": 2010,
    }
    return {**base, **kw}


def test_curate_funnel_counts_each_filter():
    df = pd.DataFrame(
        [
            _row(),
            _row(standard_relation=">"),  # censored
            _row(pchembl_value=None),  # no pChEMBL
            _row(data_validity_comment="Outside typical range"),
            _row(potential_duplicate=1),
            _row(assay_variant_mutation="T790M,L858R", assay_type="F"),
        ]
    )
    clean, funnel = curate(df)
    assert list(funnel["records"]) == [6, 4, 3, 2]
    assert list(funnel["removed"]) == [0, 2, 1, 1]
    assert len(clean) == 2
    assert set(clean["variant"]) == {"WT", "T790M/L858R"}
    assert set(clean["assay_kind"]) == {"biochemical", "cell-based"}
    assert clean["pIC50"].dtype == float


def test_aggregate_takes_median_per_group():
    df = pd.DataFrame(
        {
            "parent_molecule_chembl_id": ["A", "A", "A", "B"],
            "variant": ["WT"] * 4,
            "assay_kind": ["biochemical"] * 4,
            "pIC50": [7.0, 8.0, 9.0, 6.0],
        }
    )
    agg = aggregate(df).set_index("parent_molecule_chembl_id")
    assert agg.loc["A", "pIC50_median"] == 8.0 and agg.loc["A", "n_measurements"] == 3
    assert agg.loc["B", "n_measurements"] == 1 and pd.isna(agg.loc["B", "pIC50_sd"])
