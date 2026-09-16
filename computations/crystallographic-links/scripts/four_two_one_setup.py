#!/usr/bin/env python3
"""Finite model shared by four_two_one_counting.py (fast) and four_two_one_search.py (slow):
the coarse '(centre, corner, midpoint)' decomposition of E = C/Z[i] on the cover Z^2/12Z^2, the
group H_N = (G(4,2,2) x| Lambda')/(2Z[i])^2 acting on E_N x E_N, the product cells and the vertex orbits."""
from __future__ import annotations

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lifts import Torus, matvec, matmul  # noqa: E402

L = [[6, 0], [0, 6]]
N = 2
T = Torus(L, N)
rot = [[0, -1], [1, 0]]
_c = (3, 3)
_corners = [(0, 0), (6, 0), (6, 6), (0, 6)]
_mids = [(3, 0), (6, 3), (3, 6), (0, 3)]
base = []
for k in range(4):
    base.append((_c, _corners[k], _mids[k]))
    base.append((_c, _mids[k], _corners[(k + 1) % 4]))
tris = set()
for lam in T.lattice_vectors():
    for tri in base:
        tris.add(frozenset(T.reduce((p[0] + lam[0], p[1] + lam[1])) for p in tri))
tris = sorted(tris, key=sorted)
verts = sorted(set().union(*tris))
idx = {v: i for i, v in enumerate(verts)}
nV = len(verts)


def pid(p, q):
    return idx[p] * nV + idx[q]


_rp = lambda p: T.reduce(matvec(rot, p))
_r2 = lambda p: T.reduce(matvec(matmul(rot, rot), p))
_rinv = lambda p: T.reduce(matvec(matmul(matmul(rot, rot), rot), p))
_id = lambda p: p


def _sh(dx, dy):
    return lambda p: T.reduce((p[0] + dx, p[1] + dy))


def _perm(f1, f2, swap=False):
    P = [0] * (nV * nV)
    for p in verts:
        for q in verts:
            a, b = f1(p), f2(q)
            P[pid(p, q)] = pid(b, a) if swap else pid(a, b)
    return P


GENS = {
    "swap": _perm(_id, _id, swap=True),
    "diag(i^-1,i)": _perm(_rinv, _rp),
    "diag(-1,1)": _perm(_r2, _id),
    "t_x(1-i)": _perm(_sh(6, -6), _id),
    "t_x(1+i)": _perm(_sh(6, 6), _id),
    "t_y(1-i)": _perm(_id, _sh(6, -6)),
    "t_y(1+i)": _perm(_id, _sh(6, 6)),
    "t_diag(1,1)": _perm(_sh(6, 0), _sh(6, 0)),
}


def _compose(P, Q):
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
                h = _compose(s, g)
                th = tuple(h)
                if th not in G:
                    G.add(th)
                    new.append(h)
        frontier = new
    return [list(g) for g in G]


_H = None


def H():
    global _H
    if _H is None:
        _H = closure(list(GENS.values()))
    return _H


def H_order():
    return len(H())


def n_cells():
    return len(tris) ** 2


def n_vertex_orbits():
    seen, orbits = set(), 0
    for p in verts:
        for q in verts:
            v = pid(p, q)
            if v in seen:
                continue
            orbits += 1
            for g in H():
                seen.add(g[v])
    return orbits
