#!/usr/bin/env python3
"""Extract the full list of symmetry operations of the 35 space groups from the
spglib Hall-symbol database (independent of GAP/CrystCat).

Convention of spglib: operations act on COLUMN vectors, x -> R x + t, with R an
integer 3x3 matrix in the conventional (ITA) basis and t a fractional translation.
For each ITA number the first Hall setting is the standard ITA setting (choice '';
for R32 the hexagonal-axes setting 'H' comes first, the rhombohedral 'R' second);
both settings are stored for 155.

Translations are rationalised exactly (denominators divide 12) and the exactness
of the rationalisation as well as the closure of the operations modulo Z^3 is
verified before writing.

Run:  python3 scripts/extract_spglib.py   (needs the `spglib` package)
Output: data/spglib_operations.json
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from pathlib import Path
import numpy as np
import spglib

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "data" / "spglib_operations.json"
# The 35 groups of the audit, followed by the two symmorphic CONTROL groups 23 (I222) and
# 197 (I23), which are not in the 35-list but complete the 16 symmorphic Sohncke groups with
# non-cyclic point group.
NUMS = [16,17,21,22,24,89,90,91,93,95,97,98,149,150,151,153,155,177,178,179,180,181,182,
        195,196,198,199,207,208,209,210,211,212,213,214, 23, 197]

def frac(x: float) -> Fraction:
    f = Fraction(x).limit_denominator(12)
    if abs(float(f) - x) > 1e-9:
        raise ValueError(f"translation {x} is not a rational with denominator | 12")
    return f

def closure_ok(ops):
    """Check that the set of (R, t mod 1) is closed under composition."""
    key = lambda R, t: (tuple(map(tuple, R)), tuple(x % 1 for x in t))
    S = {key(R, t) for R, t in ops}
    for R1, t1 in ops:
        for R2, t2 in ops:
            R = R1 @ R2
            t = [sum(Fraction(int(R1[i][j])) * t2[j] for j in range(3)) + t1[i] for i in range(3)]
            if key(R, t) not in S:
                return False
    return True

def main() -> None:
    by_number: dict[int, list] = {}
    for h in range(1, 531):
        t = spglib.get_spacegroup_type(h)
        by_number.setdefault(t.number, []).append(t)
    result = {"spglib_version": spglib.__version__,
              "convention": "column vectors, x -> R x + t; R integer 3x3 in the conventional ITA basis; t exact fractions as strings",
              "groups": []}
    for n in NUMS:
        settings = by_number[n]
        chosen = settings if n == 155 else settings[:1]
        for t in chosen:
            data = spglib.get_symmetry_from_database(t.hall_number)
            ops = []
            for R, tr in zip(data["rotations"], data["translations"]):
                R = np.array(R, dtype=int)
                ops.append((R, [frac(float(x)) for x in tr]))
            assert closure_ok(ops), f"operations of group {n} (hall {t.hall_number}) are not closed"
            result["groups"].append({
                "number": n, "hall_number": t.hall_number, "hall_symbol": t.hall_symbol,
                "choice": t.choice, "international_full": t.international_full,
                "international_short": t.international_short,
                "n_operations": len(ops),
                "operations": [{"R": R.tolist(), "t": [str(x) for x in tr]} for R, tr in ops],
            })
    OUT.write_text(json.dumps(result, indent=1))
    print(f"wrote {OUT.relative_to(HERE.parent)}: {len(result['groups'])} settings; spglib {spglib.__version__}")
    for g in result["groups"]:
        print(g["number"], g["hall_number"], g["choice"] or "-", g["international_short"], g["hall_symbol"], g["n_operations"])

if __name__ == "__main__":
    main()
