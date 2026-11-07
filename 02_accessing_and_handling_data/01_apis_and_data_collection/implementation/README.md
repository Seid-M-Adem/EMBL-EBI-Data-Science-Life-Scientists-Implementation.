# 02.1 · My Implementation

My own work for [02.1 APIs & Data Collection](../): a reusable API client, and analyses built on it.

| File | What it is |
|------|------------|
| [`01_uniprot_aquaporin_family.ipynb`](01_uniprot_aquaporin_family.ipynb) | **UniProt analysis of the aquaporin water-channel family.** Retrieves all 332 reviewed members via the REST API (4 paginated requests), flattens them into a table, and asks five questions: taxonomic spread, conservation of the family hallmarks (6 helices, 2 NPA motifs), length, structural coverage, subcellular location. Separates data artefacts (fragments, annotation gaps) from real biology (non-canonical NPC/NPG motifs) |
| [`figures/`](figures/) | Figures saved by the notebook |
| [`../../../src/dsls/ebi_api.py`](../../../src/dsls/ebi_api.py) | **Reusable EMBL-EBI API client** (used by this and later modules): retries with backoff and `Retry-After`, pagination strategies for UniProt / ChEMBL / MGnify, an on-disk cache with provenance (URL, time, data release) |
| [`../../../src/dsls/uniprot.py`](../../../src/dsls/uniprot.py) | Flattens UniProtKB JSON entries into analysis-ready records |
| [`../../../tests/`](../../../tests/) | 21 offline unit tests (fake HTTP session) + 1 live smoke test; run in CI on every push |

## Key results (UniProt release 2026_04)

![Reviewed aquaporins by group](figures/01_taxonomic_distribution.png)

- **83 %** of the 332 proteins carry both hallmarks (87 % of complete sequences). All 14 fragments lack one,
  simply because they're incomplete.
- **Genuine exceptions:** AQP11 has an **NPC** motif (4 mammals), and microsporidian aquaporins have **NPG** (5 proteins).
- **Structures are scarce and skewed:** 23 proteins (7 %) have PDB entries, mostly from animals. Plants have the most
  proteins (117) but only 3 with structures.
- **Compartments by lineage:** vacuole membrane only in plants, basolateral/vesicle membranes only in animals.

Full reasoning is in the notebook's *Findings* section.

## Engineering notes
- **Testing caught what it should, and the live data caught what the tests missed.** The first version split UniProt's
  `Link` header on commas, but UniProt's next-page URLs contain commas (`fields=accession,length,…`). The fake-data tests
  passed; the first real 4-page query returned HTTP 404 on page 2. It's fixed with a regex parser, plus a regression test
  using a realistic URL.
- **Assertions as guards:** the notebook asserts that the number of entries retrieved equals UniProt's
  `X-Total-Results`, so a pagination bug can't silently produce a smaller dataset.

## Run it
```bash
make setup      # installs the dsls package (editable) and test tools
make test       # 21 offline tests
make lab        # open this notebook with the "Python 3 (EMBL-EBI DS .venv)" kernel → Run All
```
The first run calls the API (~5 s). Later runs read the cache in `data/raw/api_cache/uniprot/` and are offline and
reproducible. Delete that folder to fetch a newer UniProt release.

*UniProt data: [CC BY 4.0](https://www.uniprot.org/help/license). The UniProt Consortium, UniProt: the Universal Protein Knowledgebase.*
