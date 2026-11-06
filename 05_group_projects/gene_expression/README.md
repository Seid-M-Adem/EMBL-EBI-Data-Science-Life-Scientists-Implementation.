# Gene Expression Project

> **Status:** ⚪ Not started · **Trainers:** Victor Muñiz (CIMAT, México) & Nelly Selem (CCM-UNAM, México) ·
> **Course page:** [Gene expression](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/group-projects/gene-expression/)

## Overview
Machine learning on **cancer transcriptomics** from The Cancer Genome Atlas (TCGA). The project has two parts:
1. **Supervised:** predict **3-year recurrence in prostate cancer** from gene expression, a classic *p ≫ n* problem (243 patients, 20,530 genes).
2. **Unsupervised:** explore a **pan-cancer** dataset to see whether tumour types separate by expression (and by proteomics) using dimensionality reduction and clustering.

The material builds on the *CABANA BiotrAIn* programme and Juan Bizzoto's
[cancer_data_for_cluster_and_classification](https://github.com/jbzt/cancer_data_for_cluster_and_classification).

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### Slides
| File | What it covers |
|------|----------------|
| [`Concepts_and_models.pdf`](course_materials/Concepts_and_models.pdf) (77 slides) | **Dimensionality reduction:** why it matters (curse of dimensionality); feature *selection* (filter / wrapper / embedded) vs. feature *extraction*; distance metrics; **PCA**, classical **MDS/PCoA**, **Isomap**, **LLE**, **SNE / t-SNE**, **UMAP**. **Clustering:** hierarchical (single/complete/average/Ward), partition-based (k-means, k-medoids), density-based (**DBSCAN**, HDBSCAN, OPTICS), model-based (GMMs), spectral; cluster validation |
| [`EBI_Data_download.pdf`](course_materials/EBI_Data_download.pdf) (18 slides) | Walkthrough of the **GDC / TCGA portal**: the 32-cancer-type pan-cancer collection, onco-signatures from differential expression, and downloading a differential-expression matrix as TSV |

### Notebooks ([`course_materials/code/`](course_materials/code/))
| # | Notebook | What it does |
|---|----------|--------------|
| 1 | [`01_data_download.ipynb`](course_materials/code/01_data_download.ipynb) | Downloads TCGA **gene expression, clinical phenotype and survival** tables from **UCSC Xena** by cohort code; explains the survival endpoints (**DFI / PFI** and their times); first plots |
| 2 | [`02_classification_part1.ipynb`](course_materials/code/02_classification_part1.ipynb) | **Prostate-cancer recurrence (`recurrence.3y`)**: loads `.RDS` data with `pyreadr`; clinical baseline table; **PCA** exploration; stratified train/test split; **four gene-selection strategies**: random baseline, highest variance, literature-curated genes, and **differential expression (Mann-Whitney U)**; compares **KNN, logistic regression, SVM and random forest** with cross-validated accuracy, **Cohen's κ** and **ROC-AUC**; evaluates on the held-out test set; **random-forest gene importance** |
| 3 | [`03_classification_part2.ipynb`](course_materials/code/03_classification_part2.ipynb) | Same task, two ways of learning a representation: (a) **UMAP → classifier**; (b) a **PyTorch classifier autoencoder** trained on *all* genes, learning a compressed latent representation (300 units in the notebook) optimised for classification, with **early stopping** and latent-space plots |
| 4 | [`04_clustering.ipynb`](course_materials/code/04_clustering.ipynb) | **Pan-cancer exploration:** subsample to 1,000 tumours; **PCA**; disease-level correlation **heatmap** (molecular similarity between cancer types); **t-SNE / UMAP**; **k-means, DBSCAN, hierarchical** clustering scored with the **silhouette score**; then repeats the analysis on **proteomics** to test agreement with transcriptomics |

### Reference papers
Seven reference papers are downloaded to `course_materials/local/references/` by `scripts/fetch_course_materials.sh --local`.
They're git-ignored because publisher copyright varies.

## ▶️ Running the Notebooks
1. `scripts/fetch_course_materials.sh --data` downloads the datasets to `data/raw/gene_expression/` (~590 MB; `pan_cancer_dataset.RDS` alone is 570 MB).
2. The notebooks were written for **Colab with a shared Google Drive folder**. Locally, skip the `drive.mount` cells and
   point the working directory or file paths to `data/raw/gene_expression/`.
3. `pip install -r requirements-course.txt` (includes `pyreadr` for `.RDS` files, `umap-learn`, `plotly`).

## 🧠 Key Concepts
- **p ≫ n:** many more features than samples, so feature selection or dimensionality reduction is required to avoid overfitting.
- **Filter vs. wrapper vs. embedded selection:** statistical ranking vs. model-driven search vs. selection during training (e.g. Lasso, tree importance).
- **Cohen's κ:** agreement corrected for chance, more informative than accuracy on imbalanced outcomes.
- **Silhouette score:** how well each sample fits its cluster compared with the nearest other cluster.
- **Select features on training data only.** Choosing genes using the whole dataset leaks test information.

## 🛠️ My Implementation (planned)
- [ ] Leakage-free pipeline: feature selection *inside* cross-validation folds
- [ ] Compare selection strategies with nested CV and confidence intervals
- [ ] Survival-aware extension: Cox model or random survival forest on DFI/PFI
- [ ] Biological interpretation: pathway enrichment of the top-ranked genes

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
