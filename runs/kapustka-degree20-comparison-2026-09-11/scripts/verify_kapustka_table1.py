#!/usr/bin/env python3
"""Exact independent verification of Table 1 of G. Kapustka, 'Projections of del Pezzo
surfaces and Calabi-Yau threefolds' (arXiv:1010.3895v5 = Adv. Geom. 15 (2015) 143-158).

Everything is exact integer/rational arithmetic; no CAS is needed.

Three formulas are used, each derived in REPORT.md:

 (N)  number of nodes of a general complete intersection X' of hypersurfaces of degrees
      d_1..d_k (k = n-3) from I_S, for S a smooth surface in P^n cut out scheme-theoretically
      in the relevant degree:  Thom-Porteous applied to  O(-d_1)+..+O(-d_k) -> N^v_{S/P^n},
          #nodes = alpha(n; d) * deg S + K_S^2 - e(S),
          alpha  = C(n+1,2) - (n+1)*e1 + e1^2 - e2,   e1 = sum d_i, e2 = sum_{i<j} d_i d_j.

 (D)  degree of the contracted threefold:  deg Ybar = deg X' + deg D, and mult_P Ybar = deg D.

 (E)  Euler characteristic of the smoothing:
          chi(Y_t) = chi(X) - 2*chi(D) + chi(V),
      where X is the small resolution (chi(X) = chi(X_smooth CI) + 2*#nodes), D is the
      contracted del Pezzo surface, and V is the del Pezzo THREEFOLD of the same degree
      having D as a hyperplane section (the Milnor fibre of the smoothing of the cone
      C(D,-K_D) is V \ D, by Pinkham's sweeping-out-the-cone; chi(F) = chi(V) - chi(D)).
      Several V for one D  <=>  several smoothing families.
"""
from fractions import Fraction
from itertools import combinations

def binom(a, b):
    if b < 0 or b > a: return 0
    r = 1
    for i in range(b): r = r * (a - i) // (i + 1)
    return r

def chi_CI(n, degs):
    """Euler characteristic of a smooth complete intersection of multidegree degs in P^n,
    assuming sum(degs) = n+1 (so it is a Calabi-Yau threefold when n-len(degs)=3)."""
    assert sum(degs) == n + 1 and n - len(degs) == 3
    # c(T_X) = (1+H)^{n+1} / prod (1+d_i H), truncated at H^3 ; then chi = c_3 * prod d_i
    N = 4
    num = [binom(n + 1, i) for i in range(N)]
    ser = num[:]
    for d in degs:                       # divide by (1 + d H)
        inv = [(-d) ** i for i in range(N)]
        new = [0] * N
        for i in range(N):
            for j in range(N - i):
                new[i + j] += ser[i] * inv[j]
        ser = new
    prod = 1
    for d in degs: prod *= d
    return ser[3] * prod

def alpha(n, degs):
    e1 = sum(degs); e2 = sum(a * b for a, b in combinations(degs, 2))
    return binom(n + 1, 2) - (n + 1) * e1 + e1 * e1 - e2

def nodes(n, degs, degS, K2, eS):
    return alpha(n, degs) * degS + K2 - eS

# ---- del Pezzo surfaces D_d (anticanonical) and the del Pezzo threefolds V_d ----
# D_d = P^2 blown up in 9-d points (d<=7);  D_8 = P^1xP^1 ; e(D_d)=12-d for d<=7, e(D_8)=4
def eD(d):  return 4 if d == 8 else 12 - d
# del Pezzo threefolds V of degree d with a del Pezzo surface of degree d as hyperplane
# section (Fujita/Iskovskikh); chi(V):
VCHI = {8: [4],            # (P^3, O(2))                              chi = 4
        7: [6],            # Bl_pt P^3                                chi = 4+2 = 6
        6: [8, 6],         # P^1xP^1xP^1 (chi 8) and the flag 3-fold  W=(1,1) in P^2xP^2 (chi 6)
        5: [4],            # V_5 = G(2,5) cap P^6 ; chi = 4
        4: [0],            # intersection of two quadrics in P^5 ; chi = 0
        }

