# Structural-biology project · Lessons explained

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this project teaches:** two ML problems from a real protein-structure lab: predicting whether a computational
step will succeed (tabular data), and spotting protein crystals in microscope images (image data).

**Worked example in this repo:** [what makes molecular replacement succeed, explained with SHAP](implementation/01_mr_success_shap.ipynb)
(Lesson 1, plus [03.2](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/implementation/) for
the evaluation).

---

## Background · Why scientists need protein crystals

A protein's **3-D shape** determines what it does and how drugs can bind to it. **X-ray crystallography** is the
classic way to see that shape:

```
purify protein → grow a crystal (millions of copies in a regular lattice) → shine X-rays → record diffraction spots
             → solve the "phase problem" → compute an electron-density map → build the atomic model
```

Two bottlenecks give two ML tasks:

| Bottleneck | ML task | Data |
|------------|---------|------|
| **Growing crystals** is trial and error: thousands of tiny drops are imaged repeatedly, and someone must check each image for crystals | **Image classification:** crystal or no crystal? | crystallisation-drop images (AXIS dataset, EMBL Grenoble) |
| **Solving phases** by molecular replacement (MR) sometimes fails | **Tabular classification:** will MR succeed? | 664 structures × quality/MR statistics |

---

## Lesson 1 · The MR-success tutorial (tabular)

**In one sentence:** predict `MR_success` from numbers describing data quality and the MR attempt. It's a compact
example of the whole classical-ML workflow.

**The features in one line each:**
- **Resolution (Å):** the level of detail; *lower is better* (1.5 Å is sharp, 3.5 Å is blurry).
- **Completeness (%):** how many of the possible diffraction measurements were recorded.
- **I/σ:** signal-to-noise of the measured intensities.
- **TFZ (translation-function Z-score):** how far the best placement of the search model stands out from random
  placements. Above ~8 usually means a solution.
- **LLG (log-likelihood gain):** how much better the placed model explains the data than no model. Higher is better.
- **RMSD:** the estimated difference between the search model and the real structure.

**What this teaches:** the workflow from [03.2](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/LESSONS.md):
cleaning, scaling inside pipelines, comparing eight classifiers fairly, tuning, and reading metrics. **Domain insight
helps:** TFZ and LLG are designed to indicate success, so a model using them should do well. The interesting question is
how much the *data-quality* features add.

---

## Lesson 2 · Image classification with CNNs

**In one sentence:** a **convolutional neural network (CNN)** learns small visual patterns (edges, straight lines,
sharp corners) and combines them into larger ones, which suits crystals: straight edges and facets inside a round drop.

**The difficulty:** drops also contain things that *look* crystal-like (precipitate, dust, fibres, bubbles, drop edges)
and crystals can be tiny or blurred. Labels from humans are also imperfect.

---

## Lesson 3 · Transfer learning: don't start from scratch

**In one sentence:** take a network pre-trained on millions of everyday photos (ImageNet), keep its general visual
knowledge, and **fine-tune** it on the crystal images.

```python
import torch.nn as nn
from torchvision import models
model = models.resnet18(weights="IMAGENET1K_V1")      # pre-trained feature extractor
model.fc = nn.Linear(model.fc.in_features, 2)          # new head: crystal / no crystal
# then train, usually with a small learning rate, often freezing early layers at first
```
**Why it works:** edges, textures and shapes are useful in any image. With a few thousand labelled images, transfer
learning beats training from random weights by a wide margin.

---

## Lesson 4 · Data augmentation

**In one sentence:** create realistic variations of training images (rotations, flips, brightness and contrast
changes, small crops) so the model learns that a crystal is a crystal regardless of orientation or lighting.

- Choose augmentations that preserve the label. A rotated crystal is still a crystal, but a heavy blur might erase a
  tiny one.
- Apply augmentation to **training data only**. Validation and test images must stay untouched.

---

