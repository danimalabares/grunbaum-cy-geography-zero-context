#!/usr/bin/env python3
"""Run the resumable exact audit suite and preserve stdout/stderr."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV.setdefault("GS_ZERO_CONTEXT_SOURCE", str(ROOT.parent / "grunbaum-zero-context-proof"))
JOBS = [
    ("source", ["python3", "scripts/verify_source.py"]),
    ("deformation", ["python3", "scripts/build_outputs.py"]),
    ("first_order_export", ["M2", "--script", "equations/first_order.m2"]),
    ("six_jet_export", ["M2", "--script", "equations/six_jet.m2"]),
    ("geography", ["M2", "--script", "scripts/verify_geography.m2"]),
    ("formulas", ["python3", "scripts/verify_formulas.py"]),
    ("full_kuranishi", ["M2", "--script", "scripts/verify_full_kuranishi.m2"]),
    ("failed_truncation", ["M2", "--script", "scripts/verify_failed_truncation.m2"]),
    ("explicitness", ["python3", "scripts/audit_explicitness.py"]),
    ("publication_audit", ["python3", "scripts/publication_audit.py"]),
]

def main() -> None:
    outdir = ROOT / "computations"
    outdir.mkdir(exist_ok=True)
    for name, cmd in JOBS:
        p = subprocess.run(cmd, cwd=ROOT, env=ENV, text=True, capture_output=True)
        (outdir / f"{name}.stdout.txt").write_text(p.stdout)
        (outdir / f"{name}.stderr.txt").write_text(p.stderr)
        if p.returncode:
            raise SystemExit(f"{name} FAILED with exit {p.returncode}; see computations/{name}.stderr.txt")
        print(f"{name}: PASS")
    print("ALL_CHECKS_PASS")

if __name__ == "__main__":
    main()
