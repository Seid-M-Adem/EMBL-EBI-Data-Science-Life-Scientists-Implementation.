# Bioimaging Project

> **Status:** ⚪ Not started · **Trainer:** Guillaume Ollitrault ·
> **Course page:** [Bioimaging](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/group-projects/bioimaging/)

## Overview
**Investigating chemical mode of action with cell profiling and machine learning.**
Primary human hepatocytes were treated with ~1,085 reference compounds (8 concentrations, 44 h exposure) and imaged
with the **Cell Painting** assay. Cell Painting uses six dyes to label the nucleus, ER, mitochondria, Golgi, actin and RNA.
Each image becomes a high-dimensional **morphology profile**. The central question:

> **Can Cell Painting morphology profiles predict chemical cytotoxicity or mode of action?**

## 📚 Course Materials Explained

### [`course_materials/Bioimaging_project_overview.pdf`](course_materials/Bioimaging_project_overview.pdf) (7 slides)
- **Context:** hepatotoxicity and mode of action from morphology
- **Why Cell Painting:** an optimised high-content imaging assay; much cheaper per sample than single-cell omics, yet information-rich
- **Pipeline:** microscopy image → features (CellProfiler, or **DINOv2** embeddings) → dose-response and mode-of-action analysis
- **Labels:** in-vitro assay activity from ToxCast
- **Models:** **XGBoost** (classical ML) and a **simple sequential neural network** (deep learning)
- **Project planning** prompts and the link to the practical repository

### Practical code: [ewald-lab/2026_DataScienceForLifeScientists_Training](https://github.com/ewald-lab/2026_DataScienceForLifeScientists_Training)
*This repository has no licence, so it isn't redistributed here. `scripts/fetch_course_materials.sh --local` clones it
to `course_materials/local/ewald-lab-training/`, which is git-ignored.*

| Part | Notebook | What it does |
|------|----------|--------------|
| 1 · Foundations | `analysis/01_data_collection_preprocessing/01_plot_images.ipynb` | Look at one Cell Painting field channel by channel (AGP, ER, Mito, DNA, RNA, brightfield) |
| 1 · Foundations | `…/02_cell_painting_pipeline.ipynb` | Turn CellProfiler measurements into profiles with **pycytominer**: annotate with metadata, **normalise to DMSO controls**, select features (drop low-variance and correlated ones), aggregate replicates per compound |
| 2 · Explore | `…/03_data_handling_visualising.ipynb` | Explore the final modelling table (1,086 compounds × 4,439 columns), map compound names to `OASIS_ID`, merge with **ToxCast** cytotoxicity / cell-based / cell-free labels, choose an endpoint, visualise active vs. inactive morphology |
| 3 · Classical ML | `analysis/02_simple_ml/01_ml_protocol.ipynb` | Reproducible protocol: feature and label tables → split → leakage-safe preprocessing → baseline vs. supervised model → tuning on training data → metrics → interpretation |
| 4 · Deep learning | `analysis/03_deep_learning/01_dl_protocol.ipynb` | The same endpoint with a **PyTorch** network: tensors, train/val/test loaders, training loop, comparison with Part 3 |

The `*_results.ipynb` versions are executed reference solutions.

### Data ([`data/raw/bioimaging/`](../../data/), fetched with `--data`)
| File(s) | Role |
|---------|------|
| `BR00127145–49.parquet`, `compound_well_map.csv`, `compound_info.csv`, `perturbation_controls.csv` | Small example plates for the **processing demo** (Part 1) |
| `level6_axiom_selected_features.parquet` | **Final compound-level morphology profiles** used for modelling |
| `v5_oasis_03Sept2024_simple.csv` | Compound name → `OASIS_ID` mapping |
| `toxcast_cytotox_binary.parquet`, `toxcast_cellbased_binary.parquet`, `toxcast_cellfree_binary.parquet` (+ `_info`) | Binary activity labels (1 = active) |
| `load_data.csv` | Image manifest (S3 paths) for viewing example fields |

## ▶️ Running the Practical
```bash
scripts/fetch_course_materials.sh --local --data   # clone the repo + download inputs; links inputs/ automatically
cd 05_group_projects/bioimaging/course_materials/local/ewald-lab-training
pip install -r requirements.txt                     # pinned versions from the course (pycytominer, copairs, umap-learn, …)
jupyter lab analysis/
```

## 🧠 Key Concepts
- **Morphological profiling:** describing cell state with hundreds of image-derived features instead of one marker.
- **Normalising to controls:** per-plate standardisation against DMSO wells removes batch and plate effects.
- **Feature selection in profiling:** dropping low-variance, highly correlated and outlier-prone features.
- **ToxCast:** the US EPA's high-throughput in-vitro toxicity screening data, used here as labels.
- **Imbalanced endpoints:** active compounds are rare, so use PR-AUC, balanced accuracy and stratified splits.

## 🛠️ My Implementation (planned)
- [ ] Endpoint choice justified by class balance and biological relevance
- [ ] XGBoost vs. logistic-regression baseline with scaffold- or compound-aware splitting
- [ ] PyTorch MLP with early stopping, compared on identical splits
- [ ] Interpretation: which compartments' features (Mito, ER, …) drive cytotoxicity predictions

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
