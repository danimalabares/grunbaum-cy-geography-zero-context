#!/usr/bin/env python3
"""Enumerate all triangulations (without new vertices) of the product of two triangles
Delta_2 x Delta_2 (expected 108, all with six unimodular simplices), by depth-first completion
from a triangulation of one boundary prism, checking the opposite-side condition on every
interior 3-face and the supporting-hyperplane condition on every boundary 3-face.
Also identifies the triangulations invariant under the factor swap and among those the
'pure' ones (no simplex is mapped to itself unless fixed pointwise)."""
from __future__ import annotations

import itertools
import json
import os
import sys
from fractions import Fraction

# vertices (i,j), i,j in {0,1,2}; coordinates: e_i in R^2 (e_0 = origin) for each factor
V = [(i, j) for i in range(3) for j in range(3)]
def coord(v):
    i, j = v
    return (1 if i == 1 else 0, 1 if i == 2 else 0, 1 if j == 1 else 0, 1 if j == 2 else 0)


def det4(rows):
    M = [[Fraction(x) for x in r] for r in rows]
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


def orient(pts):
    p0 = pts[0]
    return det4([[a - b for a, b in zip(p, p0)] for p in pts[1:]])


SIMPLICES = [frozenset(s) for s in itertools.combinations(V, 5) if orient([coord(v) for v in s]) != 0]
# facets of the polytope: Delta_2 x edge  and  edge x Delta_2
PRISMS = [frozenset((i, j) for i in range(3) for j in e) for e in itertools.combinations(range(3), 2)] + \
         [frozenset((i, j) for i in e for j in range(3)) for e in itertools.combinations(range(3), 2)]


def side(face, p):
    return orient([coord(v) for v in sorted(face)] + [coord(p)])


def is_boundary_face(face):
    return any(face <= P for P in PRISMS)


def complete(chosen, faces_count):
    """chosen: set of simplices; faces_count: dict 3-face -> list of simplices containing it."""
    # find an open interior face
    open_faces = [f for f, lst in faces_count.items() if len(lst) == 1 and not is_boundary_face(f)]
    if not open_faces:
        if len(chosen) == 6:
            yield frozenset(chosen)
        return
    f = min(open_faces, key=lambda x: sorted(x))
    s0 = faces_count[f][0]
    opp0 = next(iter(s0 - f))
    sgn0 = side(f, opp0)
    for s in SIMPLICES:
        if s in chosen or not (f <= s):
            continue
        opp = next(iter(s - f))
        if side(f, opp) * sgn0 >= 0:
            continue
        # no 3-face may be contained in more than 2 simplices, boundary faces in at most 1
        ok = True
        new_faces = []
        for v in s:
            g = s - {v}
            cnt = len(faces_count.get(g, []))
            if cnt >= 2 or (cnt == 1 and is_boundary_face(g)):
                ok = False
                break
            new_faces.append(g)
        if not ok:
            continue
        for g in new_faces:
            faces_count.setdefault(g, []).append(s)
        chosen.add(s)
        if len(chosen) <= 6:
            yield from complete(chosen, faces_count)
        chosen.remove(s)
        for g in new_faces:
            faces_count[g].remove(s)
            if not faces_count[g]:
                del faces_count[g]


