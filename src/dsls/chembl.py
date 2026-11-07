"""Curate ChEMBL bioactivity records into one potency value per compound (and target variant).

ChEMBL aggregates measurements from thousands of papers, so raw activity rows contain censored values
(``>10000 nM``), records flagged by curators, values re-reported from earlier papers, and the same compound
measured in many assays. :func:`curate` applies explicit, counted filters; :func:`aggregate` collapses
repeated measurements to a median.
"""

from __future__ import annotations

import re

import pandas as pd

#: Fields to request from ``chembl/api/data/activity.json`` (passed as ``only=``).
ACTIVITY_FIELDS = (
    "activity_id,molecule_chembl_id,parent_molecule_chembl_id,molecule_pref_name,canonical_smiles,"
    "standard_type,standard_relation,standard_value,standard_units,pchembl_value,assay_chembl_id,assay_type,"
    "assay_description,assay_variant_mutation,bao_label,document_chembl_id,document_year,"
    "data_validity_comment,potential_duplicate"
)
WILD_TYPE = "WT"
#: ChEMBL's label for "a mutant was used, but which one isn't recorded".
UNDEFINED = "undefined mutant"
_POSITION = re.compile(r"(\d+)")


def normalise_variant(mutation: str | None) -> str:
    """Canonical label for a ChEMBL ``assay_variant_mutation`` string.

    ``None`` / empty → ``"WT"``; ChEMBL's ``"UNDEFINED MUTATION"`` → ``"undefined mutant"``; otherwise mutations are de-duplicated, ordered by residue position and joined
    with ``/``, so ``"T790M,L858R"`` and ``"L858R, T790M"`` both become ``"T790M/L858R"`` (790 < 858).
    """
    if mutation is None or (isinstance(mutation, float) and pd.isna(mutation)):
        return WILD_TYPE
    if "UNDEFINED" in str(mutation).upper():
        return UNDEFINED
    parts = {p.strip() for p in re.split(r"[,;/\s]+", str(mutation)) if p.strip()}
    if not parts or {p.upper() for p in parts} <= {"WT", "WILD", "TYPE", "WILD-TYPE", "NONE"}:
        return WILD_TYPE

    def position(p: str) -> tuple[int, str]:
        m = _POSITION.search(p)
        return (int(m.group(1)) if m else 10**6, p)

    return "/".join(sorted(parts, key=position))


def curate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the standard filters and return ``(clean_df, funnel)``.

    Steps (each counted in ``funnel``):

    1. exact values only: ``standard_relation == "="`` and a pChEMBL value present
    2. drop records with a ChEMBL ``data_validity_comment`` (e.g. "Outside typical range", "Potential transcription error")
    3. drop ``potential_duplicate == 1`` (the value was already reported in an earlier document)

    Adds ``pIC50`` (float), ``variant`` (normalised), ``assay_kind`` (``biochemical`` / ``cell-based`` / ``other``).
    """
    funnel = [("retrieved", len(df))]
    out = df.copy()
    out["pchembl_value"] = pd.to_numeric(out["pchembl_value"], errors="coerce")
    out = out[(out["standard_relation"] == "=") & out["pchembl_value"].notna()]
    funnel.append(("exact value with pChEMBL", len(out)))
    out = out[out["data_validity_comment"].isna()]
    funnel.append(("no data-validity flag", len(out)))
    out = out[pd.to_numeric(out["potential_duplicate"], errors="coerce").fillna(0) != 1]
    funnel.append(("not a potential duplicate", len(out)))

    out = out.assign(
        pIC50=out["pchembl_value"].astype(float),
        variant=out["assay_variant_mutation"].map(normalise_variant),
        assay_kind=out["assay_type"].map({"B": "biochemical", "F": "cell-based"}).fillna("other"),
        document_year=pd.to_numeric(out["document_year"], errors="coerce").astype("Int64"),
    )
    funnel_df = pd.DataFrame(funnel, columns=["step", "records"])
    funnel_df["removed"] = (-funnel_df["records"].diff()).fillna(0).astype(int)
    return out.reset_index(drop=True), funnel_df


def aggregate(df: pd.DataFrame, by: list[str] | None = None) -> pd.DataFrame:
    """One row per group (default: parent compound × variant × assay kind) with median pIC50, spread and count."""
    by = by or ["parent_molecule_chembl_id", "variant", "assay_kind"]
    return (
        df.groupby(by, observed=True)["pIC50"]
        .agg(pIC50_median="median", pIC50_sd="std", n_measurements="size")
        .reset_index()
    )


def has_mutation(variant: str, mutation: str) -> bool:
    """True if the normalised ``variant`` label contains ``mutation`` (e.g. ``"T790M"``)."""
    return mutation in variant.split("/")
