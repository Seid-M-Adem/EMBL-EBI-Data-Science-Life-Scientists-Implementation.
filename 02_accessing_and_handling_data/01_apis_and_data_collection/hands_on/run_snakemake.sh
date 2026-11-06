#!/usr/bin/env bash
# Run the Snakemake exercise from ANY directory, without `conda install` or `cd`.
#   bash run_snakemake.sh solution            # run the complete reference workflow
#   bash run_snakemake.sh tutorial            # run your completed scaffold
#   bash run_snakemake.sh tutorial -n         # dry run (show planned jobs)
#   bash run_snakemake.sh tutorial --sdm conda   # bonus challenge: per-rule conda environments
#   bash run_snakemake.sh solution --delete-all-output   # clean results to start again
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
WHICH="${1:-}"; shift || true
case "$WHICH" in
  solution|tutorial) ;;
  *) echo "Usage: bash run_snakemake.sh {solution|tutorial} [extra snakemake options]"; exit 1 ;;
esac

# Prefer the repo's .venv (snakemake + pandas + seaborn installed by start.sh); fall back to whatever is on PATH.
if [[ -x "$ROOT/.venv/bin/snakemake" ]]; then
  export PATH="$ROOT/.venv/bin:$PATH"
elif ! command -v snakemake >/dev/null; then
  echo "snakemake not found. Run: bash $HERE/start.sh --check   (installs it into .venv)"; exit 1
fi

cd "$HERE/python-data-tutorials/snakemake_pipeline_$WHICH"
echo "→ $(snakemake --version | tail -1) in $(pwd)"
snakemake --cores all "$@"
