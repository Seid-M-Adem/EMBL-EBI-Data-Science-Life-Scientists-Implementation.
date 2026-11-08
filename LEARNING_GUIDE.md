# Learning Guide: start here if you are new to biology, data science, or both

This repository follows EMBL-EBI's *Data Science for Life Scientists* course. The course assumes you already know
some biology **or** some programming. This guide is for people changing careers who have **neither**: for example a
software developer moving into bioinformatics, a lab scientist moving into data science, or a graduate from another field.

Every course session has a **`LESSONS.md`** file that explains its core ideas from first principles. This page gives
you the minimum background to read them, plus the route through the material.

---

## How to use this repository

| If you want to… | Read |
|-----------------|------|
| Understand a concept from scratch | the session's **`LESSONS.md`** (plain language, analogies, small code examples) |
| Look up an unfamiliar word | [`GLOSSARY.md`](GLOSSARY.md) |
| See what the official course covers | the session's **`README.md`** (summary of the EMBL-EBI material) |
| See the ideas applied to real data | the session's **`implementation/`** folder (my own analyses, with findings) |
| Run anything | [`RUNNING.md`](RUNNING.md) |

Each lesson has the same structure:

> **In one sentence** → **The idea in plain language** → **Background you need** → **What it looks like in code** →
> **Common mistakes** → **See it in this repository** → **Check yourself** → **Why it matters at work**

---

## The learning path

Work through the modules in order. Each one assumes the previous one.

| Step | Lessons | You will be able to… | Time* |
|------|---------|----------------------|-------|
| 1 | [01 · EMBL-EBI and public data](01_introduction_to_embl_ebi/LESSONS.md) | name the main biological databases and say what each one is for | 2 h |
| 2 | [02.1 · APIs and data collection](02_accessing_and_handling_data/01_apis_and_data_collection/LESSONS.md) | download data from a database with code instead of by clicking | 4 h |
| 3 | [02.2 · Handling and visualising data](02_accessing_and_handling_data/02_handling_and_visualisation/LESSONS.md) | clean a messy table and make honest plots with pandas and seaborn | 4 h |
| 4 | [03.1 · Machine learning fundamentals](03_foundations_of_machine_learning/01_intro_and_fundamentals/LESSONS.md) | frame a biological question as an ML problem and choose an algorithm | 4 h |
| 5 | [03.2 · Data, hyperparameters, performance](03_foundations_of_machine_learning/02_hyperparameters_and_performance/LESSONS.md) | train and evaluate a model without fooling yourself | 6 h |
| 6 | [04.1 · Neural networks and transformers](04_foundations_of_deep_learning/01_dnn_and_transformers/LESSONS.md) | explain how a neural network learns and why transformers work for sequences | 4 h |
| 7 | [04.2 · Evaluating deep learning models](04_foundations_of_deep_learning/02_evaluation_and_visualisation/LESSONS.md) | choose the right metric and analyse a model's errors | 3 h |
| 8 | [04.3 · Large language models](04_foundations_of_deep_learning/03_intro_to_llms/LESSONS.md) | use LLMs responsibly in scientific work | 2 h |
| 9 | Group projects: [gene expression](05_group_projects/gene_expression/LESSONS.md) · [bioimaging](05_group_projects/bioimaging/LESSONS.md) · [structural biology](05_group_projects/structural_biology/LESSONS.md) | apply everything to a realistic research question | 10 h+ |

\*Rough reading-and-running time, not counting the optional deep dives.

