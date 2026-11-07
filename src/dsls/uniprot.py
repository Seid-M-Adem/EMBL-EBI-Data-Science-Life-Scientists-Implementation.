"""Turn UniProtKB JSON entries into flat, analysis-ready records."""

from __future__ import annotations

import re
from typing import Any

#: Fields requested from the UniProt REST API for :func:`entry_to_record`.
FIELDS = (
    "accession,id,protein_name,gene_primary,organism_name,organism_id,lineage,length,"
    "ft_transmem,ft_motif,xref_pdb,annotation_score,cc_subcellular_location"
)

_EUKARYOTE_GROUPS = {"Viridiplantae": "Plants", "Metazoa": "Animals", "Fungi": "Fungi"}
_RESOLUTION = re.compile(r"([\d.]+)\s*A")


def taxonomic_group(lineage: list[str]) -> str:
    """Coarse group from a UniProt lineage: Plants, Animals, Fungi, Other eukaryotes, Bacteria, Archaea, Viruses."""
    if not lineage:
        return "Unknown"
    if lineage[0] == "Eukaryota":
        return _EUKARYOTE_GROUPS.get(lineage[1] if len(lineage) > 1 else "", "Other eukaryotes")
    return lineage[0]


def protein_name(entry: dict[str, Any]) -> str | None:
    desc = entry.get("proteinDescription", {})
    for key in ("recommendedName", "submissionNames"):
        node = desc.get(key)
        if isinstance(node, list):
            node = node[0] if node else None
        if node:
            return node["fullName"]["value"]
    return None


def entry_to_record(entry: dict[str, Any]) -> dict[str, Any]:
    """Flatten one UniProtKB entry (requested with :data:`FIELDS`) into a dict of scalar columns."""
    features = entry.get("features", [])
    motifs = [f.get("description") or "" for f in features if f["type"] == "Motif"]
    pdb = [x for x in entry.get("uniProtKBCrossReferences", []) if x["database"] == "PDB"]
    resolutions = [
        float(m.group(1))
        for x in pdb
        for p in x.get("properties", [])
        if p["key"] == "Resolution" and (m := _RESOLUTION.search(p["value"]))
    ]
    locations = sorted(
        {
            loc["location"]["value"]
            for c in entry.get("comments", [])
            if c.get("commentType") == "SUBCELLULAR LOCATION"
            for loc in c.get("subcellularLocations", [])
            if "location" in loc
        }
    )
    organism = entry.get("organism", {})
    genes = entry.get("genes") or [{}]
    return {
        "accession": entry["primaryAccession"],
        "entry_name": entry.get("uniProtkbId"),
        "protein_name": protein_name(entry),
        "gene": genes[0].get("geneName", {}).get("value"),
        "organism": organism.get("scientificName"),
        "taxon_id": organism.get("taxonId"),
        "group": taxonomic_group(organism.get("lineage", [])),
        "length": entry.get("sequence", {}).get("length"),
        # UniProt sets proteinDescription.flag to "Fragment" / "Fragments" for incomplete sequences
        "is_fragment": entry.get("proteinDescription", {}).get("flag", "").startswith("Fragment"),
        "n_transmembrane": sum(f["type"] == "Transmembrane" for f in features),
        "motifs": ";".join(m.split()[0] for m in motifs if m) or None,
        "n_npa": sum(m.startswith("NPA") for m in motifs),
        "n_pdb": len(pdb),
        "best_resolution_A": min(resolutions) if resolutions else None,
        "annotation_score": entry.get("annotationScore"),
        "subcellular_locations": "; ".join(locations) or None,
    }
