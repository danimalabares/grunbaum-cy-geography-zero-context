#!/usr/bin/env python3
"""Local model of the smoothing of the singular point of Ybar, in the coordinates of
P(1^8,2^2), and the question whether the two degree-2 equations can acquire y-terms.

Set-up (REPORT.md sec. 4.1).  U = k^4 with the quadratic form q(u) = u0*u3 - u1*u2 (so
{q=0} subset P^3 is the quadric surface D = P^1xP^1 and |-K_D| = O(2,2) = Sym^2 U^* / <q>).
The affine cone over D subset P^8 is

     C = { u.u^T : q(u) = 0 }  subset  H_0 = { lambda = 0 } subset Sym^2 U = k^10,
     lambda(A) = a_03 - a_12         (so lambda(u.u^T) = q(u)).

Its (-1)-weight smoothing sweeps out the cone over V_8 = (P^3, O(2)):

     W_s = { u.u^T : q(u) = s },   W_s - A_0  subset  H_0 = k^9   (lambda(A_0) = s).

In the affine chart w = 1 of P(1^8,2^2) the nine coordinates of H_0 split as
seven "visible" coordinates x_1..x_7 (the image of the projection P^8 --> P^6 used to
build the surface S) and two "invisible" ones y_1,y_2 (the kernel of that projection);
the degree-2 piece of the coordinate ring of P(1^8,2^2) restricts, in this chart, to

     V_0 = < monomials in x of degree <= 2 >  +  < y_1, y_2 >      (dim 28+7+1+2 = 38).

We compute, exactly, the subspace of V_0 vanishing on W_s - A_0 and its image under the
projection onto <y_1,y_2>, for s = 0 and for s != 0, and for many random choices of the
projection centre and of A_0.
"""
import random
from fractions import Fraction
from itertools import combinations_with_replacement

P = 32003                      # exact arithmetic in F_P (P prime, > any structure constant used)
random.seed(20260911)

IDX = [(i, j) for i in range(4) for j in range(i, 4)]      # 10 monomials u_i u_j
POS = {p: k for k, p in enumerate(IDX)}

def mono_mul(m1, m2):
    return tuple(a + b for a, b in zip(m1, m2))

def reduce_mod_q(poly, s):
    """Reduce a dict{exponent-tuple: coeff} modulo  u0*u3 - u1*u2 - s  (lex, u0*u3 leading)."""
    poly = dict(poly)
    changed = True
    while changed:
        changed = False
        for m in list(poly):
            c = poly[m]
            if c % P == 0:
                del poly[m]; continue
            if m[0] >= 1 and m[3] >= 1:
                del poly[m]
                r = (m[0] - 1, m[1], m[2], m[3] - 1)
                for mm, cc in ((mono_mul(r, (0, 1, 1, 0)), c), (r, c * s)):
                    poly[mm] = (poly.get(mm, 0) + cc) % P
                changed = True
                break
    return {m: c % P for m, c in poly.items() if c % P}

def A_entries():
    """A = u.u^T as 10 polynomials in u."""
    out = []
    for (i, j) in IDX:
        e = [0, 0, 0, 0]; e[i] += 1; e[j] += 1
        out.append({tuple(e): 1})
    return out

def lin_comb(polys, coeffs):
    r = {}
    for p, c in zip(polys, coeffs):
        if c % P == 0: continue
        for m, cc in p.items():
            r[m] = (r.get(m, 0) + c * cc) % P
    return {m: c for m, c in r.items() if c}

def poly_mul(p1, p2):
    r = {}
    for m1, c1 in p1.items():
        for m2, c2 in p2.items():
            m = mono_mul(m1, m2)
            r[m] = (r.get(m, 0) + c1 * c2) % P
    return {m: c for m, c in r.items() if c}

def rank_and_kernel(rows, ncols):
    """rows: list of length-ncols vectors over F_P.  Return (rank, basis of kernel of the
    map F_P^ncols -> ..., i.e. of the matrix whose COLUMNS are indexed by the unknowns)."""
    M = [r[:] for r in rows]
    piv = []; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][c] % P), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [(v * inv) % P for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % P:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(ncols) if c not in piv]
    ker = []
    for f in free:
        v = [0] * ncols; v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-M[i][f]) % P
        ker.append(v)
    return r, ker

