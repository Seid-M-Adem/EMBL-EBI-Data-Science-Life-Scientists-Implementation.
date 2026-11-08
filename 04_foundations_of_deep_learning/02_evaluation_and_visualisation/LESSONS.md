# 04.2 · Lessons explained: evaluating and understanding deep-learning models

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** *"Training performance is not scientific evidence."* It covers how to choose metrics,
read learning curves, catch leakage and imbalance, analyse errors, and track experiments so results can be trusted.

**Worked examples in this repo:** [uncertainty, calibration and errors of three classifiers](implementation/01_uncertainty_calibration_errors.ipynb)
(Lessons 1, 3–5) and [duplicates, label noise and learning curves](implementation/02_duplicates_label_noise_learning_curves.ipynb)
(Lessons 1–2). Both use the PubMed RCT models from module 04.1.

---

## Lesson 1 · Train → validate → test once → report

**In one sentence:** each data split has one job, and the test set is used **once**, at the end. Otherwise it stops
being an independent test.

| Split | Job | Touch it… |
|-------|-----|-----------|
| Training | fit the weights | every epoch |
| Validation | choose epochs, learning rate, architecture; early stopping | many times |
| Test | estimate real-world performance | **once**, after all decisions are made |

If you check the test score, change something, and check again, the test set has become a second validation set and
your reported score is optimistic.

---

## Lesson 2 · Learning curves: diagnose before you fix

**In one sentence:** plotting training and validation loss over time tells you *which* problem you have, and therefore
which fix to apply.

| What you see | Diagnosis | What to try |
|--------------|-----------|-------------|
| both losses high and flat | **underfitting** | bigger model, better features, train longer |
| training loss falls, validation loss rises | **overfitting** | more data, regularisation, augmentation, early stopping |
| both fall and level off together | **good fit** | stop; evaluate on the test set |
| validation suspiciously better than training, or near-perfect scores | **possible leakage** | check for duplicates and features that encode the answer |

---

## Lesson 3 · Metrics under class imbalance: macro, micro and weighted

**In one sentence:** with several classes of different sizes, *how* you average per-class scores changes the story, and
**macro-F1** is the honest choice when rare classes matter.

For each class, compute precision, recall and F1 (see [03.2 lessons](../../03_foundations_of_machine_learning/02_hyperparameters_and_performance/LESSONS.md)).
Then combine:

| Average | How | Effect |
|---------|-----|--------|
| **Micro** | pool all predictions, then compute | equals accuracy for single-label tasks; dominated by big classes |
| **Weighted** | average per-class F1, weighted by class size | still leans towards big classes |
| **Macro** | plain average of per-class F1 | every class counts equally, so rare classes can't hide |

```python
from sklearn.metrics import classification_report, f1_score
f1_score(y_true, y_pred, average="macro")
print(classification_report(y_true, y_pred))   # per-class precision/recall/F1 + all three averages
```

**Example:** a model that never predicts the rare "objective" class can still score 85 % accuracy, but its macro-F1 drops
sharply. In biomedicine the rare class is often the important one: the adverse event, the positive result.

---

## Lesson 4 · Confusion matrices and error analysis

**In one sentence:** after the numbers, look at **which** classes get confused and **read the actual mistakes**. That is
where you learn what the model doesn't understand.

- **Quantitative error analysis:** *how many* errors, and *where*? A confusion matrix normalised by row shows, for each
  true class, where its examples went.
- **Qualitative error analysis:** *what kind* of errors? Read 20–50 misclassified examples. Typical findings:
  ambiguous sentences (a "background" sentence that sounds like an "objective"), label noise (the annotation was wrong),
  or missing context (the sentence only makes sense next to its neighbours).
- **Agreement analysis:** compare two models. Examples *both* get wrong are often genuinely ambiguous or mislabelled;
  examples only the simple model gets wrong show what the better model learned.

---

## Lesson 5 · Confidence and calibration

**In one sentence:** a model's predicted probability should mean what it says. Among predictions made with "90 %
confidence", about 90 % should be correct. A model that is **confidently wrong** is dangerous.

- A **reliability diagram** bins predictions by confidence and plots actual accuracy per bin. A well-calibrated model
  lies on the diagonal.
- Large neural networks are often **over-confident**. Calibration methods (temperature scaling, for example) can fix
  this.
- **Why it matters:** if predictions feed decisions ("flag this paper for review"), the confidence threshold you choose
  is only meaningful if confidence is calibrated.

---

## Lesson 6 · Experiment tracking and reproducibility

**In one sentence:** record every run's settings, data version, metrics and outputs automatically, so you can compare
runs and reproduce the best one months later.

- Tools: **Weights & Biases** (used in the course), MLflow, or at minimum a results table plus saved config files.
- Log the configuration (hyperparameters, seed, data version, code commit), metrics per epoch, final test metrics and
  artefacts (model files, plots, predictions).
- **Never commit API keys.** Keep them in a git-ignored `.env` file, as the course notebooks do.

**Why it matters at work:** teams can't build on results that can't be reproduced. Being able to answer "which run
produced this number, with what data?" is a basic expectation in professional ML.
