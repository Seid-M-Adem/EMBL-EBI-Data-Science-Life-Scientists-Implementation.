# 04.3 · Intro to LLMs

> **Status:** ✅ Implementation complete (3 / 3 tasks) · **Trainer:** Luigi Sigillo (Postdoctoral Fellow, Petroni Lab, EMBL Rome) ·
> **Course page:** [Introduction to Large Language Models](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-deep-learning-dl/introduction-to-large-language-models/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

*From next-token prediction to reasoning and agentic AI.* A conceptual lecture on what happens inside an LLM,
how a raw model becomes an assistant, why LLMs hallucinate, and how to use them **reliably** in scientific work.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Intro_to_LLMs.pdf`](course_materials/Intro_to_LLMs.pdf) (39 slides)
| Act | Topic | Highlights |
|-----|-------|-----------|
| I | **The core task** | Predicting the next token as a probability distribution; **tokens** are sub-word chunks (e.g. how *"TP53 regulates the cell cycle"* is split), so character-level tasks can fail |
| II | **Transformers** | Intuition for attention; *Attention Is All You Need* (2017); encoder (BERT) vs. decoder (GPT/Llama) blocks |
| III | **Inside a modern LLM** | Text → token IDs → embeddings → repeated (attention + MLP) blocks → logits → sampling; where knowledge "lives" |
| IV | **From base model to assistant** | **Pre-training** at scale (Common Crawl → FineWeb data curation) → **instruction tuning (SFT)** and few-shot prompting → **post-training** (SFT, preference training for helpfulness and safety, verifier training for maths, code and tool use); **test-time compute** in reasoning models |
| V | **Capability ≠ reliability** | Benchmarks are proxies; **benchmark contamination**; **hallucination is structural** (compressed statistical memory, rewarded for plausibility) |
| — | **Grounding and agents** | Parametric vs. external memory; **RAG** (retrieve evidence, then answer); **agents** = LLM + harness (observe → plan → act → check) + tools; agent safety; scientific tool calls (e.g. `get_protein_interactions("TP53")`) |
| — | **Practical takeaways** | Prompting as *context engineering*; draft → ground → verify; five take-home messages and a cheat-sheet |

## 🧠 Key Concepts
- **Tokenisation:** models see sub-word IDs, not letters, which matters for gene names and sequences.
- **Pre-training → instruction tuning → post-training:** the three stages from a text predictor to a helpful assistant.
- **Hallucination:** fluent but unsupported output. Reduce it by grounding in retrieved evidence.
- **RAG:** retrieval-augmented generation, i.e. answering from fetched documents rather than from memory.
- **Agent:** an LLM in a loop that can call tools (databases, code runners) and check the results.

## 🛠️ My Implementation
See [`implementation/`](implementation/). Both notebooks explain each step in plain language for readers new to the field.
- [x] Tokeniser exploration: how general, biomedical and protein tokenisers split all 20,188 human gene symbols, DNA and protein sequences, plus next-token prediction, temperature and a letter-counting test → [notebook 01](implementation/01_tokens_genes_dna_proteins.ipynb)
- [x] Protein language model embeddings (ESM-2) → UMAP plus classifiers for subcellular location: done in module 04.1 → [04.1 notebook 03](../01_dnn_and_transformers/implementation/03_esm2_protein_localisation.ipynb)
- [x] Minimal RAG over UniProt with retrieval comparison, graded answers, abstention on made-up genes and source checking → [notebook 02](implementation/02_rag_over_uniprot.ipynb), reusable code in [`src/dsls/rag.py`](../../src/dsls/rag.py) (5 tests)

## 📝 Notes & Reflections
- **Fluency is not knowledge.** Asked for TP53's UniProt accession, the model had no confident next token but would
  still write one; closed-book, it got 0 of 100 accessions right and invented functions for 13 of 20 made-up genes.
- **The tokeniser decides what the model can see.** Gene symbols are shredded into fragments by general tokenisers,
  whole sequences become one `[UNK]` in BERT-style models, and the same DNA motif splits differently depending on its
  neighbours. Checking the tokenised input is a cheap first step for any biological text.
- **Retrieval is the part to get right first.** The popular neural-embedding search found the right gene's entry 18 %
  of the time; an exact-match rule reached 100 %. Grading retrieval separately from generation showed where each
  error came from.
- **Prompts need testing like code.** My own example accession in the instructions caused 17 of 18 errors on one test,
  and no single wording was best on both tests. I reported the trade-off instead of choosing the best result after
  seeing the test scores.
- **Don't rely on a small model to cite.** It never did, but the system can attach sources itself: every answer was
  traceable to the correct entry by word overlap.
