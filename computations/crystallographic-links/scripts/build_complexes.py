#!/usr/bin/env python3
"""Build and verify the input triangulations.

* CP^2_9 (Kuehnel--Banchoff 1983 table) -- regenerated independently from the
  Morin--Yoshida orbit description K = G.(12459) u G.(12456), G = <alpha,beta,gamma>.
* (S^2 x S^2)_16 and CP^2_10 (Bagchi--Datta, arXiv:1004.3157) -- generated from the
  published basic facets and the published generators of the automorphism groups.
Writes data/*.txt facet lists and output/build_complexes.json.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import simplicial as S  # noqa: E402

DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)
report = {}


def perm_closure(gens, points):
    e = {p: p for p in points}
    G = {tuple(sorted(e.items()))}
    frontier = [e]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = {p: s[g[p]] for p in points}
                key = tuple(sorted(h.items()))
                if key not in G:
                    G.add(key)
                    new.append(h)
        frontier = new
    return [dict(k) for k in G]


def orbit_of_facets(basic, group):
    out = set()
    for F in basic:
        for g in group:
            out.add(frozenset(g[v] for v in F))
    return sorted(out, key=lambda F: sorted(F))


# ---------------------------------------------------------------------------
# CP^2_9
# ---------------------------------------------------------------------------
kb = S.parse_facets(open(os.path.join(DATA, "cp2_9_facets_kuhnel_banchoff_1983.txt")).read())
assert len(kb) == 36 and len(set(kb)) == 36

# Morin--Yoshida Section 1 (p. 59): array [[1,4,7],[2,5,8],[3,6,9]];
# alpha cyclically permutes the columns, beta the rows, gamma is beta on column 1,
# beta^{-1} on column 2, identity on column 3.
alpha = {1: 4, 4: 7, 7: 1, 2: 5, 5: 8, 8: 2, 3: 6, 6: 9, 9: 3}
beta = {1: 2, 2: 3, 3: 1, 4: 5, 5: 6, 6: 4, 7: 8, 8: 9, 9: 7}
gamma = {1: 2, 2: 3, 3: 1, 4: 6, 6: 5, 5: 4, 7: 7, 8: 8, 9: 9}
G27 = perm_closure([alpha, beta, gamma], range(1, 10))
assert len(G27) == 27
my = orbit_of_facets([frozenset({1, 2, 4, 5, 9}), frozenset({1, 2, 4, 5, 6})], G27)
orb1 = orbit_of_facets([frozenset({1, 2, 4, 5, 9})], G27)
orb2 = orbit_of_facets([frozenset({1, 2, 4, 5, 6})], G27)
report["cp2_9"] = {
    "kuehnel_banchoff_facets": len(kb),
    "morin_yoshida_orbit_sizes": [len(orb1), len(orb2)],
    "morin_yoshida_regeneration_equals_KB_list": set(my) == set(kb),
}
assert set(my) == set(kb), "Morin--Yoshida orbit description must reproduce the KB table"
fv = S.f_vector(kb)
report["cp2_9"].update({
    "f_vector": fv, "euler_characteristic": S.euler_characteristic(fv),
    "pure": S.is_pure(kb), "pseudomanifold": S.is_pseudomanifold(kb),
    "strongly_connected": S.is_strongly_connected(kb),
    "two_neighbourly": fv[1] == 36, "three_neighbourly": fv[2] == 84,
})
auts9 = S.automorphism_group(kb)
report["cp2_9"]["automorphism_group_order"] = len(auts9)
report["cp2_9"]["vertex_orbits_under_Aut"] = S.orbits(auts9, range(1, 10))
mnf9 = S.minimal_nonfaces(kb)
report["cp2_9"]["minimal_nonfaces_by_size"] = {k: sum(1 for m in mnf9 if len(m) == k) for k in sorted({len(m) for m in mnf9})}
report["cp2_9"]["betti"] = S.betti_numbers(kb)
open(os.path.join(DATA, "cp2_9_facets.txt"), "w").write(
    "# CP^2_9: 36 facets, canonical labelling 1..9 of Kuehnel--Banchoff 1983 (= Morin--Yoshida 1991).\n"
    + "\n".join(S.facets_to_str([F]) for F in sorted(kb, key=sorted)) + "\n")

# ---------------------------------------------------------------------------
# (S^2 x S^2)_16 and CP^2_10  (Bagchi--Datta arXiv:1004.3157, Section 1)
# ---------------------------------------------------------------------------
def x(i, j):  # vertex label for x_{ij}, 1..16
    return 4 * (i - 1) + j

def a4_generators_on_indices():
    # alpha=(123), beta=(12)(34) acting on indices 1..4
    al = {1: 2, 2: 3, 3: 1, 4: 4}
    be = {1: 2, 2: 1, 3: 4, 4: 3}
    return al, be

al, be = a4_generators_on_indices()
A4 = perm_closure([al, be], range(1, 5))
assert len(A4) == 12
V16 = [x(i, j) for i in range(1, 5) for j in range(1, 5)]
def lift16(g):  # index permutation -> permutation of x_{ij}
    return {x(i, j): x(g[i], g[j]) for i in range(1, 5) for j in range(1, 5)}
swap16 = {x(i, j): x(j, i) for i in range(1, 5) for j in range(1, 5)}
G16 = perm_closure([lift16(al), lift16(be), swap16], V16)
assert len(G16) == 24
def X(s):  # parse "x11x22x33x12x13" -> frozenset of labels
    s = s.replace("x", " ").split()
    return frozenset(x(int(t[0]), int(t[1])) for t in s)
basic16 = [X("x11x22x33x12x13"), X("x11x22x12x14x34"), X("x11x22x14x24x34"),
           X("x11x22x21x24x31"), X("x11x22x24x31x34")]
S2S2 = orbit_of_facets(basic16, G16)
orbit_sizes16 = [len(orbit_of_facets([b], G16)) for b in basic16]
fv16 = S.f_vector(S2S2)
report["s2xs2_16"] = {
    "facets": len(S2S2), "orbit_sizes_of_basic_facets": orbit_sizes16,
    "f_vector": fv16, "expected_f_vector": [16, 84, 216, 240, 96],
    "pseudomanifold": S.is_pseudomanifold(S2S2), "strongly_connected": S.is_strongly_connected(S2S2),
    "euler_characteristic": S.euler_characteristic(fv16),
}
assert fv16 == [16, 84, 216, 240, 96]
auts16 = S.automorphism_group(S2S2)
report["s2xs2_16"]["automorphism_group_order"] = len(auts16)
report["s2xs2_16"]["betti"] = S.betti_numbers(S2S2)

# subdivision of the product cell complex S^2_4 x S^2_4: each facet lies in exactly one cell
def cell_of(F):
    I = frozenset((v - 1) // 4 + 1 for v in F)
    J = frozenset((v - 1) % 4 + 1 for v in F)
    return I, J
cells = {}
for F in S2S2:
    I, J = cell_of(F)
    assert len(I) == 3 and len(J) == 3, (sorted(F), I, J)
    cells.setdefault((I, J), []).append(F)
report["s2xs2_16"]["product_cells"] = len(cells)
report["s2xs2_16"]["facets_per_cell"] = sorted({len(v) for v in cells.values()})
assert len(cells) == 16 and set(len(v) for v in cells.values()) == {6}

# geometric check: in each cell Delta_2 x Delta_2 the six simplices form a triangulation.
def geometric_triangulation_check(cell_facets, I, J):
    """Coordinates: Delta_2 with vertices e_i (i in I) in R^2 (drop last), product in R^4.
    Check: (a) every simplex nondegenerate, (b) volumes sum to vol(Delta_2 x Delta_2) = 1/4 * ... in
    normalized units each simplex has |det| = 1 and there are 6 = C(4,2) of them, (c) opposite-side
    condition across every interior 3-face, (d) every boundary 3-face lies on a facet hyperplane of
    the polytope with all vertices on one side."""
    Il, Jl = sorted(I), sorted(J)
    def coord(v):
        i, j = (v - 1) // 4 + 1, (v - 1) % 4 + 1
        a = [1 if i == Il[0] else 0, 1 if i == Il[1] else 0]
        b = [1 if j == Jl[0] else 0, 1 if j == Jl[1] else 0]
        return a + b
    def det4(rows):
        # exact determinant of 4x4 via Fraction Gaussian elimination
        M = [[Fraction(v) for v in r] for r in rows]
        d = Fraction(1)
        for c in range(4):
            piv = next((r for r in range(c, 4) if M[r][c] != 0), None)
            if piv is None:
                return Fraction(0)
            if piv != c:
                M[c], M[piv] = M[piv], M[c]
                d = -d
            d *= M[c][c]
            for r in range(c + 1, 4):
                f = M[r][c] / M[c][c]
                for cc in range(c, 4):
                    M[r][cc] -= f * M[c][cc]
        return d
    def orient(simplex_pts):
        p0 = simplex_pts[0]
        return det4([[a - b for a, b in zip(p, p0)] for p in simplex_pts[1:]])
    vols = []
    for F in cell_facets:
        pts = [coord(v) for v in sorted(F)]
        d = orient(pts)
        assert d != 0, "degenerate simplex"
        vols.append(abs(d))
    assert sum(vols) == 6, vols  # normalized volume of Delta_2 x Delta_2 is C(4,2)=6
    # 3-faces
    inc = {}
    for F in cell_facets:
        for v in F:
            inc.setdefault(F - {v}, []).append(F)
    all_pts = [coord(x(i, j)) for i in I for j in J]
    for R, Fs in inc.items():
        Rpts = [coord(v) for v in sorted(R)]
        def side(p):
            return orient(Rpts + [p])
        if len(Fs) == 2:
            (F1,), (F2,) = [tuple(F - R) for F in Fs[:1]], [tuple(F - R) for F in Fs[1:]]
            s1, s2 = side(coord(F1[0])), side(coord(F2[0]))
            assert s1 * s2 < 0, "two simplices on the same side of a shared 3-face"
        else:
            assert len(Fs) == 1
            signs = {(-1 if side(p) < 0 else (1 if side(p) > 0 else 0)) for p in all_pts}
            signs.discard(0)
            assert len(signs) == 1, "boundary 3-face is not on a supporting hyperplane"
    return True

for (I, J), Fs in cells.items():
    geometric_triangulation_check(Fs, I, J)
report["s2xs2_16"]["each_cell_is_a_geometric_triangulation_of_Delta2xDelta2"] = True

# staircase description of each cell: the six simplices are the staircase paths for the vertex order 1<2<3<4?
def is_staircase(cell_facets, I, J):
    Il, Jl = sorted(I), sorted(J)
    paths = set()
    for pat in set(itertools.permutations("RRUU")):
        i = j = 0
        simplex = [x(Il[i], Jl[j])]
        for step in pat:
            if step == "R":
                i += 1
            else:
                j += 1
            simplex.append(x(Il[i], Jl[j]))
        paths.add(frozenset(simplex))
    return paths == set(cell_facets)
report["s2xs2_16"]["all_cells_are_staircase_triangulations_for_order_1<2<3<4"] = all(is_staircase(Fs, I, J) for (I, J), Fs in cells.items())

# swap invariance, pure action, quotient
swapped = {frozenset(swap16[v] for v in F) for F in S2S2}
assert swapped == set(S2S2)
pure = True
for F in S2S2:
    if frozenset(swap16[v] for v in F) == F:
        # the swap fixes this simplex as a set: pure iff it fixes it pointwise
        pure = pure and all(swap16[v] == v for v in F)
report["s2xs2_16"]["swap_invariant"] = True
report["s2xs2_16"]["swap_action_pure_on_facets"] = pure
# also check purity on all faces
faces16 = S.all_faces(S2S2)
pure_all = all(all(swap16[v] == v for v in f) for f in faces16 if frozenset(swap16[v] for v in f) == f)
report["s2xs2_16"]["swap_action_pure_on_all_faces"] = pure_all

# CP^2_10 from Bagchi--Datta basic facets
V10 = [(i, j) for i in range(1, 5) for j in range(i, 5)]
lab10 = {p: k + 1 for k, p in enumerate(V10)}   # (1,1)->1,(1,2)->2,...,(4,4)->10
def y(i, j):
    return lab10[(min(i, j), max(i, j))]
def Y(s):
    s = s.replace("x", " ").split()
    return frozenset(y(int(t[0]), int(t[1])) for t in s)
def lift10(g):
    return {y(i, j): y(g[i], g[j]) for (i, j) in V10}
G10 = perm_closure([lift10(al), lift10(be)], list(range(1, 11)))
assert len(G10) == 12
basic10 = [Y("x11x22x33x12x13"), Y("x11x22x12x14x34"), Y("x11x22x14x24x34"),
           Y("x11x22x12x13x24"), Y("x11x22x13x24x34")]
CP10 = orbit_of_facets(basic10, G10)
orbit_sizes10 = [len(orbit_of_facets([b], G10)) for b in basic10]
fv10 = S.f_vector(CP10)
report["cp2_10"] = {
    "vertex_labels": {str(k): f"x{i}{j}" for (i, j), k in lab10.items()},
    "facets": len(CP10), "orbit_sizes_of_basic_facets": orbit_sizes10,
    "f_vector": fv10, "expected_f_vector": [10, 45, 110, 120, 48],
    "euler_characteristic": S.euler_characteristic(fv10),
    "pseudomanifold": S.is_pseudomanifold(CP10), "strongly_connected": S.is_strongly_connected(CP10),
    "two_neighbourly": fv10[1] == 45,
}
assert fv10 == [10, 45, 110, 120, 48]
auts10 = S.automorphism_group(CP10)
report["cp2_10"]["automorphism_group_order"] = len(auts10)
report["cp2_10"]["vertex_orbits_under_Aut"] = S.orbits(auts10, range(1, 11))
report["cp2_10"]["betti"] = S.betti_numbers(CP10)
mnf10 = S.minimal_nonfaces(CP10)
report["cp2_10"]["minimal_nonfaces_by_size"] = {k: sum(1 for m in mnf10 if len(m) == k) for k in sorted({len(m) for m in mnf10})}

# quotient of (S^2xS^2)_16 by the swap equals CP^2_10 (as labelled complexes)
proj = {x(i, j): y(i, j) for i in range(1, 5) for j in range(1, 5)}
quot = {frozenset(proj[v] for v in F) for F in S2S2}
assert all(len(F) == 5 for F in quot)
report["cp2_10"]["equals_swap_quotient_of_s2xs2_16"] = quot == set(CP10)
report["cp2_10"]["swap_quotient_facet_count"] = len(quot)
assert quot == set(CP10)

# odd permutations of the 4 indices are NOT automorphisms (needed for the (4,2)_1 discussion)
def index_perm_is_aut(g, complex_facets, lift):
    L = lift(g)
    return {frozenset(L[v] for v in F) for F in complex_facets} == set(complex_facets)
S4 = perm_closure([{1: 2, 2: 1, 3: 3, 4: 4}, {1: 2, 2: 3, 3: 4, 4: 1}], range(1, 5))
assert len(S4) == 24
def sign(g):
    s = 1
    for i, j in itertools.combinations(range(1, 5), 2):
        if (g[i] - g[j]) * (i - j) < 0:
            s = -s
    return s
report["cp2_10"]["index_permutations_that_are_automorphisms"] = {
    "even_count": sum(1 for g in S4 if sign(g) == 1 and index_perm_is_aut(g, CP10, lift10)),
    "odd_count": sum(1 for g in S4 if sign(g) == -1 and index_perm_is_aut(g, CP10, lift10)),
}
report["s2xs2_16"]["index_permutations_that_are_automorphisms"] = {
    "even_count": sum(1 for g in S4 if sign(g) == 1 and index_perm_is_aut(g, S2S2, lift16)),
    "odd_count": sum(1 for g in S4 if sign(g) == -1 and index_perm_is_aut(g, S2S2, lift16)),
}
# the odd permutation (34) carries CP^2_10 to the other (isomorphic) subdivision
t34 = {1: 1, 2: 2, 3: 4, 4: 3}
CP10_prime = [frozenset(lift10(t34)[v] for v in F) for F in CP10]
report["cp2_10"]["image_under_(34)_is_different_complex"] = set(CP10_prime) != set(CP10)
report["cp2_10"]["image_under_(34)_is_isomorphic"] = S.isomorphism(CP10, CP10_prime) is not None

open(os.path.join(DATA, "s2xs2_16_facets.txt"), "w").write(
    "# (S^2 x S^2)_16 of Bagchi--Datta arXiv:1004.3157; vertex x_ij -> label 4(i-1)+j, i,j in 1..4.\n"
    "# Generated from the five basic facets and the group A_4 x Z_2 of the paper.\n"
    + "\n".join(",".join(map(str, sorted(F))) for F in S2S2) + "\n")
open(os.path.join(DATA, "cp2_10_facets.txt"), "w").write(
    "# CP^2_10 of Bagchi--Datta arXiv:1004.3157; vertex labels: "
    + ", ".join(f"{k}=x{i}{j}" for (i, j), k in sorted(lab10.items(), key=lambda t: t[1])) + "\n"
    "# Generated from the five basic facets and the group A_4 = <(123),(12)(34)> of the paper.\n"
    + "\n".join(",".join(map(str, sorted(F))) for F in CP10) + "\n")

json.dump(report, open(os.path.join(OUT, "build_complexes.json"), "w"), indent=1, default=str)
print(json.dumps(report, indent=1, default=str))