def run(s, trial):
    # H_0 = ker(lambda), lambda(A) = a_03 - a_12 : a basis of H_0 inside Sym^2 U
    lam = [0]*10; lam[POS[(0,3)]] = 1; lam[POS[(1,2)]] = -1 % P
    basis = []
    for k in range(10):
        if k == POS[(0,3)]:
            continue
        v = [0]*10; v[k] = 1
        if k == POS[(1,2)]:
            v[POS[(0,3)]] = 1                    # a_03 + a_12 direction, in ker(lambda)
        basis.append(v)                          # 9 vectors spanning ker(lambda)
    assert len(basis) == 9
    assert all(sum(l*b for l, b in zip(lam, v)) % P == 0 for v in basis)
    # A_0 with lambda(A_0) = s : take A_0 = s * e_{03}
    A0 = [0]*10; A0[POS[(0,3)]] = s % P
    Apoly = A_entries()
    # coordinates of  A - A_0  along the chosen basis of H_0 : need the dual basis.
    # Instead work directly: pick a general linear coordinate system (z_1..z_9) on H_0 by
    # choosing 9 general functionals on Sym^2 U vanishing on the line spanned by lambda's
    # "dual" direction. Simplest: use general functionals phi_k on Sym^2 U restricted to H_0.
    phis = [[random.randrange(P) for _ in range(10)] for _ in range(9)]
    # value of phi_k on (A - A_0), as a polynomial in u reduced mod q - s
    coord = []
    for ph in phis:
        p = lin_comb(Apoly, ph)
        const = sum(a*b for a, b in zip(ph, A0)) % P
        p = dict(p); p[(0,0,0,0)] = (p.get((0,0,0,0), 0) - const) % P
        coord.append(reduce_mod_q(p, s))
    x = coord[:7]; y = coord[7:]                 # 7 visible + 2 invisible coordinates
    # basis of V_0 : 1, x_i, x_i x_j, y_1, y_2   (1 + 7 + 28 + 2 = 38)
    V = [{(0,0,0,0): 1}] + x + [poly_mul(x[i], x[j]) for i, j in combinations_with_replacement(range(7), 2)] + y
    V = [reduce_mod_q(p, s) for p in V]
    assert len(V) == 38
    mons = sorted({m for p in V for m in p})
    rows = [[p.get(m, 0) for p in V] for m in mons]
    rk, ker = rank_and_kernel(rows, 38)
    ypart = [[v[36], v[37]] for v in ker]
    rky, _ = rank_and_kernel([[v[36], v[37]] for v in ker] or [[0, 0]], 2)
    return len(ker), rky

print("s        trial   dim{f in V_0 : f|_{W_s} = 0}   dim of its image in <y_1,y_2>")
ok = True
for s in [0, 1, 7, 12345]:
    for trial in range(3):
        d, ry = run(s, trial)
        print("%-8d %-7d %-29d %d" % (s, trial, d, ry))
        if ry != 0: ok = False
print()
print("CONCLUSION: in this local model the two degree-2 equations never acquire a y-term"
      if ok else "CONCLUSION: a y-term does occur")

