# 02.1 · Lessons explained: APIs and programmatic data collection

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../../GLOSSARY.md); the overall route is
in [`LEARNING_GUIDE.md`](../../LEARNING_GUIDE.md).*

**What this session teaches:** how to get data out of a database **with code** instead of by clicking around a website,
so the work is repeatable, scalable and documented.

---

## Lesson 1 · What an API is, and why scientists use one

**In one sentence:** an **API** (Application Programming Interface) is a set of web addresses that return data in a
structured format (usually JSON) instead of a web page for humans.

**The idea in plain language.**
A website is a shop window designed for people. An API is the loading dock designed for machines. Both hold the same
goods, but the API gives them to you in labelled boxes that a program can unpack.

Why bother?
- **Scale:** downloading 1 protein by hand is fine. Downloading 19,378 drug measurements is not.
- **Reproducibility:** a script records exactly *what* you asked for. Clicks are forgotten.
- **Freshness:** re-run the script to get the latest data release.

**What it looks like in code:**
```python
import requests

url = "https://rest.uniprot.org/uniprotkb/search"
params = {"query": "gene:EGFR AND organism_id:9606 AND reviewed:true", "fields": "accession,length", "format": "json"}
r = requests.get(url, params=params, timeout=30)
r.raise_for_status()                  # stop with an error if the server said no
print(r.json()["results"][0]["primaryAccession"])   # 'P00533'
```
Four parts of every API call: the **endpoint** (URL), **parameters** (your question), the **response status** (did it
work?), and the **response body** (the data).

**Common mistakes:**
- Not checking the status code. A 404 or 500 error page then gets parsed as if it were data.
- Building URLs by string concatenation. Pass `params=` and let the library handle encoding.

**Check yourself:** *What does HTTP status 500 mean, and what should your code do?*
<details><summary>Answer</summary>A server-side error. It isn't your fault, and it may be temporary. Wait and retry a
few times with increasing delays ("backoff"), then fail with a clear message. This repository's client does exactly
that, and it was needed: ChEMBL had two full outages during this work.</details>

---

## Lesson 2 · JSON: the shape of API data

**In one sentence:** **JSON** is a text format of nested dictionaries (`{key: value}`) and lists (`[...]`), and getting
data out means walking down its structure.

**The idea in plain language.** A UniProt entry looks roughly like this:
```json
{"primaryAccession": "P00533",
 "genes": [{"geneName": {"value": "EGFR"}}],
 "sequence": {"length": 1210, "value": "MRPSGTAGAALLALL..."}}
```
To get the gene name you follow the path `genes → first item → geneName → value`:
```python
entry["genes"][0]["geneName"]["value"]   # 'EGFR'
```
On the command line, the tool **`jq`** does the same: `jq '.genes[0].geneName.value'`.

**Common mistake:** assuming every field exists. Many entries have no gene name, so use `.get()` with a default. The
repository's [`dsls/uniprot.py`](../../src/dsls/uniprot.py) flattens nested JSON safely into one table row per protein.

---

## Lesson 3 · Pagination: large results come in pages

**In one sentence:** APIs return big result sets a page at a time, and your code must follow the "next page" link
until there are no more.

**The idea in plain language.** Like search engine results, you get the first 100 and a link to the next 100.
Different databases tell you where the next page is in different ways:

| Database | Where the "next" link is |
|----------|--------------------------|
| UniProt | in an HTTP **header** called `Link` |
| ChEMBL | inside the JSON: `page_meta.next` |
| MGnify | inside the JSON: `links.next` |
| ENA Portal | no paging: `limit=0` returns everything at once |

**What it looks like in code:**
```python
url = "https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL203&standard_type=IC50&limit=1000"
records = []
while url:
    page = requests.get(url, timeout=60).json()
    records += page["activities"]
    url = page["page_meta"]["next"] and "https://www.ebi.ac.uk" + page["page_meta"]["next"]
```

