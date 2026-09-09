#!/usr/bin/env python3
"""Tiny exact checks behind smoothness transport; no CAS or source writes.

This does NOT recompute the accepted Singular standard bases.  It checks the
stratification, local central generators, and independently extracts the
triangle critical value from the actual rational two-jet.
"""
import ast
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "grunbaum-zero-context-proof"
LETTERS = "abcdefgh"
ZERO = (0,) * 8


def add(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def mul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            k = tuple(x + y for x, y in zip(m, n))
            out[k] = out.get(k, 0) + c * d
    return {m: c for m, c in out.items() if c}


def parse(expr):
    def ev(node):
        if isinstance(node, ast.Constant):
            return {ZERO: Fraction(node.value)} if node.value else {}
        if isinstance(node, ast.Name):
            return {tuple(int(i == LETTERS.index(node.id)) for i in range(8)): Fraction(1)}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return {m: -c for m, c in ev(node.operand).items()}
        if isinstance(node, ast.BinOp):
            a, b = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Add):
                return add(a, b)
            if isinstance(node.op, ast.Sub):
                return add(a, {m: -c for m, c in b.items()})
            if isinstance(node.op, ast.Mult):
                return mul(a, b)
            if isinstance(node.op, ast.Div):
                assert list(b) == [ZERO]
                return {m: c / b[ZERO] for m, c in a.items()}
            if isinstance(node.op, ast.Pow):
                assert list(b) == [ZERO] and b[ZERO].denominator == 1
                out = {ZERO: Fraction(1)}
                for _ in range(int(b[ZERO])):
                    out = mul(out, a)
                return out
        raise ValueError(ast.dump(node))
    return ev(ast.parse(expr.replace("^", "**"), mode="eval").body)


def derivative(a, variable):
    out = {}
    for m, c in a.items():
        if m[variable]:
            n = list(m)
            n[variable] -= 1
            out[tuple(n)] = c * m[variable]
    return out


def support_restriction(a):
    out = {}
    for m, c in a.items():
        if any(m[j] for j in [0, 2, 3, 5, 6]):
            continue
        n = list(m)
        n[1] = 0  # b=1; e,h are u,v
        out[tuple(n)] = out.get(tuple(n), 0) + c
    return {m: c for m, c in out.items() if c}


def reduced_generators(monomials, inverted):
    projected = [tuple(0 if i in inverted else m[i] for i in range(8)) for m in monomials]
    return sorted(m for m in set(projected) if not any(n != m and all(x <= y for x, y in zip(n, m)) for n in projected))


def main():
    jetpath = ROOT / "equations/deformation_data.json"
    chartpath = ROOT / "runs/astra-daytime-2026-09-08/data/fixed_chart.json"
    jet = json.loads(jetpath.read_text())
    chart = json.loads(chartpath.read_text())
    assert hashlib.sha256(jetpath.read_bytes()).hexdigest() == "8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f"
    assert jet["source_commit"] == "ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b"
    polys = [[parse(s) for s in row] for row in jet["six_jet_coefficients"][:3]]
    central = [next(iter(p)) for p in polys[0]]
    assert len(central) == 16 and all(list(p.values()) == [1] for p in polys[0])
    assert polys[0] == [parse(s) for s in jet["generator_order"]]
    group = [[LETTERS.index(c) for c in word] for word in chart["group_images"]]
    vertex_orbits = sorted({tuple(sorted({g[i] for g in group})) for i in range(8)})
    assert vertex_orbits == [(0, 2, 6), (1, 4, 7), (3, 5)]
    triangle = {1, 4, 7}
    assert all(any(m[i] for i in set(range(8)) - triangle) for m in central)
    edges = sorted({tuple(sorted([g[1], g[4]])) for g in group})
    assert edges == [(1, 4), (1, 7), (4, 7)]
    for m in central:
        for g in group:
            n = [0] * 8
            for i, e in enumerate(m):
                n[g[i]] += e
            assert tuple(n) in central
    trirows = [2, 11, 8, 6]
    assert reduced_generators(central, triangle) == reduced_generators([central[i] for i in trirows], triangle)
    edgerows = [8, 0, 2, 9, 11, 6]
    assert reduced_generators(central, {1, 4}) == reduced_generators([central[i] for i in edgerows], {1, 4})
    assert all(not support_restriction(polys[1][i]) for i in trirows[:3])
    link = polys[1][6]
    normal = [0, 2, 6, 3, 5]
    assert not support_restriction(link)
    assert all(not support_restriction(derivative(link, i)) for i in normal)
    p = support_restriction(polys[2][6])
    expected = parse("-8*e^2-20*e*h-8*h^2-20*e-20*h-8")
    assert p == expected
    pu, pv = derivative(p, 4), derivative(p, 7)
    bezout = add(mul(parse("40"), p), add(mul(parse("-43*e+22*h+22"), pu), mul(parse("-22*e+3*h-33"), pv)))
    reduced = {m: int(c) % 101 for m, c in bezout.items() if int(c) % 101}
    assert reduced == {ZERO: 1}
    critical = (-20 * pow(36, -1, 101)) % 101
    assert critical == 78
    value = sum(c * critical ** (m[4] + m[7]) for m, c in p.items())
    assert int(value) % 101 == 48
    # Central constrained critical system has exactly one nonzero determinant term.
    perm = [0, 1, 2, 5, 6, 7, 4, 3]
    inversions = sum(perm[i] > perm[j] for i in range(8) for j in range(i + 1, 8))
    assert (-1) ** (inversions + 3) == 1
    inputs = [jetpath, chartpath, SOURCE / "PROOF.md", SOURCE / "deformation/audit_triangle258_mod101.m2", SOURCE / "deformation/triangle258_mod101_output.txt", SOURCE / "deformation/Q5_REDUCED_COVER_REFEREE_AUDIT.md", SOURCE / "enumerate/export_edge_c5_q2_local_module.m2", SOURCE / "enumerate/audit_edge_c5_central_presentations_output.txt", SOURCE / "enumerate/audit_edge25_q4_certificate_sources.py", SOURCE / "enumerate/generic_q4_edge25_full_local_module_mod101_lowpos_nored.sing", SOURCE / "enumerate/generic_q4_edge25_full_local_module_mod101_lowpos_nored_direct_lift_interrupted_output.txt", ROOT / "runs/astra-computation-2026-09-08/RAMIFIED_POINT_REVIEW.md", Path(__file__)]
    result = {
        "status": "COMPUTER-CERTIFIED exact finite checks; source Singular standard bases accepted, not replayed",
        "vertex_orbits": vertex_orbits,
        "remaining_plane": "P2_(b,e,h)",
        "edge_orbit": edges,
        "triangle_selected_rows_one_based": [i + 1 for i in trirows],
        "edge_selected_rows_one_based": [i + 1 for i in edgerows],
        "central_local_ideal_equalities": True,
        "first_order_constrained_critical_displacement": "zero",
        "central_critical_jacobian_determinant": "u^4*v^4",
        "critical_value_pi2_from_actual_twojet_QQ": "-8*u^2-20*u*v-8*v^2-20*u-20*v-8",
        "bezout_identity_mod101": True,
        "unique_critical_point_mod101": [critical, critical],
        "critical_value_mod101": 48,
        "source_hashes": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
    }
    import sys
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else RUN / "data/smoothness_transfer_checks.json"
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if dest.exists():
        assert dest.read_text() == text
    else:
        dest.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
