# Hands-on: APIs & Python for data collection

My workspace for the practical of [02.1 · APIs & Data Collection](../), following the instructions on
slides 22–24 of [the session slides](../course_materials/APIs_and_Python_for_data_collection.pdf).

```
hands_on/
├── README.md                    ← this guide (setup, steps, checklist, notes)
├── start.sh                     ← one-command launcher (venv + checks + Jupyter Lab)
├── check_setup.py               ← verifies packages, jq and API access
├── run_snakemake.sh             ← run the Snakemake exercise from any folder
├── requirements.txt             ← packages for this practical (mgnipy pinned, see below)
├── part0_first_api_call/
│   └── first_api_call.sh        ← Part 0: first API call from the terminal
└── python-data-tutorials/       ← full copy of github.com/SandyRogers/python-data-tutorials (Apache-2.0)
    ├── apis.ipynb               ← Part 1
    ├── intro_to_data_handling_and_viz.ipynb   ← Part 2
    ├── intro_to_ml.ipynb        ← Part 3 (also the practical for 03.1)
    ├── Pediatric Anemia Dataset…/Anemia Dataset.xlsx  ← downloaded by start.sh (CC BY 4.0, git-ignored)
    ├── people.tsv, measurements.tsv, iss-dust.png   ← data used by the notebooks
    ├── snakemake_pipeline_tutorial/   ← optional extra: build a Snakemake pipeline
    └── snakemake_pipeline_solution/   ← its solution
```

`python-data-tutorials/` is my **working copy**: I fill in the exercises there. The untouched original is kept in
[`../course_materials/python-data-tutorials/`](../course_materials/python-data-tutorials/) for reference.

## 🚀 Quick Start (one command)
```bash
bash 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/start.sh
```
This creates or repairs `.venv` if needed, runs `check_setup.py` (packages, `jq`, API connectivity), and opens
Jupyter Lab in `python-data-tutorials/`. It works from any folder and in any conda env.
`bash …/start.sh --check` runs the checks only.

## ⚠️ Terminal vs. Python: where to type what
| Where | What runs there | Example |
|-------|-----------------|---------|
| **Terminal (zsh)**: prompt like `seid@MacBook … %` | Shell commands | `curl …`, `jq`, `bash start.sh`, `jupyter lab` |
| **Jupyter notebook cell**, or a `python` session (`>>>`) | Python code | `import pandas as pd` |

Typing Python into the terminal doesn't work. On macOS `import` is also the ImageMagick screenshot tool, so
`import pandas as pd` in zsh prints a long ImageMagick help text and `delegate library support not built-in (X11)`.
That isn't a broken install: run the code in a notebook cell, or start `python` first.

Also check the prompt: `(base)` means Anaconda's base environment is active, which **doesn't** have `mgnipy`.
Use `start.sh`, or `source .venv/bin/activate` (the prompt then shows `(.venv)`).

## 0 · Setup by hand (alternative to `start.sh`; replaces the course VM and `conda activate sandy`)
From the repository root:
```bash
brew install jq                                             # JSON processor (Part 0 and apis.ipynb)
python -m venv .venv && source .venv/bin/activate
pip install -r 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/requirements.txt
```
> **Why `mgnipy==0.1.3`?** The tutorial calls `studies.bulk_fetch()`. I tested every release: 0.2.x and 0.3.0
> removed `bulk_fetch`, and 0.1.0–0.1.2 return `None` from it. 0.1.3 (the version current when the course ran in June 2026)
> runs every solution cell.

## Part 0 · First API call (terminal)
```bash
bash 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/part0_first_api_call/first_api_call.sh
```
✅ Expected: JSON from the Open-Meteo weather API, with `current.temperature_2m` (°C) for latitude 52, longitude 0.
Try changing the coordinates or adding `&current=wind_speed_10m`.

## Part 1 · `apis.ipynb`: microbial dust on the International Space Station
```bash
cd 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/python-data-tutorials
jupyter lab apis.ipynb
```
| Section | Task |
|---------|------|
| 0 | Find the dataset with EBI Search |
| 1.1 | Call the **MGnify API** with `curl` |
| 1.2 | Make the JSON readable with `jq` |
| 1.3 | Select fields and filter arrays with `jq` (study title; v6 pipeline downloads) |
| 1.4 | Download the files with `xargs curl` |
| 1.5 | Do the same in Python with **MGnipy** → pandas DataFrame; filter `pipeline_version == 'v6'` |
| 2 | Find the raw sequencing files on the **ENA Portal API** |

Each ☑️ task has a hidden **solution cell** underneath. Try first, then unfold it.

ℹ️ `mgnipy` prints many `DEBUG:` log lines when imported. They're harmless; to hide them, run
`import logging; logging.disable(logging.INFO)` in the first cell.

⚠️ **Known issue:** the cell `ssu = mgazine['Summary of SILVA-SSU taxonomies']` currently fails (`'NoneType' has no
attribute 'load'`) because the live MGnify dataset no longer has an entry with that name. Print `mgazine` to list
the available summaries and pick one that exists.

## Part 2 · `intro_to_data_handling_and_viz.ipynb`
```bash
jupyter lab intro_to_data_handling_and_viz.ipynb
```
Python lists vs. NumPy arrays → reading data with `csv` vs. **pandas** → **Task: anonymise `people.tsv`**
(hash the names, parse dates with `to_datetime`, drop `NaT`, compute ages) → save to TSV → plot `measurements.tsv`.