**Prerequisite:** basic Python (variables, lists, dictionaries, loops, functions). If you've never programmed, first
work through a free introductory course (for example the official [Python tutorial](https://docs.python.org/3/tutorial/))
and the PyLab challenges described in [02.2](02_accessing_and_handling_data/02_handling_and_visualisation/README.md).

---

## Biology in ten minutes

You don't need a biology degree to follow this course, but you do need the **central dogma** and a few words.

### Cells, DNA, genes
- Living things are made of **cells**. Each cell carries a full copy of the organism's **genome**: its **DNA**.
- DNA is a long string over a four-letter alphabet: **A, C, G, T** (nucleotides). The human genome is about
  3 billion letters long.
- A **gene** is a stretch of DNA that encodes a product, usually a protein. Humans have about 20,000 protein-coding
  genes. Genes have names such as *EGFR* or *TP53*.

### The central dogma: DNA → RNA → protein
```
DNA  (stored instructions)     ATG GCC TTA ...
  │  transcription
  ▼
RNA  (working copy)            AUG GCC UUA ...
  │  translation (3 letters = 1 amino acid)
  ▼
Protein (the machine)          M   A   L  ...
```
- **Transcription** copies a gene into **RNA**. How much RNA a cell makes from a gene is its **gene expression**.
  Measuring expression for every gene at once (**RNA-seq**) is one of the most common data types in biology. You'll
  meet it in the gene-expression project.
- **Translation** reads the RNA three letters at a time (**codons**) and builds a **protein**, a chain of 20 kinds of
  **amino acid** (one-letter codes such as M, A, L).
- A protein **folds** into a 3-D shape, and the shape determines what it does: enzymes speed up reactions, receptors
  sense signals, channels let molecules through membranes. Protein shapes are measured experimentally (**X-ray
  crystallography**, **cryo-EM**) and stored in the **PDB**; since 2021 they can also be predicted (**AlphaFold**).

### Variation, disease and drugs
- A **mutation** is a change in DNA. In a protein-coding gene it can change one amino acid. For example, **L858R** in
  EGFR means the amino acid at position 858 changed from leucine (L) to arginine (R).
- Some mutations drive disease. Mutated EGFR, for instance, drives some lung cancers.
- A **drug** is often a small molecule that binds a protein (its **target**) and changes its activity. **Potency** is
  how little drug you need. It is measured as an **IC50** (the concentration that halves the target's activity):
  lower IC50 means a more potent drug.

### Where the data come from
- **Sequencing** machines read DNA or RNA and produce **reads** (short pieces of sequence), stored in archives such as
  **ENA**.
- **Microscopes** produce images of cells (bioimaging project).
- **Assays** measure biological activity, such as a drug's IC50, and are collected in databases like **ChEMBL**.
- Every record gets a stable ID, its **accession** (e.g. UniProt `P00533`). Accessions are how you join data across
  databases.

---

## Data science in ten minutes

### The workflow
```
question → get data → clean data → explore (plots, summaries) → model → evaluate → interpret → communicate
```
Most of the time goes into **getting and cleaning data**, not modelling. This repository reflects that: module 02 is
about data, and every analysis records its cleaning decisions.

### Tables are the core data structure
Almost everything becomes a **table** (a pandas **DataFrame**): one row per *thing* (a protein, a patient, an image) and
one column per *measurement* (length, age, a gene's expression). In machine learning:
- the measurements are **features** (written `X`),
- the thing you want to predict is the **label** or **target** (written `y`).

### Machine learning in one paragraph
A **model** is a function with adjustable settings (**parameters**). **Training** adjusts the parameters so the model's
outputs match known answers on **training data**. The real test is new data the model has never seen: the **test set**.
A model that memorises its training data but fails on new data is **overfitting**, the most common way to fool yourself
in this field. Modules 03 and 04 are largely about avoiding that.

### Three habits that make your work professional
1. **Reproducibility:** code, not clicking; fixed random seeds; recorded data versions.
2. **Honest evaluation:** test on data the model has never seen, and pick metrics that fit the problem.
3. **Explain your decisions:** every filter, threshold and exclusion is written down with its reason and its effect.

---

## Career notes: what this material maps to

| Skill in this repo | Typical job-description wording |
|--------------------|---------------------------------|
| Programmatic data access (02.1) | "experience with public biological databases / REST APIs" |
| pandas cleaning, tidy data, seaborn (02.2) | "data wrangling", "exploratory data analysis", "data visualisation" |
| scikit-learn pipelines, cross-validation (03) | "machine learning model development and validation" |
| PyTorch, transformers, fine-tuning (04) | "deep learning", "NLP / foundation models" |
| Unit tests, CI, packaging (`src/dsls`, `tests/`) | "software engineering best practices", "version control, testing" |
| FAIR, provenance, licensing ([`FAIR.md`](01_introduction_to_embl_ebi/implementation/FAIR.md)) | "reproducible research", "data stewardship" |

The most useful habit to build is **writing down what you did and why**, the way the *Findings* sections of the
notebooks in this repository do.
