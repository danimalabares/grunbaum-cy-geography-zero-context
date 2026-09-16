#!/usr/bin/env python3
"""Independent combinatorial computation of dim T^1_{A_K,0} (intrinsic first-order deformations
in degree 0 of the Stanley--Reisner ring of a combinatorial sphere K) from
Altmann--Christophersen, "Deforming Stanley-Reisner schemes", Math. Ann. 348 (2010):

  Theorem 4.6:  dim T^1_{A_K, c} = 1  iff  a in K and b in B(lk(a,K)),  for c = a - b,
  Definition 4.4: B(L) = { b subset of [L], |b| >= 2 : L = M * db with |M| a sphere (b not in L),
                                                 or L = (M * db) u (dM * b) with |M| a ball (b in L) },
  Theorem 4.1:  T^1_c depends only on the supports; b is squarefree, a has positive entries.

Degree 0 means |a|_1 = |b|, so the number of multidegrees with supports (a,b) is C(|b|-1,|a|-1):
  dim T^1_{A,0} = sum_{a in K, a nonempty} sum_{b in B(lk a), |b| >= |a|} C(|b|-1, |a|-1).
For a sphere, Theorem 5.5 identifies this with dim T^1_{P(K)} (H^1(Theta) = H^2(K) = 0), and with
Hom_S(I,A)_0 modulo the gl_n coordinate orbit -- the quantity computed by Macaulay2 in link_t1_t2.m2.
Also evaluates the closed formula of Theorem 5.7 for comparison."""
from __future__ import annotations

import itertools
import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import simplicial as S  # noqa: E402


def faces_of(facets):
    return S.all_faces(facets)


def join(A, B):
    """Join of two complexes given by their face sets (including empty face handled separately)."""
    out = set()
    for f in A | {frozenset()}:
        for g in B | {frozenset()}:
            if f or g:
                out.add(f | g)
    return out


def boundary_of_simplex(b):
    b = frozenset(b)
    return {frozenset(s) for k in range(1, len(b)) for s in itertools.combinations(sorted(b), k)}


def B_set(L_facets):
    """B(L) for a pure complex L (Definition 4.4), by direct verification of the join decompositions."""
    if not L_facets:
        return []
    L = faces_of(L_facets)
    V = S.vertices(L_facets)
    n = len(next(iter(L_facets))) - 1  # dim L
    out = []
    for k in range(2, len(V) + 1):
        for b in itertools.combinations(V, k):
            b = frozenset(b)
            db = boundary_of_simplex(b)
            # M := intersection of links of the facets of db  (= lk(b', L) for any facet b' of db)
            Ms = []
            for bp in db:
                if len(bp) == k - 1:
                    Ms.append({f for f in L if not (f & bp) and (f | bp) in L})
            M = set.intersection(*Ms) if Ms else set()
            if b not in L:
                # L = M * db  with M a sphere of dimension n-|b|+1
                if join(M, db) == L and M:
                    Mf = [f for f in M if len(f) == n - k + 2 + 0]  # facets of M have dim n-|b|+1 -> size n-k+2
                    if Mf and len({len(f) for f in Mf}) == 1 and set(faces_of(Mf)) == M and S.is_pseudomanifold(Mf) \
                            and S.euler_characteristic(S.f_vector(Mf)) == (1 + (-1) ** (n - k + 1)):
                        out.append(sorted(b))
                elif not M and k == n + 2:
                    # M empty: L = db itself (boundary of the simplex b); the empty complex is the (-1)-sphere
                    if db == L:
                        out.append(sorted(b))
            else:
                # b in L: L \ st(b) = M * db with M a ball
                stb = {f for f in L if b <= f}
                rest = L - stb
                if M and join(M, db) == rest:
                    Mf = [f for f in M if len(f) == n - k + 2]
                    if Mf and set(faces_of(Mf)) == M and S.euler_characteristic(S.f_vector(Mf)) == 1:
                        out.append(sorted(b))
                elif not M and rest == db:
                    out.append(sorted(b))
    return out


def t1_degree0(facets):
    facets = [frozenset(F) for F in facets]
    K = faces_of(facets)
    total = 0
    detail = {}
    for a in sorted(K, key=lambda f: (len(f), sorted(f))):
        lk = [F - a for F in facets if a <= F]
        lk = [f for f in lk if f]
        Bs = B_set(lk) if lk else []
        contrib = sum(comb(len(b) - 1, len(a) - 1) for b in Bs if len(b) >= len(a))
        if contrib:
            detail[",".join(map(str, sorted(a)))] = {"B(lk a)": Bs, "contribution": contrib}
        total += contrib
    return total, detail


def closed_formula(facets):
    """Theorem 5.7 (spheres): 11 d3 + 5 e3 + 3 e4 + e>=5 + c>=6 + 5 f1^(3) + 2 f1^(4)."""
    facets = [frozenset(F) for F in facets]
    V = S.vertices(facets)
    d3 = e3 = e4 = e5 = c6 = 0
    types = {}
    for v in V:
        lk = [F - {v} for F in facets if v in F]
        Bs = B_set(lk)
        nb = len(Bs)
        nv = len(S.vertices(lk))
        if nv == 4:
            d3 += 1; types[v] = "boundary of tetrahedron"
        elif nb == 5:
            e3 += 1; types[v] = "Sigma E_3"
        elif nb == 3:
            e4 += 1; types[v] = "Sigma E_4 (octahedron)"
        elif nb == 1:
            # Sigma E_n (n>=5) or dC(n,3), n>=6: distinguish by adjacency of the two special vertices
            b = Bs[0]
            edges = {f for f in faces_of(lk) if len(f) == 2}
            if frozenset(b) in edges:
                c6 += 1; types[v] = "boundary of cyclic C(n,3)"
            else:
                e5 += 1; types[v] = "Sigma E_n, n>=5"
        else:
            types[v] = "other (B empty)" if nb == 0 else f"B of size {nb}"
    edges = {f for f in faces_of(facets) if len(f) == 2}
    val = {e: sum(1 for F in facets if e <= F) for e in edges}
    f13 = sum(1 for e in edges if val[e] == 3)
    f14 = sum(1 for e in edges if val[e] == 4)
    return {"d3": d3, "e3": e3, "e4": e4, "e>=5": e5, "c>=6": c6, "f1^(3)": f13, "f1^(4)": f14,
            "vertex_link_types": {str(v): t for v, t in types.items()},
            "Theorem_5_7_value": 11 * d3 + 5 * e3 + 3 * e4 + e5 + c6 + 5 * f13 + 2 * f14}


if __name__ == "__main__":
    DATA = os.path.join(ROOT, "data", "links")
    out = {}
    for name in ("cp2_9_link_v9", "cp2_10_link_v1_x11", "cp2_10_link_v2_x12"):
        fac = S.parse_facets(open(os.path.join(DATA, name + ".txt")).read().replace("# MNF", "#"))
        total, detail = t1_degree0(fac)
        cf = closed_formula(fac)
        out[name] = {"dim_T1_A0_from_Theorem_4_6_and_Definition_4_4": total,
                     "contributions_by_face": detail, "closed_formula_Theorem_5_7": cf}
        print(name, "T1_A0 (Thm 4.6) =", total, "| Thm 5.7 closed formula =", cf["Theorem_5_7_value"],
              "| counts", {k: cf[k] for k in ("d3", "e3", "e4", "e>=5", "c>=6", "f1^(3)", "f1^(4)")})
    json.dump(out, open(os.path.join(ROOT, "output", "t1_formula.json"), "w"), indent=1)
