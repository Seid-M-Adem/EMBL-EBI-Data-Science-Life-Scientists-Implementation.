"""A minimal retrieval-augmented generation (RAG) toolkit over UniProt entries. No LLM inside: bring your own.

* ``uniprot_documents`` – one short, citable text passage per UniProt entry (evidence tags and PubMed ids removed)
* ``HybridIndex`` – search: exact identifier match (e.g. a gene symbol in the question) first, then TF-IDF keywords
* ``rag_messages`` – the chat prompt: numbered evidence passages, instructions to cite and to abstain
* ``is_abstention`` / ``cited_accessions`` – grade answers: did the model decline, and what did it cite?
* ``evidence_overlap`` – how much of an answer is copied from a passage (a cheap groundedness check)
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

TOKEN = r"[A-Za-z0-9-]+"
ACCESSION = re.compile(r"\b(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})\b")
NOT_FOUND = "Not found in UniProt."

SYSTEM_PROMPT = (
    "You answer questions about human proteins using only the UniProt entries provided. "
    "After each fact, cite the entry's accession in square brackets, e.g. [P04637]. "
    f"If the entries do not contain the answer, reply exactly: {NOT_FOUND}"
)


def _clean_function(text: str) -> str:
    text = re.sub(r"^FUNCTION:\s*", "", text)
    text = re.sub(r"\s*\{ECO:[^}]*\}", "", text)  # evidence codes
    text = re.sub(r"\s*\((?:PubMed|Ref\.)[^)]*\)", "", text)  # literature references
    return re.sub(r"\s+", " ", text).strip()


def uniprot_documents(entries: pd.DataFrame, max_function_chars: int = 500) -> pd.DataFrame:
    """Turn UniProt rows (columns ``accession, gene, protein, function``) into citable passages.

    Rows without a gene symbol or function text are dropped; the protein name keeps only its first (recommended) form.
    """
    docs = entries.dropna(subset=["gene", "function"]).copy()
    docs["protein"] = docs["protein"].str.split(" \\(").str[0]
    docs["function"] = docs["function"].map(_clean_function).str[:max_function_chars]
    docs["text"] = (
        "UniProt " + docs["accession"] + " | Gene: " + docs["gene"] + " | Protein: " + docs["protein"]
        + " | Function: " + docs["function"]
    )  # fmt: skip
    return docs.reset_index(drop=True)


class HybridIndex:
    """Keyword (TF-IDF) search with an exact-identifier boost.

    Neural sentence embeddings split identifiers such as "CDKN2A" into meaningless fragments; an exact match on a
    structured field is far more reliable. If a word in the query equals a known identifier (case-insensitive), that
    document is ranked first; the rest are ordered by TF-IDF similarity.
    """

    def __init__(self, texts, identifiers=None, boost: float = 10.0):
        self.vectorizer = TfidfVectorizer(sublinear_tf=True, token_pattern=TOKEN)
        self.matrix = self.vectorizer.fit_transform(list(texts))
        self.boost = boost
        self.ids: dict[str, list[int]] = {}
        for i, ident in enumerate(identifiers if identifiers is not None else []):
            self.ids.setdefault(str(ident).upper(), []).append(i)

    def scores(self, query: str, use_identifiers: bool = True) -> np.ndarray:
        s = (self.vectorizer.transform([query]) @ self.matrix.T).toarray().ravel()
        if use_identifiers:
            for word in re.findall(TOKEN, query):
                for i in self.ids.get(word.upper(), []):
                    s[i] += self.boost
        return s

    def search(self, query: str, k: int = 3, use_identifiers: bool = True) -> list[int]:
        s = self.scores(query, use_identifiers)
        top = np.argpartition(-s, min(k, len(s) - 1))[:k]
        return [int(i) for i in top[np.argsort(-s[top], kind="stable")]]


def rag_messages(question: str, passages: list[str], system: str = SYSTEM_PROMPT) -> list[dict]:
    """Chat messages for an instruction-tuned LLM: system rules, then numbered evidence and the question."""
    evidence = "\n".join(f"[{n}] {p}" for n, p in enumerate(passages, 1))
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"UniProt entries:\n{evidence}\n\nQuestion: {question}"},
    ]


_ABSTAIN = re.compile(
    r"not found|cannot (?:provide|find|answer)|no (?:specific |available )?information|"
    r"(?:not|no longer) (?:yet )?(?:known|determined|available|characteri[sz]ed)|unknown|not aware|sorry",
    re.I,
)


def is_abstention(answer: str) -> bool:
    """True if the answer declines (e.g. "Not found in UniProt.", "I'm sorry, I cannot…") rather than asserting."""
    return bool(_ABSTAIN.search(answer))


def cited_accessions(answer: str) -> list[str]:
    """UniProt accessions mentioned in an answer, in order of first appearance."""
    return list(dict.fromkeys(ACCESSION.findall(answer)))


def _ngrams(text: str, n: int) -> set[tuple[str, ...]]:
    words = [w.lower() for w in re.findall(TOKEN, text)]
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def evidence_overlap(answer: str, passage: str, n: int = 4) -> float:
    """Share of the answer's word n-grams that also occur in the passage (0 = nothing copied, 1 = all copied).

    High overlap means the answer restates the passage; it does not prove the answer is correct or complete. Answers
    shorter than ``n`` words return 0.
    """
    a = _ngrams(answer, n)
    return len(a & _ngrams(passage, n)) / len(a) if a else 0.0
