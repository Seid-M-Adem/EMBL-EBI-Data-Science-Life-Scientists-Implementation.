# 02.2 · Handling & Visualisation

> **Status:** ✅ Implementation complete (3 / 3 tasks) · **Trainers:** Mahfouz Shehu & Sandy Rogers ·
> **Course page:** [Handling and visualising data in Python](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/accessing-and-handling-data-with-python/handling-and-visualising-data-in-python/)

## Overview
Raw data is rarely ready to analyse. This session covers the everyday Python skills of data science:
core data structures, reading files, cleaning and transforming tables with **pandas**, and plotting with **seaborn**.
It's aimed especially at life scientists coming from **R**.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/PyLab_teaching_slides.pdf`](course_materials/PyLab_teaching_slides.pdf) (16 slides)
Companion to **PyLab**, a browser-based (Pyodide) set of 30 graded Python challenges in six biology-themed tiers:

| Tier | Theme | Skills |
|------|-------|--------|
| 1 · Nucleotide | Fundamentals | `print`, 0-based indexing and end-exclusive slicing (`seq[0:3]`), types |
| 2 · Amino Acid | Data structures | `list`, `dict` (codon tables), `set` (gene overlaps), `tuple` |
| 3 · Organelle | Control flow | `for`/`enumerate`, list comprehensions (the Pythonic `sapply`), functions with defaults |
| 4 · Organism | Real data | `csv.DictReader`, `defaultdict` group-bys, `statistics`/`scipy`, regex |
| 5 · Ecosystem | Pipelines | FASTA parser with generators, `Counter` for k-mers, dict comprehensions |
| 6 · Bug Hunt | Gotchas | Off-by-one slicing, mutating a shared list, `str + int` TypeError, `KeyError` → `dict.get`, `/` vs `//`, `UnboundLocalError`, mutable default arguments, `is None` |

It also includes an **"R → Python mindset"** table (`<-` vs `=`, 1- vs 0-based indexing, `NA` vs `None`/`NaN`, …).

### Practical: [`intro_to_data_handling_and_viz.ipynb`](../01_apis_and_data_collection/course_materials/python-data-tutorials/intro_to_data_handling_and_viz.ipynb)
*(stored in the 02.1 tutorial repo)*
- **Duck typing**, Python lists vs **NumPy arrays** (and why vectorised arrays are faster)
- **Reading data** with the standard `csv` module vs `pd.read_csv` → the pandas `DataFrame`
- **Task: anonymise patient data**
  - *Pseudonymise* names with a `hashlib` hash, so future data can still be joined on the same key
  - Parse messy dates with `pd.to_datetime(errors="coerce")`, drop `NaT` rows with `dropna`
  - Turn dates of birth into ages, then drop the identifying column
- **Saving** DataFrames back to TSV
- **Visualisation** with seaborn on the sample datasets (`measurements.tsv`, `people.tsv`)

## 🧠 Key Concepts
- **Tidy data:** one variable per column, one observation per row.
- **Vectorisation:** apply an operation to a whole array or column instead of looping in Python.
- **Pseudonymisation vs. anonymisation:** a consistent hash keeps records linkable without exposing identities.
- **Missing values:** `NaN`/`NaT` must be handled explicitly (drop, impute, or flag).

## 🛠️ My Implementation
See [`implementation/`](implementation/).
- [x] EDA notebook on the API data from 02.1: cleaning, reshaping (`melt`/`pivot`), group-by summaries → [aquaporin sequence EDA](implementation/01_aquaporin_sequence_eda.ipynb)
- [x] Figure set: distributions, correlations and categorical comparisons, each with an interpretation → [`implementation/figures/`](implementation/figures/)
- [x] Small FASTA/k-mer utility (Tier 5 PyLab skills) with unit tests → [`src/dsls/seq.py`](../../src/dsls/seq.py), [`tests/test_seq.py`](../../tests/test_seq.py)

## 📝 Notes & Reflections
- **Most of the work is in cleaning, and cleaning decisions are findings.** Mapping 150 protein names to subfamilies
  required lineage-aware rules: a name-only mapping would have put 18 fungal proteins into mammalian subfamilies.
- **Long format makes analysis straightforward.** Once composition was melted to one row per protein × residue, every
  summary was a `groupby` or `pivot_table` call, and seaborn plotted it directly.
- **Check derived measures against the data.** My first NPA-spacing rule looked reasonable but produced a spread of 70
  residues. Looking at the outliers led to a stricter rule, and the result became much cleaner.
- **Use more than one view of the same question.** The name-based curation was checked with an independent,
  alignment-free k-mer representation (93 % agreement), which gives more confidence than either method alone.
