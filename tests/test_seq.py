"""Tests for dsls.seq (pure functions, no network)."""

import io

import pytest

from dsls.seq import Record, composition, find_motif, gravy, kmer_counts, kmers, parse_fasta

FASTA = """>sp|P29972|AQP1_HUMAN Aquaporin-1 OS=Homo sapiens OX=9606 GN=AQP1
MASEFKKKLF
wrAVVAEFLA\r

>seq2 plain header
ACGT
"""


def test_parse_fasta_multiline_blank_lines_crlf_and_case():
    recs = list(parse_fasta(FASTA))
    assert [r.id for r in recs] == ["sp|P29972|AQP1_HUMAN", "seq2"]
    assert recs[0].sequence == "MASEFKKKLFWRAVVAEFLA"
    assert recs[0].description.startswith("Aquaporin-1 OS=Homo sapiens")
    assert recs[0].accession == "P29972" and recs[1].accession == "seq2"
    assert recs[1].description == "plain header"


def test_parse_fasta_accepts_file_handles_and_paths(tmp_path):
    assert [r.sequence for r in parse_fasta(io.StringIO(FASTA))][1] == "ACGT"
    p = tmp_path / "x.fa"
    p.write_text(FASTA)
    assert len(list(parse_fasta(p))) == 2
    assert len(list(parse_fasta(str(p)))) == 2


def test_parse_fasta_rejects_sequence_before_header():
    with pytest.raises(ValueError, match="before the first"):
        list(parse_fasta("ACGT\n>x\nAC\n"))


def test_parse_fasta_empty_input_and_empty_record():
    assert list(parse_fasta("")) == []
    assert list(parse_fasta(">only_header\n")) == [Record("only_header", "", "")]


def test_kmers_overlap_and_edge_cases():
    assert list(kmers("ACGT", 2)) == ["AC", "CG", "GT"]
    assert list(kmers("AC", 3)) == []
    with pytest.raises(ValueError):
        list(kmers("AC", 0))


def test_kmer_counts_with_alphabet_filter():
    assert kmer_counts("AAAA", 2) == {"AA": 3}  # overlapping
    assert kmer_counts("ANXA", 2, alphabet="AN") == {"AN": 1}


def test_composition_ignores_non_alphabet_and_sums_to_one():
    comp = composition("AAX-C", alphabet="AC")
    assert comp == {"A": 2 / 3, "C": 1 / 3}
    assert composition("", alphabet="AC") == {"A": 0.0, "C": 0.0}


def test_gravy_matches_kyte_doolittle():
    assert gravy("IV") == pytest.approx((4.5 + 4.2) / 2)
    assert gravy("RX") == pytest.approx(-4.5)  # X ignored
    with pytest.raises(ValueError):
        gravy("XXX")


def test_find_motif_reports_overlapping_hits():
    assert find_motif("NPANPA", "NPA") == [0, 3]
    assert find_motif("AAAA", "AA") == [0, 1, 2]
    assert find_motif("NPGxNPC", "NP[ACG]") == [0, 4]
