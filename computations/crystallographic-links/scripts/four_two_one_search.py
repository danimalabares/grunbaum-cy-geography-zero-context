#!/usr/bin/env python3
"""Vertex-minimal search for the row (4,2)_1.

Setting (see REPORT.md): with s = (1+i)/2 one has s^{-1} (4,2)_1 s = H := G(4,2,2) x| Lambda',
Lambda' = ((1-i)Z[i])^2 + Z(1,1), a subgroup of index 4 of (4,1)_0 = G(4,1,2) x| Z[i]^2.  The
points of C^2 lying on two reflection lines of H are exactly the pairs of points of
(1/2)Z[i] (in the coordinates of (4,1)_0), i.e. E[2] x E[2] on E x E, E = C/Z[i].  The natural
H-invariant cell structure with this vertex set is the product of two copies of the
'(centre, corner, midpoint)' decomposition of E (8 triangles per period, vertex set E[2]).
We search for an admissible diagonalisation (Arnoux--Marin's notion): a choice of one of the
108 triangulations of Delta_2 x Delta_2 in every product cell, compatible on shared prisms,
H-invariant, and regular (no simplex mapped to itself by a nontrivial element unless fixed
pointwise), such that the quotient by H is a simplicial complex.  The search runs on the torus
cover Z^2/12Z^2 (E-coordinates scaled by 6, as in lifts.py, model m4 without barycentres).
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import prism_triangulations as PT  # noqa: E402
from lifts import Torus, matvec, matmul  # noqa: E402

OUT = os.path.join(ROOT, "output")

# ------------------------------------------------------------------ E-model: coarse (c, corner, midpoint)
L = [[6, 0], [0, 6]]
N = 2
T = Torus(L, N)
rot = [[0, -1], [1, 0]]
c = (3, 3)
corners = [(0, 0), (6, 0), (6, 6), (0, 6)]
mids = [(3, 0), (6, 3), (3, 6), (0, 3)]
base = []
for k in range(4):
    base.append((c, corners[k], mids[k]))
    base.append((c, mids[k], corners[(k + 1) % 4]))
tris = set()
for lam in T.lattice_vectors():
    for tri in base:
        tris.add(frozenset(T.reduce((p[0] + lam[0], p[1] + lam[1])) for p in tri))
tris = sorted(tris, key=sorted)
verts = sorted(set().union(*tris))
assert len(tris) == 32 and len(verts) == 16
# check simplicial on the cover
edges = {}
for t in tris:
    for e in itertools.combinations(sorted(t), 2):
        edges[frozenset(e)] = edges.get(frozenset(e), 0) + 1
assert all(v == 2 for v in edges.values())

# ------------------------------------------------------------------ group H_N acting on the cover E_N x E_N
idx = {v: i for i, v in enumerate(verts)}
nV = len(verts)
def pid(p, q):
    return idx[p] * nV + idx[q]
R = rot
rp = lambda p: T.reduce(matvec(R, p))
r2 = lambda p: T.reduce(matvec(matmul(R, R), p))
rinv = lambda p: T.reduce(matvec(matmul(matmul(R, R), R), p))
ident = lambda p: p
def sh(dx, dy):
    return lambda p: T.reduce((p[0] + dx, p[1] + dy))
def perm(f1, f2, swap=False):
    P = [0] * (nV * nV)
    for p in verts:
        for q in verts:
            a, b = f1(p), f2(q)
            P[pid(p, q)] = pid(b, a) if swap else pid(a, b)
    return P
GENS = {
    "swap": perm(ident, ident, swap=True),
    "diag(i^-1,i)": perm(rinv, rp),
    "diag(-1,1)": perm(r2, ident),
    "t_x(1-i)": perm(sh(6, -6), ident),
    "t_x(1+i)": perm(sh(6, 6), ident),
    "t_y(1-i)": perm(ident, sh(6, -6)),
    "t_y(1+i)": perm(ident, sh(6, 6)),
    "t_diag(1,1)": perm(sh(6, 0), sh(6, 0)),
}
def compose(P, Q):  # P after Q
    return [P[Q[i]] for i in range(len(Q))]
def closure(gens):
    n = len(next(iter(gens)))
    e = list(range(n))
    G = {tuple(e)}
    frontier = [e]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = compose(s, g)
                th = tuple(h)
                if th not in G:
                    G.add(th)
                    new.append(h)
        frontier = new
    return [list(g) for g in G]
H = closure(list(GENS.values()))
print("order of H_N on the cover:", len(H), flush=True)

# ------------------------------------------------------------------ product cells and their vertex sets
cells = []
for s in tris:
    for t in tris:
        cells.append((s, t))
cell_vertices = [frozenset(pid(p, q) for p in s for q in t) for (s, t) in cells]
cell_index = {cv: i for i, cv in enumerate(cell_vertices)}
assert len(cell_index) == len(cells)

# each cell gets coordinates: identify its 9 vertices with (i,j) of the standard Delta_2 x Delta_2
def cell_frame(ci):
    s, t = cells[ci]
    ss, tt = sorted(s), sorted(t)
    fw = {pid(ss[i], tt[j]): (i, j) for i in range(3) for j in range(3)}
    bw = {(i, j): pid(ss[i], tt[j]) for i in range(3) for j in range(3)}
    return fw, bw
FRAMES = [cell_frame(ci) for ci in range(len(cells))]

TRIS108 = sorted(PT.all_triangulations(), key=lambda Tt: sorted(sorted(x) for x in Tt))
print("triangulations of Delta2xDelta2:", len(TRIS108), flush=True)

def realise(ci, k):
    """Facets (as frozensets of cover vertex ids) of triangulation k placed in cell ci."""
    fw, bw = FRAMES[ci]
    return [frozenset(bw[v] for v in s) for s in TRIS108[k]]

# group action on cells
def act_cell(g, ci):
    return cell_index[frozenset(g[v] for v in cell_vertices[ci])]

# orbits of cells and stabilisers
seen = set()
orbits = []
for ci in range(len(cells)):
    if ci in seen:
        continue
    orb = {}
    for g in H:
        cj = act_cell(g, ci)
        if cj not in orb:
            orb[cj] = g  # g maps ci -> cj
    for cj in orb:
        seen.add(cj)
    stab = [g for g in H if act_cell(g, ci) == ci]
    orbits.append({"rep": ci, "members": orb, "stab": stab})
print("cell orbits:", len(orbits), "sizes:", [len(o["members"]) for o in orbits], "stabiliser orders:", [len(o["stab"]) for o in orbits], flush=True)

# admissible choices for a representative: triangulations invariant under its stabiliser and regular
def transport(facets, g):
    return {frozenset(g[v] for v in F) for F in facets}
def regular(facets, stab):
    for g in stab:
        for F in facets:
            if frozenset(g[v] for v in F) == F and any(g[v] != v for v in F):
                return False
    return True
domains = []
for o in orbits:
    ci = o["rep"]
    dom = []
    for k in range(len(TRIS108)):
        fac = set(realise(ci, k))
        if all(transport(fac, g) == fac for g in o["stab"]) and regular(fac, o["stab"]):
            dom.append(k)
    domains.append(dom)
print("domain sizes after stabiliser invariance + regularity:", [len(d) for d in domains], flush=True)

# prism (3-face) compatibility: two cells sharing a prism (6 common vertices) must induce the same
# triangulation on it.  For a choice on all cells we check: every 3-face (tetrahedron) that lies in
# a prism shared by two cells is a face of the triangulation of both or of neither.
def induced_on_prism(facets, prism_vertices):
    out = set()
    for F in facets:
        for v in F:
            g = F - {v}
            if g <= prism_vertices:
                out.add(g)
    return frozenset(out)

# adjacency between cells: shared 6-vertex prisms
prism_of = {}
for ci, cv in enumerate(cell_vertices):
    s, t = cells[ci]
    for e in itertools.combinations(sorted(s), 2):
        pv = frozenset(pid(p, q) for p in e for q in t)
        prism_of.setdefault(pv, []).append(ci)
    for e in itertools.combinations(sorted(t), 2):
        pv = frozenset(pid(p, q) for p in s for q in e)
        prism_of.setdefault(pv, []).append(ci)
assert all(len(l) == 2 for l in prism_of.values())
neighbours = {}
for pv, (a, b) in prism_of.items():
    neighbours.setdefault(a, []).append((b, pv))
    neighbours.setdefault(b, []).append((a, pv))

# assignment: orbit variable -> triangulation index k for the representative; cells in the orbit
# get transported triangulations.
orbit_of_cell = {}
for oi, o in enumerate(orbits):
    for cj in o["members"]:
        orbit_of_cell[cj] = oi
def facets_of_cell_choice(cj, k):
    oi = orbit_of_cell[cj]
    o = orbits[oi]
    g = o["members"][cj]  # maps rep -> cj
    return transport(set(realise(o["rep"], k)), g)

# Binary CSP: for every prism shared by cells (a,b) the induced prism triangulations must agree.
# Precompute, for each cell and each admissible choice, the induced triangulation on each of its prisms.
induced_cache = {}
def induced(cj, k, pv):
    key = (cj, k, pv)
    if key not in induced_cache:
        induced_cache[key] = induced_on_prism(facets_of_cell_choice(cj, k), pv)
    return induced_cache[key]

# constraints between orbit variables: allowed pairs
allowed = {}   # (oi, oj) with oi < oj -> set of (ki, kj) ; unary constraints for oi == oj
unary = {oi: set(domains[oi]) for oi in range(len(orbits))}
pair_sets = {}
for pv, (a, b) in prism_of.items():
    oa, ob = orbit_of_cell[a], orbit_of_cell[b]
    if oa == ob:
        ok = {k for k in unary[oa] if induced(a, k, pv) == induced(b, k, pv)}
        unary[oa] &= ok
    else:
        if oa > ob:
            a, b, oa, ob = b, a, ob, oa
        S_ab = {(ka, kb) for ka in domains[oa] for kb in domains[ob] if induced(a, ka, pv) == induced(b, kb, pv)}
        if (oa, ob) in pair_sets:
            pair_sets[(oa, ob)] &= S_ab
        else:
            pair_sets[(oa, ob)] = S_ab
print("unary-reduced domains:", [len(unary[oi]) for oi in range(len(orbits))], flush=True)
print("binary constraints:", {str(k): len(v) for k, v in pair_sets.items()}, flush=True)

solutions = []
t0 = time.time()
order = sorted(range(len(orbits)), key=lambda oi: len(unary[oi]))
def compatible(assign, oi, k):
    for oj, kj in assign.items():
        key = (min(oi, oj), max(oi, oj))
        if key in pair_sets:
            pair = (k, kj) if oi < oj else (kj, k)
            if pair not in pair_sets[key]:
                return False
    return True
def backtrack(pos, assign):
    if len(solutions) >= 1000:
        return
    if pos == len(order):
        solutions.append(dict(assign))
        return
    oi = order[pos]
    for k in sorted(unary[oi]):
        if compatible(assign, oi, k):
            assign[oi] = k
            backtrack(pos + 1, assign)
            del assign[oi]
backtrack(0, {})
print(f"invariant compatible diagonalisations found: {len(solutions)} (search time {time.time() - t0:.1f}s)", flush=True)

def facets_of_cell(cj, assignment):
    return facets_of_cell_choice(cj, assignment[orbit_of_cell[cj]])

# quotient admissibility for each solution: all faces have pairwise distinct H-orbits, and face
# orbits inject into colour-sets
result = {"H_order_on_cover": len(H), "cells": len(cells), "cell_orbits": len(orbits),
          "orbit_sizes": [len(o["members"]) for o in orbits], "stabiliser_orders": [len(o["stab"]) for o in orbits],
          "domain_sizes": [len(d) for d in domains], "unary_reduced_domains": [len(unary[oi]) for oi in range(len(orbits))],
          "invariant_compatible_solutions": len(solutions), "admissible": []}
def union_find_orbits(items, gens):
    parent = {x: x for x in items}
    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root
    for x in items:
        for P in gens:
            y = frozenset(P[v] for v in x)
            ra, rb = find(x), find(y)
            if ra != rb:
                parent[ra] = rb
    roots = {}
    for x in items:
        roots.setdefault(find(x), []).append(x)
    return roots
n_adm = 0
for sol in solutions:
    facets = set()
    for cj in range(len(cells)):
        facets |= facets_of_cell(cj, sol)
    faces = {k: set() for k in range(5)}
    for F in facets:
        Fs = sorted(F)
        for k in range(1, 6):
            for Sub in itertools.combinations(Fs, k):
                faces[k - 1].add(frozenset(Sub))
    gens = list(GENS.values())
    vorb = union_find_orbits(list(faces[0]), gens)
    colour = {}
    for r, mem in vorb.items():
        for x in mem:
            colour[next(iter(x))] = r
    distinct = all(len({colour[v] for v in F}) == 5 for F in facets)
    inj = {}
    for k in range(5):
        orbs = union_find_orbits(list(faces[k]), gens)
        images = {frozenset(colour[v] for v in f) for f in faces[k]}
        inj[k] = (len(orbs), len(images))
    adm = distinct and all(a == b for a, b in inj.values())
    qf = [inj[k][1] for k in range(5)]
    entry = {"assignment": {str(k): v for k, v in sol.items()}, "facets_on_cover": len(facets),
             "vertex_orbits": len(vorb), "facets_distinct_colours": distinct,
             "face_orbits_vs_images": inj, "quotient_is_simplicial": adm, "quotient_f_vector_of_images": qf}
    if adm:
        n_adm += 1
        qfacets = sorted({tuple(sorted(colour[v] for v in F)) for F in facets})
        entry["quotient_facets"] = qfacets
    result["admissible"].append(entry)
    print("solution:", json.dumps({k: v for k, v in entry.items() if k != "quotient_facets"}), flush=True)
result["admissible_solutions"] = n_adm
json.dump(result, open(os.path.join(OUT, "four_two_one_search.json"), "w"), indent=1, default=str)
print("DONE")
