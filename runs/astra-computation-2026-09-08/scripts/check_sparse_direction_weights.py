#!/usr/bin/env python3
"""Tiny exact weight certificates for TWO documented directions, not a sweep.

The rejected direction has intrinsic S3 orbit weights 3=8=1, others0.
The sole proposed follow-up adds orbit10=1. Derive both from the exact
53-column source basis; never infer orbit membership from numeric g_i
coefficients. This script checks 9-variable grading equations, the fixed
chart tangent equations, and the already selected twelve product rows.
It does NOT lift, specialize a putative fibre, or claim smoothness.

Prepared only. Obtain root authorization before running the three-orbit
test; no curve-lifting variant is created by this script.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from compare_lineage_tangents import polynomial, plus, mul
from picard_product_first_order import determinant_bareiss
from build_fixed_chart import name

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]


def rref(matrix, columns):
    rows = [[Q(x) for x in row] for row in matrix]
    pivots = []
    for j in range(columns):
        k = len(pivots)
        selected = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if selected is None:
            continue
        rows[k], rows[selected] = rows[selected], rows[k]
        unit = rows[k][j]
        rows[k] = [a / unit for a in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][j]:
                factor = rows[i][j]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[k])]
        pivots.append(j)
    kernel = []
    for j in range(columns):
        if j not in pivots:
            vector = [Q(int(k == j)) for k in range(columns)]
            for row, pivot in zip(rows, pivots):
                vector[pivot] = -row[j]
            kernel.append(vector)
    return pivots, kernel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--direction', choices=['two-orbit-rejected', 'three-orbit-proposed'], required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    output = args.output.resolve()
    assert output.is_relative_to(RUN) and not output.exists()
    source = REPO / 'equations/deformation_data.json'
    chart_path = RUN / 'data/fixed_chart.json'
    minor_path = RUN / 'logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json'
    data = json.loads(source.read_text())
    chart = json.loads(chart_path.read_text())
    certificate = json.loads(minor_path.read_text())
    chosen_orbits = [3, 8] if args.direction == 'two-orbit-rejected' else [3, 8, 10]
    orbit_weights = [int(i + 1 in chosen_orbits) for i in range(10)]
    vector = [0] * 53
    for k in chosen_orbits:
        for j in data['intrinsic_basis_orbits_1_based'][k - 1]:
            vector[j - 1] = 1
    f0 = [polynomial(s) for s in data['generator_order']]
    f0_exponents = [next(iter(f)) for f in f0]
    g = [{} for _ in range(16)]
    for j, coefficient in enumerate(vector):
        if coefficient:
            b = data['intrinsic_columns_in_embedded_basis_1_based'][j] - 1
            images = data['embedded_tangent_basis'][b]['images_in_generator_order']
            g = [plus(a, polynomial(s)) for a, s in zip(g, images)]
    assert all(not any(m in f0_exponents for m in row) for row in g)
    z = []
    for orbit in chart['coefficient_orbits']:
        values = {g[i].get(tuple(m), Q(0)) for i, m in orbit}
        assert len(values) == 1, 'direction is not S3 invariant in the actual chart'
        z.append(values.pop())
    assert all(sum(Q(a) * z[j] for j, a in row) == 0 for row in chart['linear_rows'])
    weights = [0, 1, 0, 0, 1, 0, 0, 1, 0]  # a,...,h,q
    equations = [[m[k] - f0_exponents[i][k] for k in range(8)] + [1]
                 for i, row in enumerate(g) for m in row]
    pivots, kernel = rref(equations, 9)
    fixed_pivots, fixed_kernel = rref(equations + [[0] * 8 + [1]], 9)
    expected_rank = 7 if len(chosen_orbits) == 2 else 8
    assert len(pivots) == len(fixed_pivots) == expected_rank
    assert all(v[8] == 0 for v in kernel)
    b_defects = [sum(a * b for a, b in zip(row, weights)) for row in equations]
    assert (not any(b_defects)) == (len(chosen_orbits) == 2)
    # The six source permutations preserve the two weight spaces, so their
    # action commutes with the rejected torus on the whole invariant chart.
    for permutation in chart['group_images']:
        assert all(weights[i] == weights['abcdefgh'.index(permutation[i])] for i in range(8))
    pairs = list(combinations_with_replacement(range(16), 2))
    quadratics = [tuple(c.count(i) for i in range(8))
                  for c in combinations_with_replacement(range(8), 2)]
    def derivative(column):
        i, j = pairs[column // 36]
        m = quadratics[column % 36]
        return mul({m: Q(1)}, plus(mul(g[i], f0[j]), mul(f0[i], g[j])))
    residuals = [plus(derivative(column['index']), derivative(column['central_representative_column']), Q(-1))
                 for column in certificate['minor_columns']]
    minor = [[residual.get(tuple(m), Q(0)) for residual in residuals]
             for m in certificate['minor_rows_exponents']]
    assert all(a.denominator == 1 for row in minor for a in row)
    minor = [[int(a) for a in row] for row in minor]
    determinant = determinant_bareiss(minor)
    assert determinant == -1
    result = {
        'status': 'COMPUTER-CERTIFIED exact weight analysis, not a lifted family',
        'direction': args.direction, 'orbit_weights': orbit_weights,
        'intrinsic_vector_53': vector,
        'generator_first_order_terms': [{name(m): str(a) for m, a in sorted(row.items())} for row in g],
        'number_nonzero_generator_terms': sum(len(row) for row in g),
        'chart_tangent_z': [str(a) for a in z],
        'all_6960_standard_linear_tangent_equations_zero': True,
        'weight_variable_order': 'abcdefghq', 'weight_equations': equations,
        'weight_rank': len(pivots), 'weight_kernel_basis': [[str(a) for a in row] for row in kernel],
        'q_fixed_weight_rank': len(fixed_pivots),
        'q_fixed_weight_kernel_basis': [[str(a) for a in row] for row in fixed_kernel],
        'preserves_bad_B_grading': not any(b_defects),
        'central_generator_B_degrees': [sum(a * b for a, b in zip(m, weights)) for m in f0_exponents],
        'same_product_minor_integer_matrix': minor, 'same_product_minor_determinant': determinant,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'chart_sha256': hashlib.sha256(chart_path.read_bytes()).hexdigest(),
        'original_minor_sha256': hashlib.sha256(minor_path.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'same_selected_zero_context_tangent': False, 'inherits_selected_sixjet_smoothness': False,
        'curve_lifting_executed': False, 'smoothness_certified': False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('WEIGHT_RANK', len(pivots), 'PRODUCT_MINOR', determinant)
    print('PRESERVES_BAD_B_GRADING', not any(b_defects))
    print('CERTIFICATE', output)


if __name__ == '__main__':
    main()
