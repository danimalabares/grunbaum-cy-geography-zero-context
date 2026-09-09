#!/usr/bin/env python3
"""Cheap integer certificate: locate the proof tangent on the quadratic cone.

No CAS dependencies, no Groebner bases, no writes to the frozen source.
The one-based intrinsic coordinates are the ordered 53-column complement in
deformation/build_equivariant_sixjet.m2, not the full 109-column normal matrix.
This certifies quadratic-component membership, not a completed Hilbert branch.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import re

SOURCE = Path('/Users/daniel/github/grunbaum-zero-context-proof')
builder = SOURCE / 'deformation/build_equivariant_sixjet.m2'
quartic = SOURCE / 'reconstruct/p1_quartic_component.m2'
text = builder.read_text()
raw = re.search(r'fixedOrbits=(\{.*?\});', text, re.S).group(1)
orbits = [[int(x) for x in re.findall(r'\d+', b)]
          for b in re.findall(r'\{([^{}]*)\}', raw)]
assert sorted(sum(orbits, [])) == list(range(1, 54))
orbit_of = {i: j for j, block in enumerate(orbits) for i in block}
matrices = {
    'A': [[1, 4, 43, 40, 31, 32], [11, 13, 46, 49, 21, 25]],
    'B': [[19, 20, 36, 41, 14, 15], [34, 35, 44, 52, 29, 30]],
    'C': [[26, 27, 50, 39, 2, 3], [22, 23, 48, 53, 16, 17]],
}
for name, (top, bottom) in matrices.items():
    assert all(orbit_of[a] == orbit_of[b] for a, b in zip(top, bottom))
    print(name, 'rows agree identically on the S3-fixed ten-plane')
    values = [[orbit_of[i]+1 for i in row] for row in [top, bottom]]
    assert all(values[0][i]*values[1][j]-values[0][j]*values[1][i] == 0
               for i, j in combinations(range(6), 2))
    assert all(x != 0 for row in values for x in row)
    print(name, 'proof tangent matrix:', values, '; all 15 minors zero')

raw_sparse = re.search(r'nonzero=(\{.*?\});', text, re.S).group(1)
sparse_set = set(map(int, re.findall(r'\d+', raw_sparse)))
sparse_weights = []
for orbit in orbits:
    flags = {int(i in sparse_set) for i in orbit}
    assert len(flags) == 1
    sparse_weights.append(flags.pop())
print('proof orbit weights:', list(range(1, 11)))
print('sparse orbit weights:', sparse_weights)
assert sparse_weights == [1, 1, 1, 1, 0, 0, 1, 1, 0, 1]
print('distinct tangents; neither jet equality nor component equality follows')
print('quadratic component dimension:', 17 + 3*(2+6-1))
print('embedded upper bound:', 56 + 17 + 3*(2+6-1))
print('input SHA256:', json.dumps({str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in [builder, quartic]}, sort_keys=True))
