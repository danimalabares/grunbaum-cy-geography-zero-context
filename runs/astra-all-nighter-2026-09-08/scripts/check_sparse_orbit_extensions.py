#!/usr/bin/env python3
"""Exact support closure for seven new four-orbit paths; no jet extension."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import time

RUN = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    start = time.monotonic()
    old = RUN.parent / 'astra-computation-2026-09-08'
    paths = [RUN / 'data/sparse_support_QQ/support_closure.json',
             RUN / 'data/linear_u_locus_p101/necessary_locus.json',
             old / 'data/sparse3_direction_exact.json', old / 'data/equivariant_blocks_QQ.json',
             old / 'data/fixed_chart.json', Path(__file__)]
    full, tangents, sparse, blocks, chart = [json.loads(p.read_text()) for p in paths[:-1]]
    base = list(map(Q, sparse['chart_tangent_z']))
    directions = [list(map(Q, v)) for v in tangents['exact_tangent_vectors']]
    assert base == [sum(directions[j][i] for j in [2, 7, 9]) for i in range(291)]
    h = [[tuple(m) for m, c in poly if Q(c)] for poly in full['quadratic_map']]
    dep = set(blocks['dependent_coordinates'])
    rowsB = [cell for b in blocks['blocks'].values() for row in b['B'] for cell in row]
    rowsD = [cell for b in blocks['blocks'].values() for row in b['D'] for cell in row]
    results = []
    for added in [0, 1, 3, 4, 5, 6, 8]:
        t = [a + b for a, b in zip(base, directions[added])]
        assert all(sum(Q(c) * t[k] for k, c in cell) == 0 for cell in rowsD)
        v1 = t + [sum(Q(c) * t[k] for k, c in cell) for cell in rowsB]
        assert len(v1) == 781
        active = {i for i, a in enumerate(v1) if a}
        history = [len(active)]
        while True:
            new = {i for i, poly in enumerate(h) if i not in active
                   and any(v in active and w in active for v, w in poly)}
            if not new:
                break
            active.update(new)
            history.append(len(active))
        assert all(not any(v in active and w in active for v, w in h[i])
                   for i in range(781) if i not in active)
        points = []
        for vertex in range(8):
            pure = []
            edges = [set() for _ in range(16)]
            for k, orbit in enumerate(chart['coefficient_orbits']):
                if k not in active:
                    continue
                for i, m in orbit:
                    if m[vertex] == 3:
                        pure.append(k)
                    if m[vertex] == 2:
                        edges[i].add(next(j for j in range(8) if j != vertex and m[j]))
            match = {}
            def augment(i, seen):
                for j in sorted(edges[i]):
                    if j in seen:
                        continue
                    seen.add(j)
                    if j not in match or augment(match[j], seen):
                        match[j] = i
                        return True
                return False
            for i in range(16):
                augment(i, set())
            points.append({'vertex': 'abcdefgh'[vertex], 'active_pure_cube_coordinates': sorted(set(pure)),
                           'rank_upper_bound': len(match), 'forced_singular': not pure and len(match) < 4})
        weights = sparse['orbit_weights'][:]
        weights[added] = 1
        result = {'added_orbit_one_based': added + 1, 'orbit_weights': weights,
                  'linear_q_coefficient': list(map(str, v1)), 'support_history': history,
                  'active_z_indices': sorted(active & set(range(291))),
                  'active_dependent_z': sorted(active & dep),
                  'active_U_indices': sorted(active - set(range(291))), 'coordinate_points': points,
                  'forced_coordinate_singularities': [x['vertex'] for x in points if x['forced_singular']],
                  'smoothness': 'OPEN unless a forced singular point is listed'}
        results.append(result)
        print('ORBIT', added + 1, 'ACTIVE_DEPENDENT', len(result['active_dependent_z']),
              'FORCED_SINGULAR', result['forced_coordinate_singularities'], flush=True)
    out.mkdir(parents=True)
    (out / 'orbit_extension_certificates.json').write_text(json.dumps({
        'field': 'Q', 'cases': results, 'seconds': time.monotonic() - start,
        'quadratic_map_reference': str(paths[0].relative_to(RUN)),
        'proof': 'The fixed rational quadratic map is unchanged. The exact first-order vector satisfies all D equations. Each displayed coordinate subspace contains its forcing and is invariant under the quadratic map; implicit uniqueness proves all omitted coordinates vanish exactly on that new free path.',
        'limitation': 'Passing the coordinate support test does not certify smoothness, actual nonzero coordinates, or a manageable coefficient field.',
        'input_hashes': {str(p.relative_to(RUN.parents[1])): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in paths}}, indent=2) + '\n')


if __name__ == '__main__':
    main()
