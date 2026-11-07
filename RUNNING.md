# How to Run Everything (any IDE)

Everything in this repository runs from **one Python environment** (`.venv`) and **one Jupyter kernel**
(**"Python 3 (EMBL-EBI DS .venv)"**), with **one command list** (`make help`). The same commands work in
macOS Terminal, VS Code, Cursor, PyCharm, JupyterLab and Anaconda Navigator. It doesn't matter which conda
environment is active.

---

## 1 · One-time setup (≈ 5 min)

```bash
cd ~/Projects/EMBL-EBI-Data-Science-Life-Scientists-Implementation.
make setup          # creates .venv, installs requirements, registers the Jupyter kernel
make check          # verifies packages, jq/curl, datasets and API access → "All good"
brew install jq     # only if `make check` reports jq missing
```

| Command | Installs |
|---------|----------|
| `make setup` | Core stack (`requirements.txt`: pandas, NumPy, scikit-learn, PyTorch, Biopython, …) and the 02.1 hands-on packages (MGnipy 0.1.3, JupyterLab, SciPy, openpyxl, Snakemake) |
| `make setup-course` | Also the large extras for the course notebooks of modules 03–05 (`requirements-course.txt`: transformers, xgboost, imbalanced-learn, pyreadr, pycytominer, …) |

> **Why `.venv` and not conda `(base)`?** Base doesn't have MGnipy, and its conda can't install Snakemake
> (only the `defaults` channel is configured). `.venv` is isolated, reproducible, and every IDE can find it.

---

## 2 · Running from each IDE