# ---------------------------------------------------------------------------
# Structural explanation of the rank.  Write lambda for the linear functional on
# Sym^2 U with lambda(u.u^T) = q(u), H_0 = ker(lambda), and K subset H_0 the
# 2-dimensional centre of the projection P^8 --> P^6.  Restriction of quadrics
# I_{v_2(P^3)}(2) --> I_{D_8}(2) is an isomorphism (both 20-dimensional), so every
# Q in I_{D_8}(2) has a unique extension Qt to Sym^2 U vanishing on the cone over
# v_2(P^3).  Then:
#     Lambda   = { Q : K subset rad(Q|_{H_0}) }          (= H^0(I_S(2)), expected dim 3)
#     Lambda_0 = { Q : K subset rad(Qt) on Sym^2 U }     (expected dim 2)
# and for Q in Lambda, B_Qt( . , k) = c_Q(k) * lambda, so the y-coefficient of the
# corresponding element of V_0 is c_Q, and rank(Lambda -> K^*) = dim Lambda - dim Lambda_0.
print()
print("Structural computation:   dim Lambda,  dim Lambda_0,  rank")
def minors_basis():
    """The 20 quadrics cutting out the cone over v_2(P^3) in Sym^2 U, as symmetric
    10x10 matrices (quadratic forms in the a_ij)."""
    out = []
    def sym(i, j):   # index of the coordinate a_{ij}
        return POS[(min(i, j), max(i, j))]
    seen = set()
    for (i, j) in [(i, j) for i in range(4) for j in range(4)]:
        for (k, l) in [(k, l) for k in range(4) for l in range(4)]:
            key = tuple(sorted([tuple(sorted((i, j))), tuple(sorted((k, l)))])) + \
                  tuple(sorted([tuple(sorted((i, l))), tuple(sorted((k, j)))]))
            # a_ij a_kl - a_il a_kj
            M = [[0]*10 for _ in range(10)]
            def add(p, q, c):
                M[p][q] = (M[p][q] + c) % P; M[q][p] = (M[q][p] + c) % P
            add(sym(i, j), sym(k, l), 1)
            add(sym(i, l), sym(k, j), -1 % P)
            if all(all(v % P == 0 for v in row) for row in M): continue
            flat = tuple(v % P for row in M for v in row)
            if flat in seen: continue
            seen.add(flat); out.append(M)
    # reduce to a basis
    rows = [[v for row in M for v in row] for M in out]
    rk, _ = rank_and_kernel(list(map(list, zip(*rows))), len(rows))   # rank of the span
    return out
def span_dim(mats):
    rows = [[v for row in M for v in row] for M in mats]
    r, _ = rank_and_kernel([[rows[j][i] for j in range(len(rows))] for i in range(100)], len(rows))
    return r
lam_vec = [0]*10; lam_vec[POS[(0,3)]] = 1; lam_vec[POS[(1,2)]] = (-1) % P
mins = minors_basis()
print("   number of independent 2x2 minors (expect 20):", span_dim(mins))
for trial in range(4):
    # a general 2-dimensional K inside H_0 = ker(lambda)
    Kb = []
    while len(Kb) < 2:
        v = [random.randrange(P) for _ in range(10)]
        c = sum(a*b for a, b in zip(lam_vec, v)) % P
        # project v into ker(lambda) : subtract (c / lambda(e)) * e with lambda(e)=1
        e = [0]*10; e[POS[(0,3)]] = 1
        v = [(vi - c*ei) % P for vi, ei in zip(v, e)]
        Kb.append(v)
    # coefficients c_M of a combination sum c_M * M ; conditions
    n = len(mins)
    def cond_rows(restrict_to_H0):
        rows = []
        for k in Kb:
            for t in range(10):
                if restrict_to_H0:
                    # B_Q(v,k) = 0 for all v in H_0 : test against a basis of H_0
                    pass
            # build: for each basis vector v of the relevant space, the linear form in c_M
        return rows
    # Lambda : B_Q(v,k)=0 for v in H_0 ; Lambda_0 : for v in Sym^2 U
    H0basis = []
    for t in range(10):
        e = [0]*10; e[t] = 1
        c = sum(a*b for a, b in zip(lam_vec, e)) % P
        ee = [0]*10; ee[POS[(0,3)]] = 1
        H0basis.append([(ei - c*fi) % P for ei, fi in zip(e, ee)])
    full = [[1 if t == r else 0 for t in range(10)] for r in range(10)]
    res = {}
    for name, vs in (("Lambda", H0basis), ("Lambda_0", full)):
        rows = []
        for k in Kb:
            for v in vs:
                rows.append([sum(v[a]*mins[m][a][b]*k[b] for a in range(10) for b in range(10)) % P
                             for m in range(n)])
        rk, ker = rank_and_kernel(rows, n)
        res[name] = len(ker)
    red = n - 20                      # the generating list of minors is redundant
    print("   trial %d :  dim Lambda = %d , dim Lambda_0 = %d , rank = %d"
          % (trial, res["Lambda"] - red, res["Lambda_0"] - red, res["Lambda"] - res["Lambda_0"]))
