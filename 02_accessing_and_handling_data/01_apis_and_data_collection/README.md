# 02.1 · APIs & Data Collection

> **Status:** ✅ Implementation complete (4 / 4 tasks) · **Trainer:** Sandy Rogers (Project Leader, MGnify Web & Platform) ·
> **Course page:** [Introduction to APIs and Python for data collection](https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/accessing-and-handling-data-with-python/introduction-to-apis-and-python-for-data-collection/)

## Overview
> 🎓 **New to the field?** [`LESSONS.md`](LESSONS.md) explains this material in plain language, with no biology or data-science background assumed.

Clicking through a website doesn't scale to hundreds of samples. This session teaches **programmatic data access**:
calling EMBL-EBI web APIs to search, filter and download data with code. Every step is then repeatable and auditable.

## 📚 Course Materials Explained
_Official EMBL-EBI material, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); sources and credits in [`course_materials/ATTRIBUTION.md`](course_materials/ATTRIBUTION.md)._

### [`course_materials/APIs_and_Python_for_data_collection.pdf`](course_materials/APIs_and_Python_for_data_collection.pdf) (24 slides)
- **Why Python:** readable, good for both quick scripts and full libraries, with a large ecosystem
  (`pandas`, `numpy`, `scikit-learn`, `requests`/`httpx`, `matplotlib`/`seaborn`)
- **Ways to package Python work:** scripts (`uv` recommended), command-line tools, web apps (Dash/Streamlit/Shiny),
  GUI/TUI tools (`click`, Textual), and notebooks (Jupyter, Quarto)
- **"If you learn one thing…"**: *pandas* for data handling, *seaborn* for visualisation
- **What an API is:** a contract that says "I, web service X, will give you data at these URLs in this format"
- **EMBL-EBI APIs showcased:** ENA Portal API, MGnify API, AlphaFold DB API
- **Uses:** bulk downloads, repeated metadata lookups for lists of IDs, and building pipelines on top of public data

### [`course_materials/python-data-tutorials/`](course_materials/python-data-tutorials/) (Apache-2.0, by Sandy Rogers)
| Notebook | What it does |
|----------|--------------|
| [`apis.ipynb`](course_materials/python-data-tutorials/apis.ipynb) | **Case study: microbial dust from the International Space Station.** Finds the study with EBI Search, then (1) calls the **MGnify API** with `curl`, pretty-prints and filters the JSON with `jq`, and downloads analysis files with `xargs curl`; (2) repeats the job in Python with the **MGnipy** client, loads the SSU taxonomic summary into a pandas DataFrame; (3) uses the **ENA Portal API** to find the raw sequencing files behind the study |
| [`intro_to_data_handling_and_viz.ipynb`](course_materials/python-data-tutorials/intro_to_data_handling_and_viz.ipynb) | Practical for [02.2](../02_handling_and_visualisation/) |
| [`intro_to_ml.ipynb`](course_materials/python-data-tutorials/intro_to_ml.ipynb) | Practical for [03.1](../../03_foundations_of_machine_learning/01_intro_and_fundamentals/) |

Each exercise has a hidden **solution cell** underneath. Try the task first, then unfold it.

## ▶️ Running the Practical
**👉 Step-by-step guide and my working copy: [`hands_on/`](hands_on/)** (Parts 0–2, setup tested, known issues).

```bash
brew install jq                       # command-line JSON processor used in apis.ipynb
pip install -r requirements.txt -r requirements-course.txt   # includes mgnipy
jupyter lab 02_accessing_and_handling_data/01_apis_and_data_collection/course_materials/python-data-tutorials/apis.ipynb
```

## 🧠 Key Concepts
- **REST API / endpoint:** a URL that returns structured data (usually JSON) instead of a web page.
- **JSON path:** a way to address part of a JSON document, e.g. `.data.attributes.title` in `jq`.
- **Pagination:** large result sets come back in pages, and the client must follow `next` links.
- **Client library:** a Python wrapper (e.g. MGnipy) that hides raw HTTP calls behind functions.
- **Study → sample → run → analysis:** how MGnify/ENA records link from metadata to raw reads.

## 🛠️ My Implementation
See [`implementation/`](implementation/).
- [x] Reusable API helper: retries, pagination and caching to `data/raw/` → [`src/dsls/ebi_api.py`](../../src/dsls/ebi_api.py), with tests
- [x] UniProt: search entries for a protein family and tabulate annotations → [aquaporin family analysis](implementation/01_uniprot_aquaporin_family.ipynb)
- [x] ChEMBL: fetch bioactivity (IC50) data for one target and plot the distribution → [EGFR inhibitors and resistance mutations](implementation/02_chembl_egfr_ic50.ipynb)
- [x] ENA: list the runs for a study and summarise read counts and instruments → [Tara Oceans run inventory and metadata audit](implementation/03_ena_tara_oceans_runs.ipynb)

## 📝 Notes & Reflections
- **One client, three APIs, three pagination styles.** UniProt pages through a `Link` header, ChEMBL through
  `page_meta.next`, and ENA returns everything in one response. Putting retries, caching and pagination in one tested
  client ([`ebi_api.py`](../../src/dsls/ebi_api.py)) meant each analysis notebook only had to deal with the science.
- **Check counts, not just status codes.** Every notebook asserts that it received as many records as the API says
  exist. That assertion is what made a pagination bug (UniProt) and an unreliable API (ChEMBL) visible.
- **Data problems outnumbered code problems.** Each database had its own quirk, and none showed up until I looked at real
  outputs:
  - UniProt: fragments look like missing hallmarks.
  - ChEMBL: re-reported duplicates, and point-mutation-only variant fields.
  - ENA: collection dates exist only in free text, and ontology IDs are left as `ENVO:xxxxxxxx` templates.
- **FAIR in practice:** all three resources are open, but how *findable* the data are depends on the submitter's
  metadata. The Tara Oceans audit is a concrete example: date-based search returns none of a 6,423-run flagship project.
