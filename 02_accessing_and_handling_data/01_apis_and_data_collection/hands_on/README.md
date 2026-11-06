# Hands-on: APIs & Python for data collection

My workspace for the practical of [02.1 · APIs & Data Collection](../), following the instructions on
slides 22–24 of [the session slides](../course_materials/APIs_and_Python_for_data_collection.pdf).

```
hands_on/
├── README.md                    ← this guide (setup, steps, checklist, notes)
├── start.sh                     ← one-command launcher (venv + checks + Jupyter Lab)
├── check_setup.py               ← verifies packages, jq and API access
├── requirements.txt             ← packages for this practical (mgnipy pinned, see below)
├── part0_first_api_call/
│   └── first_api_call.sh        ← Part 0: first API call from the terminal
└── python-data-tutorials/       ← full copy of github.com/SandyRogers/python-data-tutorials (Apache-2.0)
    ├── apis.ipynb               ← Part 1
    ├── intro_to_data_handling_and_viz.ipynb   ← Part 2
    ├── intro_to_ml.ipynb        ← used later in 03.1
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

## Optional · Snakemake pipeline
Follow `python-data-tutorials/snakemake_pipeline_tutorial/README.md` (needs `pip install snakemake`); compare your
version with `snakemake_pipeline_solution/`.

## ✅ Progress
- [ ] Part 0: first API call
- [ ] Part 1: MGnify via curl/jq
- [ ] Part 1: MGnify via MGnipy + pandas
- [ ] Part 1: ENA Portal API
- [ ] Part 2: data handling & anonymisation task
- [ ] Part 2: visualisation
- [ ] Optional: Snakemake pipeline

## 📝 My Notes
_Answers, surprises, errors and what I'd do differently._

---
*Tested 2026-11-06 with mgnipy 0.1.3 and pandas 2.3.3 (installed by `start.sh`): every solution cell in both notebooks runs. The only errors
come from the intentional `...` exercise blanks and the known issue above.*
