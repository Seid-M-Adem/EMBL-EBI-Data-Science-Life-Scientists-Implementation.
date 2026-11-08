"""Helpers for protein-sequence machine learning.

* ``coarse_locations`` – turn UniProt's free-text "Subcellular location" comment into a few broad compartments,
  optionally keeping only experimentally supported statements
* ``aa_composition`` – the classic 20-number baseline: the fraction of each amino acid in a sequence
"""

from __future__ import annotations

import re
from collections import Counter

import numpy as np

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"
# Evidence & Conclusion Ontology code for "experimental evidence used in manual assertion"
EXPERIMENTAL = "ECO:0000269"

# UniProt location terms → broad compartment, matched on the term's main part (text before the first comma).
COMPARTMENTS = {
    "Nucleus": "nucleus",
    "Cytoplasm": "cytoplasm",
    "Cytosol": "cytoplasm",
    "Mitochondrion": "mitochondrion",
    "Secreted": "secreted",
    "Cell membrane": "cell membrane",
    "Endoplasmic reticulum": "endoplasmic reticulum",
    "Golgi apparatus": "Golgi apparatus",
}

_TERM = re.compile(r"([A-Z][^.;{}]*?)\s*\{([^}]*)\}")
_NOTE = re.compile(r"Note=.*?(?=SUBCELLULAR LOCATION:|$)", re.S)
_ISOFORM = re.compile(r"\[[^\]]*\]:\s*")


def coarse_locations(comment: str | None, experimental_only: bool = True) -> set[str]:
    """Broad compartments named in a UniProt ``cc_subcellular_location`` text.

    Free-text notes (``Note=...``) are ignored. A term counts only if it carries an evidence tag, and, with
    ``experimental_only``, only if that tag includes direct experimental evidence (ECO:0000269).

    >>> sorted(coarse_locations("SUBCELLULAR LOCATION: Nucleus {ECO:0000269}. Cytoplasm {ECO:0000250}."))
    ['nucleus']
    """
    if not comment or not isinstance(comment, str):
        return set()
    text = _ISOFORM.sub("", _NOTE.sub("", comment))
    found = set()
    for term, evidence in _TERM.findall(text):
        term = term.replace("SUBCELLULAR LOCATION:", "").strip()
        if experimental_only and EXPERIMENTAL not in evidence:
            continue
        main = term.split(",")[0].strip()
        for prefix, compartment in COMPARTMENTS.items():
            if main == prefix or main.startswith(prefix + " "):
                found.add(compartment)
                break
    return found


def aa_composition(sequence: str) -> np.ndarray:
    """Fraction of each of the 20 standard amino acids (order: ``AMINO_ACIDS``); other letters are ignored."""
    counts = Counter(sequence.upper())
    total = sum(counts[a] for a in AMINO_ACIDS)
    if total == 0:
        raise ValueError("sequence contains no standard amino acids")
    return np.array([counts[a] / total for a in AMINO_ACIDS], dtype=np.float32)
