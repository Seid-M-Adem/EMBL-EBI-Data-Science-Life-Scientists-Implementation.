# FAIR in this repository: what I do, and where it falls short

The lecture introduces the **FAIR principles** (Findable, Accessible, Interoperable, Reusable;
[Wilkinson et al., 2016](https://doi.org/10.1038/sdata.2016.18)). They were written for *data*, but the same ideas
apply to an analysis repository: could someone else find, run and trust what I did? Below, each principle is mapped to
concrete practices in this repo, with links. The gaps are listed honestly at the end.

## How the repository applies FAIR

| Principle | What it asks | How this repo does it |
|-----------|--------------|-----------------------|
| **F**indable | Persistent identifiers; rich metadata; indexed | Every dataset is named by its **accession** (UniProt `P00533`, ChEMBL `CHEMBL203`, ENA `PRJEB402`) and the database **release** (`2026_04`, `ChEMBL_37`) is printed in the notebook. Course material is cited by its **DOI** ([`COURSE_MATERIALS.md`](../../COURSE_MATERIALS.md)). A [`CITATION.cff`](../../CITATION.cff) makes the repo citable. Each module README indexes its files. |
| **A**ccessible | Retrievable by identifier over a standard, open protocol | All data come from **open HTTPS APIs** without authentication, through one client ([`ebi_api.py`](../../src/dsls/ebi_api.py)). Course files that can't be redistributed are fetched by a script ([`scripts/fetch_course_materials.sh`](../../scripts/fetch_course_materials.sh)) instead of being committed. |
| **I**nteroperable | Standard formats and vocabularies; qualified references | Plain, standard formats (TSV/CSV, JSON, FASTA, `.ipynb`). Joins use **stable accessions** rather than names. 02.2 shows why: names such as "Aquaporin-5" mean different things in different kingdoms. The cross-reference walk ([`01_egfr_cross_reference_walk.ipynb`](01_egfr_cross_reference_walk.ipynb)) checks that identifiers resolve across six resources. |
| **R**eusable | Clear licence; detailed provenance; community standards | **Licences** are explicit and kept separate: MIT for my code, CC BY 4.0 / Apache-2.0 / MIT for course material, with per-folder `ATTRIBUTION.md` ([`LICENSE-SCOPE.md`](../../LICENSE-SCOPE.md)). **Provenance:** every API response is cached with its request URL, fetch time and release headers (`data/raw/api_cache/<resource>/*.meta.json`). **Raw is never edited:** `data/raw/` holds data as retrieved, `data/processed/` only holds outputs of code ([`data/README.md`](../../data/README.md)). **Environment:** flexible ranges in `requirements*.txt`, plus the exact tested versions in [`requirements-lock.txt`](../../requirements-lock.txt). **Correctness:** 60+ unit tests run in CI on every push. |

## Practices that come from FAIR thinking

- **Integrity checks, not assumptions.** Each retrieval asserts that it received as many records as the API reports
  (UniProt `X-Total-Results`, ChEMBL `total_count`, ENA `/count`), and joins use `validate="one_to_one"`.
- **Every filter is counted.** Curation steps report how many records each one removed (e.g. the ChEMBL funnel), so a
  reader can disagree with a step and see its effect.
- **Parsing is measured, not assumed.** When information exists only as free text (Tara Oceans sample descriptions),
  the notebook reports the parse rate (88–92 %) and leaves unparsed values empty rather than guessing.
- **Release-aware results.** The headline numbers in each README name the database release, because UniProt, ChEMBL
  and ENA all change under a fixed query.

## What I learned by auditing other people's metadata

The [Tara Oceans audit](../../02_accessing_and_handling_data/01_apis_and_data_collection/implementation/03_ena_tara_oceans_runs.ipynb)
showed how open data can still be hard to *find*:
- collection date and country are empty in 100 % of structured fields, and exist only inside prose;
- 82 % of runs carry an ontology placeholder (`ENVO:xxxxxxxx`) rather than a real term;
- size fractions are spelled 22 different ways.

The data are fully **Accessible** but only partly **Findable** and **Interoperable**: a search by date or country
returns none of a 6,423-run flagship project. Writing structured metadata at submission time costs minutes; recovering it
later costs a regex and still misses about 10 %.

## Honest gaps

| Gap | Why it matters | What would close it |
|-----|----------------|---------------------|
| Raw data and API caches are **not committed** | Re-running depends on the APIs still serving the same data; releases change results | Deposit the cached raw data for each published result in Zenodo and cite the DOI (planned, user-side) |
| **No persistent identifier** for the repo itself | GitHub URLs can change (the repo name may be cleaned up) | Archive a release on Zenodo to mint a DOI, and add it to `CITATION.cff` |
| Lock file is **platform-specific** (macOS arm64, Python 3.13) | PyTorch wheels differ by OS/GPU | Optionally a container image; the flexible requirements already install on Linux CI |
| Some results depend on **live services** that fail (ChEMBL had two full outages while I worked) | A notebook can't be re-run during an outage | Caching makes completed runs replayable offline; a committed small sample would help newcomers |
| ENA has **no release numbers** | "Retrieved on" dates are the only version stamp | Recorded in cache metadata and in README headings |
