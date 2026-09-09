#!/usr/bin/env python3
"""Exact Q(sqrt(7)) support point for the local topology reduction.

The output checks the point and transversality only. The local-ring and
fundamental-group arguments are mathematical proofs in the accompanying note.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sys

RUN = Path(__file__).resolve().parents[1]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0] + 7 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scalar(c):
    return (Q(c), Q(0))


def norm(a):
    return a[0] ** 2 - 7 * a[1] ** 2


def render(a):
    return [str(c) for c in a]


def main():
    u = scalar(1)
    v = (Q(-5, 2), Q(1, 2))
    p = scalar(-8)
    for c, a in [(-8, mul(u, u)), (-20, mul(u, v)), (-8, mul(v, v)), (-20, u), (-20, v)]:
        p = add(p, mul(scalar(c), a))
    pv = add(add(mul(scalar(-20), u), mul(scalar(-16), v)), scalar(-20))
    assert p == scalar(0)
    assert pv == (Q(0), Q(-8))
    assert norm(v) == Q(9, 2) and norm(pv) == -448
    smoothness = RUN / "data/smoothness_transfer_checks.json"
    data = json.loads(smoothness.read_text())
    assert data["critical_value_pi2_from_actual_twojet_QQ"] == "-8*u^2-20*u*v-8*v^2-20*u-20*v-8"
    result = {
        "status": "COMPUTER-CERTIFIED exact point/transversality; topology proof is separate",
        "field": "Q[s]/(s^2-7), irreducible since 7 is not a rational square",
        "basis": ["1", "s"],
        "u": render(u), "v": render(v), "p_at_point": render(p),
        "p_v_at_point": render(pv),
        "norm_v": str(norm(v)), "norm_p_v": str(norm(pv)),
        "source_hashes": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [smoothness, Path(__file__)]},
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else RUN / "data/topology_local_point.json"
    if dest.exists():
        assert dest.read_text() == text
    else:
        dest.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
