# 03.1 · Lessons explained: machine learning fundamentals

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** how to turn a biological question into a machine-learning problem, why biological data
is especially tricky, and how to choose among the main families of algorithms.

**Worked examples in this repo:** [Iris model comparison](implementation/01_iris_pipeline_model_comparison.ipynb)
(Lessons 5–6), [PCA vs t-SNE vs UMAP on cancer data](implementation/02_tcga_dimensionality_reduction.ipynb) and
[k-means vs hierarchical clustering](implementation/03_tcga_clustering_kmeans_vs_hierarchical.ipynb) (Lessons 3, 4, 6).

---

## Lesson 1 · What machine learning actually is

**In one sentence:** machine learning means **learning a rule from examples** instead of writing the rule by hand.

**The idea in plain language.**
A traditional program is: *rules + data → answers*. Machine learning flips it: *data + answers → rules*. You show the
algorithm many examples (protein measurements labelled "soluble" or "insoluble") and it finds a rule that separates
them. The rule is then applied to new examples.

- **AI** is the broad goal of machines doing "intelligent" tasks.
- **Machine learning** is the subset that learns from data.
- **Deep learning** is the subset of ML that uses large neural networks (module 04).

Everything must become **numbers**: a cell becomes a vector of 20,000 gene-expression values, an image becomes a grid of
pixel intensities, a protein becomes counts of amino acids. Turning raw data into informative numbers is **feature
engineering**.

---

## Lesson 2 · The ML pipeline

**In one sentence:** every ML project follows the same stages, and the early ones (data and features) usually decide
whether it succeeds.

```
collect data → preprocess & normalise → engineer features → choose model → train → evaluate → interpret biologically
```

**A useful rule of thumb:** if a model performs badly, look at the data before trying a fancier algorithm.

---

## Lesson 3 · Supervised vs unsupervised learning

**In one sentence:** **supervised** learning predicts a known label; **unsupervised** learning finds structure when
there are no labels.

| | Supervised | Unsupervised |
|---|-----------|--------------|
| You have | features **and** labels | features only |
| Goal | predict the label for new samples | discover groups or patterns |
| Sub-types | **classification** (categories: tumour/normal) · **regression** (numbers: drug potency) | **clustering** (groups of cells) · **dimensionality reduction** (2-D maps of 20,000-D data) |
| Example in course | Iris species; prostate-cancer recurrence | cell types in single-cell data; pan-cancer clustering |

**Check yourself:** *Predicting a compound's pIC50 (e.g. 7.3) from its structure. Classification or regression?*
<details><summary>Answer</summary>Regression: the target is a continuous number. If you instead predicted "active
(pIC50 ≥ 7) vs inactive", it would become classification.</details>

---

## Lesson 4 · Why biological data is hard

**In one sentence:** biological datasets usually have **far more measurements than samples**, plus technical noise,
batch effects and imbalanced classes. Each of these can fool a model.

| Problem | What it means | What to do |
|---------|---------------|------------|
| **p ≫ n** (curse of dimensionality) | 20,000 genes but 200 patients: a model can always find *some* genes that separate the training set by chance | feature selection, dimensionality reduction, regularisation, cross-validation |
| **Batch effects** | samples processed on different days or machines differ for technical reasons | randomise processing; normalise per batch; check that clusters aren't batches |
| **Dropout** (single-cell data) | many zeros because tiny amounts of RNA weren't captured, not because the gene is off | models and normalisations designed for sparse counts |
| **Class imbalance** | 5 % "active" compounds: predicting "inactive" always gives 95 % accuracy | balanced metrics, stratified splits, class weights |
| **Non-linearity** | effects combine in complex ways | non-linear models (trees, kernels, neural networks) |

**Why it matters at work:** being able to explain these pitfalls, and how you guarded against them, is what interviewers
for biology-focused data roles look for.

---

## Lesson 5 · Overfitting, underfitting and the train/test split

**In one sentence:** a model must be judged on data it **has not seen**. A model that does well on training data but
badly on new data has **overfitted**: it memorised noise instead of learning the pattern.

**The idea in plain language.** It's the difference between a student who memorised last year's exam answers and one
who understood the subject. Only a new exam tells them apart, so you hold back a **test set** that the model never
sees during training.

- **Underfitting:** too simple to capture the pattern (bad on training *and* test data).
- **Overfitting:** too flexible, captures noise (great on training, poor on test).
- The **bias–variance trade-off** is the balance between the two.

**What it looks like in code:**
```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
model = RandomForestClassifier(random_state=0).fit(X_train, y_train)
print(model.score(X_train, y_train), model.score(X_test, y_test))   # training vs test accuracy
```
`stratify=y` keeps class proportions equal in both parts, and `random_state` makes the split reproducible.

**Cross-validation** goes further: split into *k* parts, train on *k − 1* and test on the remaining one, rotate, and
average. That gives a more reliable estimate than one lucky or unlucky split (`cross_val_score(model, X, y, cv=5)`).

---

## Lesson 6 · A tour of the algorithm families

**In one sentence:** there's no single best algorithm. Each family suits different data, and simple interpretable
baselines should come first.

**Dimensionality reduction:** squash many features into a few for visualisation or denoising.
- **PCA:** finds the directions of greatest variation (linear). Fast, deterministic, and its axes have meaning.
- **t-SNE / UMAP:** non-linear maps that keep *neighbours* together. They're good for seeing clusters, but distances
  between clusters and cluster sizes are **not** meaningful.

**Clustering:** group samples without labels.
- **k-means:** you choose *k*, and it finds *k* compact, round clusters.
- **Hierarchical:** builds a tree (dendrogram) of similarities, common in gene-expression heatmaps.

**Supervised models:**

| Model | Intuition | Strengths | Watch out for |
|-------|-----------|-----------|---------------|
| Linear / logistic regression | weighted sum of features | interpretable baseline | only linear relationships (unless you engineer features) |
| SVM | find the widest gap between classes | strong in high dimensions | needs scaled features; slow on large n |
| Decision tree | a flowchart of yes/no questions | readable | unstable: small data changes give a different tree |
| Random forest | many trees vote | robust, gives feature importance | less interpretable than one tree |
| Neural networks | layers of learned features | images, sequences, huge data | needs lots of data; module 04 |

**Foundation models:** large models pre-trained on huge unlabelled data (e.g. **protein language models** trained on
millions of sequences). Their internal representations (**embeddings**) can then be reused for a small labelled task.

---

## Lesson 7 · What makes a good ML question in biology

A good question has:
1. **A clear, measurable outcome** ("recurrence within 3 years", not "aggressiveness").
2. **Numeric inputs available *before* the outcome happens.** Otherwise you are predicting the past with the future.
3. **Enough labelled examples,** with reliable labels.
4. **A biological rationale** for why the inputs should carry information about the outcome.

Red flags: tiny datasets, noisy labels, and **confounders**. For example, if all tumour samples were sequenced in one
lab and all normal samples in another, a model may learn the lab rather than the disease.
