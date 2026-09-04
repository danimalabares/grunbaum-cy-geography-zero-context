#!/usr/bin/env python3
"""Build and verify all equation exports from exact Macaulay2 output."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    os.environ.get("GS_ZERO_CONTEXT_SOURCE", ROOT.parent / "grunbaum-zero-context-proof")
).expanduser().resolve()
EXPECTED_COMMIT = "ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b"
EXPECTED_TREE = "451a038cdd9fece1d35bb32f1268756fb55cebcd"
EXPECTED_STATE_SHA256 = "8c5040d19de950bd4e852ce6b11fc08c1bb605d2f97b5bacdaebce3b10056351"
EXPECTED_RELATION_STATE_SHA256 = "39e841e2e5b5196a160c3fd3ac8457727976ecd2d9ecc933abf25728fa985874"


def run(cmd: list[str], cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if p.returncode:
        sys.stderr.write(p.stdout)
        sys.stderr.write(p.stderr)
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(cmd)}")
    return p.stdout


def git(*args: str) -> str:
    return run(["git", *args], SOURCE).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_source() -> None:
    if git("rev-parse", "HEAD") != EXPECTED_COMMIT:
        raise SystemExit("SOURCE HEAD DIFFERS FROM FROZEN COMMIT")
    if git("rev-parse", "HEAD^{tree}") != EXPECTED_TREE:
        raise SystemExit("SOURCE TREE DIFFERS FROM FROZEN TREE")
    if git("status", "--porcelain"):
        raise SystemExit("SOURCE WORKTREE IS NOT CLEAN")
    state = SOURCE / "deformation/generic_equivariant_state_F_order6.txt"
    if sha256(state) != EXPECTED_STATE_SHA256:
        raise SystemExit("FROZEN SIX-JET HASH DIFFERS")
    relation_state = SOURCE / "deformation/generic_equivariant_state_R_order6.txt"
    if sha256(relation_state) != EXPECTED_RELATION_STATE_SHA256:
        raise SystemExit("FROZEN SIX-JET RELATION HASH DIFFERS")


def parse_list(s: str) -> list[int]:
    if not (s.startswith("{") and s.endswith("}")):
        raise ValueError(s)
    return [] if s == "{}" else [int(x) for x in s[1:-1].split(",")]


def latex(poly: str) -> str:
    p = poly.replace("*", r"\,")
    p = re.sub(r"\^([0-9]+)", r"^{\1}", p)
    p = re.sub(r"\(([-0-9]+)/([0-9]+)\)", r"\\frac{\1}{\2}", p)
    return p


def main() -> None:
    verify_source()
    env = os.environ.copy()
    env["GS_ZERO_CONTEXT_SOURCE"] = str(SOURCE)
    split = subprocess.run(
        ["M2", "--script", str(ROOT / "scripts/verify_coordinate_split.m2")],
        cwd=ROOT, env=env, text=True, capture_output=True
    )
    (ROOT / "computations/verify_coordinate_split.stdout.txt").write_text(split.stdout)
    (ROOT / "computations/verify_coordinate_split.stderr.txt").write_text(split.stderr)
    if split.returncode or "CHECK|intrinsic_split_recomputed|true" not in split.stdout:
        raise SystemExit(f"Macaulay2 coordinate-split check failed with exit {split.returncode}")
    p = subprocess.run(
        ["M2", "--script", str(ROOT / "scripts/extract_deformation.m2")],
        cwd=ROOT, env=env, text=True, capture_output=True
    )
    (ROOT / "computations/extract_deformation.stdout.txt").write_text(p.stdout)
    (ROOT / "computations/extract_deformation.stderr.txt").write_text(p.stderr)
    if p.returncode:
        raise SystemExit(f"Macaulay2 extraction failed with exit {p.returncode}")

    meta: dict[str, str] = {}
    generators: dict[int, str] = {}
    basis = {i: ["0"] * 16 for i in range(1, 110)}
    intrinsic: list[int] | None = None
    orbits: dict[int, list[int]] = {}
    vector: list[int] | None = None
    g1: dict[int, str] = {}
    jet = {d: {} for d in range(7)}
    checks: dict[str, bool] = {}
    checks["intrinsic_split_recomputed"] = True
    for raw in p.stdout.splitlines():
        fields = raw.split("|")
        tag = fields[0]
        if tag == "META": meta[fields[1]] = fields[2]
        elif tag == "GEN": generators[int(fields[1])] = fields[2]
        elif tag == "BASIS": basis[int(fields[1])][int(fields[2])-1] = fields[3]
        elif tag == "INTRINSIC": intrinsic = parse_list(fields[1])
        elif tag == "ORBIT": orbits[int(fields[1])] = parse_list(fields[2])
        elif tag == "VECTOR53": vector = parse_list(fields[1])
        elif tag == "G1": g1[int(fields[1])] = fields[2]
        elif tag == "JET": jet[int(fields[1])][int(fields[2])] = fields[3]
        elif tag == "CHECK": checks[fields[1]] = fields[2] == "true"

    if meta.get("tangent_columns") != "109" or meta.get("intrinsic_dimension") != "53":
        raise SystemExit("EXTRACTED DIMENSIONS DIFFER")
    if sorted(generators) != list(range(1, 17)) or sorted(g1) != list(range(1, 17)):
        raise SystemExit("GENERATOR ORDER/COUNT DIFFER")
    if intrinsic is None or len(intrinsic) != 53:
        raise SystemExit("INTRINSIC BASIS ORDER/COUNT DIFFER")
    if sorted(x for orbit in orbits.values() for x in orbit) != list(range(1, 54)):
        raise SystemExit("ORBIT PARTITION DIFFERS")
    if vector is None or len(vector) != 53:
        raise SystemExit("TANGENT VECTOR LENGTH DIFFERS")
    if not checks or not all(checks.values()):
        raise SystemExit("ONE OR MORE EXACT CHECKS FAILED")
    for d in range(7):
        if sorted(jet[d]) != list(range(1, 17)):
            raise SystemExit(f"JET ORDER {d} GENERATOR ORDER/COUNT DIFFER")
    if any(g1[i] != jet[1][i] for i in range(1, 17)):
        raise SystemExit("RECOMPUTED FIRST JET DIFFERS FROM STORED SIX-JET")

    data = {
        "format": "grunbaum-zero-context-deformation-v1",
        "source_commit": EXPECTED_COMMIT,
        "source_tree": EXPECTED_TREE,
        "base_field": "QQ",
        "variables": {chr(96+i): f"x{i}" for i in range(1, 9)},
        "generator_order": [generators[i] for i in range(1, 17)],
        "embedded_tangent_basis": [
            {"index_1_based": i, "images_in_generator_order": basis[i]}
            for i in range(1, 110)
        ],
        "intrinsic_columns_in_embedded_basis_1_based": intrinsic,
        "intrinsic_basis_orbits_1_based": [orbits[i] for i in range(1, 11)],
        "selected_tangent_coordinates_53": vector,
        "first_order_corrections": [g1[i] for i in range(1, 17)],
        "six_jet_coefficients": [
            [jet[d][i] for i in range(1, 17)] for d in range(7)
        ],
        "checks": checks,
    }
    eq = ROOT / "equations"
    eq.mkdir(exist_ok=True)
    (eq / "deformation_data.json").write_text(json.dumps(data, indent=2) + "\n")

    tb = [
        "# Embedded tangent basis",
        "",
        "This is the exact one-based column order returned by",
        "`normalMatrix({0},F0)` over `QQ[a,b,c,d,e,f,g,h]`. Each `b_j`",
        "is recorded by its nonzero images of the ordered generators; omitted",
        "images are zero in the chosen polynomial representatives.",
        "",
    ]
    for item in data["embedded_tangent_basis"]:
        images = [
            f"f_{i} -> {p}" for i, p in enumerate(item["images_in_generator_order"], 1)
            if p != "0"
        ]
        tb.append(f"- `b_{item['index_1_based']}`: " + "; ".join(images))
    (eq / "tangent_basis.md").write_text("\n".join(tb) + "\n")

    m2 = [
        "-- Generated exactly from the frozen zero-context source.",
        "S = QQ[a,b,c,d,e,f,g,h,q];",
        "f0List = {" + ",".join(data["generator_order"]) + "};",
        "g1List = {" + ",".join(data["first_order_corrections"]) + "};",
        "Ffirst = apply(16,i->(f0List#i)+q*(g1List#i));",
        "Ifirst = ideal Ffirst;",
    ]
    (eq / "first_order.m2").write_text("\n".join(m2) + "\n")

    six_m2 = [
        "-- Full q^6 jet generated from the frozen zero-context source.",
        "S = QQ[a,b,c,d,e,f,g,h,q];",
    ]
    for d in range(7):
        six_m2.append(f"H{d} = {{" + ",".join(jet[d][i] for i in range(1,17)) + "};")
    fsix = []
    for i in range(1, 17):
        fsix.append("+".join(
            f"({jet[d][i]})" if d == 0 else f"q^{d}*({jet[d][i]})"
            for d in range(7)
        ))
    six_m2 += ["Fsix = {" + ",".join(fsix) + "};", "Isix = ideal Fsix;"]
    (eq / "six_jet.m2").write_text("\n".join(six_m2) + "\n")

    tex_lines = [
        r"% Generated exactly from the frozen zero-context source.",
        r"\begin{align*}",
    ]
    md_lines = ["# First-order generators", "", "Here `a=x_1, ..., h=x_8` and the ordering is frozen.", ""]
    for i, (f, g) in enumerate(zip(data["generator_order"], data["first_order_corrections"]), 1):
        formula = f"F_{{{i}}}^{{(1)}} = {latex(f)} + q\\left({latex(g)}\\right)"
        tex_lines.append(formula + (r"\\" if i < 16 else ""))
        md_lines.append(f"- $${formula}$$")
    tex_lines.append(r"\end{align*}")
    (eq / "first_order.tex").write_text("\n".join(tex_lines) + "\n")
    (eq / "first_order.md").write_text("\n".join(md_lines) + "\n")

    # A compact tab-separated format: order, generator, cubic coefficient.
    tsv = ["q_order\tgenerator_index\tcoefficient"]
    for d in range(7):
        for i in range(1, 17):
            tsv.append(f"{d}\t{i}\t{jet[d][i]}")
    (eq / "six_jet.tsv").write_text("\n".join(tsv) + "\n")

    digest_lines = []
    for path in sorted(eq.iterdir()):
        if path.is_file(): digest_lines.append(f"{sha256(path)}  {path.relative_to(ROOT)}")
    (ROOT / "computations/equation_sha256.txt").write_text("\n".join(digest_lines) + "\n")
    print("EXTRACTION_AND_VERIFICATION_PASSED")
    print("embedded tangent basis 109; coordinate orbit 56; intrinsic complement 53")
    print("stored q coefficient equals independently recomputed T1*y")
    print("six-jet orders 0..6 and all 16 generator slots exported")


if __name__ == "__main__":
    main()