### 🖥️ Terminal (macOS Terminal, iTerm, any IDE's built-in terminal)
```bash
make help                 # list every command
make lab                  # Jupyter Lab at the repo root (all modules)
make lab-hands-on         # check the setup, then open the 02.1 hands-on notebooks
```
To use Python interactively: `source .venv/bin/activate` (the prompt shows `(.venv)`), then `python`.
⚠️ Type Python code **inside** `python`, a notebook or a `.py` file, never at the `%` prompt.
(In zsh, `import pandas as pd` runs ImageMagick's `import` tool instead.)

### 🟦 VS Code / Cursor
Settings are committed in [`.vscode/`](.vscode/), so it works out of the box:
1. **File → Open Folder…** → select the repository folder.
2. Accept **"Install recommended extensions"** (Python, Jupyter, Ruff, Snakemake, EditorConfig).
3. The interpreter is preset to `.venv` (bottom-right status bar). If it isn't: `⇧⌘P` → *Python: Select Interpreter* → `./.venv/bin/python`.
4. **Notebooks:** open any `.ipynb`, then **Select Kernel** (top-right) → *Python Environments* → `.venv`, or *Jupyter Kernel* → **Python 3 (EMBL-EBI DS .venv)**.
   Notebooks run in their own folder (`jupyter.notebookFileRoot`), so relative data paths work.
5. **Tasks:** `⇧⌘P` → *Tasks: Run Task* → every `make …` target is listed (`⇧⌘B` = `make setup`).
6. **Run/debug a script:** open it and press **F5** → *Python: current file (run in its own folder)*.
7. The integrated terminal activates `.venv` automatically.

### 🟩 PyCharm (Professional or Community)
1. **Open** the repository folder.
2. **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Virtualenv → Existing** → `<repo>/.venv/bin/python`.
3. **Notebooks** (Professional, or the Jupyter plugin): open an `.ipynb`; it uses the project interpreter. Or choose the kernel **Python 3 (EMBL-EBI DS .venv)**.
4. **Makefile targets:** the bundled *Makefile Language* plugin shows ▶ next to each target in `Makefile`. Or use the terminal (`make …`).
5. **Scripts:** right-click → *Run*. Set *Working directory* to the script's folder when a script reads relative files.

### 🟧 JupyterLab / Jupyter Notebook / Anaconda Navigator
- From the repo: `make lab`. It uses `.venv` directly.
- From an **existing** Jupyter (e.g. launched from Anaconda Navigator or `(base)`): open a notebook →
  **Kernel → Change Kernel → Python 3 (EMBL-EBI DS .venv)**. Tested: Anaconda's Jupyter runs notebooks with the `.venv` packages through this kernel.

### 🟪 Google Colab (optional, for GPU)
The 04.1/04.2 and gene-expression notebooks were written for Colab: use the Colab links in each module README.
To run them **locally** instead, skip the `google.colab` / `drive.mount` cells and point paths to local files.

---

## 3 · Every runnable item, documented

### Repository-level
| Item | What it does | How to run |
|------|--------------|-----------|
| [`Makefile`](Makefile) | One documented command per task (below) | `make help` |
| [`scripts/fetch_course_materials.sh`](scripts/fetch_course_materials.sh) | Re-downloads official slides, notebooks, Colab notebooks and tutorial repos; optionally local-only resources, datasets and the 2025 edition. Safe to re-run: existing files are skipped | `make fetch` · `make fetch-local` · `make fetch-data` · `make fetch-2025` |
| [`notebooks/00_environment_check.ipynb`](notebooks/00_environment_check.ipynb) | Prints the Python version and the versions of the key packages | Open in any IDE with the **EMBL-EBI DS** kernel |
| [`ruff.toml`](ruff.toml) + [`.github/workflows/lint.yml`](.github/workflows/lint.yml) | Lints my own code and notebooks (course materials excluded) locally and on every push | `make lint` |
| [`.vscode/`](.vscode/) | Interpreter, notebook folder, Ruff, tasks, debug configs, recommended extensions | Automatic in VS Code / Cursor |
| [`.editorconfig`](.editorconfig) | Same indentation, line endings and charset in every editor | Automatic (VS Code needs the EditorConfig extension; PyCharm has it built in) |

### Makefile targets
| Target | Purpose |
|--------|---------|
| `make setup` | Create `.venv`, install core + hands-on packages, register the kernel |
| `make setup-course` | `setup` plus the large course-notebook extras |
| `make kernel` | (Re)register `.venv` as the Jupyter kernel **Python 3 (EMBL-EBI DS .venv)**, with `OMP_NUM_THREADS=1` (prevents a PyTorch + scikit-learn deadlock on macOS) |
| `make check` | Run [`check_setup.py`](02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/check_setup.py): packages, `jq`/`curl`, the anaemia dataset, three APIs |
| `make lab` | Jupyter Lab at the repo root |
| `make lab-hands-on` | Setup check, then Jupyter Lab in the 02.1 tutorials folder |
| `make api-call` | 02.1 Part 0: first API call with `curl` + `jq` |
| `make snakemake-solution` | 02.1 Part 4: run the complete Snakemake workflow |
| `make snakemake-tutorial` | 02.1 Part 4: run your completed scaffold |
| `make snakemake-clean` | Delete both workflows' outputs |
| `make runnable` | Colab-free copies of the 04.x and gene-expression notebooks in `course_materials/local/runnable/` (existing copies are kept) |
| `make fetch` / `fetch-local` / `fetch-data` / `fetch-2025` | Course materials / local-only resources / datasets / supplementary 2025 edition |
| `make test` | My unit tests (offline); `make test ARGS="-m network"` adds the live API check |
| `make lint` | Ruff, same as CI |
| `make clean` | Remove caches and notebook checkpoints |

### 02.1 hands-on ([`hands_on/`](02_accessing_and_handling_data/01_apis_and_data_collection/hands_on/))
| Item | What it does | How to run |
|------|--------------|-----------|
| `start.sh` | Creates or repairs `.venv`, downloads the anaemia dataset, runs the setup check, opens Jupyter Lab | `make lab-hands-on` (or `--check`: `make check`) |
| `check_setup.py` | ✅/❌ report of the environment | `make check`, or F5 → *02.1 hands-on: check setup* |
| `run_snakemake.sh` | Runs the Snakemake solution or tutorial from any folder; passes extra options (`-n`, `--sdm conda`, …) | `make snakemake-solution` · `bash …/run_snakemake.sh tutorial -n` |
| `part0_first_api_call/first_api_call.sh` | Open-Meteo API call piped to `jq` | `make api-call` |
| `python-data-tutorials/apis.ipynb` | Part 1: MGnify and ENA APIs (curl/jq → MGnipy → pandas) | Open with the EMBL-EBI DS kernel |
| `python-data-tutorials/intro_to_data_handling_and_viz.ipynb` | Part 2: pandas, pseudonymisation, seaborn | Same |
| `python-data-tutorials/intro_to_ml.ipynb` | Part 3: Iris ML workflow + anaemia exercise | Same |
| `python-data-tutorials/snakemake_pipeline_{tutorial,solution}/` | Part 4: filter → plot pipeline | `make snakemake-tutorial` / `make snakemake-solution` |

### Course notebooks in other modules
| Notebook(s) | Run notes |
|-------------|-----------|
| `03.2 …/image_augmentation_colab.ipynb` | Needs `pip install tensorflow albumentations` (not in the requirements; Colab has both). Skip the `drive.mount` cells and load any local JPEG |
| `03.2 …/DataScience_EBI/tutorials/*.ipynb` | Need `make setup-course` (imbalanced-learn). They read `data.csv` from their own folder; IDEs set that working directory automatically |
| `04.1 session1A/1B`, `04.2 session2` | `make setup-course runnable`, then open the copies in `04_…/01_dnn_and_transformers/course_materials/local/runnable/`. 1B fine-tunes BERT: 3 h 15 min on this Mac's GPU (`mps`), minutes on a Colab GPU. Session 2 needs the filename fix in the [04.2 README](04_foundations_of_deep_learning/02_evaluation_and_visualisation/) |
| `05 gene_expression code/*.ipynb` | `make setup-course fetch-data runnable`, then open the copies in `05_…/gene_expression/course_materials/local/runnable/` (`Data/` is linked to `data/raw/gene_expression/`). See that README for two fixes |
| `supplementary/2025_edition/local/` | `make fetch-2025`. Python, statistics and ML notebooks run in `.venv`; the scRNA-seq project also needs `pip install scanpy`; the Cytoscape practical needs the Cytoscape desktop app |
| `05 bioimaging` (local repo) | `make fetch-local fetch-data`, then that repo's own `requirements.txt` (pinned versions) |

---

### Verified runs (2026-11-07, Apple-silicon Mac, `.venv`)
Every course notebook was executed unattended with `jupyter nbconvert --execute` on scratch or local copies:

| Module | Result |
|--------|--------|
| 02.1 hands-on | ✅ all notebooks + Snakemake solution (one `apis.ipynb` cell depends on live MGnify data) |
| 03.2 `DataScience_EBI` | ✅ 10/10 (`predict` needs your own model filename, by design) |
| 04.1 / 04.2 | ✅ 3/3 via `make runnable`, after adding `accelerate` and fixing the 1B → session 2 filename mismatch |
| 05 gene expression | ✅ 4/4 via `make runnable`; needs the EMBL-EBI DS kernel (it sets `OMP_NUM_THREADS=1` for part 2) and a one-word fix in `01_data_download` ([details](05_group_projects/gene_expression/)) |
| 05 bioimaging | ✅ 6/7; `01_dl_protocol` stops at its "Your turn" exercise (intended) |

## 4 · Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| `import pandas as pd` in the terminal prints ImageMagick help / `X11` error | Python typed at the shell prompt | Use a notebook cell, or start `python` first |
| `ModuleNotFoundError: mgnipy` (or another package) | Wrong interpreter/kernel, e.g. `(base)` | Select `.venv` / **EMBL-EBI DS** kernel; `make setup` |
| `PackagesNotFoundError` from `conda install snakemake` | Conda only uses `defaults`; Snakemake is on conda-forge/bioconda | Not needed: Snakemake is in `.venv` (`make snakemake-solution`) |
| `cd: no such file or directory: snakemake_pipeline_solution` | Wrong folder | `make snakemake-solution` works from anywhere |
| `'Studies' object has no attribute 'bulk_fetch'` | MGnipy ≥ 0.2 | `make setup` pins MGnipy 0.1.3 |
| `FileNotFoundError: … Anemia Dataset.xlsx` | Dataset not downloaded | `make lab-hands-on` downloads it (or `make check` reports it) |
| `pip … No matching distribution found for torch` | Network dropped during download | Re-run `make setup` (pip retries are built in) |
| A notebook cell hangs forever at 0 % CPU (PyTorch + scikit-learn/UMAP in one kernel) | Two OpenMP runtimes (`sklearn/.dylibs/libomp.dylib` and `torch/lib/libomp.dylib`) deadlock on macOS | The **EMBL-EBI DS** kernel sets `OMP_NUM_THREADS=1` (since 2026-11-07): run `make kernel` once, reload the IDE, and select that kernel |
| `ImportError: … requires accelerate>=0.26.0` | Hugging Face `Trainer` dependency | `make setup-course` |
| `ValueError: <COMPRESSION.LZW: 5> requires the 'imagecodecs' package` | Compressed TIFFs | `make setup-course` |
| Kernel **EMBL-EBI DS** not listed | Kernel not registered, or IDE needs a refresh | `make kernel`, then reload the IDE window |
| Notebook can't find `people.tsv`, `data.csv`, … | Notebook not running in its own folder | VS Code: preset. PyCharm/others: set the working directory to the notebook's folder |
