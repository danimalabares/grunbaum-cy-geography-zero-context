#!/usr/bin/env python3
"""Independent pure-Python re-verification of an equivariant T^1/T^2 certificate.

Reads certificates/<prefix>_certificate.json produced by equivariant_t2.m2 and, with exact
Fraction arithmetic, checks: (i) the listed permutations preserve the facet set; (ii) the
matrices form a representation of the group they generate (closing the group by permutation
composition and matrix multiplication, so generator-only certificates are extended to the whole
group); (iii) Reynolds projector rank = number of invariants; (iv) character decomposition.
Usage: python3 verify_certificate.py <prefix> [expected_group_order]
"""
import json, sys, os, itertools
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__)); RUN = os.path.dirname(HERE)
prefix = sys.argv[1]
cert = json.load(open(os.path.join(RUN, "certificates", prefix + "_certificate.json")))
facets = [frozenset(F) for F in json.load(open(os.path.join(RUN, "data", "minimal_nonfaces.json")))["facets"]]
fset = set(facets)

def compose(g, h):  # (g*h)(i) = g(h(i)), perms as image tuples (1-based values)
    return tuple(g[h[i] - 1] for i in range(9))
import numpy as np
BOUND = 10**9  # exactness guard for int64 products (entries stay in {-1,0,1} in practice)
def matmul(A, B):
    """Exact product.  Integer matrices use numpy int64 with an overflow guard; otherwise Fractions."""
    if isinstance(A, np.ndarray) and isinstance(B, np.ndarray):
        C = A @ B
        assert np.abs(C).max() < BOUND and np.abs(A).max() < 10**4 and np.abs(B).max() < 10**4
        return C
    n = len(A); m = len(B[0]); k = len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k) if A[i][t] != 0) for j in range(m)] for i in range(n)]
def to_fr(M):
    fr = [[Fr(e) for e in row] for row in M]
    if all(x.denominator == 1 for row in fr for x in row):
        return np.array([[int(x) for x in row] for row in fr], dtype=np.int64)
    return fr
def eq(A, B):
    return np.array_equal(A, B) if isinstance(A, np.ndarray) else A == B
def as_fr(M):
    return [[Fr(int(e)) for e in row] for row in M] if isinstance(M, np.ndarray) else M
def rank(M):
    M = [row[:] for row in M]; r = 0; rows = len(M); cols = len(M[0]) if rows else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]; M[r] = [e / pv for e in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def trace(M): return int(np.trace(M)) if isinstance(M, np.ndarray) else sum(M[i][i] for i in range(len(M)))
def perm_order(p):
    e = tuple(range(1, 10)); q = p; k = 1
    while q != e: q = compose(p, q); k += 1
    return k

gens = {}
for el in cert["elements"]:
    p = tuple(el["perm"])
    assert {frozenset(p[i - 1] for i in F) for F in facets} == fset, "permutation does not preserve Delta"
    gens[p] = (to_fr(el["M_T2"]), to_fr(el["M_T1"]))
d2 = cert["dimT2_0"]; d1 = cert["dimT1_0"]
for p, (M2, M1) in gens.items():
    assert len(M2) == d2 and all(len(r) == d2 for r in M2)
    assert len(M1) == d1 and all(len(r) == d1 for r in M1)

# close the group; check consistency (a well-defined homomorphism)
e = tuple(range(1, 10))
I2 = np.eye(d2, dtype=np.int64); I1 = np.eye(d1, dtype=np.int64)
if not all(isinstance(M, np.ndarray) for pair in gens.values() for M in pair):
    I2 = [[Fr(int(i == j)) for j in range(d2)] for i in range(d2)]; I1 = [[Fr(int(i == j)) for j in range(d1)] for i in range(d1)]
group = {e: (I2, I1)}
if e in gens:
    assert eq(gens[e][0], I2) and eq(gens[e][1], I1)
frontier = [e]
while frontier:
    new = []
    for q in frontier:
        Mq2, Mq1 = group[q]
        for s, (Ms2, Ms1) in gens.items():
            if s == e: continue
            prod = compose(s, q)
            P2 = matmul(Ms2, Mq2); P1 = matmul(Ms1, Mq1)
            if prod in group:
                assert eq(group[prod][0], P2) and eq(group[prod][1], P1), "representation property violated"
            else:
                group[prod] = (P2, P1); new.append(prod)
    frontier = new
order = len(group)
print("group_order", order)
if len(sys.argv) > 2: assert order == int(sys.argv[2])
# full representation check on all pairs (T2)
keys = list(group)
for a in keys:
    for b in keys:
        assert eq(group[compose(a, b)][0], matmul(group[a][0], group[b][0]))
print("representation_property_all_pairs_T2", True)
# entries
ents = sorted({int(e) if isinstance(group[p][0], np.ndarray) else e for p in keys for row in group[p][0] for e in row})
print("T2_matrix_entries", [str(x) for x in ents])
# Reynolds projectors
S2 = as_fr(sum(as_fr(group[p][0]) if False else group[p][0] for p in keys)) if all(isinstance(group[p][0], np.ndarray) for p in keys) else None
def reynolds(idx):
    mats = [group[p][idx] for p in keys]
    if all(isinstance(M, np.ndarray) for M in mats):
        tot = np.zeros_like(mats[0]);
        for M in mats: tot = tot + M
        return [[Fr(int(tot[i][j]), order) for j in range(tot.shape[1])] for i in range(tot.shape[0])]
    mats = [as_fr(M) for M in mats]
    return [[sum(M[i][j] for M in mats) / order for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
R2 = reynolds(0); R1 = reynolds(1)
assert matmul(R2, R2) == R2 and matmul(R1, R1) == R1
inv2 = rank(R2); inv1 = rank(R1)
print("dim_T2_0_invariants", inv2, "trace_check", trace(R2))
print("dim_T1_0_invariants", inv1, "trace_check", trace(R1))
assert trace(R2) == inv2 and trace(R1) == inv1
# characters by element order / conjugacy class summary
classes = {}
for p in keys:
    classes.setdefault((perm_order(p), str(trace(group[p][0])), str(trace(group[p][1]))), 0)
    classes[(perm_order(p), str(trace(group[p][0])), str(trace(group[p][1])))] += 1
print("character_table_data (element order, trace T2, trace T1): count")
for k, v in sorted(classes.items()): print("  ", k, v)
json.dump({"prefix": prefix, "group_order": order, "dimT2_0": d2, "dimT1_0": d1,
           "dim_T2_0_invariants": inv2, "dim_T1_0_invariants": inv1,
           "character_data": [[list(k), v] for k, v in sorted(classes.items())]},
          open(os.path.join(RUN, "certificates", prefix + "_python_reverification.json"), "w"), indent=1)
print("CERTIFICATE_REVERIFIED", prefix)
