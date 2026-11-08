# 01 · Introduction to EMBL-EBI

> **Status:** ✅ Implementation complete (2 / 2 tasks) · **Trainer:** Dr Colman O'Cathail (ENA Project Lead) ·
> **Course page:** [Introduction to EMBL-EBI, its role, and mission](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/introduction-to-embl-ebi-its-role-and-mission/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

This session sets the context for the whole course. It explains **where public life-science data comes from**
and who looks after it. EMBL-EBI runs many of the world's core biological databases (ENA, UniProt, PDBe,
ChEMBL, Ensembl, MGnify, …). Knowing what each one holds is the first step in any data-science project in biology.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/Intro_to_EMBL-EBI.pdf`](course_materials/Intro_to_EMBL-EBI.pdf) (54 slides)
*"Unleashing the potential of big data in biology"*

| Part | What it covers |
|------|----------------|
| **Who EMBL-EBI is** | Part of EMBL (sites in Heidelberg, Hinxton, Grenoble, Hamburg, Barcelona, Rome), its member states, and its funders (member states, European Commission, UKRI, NIH, Wellcome) |
| **Mission** | Five pillars: deliver data resources · perform research · train scientists · engage with industry · coordinate bioinformatics in Europe |
| **Data resources** | The catalogue of services at [ebi.ac.uk/services](https://www.ebi.ac.uk/services), and how the resources cross-reference each other |
| **AI & ML** | Why well-curated public data underpins AI. The flagship example is **AlphaFold**, trained on UniProt, PDB and MGnify |
| **Application areas** | Bioimaging, drug discovery, genomic medicine, biosecurity (Pathogens Portal), biodiversity, sustainable food production |
| **Infrastructure, research & training** | Data centres and cloud, research groups, the PhD and postdoc programmes, the training programme, and industry partnerships (e.g. Open Targets) |

**Key takeaway:** for an ML project in biology, the quality and provenance of the training data matter as much
as the model. EMBL-EBI's curated, cross-referenced resources are the usual starting point.

### [`EMBLEBI_resources_introduction26.pptx`](EMBLEBI_resources_introduction26.pptx) (37 slides, supplementary)
*"An introduction to EMBL-EBI data resources"*: an EMBL-EBI webinar deck added alongside the course slides.
- How to **find**, **submit** and **learn about** data on the EMBL-EBI site
- Flash talks on individual resources: **ChEMBL** (compound–target bioactivity), **MetaboLights** (metabolomics),
  **Ensembl** (genome browser), **UniProt** (protein sequence and function), **PDBe / PDBe-KB** (structures),
  **MGnify** (metagenomics)
- Appendix of useful links and help-desk contacts for each resource

> Source: EMBL-EBI webinar [*An introduction to EMBL-EBI resources* (2026)](https://www.ebi.ac.uk/training/events/introduction-embl-ebi-resources-2026/),
> unmodified, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## 🧠 Key Concepts
- **Data resource:** a structured, accessible collection of data, plus the tools, infrastructure and documentation to store, find and reuse it.
- **FAIR principles:** data should be Findable, Accessible, Interoperable and Reusable.
- **Primary vs. added-value databases:** archives such as ENA store data as submitted; curated resources such as UniProt add expert annotation.

## 🛠️ My Implementation
See [`implementation/`](implementation/).
- [x] One-page map of the EMBL-EBI resources used later in this repository (ENA, MGnify, UniProt, ChEMBL, PDBe, TCGA via UCSC Xena) → [`RESOURCE_MAP.md`](implementation/RESOURCE_MAP.md), with cross-references checked in code: [`01_egfr_cross_reference_walk.ipynb`](implementation/01_egfr_cross_reference_walk.ipynb)
- [x] Short notes on FAIR data and how this repository follows it (raw vs. processed data, reproducible fetch script) → [`FAIR.md`](implementation/FAIR.md), plus [`CITATION.cff`](../CITATION.cff) and [`requirements-lock.txt`](../requirements-lock.txt)

## 📝 Notes & Reflections
- **"The resources cross-reference each other" is testable.** Following one accession (EGFR) through six APIs showed
  that the links resolve and agree, apart from a small, explainable lag between PDBe and UniProt.
- **Archives and added-value resources need different handling.** Archives (ENA) keep submitters' metadata as it was
  submitted, including errors. Curated resources (UniProt, ChEMBL) apply filters that I need to understand before I
  trust a count.
- **FAIR applies to my own work too.** Accessions, release numbers, cached raw responses with provenance, licences,
  a citation file and exact package versions are what let someone else reproduce these notebooks.
