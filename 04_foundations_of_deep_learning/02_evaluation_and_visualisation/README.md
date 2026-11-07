# 04.2 · Evaluation & Visualisation

> **Status:** ⚪ Not started · **Trainer:** Amina Mardiyyah Rufai (Machine Learning Data Scientist) ·
> **Course page:** [Model evaluation and visualisation](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-deep-learning-dl/model-evaluation-and-visualisation/)

## Overview
*"Training performance is not scientific evidence."* This session moves from **training** models to
**understanding** them: choosing the right metric, reading learning curves, spotting leakage and imbalance,
analysing errors, and tracking experiments so the results can be trusted and reproduced.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Deep_learning_model_evaluation_and_visualisation.pdf`](course_materials/Deep_learning_model_evaluation_and_visualisation.pdf) (23 slides)
- **Train → validate → test once → report**: what each split is for
- **Metrics by NLP task:** text classification (accuracy, precision, recall, F1), token classification/NER (micro/macro and entity-level F1), language modelling (perplexity, cross-entropy) — there's no one-size-fits-all metric
- **Learning curves:** underfitting vs. good fit vs. overfitting, and *which action to take* for each
- **Failure modes:** **data leakage** (suspiciously good scores), **class imbalance** (majority-class bias)
- **Accuracy vs. precision / recall / F1**, and **macro vs. micro vs. weighted** averaging under imbalance
- **Confusion matrices:** reading false positives and false negatives, and when the plot is (not) useful
- **Error analysis:** quantitative (*how many, where*) and qualitative (*what kind*)
- **Biomedical caveats:** rare but important labels, small datasets, label noise, the cost of missed evidence
- **Experiment tracking with Weights & Biases:** logging configs, metrics, plots and artefacts across runs

### [`course_materials/session2_model_evaluation_visualisation.ipynb`](course_materials/session2_model_evaluation_visualisation.ipynb) ([Colab](https://colab.research.google.com/drive/1ldJZHM8150Lc3Y3z9r6gCLGiYMW_1fEX?usp=sharing))
Compares the **Session 1 MLP baseline** with the **PubMedBERT** model:
1. Loads both prediction tables into a common schema (`text`, `true_label`, `pred_label`, `correct`, `confidence`)
2. Sanity-checks the class balance of the test set
3. Overall metrics side by side → **per-class precision/recall/F1** bar charts
4. **Confusion matrices** for both models
5. **Agreement analysis:** sentences both models get wrong vs. only one does
6. Shows each model's **misclassified examples** (qualitative error analysis)
7. **Confidence analysis:** is the transformer *confidently wrong*?
8. Saves the comparison tables and figures; optionally logs them to **W&B**

## ▶️ Running the Practical
Run [04.1](../01_dnn_and_transformers/) **1A and 1B first**.

> ⚠️ **Bug in the published notebooks (found 2026-11-07):** 1B saves its predictions as `predictions/test_predictions.csv`,
> but this notebook expects `predictions/transformer_test_predictions.csv` (1A uses the matching `dnn_` prefix). Fix it after running 1B:
> ```bash
> cd <your artifacts>/session1B_transformer/predictions
> cp test_predictions.csv transformer_test_predictions.csv && cp validation_predictions.csv transformer_validation_predictions.csv
> ```
> With that fix the notebook runs end to end locally (tested: comparison tables and 6 figures written to `artifacts/session2_evaluation/`).
 This notebook loads their saved prediction CSVs and
metrics JSON. Update the candidate paths cell if your outputs are stored elsewhere. Skip the `google.colab`
cells when running locally. The live Colab version (later edits: extra discussion prompts, `rprint` output) is saved by
`make fetch-local` to `course_materials/local/colab/` for comparison. W&B logging is optional and needs `WANDB_API_KEY` in a `.env` file, which is git-ignored.

## 🧠 Key Concepts
- **Macro-F1:** the unweighted mean over classes, so rare classes count equally.
- **Weighted-F1:** each class weighted by its frequency, which leans towards the majority classes.
- **Calibration / confidence:** whether predicted probabilities match how often the model is actually right.
- **Data leakage:** test information reaching training (e.g. duplicate sentences across splits).

## 🛠️ My Implementation (planned)
- [ ] Reusable `evaluation.py`: learning curves, per-class report, normalised confusion matrix, reliability diagram
- [ ] Repeat the confidence analysis for the MLP (the notebook's extra exercise)
- [ ] Check for leakage: near-duplicate sentences across train and test

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
