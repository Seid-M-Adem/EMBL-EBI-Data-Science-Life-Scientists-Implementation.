# Structural Biology Project

> **Status:** 🟡 Part 1 complete; Part 2 not started · **Trainer:** Melanie Vollmar ·
> **Course page:** [Structural biology](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/group-projects/structural-biology/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

During the live course only a few participants chose this track, so they worked on their own research questions.
For on-demand learners the trainer provides **a tutorial and a short research challenge**. Both use tabular
**X-ray diffraction** data and **crystallisation images** from *AXIS: a Lab-in-the-Loop machine learning approach
for automated detection of macromolecular crystals* (EMBL Grenoble).

## 📚 Course Materials Explained
There are no separate project files. Everything is at the end of the
[Data, hyperparameters & model performance slides](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/course_materials/Data_hyperparameters_and_model_performance.pdf)
(**from slide 77**) and in the tutorial repository:

| Resource | What it is |
|----------|-----------|
| **Slide 77: tutorial data** | Structures from two structural-genomics centres (JCSG: 507, SGC: 303; phased by S/MAD: 446, native: 364), giving **664 training samples** at 1.05–3.8 Å resolution |
| [`DataScience_EBI/`](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/course_materials/DataScience_EBI/) (MIT) | **Part 1, the tutorial:** predict **molecular-replacement success** (`MR_success`) from data-quality and MR statistics (TFZ, LLG, RMSD, I/σ, completeness, …): preprocessing notebook, eight classifier notebooks, prediction notebook. Explained in the [03.2 README](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/) |
| [Image-augmentation Colab](https://colab.research.google.com/drive/18Ew7O8HnyhlUAkK9lNfwV9By3qTltlM6?usp=sharing) | Augmentation techniques for small image datasets |
| **Slides 81–84: the challenge** | **Part 2, protein-crystal image classification.** Build a classifier that detects crystals in crystallisation-drop images |
| [AXIS paper (IUCrJ, 2026)](https://journals.iucr.org/m/issues/2026/03/00/jt5083/index.html) | Background and baseline methods |

### 🎯 The challenge: targets to beat (slide 83)
| Model | Balanced accuracy (%) | Crystal recall (%) |
|-------|----------------------|--------------------|
| AXIS-Vis-v1 | 93.1 | 90.0 |
| AXIS-VMXi | 92.0 | 94.5 |
| CHiMP-v2 | 91.1 | 90.3 |
| MARCO | 85.1 | 76.6 |

**Data (Zenodo):** [training set](https://zenodo.org/records/17279592) (5.6 GB) · [test set](https://zenodo.org/records/17279082) (2.4 GB).
These aren't included in the fetch script because of their size; download them manually into `data/raw/structural_biology/`.
The slides also suggest [Teachable Machine](https://teachablemachine.withgoogle.com/) for a quick no-code baseline.

## 🧠 Key Concepts
- **Molecular replacement (MR):** solving the phase problem by using a known homologous structure as a search model.
- **TFZ / LLG:** translation-function Z-score and log-likelihood gain, the standard indicators of whether MR succeeded.
- **Balanced accuracy and recall:** the right metrics when crystals are rare and a missed crystal is costly.
- **Transfer learning:** fine-tuning a pretrained CNN or ViT is the practical route with a few thousand labelled images.

## 🛠️ My Implementation
See [`implementation/`](implementation/).
- [x] **Part 1:** leakage-free MR-success classifier with nested CV (in [03.2](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/implementation/)) and **SHAP interpretation** on unseen crystals, with stability, feature-family and proxy checks → [notebook 01](implementation/01_mr_success_shap.ipynb)
- [ ] **Part 2:** PyTorch transfer-learning crystal classifier (augmentation, class weighting), reported against the targets above. *The image data are CC BY-NC 4.0; to be decided before download.*
- [ ] Error analysis for Part 2: show false negatives (missed crystals) and discuss why they were missed. *(Part 1's error analysis is in notebook 01.)*

## 📝 Notes & Reflections
- **The search model decides MR success.** Three search-model features matched all 28 features (AUC 0.87–0.89);
  the data-quality statistics the tutorial centres on add almost nothing once sequence identity is known.
- **SHAP explains the model, not the world.** Both models leaned on the anomalous signal, which MR doesn't use. A
  stratified table showed why: anomalous data are collected when no close homologue exists, so the signal is a proxy.
- **Check explanations like results:** out-of-fold only, across many training sets, and grouped by family when
  features are near-duplicates. Only the top two features were stable.
- **Interpretation found a data error the metrics hid:** a 73 Å model resolution barely changed AUC but dominated
  one attempt's explanation.
