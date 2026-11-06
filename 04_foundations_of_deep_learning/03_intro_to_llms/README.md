# 04.3 · Intro to LLMs

> **Status:** ⚪ Not started · **Trainer:** Luigi Sigillo (Postdoctoral Fellow, Petroni Lab, EMBL Rome) ·
> **Course page:** [Introduction to Large Language Models](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-deep-learning-dl/introduction-to-large-language-models/)

## Overview
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

## 🛠️ My Implementation (planned)
- [ ] Tokeniser exploration: how general vs. biomedical tokenisers split gene names, DNA and protein sequences
- [ ] Protein language model embeddings (e.g. ESM-2) → UMAP plus a simple classifier on a protein property
- [ ] Minimal RAG demo over UniProt entries, with citation of the retrieved evidence

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
