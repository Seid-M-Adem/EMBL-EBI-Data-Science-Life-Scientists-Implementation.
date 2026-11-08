# 04.1 · Lessons explained: neural networks and transformers

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** how a neural network learns, and why **transformers** (the architecture behind modern
language models and protein models) work so well for sequences. The practical compares a classical text classifier
with a fine-tuned biomedical transformer.

---

## Background · The practical task in plain language

Scientific abstracts follow a structure: **background, objective, methods, results, conclusions**. The **PubMed RCT**
dataset labels each sentence of thousands of clinical-trial abstracts with its role. The task is to **read a sentence
and predict which of the five sections it belongs to**. Tools that do this help researchers skim and mine the
literature.

---

## Lesson 1 · From features we design to features the model learns

**In one sentence:** in classical ML, humans design the features; in deep learning, the network **learns its own
features** from raw input.

**The idea in plain language.** For the abstract task, a classical approach counts words (**TF-IDF** gives each word a
weight: high if it's frequent in this sentence but rare overall). A deep model instead learns which patterns of words,
in which order and context, are informative. That flexibility needs more data and computation, but it can capture what
word counts miss, such as "*not* significant".

---

## Lesson 2 · The artificial neuron and the network

**In one sentence:** a neuron computes a weighted sum of its inputs, adds a bias, and passes the result through a
non-linear **activation function**. Layers of neurons stacked together form a network.

```
inputs x1, x2, x3 ──► w1·x1 + w2·x2 + w3·x3 + b ──► activation ──► output
```

| Activation | Shape | Typical use |
|------------|-------|-------------|
| **ReLU** | 0 for negatives, the identity for positives | hidden layers (default choice) |
| **Sigmoid** | squashes to 0–1 | binary output probability |
| **Softmax** | turns a vector into probabilities that sum to 1 | multi-class output (our five sections) |
| tanh | squashes to −1…1 | older recurrent networks |

**Why non-linearity matters:** without it, any number of stacked layers would collapse into one linear function. The
activation is what lets networks model curved, complex relationships.

---

## Lesson 3 · How a network learns: the training loop

**In one sentence:** show examples, measure how wrong the outputs are (**loss**), work out how each weight contributed to
the error (**backpropagation**), nudge every weight to reduce it (**optimiser**), and repeat.

```python
for epoch in range(n_epochs):              # one epoch = one pass over the training data
    for X_batch, y_batch in train_loader:
        logits = model(X_batch)            # 1. forward pass
        loss = loss_fn(logits, y_batch)    # 2. how wrong? (cross-entropy for classification)
        optimizer.zero_grad()
        loss.backward()                    # 3. backpropagation: gradient of loss for every weight
        optimizer.step()                   # 4. update weights a small step downhill
```
**Analogy:** walking down a foggy hill to the valley floor. You can only feel the slope underfoot (the **gradient**),
so you take a step downhill (sized by the **learning rate**), feel again, and repeat. Too big a step and you overshoot;
too small and you never arrive.

**Key words:** *batch* (a few examples processed together), *epoch* (one full pass), *learning rate* (step size),
*early stopping* (stop when validation performance stops improving, to avoid overfitting).

---

## Lesson 4 · Architectures for different data

| Data | Architecture | Why |
|------|--------------|-----|
| Fixed-length feature vectors | **feed-forward network / MLP** | general purpose |
| Images | **CNN** (convolutional) | learns local patterns (edges → shapes → objects) that can appear anywhere |
| Sequences (older approach) | **RNN / LSTM** | reads one token at a time, carrying a memory |
| Sequences (modern) | **Transformer** | looks at all positions at once with attention (Lesson 5) |

---

## Lesson 5 · Transformers and self-attention

**In one sentence:** **self-attention** lets every word (token) in a sequence look at every other word and decide which
ones matter for its meaning, so each word's representation depends on its context.

**The idea in plain language.** "The dog bit the man" and "the man bit the dog" contain the same words, so word counts
can't tell them apart. In biomedical text, context decides whether "EGFR" is a gene, a protein or a test result. In
self-attention, each token asks a **query** ("what am I looking for?"), every token offers a **key** ("what do I
contain?") and a **value** ("what information do I pass on?"). Tokens whose keys match the query get more weight.

- **Encoder models (BERT-style)** read the whole sentence in both directions. They suit classification and tagging.
  **PubMedBERT** is a BERT pre-trained on PubMed abstracts, so it already "knows" biomedical language.
- **Decoder models (GPT-style)** predict the next token from the previous ones, and they suit text generation
  (module 04.3).

The same idea works on **protein sequences**: protein language models treat amino acids as tokens.

---

## Lesson 6 · Pre-training and fine-tuning

**In one sentence:** **pre-training** teaches a big model general patterns from huge unlabelled data; **fine-tuning**
adapts it to your specific task with a small labelled dataset.

**Analogy:** a medical graduate (pre-trained on years of general study) becomes a radiologist with focused specialist
training (fine-tuning). It is much faster than training a radiologist from birth.

**In the practical:** PubMedBERT plus a small classification head, fine-tuned for 3 epochs on 8,000 sentences:

| Model | Test accuracy | Macro-F1 | Training time (Apple-silicon laptop) |
|-------|---------------|----------|----------------------------------------|
| TF-IDF → SVD → MLP | 0.635 | 0.535 | 14 s |
| PubMedBERT fine-tuned | **0.853** | **0.790** | 3 h 15 min (minutes on a cloud GPU) |

**Lessons from this result:**
- Pre-trained context-aware models beat word counts by a large margin on this task.
- The cost is computation, so **always train a cheap baseline first**. It tells you how much the expensive model adds.
- Macro-F1 is lower than accuracy for both models because some sections (e.g. "objective") are rarer and harder.
  Module 04.2 explains why that matters.

**Why it matters at work:** "fine-tune a pre-trained model on domain data and compare it against a baseline" is one of
the most common real-world deep-learning tasks in industry and research.
