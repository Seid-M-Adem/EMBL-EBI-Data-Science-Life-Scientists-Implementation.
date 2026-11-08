# 04.1 · DNNs & Transformers

> **Status:** ✅ Implementation complete (3 / 3 tasks) · **Trainer:** Amina Mardiyyah Rufai (Machine Learning Data Scientist) ·
> **Course page:** [Deep neural networks (DNNs) and transformers](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/foundations-of-deep-learning-dl/deep-neural-networks-dnns-and-transformers/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

Part A explains **how neural networks learn**. Part B explains **why transformers** became the standard architecture
for sequences. The practicals compare a classical neural baseline with a **fine-tuned biomedical transformer** on the
same task.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Introduction_to_DNNs_and_Transformers.pdf`](course_materials/Introduction_to_DNNs_and_Transformers.pdf) (44 slides)
**Part A: Deep neural networks**
- DL vs. traditional ML: *the model learns the features* instead of humans engineering them
- Anatomy of an **artificial neuron**: inputs × weights + bias → activation (**ReLU, sigmoid, tanh, softmax**) → output
- From neurons to **layers**; what makes a network *deep*
- **Training loop:** forward pass → loss → backpropagation → optimiser update → repeat
- Common architectures for life-science data: feed-forward, CNNs (images), RNNs (sequences), transformers

**Part B: Transformers (*"Attention is all you need"*)**
- Sequence vs. language modelling, and why **order and context** matter (*"the dog bit the man"*)
- Biomedical context: neighbouring words decide whether a mention is a gene or a protein, a cell type or a cell line
- **Self-attention:** every token weighs every other token; encoder (BERT) vs. decoder (GPT) models
- Pre-training then **fine-tuning** on a downstream task

### Practical notebooks (task: **PubMed RCT 20k** sentence classification, 5 labels)
| Notebook | Model | What it does |
|----------|-------|--------------|
| [`session1A_dnn_pubmed_rct20k_tutorial.ipynb`](course_materials/session1A_dnn_pubmed_rct20k_tutorial.ipynb) ([Colab](https://colab.research.google.com/drive/1WDO6TtHylzrw3HpLMzIqQsQ5WNPVzDc-?usp=sharing)) | **TF-IDF → TruncatedSVD → MLP** (scikit-learn `MLPClassifier`) | Loads `armanc/pubmed-rct20k` from Hugging Face; takes an 8,000-sentence subset; looks at the class balance; cleans text (`@` placeholders, symbols); trains and tunes the MLP; reports metrics and a confusion matrix; **saves predictions for Session 2** |
| [`session1B_finetune_a_pretrained_transformer.ipynb`](course_materials/session1B_finetune_a_pretrained_transformer.ipynb) ([Colab](https://colab.research.google.com/drive/1TInWLPKvYTG9icYRuHp2LKp2muX7HqhX?usp=sharing)) | **PubMedBERT** (`microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext`) + classification head | Loads the cleaned subset `Mardiyyah/pubmed-rct-subset_cleaned`; tokenises; dynamic padding with `DataCollatorWithPadding`; Hugging Face `Trainer` (3 epochs, lr 2e-5, best checkpoint by accuracy); per-class report, confusion matrix and error inspection; **saves predictions and metrics for Session 2** |

Both notebooks end with reflection questions: which labels are confused, and why (class imbalance, ambiguity, context)?

## ▶️ Running the Practicals
- ⚠️ The course page's Colab links for 1A and 1B are **swapped** (its "1A" link opens the 1B notebook). The links above are corrected.
- The committed notebooks are the published FTP snapshot. The trainers kept editing the Colab versions afterwards (e.g. a 60/40 instead of
  70/30 first split in 1A, extra discussion prompts, Drive-mount cells). `make fetch-local` saves those live versions, with outputs
  stripped, to `course_materials/local/colab/` (git-ignored) for comparison.
- **Run locally without editing the originals:** `make runnable` writes Colab-free copies of 1A, 1B and session 2 into
  `course_materials/local/runnable/` (git-ignored) using [`scripts/localize_notebook.py`](../../scripts/localize_notebook.py).
  The copies comment out `drive.mount` / `!pip`, set `BASE_DIR` to the notebook's folder, and disable the optional Hugging Face
  upload steps. All three share that folder, so session 2 finds the 1A/1B outputs.
- **Tested on 2026-11-07** on an Apple-silicon Mac (`.venv`, PyTorch on the GPU via `mps`):

  | Notebook | Time | Test accuracy | Test macro-F1 |
  |----------|------|---------------|---------------|
  | 1A · TF-IDF → SVD → MLP | 14 s | 0.635 | 0.535 |
  | 1B · PubMedBERT fine-tune (3 epochs) | **3 h 15 min** | **0.853** | **0.790** |

  1B needs **`accelerate`** (the Hugging Face `Trainer` refuses to start without it). It's now in `requirements-course.txt`.
  The 3 h 15 min is wall-clock time, not compute: the run's own log shows one 9.5-second evaluation taking 35 minutes
  (the laptop paused). My own fine-tuning loop trains the same model on similar data in about 5 minutes on the same
  machine ([notebook 02](implementation/02_small_biomedical_transformers.ipynb)). For long local runs, keep the Mac
  awake with `caffeinate -i`.
- Written for **Google Colab**. Locally, **skip the `google.colab` / `drive.mount` cells** and set the output paths to a local folder.
- 1B pins its own versions (`transformers==4.48.2`, `datasets==3.0.2`, `evaluate==0.4.5`). `requirements-course.txt` is compatible with them.
- 1B fine-tunes a BERT-base model. A **GPU is strongly recommended**; on CPU, reduce the subset size or the number of epochs.
- The optional Hugging Face Hub upload cell in 1A needs a token. Skip it unless you want to share the outputs.

## 🧠 Key Concepts
- **Activation function:** the non-linearity that lets networks learn more than linear maps.
- **Backpropagation:** applying the chain rule to get the gradient of the loss with respect to every weight.
- **TF-IDF:** word-importance features; a strong classical baseline for text.
- **Self-attention:** context-dependent token representations computed from query/key/value similarity.
- **Fine-tuning:** adapting a pretrained model to a new task by training a small head (and optionally all layers) on labelled data.

## 🛠️ My Implementation
See [`implementation/`](implementation/). All three notebooks explain each step in plain language for readers new to the field.
- [x] Re-implement the MLP baseline in **PyTorch** (custom `Dataset`, `nn.Module`, training loop with early stopping) → [notebook 01](implementation/01_pytorch_mlp_pubmed_rct.ipynb), [`src/dsls/textclf.py`](../../src/dsls/textclf.py)
- [x] Fine-tune smaller biomedical checkpoints and compare speed against accuracy → [notebook 02](implementation/02_small_biomedical_transformers.ipynb)
- [x] Apply the same pipeline to a **biological sequence** task: protein localisation from ESM-2 embeddings → [notebook 03](implementation/03_esm2_protein_localisation.ipynb), [`src/dsls/protein.py`](../../src/dsls/protein.py)

## 📝 Notes & Reflections
- **Preprocessing must fit the question.** The course's 1A network was held back by removing stop words: for
  *sentence roles*, the small words ("we", "were", "to") are the signal. A plain linear model without that step beat
  the network by 0.14 macro-F1.
- **One piece of domain knowledge beat everything else I tried.** Where a sentence sits in its abstract raised a small
  network's macro-F1 by 0.13. Written into the text ("sentence 3 of 12: …"), it lifted PubMedBERT to 0.847 from just
  400 training abstracts. The same idea for proteins (look at the N-terminus, where targeting signals sit) helped a
  crude baseline but not ESM-2, which already reads that signal. **Domain knowledge helps most where the model
  can't find the pattern alone, so measure it.**
- **Read the logs before blaming the model.** The course's 3 h 15 min fine-tune was mostly a 35-minute stall and
  other pauses; the same training takes about 5 minutes.
- **When a model scores near chance, look inside it.** bio-mobilebert's new output layer started with scores in the
  tens of thousands (MobileBERT has no normalisation layers to keep values small). Neither the learning rate nor a
  normalisation layer fixed it. I report it as a failure rather than dropping it.
- **Reproducibility needs every random step seeded.** Identical runs of the protein network differed by up to 0.015
  macro-F1 until I seeded the starting weights. `MLPClassifier` now takes a `seed`, with a unit test.
- **The better the features, the more a leaky split flatters them.** For proteins, a random split inflated ESM-2
  results by up to 0.07 but simple composition features by only 0.01. I grouped by protein family throughout.
