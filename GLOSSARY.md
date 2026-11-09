# Glossary

Plain-English definitions of the biology, data and machine-learning terms used in this repository. The **Lesson**
column points to where each term is explained in context. For the learning route, see
[`LEARNING_GUIDE.md`](LEARNING_GUIDE.md).

**Lesson keys:** 01 = [EMBL-EBI](01_introduction_to_embl_ebi/LESSONS.md) ·
02.1 = [APIs](02_accessing_and_handling_data/01_apis_and_data_collection/LESSONS.md) ·
02.2 = [Data handling](02_accessing_and_handling_data/02_handling_and_visualisation/LESSONS.md) ·
03.1 = [ML fundamentals](03_foundations_of_machine_learning/01_intro_and_fundamentals/LESSONS.md) ·
03.2 = [Model performance](03_foundations_of_machine_learning/02_hyperparameters_and_performance/LESSONS.md) ·
04.1 = [Neural networks](04_foundations_of_deep_learning/01_dnn_and_transformers/LESSONS.md) ·
04.2 = [DL evaluation](04_foundations_of_deep_learning/02_evaluation_and_visualisation/LESSONS.md) ·
04.3 = [LLMs](04_foundations_of_deep_learning/03_intro_to_llms/LESSONS.md) ·
GE / BI / SB = the [gene-expression](05_group_projects/gene_expression/LESSONS.md),
[bioimaging](05_group_projects/bioimaging/LESSONS.md) and
[structural-biology](05_group_projects/structural_biology/LESSONS.md) projects

## Biology and life-science data

| Term | Meaning | Lesson |
|------|---------|--------|
| **Accession** | A stable ID for a database record (e.g. UniProt `P00533` = human EGFR). It is how databases link to each other | 01 |
| **Amino acid** | One of 20 building blocks of proteins, each written as one letter (A, C, D, …) | 02.2 |
| **AlphaFold** | An AI system that predicts 3-D protein structures; its database holds 200M+ predictions | 01 |
| **Batch effect** | Technical differences between groups of samples processed at different times or places | 03.1, BI |
| **Cell Painting** | A microscopy assay that stains six cell compartments so cell shape can be measured | BI |
| **ChEMBL** | EMBL-EBI's database of bioactive molecules and their measured effects on targets | 02.1 |
| **Censoring** | In survival data: the event wasn't observed during follow-up, which isn't the same as "never happened" | GE |
| **Crystallography (X-ray)** | Determining a molecule's 3-D structure from how its crystal diffracts X-rays | SB |
| **DMSO control** | Cells treated with solvent only, the "normal" baseline to compare treatments with | BI |
| **DNA / RNA / protein** | DNA stores genetic information; RNA is a working copy of a gene; proteins are the machines it encodes | 01 |
| **Differential expression (DGE)** | Testing whether a gene's activity differs between two groups | GE |
| **EGFR** | Epidermal growth factor receptor, a protein that is a major cancer drug target. The repo's running example | 01, 02.1 |
| **ENA** | European Nucleotide Archive: raw sequencing data and metadata | 02.1 |
| **Gene expression** | How actively a gene is being copied into RNA in a sample | GE |
| **Hepatotoxicity** | Chemical damage to the liver | BI |
| **IC50 / pIC50** | The concentration that inhibits 50 % of activity; pIC50 = −log10(IC50 in mol/L), so higher means more potent | 02.1 |
| **Metagenomics** | Sequencing all the DNA in an environmental sample (e.g. seawater) at once | 02.1 |
| **Molecular replacement (MR)** | Solving a crystal structure's phases using a similar known structure | 03.2, SB |
| **Motif** | A short sequence pattern with a function (e.g. NPA in aquaporins) | 02.2 |
| **Mutation / variant** | A change in a DNA or protein sequence (e.g. EGFR T790M) | 02.1 |
| **PDB / PDBe** | The Protein Data Bank (experimentally determined structures) and its European node | 01 |
| **pLDDT** | AlphaFold's per-residue confidence score (0–100) | 01 |
| **Proteomics** | Measuring the proteins in a sample | GE |
| **Resolution (Å)** | The level of detail in a structure; a lower number means sharper | 03.2, SB |
| **RNA-seq** | Sequencing that counts RNA molecules to measure gene expression | GE |
| **TCGA** | The Cancer Genome Atlas: public multi-omics data on ~11,000 tumours | GE |
| **ToxCast** | US EPA high-throughput toxicity screening data, used as labels | BI |
| **UniProt** | The central database of protein sequences and functions | 01, 02.1 |

