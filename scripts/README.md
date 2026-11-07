# Scripts

| Script | Purpose |
|--------|---------|
| [`fetch_course_materials.sh`](fetch_course_materials.sh) | Downloads the official course slides, notebooks, Colab notebooks and tutorial repositories into the matching `course_materials/` folders. Optionally fetches local-only resources, the project datasets and the supplementary 2025 edition |

```bash
scripts/fetch_course_materials.sh            # slides, notebooks, tutorial code (committed)
scripts/fetch_course_materials.sh --local    # + unlicensed repo, reference papers, live Colab versions (git-ignored)
scripts/fetch_course_materials.sh --data     # + project datasets into data/raw (~730 MB, git-ignored)
scripts/fetch_course_materials.sh --2025     # + 2025 course edition (~140 MB + 165 MB dataset, git-ignored)
scripts/fetch_course_materials.sh --all      # everything (~1.1 GB)
scripts/fetch_course_materials.sh --help
```

| [`localize_notebook.py`](localize_notebook.py) | Writes a **Colab-free copy** of a course notebook: comments out `drive.mount`, `!pip`, `os.chdir('/content/…')`; turns `Path("/content/drive/…")` into `Path.cwd()`; disables optional token/upload steps; can symlink a data folder. Originals are never modified, and existing copies are kept unless `--force`. Used by `make runnable` |

| Helper (in the fetch script) | What it does |
|--------|--------------|
| `get` | Downloads one FTP file, with retries, to a `.part` file that's renamed only when complete |
| `drive_nb` | Downloads a shared Colab/Drive notebook and **strips its saved outputs**, which can embed third-party images |
| `clone_snapshot` | Shallow-clones a GitHub repo. For committed snapshots it removes `.git` and writes `SNAPSHOT_SOURCE.txt` with the commit |

Re-running is safe: files that already exist are skipped, so an interrupted run can simply be restarted.
Tested on 2026-11-06: `--all` downloads everything; a second run downloads nothing.

Shortcut targets: `make fetch`, `make fetch-local`, `make fetch-data`, `make fetch-2025` (see the root [Makefile](../Makefile) and [RUNNING.md](../RUNNING.md)).
