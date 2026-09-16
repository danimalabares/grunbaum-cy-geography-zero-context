#!/usr/bin/env python3
"""Single reproduction command for computations/crystallographic-links.

    python3 scripts/run_all.py            # all exact combinatorial checks (~3 min) + Macaulay2 parts if M2 is on PATH
    python3 scripts/run_all.py --no-m2    # skip Macaulay2
    python3 scripts/run_all.py --full-search   # additionally rerun the capped (4,2)_1 diagonalisation search
                                               # (recorded run: 45 h wall clock; the counting obstruction that
                                               # settles the question runs in seconds and is always included)

Every step writes its stdout/stderr to output/<step>.log; a summary goes to output/run_all.log.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")
os.makedirs(os.path.join(OUT, "m2"), exist_ok=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

python_steps = [
    ("build_complexes", ["python3", "scripts/build_complexes.py"]),
    ("links", ["python3", "scripts/links.py"]),
    ("lifts", ["python3", "scripts/lifts.py"]),
    ("t1_formula", ["python3", "scripts/t1_formula.py"]),
    ("prism_triangulations", ["python3", "scripts/prism_triangulations.py"]),
    ("four_two_one_counting", ["python3", "scripts/four_two_one_counting.py"]),
    ("verify_33_identification", ["python3", "scripts/verify_33_identification.py"]),
]
m2_steps = [
    ("m2/L9", ["M2", "--script", "scripts/link_t1_t2.m2", "data/links/cp2_9_link_v9.txt", "L9"]),
    ("m2/L10a", ["M2", "--script", "scripts/link_t1_t2.m2", "data/links/cp2_10_link_v1_x11.txt", "L10a"]),
    ("m2/L10b", ["M2", "--script", "scripts/link_t1_t2.m2", "data/links/cp2_10_link_v2_x12.txt", "L10b"]),
    ("m2/CP2_10", ["M2", "--script", "scripts/cp2_10_t1_t2.m2", "data/cp2_10_facets.txt"]),
    ("m2/L9_equivariant", ["M2", "--script", "scripts/link_equivariant.m2", "data/links/cp2_9_link_v9.txt", "data/links/cp2_9_link_v9_aut.txt", "L9"]),
    ("m2/L10a_equivariant", ["M2", "--script", "scripts/link_equivariant.m2", "data/links/cp2_10_link_v1_x11.txt", "data/links/cp2_10_link_v1_x11_aut.txt", "L10a"]),
    ("m2/L10b_equivariant", ["M2", "--script", "scripts/link_equivariant.m2", "data/links/cp2_10_link_v2_x12.txt", "data/links/cp2_10_link_v2_x12_aut.txt", "L10b"]),
]
search_step = ("four_two_one_search", ["python3", "scripts/four_two_one_search.py"])


def main():
    args = sys.argv[1:]
    steps = list(python_steps)
    if "--no-m2" not in args and shutil.which("M2"):
        steps += m2_steps
    elif "--no-m2" not in args:
        print("M2 not found on PATH: skipping the Macaulay2 steps")
    if "--full-search" in args:
        steps.append(search_step)
    summary = []
    for name, cmd in steps:
        t0 = time.time()
        with open(os.path.join(OUT, name + ".log"), "w") as log:
            p = subprocess.run(cmd, cwd=ROOT, env=ENV, stdout=log, stderr=subprocess.STDOUT, text=True)
        status = "PASS" if p.returncode == 0 else f"FAIL(exit {p.returncode})"
        line = f"{name}: {status} ({time.time() - t0:.1f}s)"
        print(line, flush=True)
        summary.append(line)
        if p.returncode:
            open(os.path.join(OUT, "run_all.log"), "w").write("\n".join(summary) + "\n")
            raise SystemExit(f"{name} failed; see output/{name}.log")
    # collect the CHECK lines of the Macaulay2 logs
    checks = []
    for name, _ in m2_steps:
        path = os.path.join(OUT, name + ".log")
        if os.path.exists(path):
            checks += [l.rstrip() for l in open(path, errors="replace") if l.startswith("CHECK|")]
    open(os.path.join(OUT, "run_all.log"), "w").write("\n".join(summary + ["", "Macaulay2 CHECK lines:"] + checks) + "\n")
    print("ALL_STEPS_PASS")


if __name__ == "__main__":
    main()
