# Course Materials — Sources, Index & Attribution

This repository contains a copy of the official training materials from the
**EMBL-EBI _Data science for life scientists_ course (2026 edition)**. They're kept as a reference
next to my own implementations. Everything inside a `course_materials/` folder is
**original course content, not my work**. My own code and write-ups live outside those folders.

## 📜 Attribution & Licence

> Green A., Tirunagari S., Zane F. (eds.) (2026). *Data science for life scientists* [Course materials].
> EMBL-EBI Training. https://doi.org/10.6019/TOL.data-science-for-life-scientists-course-t.2026.00001.1

- **Course page:** https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/
- **Licence:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/),
  except where further licensing details are provided.
- **Changes made:** files were renamed for consistency (e.g. spaces removed) and filed by module.
  Their content is unchanged.
- This repository is not affiliated with or endorsed by EMBL-EBI.

**Third-party code included under its own licence:**
[`SandyRogers/python-data-tutorials`](https://github.com/SandyRogers/python-data-tutorials) (Apache-2.0) and
[`mevol/DataScience_EBI`](https://github.com/mevol/DataScience_EBI) (MIT). Each snapshot keeps its `LICENSE` file and a
`SNAPSHOT_SOURCE.txt` recording the commit it was taken from.

**Supplementary webinar deck:** `01_introduction_to_embl_ebi/EMBLEBI_resources_introduction26.pptx` is the unmodified
slide deck of the EMBL-EBI webinar *An introduction to EMBL-EBI resources* (2026; speakers: Flaminia Zane, James Alan Blackshaw,
Noemi Tejera Hernandez, Louisse Mirabueno, Paulyna Gabriela Magana Gomez, Aurelien Luciani, Sandy Rogers). It's published under
**CC BY 4.0** at https://www.ebi.ac.uk/training/events/introduction-embl-ebi-resources-2026/
(file: https://ftp.ebi.ac.uk/pub/training/2026/Webinars/EMBLEBI_resources_introduction26.pptx).

**Third-party content and trademarks:** some slides include figures or photos credited to third parties
("Credit: …", "© …"). Those elements remain the property of their owners and are reproduced only as published by
EMBL-EBI; CC BY 4.0 doesn't extend to them. EMBL and EMBL-EBI names and logos are trademarks of EMBL, aren't
licensed for reuse, and their appearance doesn't imply endorsement of this repository.

Each `course_materials/` folder contains an `ATTRIBUTION.md` listing its files, original URLs, trainers and licence.

## 🗂️ Index

| Module | Session | Materials in repo | Online extras |
|--------|---------|-------------------|---------------|
| [01](01_introduction_to_embl_ebi/course_materials/) | Introduction to EMBL-EBI, its role, and mission | `Intro_to_EMBL-EBI.pdf` (+ supplementary webinar deck `../EMBLEBI_resources_introduction26.pptx`, CC BY 4.0) | — |
| [02.1](02_accessing_and_handling_data/01_apis_and_data_collection/course_materials/) | Introduction to APIs and Python for data collection | `APIs_and_Python_for_data_collection.pdf`, `python-data-tutorials/` (notebooks + data, Apache-2.0) | [GitHub](https://github.com/SandyRogers/python-data-tutorials) |
| [02.2](02_accessing_and_handling_data/02_handling_and_visualisation/course_materials/) | Handling and visualising data in Python | `PyLab_teaching_slides.pdf` | Practical: `intro_to_data_handling_and_viz.ipynb` in 02.1's `python-data-tutorials/` |
| [03.1](03_foundations_of_machine_learning/01_intro_and_fundamentals/course_materials/) | Intro to ML; ML fundamentals: types of ML and common algorithms | `Intro_to_ML.pdf`, `ML_fundamentals_and_algorithms.pdf` | Practical: `intro_to_ml.ipynb` in 02.1's `python-data-tutorials/` |
| [03.2](03_foundations_of_machine_learning/02_hyperparameters_and_performance/course_materials/) | Data, hyperparameters, and model performance | `Data_hyperparameters_and_model_performance.pdf`, `DataScience_EBI/` (10 tutorial notebooks + data, MIT), `image_augmentation_colab.ipynb` (outputs stripped) | [GitHub](https://github.com/mevol/DataScience_EBI) · [Image-augmentation Colab](https://colab.research.google.com/drive/18Ew7O8HnyhlUAkK9lNfwV9By3qTltlM6?usp=sharing) |
| [04.1](04_foundations_of_deep_learning/01_dnn_and_transformers/course_materials/) | Deep neural networks (DNNs) and transformers | `Introduction_to_DNNs_and_Transformers.pdf`, `session1A_dnn_pubmed_rct20k_tutorial.ipynb`, `session1B_finetune_a_pretrained_transformer.ipynb` | Colab (links corrected; the course page swaps them): [1A](https://colab.research.google.com/drive/1WDO6TtHylzrw3HpLMzIqQsQ5WNPVzDc-?usp=sharing) · [1B](https://colab.research.google.com/drive/1TInWLPKvYTG9icYRuHp2LKp2muX7HqhX?usp=sharing) |
| [04.2](04_foundations_of_deep_learning/02_evaluation_and_visualisation/course_materials/) | Model evaluation and visualisation | `Deep_learning_model_evaluation_and_visualisation.pdf`, `session2_model_evaluation_visualisation.ipynb` | [Colab](https://colab.research.google.com/drive/1ldJZHM8150Lc3Y3z9r6gCLGiYMW_1fEX?usp=sharing) |
| [04.3](04_foundations_of_deep_learning/03_intro_to_llms/course_materials/) | Introduction to Large Language Models | `Intro_to_LLMs.pdf` | — |
| [05 · GE](05_group_projects/gene_expression/course_materials/) | Gene expression project | `Concepts_and_models.pdf`, `EBI_Data_download.pdf`, `code/01–04_*.ipynb` (Drive copies checked: same content) | Google Drive: [folder 1](https://drive.google.com/drive/folders/1L0sjGzA9NhXvgw6Zf0KVwUoocmI5HWvU?usp=sharing) · [folder 2](https://drive.google.com/drive/folders/1bM2drlzUaloM2-adSJQ7ntmQLJ6Z4yUM?usp=drive_link) |
| [05 · SB](05_group_projects/structural_biology/) | Structural biology project | *(no separate files)*: 03.2 slides **77–84** and `DataScience_EBI/` | [AXIS paper (IUCrJ, 2026)](https://journals.iucr.org/m/issues/2026/03/00/jt5083/index.html) · Zenodo [train](https://zenodo.org/records/17279592) / [test](https://zenodo.org/records/17279082) |
| [05 · BI](05_group_projects/bioimaging/course_materials/) | Bioimaging project | `Bioimaging_project_overview.pdf` | [GitHub: ewald-lab](https://github.com/ewald-lab/2026_DataScienceForLifeScientists_Training) |

## 🔒 Not Committed (fetched locally)

These resources are used by the course but **can't be redistributed** here, because they
are too large or have no open licence. One command re-creates them locally:

```bash
scripts/fetch_course_materials.sh --all     # or: make fetch-local fetch-data fetch-2025
```

| Resource | Why not committed | Local path (git-ignored) |
|----------|-------------------|--------------------------|
| Gene-expression datasets (~590 MB, incl. a 570 MB `.RDS`) | Size | `data/raw/gene_expression/` |
| Bioimaging Cell Painting / ToxCast inputs (16 files, mostly Parquet) | Size | `data/raw/bioimaging/` |
| Bioimaging practical repo (`ewald-lab`) | No licence file, so all rights reserved | `05_group_projects/bioimaging/course_materials/local/` |
| Gene-expression reference papers (7 PDFs) | Publisher copyright varies | `05_group_projects/gene_expression/course_materials/local/references/` |
| AXIS crystallisation images (5.6 GB + 2.4 GB) | Size; download manually from Zenodo | `data/raw/structural_biology/` |
| Live Colab versions of the 04.1/04.2 notebooks (outputs stripped) | Later trainer edits, kept only for comparison; the FTP snapshot is the committed copy | `04_*/*/course_materials/local/colab/` |
| 2025 course edition (slides, notebooks, Cytoscape practical, two repos) | Supplementary; one repo has no licence | `supplementary/2025_edition/local/` (index: [`supplementary/2025_edition/`](supplementary/2025_edition/)) |
| 2025 single-cell dataset `project_data.h5ad` (165 MB) | Size | `data/raw/2025_gene_expression/` |

## ✅ Completeness Audit (2026-11-06)

- **FTP:** all **48 files** (849 MB) in the 2026 FTP folder are covered by `scripts/fetch_course_materials.sh`.
  19 are committed and byte-identical to the server, 7 reference papers are local-only, and 22 datasets go to `data/raw/`.
- **Colab / Drive:** every Colab and Drive link on the 2026 session pages was downloaded and compared:
  - The image-augmentation notebook (03.2) exists only on Colab. It's now committed.
  - The 04.x Colab versions were edited after the FTP snapshot. They're kept local for comparison.
  - The gene-expression Drive folders match the FTP files.
- **GitHub:** `SandyRogers/python-data-tutorials` and `mevol/DataScience_EBI` are committed snapshots;
  `ewald-lab/2026_DataScienceForLifeScientists_Training` is local-only (no licence).
- **Not downloadable here:** the session **videos** (streamed from the course pages) and the 8 GB Zenodo images.

## 🔭 Further Learning

Recommended by the course's [Further learning](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/further-learning/) page:

| Resource | Type | Fits after module |
|----------|------|-------------------|
| [2025 edition of this course](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/) (statistics, Cytoscape, FAIR, ethics) | Course materials ([local index](supplementary/2025_edition/)) | all |
| [A beginner's guide to interpreting results from biostatistics](https://www.ebi.ac.uk/training/events/beginners-guide-interpreting-results-biostatistics/) | Recorded webinar | 03 |
| [A guide to molecular interactions](https://www.ebi.ac.uk/training/events/guide-molecular-interactions/) | Recorded webinar | 05 |
| [AlphaFold: a practical guide](https://www.ebi.ac.uk/training/online/courses/alphafold/) | Online tutorial | 05 · SB |
| [Biostatistics](https://www.ebi.ac.uk/training/online/courses/biostatistics-introduction/) | Online tutorial | 03 |
| [Data-driven plant science](https://www.ebi.ac.uk/training/online/courses/data-driven-plant-sciences/) | Online tutorial | 02 |
| [EMBL-EBI, programmatically](https://www.ebi.ac.uk/training/online/courses/embl-ebi-programmatically/) | Online tutorial | 02.1 |
| [EMBL-EBI tools](https://www.ebi.ac.uk/training/online/courses/embl-ebi-tools-introduction/) | Online tutorial | 01 |
| [Machine learning in drug discovery](https://www.ebi.ac.uk/training/online/courses/machine-learning-drug-discovery/) | Online tutorial | 03–04 |
| [Network analysis of protein interaction data](https://www.ebi.ac.uk/training/online/courses/network-analysis-of-protein-interaction-data-an-introduction/) | Online tutorial | 05 |
| [Workflows: combining tools for data analysis](https://www.ebi.ac.uk/training/online/courses/workflows-combining-tools-for-data-analysis/) | Online tutorial | 02.1 (Snakemake) |

**Acknowledgement (from the course page):** the course was supported by the **BiotrAIn** project, funded by the
Chan Zuckerberg Initiative, which builds an AI curriculum for bioscientists in Latin America.

## 🧪 Running the Course Notebooks

The course notebooks need packages beyond the core stack:

```bash
pip install -r requirements.txt -r requirements-course.txt
```

Several notebooks were written for Google Colab (`from google.colab import ...`).
If you run them locally, skip or adapt those cells.
