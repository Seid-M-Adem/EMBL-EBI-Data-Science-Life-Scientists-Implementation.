<div align="center">

# 🧬 Data Science for Life Scientists — Proof of Learning

**Independent On-Demand Implementation of the EMBL-EBI Curriculum**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![License](https://img.shields.io/badge/license-MIT%20(own%20work)-blue)
[![CI](https://github.com/Seid-M-Adem/EMBL-EBI-Data-Science-Life-Scientists-Implementation./actions/workflows/lint.yml/badge.svg)](https://github.com/Seid-M-Adem/EMBL-EBI-Data-Science-Life-Scientists-Implementation./actions/workflows/lint.yml)

</div>

---

## 📌 Course Overview

This repository is an **Independent On-Demand Implementation of the EMBL-EBI Curriculum** for
[*Data Science for Life Scientists*](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/)
(2026 edition), delivered by the European Bioinformatics Institute (EMBL-EBI).

The course goes from **programmatic access to public biological databases**, through **classical machine learning**,
to **deep learning and large language models**, and ends with three applied projects in **gene expression**,
**structural biology** and **bioimaging**. For each module I study the official materials, then **re-implement the
ideas myself** as clean, documented, reproducible code, with a write-up of what I learned.

> **Disclaimer:** This is a personal learning portfolio. It is not affiliated with, or endorsed
> by, EMBL-EBI. Course materials are credited to their original authors. See [COURSE_MATERIALS.md](COURSE_MATERIALS.md).

---

## 🛠️ Technologies Used

| Area | Tools |
|------|-------|
| **Language** | Python 3.11+ |
| **Data Handling** | Pandas, NumPy, PyArrow (Parquet), pyreadr (R `.RDS`) |
| **Visualisation** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | Scikit-learn, XGBoost, imbalanced-learn, UMAP |
| **Deep Learning** | PyTorch, Hugging Face Transformers / Datasets |
| **Bioinformatics** | Biopython, pycytominer |
| **Biological APIs** | MGnify, ENA, UniProt, ChEMBL (EMBL-EBI REST services) via `requests` |
| **Environment** | Jupyter, `venv`, Ruff, GitHub Actions |

---

## 🎯 Core Skills Demonstrated

- **Data Preprocessing:** retrieving, cleaning, normalising and reshaping varied biological datasets (omics, morphology profiles, crystallography metrics, text).
- **Reproducible Pipelines:** pinned environments, fixed seeds, separate raw and processed data, and a one-command data fetch.
- **ML/DL Evaluation:** stratified splits, cross-validation, hyperparameter tuning, learning curves, confusion matrices, and metrics chosen for imbalanced data.
- **Programmatic Data Access:** querying public life-science databases through REST APIs, with pagination and error handling.
- **Scientific Communication:** clear figures and written interpretation of results for each module.

---

## 🧭 How This Repository Is Organised

Every module folder follows the same pattern:

```
NN_module/
├── README.md            ← what the module covers, every course file explained, key concepts, my plan
├── course_materials/    ← official slides & notebooks (third-party; not my work)
│   └── local/           ← resources without a redistribution licence (git-ignored)
└── <my work>            ← my own notebooks, scripts and write-ups
```

So it's always clear what came from the course and what I built myself.
CI lints **only my code**; `course_materials/` is excluded.

---

## 🗂️ Repository Structure

| # | Module | What it covers |
|---|--------|----------------|
| 01 | [Introduction to EMBL-EBI](01_introduction_to_embl_ebi/) | EMBL-EBI's mission and data resources (ENA, UniProt, PDBe, ChEMBL, Ensembl, MGnify) |
| 02 | [Accessing & Handling Data](02_accessing_and_handling_data/) | Getting data out of databases and into tidy tables |
| ↳ | [APIs & Data Collection](02_accessing_and_handling_data/01_apis_and_data_collection/) | MGnify and ENA APIs with `curl`/`jq`, `requests` and MGnipy |
| ↳ | [Handling & Visualisation](02_accessing_and_handling_data/02_handling_and_visualisation/) | Python for R users, pandas cleaning and pseudonymisation, seaborn |
| 03 | [Foundations of Machine Learning](03_foundations_of_machine_learning/) | Framing biological problems as ML tasks |
| ↳ | [Intro & Fundamentals](03_foundations_of_machine_learning/01_intro_and_fundamentals/) | Supervised vs. unsupervised learning; PCA/t-SNE/UMAP, clustering, SVM, random forests, protein language models |
| ↳ | [Hyperparameters & Performance](03_foundations_of_machine_learning/02_hyperparameters_and_performance/) | Data preparation, SMOTE, cross-validation, grid/random search, ROC-AUC; 8 classifiers on crystallography data |
| 04 | [Foundations of Deep Learning](04_foundations_of_deep_learning/) | Neural networks to LLMs, via biomedical text classification |
| ↳ | [DNNs & Transformers](04_foundations_of_deep_learning/01_dnn_and_transformers/) | TF-IDF + MLP baseline vs. fine-tuned PubMedBERT on PubMed RCT; protein language models |
| ↳ | [Evaluation & Visualisation](04_foundations_of_deep_learning/02_evaluation_and_visualisation/) | Learning curves, macro-F1, confusion matrices, error and confidence analysis, W&B |
| ↳ | [Intro to LLMs](04_foundations_of_deep_learning/03_intro_to_llms/) | Tokens, pre-training → post-training, hallucination, RAG, agents |
| 05 | [Group Projects](05_group_projects/) | Three end-to-end applied projects |
| ↳ | [Gene Expression](05_group_projects/gene_expression/) | TCGA prostate-cancer recurrence prediction; pan-cancer clustering |
| ↳ | [Structural Biology](05_group_projects/structural_biology/) | Molecular-replacement success prediction; protein-crystal image classification |
| ↳ | [Bioimaging](05_group_projects/bioimaging/) | Predicting cytotoxicity from Cell Painting morphology profiles |
| — | [LEARNING_GUIDE.md](LEARNING_GUIDE.md) · [GLOSSARY.md](GLOSSARY.md) | **Start here if you're new to the field:** a learning path through plain-language lessons for every session (no biology or data-science background assumed), plus an A–Z glossary |
| — | [`src/dsls/`](src/dsls/) · [`tests/`](tests/) | My reusable Python package (EMBL-EBI API client; UniProt, ChEMBL and ENA helpers; FASTA/k-mer utilities; expression-data and MR-dataset helpers; PyTorch text-classification, protein-sequence and model-evaluation tools; a minimal RAG toolkit; survival-analysis helpers) and its 105 unit tests (run in CI) |
| — | [Supplementary](supplementary/) | 2025 edition index (statistics, Cytoscape, FAIR, ethics) — fetched locally |
| — | [Notebooks](notebooks/) | Exploratory sandbox notebooks |
| — | [Data](data/) | Local data layout (contents git-ignored) |
| — | [Scripts](scripts/) | Reproducible download of all course resources |
| — | [RUNNING.md](RUNNING.md) · [Makefile](Makefile) | How to run everything from any IDE; one command per task |

---

## 🚀 Getting Started

> 🎓 **Changing careers or new to biology or data science?** Start with **[LEARNING_GUIDE.md](LEARNING_GUIDE.md)**. Every session
> has a `LESSONS.md` that explains its core ideas in plain language, and **[GLOSSARY.md](GLOSSARY.md)** defines the terms.

```bash
git clone https://github.com/Seid-M-Adem/EMBL-EBI-Data-Science-Life-Scientists-Implementation..git
cd EMBL-EBI-Data-Science-Life-Scientists-Implementation.

make setup     # .venv + packages + Jupyter kernel "Python 3 (EMBL-EBI DS .venv)"
make check     # verify everything → "All good"
make lab       # open Jupyter Lab
make test      # run my unit tests
make help      # every available command
```

Works the same in **VS Code / Cursor** (settings, tasks and debug configs included), **PyCharm**, **JupyterLab**
and **Anaconda Navigator**. See **[RUNNING.md](RUNNING.md)** for per-IDE steps, every runnable file, and troubleshooting.

---

## 📈 Progress

| Module | Course materials | My implementation |
|--------|------------------|-------------------|
| 01 · Introduction to EMBL-EBI | ✅ Collected & summarised | ✅ [Resource map + EGFR cross-reference walk, FAIR notes](01_introduction_to_embl_ebi/implementation/) |
| 02 · Accessing & Handling Data | ✅ Collected & summarised | ✅ [02.1: API client, UniProt, ChEMBL EGFR, ENA Tara Oceans](02_accessing_and_handling_data/01_apis_and_data_collection/implementation/) · [02.2: FASTA/k-mer utility, aquaporin sequence EDA](02_accessing_and_handling_data/02_handling_and_visualisation/implementation/) |
| 03 · Foundations of Machine Learning | ✅ Collected & summarised | ✅ [03.1: Iris model comparison, PCA/t-SNE/UMAP and clustering on TCGA](03_foundations_of_machine_learning/01_intro_and_fundamentals/implementation/) · [03.2: MR data audit, leakage, nested CV, imbalance and learning curves](03_foundations_of_machine_learning/02_hyperparameters_and_performance/implementation/) |
| 04 · Foundations of Deep Learning | ✅ Collected & summarised | ✅ [04.1: PyTorch MLP, small biomedical transformers, ESM-2 protein localisation](04_foundations_of_deep_learning/01_dnn_and_transformers/implementation/) · [04.2: bootstrap intervals, calibration, leakage and learning curves](04_foundations_of_deep_learning/02_evaluation_and_visualisation/implementation/) · [04.3: tokenisers for genes and sequences, a graded RAG system over UniProt](04_foundations_of_deep_learning/03_intro_to_llms/implementation/) |
| 05 · Group Projects | ✅ Collected & summarised | 🟡 [Gene expression: honest recurrence prediction, survival analysis and Reactome pathways](05_group_projects/gene_expression/implementation/) · structural biology and bioimaging next |

---

## ⚖️ Licensing

This repository combines material under different licences:

| Content | Licence |
|---------|---------|
| EMBL-EBI course slides and notebooks (`*/course_materials/`) and the supplementary webinar deck in `01_…` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credited in [COURSE_MATERIALS.md](COURSE_MATERIALS.md) and each `ATTRIBUTION.md` |
| `python-data-tutorials/` | Apache-2.0 (licence file included) |
| `DataScience_EBI/` | MIT (licence file included) |
| Third-party figures inside slides; EMBL/EMBL-EBI trademarks | Owned by their rights holders; not relicensed |
| Datasets, the unlicensed bioimaging repo, journal articles, the 2025 edition, live Colab copies | **Not redistributed**: fetched locally by `scripts/fetch_course_materials.sh` |
| My own code and write-ups (everything outside `course_materials/`) | [MIT](LICENSE): scope in [LICENSE-SCOPE.md](LICENSE-SCOPE.md) |

---

## 📬 Contact

**Seid Adem**: open to opportunities in computational biology and bioinformatics.

[![GitHub](https://img.shields.io/badge/GitHub-Seid--M--Adem-181717?logo=github)](https://github.com/Seid-M-Adem)
<!-- TODO: add LinkedIn / email badges -->
