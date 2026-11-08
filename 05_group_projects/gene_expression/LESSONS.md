# Gene-expression project · Lessons explained

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this project teaches:** how to apply ML to cancer genomics data honestly. That means predicting a clinical
outcome when there are 100× more genes than patients, and exploring whether cancer types have molecular "signatures".

---

## Background · Gene expression and TCGA in plain language

Every cell has the same DNA, but each cell type **switches different genes on**. When a gene is on, the cell makes
RNA copies of it (**expression**). **RNA sequencing (RNA-seq)** counts those copies for all ~20,000 genes at once, which
gives each sample a 20,000-number "activity profile". Cancer changes these profiles, so they carry information about
tumour type and behaviour.

**TCGA (The Cancer Genome Atlas)** profiled about 11,000 tumours across 33 cancer types, and the data is public. The
project uses two parts of it:

| Part | Data | Question |
|------|------|----------|
| Supervised | 243 prostate-cancer patients × 20,530 genes | Will the cancer **recur within 3 years**? |
| Unsupervised | ~1,000 tumours from many cancer types | Do tumour types separate by expression? |

**Clinical outcome words:** *recurrence* means the cancer comes back after treatment. **DFI** (disease-free interval)
and **PFI** (progression-free interval) record *how long* until it came back or progressed, and whether it was observed
at all (**censoring**: a patient who left the study at 2 years without recurrence didn't necessarily stay cancer-free).

---

## Lesson 1 · p ≫ n: when features vastly outnumber samples

**In one sentence:** with 20,530 genes and 243 patients, some genes will separate the two groups **purely by chance**,
so a flexible model can fit the training set perfectly and learn nothing real.

**Analogy:** survey 20,000 random facts about 243 people and some fact will "predict" who likes jazz, by coincidence.
The more facts you check, the more coincidences you find.

**Defences:** feature selection, dimensionality reduction, regularisation (penalties that keep models simple), simple
models, and above all **honest validation** (Lesson 2).

---

## Lesson 2 · Select features inside cross-validation, or you're measuring leakage

**In one sentence:** if you pick "the most informative genes" using all patients, every test fold has already
influenced the choice, and the scores are inflated, sometimes dramatically.

**Seeing it happen (verified run, pure random data):**
```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
X = rng.normal(size=(200, 5000))   # 200 "patients", 5,000 random "genes"
y = rng.integers(0, 2, size=200)   # labels unrelated to X: the true accuracy is 50 %

leaky_X = SelectKBest(f_classif, k=50).fit_transform(X, y)    # selection saw every label
cross_val_score(LogisticRegression(max_iter=1000), leaky_X, y, cv=5).mean()   # 0.94  ← an illusion

honest = make_pipeline(SelectKBest(f_classif, k=50), LogisticRegression(max_iter=1000))
cross_val_score(honest, X, y, cv=5).mean()                    # 0.48  ← the truth: chance level
```
**94 % accuracy on noise.** That is why this error is so dangerous: the result looks like a discovery.

---

## Lesson 3 · Feature-selection strategies

| Family | How it works | Example in the course |
|--------|--------------|-----------------------|
| **Random** (baseline) | pick genes at random | tells you what "no knowledge" scores |
| **Filter** | rank each gene by a statistic, independent of the model | highest variance; **differential expression** |
| **Knowledge-based** | genes from the literature | published prostate-cancer genes |
| **Wrapper** | search subsets by training models (e.g. RFE) | slow but model-aware |
| **Embedded** | selection happens during training | Lasso (zeroes weights), random-forest importance |

**Differential expression (DGE)** asks: "is this gene's expression different between recurrence and no-recurrence
patients?" The course uses the **Mann-Whitney U test**, which compares ranks rather than raw values. It is robust to
the skewed, outlier-heavy distributions typical of expression data.

**Multiple testing:** testing 20,000 genes at p < 0.05 gives about 1,000 "significant" genes by chance alone.
Corrections like **Benjamini-Hochberg (FDR)** adjust for this.

---

## Lesson 4 · Metrics for an imbalanced clinical outcome

- **ROC-AUC:** how well the model ranks recurrent patients above non-recurrent ones (0.5 = coin flip).
- **Cohen's κ (kappa):** agreement between predictions and truth **corrected for chance**. A model that always predicts
  the majority class can have high accuracy but **κ = 0**.

```python
from sklearn.metrics import cohen_kappa_score
cohen_kappa_score([0,0,0,0,0,0,0,0,1,1], [0]*10)   # 0.0, despite 80 % accuracy
```

**Course results (held-out test set):** classifiers reached test AUC 0.54–0.72, and an autoencoder with **early
stopping** reached 0.74. Those are modest numbers, and that's an honest finding: predicting recurrence from expression
alone is hard, and claims of near-perfect accuracy on such data should raise suspicion.

---

## Lesson 5 · Learned representations: UMAP features and autoencoders

**In one sentence:** instead of picking genes, you can **compress** all genes into a few learned dimensions and classify
from those.

- **UMAP → classifier:** reduce to a handful of dimensions, then train a simple model. UMAP must be fitted on training
  data only.
- **Autoencoder:** a neural network that squeezes the input through a narrow "bottleneck" layer and reconstructs it.
  The bottleneck becomes a compact representation. A *classifier* autoencoder also optimises that bottleneck for
  predicting recurrence.
- **Early stopping mattered:** trained for 100 epochs, the autoencoder memorised the training set (training accuracy
  1.0, test AUC 0.66). Stopping when validation loss stopped improving (epoch 54) gave test AUC 0.74.

---

## Lesson 6 · Unsupervised exploration: do cancer types cluster?

**In one sentence:** reduce the pan-cancer data to 2-D, cluster it, and check whether the clusters match the known
tumour types. That shows whether tissue of origin dominates the molecular signal.

1. **PCA** first (fast, linear, interpretable), then **t-SNE / UMAP** for neighbourhood structure.
2. **Clustering:** k-means (round clusters, choose k), **DBSCAN** (density-based, finds arbitrary shapes and labels
   outliers as noise), hierarchical (a tree of similarity).
3. **Silhouette score:** −1 to 1. It asks how close each sample is to its own cluster compared with the nearest other
   cluster, so higher means clearer separation.
4. **Compare with labels:** the adjusted Rand index (ARI) measures agreement between clusters and known types.
5. **Cross-check with another data type:** repeating the analysis on **proteomics** (protein levels) tests whether
   the structure is biological, not a quirk of one technology.

**Caution:** clusters can reflect **batch** (sequencing centre, processing date) rather than biology. Always check
whether clusters line up with technical variables.

---

## Why it matters at work

Biomarker discovery, patient stratification and diagnostic development are core activities in pharma, diagnostics
and hospital research. Employers need people who can say *how they know* a gene signature is real, and Lesson 2 is
the most common thing that goes wrong.
