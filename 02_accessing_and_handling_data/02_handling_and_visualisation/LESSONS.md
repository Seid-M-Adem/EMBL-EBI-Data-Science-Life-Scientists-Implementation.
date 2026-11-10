# 02.2 · Lessons explained: handling and visualising data in Python

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** the everyday Python skills of data science (core data structures, reading files,
cleaning tables with **pandas**, plotting with **seaborn**), with notes for people coming from **R** or Excel.

**Worked example in this repo:** [exploring aquaporin sequences](implementation/01_aquaporin_sequence_eda.ipynb)
(pore motifs, length, hydrophobicity and alignment-free comparison).

---

## Lesson 1 · Python's core data structures, and when to use each

**In one sentence:** lists hold ordered items, dictionaries map keys to values, sets hold unique items, and choosing
the right one makes code simpler and faster.

| Structure | Looks like | Use it for | Biology example |
|-----------|-----------|------------|-----------------|
| `list` | `["ATG", "GCC"]` | ordered collections | codons in reading order |
| `dict` | `{"ATG": "M"}` | look-ups by key | the genetic code (codon → amino acid) |
| `set` | `{"TP53", "EGFR"}` | membership, overlaps | genes shared between two experiments |
| `tuple` | `("chr7", 55019017)` | fixed records | a genomic position |

```python
genetic_code = {"ATG": "M", "GCC": "A", "TTA": "L"}
seq = "ATGGCCTTA"
protein = "".join(genetic_code[seq[i:i + 3]] for i in range(0, len(seq), 3))   # 'MAL'

experiment_a, experiment_b = {"TP53", "EGFR", "KRAS"}, {"EGFR", "BRCA1"}
experiment_a & experiment_b    # {'EGFR'}: genes in both
```

**Gotchas for R users:** Python counts from **0** (`seq[0]` is the first letter), and slices exclude the end
(`seq[0:3]` is letters 0, 1, 2). Missing values are `None` or `NaN`, not `NA`.

---

## Lesson 2 · Vectorisation: let NumPy and pandas do the loops

**In one sentence:** operating on a whole column at once (vectorised) is clearer and often 100× faster than a Python
`for` loop.

```python
import numpy as np
lengths = np.array([231, 264, 295])
lengths / 1000                      # all at once: array([0.231, 0.264, 0.295])
# instead of: [x / 1000 for x in lengths]
```

**Why it's faster:** NumPy arrays store numbers of one type in one block of memory, and the loop runs in compiled C
code rather than the Python interpreter.

---

## Lesson 3 · The DataFrame and tidy data

**In one sentence:** a pandas **DataFrame** is a table, and **tidy** data means one row per observation and one column
per variable. That's the shape almost every analysis and plotting tool expects.

**The idea in plain language.** Spreadsheets often put things in the "wrong" shape for analysis:

*Wide (one column per amino acid):*

| protein | A | C | G |
|---------|---|---|---|
| AQP1 | 0.08 | 0.02 | 0.11 |

*Long / tidy (one row per protein × amino acid):*

| protein | residue | fraction |
|---------|---------|----------|
| AQP1 | A | 0.08 |
| AQP1 | C | 0.02 |
| AQP1 | G | 0.11 |

`melt` goes wide → long, and `pivot_table` goes long → wide:
```python
import pandas as pd
wide = pd.DataFrame({"protein": ["AQP1"], "A": [0.08], "C": [0.02], "G": [0.11]})
long = wide.melt(id_vars="protein", var_name="residue", value_name="fraction")
back = long.pivot_table(index="protein", columns="residue", values="fraction")
```

**Split–apply–combine** with `groupby` is the other everyday move: *split* rows into groups, *apply* a summary, and
*combine* the results:
```python
df.groupby("subfamily")["length"].median()
```

**See it in this repository:** the [aquaporin EDA](implementation/01_aquaporin_sequence_eda.ipynb), section 4, melts 20
composition columns into 6,160 rows and pivots them into a subfamily × residue heatmap.

