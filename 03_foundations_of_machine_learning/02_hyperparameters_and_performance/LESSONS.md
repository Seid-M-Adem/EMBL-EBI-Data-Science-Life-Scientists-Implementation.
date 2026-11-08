# 03.2 · Lessons explained: data preparation, hyperparameters and model performance

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** the practical decisions that determine whether a model really works: preparing data,
splitting it correctly, tuning settings, and reading performance metrics honestly. The examples use a
structural-biology dataset, explained first.

**Worked examples in this repo:** [data audit, leakage and nested CV](implementation/01_mr_audit_leakage_nested_cv.ipynb)
(Lessons 1–3, 5, 7) and [imbalance, thresholds and learning curves](implementation/02_mr_imbalance_and_learning_curves.ipynb)
(Lessons 4, 6). The first one shows a real case of Lesson 3's *grouped* splits: the same crystal in several rows
inflated a model's score from 0.74 to 0.93.

---

## Background · The tutorial dataset in plain language

To see a protein's 3-D structure by **X-ray crystallography**, scientists grow a crystal of the protein, shine X-rays
at it, and record the diffraction pattern. The pattern gives the *intensities* of the scattered waves but not their
*phases*, and both are needed to compute the structure. That is the **phase problem**.

**Molecular replacement (MR)** solves it by borrowing phases from a similar, already-known structure. Sometimes this
works and sometimes it doesn't. The tutorial asks: **from statistics about the data and the MR attempt, can we predict
whether MR succeeded?** (`MR_success` = 1 or 0).

The features are quality numbers such as **resolution** (in Å; lower is sharper), **completeness** (% of possible
measurements collected), **I/σ** (signal-to-noise), and MR scores like **TFZ** and **LLG** (how convincing the placed
model is). You don't need to understand each one to learn the ML lessons. Treat them as numeric measurements.

---

## Lesson 1 · Preparing tabular data

**In one sentence:** most models need complete, numeric, comparably scaled features, and every preparation step is a
decision that should be justified.

| Step | What and why | Code |
|------|--------------|------|
| **Missing values** | models can't take `NaN`; drop rows or **impute** (fill with the median, for example) | `SimpleImputer(strategy="median")` |
| **Outliers** | extreme values can dominate some models; flag them with the IQR rule (beyond 1.5× the interquartile range) or z-scores, then *investigate*, don't just delete | `df[(z.abs() > 3)]` |
| **Categories → numbers** | "beamline A/B/C" becomes three 0/1 columns | `OneHotEncoder()` |
| **Scaling** | put features on comparable scales; essential for distance- and margin-based models (KNN, SVM, k-means, PCA), irrelevant for trees | `StandardScaler()` |
| **Feature selection** | drop redundant or uninformative features (e.g. **RFE** removes the weakest features one at a time) | `RFECV(...)` |
| **PCA** | replace correlated features with fewer uncorrelated components (e.g. keep 95 % of variance) | `PCA(n_components=0.95)` |

---

## Lesson 2 · Data leakage: the most common way to fool yourself

**In one sentence:** **leakage** is when information from the test set influences training, so test scores look better
than the model will really perform.

**The idea in plain language.** If a teacher computes the class average *including tomorrow's exam answers* and uses it
to prepare the students, their exam scores are no longer an honest test. In ML the classic case is fitting a scaler,
imputer or feature selector on **all** the data before splitting. The test rows then influence the training transform.

**The fix: put every learned step inside a `Pipeline`, and fit it on training data only.**
```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), SVC())
model.fit(X_train, y_train)          # imputer and scaler learn from training data only
model.score(X_test, y_test)          # test data is transformed with the training statistics
```
Inside cross-validation, the pipeline is re-fitted on each training fold, so no fold ever sees its own test data.

**Other forms of leakage to look for:**
- duplicates or near-duplicates in both train and test (the same protein twice, the same patient twice);
- features recorded *after* the outcome (e.g. "treatment given" when predicting diagnosis);
- choosing features or hyperparameters by looking at test performance.

**Check yourself:** *You select the 100 genes most different between groups using all patients, then cross-validate a
model on those 100 genes. Is that leakage?*
<details><summary>Answer</summary>Yes. The gene selection saw every patient's label, including those later used as
test folds. Selection must happen inside each training fold, e.g. as a step in the pipeline.</details>

---

## Lesson 3 · Splitting: train, validation, test, and stratification

**In one sentence:** use the **training** set to fit, a **validation** set (or cross-validation) to make choices, and
touch the **test** set **once**, at the end.

