#!/usr/bin/env python3
"""Necessary projective smoothness test from an exact all-orders zero support."""
import argparse
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
    paths = [RUN / 'data/sparse_support_QQ/support_closure.json',
             RUN.parent / 'astra-computation-2026-09-08/data/fixed_chart.json', Path(__file__)]
    support, chart = [json.loads(p.read_text()) for p in paths[:2]]
    active = set(support['active_z_indices'])
    answers = []
    for vertex in range(8):
        pure = []
        edges = {i: set() for i in range(16)}
        entries = []
        for k, orbit in enumerate(chart['coefficient_orbits']):
            if k not in active:
                continue
            for i, m in orbit:
                if m[vertex] == 3:
                    pure.append([i, k])
                if m[vertex] == 2:
                    other = next(j for j in range(8) if j != vertex and m[j])
                    edges[i].add(other)
                    entries.append([i, other, k])
        # Maximum bipartite matching bounds matrix rank for every possible
        # value of its entries, even when orbit coefficients are repeated.
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
        answers.append({'vertex': 'abcdefgh'[vertex],
                        'potential_pure_cube_coefficients': pure,
                        'point_contained_exactly_by_support': not pure,
                        'possible_jacobian_entries_row_variable_coefficient': entries,
                        'structural_rank_upper_bound': len(match),
                        'matching': sorted([i, j] for j, i in match.items()),
                        'singularity_proved_by_support': not pure and len(match) < 4})
    result = {'scope': 'Alternate sparse3 formal path; exact support zeros only.',
              'points': answers,
              'proof': 'A coordinate point with no active pure cube is contained exactly. The projective Jacobian there uses only x_vertex^2*x_j tails. Matching size bounds all minors structurally; rank below codimension4 proves singularity. A larger bound proves nothing about smoothness.',
              'input_hashes': {str(p.relative_to(RUN.parents[1])): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in paths}}
    out.mkdir(parents=True)
    (out / 'coordinate_point_check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in a.items() if k not in ['possible_jacobian_entries_row_variable_coefficient', 'matching']}
                      for a in answers], indent=2))


if __name__ == '__main__':
    main()
