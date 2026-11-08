# 03.1 · Intro & Fundamentals

> **Status:** ⚪ Not started · **Trainer:** Jiawei Wang (Lecturer in Computational Biology, University of Bath) ·
> **Course pages:** [Intro to ML](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-machine-learning-ml/intro-to-ml/) ·
> [ML fundamentals](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-machine-learning-ml/ml-fundamentals-types-of-ml-and-common-algorithms/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

Two lectures with one question: *"Can we turn a biological problem into a machine learning problem?"*
The first builds intuition (what ML is, why biological data is hard). The second is a tour of the
algorithms, from PCA to protein language models, with guidance on picking the right one.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Intro_to_ML.pdf`](course_materials/Intro_to_ML.pdf): *How to think about biology as an ML problem* (34 slides)
- **AI vs. ML vs. DL**, and the idea of *learning patterns from numeric data* (vectors and matrices)
- **The ML pipeline:** data collection → preprocessing and normalisation → feature engineering → model selection → training → evaluation → biological interpretation
- **Why biological data is hard:** high dimensionality with few samples (*p ≫ n*), batch effects, scRNA-seq dropout, non-linearity, class imbalance
- **Feature preprocessing:** log transforms, z-scores, highly variable gene selection, missing values
- **Unsupervised vs. supervised learning**, train/test splits, and **overfitting vs. underfitting**
- **Case studies:** scRNA-seq cell typing (UMAP and clustering, then supervised labelling); drug-response regression; PI3Kγ bioactivity classification; image classification and cell segmentation (Cellpose)
- **What makes a good ML question:** a clear outcome, numeric inputs, enough data, a biological rationale; beware tiny datasets, noisy labels and confounders

### [`course_materials/ML_fundamentals_and_algorithms.pdf`](course_materials/ML_fundamentals_and_algorithms.pdf): *Choosing the right algorithm* (35 slides)
| Family | Methods covered | When to use |
|--------|-----------------|-------------|
| Dimensionality reduction | **PCA** (linear, max variance), **t-SNE** (local structure; perplexity), **UMAP** (faster; keeps more global structure) | Visualisation, denoising, before clustering |
| Clustering | **k-means** (compact, spherical clusters; choose *k*), **hierarchical** (dendrograms, expression heatmaps) | Discovering groups without labels |
| Regression / classification | **Linear** and **logistic regression** (interpretable baselines), **SVM** (maximum margin; good in high dimensions), **decision trees** (readable but unstable), **random forest** (robust; gives feature importance) | Prediction with labels |
| Deep learning | **U-Net** (segmentation), **autoencoders** (learned embeddings), **GANs** (generation) | Images, representation learning |
| Foundation models | **Protein language models** (BERT/GPT-style self-supervised training on sequences → embeddings), masked language modelling, continued pre-training | Little labelled data, but lots of unlabelled sequence |

It ends with a decision guide for choosing a method, after *"A guide to machine learning for biologists"* (Nat Rev Mol Cell Biol, 2022).

### Practical: [`intro_to_ml.ipynb`](../../02_accessing_and_handling_data/01_apis_and_data_collection/course_materials/python-data-tutorials/intro_to_ml.ipynb)
*(stored in the 02.1 tutorial repo)*, an end-to-end scikit-learn workflow on the **Iris** dataset:
1. **EDA:** `seaborn.pairplot` to see how separable the classes are
2. **Train/test split** (70–80 % train)
3. **Random forest classifier**, explained through a hand-drawn decision tree
4. **Metrics:** accuracy, precision, recall, F1, confusion matrix
5. **5-fold cross-validation** with `cross_val_score`, and why a single split is risky for rare classes
6. **Unsupervised k-means**, compared with the true species labels

## 🧠 Key Concepts
- **Supervised** (labels → classification/regression) vs. **unsupervised** (no labels → clustering/dimensionality reduction)
- **Curse of dimensionality:** with thousands of genes and few samples, distances lose meaning and models overfit
- **Bias–variance trade-off:** simple models underfit, complex models overfit
- **Feature importance:** which genes or biomarkers drive a prediction

## 🛠️ My Implementation (planned)
- [ ] Re-implement the Iris workflow with a scikit-learn `Pipeline` and compare logistic regression, SVM and random forest
- [ ] PCA vs. t-SNE vs. UMAP on a public expression dataset, with a written comparison
- [ ] k-means vs. hierarchical clustering, evaluated with silhouette score and adjusted Rand index

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
