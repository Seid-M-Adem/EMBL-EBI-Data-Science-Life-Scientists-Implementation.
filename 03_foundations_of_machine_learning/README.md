# 03 · Foundations of Machine Learning

The core ideas of machine learning, and how to turn a biological question into one.
The emphasis is on **choosing the right algorithm**, **preparing data properly**, and **evaluating models honestly**.

## 🗺️ Learning Path
| Step | Folder | Session(s) | You learn to… |
|------|--------|------------|---------------|
| 1 | [01_intro_and_fundamentals](01_intro_and_fundamentals/) | Intro to ML · ML fundamentals: types of ML and common algorithms | Frame biological problems as supervised/unsupervised tasks; know PCA/t-SNE/UMAP, k-means/hierarchical clustering, linear/logistic regression, SVM, trees, random forests; see where protein language models fit |
| 2 | [02_hyperparameters_and_performance](02_hyperparameters_and_performance/) | Data, hyperparameters, and model performance | Prepare tabular and image data, handle outliers, class imbalance and bias, split and cross-validate correctly, tune hyperparameters, and read performance metrics |

## 🔍 What to Look For
- **Correct problem framing**: choosing supervised vs. unsupervised approaches and justifying the choice.
- **Leakage-free evaluation**: preprocessing inside `Pipeline` objects, stratified splits, and held-out test sets.
- **Rigorous model selection**: cross-validation, grid/random search, and comparison against sensible baselines.
- **Metric literacy**: metrics suited to class imbalance and the biological context (e.g. balanced accuracy, recall, ROC-AUC).
- **Reproducibility**: fixed random seeds and clearly reported results.

## 📚 Course Materials
- Slides: in each subfolder's `course_materials/`
- Practical (step 1): [`intro_to_ml.ipynb`](../02_accessing_and_handling_data/01_apis_and_data_collection/course_materials/python-data-tutorials/intro_to_ml.ipynb)
- Practical (step 2): [`DataScience_EBI/`](02_hyperparameters_and_performance/course_materials/DataScience_EBI/) (MIT), 10 notebooks on a protein-crystallography dataset
