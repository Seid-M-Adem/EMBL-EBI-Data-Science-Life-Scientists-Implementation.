# 03.2 · Hyperparameters & Performance

> **Status:** ⚪ Not started · **Trainer:** Melanie Vollmar · **Course page:** [Data, hyperparameters, and model performance](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-machine-learning-ml/data-hyperparameters-and-model-performance/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

A practical session on what decides whether a model works in practice: **data preparation**,
**correct splitting**, **hyperparameter search**, and **reading performance metrics**. The tutorials use a real
structural-biology dataset: predicting whether **molecular replacement (MR) phasing** succeeds for X-ray
crystallography data. The same slides and code are the starting point for the
[structural biology project](../../05_group_projects/structural_biology/).

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Data_hyperparameters_and_model_performance.pdf`](course_materials/Data_hyperparameters_and_model_performance.pdf) (84 slides)
| Slides | Topic | Highlights |
|--------|-------|-----------|
| 1–5 | Recap | Supervised vs. unsupervised; classification vs. regression |
| 6–26 | **Tabular data preparation** | Missing-value imputation; outliers (standard-deviation and IQR methods); one-hot encoding; feature selection (**recursive feature elimination** with linear SVM); **PCA** to 95 % variance; correlation matrices; power transforms and binning; **StandardScaler fitted on training data only**; when scaling matters (KNN, k-means, SVM, PCA) and when it doesn't (trees) |
| 27–33 | **Image data preparation** | Resizing, array conversion, pixel normalisation |
| 34–41 | **Overfitting and bias** | Causes, structural risk minimisation, detecting and reducing dataset bias |
| 42–44 | **Splitting** | Train/validation/test, k-fold cross-validation, **stratified** splits |
| 45–62 | **Sampling and augmentation** | Random over- and undersampling, class weights, **SMOTE**; image augmentation (rotation, flips, shifts, shear, brightness, zoom) with Keras and **Albumentations**; *mistake:* never augment validation or test sets |
| 63–64 | **Hyperparameter search** | `GridSearchCV` and `RandomizedSearchCV` (with `loguniform`) |
| 65–67 | **Performance indicators** | Accuracy, sensitivity/recall, specificity, FPR, precision, F1; **ROC curve and AUC** |
| 68–76 | **Classifiers** | Linear SVM, RBF SVM, decision tree, bagging, AdaBoost, random forest, KNN, extremely randomised trees |
| 77 | Tutorial data | JCSG and SGC structures (S/MAD- and native-phased) → 664 training samples, 1.05–3.8 Å |
| 78–80 | Resources | Further reading; **tutorial repo** and **image-augmentation Colab** |
| 81–84 | **Structural biology challenge** | Protein-crystal image classification (AXIS); see the [project README](../../05_group_projects/structural_biology/) |

### [`course_materials/DataScience_EBI/`](course_materials/DataScience_EBI/): tutorial notebooks (MIT)
Dataset: [`tutorials/data.csv`](course_materials/DataScience_EBI/tutorials/data.csv). Each row is a crystallographic
data set with diffraction and MR statistics (TFZ, LLG, RMSD, resolution, completeness, I/σ, R-merge, Wilson B, …).
The target is **`MR_success`** (0/1).

| Notebook | What it does |
|----------|--------------|
| `DataScience_2026_preprocessing.ipynb` | Full data-preparation walkthrough: imputation, train/test split, per-feature histograms, **Pearson correlation matrix**, scatter-plot matrix, PDF/CDF/ECDF plots, standardisation, **PCA to 95 % variance**, **RFECV** feature ranking, and **SMOTE** (+ undersampling) evaluated with repeated stratified CV ROC-AUC |
| `DataScience_2026_training_<Model>.ipynb` ×8 | One notebook per classifier: Linear SVM, RBF SVM, Decision Tree, Decision Tree + Bagging, Decision Tree + AdaBoost, Random Forest, Extremely Randomised Trees, KNN. Each runs **`RandomizedSearchCV`**, refits the best model, reports CV accuracy and ROC-AUC, feature importances, and test-set performance |
| `DataScience_2026_predict.ipynb` | Loads a saved model (`joblib`) and predicts on new samples in `predict.csv` |

### [`course_materials/image_augmentation_colab.ipynb`](course_materials/image_augmentation_colab.ipynb) ([Colab](https://colab.research.google.com/drive/18Ew7O8HnyhlUAkK9lNfwV9By3qTltlM6?usp=sharing))
The image-augmentation demo linked from slide 80 (26 cells), saved with **outputs stripped**:
1. Loads an example photo with Keras `load_img`, resizes it to 500 × 500 and converts it to an array
2. **Normalises pixels** from 0–255 to 0–1, and explains why models need a common scale
3. **Augments** with Keras `ImageDataGenerator`: rotation, width/height shift, shear, zoom, horizontal/vertical flip, and a combined pipeline
4. Repeats the idea with **Albumentations** (`HorizontalFlip`, `RandomBrightnessContrast`, …) as the modern alternative

To run it, use the Colab link, or locally `pip install tensorflow albumentations`, skip the `google.colab` / `drive.mount` cells and point
`load_img(...)` at any JPEG. The trainer's example photo (`pexels-rinoadamo-35224529.jpg`, from Pexels) is **not** included: it's a
third-party image, which is why the saved outputs were stripped. The notebook itself notes that `tensorflow.keras.preprocessing.image`
is deprecated and kept only for teaching.

## ▶️ Running the Tutorials
The notebooks read `data.csv` from their own folder, so start Jupyter there:
```bash
cd 03_foundations_of_machine_learning/02_hyperparameters_and_performance/course_materials/DataScience_EBI/tutorials
pip install imbalanced-learn   # needed for SMOTE in the preprocessing notebook
jupyter lab
```

**Tested on 2026-11-07** (`.venv`, kernel *EMBL-EBI DS*, run on a scratch copy): **all 10 notebooks run.**
Preprocessing and the 8 training notebooks take 5–100 s each (AdaBoost is the slowest).
- **`predict` needs one edit, by design:** it loads `best_tree_rand_20260513_1105.pkl`, the trainer's own model. Change the
  filename to a model you trained; the notebook says *"load your own model here by adjusting the name"*.
- **Gotcha:** the six tree-based training notebooks (Decision Tree, Bagging, AdaBoost, Random Forest, Extra Trees) all save
  to `best_tree_rand_<YYYYMMDD_HHMM>.pkl`. Two runs in the same minute overwrite each other; in my test the
  "Decision Tree" file held the AdaBoost model. Rename each model after training it.

## 🧠 Key Concepts
- **Data leakage:** fitting scalers or selectors on the full dataset inflates test scores. Fit on training data only (use a `Pipeline`).
- **Stratification:** keeps class proportions the same in every split, which is essential for imbalanced labels.
- **Hyperparameters vs. parameters:** set before training (e.g. `C`, `max_depth`) vs. learned during training (weights, splits).
- **Grid vs. random search:** random search covers large spaces more efficiently.
- **ROC-AUC:** threshold-independent ranking quality. **Balanced accuracy** is more honest when classes are imbalanced.

## 🛠️ My Implementation (planned)
- [ ] Leakage-free `Pipeline` (impute → scale → select → model) on the MR dataset
- [ ] Compare all eight classifiers with nested cross-validation and a summary table and plot
- [ ] Class-imbalance study: class weights vs. SMOTE vs. undersampling
- [ ] Learning and validation curves for the best model

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
