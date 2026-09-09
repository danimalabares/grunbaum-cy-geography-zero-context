#!/usr/bin/env python3
"""Task 1: verify the combinatorial input for the 9-vertex triangulation of CP^2.

Checks: 36 facets, f-vector (9,36,84,90,36), pseudomanifold property,
minimal nonfaces (expect 36 quartics = 36 4-subsets, no other minimal nonfaces),
G = <(23)(46)(78),(12)(45)(78)> has order 6, is isomorphic to S_3, fixes 9,
and preserves the facet set (hence I_Delta).  Also computes the full
automorphism group of Delta (expect order 54) by brute force over S_9.
Pure Python, exact.  Writes data/minimal_nonfaces.json and data/groups.json.
"""
import itertools, json, os, sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
DATA = os.path.join(RUN, "data")

facets = []
with open(os.path.join(DATA, "facets_chapoton_manivel_1109.6490v1.txt")) as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for tok in line.split():
            facets.append(frozenset(int(c) for c in tok))
assert len(facets) == 36, len(facets)
assert len(set(facets)) == 36
assert all(len(F) == 5 for F in facets)
V = sorted(set().union(*facets))
assert V == list(range(1, 10))

# faces
faces = set()
for F in facets:
    for k in range(1, 6):
        for S in itertools.combinations(sorted(F), k):
            faces.add(frozenset(S))
fvec = [sum(1 for f in faces if len(f) == k) for k in range(1, 6)]
print("f_vector", fvec)
assert fvec == [9, 36, 84, 90, 36], fvec

# pseudomanifold: every 4-face (ridge) in exactly two facets
ridges = {}
for F in facets:
    for S in itertools.combinations(sorted(F), 4):
        ridges.setdefault(frozenset(S), 0)
        ridges[frozenset(S)] += 1
assert all(v == 2 for v in ridges.values())
print("ridge_in_exactly_two_facets", True)

# minimal nonfaces: subsets not faces all of whose proper subsets are faces
minimal_nonfaces = []
for k in range(1, 10):
    for S in itertools.combinations(V, k):
        fs = frozenset(S)
        if fs in faces:
            continue
        if all(frozenset(T) in faces for T in itertools.combinations(S, k - 1)):
            minimal_nonfaces.append(sorted(S))
by_size = {}
for m in minimal_nonfaces:
    by_size[len(m)] = by_size.get(len(m), 0) + 1
print("minimal_nonfaces_by_size", by_size)
assert by_size == {4: 36}, by_size
# all 3-subsets are faces (2-neighbourly), 4-faces = 90 of 126 4-subsets, so 36 missing 4-subsets
assert comb(9, 4) - 90 == 36

# link of vertex 9 (expect an 8-vertex 3-sphere with 24 facets)
link9 = [F - {9} for F in facets if 9 in F]
print("link_9_facets", len(link9))

def perm_from_cycles(cycles, n=9):
    p = {i: i for i in range(1, n + 1)}
    for cyc in cycles:
        for i in range(len(cyc)):
            p[cyc[i]] = cyc[(i + 1) % len(cyc)]
    return tuple(p[i] for i in range(1, n + 1))

def compose(p, q):  # (p*q)(i) = p(q(i))
    return tuple(p[q[i] - 1] for i in range(len(q)))

def apply_perm(p, S):
    return frozenset(p[i - 1] for i in S)

def closure(gens):
    n = len(gens[0])
    e = tuple(range(1, n + 1))
    G = {e}
    frontier = [e]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = compose(s, g)
                if h not in G:
                    G.add(h)
                    new.append(h)
        frontier = new
    return G

facet_set = set(facets)
def preserves(p):
    return {apply_perm(p, F) for F in facets} == facet_set

s1 = perm_from_cycles([(2, 3), (4, 6), (7, 8)])
s2 = perm_from_cycles([(1, 2), (4, 5), (7, 8)])
G = closure([s1, s2])
print("G_order", len(G))
assert len(G) == 6
assert all(preserves(g) for g in G)
assert all(g[8] == 9 for g in G)
# nonabelian of order 6 => S_3
assert compose(s1, s2) != compose(s2, s1)
print("G_is_S3", True)
# orders of elements
def order(p):
    e = tuple(range(1, 10)); q = p; k = 1
    while q != e:
        q = compose(p, q); k += 1
    return k
print("G_element_orders", sorted(order(g) for g in G))

# full automorphism group by brute force
Aut = [p for p in itertools.permutations(range(1, 10)) if preserves(p)]
print("Aut_order", len(Aut))
assert len(Aut) == 54
assert all(g in set(Aut) for g in G)
h1 = perm_from_cycles([(1, 4, 7), (2, 5, 8), (3, 6, 9)])
h2 = perm_from_cycles([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
tau = perm_from_cycles([(1, 2), (4, 6), (8, 9)])
assert preserves(h1) and preserves(h2) and preserves(tau)
# stabiliser of 9 in Aut
Stab9 = [p for p in Aut if p[8] == 9]
print("Aut_stabiliser_of_9_order", len(Stab9))
assert len(Stab9) == 6 and set(Stab9) == G
print("G_equals_full_stabiliser_of_vertex_9", True)

json.dump({"minimal_nonfaces": minimal_nonfaces,
           "facets": [sorted(F) for F in facets],
           "f_vector": fvec}, open(os.path.join(DATA, "minimal_nonfaces.json"), "w"), indent=1)
json.dump({"G_generators": [list(s1), list(s2)],
           "G": sorted(list(g) for g in G),
           "Aut": sorted(list(g) for g in Aut),
           "Aut_generators_from_paper": {"h1": list(h1), "h2": list(h2), "tau": list(tau)},
           "convention": "permutation p stored as image list [p(1),...,p(9)]"},
          open(os.path.join(DATA, "groups.json"), "w"), indent=1)
print("INPUT_VERIFIED")
