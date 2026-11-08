# 04.3 · Lessons explained: large language models (LLMs) in science

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** what happens inside an LLM, how a raw text predictor becomes an assistant, why LLMs
make things up, and how to use them **reliably** in scientific work.

---

## Lesson 1 · The core task: predict the next token

**In one sentence:** an LLM is trained to predict the next **token** (a piece of a word) given all the previous ones,
and everything it does emerges from doing that task at enormous scale.

**Tokens are not letters or whole words.** A tokenizer splits text into frequent sub-word chunks:
```
"TP53 regulates the cell cycle" → ["TP", "53", " regulates", " the", " cell", " cycle"]   (illustrative)
```
**Consequence:** tasks that need individual characters (counting letters, reversing a DNA sequence, spotting a single
amino-acid change in a long protein) can fail, because the model never "sees" individual letters. Gene names and
sequences get chopped in unexpected places.

**Generation:** the model outputs a probability for every possible next token, one is **sampled**, appended, and the
process repeats. **Temperature** controls randomness: low gives predictable output, high gives more varied output.

---

## Lesson 2 · Inside the model (the short version)

```
text → token IDs → embeddings (vectors) → [attention + MLP] × many layers → scores for every next token → sample
```
- **Embeddings** turn each token into a vector of numbers.
- **Attention** layers mix information between positions (see [04.1](../01_dnn_and_transformers/LESSONS.md)).
- **MLP** layers transform each position, and much factual association is thought to be stored here.
- Modern assistants (GPT-style) are **decoder** transformers: they only look backwards, which suits generation.

---

## Lesson 3 · From base model to assistant: three training stages

| Stage | Data | Result |
|-------|------|--------|
| **Pre-training** | trillions of tokens of curated web text, books, code | a *base model*: good at continuing text, not at following instructions |
| **Instruction tuning (SFT)** | example conversations: instruction → good answer | follows requests in a helpful format |
| **Post-training / preference training** | human or AI preference judgements; verifiable tasks (maths, code, tool use) | more helpful, safer, better at reasoning |

**Reasoning models** additionally spend extra computation at answer time ("test-time compute"), working through
intermediate steps before answering.

---

## Lesson 4 · Capability is not reliability: hallucination

**In one sentence:** LLMs can produce fluent, confident, **wrong** statements, because they are trained to produce
*plausible* text, not to look up facts.

- A model's "knowledge" is a compressed statistical memory of its training data, not a database. Rare facts (a specific
  gene's binding partner, an exact IC50) are the most likely to be wrong.
- **Fabricated citations** are a well-known failure: a reference that looks right but doesn't exist.
- **Benchmarks are proxies:** high scores don't guarantee correctness on your question, and benchmark questions may
  have leaked into training data (**contamination**).

**Professional rule:** treat LLM output as a **draft from a fast but unreliable assistant**. Verify every factual claim
against a primary source (UniProt, ChEMBL, the paper itself).

---

## Lesson 5 · Grounding: retrieval-augmented generation (RAG)

**In one sentence:** **RAG** first *retrieves* relevant documents (from a database or literature search) and then asks
the model to answer *from those documents*, citing them.

```
question → search (e.g. UniProt, Europe PMC) → top passages → LLM: "answer using only these; cite them" → answer + citations
```
- It reduces hallucination because the evidence is in front of the model.
- It makes answers **checkable**: each claim points to a source you can read.
- It doesn't eliminate errors. The model can still misread a source, and retrieval can miss the right document.

---

## Lesson 6 · Agents and tools

**In one sentence:** an **agent** is an LLM in a loop that can **call tools** (search a database, run code, query an
API), observe the result, and decide the next step.

```
observe → plan → act (call a tool, e.g. get_protein_interactions("TP53")) → check the result → repeat or answer
```
Agents can automate multi-step tasks, such as finding a protein's structures, fetching its ligands and summarising
them. They also need safeguards: limited permissions, human approval for consequential actions, and checks on every
tool output.

---

## Lesson 7 · Using LLMs well in scientific work

1. **Context engineering:** give the model the relevant material (data definitions, the paper, your code) rather than
   relying on its memory.
2. **Draft → ground → verify:** let it draft, ground claims in retrieved evidence, then verify yourself.
3. **Use it where checking is cheap:** code (you can run it and test it), summaries of documents you provide,
   reformatting. Be most cautious where checking is expensive, such as novel factual claims.
4. **Record what you used:** model, version, prompt, date. This is part of reproducibility.
5. **Protect data:** don't paste confidential or patient data into external services without approval.

**Why it matters at work:** organisations are adopting LLMs quickly, and people who can use them productively *and*
explain their failure modes and safeguards are in demand.
