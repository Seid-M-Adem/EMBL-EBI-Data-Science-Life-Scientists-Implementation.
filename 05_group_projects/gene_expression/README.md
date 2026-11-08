# Gene Expression Project

> **Status:** ⚪ Not started · **Trainers:** Victor Muñiz (CIMAT, México) & Nelly Selem (CCM-UNAM, México) ·
> **Course page:** [Gene expression](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/group-projects/gene-expression/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

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
2. The notebooks were written for **Colab with a shared Google Drive folder**. `make runnable` writes local copies into
   `course_materials/local/runnable/` (git-ignored): `drive.mount`, `!pip` and the `os.chdir` into the trainer's Drive are commented out,
   and `Data/` is linked to `data/raw/gene_expression/`. Open those copies with the **EMBL-EBI DS** kernel.
3. The two Google Drive folders linked from the session page were checked on 2026-11-06. *Folder 1* holds the same six data
   files as the FTP `Data/` folder. *Folder 2* holds notebooks 1, 2 and 4; they're identical to the committed copies except that
   the Drive clustering notebook has one extra cell that just displays `df`. The FTP copies (which also include part 2) are used here.
4. `pip install -r requirements-course.txt` (includes `pyreadr` for `.RDS` files, `umap-learn`, `plotly`).

### ✅ Tested on 2026-11-07 (Apple-silicon Mac, `.venv`, `make runnable` copies)

| Notebook | Result | Notes |
|----------|--------|-------|
| `01_data_download` | ✅ 10 s, after a one-word fix | **Bug in the published notebook:** cell 16 defines `dfi_counts_with_nan` but prints `pfi_counts_with_nan` (`NameError`). Change the print to `dfi_counts_with_nan`. Downloads `PRAD_*` tables from UCSC Xena |
| `02_classification_part1` | ✅ 18 s | |
| `03_classification_part2` | ✅ 70 s | Needs `OMP_NUM_THREADS=1`, otherwise the kernel **deadlocks** (0 % CPU forever) when PyTorch and scikit-learn/UMAP each load their own OpenMP runtime on macOS. The **EMBL-EBI DS** kernel sets it (`make kernel`); in another kernel, run `import os; os.environ['OMP_NUM_THREADS']='1'` before any imports |
| `04_clustering` | ✅ 33 s | Loads the 598 MB pan-cancer `.RDS` |

Results from that run (held-out test set, `recurrence.3y`):
- **Part 1/2 classifiers:** test AUC 0.54 (KNN) to 0.72 (logistic regression).
- **Classifier autoencoder:** trained for 100 epochs it overfits (training accuracy 1.0, test AUC 0.66). With **early stopping**
  (it stopped at epoch 54) test AUC rises to **0.74**, the best model in the notebook. A neat demonstration of why
  early stopping matters with p ≫ n.

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
