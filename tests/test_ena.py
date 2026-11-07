"""Tests for dsls.ena (offline: a fake client returns canned /count and /search responses)."""

import pandas as pd
import pytest

from dsls.ena import assay_type, completeness, fetch_runs, fetch_samples, is_placeholder, sum_bytes

TSV = (
    "run_accession\tinstrument_model\tread_count\tbase_count\tfastq_bytes\tfirst_public\tlat\n"
    "ERR1\tIllumina HiSeq 2000\t100\t20000\t10;12\t2014-01-02\t-20.5\n"
    "ERR2\tunspecified\t50\t5000\t7\t2013-07-22\t\n"
)


class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeClient:
    def __init__(self, count):
        self.count, self.calls = count, []

    def get(self, path, params=None, **kw):
        self.calls.append((path, params))
        return FakeResponse(f"{self.count}\n" if path == "count" else TSV)


def test_fetch_runs_parses_types_and_checks_count():
    client = FakeClient(2)
    df = fetch_runs("PRJEB0", fields="x", client=client)
    assert list(df["read_count"]) == [100, 50]
    assert list(df["fastq_bytes"]) == [22, 7]  # paired files summed
    assert df["first_public"].dt.year.tolist() == [2014, 2013]
    assert pd.isna(df.loc[1, "lat"])
    assert client.calls[1][1]["limit"] == 0 and client.calls[1][1]["query"] == "study_accession=PRJEB0"


def test_fetch_runs_rejects_truncated_download():
    with pytest.raises(ValueError, match="/count reports 3"):
        fetch_runs("PRJEB0", fields="x", client=FakeClient(3))


@pytest.mark.parametrize(
    ("value", "expected"), [("1;2", 3), ("5", 5), ("", None), (None, None), (float("nan"), None)]
)
def test_sum_bytes(value, expected):
    assert sum_bytes(value) == expected


@pytest.mark.parametrize(
    ("strategy", "source", "expected"),
    [
        ("AMPLICON", "METAGENOMIC", "Amplicon (marker gene)"),
        ("RNA-Seq", "METATRANSCRIPTOMIC", "Metatranscriptome"),
        ("WGS", "METAGENOMIC", "Metagenome"),
        ("WGA", "GENOMIC", "Single-cell genome (WGA)"),
        ("WGS", "GENOMIC", "Genome (WGS)"),
        (None, None, "Other"),
    ],
)
def test_assay_type(strategy, source, expected):
    assert assay_type(strategy, source) == expected


def test_is_placeholder():
    assert is_placeholder("deep chlorophyll maximum layer (ENVO:xxxxxxxx)")
    assert is_placeholder("filtered seawater (ENVO:xxxxxxxxx)")
    assert not is_placeholder("surface water layer (ENVO:00002042)")
    assert not is_placeholder(None)


def test_completeness_treats_unspecified_as_empty():
    df = pd.DataFrame({"a": ["x", None, "unspecified", " "], "b": ["1", "2", "3", "4"]})
    c = completeness(df).set_index("field")
    assert c.loc["a", "filled"] == 0.25 and c.loc["a", "empty_runs"] == 3
    assert c.loc["b", "filled"] == 1.0


class SampleClient:
    def __init__(self, known):
        self.known, self.batches = known, []

    def get(self, path, params=None, **kw):
        acc = params["includeAccessions"].split(",")
        self.batches.append(acc)
        rows = "".join(f"{a}\talias_{a}\n" for a in acc if a in self.known)
        return FakeResponse("sample_accession\tsample_alias\n" + rows)


def test_fetch_samples_batches_and_deduplicates():
    client = SampleClient({"S1", "S2", "S3"})
    df = fetch_samples(
        ["S3", "S1", "S2", "S1"], fields="sample_accession,sample_alias", client=client, batch=2
    )
    assert client.batches == [["S1", "S2"], ["S3"]]
    assert sorted(df["sample_accession"]) == ["S1", "S2", "S3"]


def test_fetch_samples_reports_missing_accessions():
    with pytest.raises(ValueError, match="1 sample accessions not returned"):
        fetch_samples(["S1", "S9"], fields="sample_accession", client=SampleClient({"S1"}))