def prism_triangulations(P):
    """The triangulations of a prism (3 tetrahedra from its 6 vertices, proper)."""
    pts = sorted(P)
    tets = [frozenset(t) for t in itertools.combinations(pts, 4)
            if det4([[a - b for a, b in zip(coord(q), coord(t[0]))] for q in t[1:]] + [[0, 0, 0, 0]]) is not None]
    # 3-dimensional nondegeneracy inside the prism's affine hull: use rank via volumes in 4D with an extra point
    def nondeg3(t):
        # 4 points affinely independent iff some 4x4 det with an outside point is nonzero
        outside = next(v for v in V if v not in P)
        return orient([coord(v) for v in sorted(t)] + [coord(outside)]) != 0
    tets = [t for t in tets if nondeg3(t)]
    out = []
    for trip in itertools.combinations(tets, 3):
        # proper: every 2-face inside the prism either boundary (in one tet) or shared by two tets
        fc = {}
        for t in trip:
            for v in t:
                g = t - {v}
                fc.setdefault(g, []).append(t)
        if any(len(l) > 2 for l in fc.values()):
            continue
        # covering check: total volume = 3 unit tetrahedra? use the 4-simplex volumes with the outside point
        outside = next(v for v in V if v not in P)
        vol = sum(abs(orient([coord(v) for v in sorted(t)] + [coord(outside)])) for t in trip)
        if vol != 3 * abs(orient([coord(v) for v in sorted(tets[0])] + [coord(outside)])):
            continue
        # opposite sides inside the prism: for shared faces the two opposite vertices are separated
        good = True
        for g, l in fc.items():
            if len(l) == 2:
                a = next(iter(l[0] - g)); b = next(iter(l[1] - g))
                # separated within the 3-flat: check via 4D orientation with the outside point
                sa = orient([coord(v) for v in sorted(g)] + [coord(a)] + [coord(outside)])
                sb = orient([coord(v) for v in sorted(g)] + [coord(b)] + [coord(outside)])
                if sa * sb >= 0:
                    good = False
                    break
        if good:
            out.append(frozenset(trip))
    return out


def all_triangulations():
    P0 = PRISMS[0]
    result = set()
    for pt in prism_triangulations(P0):
        # each boundary tetrahedron of pt must be the boundary 3-face of a unique simplex; seed with them
        for combo in itertools.product(*[[s for s in SIMPLICES if t <= s] for t in pt]):
            chosen = set(combo)
            if len(chosen) != 3:
                continue
            faces_count = {}
            ok = True
            for s in chosen:
                for v in s:
                    g = s - {v}
                    faces_count.setdefault(g, []).append(s)
            if any(len(l) > 2 or (len(l) == 2 and is_boundary_face(g)) for g, l in faces_count.items()):
                continue
            # opposite sides for shared faces among the seed
            for g, l in faces_count.items():
                if len(l) == 2:
                    a = next(iter(l[0] - g)); b = next(iter(l[1] - g))
                    if side(g, a) * side(g, b) >= 0:
                        ok = False
            if not ok:
                continue
            for T in complete(chosen, faces_count):
                result.add(T)
    return result


def check_triangulation(T):
    fc = {}
    for s in T:
        for v in s:
            fc.setdefault(s - {v}, []).append(s)
    for g, l in fc.items():
        if len(l) == 2:
            a = next(iter(l[0] - g)); b = next(iter(l[1] - g))
            assert side(g, a) * side(g, b) < 0
        else:
            assert len(l) == 1 and is_boundary_face(g)
    assert sum(abs(orient([coord(v) for v in sorted(s)])) for s in T) == 6
    return True


SWAP = {(i, j): (j, i) for (i, j) in V}


def swap_invariant(T):
    return {frozenset(SWAP[v] for v in s) for s in T} == set(T)


def pure_under_swap(T):
    for s in T:
        if frozenset(SWAP[v] for v in s) == s and any(SWAP[v] != v for v in s):
            return False
    return True


if __name__ == "__main__":
    tri = all_triangulations()
    for T in tri:
        check_triangulation(T)
    inv = [T for T in tri if swap_invariant(T)]
    pure = [T for T in inv if pure_under_swap(T)]
    print(json.dumps({"nondegenerate_5_subsets": len(SIMPLICES), "prisms": len(PRISMS),
                      "triangulations_of_Delta2xDelta2": len(tri),
                      "swap_invariant": len(inv), "swap_invariant_and_pure": len(pure)}))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "prism_triangulations.json")
    json.dump({"triangulations": [[sorted(s) for s in T] for T in sorted(tri, key=lambda T: sorted(sorted(s) for s in T))],
               "swap_invariant_indices": None}, open(out, "w"))
