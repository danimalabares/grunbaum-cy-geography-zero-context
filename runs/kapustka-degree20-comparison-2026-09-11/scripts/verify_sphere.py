#!/usr/bin/env python3
"""Facts about the Gruenbaum-Sreedharan complex M used by the reduction theorem.

I_M is read from scripts/verify_geography.m2 of the repository root (frozen):
   I = (abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg)  in QQ[a..h].
We check: f-vector, neighbourliness, closed 3-pseudomanifold, all vertex links are
2-spheres, integral homology = that of S^3, and the consequences
   h^1(O_X) = h^2(O_X) = 0,  h^3(O_X) = 1,  X = Proj k[M] arithmetically Gorenstein,
   h-vector (1,4,10,4,1), degree 20, Hilbert polynomial (10/3)m^3 + (14/3)m.
"""
from itertools import combinations
from fractions import Fraction

V = "abcdefgh"
NONFACES = ["abf","abg","abh","acg","ach","adh","bdf","bdg","beg",
            "cde","ceg","ceh","cfh","def","dfh","efg"]
NF = [frozenset(s) for s in NONFACES]
def isface(S):
    S = frozenset(S)
    return not any(nf <= S for nf in NF)

faces = {k: [c for c in combinations(V, k)] for k in range(1, 5)}
faces = {k: [c for c in faces[k] if isface(c)] for k in faces}
f = [len(faces[k]) for k in range(1, 5)]
print("f-vector                :", f)
assert f == [8, 28, 40, 20]
print("neighbourly (f1=C(8,2)) :", f[1] == 28)

# closed pseudomanifold: every 2-face in exactly two facets
cnt = {}
for F in faces[4]:
    for t in combinations(F, 3):
        cnt[t] = cnt.get(t, 0) + 1
print("every triangle in 2 facets:", set(cnt.values()) == {2}, " #triangles:", len(cnt))
assert len(cnt) == 40 and set(cnt.values()) == {2}

# vertex links are 2-spheres
ok = True
for v in V:
    L = [tuple(sorted(set(F) - {v})) for F in faces[4] if v in F]
    e = {}
    for t in L:
        for ed in combinations(t, 2): e[ed] = e.get(ed, 0) + 1
    vv = sorted({x for t in L for x in t})
    chi = len(vv) - len(e) + len(L)
    ok &= (set(e.values()) == {2}) and chi == 2
print("all 8 vertex links are 2-spheres (chi=2, every edge in 2 triangles):", ok)
assert ok

# integral homology of M by Smith normal form of the boundary maps
def smith(mat):
    """Return the list of elementary divisors and the rank (integer Smith form)."""
    import copy
    A = [row[:] for row in mat]; m = len(A); n = len(A[0]) if m else 0
    divs = []; r = 0
    while r < m and r < n:
        # find pivot with smallest nonzero abs value
        piv = None
        for i in range(r, m):
            for j in range(r, n):
                if A[i][j] and (piv is None or abs(A[i][j]) < abs(A[piv[0]][piv[1]])):
                    piv = (i, j)
        if piv is None: break
        i0, j0 = piv
        A[r], A[i0] = A[i0], A[r]
        for row in A: row[r], row[j0] = row[j0], row[r]
        done = False
        while not done:
            done = True
            for i in range(r + 1, m):
                if A[i][r]:
                    q = A[i][r] // A[r][r]
                    for j in range(r, n): A[i][j] -= q * A[r][j]
                    if A[i][r]:
                        A[r], A[i] = A[i], A[r]; done = False
            for j in range(r + 1, n):
                if A[r][j]:
                    q = A[r][j] // A[r][r]
                    for i in range(r, m): A[i][j] -= q * A[i][r]
                    if A[r][j]:
                        for i in range(r, m): A[i][r], A[i][j] = A[i][j], A[i][r]
                        done = False
        divs.append(abs(A[r][r])); r += 1
    return divs, r

idx = {k: {c: i for i, c in enumerate(faces[k])} for k in faces}
def bdry(k):                                   # C_k -> C_{k-1}  (k = size of face)
    rows, cols = len(faces[k - 1]), len(faces[k])
    Mx = [[0] * cols for _ in range(rows)]
    for c, j in idx[k].items():
        for t in range(k):
            fc = c[:t] + c[t + 1:]
            Mx[idx[k - 1][fc]][j] = (-1) ** t
    return Mx
ranks, tors = {}, {}
for k in (2, 3, 4):
    d, r = smith(bdry(k)); ranks[k] = r; tors[k] = [x for x in d if x > 1]
H = {}
for i in range(4):                             # H_i, i = 0..3 (dimension i)
    nk = len(faces[i + 1])
    rk_out = ranks.get(i + 1, 0)               # rank of d_i : C_i -> C_{i-1}
    rk_in  = ranks.get(i + 2, 0)               # rank of d_{i+1}
    H[i] = (nk - rk_out - rk_in, tors.get(i + 2, []))
print("integral homology H_i(M) = (free rank, torsion):", H)
assert H[0][0] == 1 and H[1] == (0, []) and H[2] == (0, []) and H[3][0] == 1
print("=> M is a Z-homology 3-sphere (in fact the Gruenbaum-Sreedharan 3-sphere)")

# h-vector and Hilbert polynomial of k[M]
h = [0] * 5
for i, fi in enumerate([1] + f):               # f_{-1}=1, f_0..f_3
    for j in range(5):
        # h_j = sum_i (-1)^{j-i} C(4-i, j-i) f_{i-1}
        pass
def binom(a, b):
    if b < 0 or b > a: return 0
    r = 1
    for t in range(b): r = r * (a - t) // (t + 1)
    return r
fv = [1] + f                                   # f_{-1}, f_0, f_1, f_2, f_3
h = [sum((-1) ** (j - i) * binom(4 - i, j - i) * fv[i] for i in range(j + 1)) for j in range(5)]
print("h-vector                :", h, " sum =", sum(h))
assert h == [1, 4, 10, 4, 1] and sum(h) == 20
P = lambda m: sum(h[j] * binom(m - j + 3, 3) for j in range(5))
print("Hilbert function values H(0..4):", [P(m) for m in range(5)])
print("Hilbert polynomial      : (10/3)m^3 + (14/3)m  ->", [Fraction(10,3)*m**3 + Fraction(14,3)*m for m in range(5)])
assert all(P(m) == Fraction(10,3)*m**3 + Fraction(14,3)*m for m in range(1, 8))
print()
print("CONSEQUENCES USED BY THE REDUCTION THEOREM")
print("  h^i(O_X) = dim ~H^i(M;k) :  h^1 = h^2 = 0,  h^3 = 1   (Hochster)")
print("  k[M] Gorenstein with a-invariant 0  =>  omega_X = O_X,  X aG of degree 20 in P^7")
print("  h^0(O_X(1)) = 8 = h^0(O_{P^7}(1))   =>  X nondegenerate and linearly normal")
print("ALL CHECKS PASSED")
