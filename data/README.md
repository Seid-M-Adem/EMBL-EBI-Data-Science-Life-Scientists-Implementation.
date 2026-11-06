# Data

Data files are **not** committed to version control. Each notebook/script documents how to
download or regenerate the data it uses, so every result is reproducible from source.

| Folder | Contents |
|--------|----------|
| `raw/` | Unmodified data as retrieved from source (ENA, UniProt, ChEMBL, etc.) |
| `processed/` | Cleaned, transformed, analysis-ready data produced by code in this repo |

Course datasets are fetched with `scripts/fetch_course_materials.sh --data` into
`raw/gene_expression/` and `raw/bioimaging/`; `--2025` adds the 2025 edition's single-cell dataset
(`raw/2025_gene_expression/project_data.h5ad`, 165 MB). The structural-biology images (~8 GB, Zenodo) go in
`raw/structural_biology/`; they're downloaded manually, as described in that project's README.

**Rule:** files in `raw/` are never edited by hand — all transformations happen in code.
