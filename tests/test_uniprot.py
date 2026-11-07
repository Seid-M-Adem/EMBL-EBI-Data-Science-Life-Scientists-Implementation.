"""Tests for dsls.uniprot (offline; the entry below is a trimmed copy of UniProt's JSON shape)."""

from dsls.uniprot import entry_to_record, protein_name, taxonomic_group

ENTRY = {
    "primaryAccession": "P29972",
    "uniProtkbId": "AQP1_HUMAN",
    "annotationScore": 5.0,
    "organism": {"scientificName": "Homo sapiens", "taxonId": 9606, "lineage": ["Eukaryota", "Metazoa"]},
    "proteinDescription": {"recommendedName": {"fullName": {"value": "Aquaporin-1"}}},
    "genes": [{"geneName": {"value": "AQP1"}}],
    "comments": [
        {
            "commentType": "SUBCELLULAR LOCATION",
            "subcellularLocations": [
                {"location": {"value": "Cell membrane"}},
                {"location": {"value": "Apical cell membrane"}},
                {"topology": {"value": "Multi-pass membrane protein"}},  # no location key
            ],
        }
    ],
    "features": [
        *[{"type": "Transmembrane"} for _ in range(6)],
        {"type": "Motif", "description": "NPA 1"},
        {"type": "Motif", "description": "NPA 2"},
    ],
    "uniProtKBCrossReferences": [
        {"database": "PDB", "id": "1FQY", "properties": [{"key": "Resolution", "value": "3.80 A"}]},
        {"database": "PDB", "id": "1H6I", "properties": [{"key": "Resolution", "value": "3.54 A"}]},
        {"database": "PDB", "id": "XXXX", "properties": [{"key": "Resolution", "value": "-"}]},  # NMR
        {"database": "EMBL", "id": "M77829"},
    ],
    "sequence": {"length": 269},
}


def test_entry_to_record_human_aqp1():
    r = entry_to_record(ENTRY)
    assert r["accession"] == "P29972" and r["gene"] == "AQP1" and r["protein_name"] == "Aquaporin-1"
    assert r["group"] == "Animals" and r["length"] == 269 and r["is_fragment"] is False
    assert r["n_transmembrane"] == 6 and r["n_npa"] == 2 and r["motifs"] == "NPA;NPA"
    assert r["n_pdb"] == 3 and r["best_resolution_A"] == 3.54
    assert r["subcellular_locations"] == "Apical cell membrane; Cell membrane"


def test_non_canonical_motif_and_missing_sections():
    entry = {
        "primaryAccession": "Q0",
        "organism": {"lineage": ["Bacteria", "Pseudomonadati"]},
        "proteinDescription": {
            "submissionNames": [{"fullName": {"value": "Putative aquaporin"}}],
            "flag": "Fragment",
        },
        "features": [{"type": "Motif", "description": "NPC"}, {"type": "Motif", "description": "NPA 2"}],
    }
    r = entry_to_record(entry)
    assert r["motifs"] == "NPC;NPA" and r["n_npa"] == 1
    assert r["group"] == "Bacteria" and r["protein_name"] == "Putative aquaporin" and r["is_fragment"]
    assert r["gene"] is None and r["n_pdb"] == 0 and r["best_resolution_A"] is None


def test_taxonomic_group():
    assert taxonomic_group(["Eukaryota", "Viridiplantae", "Streptophyta"]) == "Plants"
    assert taxonomic_group(["Eukaryota", "Sar"]) == "Other eukaryotes"
    assert taxonomic_group(["Archaea"]) == "Archaea"
    assert taxonomic_group([]) == "Unknown"


def test_protein_name_absent():
    assert protein_name({}) is None
