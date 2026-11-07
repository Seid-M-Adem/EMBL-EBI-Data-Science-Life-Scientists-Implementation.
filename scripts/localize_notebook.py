"""Make a Colab-only course notebook runnable locally, without touching the original.

Writes a copy in which Colab-specific lines are commented out:
  - ``from google.colab import ...`` and ``drive.mount(...)``
  - ``os.chdir('/content/...')`` into the trainer's Google Drive
  - ``!pip install ...`` / ``%pip install ...`` (packages come from requirements-course.txt)
  - ``%%capture`` cell magics that only hid pip output
  - ``X = Path("/content/drive/...")`` becomes ``X = Path.cwd()`` (outputs land next to the copy)
  - steps that need a personal account token are disabled (they are optional in the course): single-line
    Hugging Face ``push_to_hub(...)`` calls, and whole cells that log in, prompt for credentials or upload
    (``wandb.login`` / ``wandb.init``, Colab ``userdata``, ``getpass``, ``create_repo`` / ``upload_file``)

Optionally symlinks a data folder next to the copy, so relative paths such as ``Data/x.RDS`` resolve.

Usage:
    python scripts/localize_notebook.py NOTEBOOK... --out DIR [--link NAME=TARGET ...] [--force]

Existing copies are kept (so your edits and outputs survive); pass --force to regenerate them.

Example (gene-expression project):
    python scripts/localize_notebook.py 05_group_projects/gene_expression/course_materials/code/*.ipynb \
        --out 05_group_projects/gene_expression/course_materials/local/runnable \
        --link Data=data/raw/gene_expression
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

COLAB_LINE = re.compile(
    r"^\s*("
    r"from google\.colab import|import google\.colab|drive\.mount\(|"
    r"os\.chdir\(\s*['\"]/content|"
    r"[!%]\s*pip install|[!%]\s*uv pip install|!\s*pip install uv"
    r")"
)
MARK = "# [localized] "
DRIVE_PATH = re.compile(r"""^(\s*)(\w+)\s*=\s*Path\(\s*['"]/content/drive/[^'"]*['"]\s*\)""")
TOKEN_CELL = re.compile(
    r"wandb\.login\(|wandb\.init\(|google\.colab import userdata|getpass\(|\.create_repo\(|upload_file\("
)
TOKEN_LINE = re.compile(r"\.push_to_hub\(|notebook_login\(")


def localize_source(src: str) -> tuple[str, int]:
    """Comment out Colab-only lines in one cell's source; return new source and count."""
    lines = src.splitlines(keepends=True)
    if TOKEN_CELL.search(src):
        disabled = [MARK + "optional cell disabled (needs a personal account token)\n"]
        return "".join(disabled + [MARK + ln for ln in lines]), len(lines)
    out, n = [], 0
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        m = DRIVE_PATH.match(line)
        if m:
            out.append(f"{m.group(1)}{m.group(2)} = Path.cwd()  {MARK}was: {line.strip()}\n")
            n += 1
        elif TOKEN_LINE.search(line) and line.count("(") == line.count(")"):
            out.append(MARK + "optional (needs a Hugging Face token): " + line)
            n += 1
        elif (i == 0 and stripped.startswith("%%capture")) or COLAB_LINE.match(line):
            out.append(MARK + line)
            n += 1
        else:
            out.append(line)
    return "".join(out), n


def localize(nb_path: Path, out_dir: Path) -> int:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    total = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        new, n = localize_source(src)
        if n:
            # A cell that is now only comments still runs fine; add `pass` for clarity.
            if all(not ln.strip() or ln.lstrip().startswith("#") for ln in new.splitlines()):
                new += "\npass  # [localized] Colab-only cell\n"
            cell["source"] = new.splitlines(keepends=True)
            total += n
        cell["outputs"], cell["execution_count"] = [], None
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / nb_path.name).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return total


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notebooks", nargs="+", type=Path)
    ap.add_argument("--out", required=True, type=Path, help="folder for the runnable copies")
    ap.add_argument(
        "--link",
        action="append",
        default=[],
        metavar="NAME=TARGET",
        help="create OUT/NAME -> TARGET symlink (TARGET relative to the current directory)",
    )
    ap.add_argument("--force", action="store_true", help="overwrite copies that already exist")
    args = ap.parse_args()

    for nb in args.notebooks:
        if (args.out / nb.name).exists() and not args.force:
            print(f"  {nb.name}: copy exists, kept (use --force to regenerate)")
            continue
        n = localize(nb, args.out)
        print(f"  {nb.name}: {n} Colab-only line(s) commented out -> {args.out / nb.name}")
    for spec in args.link:
        name, target = spec.split("=", 1)
        link = args.out / name
        if not link.exists() and not link.is_symlink():
            link.symlink_to(os.path.relpath(Path(target).resolve(), args.out.resolve()))
            print(f"  linked {link} -> {target}")


if __name__ == "__main__":
    main()
