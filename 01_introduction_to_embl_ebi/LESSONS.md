# 01 · Lessons explained: EMBL-EBI and public biological data

*For readers with no biology or data background. New words are in [`GLOSSARY.md`](../GLOSSARY.md); the overall route is in
[`LEARNING_GUIDE.md`](../LEARNING_GUIDE.md).*

**What this session teaches:** where the world's public life-science data lives, who maintains it, and how to tell
different kinds of databases apart. Every later module downloads data from these places, so this is the map of the
territory.

**Worked examples in this repo:** a [resource map](implementation/RESOURCE_MAP.md), a
[cross-reference walk from the EGFR gene to its structures, drugs and literature](implementation/01_egfr_cross_reference_walk.ipynb)
and [FAIR notes](implementation/FAIR.md).

---

## Lesson 1 · EMBL-EBI is the infrastructure behind most biological data science

**In one sentence:** EMBL-EBI (the European Bioinformatics Institute, near Cambridge, UK) runs many of the free,
public databases that biologists and data scientists download data from.

**The idea in plain language.**
Think of it as a national library, but for biological data. Scientists who publish a DNA sequence, a protein
structure or a drug measurement are usually *required* to deposit it in a public database. EMBL-EBI stores this data,
checks it, adds annotation, and gives it away free to anyone, including through code (module 02).

EMBL-EBI is part of **EMBL** (the European Molecular Biology Laboratory), an intergovernmental organisation funded by
its member states, with sites in Heidelberg, Hinxton, Grenoble, Hamburg, Barcelona and Rome. Its mission has five parts:
provide data services, do research, train scientists, work with industry, and coordinate bioinformatics in Europe.

**The resources you'll meet in this repository:**

| Resource | Holds | Everyday analogy |
|----------|-------|------------------|
| **ENA** | raw DNA/RNA sequencing reads | the archive of original recordings |
| **UniProt** | proteins: sequence, function, annotations | an encyclopedia with an entry for every protein |
| **PDBe** | experimentally determined 3-D protein structures | a museum of measured shapes |
| **AlphaFold DB** | *predicted* 3-D structures | an atlas drawn by a very good model |
| **ChEMBL** | how strongly molecules affect biological targets | a lab notebook of drug experiments from thousands of papers |
| **Ensembl** | genomes: where genes are and what they produce | a map of each genome |
| **MGnify** | analyses of microbial communities (metagenomes) | a census of microbes in a sample |
| **Europe PMC** | scientific papers | a search engine for the literature |

**See it in this repository:** [`implementation/RESOURCE_MAP.md`](implementation/RESOURCE_MAP.md) shows which resource is
used where.

**Check yourself:** *You want to know which drugs inhibit a particular protein. Which resource do you start with?*
<details><summary>Answer</summary>ChEMBL, for measured bioactivity. UniProt would tell you what the protein does, and
PDBe whether its structure has been solved with a drug bound.</details>

**Why it matters at work:** almost every bioinformatics or computational biology job uses these resources. Knowing
which one holds what saves days of searching.

---

## Lesson 2 · Primary archives vs added-value databases

**In one sentence:** some databases store data **exactly as submitted** (archives), others **curate, combine and
annotate** data (added-value resources), and you handle the two differently.

**The idea in plain language.**
- An **archive** (ENA, PDB) is like a records office. It keeps what was deposited, including the submitter's mistakes
  and inconsistencies. It's the *source of truth* for what was measured.
- An **added-value** resource (UniProt, ChEMBL, Ensembl) is like an edited reference book. Experts and pipelines read
  the archives and literature, standardise the data, link it together, and filter out problems.

**Why the difference matters in practice (from this repository):**
- ENA's Tara Oceans records have collection dates only in free text, so *you* have to clean them
  ([02.1 ENA analysis](../02_accessing_and_handling_data/01_apis_and_data_collection/implementation/03_ena_tara_oceans_runs.ipynb)).
- ChEMBL has already removed unreliable measurements from its "pChEMBL" values. If you don't know that, you might
  wrongly think your own filter did nothing
  ([02.1 ChEMBL analysis](../02_accessing_and_handling_data/01_apis_and_data_collection/implementation/02_chembl_egfr_ic50.ipynb)).
- UniProt has a **reviewed** section (Swiss-Prot, manually curated) and an **unreviewed** one (TrEMBL, automatic).
  Choosing between them changes your results.

