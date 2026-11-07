"""Fetch and tidy ENA read-run metadata (Portal API ``result=read_run``).

The Portal API returns every matching row in one TSV response when ``limit=0``. :func:`fetch_runs` checks the row
count against the API's own ``/count`` endpoint, so a truncated download can't pass silently.
"""

from __future__ import annotations

import io
import re

import pandas as pd

from dsls.ebi_api import EBIClient, ena_portal

#: Run-level fields requested by :func:`fetch_runs`.
RUN_FIELDS = (
    "run_accession,experiment_accession,sample_accession,study_accession,study_title,instrument_platform,"
    "instrument_model,library_strategy,library_source,library_selection,library_layout,nominal_length,read_count,"
    "base_count,fastq_bytes,first_public,scientific_name,lat,lon,depth,collection_date,country,"
    "environment_feature,environment_material"
)
_PLACEHOLDER = re.compile(r"ENVO:x+", re.IGNORECASE)
_MISSING_TEXT = {"", "unspecified", "not provided", "not applicable", "missing", "na", "n/a", "unknown"}


def fetch_runs(accession: str, fields: str = RUN_FIELDS, client: EBIClient | None = None) -> pd.DataFrame:
    """All read runs for a study/project accession (umbrella projects include their sub-studies)."""
    client = client or ena_portal(timeout=300)
    query = f"study_accession={accession}"
    expected = int(
        client.get("count", {"result": "read_run", "query": query}, accept="text/plain").text.split()[-1]
    )
    text = client.get(
        "search",
        {"result": "read_run", "query": query, "fields": fields, "limit": 0, "format": "tsv"},
        accept="text/plain",
    ).text
    df = pd.read_csv(io.StringIO(text), sep="\t", dtype=str)
    if len(df) != expected:
        raise ValueError(f"ENA returned {len(df)} runs but /count reports {expected} for {accession}")
    for col in ("read_count", "base_count", "nominal_length", "lat", "lon", "depth"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "fastq_bytes" in df:
        df["fastq_bytes"] = df["fastq_bytes"].map(sum_bytes)
    if "first_public" in df:
        df["first_public"] = pd.to_datetime(df["first_public"], errors="coerce")
    return df


def sum_bytes(value: str | float | None) -> int | None:
    """ENA lists one size per FASTQ file, separated by ``;`` (two for paired-end); return the total."""
    if value is None or (isinstance(value, float) and pd.isna(value)) or str(value).strip() == "":
        return None
    return sum(int(v) for v in str(value).split(";") if v.strip())


def assay_type(strategy: str | None, source: str | None) -> str:
    """Readable assay label from ENA's ``library_strategy`` + ``library_source``."""
    strategy, source = (strategy or "").upper(), (source or "").upper()
    if strategy == "AMPLICON":
        return "Amplicon (marker gene)"
    if strategy == "RNA-SEQ" or source == "METATRANSCRIPTOMIC":
        return "Metatranscriptome"
    if strategy == "WGA":
        return "Single-cell genome (WGA)"
    if strategy == "WGS" and source == "METAGENOMIC":
        return "Metagenome"
    if strategy == "WGS":
        return "Genome (WGS)"
    return "Other"


def is_placeholder(value: str | None) -> bool:
    """True for ontology terms left as templates, e.g. ``"deep chlorophyll maximum layer (ENVO:xxxxxxxx)"``."""
    return bool(value) and isinstance(value, str) and bool(_PLACEHOLDER.search(value))


def completeness(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Per-field share of runs with a usable value (missing, blank or 'unspecified'-style text counts as empty)."""
    columns = columns or list(df.columns)
    rows = []
    for col in columns:
        s = df[col]
        empty = s.isna() | s.astype(str).str.strip().str.lower().isin(_MISSING_TEXT)
        rows.append({"field": col, "filled": float((~empty).mean()), "empty_runs": int(empty.sum())})
    return pd.DataFrame(rows).sort_values("filled").reset_index(drop=True)


#: Sample-level fields requested by :func:`fetch_samples`.
SAMPLE_FIELDS = "sample_accession,sample_alias,collection_date,country,depth,lat,lon,checklist,description"


def fetch_samples(
    accessions: list[str], fields: str = SAMPLE_FIELDS, client: EBIClient | None = None, batch: int = 200
) -> pd.DataFrame:
    """Sample records for a list of accessions, requested in batches to keep URLs short.

    Searching samples by ``study_accession`` can miss samples that runs reference (for Tara Oceans, 448 of 1,940),
    so this looks them up directly from the run table's ``sample_accession`` column.
    """
    client = client or ena_portal(timeout=300)
    accessions = sorted(set(accessions))
    frames = []
    for i in range(0, len(accessions), batch):
        text = client.get(
            "search",
            {
                "result": "sample",
                "includeAccessions": ",".join(accessions[i : i + batch]),
                "fields": fields,
                "limit": 0,
                "format": "tsv",
            },
            accept="text/plain",
        ).text
        frames.append(pd.read_csv(io.StringIO(text), sep="\t", dtype=str))
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=fields.split(","))
    missing = set(accessions) - set(df["sample_accession"])
    if missing:
        raise ValueError(f"{len(missing)} sample accessions not returned by ENA, e.g. {sorted(missing)[:3]}")
    return df
