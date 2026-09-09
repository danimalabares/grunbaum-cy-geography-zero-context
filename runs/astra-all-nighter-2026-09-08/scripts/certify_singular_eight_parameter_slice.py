#!/usr/bin/env python3
"""Certify an entire invariant formal slice has a singular coordinate plane."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    old = RUN.parent / 'astra-computation-2026-09-08'
    paths = [RUN / 'data/sparse_support_QQ/support_closure.json',
             RUN / 'data/linear_u_locus_p101/necessary_locus.json',
             old / 'data/equivariant_blocks_QQ.json', old / 'data/fixed_chart.json', Path(__file__)]
    support, source, blocks, chart = [json.loads(p.read_text()) for p in paths[:-1]]
    active = set(support['active_z_indices']) | set(support['active_U_indices'])
    for i, poly in enumerate(support['quadratic_map']):
        if i not in active:
            assert all(not Q(c) or m[0] not in active or m[1] not in active for m, c in poly)
    selected = [0, 2, 4, 5, 6, 7, 8, 9]
    rowsB = [cell for b in blocks['blocks'].values() for row in b['B'] for cell in row]
    rowsD = [cell for b in blocks['blocks'].values() for row in b['D'] for cell in row]
    forcing = []
    echelon = {}
    for j in selected:
        t = list(map(Q, source['exact_tangent_vectors'][j]))
        assert all(sum(Q(c) * t[k] for k, c in cell) == 0 for cell in rowsD)
        v = t + [sum(Q(c) * t[k] for k, c in cell) for cell in rowsB]
        assert len(v) == 781 and all(not x or i in active for i, x in enumerate(v))
        forcing.append(list(map(str, v)))
        row = [t[i] for i in chart['free_coordinates']]
        for p, e in sorted(echelon.items()):
            a = row[p]
            row = [x - a * y for x, y in zip(row, e)]
        p = next(i for i, x in enumerate(row) if x)
        a = row[p]
        echelon[p] = [x / a for x in row]
    assert len(echelon) == 8
    inside = {1, 4, 7}
    linear = []
    for i, m in enumerate(chart['F0']):
        # F0 is stored as exponent vectors in the chart.
        degree = sum(m[j] for j in range(8) if j not in inside)
        assert degree > 0
        if degree == 1:
            linear.append([i, None, m])
    for k in support['active_z_indices']:
        for i, m in chart['coefficient_orbits'][k]:
            degree = sum(m[j] for j in range(8) if j not in inside)
            assert degree > 0
            if degree == 1:
                linear.append([i, k, m])
    assert {i for i, k, m in linear} == {2, 8, 11}
    result = {'status': 'COMPUTER-CERTIFIED support identities; PROVED singular formal slice',
              'field': 'Q', 'intrinsic_orbits_one_based': [j + 1 for j in selected],
              'excluded_intrinsic_orbits_one_based': [2, 4], 'free_parameter_rank': 8,
              'forcing_vectors': forcing, 'invariant_state_support': sorted(active),
              'plane': 'P2_(b,e,h)', 'normal_linear_generator_rows_one_based': [3, 9, 12],
              'all_normal_linear_terms': linear,
              'proof': 'Every one of the eight independent free forcing directions lies in the certified invariant coordinate subspace. The unique full implicit solution therefore stays there for arbitrary values of these eight formal parameters. Every generator vanishes on P2_(b,e,h), and all except rows3,9,12 vanish to order at least2 along that plane. The projective Jacobian has rank at most3 there. Flat threefold fibres have dimension3, so every point of the plane is singular. The same identities evaluate at every convergent origin-selected fibre.',
              'scope': 'The eleven coordinate-gauge free parameters are zero; the remaining intrinsic free values lie in the displayed eight-dimensional subspace. Curves need not be linear in their parameter. This does not constrain paths activating orbit2 or4, or leaving this fixed coordinate slice.',
              'input_hashes': {str(p.relative_to(RUN.parents[1])): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in paths}}
    out.mkdir(parents=True)
    (out / 'singular_slice_certificate.json').write_text(json.dumps(result, indent=2) + '\n')
    print('CERTIFIED_EIGHT_PARAMETER_SLICE_SINGULAR_ALONG_P2_BEH')


if __name__ == '__main__':
    main()