**Common mistakes:**
- Treating an archive's metadata as clean. It rarely is.
- Not knowing what a curated resource has already filtered out, and so double-counting or misinterpreting its numbers.

**Check yourself:** *UniProt says a protein has 388 structures and PDBe says 394. Which one is wrong?*
<details><summary>Answer</summary>Probably neither. They update on different schedules, so cross-references are snapshots.
The cross-reference walk in this module found exactly this: 6 recent structures that PDBe already had and UniProt hadn't
linked yet.</details>

---

## Lesson 3 · Accessions and cross-references: how databases connect

**In one sentence:** every record has a permanent ID (**accession**), and databases point to each other's accessions;
those links are what let you combine data.

**The idea in plain language.**
Names are ambiguous ("EGFR" is a gene, a protein, and a family of receptors in many species). Accessions are not:
`P00533` in UniProt always means *human* EGFR protein. Each resource lists the matching accessions in other resources,
much like a book's references:

```
UniProt P00533 ──► ChEMBL CHEMBL203 (drug data)
               ──► PDB 1M17, 7SYD, … (structures)
               ──► AlphaFold AF-P00533-F1 (prediction)
               ──► Ensembl ENSG00000146648 (gene)
```

**What it looks like in code:**
```python
import requests
entry = requests.get("https://rest.uniprot.org/uniprotkb/P00533.json").json()
links = [(x["database"], x["id"]) for x in entry["uniProtKBCrossReferences"]
         if x["database"] in {"ChEMBL", "AlphaFoldDB"}]
print(links)   # [('AlphaFoldDB', 'P00533'), ('ChEMBL', 'CHEMBL203')]
```

**Common mistakes:**
- Joining tables on names or gene symbols instead of accessions. [02.2](../02_accessing_and_handling_data/02_handling_and_visualisation/LESSONS.md)
  shows how "Aquaporin-5" means unrelated proteins in fungi and in mammals.
- Forgetting the species: the same gene name exists in mouse, human and fly.

**See it in this repository:** [`implementation/01_egfr_cross_reference_walk.ipynb`](implementation/01_egfr_cross_reference_walk.ipynb)
follows P00533 through six resources and checks that they agree.

---

## Lesson 4 · Why curated public data underpins AI in biology

**In one sentence:** AI models in biology are only as good as the data they learn from, and decades of carefully
curated public data are why tools like AlphaFold were possible.

**The idea in plain language.**
AlphaFold learned to predict protein shapes from roughly 170,000 experimentally measured structures in the PDB, plus
sequences from UniProt and metagenomic data like MGnify's. Without public, standardised, quality-controlled archives,
there would have been nothing to train on. The same applies to your own models: **quality and provenance of training
data matter as much as the algorithm.**

**Background you need:** a *predicted* structure is not a *measured* one. AlphaFold gives a confidence score per residue
(**pLDDT**, 0–100). Low values usually mean the region is flexible or disordered, not just "badly predicted".

**See it in this repository:** the figure in the cross-reference walk compares where EGFR has *measured* structures (the
drug-binding kinase domain) with where AlphaFold is *confident* (folded domains, but not the flexible tail).

**Why it matters at work:** when evaluating any ML result in biology, first ask *what data was it trained on, and how
was that data checked?*

---

## Lesson 5 · FAIR data

**In one sentence:** **FAIR** means data should be **F**indable, **A**ccessible, **I**nteroperable and **R**eusable. It
is a checklist for making data (and analyses) useful to other people.

**The idea in plain language:**

| Letter | Question to ask | Example of failing it |
|--------|-----------------|-----------------------|
| **F**indable | Can someone search for it and find it? | Collection dates written only in free text, so a date search misses them |
| **A**ccessible | Can they download it with a standard method? | Data "available on request" from an author's email |
| **I**nteroperable | Is it in standard formats and vocabularies? | Ontology IDs left as `ENVO:xxxxxxxx` templates |
| **R**eusable | Is the licence clear, and is provenance recorded? | No licence; unknown processing steps |

**See it in this repository:** [`implementation/FAIR.md`](implementation/FAIR.md) applies the checklist to this repository
itself, including its gaps.

**Why it matters at work:** funders and journals increasingly require FAIR data management plans, and FAIR habits
(clear IDs, versions, licences, recorded processing) are what make your analyses trustworthy and reusable by colleagues.
