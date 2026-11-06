"""Check that everything the 02.1 practical needs is installed and reachable.

Run from the terminal:   .venv/bin/python <path>/check_setup.py   (or: bash start.sh --check)
"""

import importlib
import logging
import shutil
import sys
import urllib.request

logging.disable(logging.INFO)  # mgnipy's dependencies log at DEBUG level on import; keep the output readable
ok = True


def report(passed: bool, label: str, hint: str = "") -> None:
    global ok
    ok &= passed
    print(f"  {'✅' if passed else '❌'} {label}" + ("" if passed else f"  →  {hint}"))


print("Checking the 02.1 hands-on setup\n")
in_venv = sys.prefix != sys.base_prefix
report(in_venv, f"Python {sys.version.split()[0]} from a virtual env ({sys.prefix})",
       "use bash start.sh, or: source .venv/bin/activate")

for module, expected in [("pandas", None), ("numpy", None), ("seaborn", None),
                         ("requests", None), ("jupyterlab", None), ("mgnipy", "0.1.3")]:
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, "__version__", "?")
        good = expected is None or version == expected
        report(good, f"{module} {version}", f"pip install {module}=={expected}")
    except ImportError:
        report(False, f"{module} not installed", "pip install -r requirements.txt")

for tool in ("curl", "jq"):
    report(shutil.which(tool) is not None, f"{tool} on PATH", f"brew install {tool}")

for name, url in [("Open-Meteo API (Part 0)", "https://api.open-meteo.com/v1/forecast?latitude=52&longitude=0&current=temperature_2m"),
                  ("MGnify API (Part 1)", "https://www.ebi.ac.uk/metagenomics/api/v2/studies/MGYS00005116"),
                  ("ENA Portal API (Part 1)", "https://www.ebi.ac.uk/ena/portal/api/results?dataPortal=ena")]:
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            report(r.status == 200, f"{name} reachable", "check your internet connection")
    except Exception as e:  # noqa: BLE001
        report(False, f"{name} unreachable ({e.__class__.__name__})", "check your internet connection / VPN")

print("\nAll good: you're ready to start." if ok else "\nFix the ❌ items above, then run this check again.")
sys.exit(0 if ok else 1)