---

## Lesson 4 · Cleaning: missing values, messy dates, inconsistent labels

**In one sentence:** real data has gaps, typos and inconsistent formats, and cleaning means making **explicit,
recorded decisions** about each problem.

**The toolkit:**
```python
pd.to_datetime(df["date"], errors="coerce")   # unparseable dates become NaT instead of crashing
df.dropna(subset=["date"])                   # drop rows missing a key value…
df["x"].fillna(df["x"].median())             # …or fill them (imputation)
df["name"].str.strip().str.lower()           # normalise text
df["name"].str.extract(r"PIP(\d)")           # pull structured values out of text with a regex
```

**The professional part is the judgement:**
- **Never guess silently.** If a value can't be parsed, leave it missing and *report how many* there were.
- **Count every filter.** Before and after numbers belong in your write-up.
- **Check that rules make sense.** In this repository, mapping protein names to families by text alone would have put
  fungal "Aquaporin-5" with human AQP5. They are unrelated proteins that happen to share a name.

---

## Lesson 5 · Pseudonymisation: protecting personal data

**In one sentence:** replace identifying values (such as names) with a consistent code, so records stay linkable but
people aren't identifiable.

```python
import hashlib
SALT = "keep-this-secret"     # stored separately from the data
def pseudonym(name):
    return hashlib.sha256((SALT + name).encode()).hexdigest()[:12]
pseudonym("Jane Doe") == pseudonym("Jane Doe")   # True: same person, same code
```

**Important distinctions:**
- **Pseudonymised** data can be re-linked by someone who holds the key or salt. It is still personal data under GDPR.
- **Anonymised** data can't be linked back to anyone, which usually requires removing or coarsening more fields (exact
  birth dates → age bands, postcodes → regions).
- A hash *without* a secret salt can be reversed by hashing a list of likely names.

**Why it matters at work:** anyone handling clinical or patient data must know this, and it's a common interview topic
in health data science.

---

## Lesson 6 · Plotting to understand, not to decorate

**In one sentence:** choose the plot that matches your question (distribution, relationship or comparison), and make
sure it shows the data honestly.

| Question | Plot | seaborn |
|----------|------|---------|
| How is one variable distributed? | histogram, box plot, strip plot | `histplot`, `boxplot`, `stripplot` |
| How do two numeric variables relate? | scatter plot, correlation heatmap | `scatterplot`, `heatmap` |
| How do groups compare? | box + points, bar of medians | `boxplot` + `stripplot` |
| Many variables at once? | pair plot | `pairplot` |

**Honesty checklist:**
- Show the **individual points** when n is small (a box plot of 5 points hides that there are only 5).
- Use a **log scale** for data spanning orders of magnitude (read counts, concentrations).
- Label the axes **with units**. State n.
- Use **colour-blind-safe palettes** (`sns.color_palette("colorblind")`).
- Correlation is not causation: in the aquaporin data, length and hydrophobicity correlate at ρ = −0.86 because longer
  proteins carry extra charged regions, not because one causes the other.

---

## Lesson 7 · Reusable code with tests

**In one sentence:** when you write the same logic twice, turn it into a function in a module and add **unit tests**
that pin down its behaviour, including the awkward edge cases.

```python
# simplified from src/dsls/seq.py
def kmers(seq, k):
    return [seq[i:i + k] for i in range(len(seq) - k + 1)]

# tests/test_seq.py
def test_kmers_overlap():
    assert kmers("ACGT", 2) == ["AC", "CG", "GT"]
def test_kmers_longer_than_sequence():
    assert kmers("AC", 3) == []
```
Run with `pytest`. In this repository a test for empty input found a real bug: `parse_fasta("")` crashed because
`Path("")` means "the current directory".

**Why it matters at work:** "writes tested, maintainable code" separates a data scientist who can work in a team from
one who can't. Tests are also what let you change code later without fear.