ROWS = [  # (No, deg D', surface used, n, degrees of X', printed #nodes, printed chi, printed H^3, printed h^0(H))
 (1, 6, "Dt_6  in P^5",  5, (2,4), 42, -96, 14, 7),
 (2, 6, "Dt_6  in P^5",  5, (2,4), 42, -98, 14, 7),
 (3, 6, "Dt_6  in P^5",  5, (3,3), 36, -76, 15, 7),
 (4, 6, "Dt_6  in P^5",  5, (3,3), 36, -78, 15, 7),
 (5, 7, "Dtt_7 in P^5",  5, (3,3), 44, -60, 16, 7),
 (6, 8, "L_P   in P^5",  5, (3,3), 52, -44, 17, 7),
 (7, 7, "Dt_7  in P^6",  6, (2,2,3), 37, -74, 19, 8),
 (8, 8, "Dtt_8 in P^6",  6, (2,2,3), 44, -60, 20, 8),
]
# the surface used is always a (possibly iterated) generic linear projection of the
# anticanonical D_d, so it is isomorphic to D_d and keeps degree d, K^2 = d, e = e(D_d).

print("%-3s %-14s %-9s %-7s %-7s %-7s %-7s %-7s" %
      ("No","surface","#nodes","chi(Yt)","H^3","h0(H)","c2.H","ok"))
allok = True
for (no, d, name, n, degs, pn, pchi, pH3, ph0) in ROWS:
    K2, e = d, eD(d)
    k   = nodes(n, degs, d, K2, e)
    degX = 1
    for a in degs: degX *= a
    H3  = degX + d
    chiX = chi_CI(n, degs) + 2 * k
    chis = sorted(set(chiX - 2 * e + cv for cv in VCHI[d]))
    # h^0(H) = chi(H) = H^3/6 + c2.H/12 ; and h^0 = 1 + dim of the P^N, given by the
    # construction as h^0(H*) + 1 = (n+1) + 1 ... here read off from H^0(G) = h^0(O_{X'}(1)) + 1
    h0  = n + 2                        # h^0(G) = h^0(O_{X'}(1)) + 1 = (n+1) + 1
    c2H = 12 * (Fraction(h0) - Fraction(H3, 6))
    ok  = (k == pn) and (pchi in chis) and (H3 == pH3) and (h0 == ph0)
    allok &= ok
    print("%-3d %-14s %-9s %-7s %-7s %-7s %-7s %-7s" %
          (no, name, "%d(%d)" % (k, pn), "%s(%d)" % (chis, pchi),
           "%d(%d)" % (H3, pH3), "%d(%d)" % (h0, ph0), str(c2H), "OK" if ok else "FAIL"))

print()
print("chi of the smooth ambient complete intersections:")
for n, degs in [(5,(2,4)), (5,(3,3)), (6,(2,2,3)), (7,(2,2,2,2))]:
    print("   X_%s in P^%d : chi = %d" % (",".join(map(str,degs)), n, chi_CI(n, degs)))
print()
print("ROW 8 (the comparison family):")
n, degs, d = 6, (2,2,3), 8
k = nodes(n, degs, d, d, eD(d))
print("   S = double projection of D_8 = P^1xP^1 into P^6 ;  deg S = 8, K^2 = 8, e = 4")
print("   #nodes of X'_{2,2,3} = %d" % k)
print("   deg Ybar = 12 + 8 = %d ;  mult_P Ybar = 8 ;  embdim_P Ybar = h^0(-K_{P1xP1}) = 9" % (12+8))
print("   chi(X) = %d ; chi(Ybar) = %d ; chi(Y_t) = %d" %
      (chi_CI(n,degs)+2*k, chi_CI(n,degs)+2*k-4+1, chi_CI(n,degs)+2*k-2*4+4))
print("   => (h11,h12) = (1, %d) ; H^3 = 20 ; h^0(H) = 8 ; c2.H = %s" %
      (1 - (chi_CI(n,degs)+2*k-2*4+4)//2, 12*(8 - Fraction(20,6))))
print()
print("ALL ROWS 1-8 REPRODUCED" if allok else "MISMATCH")
