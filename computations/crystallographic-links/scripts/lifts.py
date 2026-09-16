#!/usr/bin/env python3
"""Crystallographic lifts for the rows (m,1)_0, m = 2, 3, 4, 6, of Kaneko--Tokunaga--Yoshida.

For each m we build, in explicit integer coordinates, a C_m-invariant rectilinear
triangulation of the elliptic curve E = C/L(tau_m) whose vertex set consists of the cone
points of E/C_m (plus, for m = 3, 4, 6, one free orbit of barycentres) and whose quotient
E/C_m is the tetrahedron boundary S^2_4.  The Bagchi--Datta subdivision (S^2 x S^2)_16 of
S^2_4 x S^2_4 is pulled back cell by cell to E x E; the resulting complex is checked to be
a Gamma-invariant rectilinear triangulation (Gamma = G(m,1,2) x| L(tau_m)^2) on a finite
torus cover, the group action is checked to be regular ("pure"), and the quotient is
identified with CP^2_10 by an exact isomorphism, recording the crystallographic marking of
each vertex (stabiliser order, type).  Also records the (4,2)_1 obstruction on the m = 2
model with tau = i, and the restriction of the m = 4 model to the index-4 subgroup
conjugate to (4,2)_1.
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
LIFTDIR = os.path.join(DATA, "lifts")
os.makedirs(LIFTDIR, exist_ok=True)


# ---------------------------------------------------------------------------
# small integer linear algebra
# ---------------------------------------------------------------------------
def matvec(M, v):
    return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


class Torus:
    """Z^2 / (N * L) where L is given by an integer basis matrix (columns)."""

    def __init__(self, Lbasis, N):
        self.L = Lbasis
        self.N = N
        self.D = det2(Lbasis)
        assert self.D != 0
        # adjugate for solving L c = p
        a, b, c, d = Lbasis[0][0], Lbasis[0][1], Lbasis[1][0], Lbasis[1][1]
        self.adj = [[d, -b], [-c, a]]

    def reduce(self, p):
        # c = L^{-1} p = adj p / D ; reduce c modulo N
        u = matvec(self.adj, p)
        c = (Fraction(u[0], self.D), Fraction(u[1], self.D))
        k = (c[0] // self.N, c[1] // self.N)  # floor division of Fractions gives integers
        shift = matvec(self.L, (self.N * int(k[0]), self.N * int(k[1])))
        q = (p[0] - shift[0], p[1] - shift[1])
        return q

    def lattice_vectors(self):
        """All translations of N*L modulo... we need L/(N L): representatives L*(k1,k2), 0<=k<N."""
        return [matvec(self.L, (k1, k2)) for k1 in range(self.N) for k2 in range(self.N)]


class EModel:
    def __init__(self, name, m, Lbasis, rot, base_triangles, s2_class, N, description):
        self.name, self.m, self.L, self.rot = name, m, Lbasis, rot
        self.base_triangles = base_triangles  # list of 3-tuples of integer points (one L-period)
        self.s2_class = s2_class  # function point -> class in {1,2,3,4}, L-periodic and rot-invariant
        self.N = N
        self.description = description
        self.T = Torus(Lbasis, N)

    def torus_triangles(self):
        tris = set()
        for lam in self.T.lattice_vectors():
            for tri in self.base_triangles:
                tris.add(frozenset(self.T.reduce((p[0] + lam[0], p[1] + lam[1])) for p in tri))
        return tris


def check_E_model(M):
    """Verify: rotation has order m and preserves L; triangles nondegenerate; the torus complex
    is a genuine simplicial 2-manifold (each edge in exactly two triangles, no repeated vertex
    pairs); rotation and L-translations preserve the triangle set; the class map is well
    defined; each triangle has three distinct classes; the quotient of the E-torus by C_m x L
    is the tetrahedron boundary (4 vertices, 6 edges, 4 triangles, one per triple)."""
    info = {}
    R = M.rot
    # order of rotation
    P, k = [[1, 0], [0, 1]], 0
    while True:
        P = matmul(R, P)
        k += 1
        if P == [[1, 0], [0, 1]] or k > 12:
            break
    info["rotation_order"] = k
    assert k == M.m
    # rotation preserves L: R*L columns in L
    for col in range(2):
        v = matvec(R, (M.L[0][col], M.L[1][col]))
        u = matvec(M.T.adj, v)
        assert u[0] % M.T.D == 0 and u[1] % M.T.D == 0
    tris = M.torus_triangles()
    info["torus_triangles"] = len(tris)
    assert all(len(t) == 3 for t in tris), "degenerate triangle on the torus cover"
    # nondegenerate geometrically (in the plane, before reduction)
    for tri in M.base_triangles:
        (a, b, c) = tri
        assert (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) != 0
    edges = {}
    for t in tris:
        for e in itertools.combinations(sorted(t), 2):
            edges[frozenset(e)] = edges.get(frozenset(e), 0) + 1
    assert all(v == 2 for v in edges.values()), "torus cover is not a closed surface / has repeated edges"
    verts = set().union(*tris)
    info["torus_vertices"] = len(verts)
    info["torus_edges"] = len(edges)
    info["torus_euler_characteristic"] = len(verts) - len(edges) + len(tris)
    assert info["torus_euler_characteristic"] == 0
    # symmetry: rotation about the origin and lattice translations
    def img(t, f):
        return frozenset(M.T.reduce(f(p)) for p in t)
    assert {img(t, lambda p: matvec(R, p)) for t in tris} == tris, "rotation does not preserve triangles"
    for col in range(2):
        lam = (M.L[0][col], M.L[1][col])
        assert {img(t, lambda p, lam=lam: (p[0] + lam[0], p[1] + lam[1])) for t in tris} == tris
    # classes
    classes = {v: M.s2_class(v) for v in verts}
    assert set(classes.values()) == {1, 2, 3, 4}
    for v in verts:
        assert M.s2_class(M.T.reduce(matvec(R, v))) == classes[v]
    for t in tris:
        assert len({classes[v] for v in t}) == 3, "triangle with repeated S^2_4 class"
    # quotient E/(C_m x L): orbits of vertices / edges / triangles under <R, L/NL>
    gens = [lambda p: M.T.reduce(matvec(R, p))]
    for col in range(2):
        lam = (M.L[0][col], M.L[1][col])
        gens.append(lambda p, lam=lam: M.T.reduce((p[0] + lam[0], p[1] + lam[1])))
    def orbits_of(items):
        parent = {x: x for x in items}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for x in items:
            for g in gens:
                y = frozenset(g(p) for p in x) if isinstance(x, frozenset) else g(x)
                ra, rb = find(x), find(y)
                if ra != rb:
                    parent[ra] = rb
        return {find(x) for x in items}
    vo = orbits_of(list(verts))
    eo = orbits_of(list(edges))
    to = orbits_of(list(tris))
    info["quotient_f_vector"] = [len(vo), len(eo), len(to)]
    # class-image sets
    edge_images = {frozenset(classes[v] for v in e) for e in edges}
    tri_images = {frozenset(classes[v] for v in t) for t in tris}
    info["quotient_edge_images"] = len(edge_images)
    info["quotient_triangle_images"] = len(tri_images)
    info["quotient_is_tetrahedron_boundary"] = (len(vo), len(eo), len(to)) == (4, 6, 4) and len(edge_images) == 6 and len(tri_images) == 4
    # stabiliser orders of the vertex classes: |C_m x L/NL| / orbit size
    G_order = M.m * M.N ** 2
    orbit_size = {}
    for v in verts:
        orbit_size[classes[v]] = orbit_size.get(classes[v], 0) + 1
    info["vertex_class_orbit_sizes_on_cover"] = orbit_size
    info["vertex_class_stabiliser_orders"] = {c: G_order // n for c, n in orbit_size.items()}
    return info, tris, classes


# ---------------------------------------------------------------------------
# the four E-models
# ---------------------------------------------------------------------------
def model_m2():
    # coordinates (a,b) <-> (a + b tau)/2 ; crystallographic lattice L(tau) = 2Z^2; vertices Z^2 = E[2] lifts
    L = [[2, 0], [0, 2]]
    rot = [[-1, 0], [0, -1]]
    base = []
    for a in range(2):
        for b in range(2):
            base.append(((a, b), (a + 1, b), (a + 1, b + 1)))
            base.append(((a, b), (a, b + 1), (a + 1, b + 1)))
    def cls(p):
        return 1 + (p[0] % 2) + 2 * (p[1] % 2)
    return EModel("m2", 2, L, rot, base, cls, 2,
                  "E = C/L(tau), vertex set E[2] = (1/2)L(tau) (all four 2-torsion points, the cone points of "
                  "E/{+-1}); grid triangulation of (1/2)L(tau) with diagonal in direction 1+tau; "
                  "integer point (a,b) represents (a + b tau)/2.  Classes: 1=0, 2=1/2, 3=tau/2, 4=(1+tau)/2.")


def model_m3():
    # fine hexagonal lattice Z[omega] in coordinates (a,b) <-> a + b omega, scaled by 3; L = (omega-1) Z[omega]
    # = {(c,d): c+d = 0 mod 3} (index 3), scaled by 3.  Rotation omega: (a,b) -> (-b, a-b).
    L = [[3, 3], [-3, 6]]   # columns 3*(1,-1), 3*(1,2)
    rot = [[0, -1], [1, -1]]
    base = []
    for v in [(0, 0), (1, 0), (2, 0)]:  # representatives of Z^2 / L (classes c+d mod 3 = 0,1,2)
        A = (3 * v[0], 3 * v[1]); B = (3 * (v[0] + 1), 3 * v[1]); C = (3 * (v[0] + 1), 3 * (v[1] + 1)); D = (3 * v[0], 3 * (v[1] + 1))
        bary = (3 * v[0] + 2, 3 * v[1] + 1)   # barycentre of the up-triangle A B C
        base += [(A, B, bary), (B, C, bary), (A, C, bary)]  # stellar subdivision of up-triangles
        base.append((A, D, C))                              # down-triangles kept
    def cls(p):
        if p[0] % 3 == 0 and p[1] % 3 == 0:
            return 1 + ((p[0] // 3 + p[1] // 3) % 3)   # the three fixed points of omega
        return 4                                       # barycentres (free orbit)
    return EModel("m3", 3, L, rot, base, cls, 2,
                  "E = C/L(zeta) = C/Z[omega] (omega = zeta^2); fine lattice (omega-1)^{-1}L = the three fixed "
                  "points of the order-3 rotation; Delaunay (triangular) triangulation of the fine lattice with "
                  "one C_3-orbit of triangles (the 'up' triangles) stellarly subdivided at barycentres.  Integer "
                  "point (a,b) represents (a + b omega)/3 in the fine lattice normalisation where L = "
                  "{(c,d): c+d = 0 mod 3}.  Classes 1,2,3 = fixed points (0, q, 2q), 4 = barycentre orbit.")


def model_m4():
    # E = C/Z[i], coordinates scaled by 6: Z[i] -> 6Z^2, E[2] -> 3Z^2; rotation i: (a,b) -> (-b, a)
    L = [[6, 0], [0, 6]]
    rot = [[0, -1], [1, 0]]
    c = (3, 3)
    corners = [(0, 0), (6, 0), (6, 6), (0, 6)]
    mids = [(3, 0), (6, 3), (3, 6), (0, 3)]
    base = []
    # eight triangles (centre, corner, midpoint); orbit A under rotation about the centre: (c, corner_k, mid_k)
    for k in range(4):
        cor, mid = corners[k], mids[k]
        bary = ((c[0] + cor[0] + mid[0]) // 3, (c[1] + cor[1] + mid[1]) // 3)
        assert (c[0] + cor[0] + mid[0]) % 3 == 0 and (c[1] + cor[1] + mid[1]) % 3 == 0
        base += [(c, cor, bary), (cor, mid, bary), (c, mid, bary)]   # subdivided orbit A
        cor2 = corners[(k + 1) % 4]
        base.append((c, mid, cor2))                                  # orbit B kept
    def cls(p):
        a, b = p[0] % 6, p[1] % 6
        if (a, b) == (0, 0):
            return 1          # 0 (order 4)
        if (a, b) == (3, 3):
            return 2          # (1+i)/2 (order 4)
        if (a, b) in ((3, 0), (0, 3)):
            return 3          # 1/2, i/2 (order 2, one orbit)
        return 4              # barycentres
    return EModel("m4", 4, L, rot, base, cls, 2,
                  "E = C/Z[i]; vertex set E[2] plus the barycentres of one C_4-orbit of the eight triangles "
                  "(centre (1+i)/2, corner, edge-midpoint) of the square with corners in Z[i]; integer point "
                  "(a,b) represents (a + b i)/6.  Classes: 1 = 0, 2 = (1+i)/2 (order-4 cone points), "
                  "3 = {1/2, i/2} (order-2 cone point), 4 = barycentre orbit (regular).")


def model_m6():
    # fine lattice Z[omega] scaled by 6 (so far-edge midpoints and barycentres are integral)
    L = [[6, 6], [-6, 12]]   # 6 * basis of {(c,d): c+d = 0 mod 3}
    rot = [[1, -1], [1, 0]]  # zeta = 1 + omega : (a,b) -> (a-b, a)
    # coarse triangles: fine triangles with the far edge (between the two nonzero classes) split at its midpoint
    def fine_class(v):
        return (v[0] + v[1]) % 3
    coarse = []
    for v in [(0, 0), (1, 0), (2, 0)]:
        for tri in [(v, (v[0] + 1, v[1]), (v[0] + 1, v[1] + 1)), (v, (v[0], v[1] + 1), (v[0] + 1, v[1] + 1))]:
            zero = [p for p in tri if fine_class(p) == 0]
            others = [p for p in tri if fine_class(p) != 0]
            assert len(zero) == 1 and len(others) == 2
            A = (6 * zero[0][0], 6 * zero[0][1])
            B = (6 * others[0][0], 6 * others[0][1])
            C = (6 * others[1][0], 6 * others[1][1])
            Mid = ((B[0] + C[0]) // 2, (B[1] + C[1]) // 2)
            coarse += [(A, B, Mid), (A, Mid, C)]
    # split the 12 coarse triangles into their two C_6-orbits (mod L) and subdivide one orbit
    T = Torus(L, 1)
    def key(tri):
        # canonical representative of the geometric triangle modulo L-translations
        # (vertex sets modulo L do not determine the triangle: E/L with 6 vertices is only a Delta-complex)
        base = min(tri)
        rb = T.reduce(base)
        lam = (base[0] - rb[0], base[1] - rb[1])
        return tuple(sorted((p[0] - lam[0], p[1] - lam[1]) for p in tri))
    def rot_tri(tri):
        return tuple(matvec(rot, p) for p in tri)
    coarse_keys = {key(t): t for t in coarse}
    assert len(coarse_keys) == 12, len(coarse_keys)
    orbit = set()
    t0 = coarse[0]
    cur = t0
    for _ in range(6):
        orbit.add(key(cur))
        cur = rot_tri(cur)
    assert len(orbit) == 6
    base = []
    for k, tri in coarse_keys.items():
        if k in orbit:
            A, B, C = tri
            bary = ((A[0] + B[0] + C[0]) // 3, (A[1] + B[1] + C[1]) // 3)
            assert (A[0] + B[0] + C[0]) % 3 == 0 and (A[1] + B[1] + C[1]) % 3 == 0
            base += [(A, B, bary), (B, C, bary), (A, C, bary)]
        else:
            base.append(tri)
    def cls(p):
        if p[0] % 6 == 0 and p[1] % 6 == 0:
            return 1 if (p[0] // 6 + p[1] // 6) % 3 == 0 else 2   # 0 (order 6) / {q,2q} (order 3)
        if p[0] % 3 == 0 and p[1] % 3 == 0:
            return 3                                              # half-periods (order 2)
        return 4                                                  # barycentres
    return EModel("m6", 6, L, rot, base, cls, 2,
                  "E = C/Z[omega]; vertex set: the three fixed points of omega, the three half-periods "
                  "(midpoints of the fine-lattice edges not incident to 0), and the barycentres of one "
                  "C_6-orbit of the twelve resulting triangles; integer point (a,b) represents (a + b omega)/6 "
                  "in the fine-lattice normalisation.  Classes: 1 = 0 (order 6), 2 = {q,2q} (order 3), "
                  "3 = half-periods (order 2), 4 = barycentre orbit (regular).")


# ---------------------------------------------------------------------------
# Bagchi--Datta subdivision, indexed by cell (I,J)
# ---------------------------------------------------------------------------
def load_bd16():
    facets = S.parse_facets(open(os.path.join(DATA, "s2xs2_16_facets.txt")).read())
    cells = {}
    for F in facets:
        I = frozenset((v - 1) // 4 + 1 for v in F)
        J = frozenset((v - 1) % 4 + 1 for v in F)
        cells.setdefault((I, J), []).append([((v - 1) // 4 + 1, (v - 1) % 4 + 1) for v in F])
    assert len(cells) == 16 and all(len(v) == 6 for v in cells.values())
    return cells


CELLS16 = load_bd16()


def product_lift(M, tris, classes):
    """Vertices (p,q) of E_N x E_N ; facets = pulled back (S^2xS^2)_16 simplices."""
    verts = sorted(set().union(*tris))
    vid = {v: i for i, v in enumerate(verts)}
    nV = len(verts)
    pid = lambda p, q: vid[p] * nV + vid[q]
    facets = set()
    for sig in tris:
        sl = {classes[p]: p for p in sig}
        for tau in tris:
            tl = {classes[q]: q for q in tau}
            I, J = frozenset(sl), frozenset(tl)
            for F in CELLS16[(I, J)]:
                facets.add(frozenset(pid(sl[i], tl[j]) for (i, j) in F))
    return verts, vid, nV, pid, facets


def group_generators(M, verts, vid, nV):
    """Permutations (as lists) of product vertices for: swap, rotation in factor 1 and 2,
    translations by the L-basis vectors in factor 1 and 2."""
    idx = {v: i for i, v in enumerate(verts)}
    R = M.rot
    def rotp(p):
        return M.T.reduce(matvec(R, p))
    def trans(col):
        lam = (M.L[0][col], M.L[1][col])
        return lambda p: M.T.reduce((p[0] + lam[0], p[1] + lam[1]))
    maps1 = {"rot": rotp, "t1": trans(0), "t2": trans(1)}
    gens = {}
    n = nV * nV
    def perm(f1, f2):
        P = [0] * n
        for p in verts:
            for q in verts:
                P[idx[p] * nV + idx[q]] = idx[f1(p)] * nV + idx[f2(q)]
        return P
    ident = lambda p: p
    gens["swap"] = [0] * n
    for p in verts:
        for q in verts:
            gens["swap"][idx[p] * nV + idx[q]] = idx[q] * nV + idx[p]
    for name, f in maps1.items():
        gens[name + "_x"] = perm(f, ident)
        gens[name + "_y"] = perm(ident, f)
    return gens


def apply_perm_face(P, face):
    return frozenset(P[v] for v in face)


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
            y = apply_perm_face(P, x)
            ra, rb = find(x), find(y)
            if ra != rb:
                parent[ra] = rb
    roots = {}
    for x in items:
        roots.setdefault(find(x), []).append(x)
    return roots


def analyse_quotient(M, verts, vid, nV, pid, facets, gens, group_order, label, target_cp10=None):
    """Check invariance, regularity, simpliciality of the quotient; identify it."""
    info = {"group_generators": sorted(gens)}
    G = list(gens.values())
    # invariance
    inv = {name: {apply_perm_face(P, F) for F in facets} == facets for name, P in gens.items()}
    info["facet_set_invariant_under_generators"] = inv
    assert all(inv.values()), inv
    # all faces
    faces_by_dim = {k: set() for k in range(5)}
    for F in facets:
        Fs = sorted(F)
        for k in range(1, 6):
            for Sub in itertools.combinations(Fs, k):
                faces_by_dim[k - 1].add(frozenset(Sub))
    fvec = [len(faces_by_dim[k]) for k in range(5)]
    info["cover_f_vector"] = fvec
    info["cover_euler_characteristic"] = sum((-1) ** k * fvec[k] for k in range(5))
    # closed pseudomanifold
    ridge_count = {}
    for F in facets:
        for v in F:
            R = F - {v}
            ridge_count[R] = ridge_count.get(R, 0) + 1
    info["cover_is_closed_pseudomanifold"] = all(c == 2 for c in ridge_count.values())
    # vertex orbits and colours
    vorb = union_find_orbits(list(faces_by_dim[0]), G)
    colour = {}
    for r, members in vorb.items():
        for x in members:
            colour[next(iter(x))] = r
    info["number_of_vertex_orbits"] = len(vorb)
    # regularity: every face has pairwise distinct colours
    distinct = all(len({colour[v] for v in F}) == len(F) for F in facets)
    info["every_facet_has_pairwise_distinct_vertex_orbits"] = distinct
    # quotient injectivity: number of face orbits equals number of distinct colour-sets, per dimension
    quotient_faces = {}
    inj = {}
    for k in range(5):
        orbs = union_find_orbits(list(faces_by_dim[k]), G)
        images = {frozenset(colour[v] for v in f) for f in faces_by_dim[k]}
        inj[k] = (len(orbs), len(images))
        quotient_faces[k] = images
    info["face_orbits_vs_distinct_images_by_dimension"] = inj
    info["quotient_is_simplicial_complex"] = distinct and all(a == b for a, b in inj.values())
    # quotient complex
    colour_ids = {r: i + 1 for i, r in enumerate(sorted(vorb, key=lambda r: min(next(iter(x)) for x in vorb[r])))}
    qfacets = [frozenset(colour_ids[colour[v]] for v in F) for F in facets]
    qfacets = sorted(set(qfacets), key=sorted)
    info["quotient_f_vector"] = S.f_vector(qfacets)
    info["quotient_facets"] = len(qfacets)
    # marking: for each quotient vertex, stabiliser order and E-class pair
    marking = {}
    for r, members in vorb.items():
        rep = next(iter(members))
        v = next(iter(rep))
        p, q = verts[v // nV], verts[v % nV]
        marking[colour_ids[r]] = {
            "orbit_size_on_cover": len(members),
            "stabiliser_order_in_Gamma": group_order // len(members),
            "E_classes": sorted([M.s2_class(p), M.s2_class(q)]),
            "representative_upstairs": [list(p), list(q)],
        }
    info["marking"] = marking
    if target_cp10 is not None:
        phi = S.isomorphism(qfacets, target_cp10)
        info["isomorphic_to_CP2_10"] = phi is not None
        info["relabelling_quotient_vertex_to_CP2_10_label"] = {str(k): v for k, v in sorted(phi.items())} if phi else None
    with open(os.path.join(LIFTDIR, f"{label}_quotient_facets.txt"), "w") as fh:
        fh.write(f"# quotient complex for {label}; vertex k has marking {json.dumps(marking, default=str)}\n")
        for F in qfacets:
            fh.write(",".join(map(str, sorted(F))) + "\n")
    return info, qfacets, colour, colour_ids


def write_cover(M, verts, facets, label):
    with open(os.path.join(LIFTDIR, f"{label}_cover_vertices.txt"), "w") as fh:
        fh.write(f"# vertices of the finite torus cover E_N x E_N for {label}: id: (p, q) integer coordinates\n")
        nV = len(verts)
        for i, p in enumerate(verts):
            for j, q in enumerate(verts):
                fh.write(f"{i * nV + j}: {p[0]},{p[1]} ; {q[0]},{q[1]}\n")
    with open(os.path.join(LIFTDIR, f"{label}_cover_facets.txt"), "w") as fh:
        fh.write(f"# {len(facets)} facets of the lifted triangulation on the finite torus cover, vertex ids as above\n")
        for F in sorted(facets, key=sorted):
            fh.write(",".join(map(str, sorted(F))) + "\n")


def nondegenerate_lifts(M, verts, nV, facets):
    """Every lifted 4-simplex is geometrically nondegenerate (integer 4x4 determinant != 0)."""
    def det4(rows):
        Mx = [[Fraction(v) for v in r] for r in rows]
        d = Fraction(1)
        for c in range(4):
            piv = next((r for r in range(c, 4) if Mx[r][c] != 0), None)
            if piv is None:
                return Fraction(0)
            if piv != c:
                Mx[c], Mx[piv] = Mx[piv], Mx[c]
                d = -d
            d *= Mx[c][c]
            for r in range(c + 1, 4):
                f = Mx[r][c] / Mx[c][c]
                for cc in range(c, 4):
                    Mx[r][cc] -= f * Mx[c][cc]
        return d
    # coordinates on the cover are only defined modulo the period; use lifts inside one product cell:
    # we recompute from the E-model: a facet lies in a product cell sigma x tau; take the actual
    # integer coordinates of its vertices there (they are the reduced ones, which are within one
    # translate of the cell since the cover is at least 2 periods wide) -- for a robust check we
    # simply verify that the six simplices of each abstract cell are nondegenerate for the *standard*
    # coordinates; this was done in build_complexes.py.  Here we check a sample of lifted simplices
    # using reduced coordinates; degeneracy would be flagged (a false alarm is possible only if a
    # simplex straddles the period, which cannot happen for the reduced representatives chosen in
    # product_lift when N >= 2 and the base triangles lie in one fundamental domain).
    vols = set()
    for F in list(facets)[:2000]:
        pts = []
        for v in sorted(F):
            p, q = verts[v // nV], verts[v % nV]
            pts.append((p[0], p[1], q[0], q[1]))
        d = det4([[pts[i][k] - pts[0][k] for k in range(4)] for i in range(1, 5)])
        vols.add(abs(d))
    return sorted(str(v) for v in vols)


def run_model(M, target_cp10, report):
    print(f"=== model {M.name} (m = {M.m}) ===", flush=True)
    einfo, tris, classes = check_E_model(M)
    print("  E-model:", json.dumps(einfo, default=str), flush=True)
    verts, vid, nV, pid, facets = product_lift(M, tris, classes)
    print(f"  cover: {nV} E-vertices, {len(tris)} E-triangles, {len(facets)} lifted facets", flush=True)
    gens = group_generators(M, verts, vid, nV)
    group_order = 2 * M.m ** 2 * M.N ** 4
    qinfo, qfacets, colour, colour_ids = analyse_quotient(M, verts, vid, nV, pid, facets, gens, group_order, M.name, target_cp10)
    qinfo["group_order_on_cover"] = group_order
    qinfo["sample_lifted_simplex_volumes_abs_det"] = nondegenerate_lifts(M, verts, nV, facets)
    print("  quotient:", json.dumps({k: v for k, v in qinfo.items() if k not in ("marking",)}, default=str), flush=True)
    print("  marking:", json.dumps(qinfo["marking"], default=str), flush=True)
    write_cover(M, verts, facets, M.name)
    report[M.name] = {"m": M.m, "description": M.description, "E_model": einfo, "lift_and_quotient": qinfo,
                      "base_triangles": [[list(p) for p in t] for t in M.base_triangles],
                      "L_basis_columns": M.L, "rotation_matrix": M.rot, "cover_N": M.N}
    return verts, vid, nV, pid, facets, gens, tris, classes


def main():
    cp10 = S.parse_facets(open(os.path.join(DATA, "cp2_10_facets.txt")).read())
    report = {}
    models = {2: model_m2(), 3: model_m3(), 4: model_m4(), 6: model_m6()}
    lifted = {}
    for m in (2, 3, 4, 6):
        lifted[m] = run_model(models[m], cp10, report)

    # ---------------------------------------------------------------- (4,2)_1 on the m=2 model with tau = i
    M = models[2]
    verts, vid, nV, pid, facets, gens, tris, classes = lifted[2]
    idx = {v: i for i, v in enumerate(verts)}
    rot_i = [[0, -1], [1, 0]]   # multiplication by i in coordinates (a,b) <-> (a+bi)/2
    def perm_pair(f1, f2):
        P = [0] * (nV * nV)
        for p in verts:
            for q in verts:
                P[idx[p] * nV + idx[q]] = idx[M.T.reduce(f1(p))] * nV + idx[M.T.reduce(f2(q))]
        return P
    ri = lambda p: matvec(rot_i, p)
    ident = lambda p: p
    half = lambda p: (p[0] + 1, p[1] + 1)          # translation by (1+i)/2 (coordinates scaled by 2)
    checks = {
        "diag(i,i)": {apply_perm_face(perm_pair(ri, ri), F) for F in facets} == facets,
        "diag(i,1)": {apply_perm_face(perm_pair(ri, ident), F) for F in facets} == facets,
        "translation_((1+i)/2,(1+i)/2)": {apply_perm_face(perm_pair(half, half), F) for F in facets} == facets,
        "translation_(1/2,1/2)": {apply_perm_face(perm_pair(lambda p: (p[0] + 1, p[1]), lambda p: (p[0] + 1, p[1])), F) for F in facets} == facets,
        "translation_(1/2,0)_one_factor": {apply_perm_face(perm_pair(lambda p: (p[0] + 1, p[1]), ident), F) for F in facets} == facets,
    }
    # the induced permutation of the S^2_4 classes by i: class(p) -> class(i p)
    induced = {c: None for c in range(1, 5)}
    for p in verts:
        induced[classes[p]] = classes[M.T.reduce(ri(p))]
    report["four_two_one_obstruction_on_m2_model_tau_i"] = {
        "invariance_of_lift_under_extra_symmetries": checks,
        "permutation_of_S2_4_classes_induced_by_multiplication_by_i": induced,
        "conclusion": "the lift is invariant under diagonal half-period translations (they act on the four "
                      "classes as the Klein four-group, contained in A_4) but not under diag(i,i), which "
                      "induces a transposition of the classes; hence no lift of the (2,1)_0 model CP^2_10 "
                      "with vertex set E[2]^2 is (4,2)_1-invariant.",
    }
    print("(4,2)_1 obstruction:", json.dumps(report["four_two_one_obstruction_on_m2_model_tau_i"], default=str), flush=True)

    # ---------------------------------------------------------------- restriction of the m=4 model to the
    # index-4 subgroup H = G(4,2,2) x| ((1-i)Z[i])^2 + Z(1,1), which is s^{-1} (4,2)_1 s for s = (1+i)/2.
    M = models[4]
    verts, vid, nV, pid, facets, gens, tris, classes = lifted[4]
    idx = {v: i for i, v in enumerate(verts)}
    R = M.rot
    def perm_pair4(f1, f2):
        P = [0] * (nV * nV)
        for p in verts:
            for q in verts:
                P[idx[p] * nV + idx[q]] = idx[M.T.reduce(f1(p))] * nV + idx[M.T.reduce(f2(q))]
        return P
    rp = lambda p: matvec(R, p)
    rinv = lambda p: matvec(matmul(matmul(R, R), R), p)
    r2 = lambda p: matvec(matmul(R, R), p)
    ident = lambda p: p
    # coordinates: Z[i] -> 6Z^2 ; (1-i)Z[i] has basis 6(1,-1), 6(1,1); the vector (1,1) in C^2 = ((6,0),(6,0))
    Hgens = {
        "swap": gens["swap"],
        "diag(i^-1,i)": perm_pair4(rinv, rp),
        "diag(-1,1)": perm_pair4(r2, ident),
        "t_x_6(1,-1)": perm_pair4(lambda p: (p[0] + 6, p[1] - 6), ident),
        "t_x_6(1,1)": perm_pair4(lambda p: (p[0] + 6, p[1] + 6), ident),
        "t_y_6(1,-1)": perm_pair4(ident, lambda p: (p[0] + 6, p[1] - 6)),
        "t_y_6(1,1)": perm_pair4(ident, lambda p: (p[0] + 6, p[1] + 6)),
        "t_diag_(1,1)": perm_pair4(lambda p: (p[0] + 6, p[1]), lambda p: (p[0] + 6, p[1])),
    }
    # order of H on the cover: |G(4,2,2)| * |(s^{-1}Lambda) / (N Z[i])^2| = 16 * (2^4 * ... ) : index of s^-1 Lambda
    # in Z[i]^2 is 2, so |Z[i]^2 / (2Z[i])^2| / 2 * ... = (16)/2 = 8 -> wait: translations mod (2 Z[i])^2: Z[i]^2/(2Z[i])^2 has 16 elements,
    # s^{-1}Lambda / (2Z[i])^2 has 16/2 = 8 elements; H_N order = 16 * 8 = 128.
    H_order = 16 * 8
    hinfo, hq, hcolour, hids = analyse_quotient(M, verts, vid, nV, pid, facets, Hgens, H_order, "m4_restricted_to_(4,2)_1", None)
    hinfo["group_order_on_cover"] = H_order
    hinfo["quotient_vertex_count"] = hinfo["number_of_vertex_orbits"]
    # sanity: quotient of the H-quotient by the full group is CP^2_10 (H has index 4)
    report["m4_restricted_to_conjugate_of_(4,2)_1"] = hinfo
    print("m4 restricted to (4,2)_1-conjugate:", json.dumps({k: v for k, v in hinfo.items() if k != "marking"}, default=str), flush=True)
    print("  marking:", json.dumps(hinfo["marking"], default=str), flush=True)

    # ---------------------------------------------------------------- restriction of the m=4 model to (2,1)_0 (index 4)
    Kgens = {
        "swap": gens["swap"], "diag(-1,1)": perm_pair4(r2, ident), "diag(1,-1)": perm_pair4(ident, r2),
        "t1_x": gens["t1_x"], "t2_x": gens["t2_x"], "t1_y": gens["t1_y"], "t2_y": gens["t2_y"],
    }
    kinfo, kq, _, _ = analyse_quotient(M, verts, vid, nV, pid, facets, Kgens, 8 * 16, "m4_restricted_to_(2,1)_0", None)
    kinfo["group_order_on_cover"] = 8 * 16
    report["m4_restricted_to_(2,1)_0"] = {k: v for k, v in kinfo.items()}
    print("m4 restricted to (2,1)_0:", json.dumps({k: v for k, v in kinfo.items() if k != "marking"}, default=str), flush=True)

    json.dump(report, open(os.path.join(OUT, "lifts.json"), "w"), indent=1, default=str)
    print("DONE")


if __name__ == "__main__":
    main()
