# 01 · Introduction to EMBL-EBI

> **Status:** 🟡 In progress · **Trainer:** Dr Colman O'Cathail (ENA Project Lead) ·
> **Course page:** [Introduction to EMBL-EBI, its role, and mission](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/introduction-to-embl-ebi-its-role-and-mission/)

## Overview
This session sets the context for the whole course. It explains **where public life-science data comes from**
and who looks after it. EMBL-EBI runs many of the world's core biological databases (ENA, UniProt, PDBe,
ChEMBL, Ensembl, MGnify, …). Knowing what each one holds is the first step in any data-science project in biology.

## 📚 Course Materials Explained

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

> ⚠️ This file isn't part of the CC BY course download, and its licence hasn't been checked. Confirm it may be
> redistributed before publishing the repository; otherwise move it into a git-ignored folder.

## 🧠 Key Concepts
- **Data resource:** a structured, accessible collection of data, plus the tools, infrastructure and documentation to store, find and reuse it.
- **FAIR principles:** data should be Findable, Accessible, Interoperable and Reusable.
- **Primary vs. added-value databases:** archives such as ENA store data as submitted; curated resources such as UniProt add expert annotation.

## 🛠️ My Implementation (planned)
- [ ] One-page map of the EMBL-EBI resources used later in this repository (ENA, MGnify, UniProt, ChEMBL, PDBe, TCGA via UCSC Xena)
- [ ] Short notes on FAIR data and how this repository follows it (raw vs. processed data, reproducible fetch script)

## 📝 Notes & Reflections
_Key takeaways, challenges, and design decisions will be recorded here as the work is completed._
