# 04 · Foundations of Deep Learning

Neural networks, from a single artificial neuron to transformers and large language models, taught through one
running biomedical NLP task: **classifying sentences in PubMed abstracts** (background / objective / methods / results / conclusions).

## 🗺️ Learning Path
| Step | Folder | Session | You learn to… |
|------|--------|---------|---------------|
| 1 | [01_dnn_and_transformers](01_dnn_and_transformers/) | Deep neural networks and transformers | Explain neurons, activations, backpropagation and attention; train a TF-IDF + MLP baseline; fine-tune **PubMedBERT** with Hugging Face |
| 2 | [02_evaluation_and_visualisation](02_evaluation_and_visualisation/) | Model evaluation and visualisation | Diagnose models with learning curves, macro/weighted F1, confusion matrices, error and confidence analysis, and W&B tracking |
| 3 | [03_intro_to_llms](03_intro_to_llms/) | Introduction to Large Language Models | Understand tokens, next-token prediction, pre-training, SFT and RLHF, hallucination, RAG and agents, and how to use LLMs safely in science |

Steps 1 and 2 are linked: notebooks **1A** and **1B** save prediction files that notebook **2** loads and compares.

## 🔍 What to Look For
- **Clean training code**: datasets, models and training loops written as reusable pieces.
- **Sound training practice**: validation monitoring, early stopping, regularisation, fixed seeds, and code that runs on CPU or GPU.
- **Diagnostic visualisation**: loss and accuracy curves, confusion matrices, and interpretation of over- and underfitting.
- **Sequence modelling**: tokenising biological text and sequences; using pretrained (protein) language models.
