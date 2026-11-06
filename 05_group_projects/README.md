# 05 · Group Projects (Independent Execution)

The course's three project tracks, each completed **independently** end to end. Each one applies the full
data-science lifecycle to a real biological dataset.

| Track | Biological question | Data | Methods |
|-------|---------------------|------|---------|
| [gene_expression](gene_expression/) | Can tumour transcriptomes predict **prostate-cancer recurrence**, and do cancer types separate by expression? | TCGA via UCSC Xena: prostate cohort (243 samples × 20,530 genes) and a pan-cancer expression and proteomics set | Feature selection (variance, literature, Mann-Whitney DGE), KNN / LR / SVM / RF, UMAP, PyTorch classifier autoencoder; PCA, t-SNE, k-means, DBSCAN, hierarchical clustering |
| [structural_biology](structural_biology/) | Can diffraction statistics predict **molecular-replacement success**, and can images detect **protein crystals**? | 664 crystallographic data sets (tabular); AXIS crystallisation images (Zenodo, ~8 GB) | Eight scikit-learn classifiers with randomised search; image augmentation and CNN classification |
| [bioimaging](bioimaging/) | Can **Cell Painting** morphology profiles predict chemical **cytotoxicity or mode of action**? | 1,086 compound-level profiles × 4,439 features (primary human hepatocytes); ToxCast labels | Profile normalisation (pycytominer), classical ML (e.g. XGBoost), PyTorch neural network |

## 🔍 What to Look For
- **Clear problem statement** and biological motivation at the top of each project README.
- **End-to-end pipeline**: data acquisition → preprocessing → modelling → evaluation → interpretation.
- **Justified methodology**: why each method was chosen, and what alternatives were considered.
- **Honest results**: limitations, failure modes, and suggested next steps.
- **Reproducibility**: one-command or step-by-step instructions to regenerate every result.

## 📦 Data
Project datasets are **not committed**. Fetch them with:
```bash
scripts/fetch_course_materials.sh --all   # gene expression + bioimaging data, local-only resources
```