## Lesson 5 · Metrics that match the cost of mistakes

**In one sentence:** a **missed crystal** may mean losing a months-long experiment, while a false alarm costs a minute of
a scientist's time. So **crystal recall** and **balanced accuracy** are the targets, not plain accuracy.

| Model (published) | Balanced accuracy | Crystal recall |
|-------------------|-------------------|----------------|
| AXIS-Vis-v1 | 93.1 % | 90.0 % |
| AXIS-VMXi | 92.0 % | 94.5 % |
| CHiMP-v2 | 91.1 % | 90.3 % |
| MARCO | 85.1 % | 76.6 % |

- **The decision threshold** is adjustable. Lowering it catches more crystals at the price of more false alarms,
  so choose it on validation data to hit a recall target.
- **Error analysis:** look at the missed crystals (false negatives). Are they tiny, blurry or at the drop edge? That
  tells you what data or augmentation to add.

---

## Lesson 6 · Lab-in-the-loop

**In one sentence:** in a working lab, the model's predictions are checked by scientists, and their corrections become
new training labels, so the model keeps improving with use.

This is how ML is deployed in many real labs: it is not a one-off model but a cycle of **predict → review → relabel →
retrain**, with monitoring for changes (a new imager, new plate types) that can silently reduce performance (**data
drift**).

---

## Lesson 7 · When the training set is not as rare as real life (prior shift)

**In one sentence:** the CRIMS training set is **60 % crystals**, a real plate is **about 7 %**, and that tenfold
difference breaks every probability and every fixed threshold the model produces — while leaving its *ranking* of
images untouched.

**Why the datasets differ.** Nobody assembled the training set to be representative. They assembled it to be
*learnable*: enough crystal examples for a network to generalise from. Collecting a representative set would mean
labelling fourteen clear drops for every crystal. This is the normal situation in screening problems, not a mistake.

**What breaks and what survives.**

| | Survives the shift | Breaks |
|---|---|---|
| **Ranking metrics** — ROC-AUC, "is this image more crystal-like than that one" | ✅ | |
| **Predicted probabilities** — "85 % sure this is a crystal" | | ❌ far too high |
| **A threshold of 0.5** | | ❌ flags far too much |
| **Precision, and how big the review pile is** | | ❌ far too optimistic |
| **Balanced accuracy and recall** | ✅ mostly — each is an average *within* a class | |

That last row is why the published AXIS numbers are balanced accuracy and crystal recall. Both average over the two
classes separately, so neither moves much when the mix between classes changes. Plain accuracy and precision do.

**The fix is one line of arithmetic, not more data.** If only the class balance changed and the images themselves
did not, you shift the **log-odds** by the difference between the two prevalences:

```python
from dsls.crystals import shift_prior
realistic = shift_prior(proba, train_prior=0.60, target_prior=0.067)
```

A prediction of 0.5 — carrying no evidence either way — becomes 0.067, the new base rate. Because the shift is the
same for every image, the ordering never changes: ROC-AUC is identical before and after. Only the numbers you would
actually act on move.

> **In plain language.** A model trained on a crystal-rich set has absorbed "crystals are common" as a belief.
> Prior correction tells it the truth about how rare they are, without retraining.

- **Choose the threshold on validation data drawn from the deployment mix**, or correct the prior first. Picking a
  threshold on the test set and then reporting that test score is a classic optimistic bias — the threshold has been
  fitted to the data it is being scored on.
- **Always report the review pile.** "94 % recall" means little if it comes with flagging a third of the plate.
- **Check whether only the balance shifted.** Prior correction assumes the images of a crystal look the same in both
  sets. A different imager or illumination breaks that assumption, and then arithmetic will not save you.

---

## Why it matters at work

Automated image classification is used in structural biology, pathology, microscopy and manufacturing quality
control. Transfer learning, augmentation, cost-aware metrics and error analysis transfer directly to all of them.