## Part 3 · `intro_to_ml.ipynb`: first machine-learning workflow
Iris dataset: pair plots → train/test split → random forest → precision/recall/F1 → 5-fold cross-validation →
k-means clustering (bonus: PCA projection). Then a **self-guided exercise** on the *Pediatric Anemia* dataset
(Mojumdar et al., 2024, Mendeley Data, [doi:10.17632/y7v7ff3wpj.1](https://doi.org/10.17632/y7v7ff3wpj.1), CC BY 4.0):
explore → encode categories → classify anaemia → evaluate. `start.sh` downloads the Excel file to the path the
notebook expects; `openpyxl` reads it.

## Part 4 (optional) · Snakemake data pipeline
A two-step workflow: **filter** `measurements.txt` with a shell script → **plot** a seaborn histogram with Python.

| Folder | What it is |
|--------|-----------|
| `snakemake_pipeline_tutorial/` | Scaffold to complete: the `<< what goes here ? >>` blank in the `Snakefile`, the `# TODO` in `scripts/filter_measurements.sh` (keep the header plus the first 100 names alphabetically), and the `# TODO`s in `scripts/plot_weight_histogram.py` (read the TSV with pandas, `sns.histplot` of `weight_kg`) |
| `snakemake_pipeline_solution/` | Complete reference workflow |

### ⚠️ Why the repo README's commands fail on this Mac
The upstream README says:
```bash
conda install snakemake
cd snakemake_pipeline_solution
snakemake --cores all
```
| Command | What goes wrong here | Fix |
|---------|---------------------|-----|
| `conda install snakemake` | Your conda only searches the `defaults` channel, and Snakemake isn't in it, so you get *"PackagesNotFoundError / No match found"*. Snakemake lives on **conda-forge / bioconda** | Not needed: Snakemake **9.27.1 is already installed** in `.venv` (by `start.sh`) and in Anaconda base. If you ever do want conda: `conda install -c conda-forge -c bioconda snakemake` (slow to solve in base; prefer a separate env) |
| `cd snakemake_pipeline_solution` | That folder isn't in `02_accessing_and_handling_data/`. It's 4 levels deeper, inside `hands_on/python-data-tutorials/` | Use the full path, or the helper below |
| `snakemake --cores all` | Works once you're in the right folder (tested: 3/3 steps) | — |

### ✅ What to run instead (works from any folder)
```bash
cd ~/Projects/EMBL-EBI-Data-Science-Life-Scientists-Implementation.
H=02_accessing_and_handling_data/01_apis_and_data_collection/hands_on

bash $H/run_snakemake.sh solution                      # run the complete reference workflow
bash $H/run_snakemake.sh tutorial -n                   # dry run of your scaffold
bash $H/run_snakemake.sh tutorial                      # run your completed scaffold
bash $H/run_snakemake.sh tutorial --sdm conda          # bonus: per-rule conda environments
bash $H/run_snakemake.sh solution --delete-all-output  # clean results and start again
```
Or the manual equivalent of the upstream README:
```bash
source .venv/bin/activate
cd 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/python-data-tutorials/snakemake_pipeline_solution
snakemake --cores all
```
✅ Expected outputs: `results/filtered_measurements.tsv` (header + 100 rows) and `results/weight_histogram.png`.
These and `.snakemake/` are git-ignored. Until you fill in the blanks, the tutorial version stops with
`SyntaxError … << what goes here ? >>`. That's expected.

🏅 **Bonus challenge (from the repo README):** make the `plot_histogram` rule run in its **own conda environment**,
with its Python dependencies listed in a YAML file. Hints: the rule-level `conda:` directive in the
[Snakemake docs](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#integrated-package-management);
run with `bash run_snakemake.sh tutorial --sdm conda`. Conda is available on this Mac (Anaconda, `conda 26.1.1`), but
because your conda only uses the `defaults` channel, list `channels: [conda-forge, bioconda]` **inside your env YAML**.

## ✅ Progress
- [ ] Part 0: first API call
- [ ] Part 1: MGnify via curl/jq
- [ ] Part 1: MGnify via MGnipy + pandas
- [ ] Part 1: ENA Portal API
- [ ] Part 2: data handling & anonymisation task
- [ ] Part 2: visualisation
- [ ] Part 3: Iris workflow (classification, CV, k-means)
- [ ] Part 3: anaemia self-guided exercise
- [ ] Part 4: Snakemake tutorial completed
- [ ] Part 4: bonus, per-rule conda environment

## 📝 My Notes
_Answers, surprises, errors and what I'd do differently._

---
*Tested 2026-11-06 (mgnipy 0.1.3, pandas 2.3.3, scikit-learn 1.9.1, snakemake 9.27.1):*
- *`python-data-tutorials/` matches GitHub commit `f2872ae` byte for byte (22/22 files)*
- *`apis.ipynb` and `intro_to_data_handling_and_viz.ipynb`: every solution cell runs; the only errors are the intentional `...` blanks and the known issue above*
- *`intro_to_ml.ipynb`: runs with no errors, including the anaemia dataset*
- *`snakemake_pipeline_solution`: 3/3 steps succeed; the tutorial version stops at its intended blanks*
