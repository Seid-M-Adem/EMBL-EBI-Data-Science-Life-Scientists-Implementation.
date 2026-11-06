#!/usr/bin/env bash
# One-command launcher for the 02.1 hands-on practical.
#   bash start.sh           -> check the setup, then open Jupyter Lab on the notebooks
#   bash start.sh --check   -> only check the setup
# Works from any directory and in any conda env: it always uses the repo's .venv.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
VENV="$ROOT/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "→ Creating virtual environment at $VENV"
  python3 -m venv "$VENV"
fi
if ! "$VENV/bin/python" -c "import mgnipy, pandas, seaborn, jupyterlab, sklearn, scipy, openpyxl, snakemake" 2>/dev/null; then
  echo "→ Installing packages from requirements.txt"
  "$VENV/bin/pip" install -q -r "$HERE/requirements.txt"
fi

# Dataset for the self-guided exercise in intro_to_ml.ipynb (Mendeley Data, CC BY 4.0; git-ignored)
ANAEMIA_DIR="$HERE/python-data-tutorials/Pediatric Anemia Dataset Hematological Indicators and Diagnostic Classification"
if [[ ! -s "$ANAEMIA_DIR/Anemia Dataset.xlsx" ]]; then
  echo "→ Downloading the Pediatric Anemia dataset (doi:10.17632/y7v7ff3wpj.1)"
  mkdir -p "$ANAEMIA_DIR"
  curl -fsSL --retry 3 -o "$ANAEMIA_DIR/Anemia Dataset.xlsx" \
    "https://data.mendeley.com/public-files/datasets/y7v7ff3wpj/files/47113cb5-ce6d-4cb3-98a6-66bff28503ca/file_downloaded"
fi

"$VENV/bin/python" "$HERE/check_setup.py"
[[ "${1:-}" == "--check" ]] && exit 0

echo "→ Opening Jupyter Lab (stop it with Ctrl+C in this terminal)"
cd "$HERE/python-data-tutorials"
PATH="$VENV/bin:$PATH" exec "$VENV/bin/jupyter" lab
