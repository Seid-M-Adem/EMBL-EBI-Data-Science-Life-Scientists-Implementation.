# =============================================================================
# One entry point for every task in this repository.
# Works the same from any terminal: macOS Terminal, VS Code / Cursor, PyCharm,
# JupyterLab's terminal. Run `make help` to list the targets.
#
# Every target uses the repository's own virtual environment (.venv) directly,
# so it doesn't matter which conda env (e.g. "(base)") is active.
# See RUNNING.md for IDE-specific instructions.
# =============================================================================

VENV        := .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip --retries 10 --timeout 60
KERNEL_NAME := embl-ebi-ds
KERNEL_DISP := Python 3 (EMBL-EBI DS .venv)
HANDS_ON    := 02_accessing_and_handling_data/01_apis_and_data_collection/hands_on

.DEFAULT_GOAL := help
.PHONY: help setup setup-course kernel check lab lab-hands-on api-call \
        snakemake-solution snakemake-tutorial snakemake-clean \
        fetch fetch-local fetch-data fetch-2025 lint clean

help: ## Show this list of commands
	@printf "Usage: make <target>\n\n"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# ---- Environment -------------------------------------------------------------
$(PY):
	python3 -m venv $(VENV)
	$(PIP) install -q --upgrade pip

setup: $(PY) ## Create .venv and install core + 02.1 hands-on packages, then register the Jupyter kernel
	$(PIP) install -q -r requirements.txt -r $(HANDS_ON)/requirements.txt
	@$(MAKE) --no-print-directory kernel

setup-course: setup ## Also install the extras used by the course notebooks of modules 03-05 (large)
	$(PIP) install -q -r requirements-course.txt

kernel: $(PY) ## Register .venv as a Jupyter kernel visible to every IDE ("Python 3 (EMBL-EBI DS .venv)")
	$(PY) -m ipykernel install --user --name $(KERNEL_NAME) --display-name "$(KERNEL_DISP)"

check: ## Verify packages, tools (jq, curl), datasets and API access for the 02.1 hands-on
	bash $(HANDS_ON)/start.sh --check

# ---- Notebooks ---------------------------------------------------------------
lab: $(PY) ## Open Jupyter Lab at the repository root (all modules)
	PATH="$(CURDIR)/$(VENV)/bin:$$PATH" $(VENV)/bin/jupyter lab

lab-hands-on: ## Check the setup, then open Jupyter Lab on the 02.1 hands-on notebooks
	bash $(HANDS_ON)/start.sh

# ---- 02.1 hands-on -----------------------------------------------------------
api-call: ## 02.1 Part 0: first API call (curl + jq)
	bash $(HANDS_ON)/part0_first_api_call/first_api_call.sh

snakemake-solution: ## 02.1 Part 4: run the complete Snakemake reference workflow
	bash $(HANDS_ON)/run_snakemake.sh solution

snakemake-tutorial: ## 02.1 Part 4: run your completed Snakemake scaffold
	bash $(HANDS_ON)/run_snakemake.sh tutorial

snakemake-clean: ## 02.1 Part 4: delete the outputs of both Snakemake workflows
	-bash $(HANDS_ON)/run_snakemake.sh solution --delete-all-output
	-bash $(HANDS_ON)/run_snakemake.sh tutorial --delete-all-output

# ---- Course materials & data -------------------------------------------------
fetch: ## Re-download the official slides, notebooks and tutorial code
	bash scripts/fetch_course_materials.sh

fetch-local: ## + local-only resources (bioimaging repo, reference papers, live Colab versions; git-ignored)
	bash scripts/fetch_course_materials.sh --local

fetch-data: ## + project datasets into data/raw (~730 MB; git-ignored)
	bash scripts/fetch_course_materials.sh --data

fetch-2025: ## + supplementary 2025 course edition (~140 MB + 165 MB dataset; git-ignored)
	bash scripts/fetch_course_materials.sh --2025

# ---- Quality -----------------------------------------------------------------
lint: ## Lint my own code and notebooks with Ruff (same check as GitHub Actions)
	@if [ -x $(VENV)/bin/ruff ]; then $(VENV)/bin/ruff check .; else ruff check .; fi

clean: ## Remove caches and notebook checkpoints (keeps .venv and data)
	find . -path ./.venv -prune -o \( -name '__pycache__' -o -name '.ipynb_checkpoints' -o -name '.ruff_cache' \) -type d -print -exec rm -rf {} +
