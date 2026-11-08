"""Loading and cleaning the molecular-replacement (MR) success dataset from the course's ``DataScience_EBI`` tutorial.

Each row is one X-ray diffraction sweep for which molecular replacement was attempted; ``MR_success`` (0/1) says
whether it worked. Several sweeps can belong to the same crystal target (``pdb_id_id``), so rows are **not**
independent: always split by target (e.g. ``StratifiedGroupKFold(groups=...)``).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LABEL = "MR_success"
GROUP = "pdb_id_id"
ID_COLUMNS = ["sweep_id", "pdb_id_id"]

#: The 27 features used by the course's training notebooks: data-quality statistics plus descriptors known
#: *before* MR is run (e.g. ``eLLG``, the expected log-likelihood gain).
COURSE_FEATURES = [
    "wavelength", "mr_reso", "mr_sg_no", "eLLG", "tncs", "model_res", "anomalousCC", "IoverSigma", "completeness",
    "diffI", "RmergeI", "lowreslimit", "RpimI", "multiplicity", "RmeasdiffI", "anomalousslope", "diffF",
    "wilsonbfactor", "RmeasI", "highreslimit", "RpimdiffI", "anomalousmulti", "RmergediffI", "totalobservations",
    "anomalouscompl", "cchalf", "totalunique",
]  # fmt: skip

#: Statistics produced *by* the MR run. ``MR_success`` is judged from them, so using them as inputs is target leakage.
POST_MR_FEATURES = ["TFZ", "LLG", "PAK", "VRMS"]


def standard_space_group(number: int) -> int:
    """Map CCP4 non-standard setting codes to the International Tables number (1–230).

    CCP4 numbers alternative axis settings by adding multiples of 1000, e.g. ``1018`` (P 2 21 21) and ``2018``
    (P 21 2 21) are both settings of space group 18 (P 21 21 2).
    """
    standard = int(number) % 1000
    if not 1 <= standard <= 230:
        raise ValueError(f"not a space-group number: {number!r}")
    return standard


def load_mr_data(path: str | Path) -> pd.DataFrame:
    """Read ``data.csv`` and fix the issues found in the data audit.

    * numbers written with thousands separators (``"2,449.00"``) are parsed as numbers;
    * ``mr_sg_no`` is mapped to standard space-group numbers (it remains a *category*, not a quantity);
    * ``model_res == 0`` (a model resolution of 0 Å is impossible) becomes missing, to be imputed in a pipeline;
    * ``MR_success`` becomes an integer label.
    """
    df = pd.read_csv(path, thousands=",")
    df["mr_sg_no"] = df["mr_sg_no"].map(standard_space_group)
    df["model_res"] = df["model_res"].mask(df["model_res"] == 0, np.nan)
    df[LABEL] = df[LABEL].astype(int)
    return df


def subsample_prevalence(df: pd.DataFrame, prevalence: float, seed: int = 0) -> pd.DataFrame:
    """Keep every negative row and add whole positive *targets* until positives make up ≈ ``prevalence``.

    Used to simulate a rarer outcome without breaking the grouping (a target is kept or dropped as a whole).
    Requires that all rows of a target share the same label.
    """
    if not 0 < prevalence < 1:
        raise ValueError("prevalence must be between 0 and 1")
    per_target = df.groupby(GROUP)[LABEL].agg(["min", "max", "size"])
    if (per_target["min"] != per_target["max"]).any():
        raise ValueError("some targets have mixed labels; target-level subsampling would be ambiguous")
    negatives = per_target.index[per_target["max"] == 0]
    positives = per_target.index[per_target["max"] == 1].to_numpy().copy()
    np.random.default_rng(seed).shuffle(positives)

    n_neg = int(per_target.loc[negatives, "size"].sum())
    kept, n_pos = [], 0
    for target in positives:
        if n_pos / (n_pos + n_neg) >= prevalence:
            break
        kept.append(target)
        n_pos += int(per_target.loc[target, "size"])
    return df[df[GROUP].isin(set(negatives) | set(kept))]