## Data and programming

| Term | Meaning | Lesson |
|------|---------|--------|
| **API** | A way for programs to request data from a service over the web | 02.1 |
| **Caching** | Saving responses locally so repeated requests don't hit the server again | 02.1 |
| **DataFrame** | A table in code (pandas): rows are samples, columns are variables | 02.2 |
| **FAIR** | Findable, Accessible, Interoperable, Reusable: principles for good data sharing | 01 |
| **FASTA** | A simple text format for sequences: a `>` header line, then the sequence | 02.2 |
| **JSON** | A text format for structured data, used by most APIs | 02.1 |
| **k-mer** | A substring of length k from a sequence; counting them turns sequences into numbers | 02.2 |
| **Pagination** | Getting large results in pages, because APIs return a limited number per request | 02.1 |
| **Provenance** | A record of where data came from and when: the version, URL and date | 02.1 |
| **Rate limit / HTTP 429** | A server telling you to slow down; retry with backoff | 02.1 |
| **Tidy data** | One row per observation, one column per variable | 02.2 |

## Machine learning and statistics

| Term | Meaning | Lesson |
|------|---------|--------|
| **Accuracy** | Fraction of predictions that are correct; misleading when classes are imbalanced | 03.2 |
| **Activation function** | The non-linear step in a neuron (ReLU, sigmoid, softmax) | 04.1 |
| **Attention (self-attention)** | A mechanism letting each token weigh every other token, so meaning depends on context | 04.1 |
| **Augmentation** | Making modified copies of training data (rotations, flips) to improve generalisation | SB |
| **Autoencoder** | A network that compresses input through a bottleneck and reconstructs it | GE |
| **Backpropagation** | Computing how each weight contributed to the error, so it can be adjusted | 04.1 |
| **Balanced accuracy** | Average of recall on each class; robust to imbalance | 03.2, SB |
| **Baseline** | A simple model to compare against; it tells you how much complexity adds | 04.1 |
| **Calibration** | Whether predicted probabilities match real frequencies | 04.2 |
| **Class imbalance** | One class is much rarer than another | 03.1, 03.2 |
| **Classification / regression** | Predicting a category / predicting a number | 03.1 |
| **Clustering** | Grouping samples by similarity without labels (k-means, hierarchical, DBSCAN) | 03.1, GE |
| **CNN** | Convolutional neural network, designed for images | 04.1, SB |
| **Cohen's κ** | Agreement corrected for chance; 0 for a model that always predicts the majority | GE |
| **Concordance index (C)** | The survival version of AUC: how often the patient with the higher predicted risk has the event first | GE |
| **Confusion matrix** | A table of true vs predicted classes | 03.2, 04.2 |
| **Cross-validation (k-fold)** | Rotating which part of the data is held out, then averaging scores | 03.1, 03.2 |
| **Data leakage** | Test information influencing training, which inflates scores | 03.2, GE |
| **Dimensionality reduction** | Representing many features with a few (PCA, t-SNE, UMAP) | 03.1, 02.2 |
| **Early stopping** | Stopping training when validation performance stops improving | 04.1, GE |
| **Embedding** | A learned vector representation of an item (a word, a protein, an image) | 04.1, 04.3 |
| **Epoch / batch** | One full pass over the training data / a small group processed together | 04.1 |
| **F1 (macro / micro / weighted)** | Harmonic mean of precision and recall; macro averages classes equally | 03.2, 04.2 |
| **Feature / label** | Input variable / the answer to predict | 03.1 |
| **Feature selection** | Keeping only informative features (filter, wrapper, embedded) | 03.2, GE |
| **Fine-tuning** | Adapting a pre-trained model to a specific task | 04.1, SB |
| **Foundation model** | A large model pre-trained on broad data and reused for many tasks | 03.1, 04.3 |
| **Gradient descent** | Repeatedly adjusting weights a small step in the direction that lowers the loss | 04.1 |
| **Grounding** | Making an LLM answer from supplied evidence (retrieved documents, tool results) rather than from memory | 04.3 |
| **Hallucination** | A fluent but false statement produced by an LLM | 04.3 |
| **Hazard ratio** | How much a factor multiplies the momentary risk of an event in a Cox model | GE |
| **Hybrid search** | Combining exact matching on identifiers with keyword or neural search | 04.3 |
| **Hyperparameter** | A setting chosen before training (tree depth, learning rate) | 03.2 |
| **Kaplan–Meier curve** | The share of patients still event-free over time, accounting for censoring | GE |
| **Learning curve** | Training and validation performance plotted over time or data size | 04.2 |
| **LLM** | Large language model, trained to predict the next token | 04.3 |
| **Loss function** | A number measuring how wrong the model is; training minimises it | 04.1 |
| **Multiple testing (FDR)** | Correcting p-values when many tests are run at once | GE |
| **Nested cross-validation** | Inner CV for tuning, outer CV for an honest estimate of the tuned model | 03.2 |
| **Overfitting / underfitting** | Memorising noise / being too simple to capture the pattern | 03.1, 04.2 |
| **p ≫ n** | Far more features than samples, common in genomics | 03.1, GE |
| **Pathway enrichment** | Testing whether genes of interest fall into known pathways (e.g. Reactome) more often than chance | GE |
| **PCA** | Principal component analysis: linear directions of greatest variance | 03.1, 02.2 |
| **Pipeline** | A chain of preprocessing and model steps fitted together, which prevents leakage | 03.2 |
| **Precision / recall** | Of predicted positives, how many are real / of real positives, how many were found | 03.2 |
| **Proxy variable** | A feature that predicts the outcome only because it travels with the real cause | SB |
| **Prompt** | The instructions and input text given to an LLM; its wording changes the answers and must be tested | 04.3 |
| **PR-AUC / ROC-AUC** | Areas under the precision–recall and ROC curves; how well a model ranks positives | 03.2, BI |
| **RAG** | Retrieval-augmented generation: an LLM answers from retrieved documents | 04.3 |
| **Random forest / XGBoost** | Ensembles of decision trees (bagged / boosted) | 03.2, BI |
| **Recall@k** | How often the correct document is among a search's top *k* results | 04.3 |
| **Silhouette score** | How well each sample fits its cluster compared with the nearest other cluster (−1 to 1) | GE |
| **SHAP values** | A split of one prediction into contributions from each feature, adding up to the prediction | SB |
| **Stratified split** | A split that keeps class proportions equal in each part | 03.2 |
| **Survival analysis / censoring** | Analysing time until an event; *censored* patients left follow-up before any event | GE |
| **Temperature (sampling)** | How adventurous an LLM's choice of next token is; 0 always takes the most likely one | 04.3 |
| **TF-IDF** | Weighting words by how often they appear in a document and how rare they are overall; classic keyword search | 04.1, 04.3 |
| **t-SNE / UMAP** | Non-linear 2-D maps preserving neighbours; distances between clusters aren't meaningful | 03.1 |
| **Test / validation set** | Data held out for the final estimate / for making modelling choices | 03.2, 04.2 |
| **Token** | A unit of text (often a word piece) processed by language models | 04.3 |
| **Tokeniser** | The fixed procedure that splits text into a model's tokens; built from its training text | 04.3 |
| **Transfer learning** | Reusing knowledge from a model trained on another task | SB |
| **Transformer** | The attention-based architecture behind modern language and protein models | 04.1 |
