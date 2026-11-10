# Bioimaging project · Lessons explained

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this project teaches:** how microscope images of cells become numbers, and how those numbers can predict whether
a chemical is toxic. The workflow is common in drug discovery and chemical safety.

**Worked example in this repo:** [predicting liver-cell cytotoxicity from Cell Painting profiles](implementation/01_cytotoxicity_from_cell_painting.ipynb)
(Lessons 4–6).

---

## Background · The biology in plain language

**Why it matters:** the liver breaks down drugs and chemicals, so **liver toxicity (hepatotoxicity)** is a leading
reason drugs fail or are withdrawn. Testing thousands of chemicals in animals is slow, expensive and ethically
difficult, so researchers want cheap **in-vitro** (cells in a dish) tests that predict harm.

**The experiment:** human liver cells (**hepatocytes**) were exposed to ~1,085 reference chemicals at 8 concentrations
for 44 hours, then photographed with **Cell Painting**.

**Cell Painting** uses six fluorescent dyes, each lighting up a different part of the cell:

| Dye target | What it is | Why it matters |
|------------|-----------|----------------|
| Nucleus (DNA) | where the genome lives | swelling or fragmentation indicates stress or death |
| Endoplasmic reticulum (ER) | protein-folding factory | stress changes its shape |
| Mitochondria | energy producers | a common toxicity target |
| Golgi / plasma membrane | packaging and cell boundary | |
| Actin | cell skeleton | shape changes |
| RNA / nucleoli | gene-activity hubs | |

**The question:** *can the way cells look predict whether a chemical is toxic, or how it acts (its "mode of
action")?*

---

## Lesson 1 · From images to morphological profiles

**In one sentence:** software (**CellProfiler**) measures thousands of features per cell (size, shape, intensity,
texture of each stained compartment), and these are averaged into one **profile** per treatment.

```
image → find cells & compartments (segmentation) → measure ~thousands of features per cell
      → aggregate per well → normalise to controls → select features → aggregate per compound
```
The final modelling table has **1,086 compounds × 4,439 columns**. An alternative is **DINOv2**: a pre-trained vision
model whose embeddings replace hand-designed features (the same idea as foundation models in text, module 04).

---

## Lesson 2 · Normalise to controls

**In one sentence:** compare each treated well with the **DMSO control wells on the same plate**, so that differences
reflect the chemical and not the plate, the day or the microscope.

- **DMSO** is the solvent the chemicals are dissolved in. Wells with DMSO alone show "normal" cells.
- Each feature is expressed as "how many control standard deviations away from the controls", using robust
  statistics (median and MAD) that resist outliers.
- **Why:** plate and batch effects can be larger than biological effects. Without normalisation, a model might learn
  *which plate* a compound was on.

---

## Lesson 3 · Feature selection for profiles

The **pycytominer** pipeline removes features that:
- barely vary (**low variance**), so they carry no information;
- are **highly correlated** with another feature (e.g. two nearly identical size measurements), which is redundant;
- contain frequent missing or extreme values.

This shrinks the feature count and makes models more stable. As in the gene-expression project, any selection that
uses *labels* must be done inside training folds.

---

## Lesson 4 · Labels: ToxCast

**In one sentence:** the labels come from **ToxCast**, the US EPA's high-throughput screening programme, which records
whether each chemical was **active (1) or inactive (0)** in many in-vitro assays.

- Endpoints are grouped as **cytotoxicity** (cell death), **cell-based** and **cell-free** assays.
- **Choosing an endpoint is a scientific decision.** Pick one with enough active compounds to learn from, and with a
  plausible link to what images can show (cell death is visible; a cell-free enzyme assay may not be).

---

## Lesson 5 · Rare positives: imbalance-aware evaluation

**In one sentence:** when only a small fraction of compounds are active, accuracy is misleading. Use **PR-AUC**,
**balanced accuracy** and **stratified** splits.

- **PR-AUC** (area under the precision–recall curve) focuses on how well the rare positives are found, and its
  baseline equals the fraction of positives, not 0.5.
- **Class weights** (e.g. `scale_pos_weight` in XGBoost) make missed actives cost more during training.
- **Splitting by compound** (or by chemical scaffold, the core ring structure) prevents near-identical chemicals from
  appearing in both training and test sets.

---

## Lesson 6 · XGBoost vs a neural network on tabular data

| | **XGBoost** (gradient-boosted trees) | **Simple neural network (MLP)** |
|---|---|---|
| Idea | trees added one at a time, each correcting the previous errors | layers of learned weighted sums |
| On tabular data | often the strongest model | competitive with tuning; needs scaling and early stopping |
| Needs | little preprocessing | scaled inputs, a training loop, more tuning |
| Interpretation | feature importance, SHAP | harder |

**Professional habit:** compare both on **identical splits and metrics**, with a simple baseline (e.g. logistic
regression), and report variability across folds.

**Interpretation:** asking *which compartment's features* drive predictions (mitochondria? nucleus?) connects the
model back to biology and suggests a mode of action.

---

## Why it matters at work

High-content screening and morphological profiling are used across pharma (target discovery, toxicity screening) and
regulatory science (alternatives to animal testing). The skills are image-derived features, batch normalisation,
imbalanced classification and interpretable models.
