import numpy as np
import pytest

from dsls.protein import AMINO_ACIDS, aa_composition, coarse_locations

REAL = (  # UniProt A0A087X1C5 (abridged): only the mitochondrion statement is experimental
    "SUBCELLULAR LOCATION: Membrane {ECO:0000305}; Multi-pass membrane protein {ECO:0000255}. "
    "Cytoplasm {ECO:0000305|PubMed:15051713}. Mitochondrion {ECO:0000269|PubMed:18838503}."
)


def test_experimental_only_keeps_ECO_0000269():
    assert coarse_locations(REAL) == {"mitochondrion"}
    # the bare "Membrane" term is too vague to map
    assert coarse_locations(REAL, experimental_only=False) == {"cytoplasm", "mitochondrion"}


def test_subterms_isoforms_and_notes():
    text = (
        "SUBCELLULAR LOCATION: [Isoform 2]: Nucleus, nucleolus {ECO:0000269|PubMed:1}. "
        "Mitochondrion inner membrane {ECO:0000269}; Single-pass membrane protein {ECO:0000255}. "
        "Cytoplasm, perinuclear region {ECO:0000269}. "
        "Note=Translocates to the Golgi apparatus {ECO:0000269} upon stress."
    )
    # "perinuclear" is not the nucleus; the Note is ignored
    assert coarse_locations(text) == {"nucleus", "mitochondrion", "cytoplasm"}


def test_membranes_and_secreted():
    text = "SUBCELLULAR LOCATION: Cell membrane {ECO:0000269}. Secreted {ECO:0000269}. Endoplasmic reticulum membrane {ECO:0000269}."
    assert coarse_locations(text) == {"cell membrane", "secreted", "endoplasmic reticulum"}


@pytest.mark.parametrize("missing", [None, "", float("nan")])
def test_missing_comment(missing):
    assert coarse_locations(missing) == set()


def test_aa_composition():
    comp = aa_composition("AACx")
    assert comp.shape == (20,)
    assert comp[AMINO_ACIDS.index("A")] == pytest.approx(2 / 3)
    assert comp.sum() == pytest.approx(1)
    np.testing.assert_array_equal(comp >= 0, True)
    with pytest.raises(ValueError):
        aa_composition("XXX")
