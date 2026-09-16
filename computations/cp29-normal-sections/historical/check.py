#!/usr/bin/env python3
"""Exact, standard-library-only check of the published CP2_9 Hilbert tangent.

Run from anywhere; the script reads only the committed historical facet JSON.
Taylor pair syzygies generate all relations on a monomial ideal. Each
coefficient equation here is v=w or v=0, so union-find is exact over QQ (and
any field). No Groebner basis, CAS, or higher-order deformation is used.
"""
import hashlib
import itertools as it
import json
from fractions import Fraction as Q
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'runs/cp2-nine-vertex-equivariant-t2-2026-09-09/data/minimal_nonfaces.json'
raw = INPUT.read_bytes()
data = json.loads(raw)
facets = [frozenset(f) for f in data['facets']]
faces = {frozenset(c) for f in facets for r in range(6) for c in it.combinations(sorted(f), r)}
assert len(facets) == len(set(facets)) == 36
fvec = [sum(len(f) == r for f in faces) for r in range(1, 6)]
assert fvec == [9, 36, 84, 90, 36]
assert all(frozenset(c) in faces for c in it.combinations(range(1, 10), 3))
# Complete 2-skeleton gives connected Delta, H_1(Delta)=0, connected vertex
# links (complete graphs), and nonempty edge links. Hochster gives depth>=3.
nonfaces = [frozenset(c) for r in range(1, 10) for c in it.combinations(range(1, 10), r)
            if frozenset(c) not in faces and all(frozenset(c)-{v} in faces for v in c)]
assert set(nonfaces) == {frozenset(g) for g in data['minimal_nonfaces']}
assert len(nonfaces) == 36 and all(len(g) == 4 for g in nonfaces)
gens = sorted(tuple(int(i in g) for i in range(1, 10)) for g in nonfaces)

def monomials(degree, n=9):
    if n == 1:
        yield (degree,)
    else:
        for first in range(degree+1):
            for tail in monomials(degree-first, n-1):
                yield (first,) + tail

def survives(a):
    return frozenset(i+1 for i, e in enumerate(a) if e) in faces

mons = [a for a in monomials(4) if survives(a)]
assert len(mons) == 459
variables = [(i, a) for i in range(36) for a in mons]
index = {v: j for j, v in enumerate(variables)}
zero = len(variables)
parent = list(range(zero+1))
size = [1]*(zero+1)

def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a

def join(a, b):
    a, b = find(a), find(b)
    if a == b:
        return
    if size[a] < size[b]:
        a, b = b, a
    parent[b] = a
    size[a] += size[b]

equations = 0
for i, j in it.combinations(range(36), 2):
    lcm = tuple(max(a, b) for a, b in zip(gens[i], gens[j]))
    outputs = []
    for k in (i, j):
        multiplier = tuple(a-b for a, b in zip(lcm, gens[k]))
        terms = {}
        for a in mons:
            product = tuple(x+y for x, y in zip(a, multiplier))
            if survives(product):
                terms[product] = index[k, a]
        outputs.append(terms)
    left, right = outputs
    for product in left.keys() | right.keys():
        join(left.get(product, zero), right.get(product, zero))
        equations += 1

classes = {}
for v in range(zero):
    r = find(v)
    if r != find(zero):
        classes.setdefault(r, []).append(v)
basis = [classes[r] for r in sorted(classes)]
assert len(basis) == 93
# Basis vector is 1 on one live component, 0 elsewhere. Distinct components
# are disjoint; all Taylor relations hold by construction; this is a full basis.
degree_counts = {}
for component in basis:
    weights = {tuple(a-b for a, b in zip(variables[v][1], gens[variables[v][0]])) for v in component}
    assert len(weights) == 1
    weight = next(iter(weights))
    degree_counts[weight] = degree_counts.get(weight, 0)+1

# Coordinate derivations x_j d/dx_i: diagonal ones kill monomial generators
# modulo I; each off-diagonal nonzero vector has distinct weight e_j-e_i.
nonzero_coordinate_directions = []
for i, j in it.permutations(range(9), 2):
    support = []
    for k, g in enumerate(gens):
        if g[i]:
            a = list(g)
            a[i] -= 1
            a[j] += 1
            a = tuple(a)
            if survives(a):
                support.append(index[k, a])
    if support:
        roots = {find(v) for v in support}
        assert find(zero) not in roots
        assert set(support) == {v for r in roots for v in classes[r]}
        nonzero_coordinate_directions.append([i+1, j+1])
assert len(nonzero_coordinate_directions) == 72

def mul(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

# A_n = sum f_(r-1) binomial(n-1,r-1) for n>=1, a polynomial in n.
poly = [Q(0)]*5
for r, f in enumerate(fvec, 1):
    term = [Q(f)]
    for k in range(1, r):
        term = [c/Q(k) for c in mul(term, [-k, 1])]
    for i, c in enumerate(term):
        poly[i] += c
assert poly == [Q(3), Q(0), Q(9,2), Q(0), Q(3,2)]
# Kummer RR: 3 binom(q n^2/2+2,2) with q=2.
rr = [c*Q(3,2) for c in mul([2, 0, 1], [1, 0, 1])]
assert rr == poly
hf = [1] + [sum(f*comb(n-1, r-1) for r, f in enumerate(fvec, 1) if r <= n) for n in range(1, 9)]
assert hf[1:4] == [9,45,165]
result = {
    'arithmetic': 'exact integer union-find and rational polynomial arithmetic',
    'input_sha256': hashlib.sha256(raw).hexdigest(),
    'f_vector': fvec, 'complete_2_skeleton': True, 'minimal_quartic_generators': len(gens),
    'A4_dimension': len(mons), 'coefficient_variables': len(variables),
    'Taylor_pairs': comb(36,2), 'coefficient_equations_including_redundancies': equations,
    'Hom_S_I_A_degree0_dimension': len(basis), 'coordinate_orbit_dimension': 72,
    'special_projective_stabilizer_dimension': 80-72, 'intrinsic_graded_tangent_dimension': 93-72,
    'hilbert_polynomial_coefficients_ascending': [str(c) for c in poly],
    'hilbert_function_degrees_0_through_8': hf, 'Kummer_q': 2, 'Kummer_h0_H': 9,
    'Kummer_polarized_dimension': 4, 'PGL9_dimension': 80, 'smooth_Kummer_Hilbert_dimension_if_nonempty': 84,
    'tangent_minus_required_dimension': 93-84,
    'multigraded_tangent_dimensions': [{'weight': list(w), 'dimension': d} for w,d in sorted(degree_counts.items())]
}
out = Path(__file__).resolve().parent
(out/'exact-check.json').write_text(json.dumps(result, indent=2)+'\n')
(out/'tangent-basis.json').write_text(json.dumps({'generators':gens,'standard_quartic_monomials':mons,
    'index_convention':'variable i*459+j is coefficient of standard_quartic_monomials[j] in image of generators[i]',
    'basis_supports':basis},separators=(',',':'))+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'multigraded_tangent_dimensions'},indent=2))
