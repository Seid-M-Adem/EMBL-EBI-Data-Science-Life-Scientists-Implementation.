# 2025 Edition — Supplementary Materials

The 2026 course's *Further learning* page recommends the
[**2025 edition's materials**](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/).
That edition was a different course: Python basics, **statistics**, **network analysis with Cytoscape**, FAIR data,
data ethics and green computing. These topics aren't in the 2026 edition, so I use it as supplementary study.

> Green A., Zane F. (eds.) (2025). *Data science for life scientists – 2025* [Course materials].
> EMBL-EBI Training. https://doi.org/10.6019/TOL.DataScience25-t.2025.00001.1 ·
> Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), except where further licensing details are provided.

**Nothing from the 2025 edition is committed.** It's supplementary (~300 MB) and some of it has no licence, so it's
downloaded on demand into `local/` (git-ignored):

```bash
make fetch-2025        # = scripts/fetch_course_materials.sh --2025   (~140 MB here + 165 MB dataset in data/raw/)
```

What the fetch **skips on purpose**:
- the participants' **flash-talk decks** (`Day5/Flashtalks/`): student work, not course material
- `.pptx` files that have a PDF version
- R cache files
- the second copy of `project_data.h5ad`

## 📚 Session Index

| Session (2025 page) | Trainer(s) | Local files (`local/…`) | Related 2026 module |
|---------------------|------------|-------------------------|---------------------|
| [Getting started with Python](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-python/getting-started-with-python/) | Iris Diana Yu, Andrian Yang | `Day1/Python practicals/getting_started_with_python.ipynb`, `colab/getting_started_with_python.ipynb` | 02.1 (Python prerequisites) |
| [Data handling with Python](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-python/data-handling-with-python/) | Andrian Yang, Iris Diana Yu | `Day1/Python practicals/data_handling_with_python.ipynb` + `data/*.csv`; solution notebook in `repos/data_science_2025/python_sessions/` | 02.2 |
| [Data visualisation with Python](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-python/data-visualisation-with-python/) | Iris Diana Yu, Andrian Yang | `Day1/Python practicals/data_visualisation_with_python.ipynb`, `colab/data_visualisation_with_python.ipynb` | 02.2 |
| [Introduction to statistics](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-statistics/) | Sarah Kaspar | `Day2/stats/Statistics_lecture.pdf`, `…Statistics-in-python.ipynb`, `mice.csv`, `colab/statistics_in_python.ipynb` | **not covered in 2026** |
| [Introduction to EMBL-EBI data resources](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/embl-ebi-data-resources/introduction-to-embl-ebi-data-resources/) | Flaminia Zane | `Day1/EMBLEBIdataresources_DAT25.pdf` | 01 |
| [Programmatic access to data resources](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/embl-ebi-data-resources/programmatic-access-to-data-resources/) | Nandana Madhusoodanan, Fabio Madeira | `Day4/Programmatic_Access_Data_Science.pdf`, `Day4/*.ipynb`, `colab/programmatic_access_examples.ipynb` (PDBe, UniProt, Ensembl REST examples), `colab/programmatic_access_exercises_blast.ipynb` (UniProt FASTA → BLAST job) | 02.1 |
| [Machine learning: introductory lecture](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-machine-learning/machine-learning-introductory-lecture/) | Melissa Adasme, Jiawei Wang | `Day3/Machine learning - morning/Introduction_to_ML.pdf` | 03.1 |
| [Machine learning: practical](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-machine-learning/machine-learning-practical/) | Melissa Adasme, Jiawei Wang | `…/ML_practical.pdf`, `…/Copy of Introduction_to_ML.ipynb`, `colab/ml_practical_iris.ipynb` | 03.1 |
| [Applications of ML in biosciences](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-machine-learning/applications-of-machine-learning-in-biosciences/) | Jiawei Wang | `Day3/ML_for_Biology_Session.pdf` | 03.1 / 04 |
| [Network analysis and Cytoscape](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/introduction-to-network-analysis-and-cytoscape/) | Kalpana Panneerselvam, Juan Jose Medina | `Day5/Cytoscape/*.pdf`, `Day5/Cytoscape/Pratical materials.zip` (session files, expression data) | **not covered in 2026** |
| [Good data management: FAIR](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/data-science-a-broader-view/good-data-management-making-your-data-fair/) | Ajay Mishra | `Day1/2025-06-12_Data_management_and_FAIR.pdf` | — |
| [Graphic design for data visualisation](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/data-science-a-broader-view/graphic-design-principles-for-data-visualisation/) | Holly Joynes | `Day1/Graphic design principles for data vis.pdf` | 02.2 |
| [Environmental impact of computing](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/data-science-a-broader-view/environmental-impact-of-computing-and-bioinformatics/) | Loïc Lannelongue | `Day4/Lannelongue_GreenAlgorithms_2025-06_EBI.pdf` | — |
| [Data ethics to AI governance](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/data-science-a-broader-view/a-journey-from-data-ethics-to-ai-governance/) | Nathanael Sheehan | `Day4/Data Ethics & Responsible Data Governance.pdf` | 04.3 |
| [Group project: gene expression (scRNA-seq)](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/group-projects-short-research-challenges/gene-expression-single-cell-rnaseq/) | Iris Diana Yu, Daianna Padilla-Gonzalez | `Day3/Gene expression/EBI_DataScience_course_06_09_2025.pdf`, `repos/data_science_2025/project_ge/`, data: `data/raw/2025_gene_expression/project_data.h5ad` | 05 · GE |
| [Group project: protein structure (PDBe)](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials/group-projects-short-research-challenges/protein-structure-with-protein-data-bank-in-europe/) | Cristian Escobar Bravo, Paulyna Magaña | `Day3/Protein structure group project/*.pdf`, `repos/pdbe-api-training/` | 05 · SB |
| Course intro / wrap-up | — | `Day1/Introduction Course.pptx`, `Day5/Wrap up session DAT25 - to share.pptx` | — |

## 📦 External Repositories (snapshots in `local/repos/`)

| Repository | Licence | Notes |
|------------|---------|-------|
| [Functional-Genomics/data_science_2025](https://github.com/Functional-Genomics/data_science_2025) | none stated (all rights reserved) | Data-handling solution notebook, and the gene-expression project notebook with answers. Local only |
| [PDBeurope/pdbe-api-training](https://github.com/PDBeurope/pdbe-api-training) | Apache-2.0 | PDBe API tutorials used by the protein-structure project |
| [Functional-Genomics/scRNA-seq_python_course_2024](https://github.com/Functional-Genomics/scRNA-seq_python_course_2024) | none stated | Linked as background; **not fetched** (184 MB) |

## ▶️ Running
- The notebooks run with the repo's `.venv` and kernel **Python 3 (EMBL-EBI DS .venv)**. Run them from their own folder (see [RUNNING.md](../../RUNNING.md)).
- The scRNA-seq project needs `scanpy` and `anndata` (`pip install scanpy`). They're not in the requirements, because the 2026 course doesn't use them.
- The Cytoscape practical needs the [Cytoscape](https://cytoscape.org/) desktop app; unzip `Pratical materials.zip` first (43 files: Cytoscape session files `.cys`, expression data, R Markdown).
- Colab notebooks were saved with **outputs stripped**. Skip any `google.colab` cells when running locally.

*This folder is not affiliated with or endorsed by EMBL-EBI. Third-party figures inside slides remain the property of their owners.*
