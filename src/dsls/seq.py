"""Small, dependency-free sequence utilities: FASTA parsing, k-mers, composition and motif search.

Written for protein and nucleotide sequences alike; nothing here assumes an alphabet unless a function says so.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

#: The 20 standard amino acids (one-letter codes).
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

#: Kyte & Doolittle (1982) hydropathy scale.
KYTE_DOOLITTLE = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
    "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}  # fmt: skip

_UNIPROT_HEADER = re.compile(r"^(?P<db>sp|tr)\|(?P<accession>[^|]+)\|(?P<entry_name>\S+)\s*(?P<rest>.*)$")


@dataclass(frozen=True)
class Record:
    """One FASTA record. ``id`` is the first word of the header; ``description`` is the rest."""

    id: str
    description: str
    sequence: str

    @property
    def accession(self) -> str:
        """UniProt accession for ``sp|P29972|AQP1_HUMAN`` style IDs, otherwise the ID itself."""
        m = _UNIPROT_HEADER.match(f"{self.id} {self.description}")
        return m.group("accession") if m else self.id


def parse_fasta(source: str | Path | TextIO | Iterable[str]) -> Iterator[Record]:
    """Yield :class:`Record` objects from a path, an open file, a FASTA string, or an iterable of lines.

    Handles multi-line sequences, blank lines, Windows line endings and lower-case residues (upper-cased).
    Raises ``ValueError`` if sequence lines appear before the first header.
    """
    lines: Iterable[str]
    if isinstance(source, Path) or (
        isinstance(source, str) and "\n" not in source and source and Path(source).is_file()
    ):
        with open(source) as fh:
            yield from parse_fasta(fh.readlines())
        return
    lines = source.splitlines() if isinstance(source, str) else source

    header: str | None = None
    chunks: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                yield _record(header, chunks)
            header, chunks = line[1:].strip(), []
        elif header is None:
            raise ValueError(f"sequence data before the first '>' header: {line[:30]!r}")
        else:
            chunks.append(line.replace(" ", "").upper())
    if header is not None:
        yield _record(header, chunks)


def _record(header: str, chunks: list[str]) -> Record:
    ident, _, description = header.partition(" ")
    return Record(ident, description.strip(), "".join(chunks))


def kmers(seq: str, k: int) -> Iterator[str]:
    """All overlapping k-mers of ``seq`` (none if ``k`` exceeds the length)."""
    if k < 1:
        raise ValueError("k must be >= 1")
    return (seq[i : i + k] for i in range(len(seq) - k + 1))


def kmer_counts(seq: str, k: int, alphabet: str | None = None) -> Counter[str]:
    """Count overlapping k-mers. With ``alphabet``, k-mers containing other characters (e.g. ``X``) are skipped."""
    allowed = set(alphabet) if alphabet else None
    return Counter(km for km in kmers(seq, k) if allowed is None or set(km) <= allowed)


def composition(seq: str, alphabet: str = AMINO_ACIDS) -> dict[str, float]:
    """Fraction of each ``alphabet`` letter among the residues that belong to the alphabet (sums to 1)."""
    counts = Counter(c for c in seq if c in alphabet)
    total = sum(counts.values())
    return {a: (counts[a] / total if total else 0.0) for a in alphabet}


def gravy(seq: str) -> float:
    """Grand average of hydropathy (Kyte-Doolittle); non-standard residues are ignored."""
    values = [KYTE_DOOLITTLE[c] for c in seq if c in KYTE_DOOLITTLE]
    if not values:
        raise ValueError("sequence has no standard amino acids")
    return sum(values) / len(values)


def find_motif(seq: str, pattern: str) -> list[int]:
    """0-based start positions of a regex ``pattern``, *including overlapping matches*."""
    return [m.start() for m in re.finditer(f"(?=({pattern}))", seq)]