**Common mistake:** silently getting only the first page. **Always compare how many records you got with how many the
API says exist.** Every notebook in this repository does this with an `assert`. That check caught a real bug: UniProt's
next-page URLs contain commas, and an early parser split on commas.

---

## Lesson 4 · Being a good API citizen: retries, rate limits and caching

**In one sentence:** public servers are shared and sometimes fail, so polite, robust code retries carefully, respects
limits and saves what it has downloaded.

**The ideas:**
- **Retry with backoff:** wait 1 s, then 2 s, then 4 s… before retrying a failed request, so a struggling server isn't
  hammered.
- **Rate limits:** HTTP **429** means "too many requests". Honour the `Retry-After` header.
- **Caching:** store every response on disk. Re-running then costs nothing, works offline, and reproduces exactly the
  same data.
- **Provenance:** record *when* you fetched data and *which release*, because databases change.

**See it in this repository:** [`src/dsls/ebi_api.py`](../../src/dsls/ebi_api.py) does all four, and it is unit-tested with a
fake server ([`tests/test_ebi_api.py`](../../tests/test_ebi_api.py)).

**Why it matters at work:** pipelines that fetch data every night must survive outages. This is a standard
data-engineering skill.

---

## Lesson 5 · From study to sample to run: how sequencing data is organised

**In one sentence:** in ENA and MGnify, a **study** contains **samples**, each sample is sequenced in one or more
**runs**, and analyses are computed from runs.

**Background you need.** A sequencing machine doesn't read a whole genome in one go. It produces millions of short
**reads**, and one batch of reads from one sample is a **run**. A **metagenome** is the DNA of *all* the organisms in
an environmental sample (seawater, soil, the gut), sequenced together.

```
(illustrative; read counts are typical values from the analysis)
Study  PRJEB402  "Tara Oceans" ──► Sample SAMEA2731342 (seawater, station 64, 5 m depth)
                                        ├──► Run ERR... (metagenome, HiSeq 2000, 160 M reads)
                                        └──► Run ERR... (16S amplicon, MiSeq, 1.5 M reads)
```

**See it in this repository:** the [Tara Oceans inventory](implementation/03_ena_tara_oceans_runs.ipynb) lists all 6,423
runs of one project and summarises their instruments and read counts.

---

## Lesson 6 · Bioactivity data and potency (ChEMBL)

**In one sentence:** ChEMBL collects measurements of how strongly molecules affect biological targets. The most
common is **IC50**, usually converted to **pIC50** so that bigger numbers mean more potent.

**Background you need.**
- **IC50** = the drug concentration that reduces the target's activity by half. 10 nM is more potent than 1,000 nM.
- Concentrations span many orders of magnitude, so we use a log scale: **pIC50 = −log10(IC50 in mol/L)**. Then
  1 µM → 6, 100 nM → 7, 10 nM → 8, 1 nM → 9. One unit is a 10× difference.
- Measurements of the same compound vary between labs. In this repository the median spread was about 4-fold, so
  small differences between papers are noise.

**What it looks like in code:**
```python
import numpy as np
ic50_nM = np.array([1000, 100, 10])
pic50 = -np.log10(ic50_nM * 1e-9)   # array([6., 7., 8.])
```

**See it in this repository:** the [EGFR analysis](implementation/02_chembl_egfr_ic50.ipynb) shows how drug resistance
appears in the data: first-generation drugs lose about 50× potency on the T790M mutant, while third-generation drugs
were designed for it.

---

## Lesson 7 · Cleaning is part of collection

**In one sentence:** data from APIs is never analysis-ready, and the decisions you make while cleaning are part of your
results and must be **counted and reported**.

**Examples from this repository:**
- ChEMBL: 10.9 % of records were the same values re-reported in a later paper (potential duplicates).
- ENA: collection dates exist only in free-text descriptions, and size fractions are spelled 22 different ways.
- UniProt: 14 sequences are fragments, so they "lack" features simply because they're incomplete.

**A professional habit:** build a **funnel table** showing records at each step and how many each filter removed.
Reviewers can then disagree with a step and see its effect.
