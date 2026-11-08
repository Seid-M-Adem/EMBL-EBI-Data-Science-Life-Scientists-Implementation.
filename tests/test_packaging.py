"""Guard against undeclared dependencies: every third-party import in src/dsls must be listed in pyproject.toml.

CI installs only the declared dependencies, so a missing entry means the package breaks for anyone installing it.
"""

import ast
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_TO_DIST = {"sklearn": "scikit-learn"}  # import name → distribution name, where they differ


def _third_party_imports() -> set[str]:
    names = set()
    for path in (ROOT / "src" / "dsls").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names.add(node.module.split(".")[0])
    return {n for n in names if n not in sys.stdlib_module_names and n not in {"dsls", "__future__"}}


def test_every_runtime_import_is_declared():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    declared = {re.split(r"[<>=!~\[ ]", d)[0].lower() for d in project["dependencies"]}
    for extra in project.get("optional-dependencies", {}).values():
        declared |= {re.split(r"[<>=!~\[ ]", d)[0].lower() for d in extra}
    missing = {IMPORT_TO_DIST.get(n, n) for n in _third_party_imports()} - declared
    assert not missing, f"imported by src/dsls but not declared in pyproject.toml: {sorted(missing)}"
