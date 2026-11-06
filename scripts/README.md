# Scripts

| Script | Purpose |
|--------|---------|
| [`fetch_course_materials.sh`](fetch_course_materials.sh) | Downloads the official course slides, notebooks and tutorial repositories into the matching `course_materials/` folders. Optionally fetches local-only resources and the project datasets |

```bash
scripts/fetch_course_materials.sh            # slides, notebooks, tutorial code (committed)
scripts/fetch_course_materials.sh --local    # + unlicensed repo & reference papers (git-ignored)
scripts/fetch_course_materials.sh --data     # + project datasets into data/raw (~700 MB, git-ignored)
scripts/fetch_course_materials.sh --all      # everything
scripts/fetch_course_materials.sh --help
```

The script is **idempotent**: files that already exist are skipped, and downloads write to a `.part` file that is only
renamed once complete, so an interrupted run can simply be restarted.
