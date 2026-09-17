#!/usr/bin/env python3
"""sgcy3.py — the single shared exact implementation used by every check of this audit.

Sections
  1. exact linear algebra over Z and Q (Smith normal form with transforms, integer kernels,
     lattice bases, determinants, inverses) — Python integers and fractions only;
  2. crystallographic input: the two databases (spglib Hall-symbol database, GAP Cryst/CrystCat)
     are read, converted to ONE convention (column vectors, x -> R x + t, conventional ITA
     basis), the full translation lattice Λ (conventional cell + centring vectors) and a
     primitive Z-basis of Λ are computed, the point group is expressed by integer matrices in
     that basis, the two databases are cross-checked coset by coset, and the symmorphic cases are
     certified (all translation parts lie in Λ at the ITA origin);
  3. finite matrix groups: closure, conjugacy classes, centralisers, isomorphisms between two
     small groups, explicit GL(3,Z)-conjugators (certificates of Z-equivalence);
  4. orbifold Hodge numbers (Chen–Ruan / Batyrev) of A_τ/G for the linear action ρ ⊕ ρ on
     L = Λ ⊕ τΛ: fixed-locus components, centraliser orbits, stabiliser characters, age shifts,
     untwisted sector by characters; the DHVW orbifold Euler number as an independent check;
     the invariants |Λ/S_Λ| (fundamental group of A_τ/G, see REPORT.md) and the axis index.

Conventions.  Matrices are lists of rows.  A 3×3 matrix M acts on column vectors, v -> M v.
An affine operation is a pair (M, t) acting by x -> M x + t.  The GAP/Cryst database stores
right actions on row vectors ((x,1) -> (x,1)·[[A,0],[t,1]]); its linear part is converted by
transposition, M = A^T (this conversion is verified against spglib in `crosscheck_databases`).
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction as Fr
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ALL35 = [16, 17, 21, 22, 24, 89, 90, 91, 93, 95, 97, 98, 149, 150, 151, 153, 155,
         177, 178, 179, 180, 181, 182, 195, 196, 198, 199, 207, 208, 209, 210, 211, 212, 213, 214]
LINEAR14 = [16, 21, 22, 89, 97, 149, 150, 155, 177, 195, 196, 207, 209, 211]

# --------------------------------------------------------------------------------------
# 1. exact linear algebra
# --------------------------------------------------------------------------------------

def ident(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def mv(A, v):
    return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]

def transpose(A):
    return [list(r) for r in zip(*A)]

def msub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def det(A):
    """Exact determinant (Fraction arithmetic); returns int when integral."""
    n = len(A)
    M = [[Fr(x) for x in row] for row in A]
    d = Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return int(d) if d.denominator == 1 else d

def inv(A):
    """Exact inverse (Fractions); entries converted to int when integral."""
    n = len(A)
    M = [[Fr(x) for x in row] + [Fr(1 if i == j else 0) for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    R = [row[n:] for row in M]
    return [[int(x) if x.denominator == 1 else x for x in row] for row in R]

def is_integral(A):
    return all(Fr(x).denominator == 1 for row in A for x in row)

def as_int(A):
    return [[int(Fr(x)) for x in row] for row in A]

def snf(M):
    """Smith normal form with transforms: returns (D, U, V) with U*M*V == D, U, V unimodular,
    D diagonal with non-negative entries d_1 | d_2 | ... (same shape as M)."""
    m, n = len(M), len(M[0])
    A = [[int(x) for x in row] for row in M]
    U, V = ident(m), ident(n)

    def swap_rows(i, j):
        A[i], A[j] = A[j], A[i]; U[i], U[j] = U[j], U[i]

    def swap_cols(i, j):
        for row in A: row[i], row[j] = row[j], row[i]
        for row in V: row[i], row[j] = row[j], row[i]

    def add_row(i, j, c):  # row_i += c*row_j
        A[i] = [a + c * b for a, b in zip(A[i], A[j])]; U[i] = [a + c * b for a, b in zip(U[i], U[j])]

    def add_col(i, j, c):  # col_i += c*col_j
        for row in A: row[i] += c * row[j]
        for row in V: row[i] += c * row[j]

    t = 0
    while t < min(m, n):
        best = None
        for i in range(t, m):
            for j in range(t, n):
                if A[i][j] != 0 and (best is None or abs(A[i][j]) < abs(A[best[0]][best[1]])):
                    best = (i, j)
        if best is None:
            break
        swap_rows(t, best[0]); swap_cols(t, best[1])
        while True:
            done = True
            for i in range(t + 1, m):
                if A[i][t] != 0:
                    add_row(i, t, -(A[i][t] // A[t][t]))
                    if A[i][t] != 0:
                        swap_rows(i, t); done = False
            for j in range(t + 1, n):
                if A[t][j] != 0:
                    add_col(j, t, -(A[t][j] // A[t][t]))
                    if A[t][j] != 0:
                        swap_cols(j, t); done = False
            if not done:
                continue
            bad = next(((i, j) for i in range(t + 1, m) for j in range(t + 1, n) if A[i][j] % A[t][t] != 0), None)
            if bad is None:
                break
            add_row(t, bad[0], 1)
        if A[t][t] < 0:
            A[t] = [-a for a in A[t]]; U[t] = [-a for a in U[t]]
        t += 1
    assert mm(mm(U, M), V) == A, "SNF transform check failed"
    assert abs(det(U)) == 1 and abs(det(V)) == 1
    return A, U, V

def invariant_factors(M):
    D, _, _ = snf(M)
    return [D[i][i] for i in range(min(len(M), len(M[0]))) if D[i][i] != 0]

def kernel_Z(M):
    """Z-basis of {v in Z^n : M v = 0} (list of column vectors)."""
    D, U, V = snf(M)
    m, n = len(M), len(M[0])
    r = sum(1 for i in range(min(m, n)) if D[i][i] != 0)
    ker = [[V[i][j] for i in range(n)] for j in range(r, n)]
    for v in ker:
        assert all(x == 0 for x in mv(M, v))
    return ker

def saturation_basis(M):
    """Z-basis of the saturation {ℓ in Z^m : Nℓ in M Z^n for some N>0} of the column span of M."""
    D, U, V = snf(M)
    m, n = len(M), len(M[0])
    r = sum(1 for i in range(min(m, n)) if D[i][i] != 0)
    Uinv = as_int(inv(U))
    return [[Uinv[i][j] for i in range(m)] for j in range(r)]

def index_of_span(vectors, dim):
    """Index in Z^dim of the Z-span of integer vectors (None if the span has lower rank)."""
    M = [[v[i] for v in vectors] for i in range(dim)]
    f = invariant_factors(M)
    if len(f) < dim:
        return None
    p = 1
    for x in f: p *= x
    return p

def lcm(a, b):
    return a * b // gcd(a, b)

def lattice_basis(vectors):
    """Z-basis (list of rational column vectors) of the Z-span of rational vectors in Q^d."""
    d = len(vectors[0])
    den = 1
    for v in vectors:
        for x in v:
            den = lcm(den, Fr(x).denominator)
    G = [[int(Fr(v[i]) * den) for v in vectors] for i in range(d)]
    D, U, V = snf(G)
    r = sum(1 for i in range(min(d, len(vectors))) if D[i][i] != 0)
    Uinv = as_int(inv(U))
    basis = [[Fr(D[i][i] * Uinv[row][i], den) for row in range(d)] for i in range(r)]
    # every generator must be an integral combination of the basis
    B = [[basis[j][i] for j in range(r)] for i in range(d)]
    if r == d:
        Binv = inv(B)
        for v in vectors:
            assert is_integral([mv(Binv, [Fr(x) for x in v])]), "lattice basis check failed"
    return basis

def frac_mod1(x):
    x = Fr(x)
    return x - (x.numerator // x.denominator)

def vec_mod1(v):
    return tuple(frac_mod1(x) for x in v)

# --------------------------------------------------------------------------------------
# 2. crystallographic input
# --------------------------------------------------------------------------------------

def load_spglib():
    d = json.loads((DATA / "spglib_operations.json").read_text())
    out = {}
    for g in d["groups"]:
        ops = [([list(map(int, r)) for r in op["R"]], [Fr(x) for x in op["t"]]) for op in g["operations"]]
        key = (g["number"], g["choice"])
        out[key] = {"meta": {k: g[k] for k in ("number", "hall_number", "hall_symbol", "choice",
                                                 "international_full", "international_short")},
                    "ops": ops}
    return d["spglib_version"], out

def load_crystcat():
    d = json.loads((DATA / "crystcat_generators.json").read_text())
    out = {}
    for g in d["groups"]:
        gens = []
        for M4 in g["generators"]:
            A = [[Fr(M4[i][j]) for j in range(3)] for i in range(3)]
            t = [Fr(M4[3][j]) for j in range(3)]
            gens.append((as_int(transpose(A)), t))  # right action on rows  ->  column convention
        out[g["number"]] = {"meta": {k: g[k] for k in ("number", "settings", "point_group_order", "is_symmorphic_crystcat")},
                            "gens": gens}
    return {k: d[k] for k in ("gap_version", "cryst_version", "crystcat_version")}, out

def conventional_lattice(ops):
    """Centring vectors (t mod 1 with R = 1) and a primitive basis B of Λ = Z^3 + centrings.
    Returns (centrings, B) with B a 3×3 rational matrix whose COLUMNS are the basis vectors in
    conventional coordinates."""
    centrings = sorted({vec_mod1(t) for R, t in ops if R == ident(3)})
    gens = [[Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(1)]] + [list(c) for c in centrings]
    basis = lattice_basis(gens)
    assert len(basis) == 3
    B = [[basis[j][i] for j in range(3)] for i in range(3)]
    assert Fr(det(B)) == Fr(1, len(centrings)), (det(B), len(centrings))
    return centrings, B

def to_primitive(ops, B):
    """Convert operations (R, t) in conventional coordinates to (M, s) in the primitive basis B
    (M integral, s reduced mod Z^3) and collapse coset duplicates."""
    Binv = inv(B)
    cosets = {}
    for R, t in ops:
        M = mm(mm(Binv, R), B)
        assert is_integral(M), "point-group matrix not integral in the primitive basis"
        M = as_int(M)
        s = vec_mod1(mv(Binv, t))
        key = tuple(map(tuple, M))
        if key in cosets:
            assert cosets[key] == s, "two different translation parts for one rotation part modulo Λ"
        else:
            cosets[key] = s
    return cosets  # dict: M (tuple of tuples) -> s (tuple of Fractions mod 1)

def closure_cosets(gens):
    """Closure of affine cosets (M, s mod 1) under composition; gens = list of (M, s)."""
    def compose(a, b):  # a∘b : x -> Ma(Mb x + sb) + sa
        Ma, sa = a; Mb, sb = b
        M = mm(Ma, Mb)
        s = vec_mod1([sum(Fr(Ma[i][k]) * sb[k] for k in range(3)) + sa[i] for i in range(3)])
        return (tuple(map(tuple, M)), s)
    start = (tuple(map(tuple, ident(3))), (Fr(0),) * 3)
    seen = {start}
    frontier = [start]
    gens = [(tuple(map(tuple, M)), vec_mod1(s)) for M, s in gens]
    while frontier:
        new = []
        for a in frontier:
            for g in gens:
                c = compose(a, g)
                if c not in seen:
                    seen.add(c); new.append(c)
        frontier = new
        assert len(seen) <= 1000
    return {M: s for M, s in seen}

def point_group_matrices(cosets):
    return [ [list(r) for r in M] for M in cosets ]

def is_symmorphic_at_origin(cosets):
    return all(all(x == 0 for x in s) for s in cosets.values())

# --------------------------------------------------------------------------------------
# 3. finite matrix groups
# --------------------------------------------------------------------------------------

def key(M):
    return tuple(map(tuple, M))

def unkey(k):
    return [list(r) for r in k]

def group_closure(gens):
    e = key(ident(len(gens[0])))
    seen = {e}
    frontier = [e]
    while frontier:
        new = []
        for a in frontier:
            for g in gens:
                c = key(mm(unkey(a), g))
                if c not in seen:
                    seen.add(c); new.append(c)
        frontier = new
        assert len(seen) <= 5000
    return [unkey(k) for k in sorted(seen)]

def order(M):
    n = len(M)
    P = M
    for k in range(1, 100):
        if P == ident(n):
            return k
        P = mm(P, M)
    raise ValueError("not of finite order")

def inverse_in_group(M):
    P = ident(len(M))
    for _ in range(order(M) - 1):
        P = mm(P, M)
    return P

def conjugacy_classes(G):
    keys = {key(g): g for g in G}
    invs = {key(g): inverse_in_group(g) for g in G}
    seen = set(); classes = []
    for g in G:
        if key(g) in seen:
            continue
        cl = sorted({key(mm(mm(h, g), invs[key(h)])) for h in G})
        seen.update(cl); classes.append([unkey(c) for c in cl])
    return classes

def centralizer(G, g):
    return [h for h in G if mm(h, g) == mm(g, h)]

def isomorphisms(G1, gens1, G2):
    """All isomorphisms G1 -> G2, given as dicts key(x) -> key(phi(x)); G1 = <gens1>."""
    e1 = key(ident(3)); e2 = key(ident(3))
    # words / Cayley graph of G1
    words = {e1: []}
    frontier = [e1]
    while frontier:
        new = []
        for a in frontier:
            for i, g in enumerate(gens1):
                c = key(mm(unkey(a), g))
                if c not in words:
                    words[c] = words[a] + [i]; new.append(c)
        frontier = new
    assert len(words) == len(G1)
    orders1 = [order(g) for g in gens1]
    cands = [[h for h in G2 if order(h) == o] for o in orders1]
    G2keys = {key(h) for h in G2}
    for images in itertools.product(*cands):
        phi = {e1: e2}
        ok = True
        frontier = [e1]
        while frontier and ok:
            new = []
            for a in frontier:
                for i, g in enumerate(gens1):
                    c = key(mm(unkey(a), g))
                    img = key(mm(unkey(phi[a]), images[i]))
                    if c in phi:
                        if phi[c] != img:
                            ok = False; break
                    else:
                        phi[c] = img; new.append(c)
                if not ok:
                    break
            frontier = new
        if ok and len(set(phi.values())) == len(G1) and set(phi.values()) == G2keys:
            yield phi

def intertwiner_kernel(pairs):
    """Z-basis of {P in M_3(Z) : P a = a' P for all (a, a') in pairs}; P flattened row-major."""
    rows = []
    for a, a2 in pairs:
        for i in range(3):
            for j in range(3):
                row = [0] * 9
                for c in range(3):
                    row[3 * i + c] += a[c][j]      # (P a)_{ij} = sum_c P_{ic} a_{cj}
                    row[3 * c + j] -= a2[i][c]     # (a' P)_{ij} = sum_c a'_{ic} P_{cj}
                rows.append(row)
    return kernel_Z(rows)

def find_conjugator(G1, gens1, G2, box=4):
    """Search P in GL(3,Z) with P G1 P^{-1} = G2 (as sets), returning (P, phi, kernel_rank) or None.
    For each isomorphism phi the intertwiner module is computed exactly; a unimodular element is
    searched in the box [-box, box]^rank (exact when rank <= 1)."""
    G2keys = {key(h) for h in G2}
    best_rank = 0
    for phi in isomorphisms(G1, gens1, G2):
        pairs = [(g, unkey(phi[key(g)])) for g in gens1]
        ker = intertwiner_kernel(pairs)
        best_rank = max(best_rank, len(ker))
        if not ker:
            continue
        rng = range(-box, box + 1)
        for coeffs in itertools.product(rng, repeat=len(ker)):
            if all(c == 0 for c in coeffs):
                continue
            flat = [sum(c * v[i] for c, v in zip(coeffs, ker)) for i in range(9)]
            P = [flat[0:3], flat[3:6], flat[6:9]]
            if abs(det(P)) != 1:
                continue
            Pinv = as_int(inv(P))
            conj = {key(mm(mm(P, g), Pinv)) for g in G1}
            if conj == G2keys and all(key(mm(mm(P, g), Pinv)) == phi[key(g)] for g in G1):
                return P, phi, len(ker)
    return None if best_rank == 0 else ("no unimodular intertwiner found", best_rank)

# --------------------------------------------------------------------------------------
# 4. orbifold Hodge numbers of A_τ/G (linear action)
# --------------------------------------------------------------------------------------

def blockdiag2(M):
    n = len(M)
    Z = [[0] * n for _ in range(n)]
    return [row + zrow for row, zrow in zip(M, Z)] + [zrow + row for zrow, row in zip(Z, M)]

def character_data(G):
    n = len(G)
    chars = []
    for g in G:
        t1 = sum(g[i][i] for i in range(3))
        g2 = mm(g, g)
        t2 = (t1 * t1 - sum(g2[i][i] for i in range(3))) // 2   # trace of Λ^2 g
        chars.append((1, t1, t2, det(g)))
    return chars

def untwisted_hodge(G):
    """h^{p,q}(A)^G = dim (Λ^p ρ ⊗ Λ^q ρ̄)^G for the real representation ρ (ρ̄ = ρ)."""
    chars = character_data(G)
    n = len(G)
    H = [[Fr(0)] * 4 for _ in range(4)]
    for p in range(4):
        for q in range(4):
            H[p][q] = Fr(sum(c[p] * c[q] for c in chars), n)
            assert H[p][q].denominator == 1
    return [[int(x) for x in row] for row in H]

def orbifold_hodge(G):
    """Chen–Ruan / Batyrev orbifold Hodge numbers of [A_τ/G] for A_τ = C^3/(Λ + τΛ), G acting
    through the integer matrices G (a group, closed under multiplication) on Λ = Z^3 and by the
    same matrices, complex-linearly, on C^3.  Returns a dict with full per-class details."""
    n = len(G)
    assert all(det(g) == 1 for g in G), "the point group must lie in SL(3,Z)"
    Gk = {key(g) for g in G}
    for g in G:
        for h in G:
            assert key(mm(g, h)) in Gk
    H = untwisted_hodge(G)
    h11, h21 = H[1][1], H[2][1]
    twisted = []
    I3 = ident(3); I6 = ident(6)
    sat_gens = []   # generators of S_Λ = Σ_g sat((g-1)Λ)
    axes = []
    for cl in conjugacy_classes(G):
        g = cl[0]
        if g == I3:
            continue
        # age: eigenvalues of a non-trivial rotation are 1, e^{iθ}, e^{-iθ} -> age 1
        ordg = order(g)
        M3 = msub(g, I3)
        axis = kernel_Z(M3)
        assert len(axis) == 1, "fixed line of a non-trivial element must be one-dimensional"
        a = axis[0]
        M6 = msub(blockdiag2(g), I6)
        D, U, V = snf(M6)
        r = sum(1 for i in range(6) if D[i][i] != 0)
        assert r == 4
        dvec = [D[i][i] for i in range(r)]
        Vinv = as_int(inv(V))
        ncomp = 1
        for x in dvec: ncomp *= x
        C = centralizer(G, g)
        # character of the centraliser on the fixed line
        chi = {}
        for h in C:
            ha = mv(h, a)
            if ha == a: chi[key(h)] = 1
            elif ha == [-x for x in a]: chi[key(h)] = -1
            else: raise AssertionError("centraliser element does not preserve the axis")
        # components labelled by (k_1,...,k_r) in ⊕ Z/d_i ; representative x = V (k_i/d_i, 0, 0)
        def label_of_point(x):
            y = mv(Vinv, x)
            lab = []
            for i in range(r):
                yi = Fr(y[i])
                assert (yi * dvec[i]).denominator == 1
                lab.append(int(frac_mod1(yi) * dvec[i]))
            return tuple(lab)
        def point_of_label(lab):
            y = [Fr(lab[i], dvec[i]) for i in range(r)] + [Fr(0)] * (6 - r)
            return mv(V, y)
        labels = list(itertools.product(*[range(d) for d in dvec]))
        assert len(labels) == ncomp
        # sanity: representatives are fixed points and labels are consistent
        for lab in labels:
            x = point_of_label(lab)
            assert all(Fr(v).denominator == 1 for v in mv(M6, x))
            assert label_of_point(x) == lab
        parent = {lab: lab for lab in labels}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]; u = parent[u]
            return u
        action = {}
        for h in C:
            h6 = blockdiag2(h)
            for lab in labels:
                lab2 = label_of_point(mv(h6, point_of_label(lab)))
                action[(key(h), lab)] = lab2
                ru, rv = find(lab), find(lab2)
                if ru != rv:
                    parent[ru] = rv
        orbits = {}
        for lab in labels:
            orbits.setdefault(find(lab), []).append(lab)
        orbit_info = []
        n_orb = 0; n_E = 0
        for rep, members in orbits.items():
            stab = [h for h in C if action[(key(h), rep)] == rep]
            assert len(stab) * len(members) == len(C)
            E_type = all(chi[key(h)] == 1 for h in stab)
            n_orb += 1; n_E += 1 if E_type else 0
            orbit_info.append({"size": len(members), "stabiliser_order": len(stab),
                               "stabiliser_acts_on_curve_by_translations_only": E_type,
                               "quotient_curve": "elliptic" if E_type else "P1"})
        twisted.append({"generator": g, "order": ordg, "class_size": len(cl), "centraliser_order": len(C),
                        "age": 1, "axis": a, "invariant_factors_of_(g-1)_on_L": dvec,
                        "components": ncomp, "centraliser_orbits": n_orb,
                        "orbits_with_elliptic_quotient": n_E, "orbit_details": orbit_info,
                        "contribution_h11": n_orb, "contribution_h21": n_E})
        h11 += n_orb; h21 += n_E
    # DHVW orbifold Euler number (independent of the component/orbit bookkeeping)
    e_sum = 0
    for g in G:
        for h in G:
            if mm(g, h) != mm(h, g):
                continue
            Hsub = group_closure([g, h])
            stacked = [row for k in Hsub for row in msub(k, I3)]
            if len(kernel_Z(stacked)) > 0:      # common fixed line -> Euler number 0
                continue
            f = invariant_factors(stacked)
            assert len(f) == 3
            cnt = 1
            for x in f: cnt *= x
            e_sum += cnt * cnt                   # fixed points on L = Λ ⊕ Λ : (count on Λ)^2
    assert e_sum % n == 0
    e_orb = e_sum // n
    # fundamental-group invariant |Λ/S_Λ|, S_Λ = Σ_{g≠1} sat_Λ((g-1)Λ), and the axis index
    # [Λ : Σ_{g≠1} Λ^g] — both sums run over ALL non-trivial elements, not only class representatives
    for g in G:
        if g == I3:
            continue
        M3 = msub(g, I3)
        axes += kernel_Z(M3)
        sat_gens += saturation_basis(M3)
    S_index = index_of_span(sat_gens, 3)
    axis_index = index_of_span(axes, 3)
    return {"order": n, "untwisted_h_pq": H, "h11": h11, "h21": h21, "h10": H[1][0], "h20": H[2][0], "h30": H[3][0],
            "euler_from_hodge": 2 * (h11 - h21), "euler_DHVW": e_orb, "euler_check": e_orb == 2 * (h11 - h21),
            "twisted_sectors": twisted, "Lambda_mod_S_index": S_index,
            "pi1_order_of_A_mod_G": None if S_index is None else S_index ** 2,
            "axis_index": axis_index}

def hodge_summary(res):
    return {"h11": res["h11"], "h21": res["h21"], "euler": res["euler_from_hodge"], "euler_check": res["euler_check"]}

# --------------------------------------------------------------------------------------
# helpers for JSON output
# --------------------------------------------------------------------------------------

def jsonable(x):
    if isinstance(x, Fr):
        return str(x) if x.denominator != 1 else int(x)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x
