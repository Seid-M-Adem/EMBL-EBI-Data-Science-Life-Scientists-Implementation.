import pandas as pd

from dsls.rag import (
    NOT_FOUND,
    HybridIndex,
    cited_accessions,
    evidence_overlap,
    is_abstention,
    rag_messages,
    uniprot_documents,
)

ENTRIES = pd.DataFrame(
    {
        "accession": ["P04637", "P42771", "P00533", "Q9XXX1"],
        "gene": ["TP53", "CDKN2A", "EGFR", None],
        "protein": [
            "Cellular tumor antigen p53 (Antigen NY-CO-13)",
            "Cyclin-dependent kinase inhibitor 2A",
            "Epidermal growth factor receptor (EC 2.7.10.1)",
            "Uncharacterized protein",
        ],  # fmt: skip
        "function": [
            "FUNCTION: Acts as a tumor suppressor {ECO:0000269|PubMed:123}. Interacts with CDKN2A (PubMed:456).",
            "FUNCTION: Acts as a negative regulator of cell proliferation {ECO:0000250}.",
            "FUNCTION: Receptor tyrosine kinase binding EGF ligands.",
            "FUNCTION: Unknown.",
        ],
    }
)


def test_uniprot_documents_cleans_and_drops():
    docs = uniprot_documents(ENTRIES)
    assert len(docs) == 3  # the entry without a gene symbol is dropped
    tp53 = docs.loc[docs["gene"] == "TP53", "text"].item()
    assert tp53 == ("UniProt P04637 | Gene: TP53 | Protein: Cellular tumor antigen p53 | Function: Acts as a tumor "
                    "suppressor. Interacts with CDKN2A.")  # fmt: skip


def test_identifier_boost_beats_keyword_confusion():
    docs = uniprot_documents(ENTRIES)
    index = HybridIndex(docs["text"], docs["gene"])
    # "CDKN2A" also appears in TP53's function text; the exact gene match must win
    assert index.search("What does CDKN2A do?", k=1) == [docs.index[docs["gene"] == "CDKN2A"][0]]
    assert index.search("what does cdkn2a do", k=1) == [1]  # case-insensitive
    assert index.search(
        "Which gene encodes the epidermal growth factor receptor?", k=1, use_identifiers=False
    ) == [2]
    assert len(index.search("tumor", k=3)) == 3


def test_rag_messages_numbers_evidence():
    msgs = rag_messages("What does TP53 do?", ["passage one", "passage two"])
    assert msgs[0]["role"] == "system" and NOT_FOUND in msgs[0]["content"]
    assert "[1] passage one\n[2] passage two" in msgs[1]["content"]
    assert msgs[1]["content"].endswith("Question: What does TP53 do?")
    assert rag_messages("q", ["p"], system="Be brief.")[0]["content"] == "Be brief."


def test_abstention_and_citations():
    assert is_abstention(NOT_FOUND)
    assert is_abstention("I'm sorry, but I cannot provide an answer.")
    assert is_abstention("The function of this gene is not yet determined.")
    assert not is_abstention("TP53 acts as a tumour suppressor [P04637].")
    assert cited_accessions("Tumour suppressor [P04637], inhibited by [P42771] and P04637 again.") == [
        "P04637",
        "P42771",
    ]
    assert cited_accessions("A0A087X1C5 and Q9Y6K9") == ["A0A087X1C5", "Q9Y6K9"]
    assert cited_accessions("no accessions here, TP53 or P53") == []


def test_evidence_overlap():
    passage = "Acts as a tumor suppressor in many tumor types; induces growth arrest or apoptosis."
    assert (
        evidence_overlap("It acts as a tumor suppressor in many tumor types.", passage) == 6 / 7
    )  # all but "it acts as a"
    assert evidence_overlap("Regulates insulin secretion in pancreatic beta cells.", passage) == 0.0
    assert evidence_overlap("Tumor suppressor.", passage) == 0.0  # shorter than n words