- **k-fold cross-validation:** rotates which part is held out, so every sample is tested once and estimates are more
  stable.
- **Stratified** splits keep the proportion of each class the same in every part. This is essential when one class is
  rare.
- **Grouped** splits keep related samples (same patient, same protein family) on the same side, to avoid leakage
  through similarity.

---

## Lesson 4 · Imbalanced classes: resampling and class weights

**In one sentence:** when one class is rare, models drift towards predicting the common class. You can rebalance the
training data or tell the model that mistakes on the rare class cost more.

| Method | Idea | Caveat |
|--------|------|--------|
| **Class weights** | errors on the rare class count more in training | simplest; try it first (`class_weight="balanced"`) |
| **Random oversampling** | duplicate rare examples | risk of memorising them |
| **Undersampling** | discard common examples | throws away data |
| **SMOTE** | create synthetic rare examples between real neighbours | can create unrealistic points; **apply to training folds only** |

**Rule:** never resample or augment the validation or test data. They must reflect reality.

---

## Lesson 5 · Hyperparameters and how to tune them

**In one sentence:** **parameters** are learned from data (a tree's split points); **hyperparameters** are settings you
choose before training (a tree's maximum depth). Tuning means searching for good hyperparameters using validation data.

```python
from scipy.stats import loguniform
from sklearn.model_selection import RandomizedSearchCV

search = RandomizedSearchCV(
    SVC(), {"C": loguniform(1e-3, 1e3), "gamma": loguniform(1e-4, 1e1)},
    n_iter=50, cv=5, scoring="roc_auc", random_state=0,
)
search.fit(X_train, y_train)
search.best_params_
```
- **Grid search** tries every combination; it is thorough but explodes with more settings.
- **Random search** samples combinations and usually finds good regions faster.
- Search over **log scales** for settings that span orders of magnitude (`C` from 0.001 to 1,000).
- **Nested cross-validation** (an outer loop for evaluation, an inner loop for tuning) gives an honest estimate of a
  *tuned* model's performance.

---

## Lesson 6 · Reading performance metrics

**In one sentence:** accuracy alone can mislead, so pick metrics that reflect what errors cost in your problem.

Start from the **confusion matrix** (for "crystal present?"):

| | Predicted: crystal | Predicted: no crystal |
|---|---|---|
| **Really crystal** | true positive (TP) | false negative (FN): *missed crystal* |
| **Really no crystal** | false positive (FP): *wasted follow-up* | true negative (TN) |

| Metric | Formula | Question it answers |
|--------|---------|---------------------|
| Accuracy | (TP+TN) / all | How often right overall? (misleading if imbalanced) |
| **Recall / sensitivity** | TP / (TP+FN) | Of the real positives, how many did we catch? |
| **Specificity** | TN / (TN+FP) | Of the real negatives, how many did we correctly reject? |
| **Precision** | TP / (TP+FP) | When we say "positive", how often are we right? |
| **F1** | harmonic mean of precision and recall | one number balancing the two |
| **Balanced accuracy** | (recall + specificity) / 2 | accuracy that isn't fooled by imbalance |
| **ROC-AUC** | area under the true-positive vs false-positive curve across all thresholds | how well does the model *rank* positives above negatives? (0.5 = random, 1 = perfect) |

**Choosing:** if missing a positive is costly (a missed crystal, a missed tumour), prioritise **recall**. If false alarms
are costly (expensive follow-up experiments), prioritise **precision**. With rare positives, also look at the
**precision–recall curve**.

---

## Lesson 7 · The classifier zoo used in the tutorials

| Model | One-line intuition |
|-------|--------------------|
| Linear SVM | the straight boundary with the widest margin between classes |
| RBF SVM | same idea, but the boundary can curve (the "kernel trick") |
| Decision tree | a flowchart of feature thresholds |
| Bagging | many trees on bootstrap resamples, then vote: lowers variance |
| AdaBoost | trees added one after another, each focusing on the previous ones' mistakes |
| Random forest | bagging plus random feature subsets at each split: decorrelates trees |
| Extremely randomised trees | like a random forest with random split thresholds: faster, sometimes more robust |
| KNN | predict from the *k* most similar training samples (needs scaling!) |

**Professional habit:** compare all models with **the same splits and the same metric**, report the spread across
folds (not only the mean), and prefer the simpler model when scores are within noise.

**Why it matters at work:** "how did you make sure your model wasn't overfitting or leaking?" is a near-universal
interview question for ML roles. Lessons 2, 3 and 5 are the answer.
