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
if ! "$VENV/bin/python" -c "import mgnipy, pandas, seaborn, jupyterlab" 2>/dev/null; then
  echo "→ Installing packages from requirements.txt"
  "$VENV/bin/pip" install -q -r "$HERE/requirements.txt"
fi

"$VENV/bin/python" "$HERE/check_setup.py"
[[ "${1:-}" == "--check" ]] && exit 0

echo "→ Opening Jupyter Lab (stop it with Ctrl+C in this terminal)"
cd "$HERE/python-data-tutorials"
PATH="$VENV/bin:$PATH" exec "$VENV/bin/jupyter" lab
