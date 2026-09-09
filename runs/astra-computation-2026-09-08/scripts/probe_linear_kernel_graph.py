#!/usr/bin/env python3
"""Capped exact test of U(q)=q U1 in the S3 multiplicity Hilbert chart.

NO Groebner basis or CAS. Do not run without the root's sole-process slot.
The default tests only q^2. A nonzero residual rejects the entire ansatz,
not the smoothing or its fixed Hilbert component. Success through order
292 proves rational closure over the selected finite field by Cayley-
Hamilton; shorter success proves only compatibility to the stated order.

Notation: L(z)=(B(z),D(z)), T(z)=(A(z)U1,C(z)U1), A here meaning
A_minus_identity. The incidence equations become Lz=q(U1,0)+qTz.
With a constant left inverse J, z=q(I-qJT)^(-1)t. Check every residual
(1-LJ)T(JT)^k t, not merely the 291 selected scalar equations.

The normalized certified FIRST tangent is preserved. Higher jets generally
change; no six-jet smoothness certificate is inherited. If successful,
the origin-selected branch lies in the same fixed Hilbert germ, and any
actual smooth closed fibre must be certified separately.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parents[1]
DAY = RUN.parent / 'astra-daytime-2026-09-08'
REPO = RUN.parents[1]
sys.path.insert(0, str(DAY / 'scripts'))
from fixed_curve_lift import normalized_jet, lu_factor, lu_solve


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prime', type=int, default=101)
    ap.add_argument('--max-order', type=int, default=2)
    ap.add_argument('--max-seconds', type=float, default=120)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    started = time.monotonic()
    p = args.prime
    assert p > 3 and all(p % d for d in range(2, int(p**.5)+1))
    assert 2 <= args.max_order <= 292
    out = args.output.resolve()
    assert out.is_relative_to(RUN), 'outputs must stay in this computation run'
    assert not out.exists(), 'preserve an existing result; select a new output'
    blockpath = RUN / 'data/equivariant_blocks_QQ.json'
    chartpath = DAY / 'data/fixed_chart.json'
    data = json.loads(blockpath.read_text())
    assert hashlib.sha256(chartpath.read_bytes()).hexdigest() == data['source_chart_sha256']
    chart = json.loads(chartpath.read_text())
    rawjet, _ = normalized_jet(chart)

    def mod(a):
        a = Q(a)
        return a.numerator * pow(a.denominator, -1, p) % p

    tangent = [mod(v) for v in rawjet[1]]
    assert len(tangent) == 291
    blocks = {}
    rows = []
    labels = []
    for kind, block in data['blocks'].items():
        converted = {}
        for label in ['A_minus_identity', 'B', 'C', 'D']:
            converted[label] = [[{int(j):mod(a) for j,a in cell if mod(a)}
                                  for cell in row] for row in block[label]]
        blocks[kind] = converted
        for label in ['B', 'D']:
            for i, row in enumerate(converted[label]):
                for j, cell in enumerate(row):
                    rows.append(cell)
                    labels.append([kind, label, i, j])
    assert len(rows) == 1650

    def dot(row, z):
        return sum(a*z[j] for j,a in row.items()) % p

    def evaluate(matrix, z):
        return [[dot(cell, z) for cell in row] for row in matrix]

    # Select 291 independent ORIGINAL scalar rows, retaining their indices.
    echelon = {}
    selected = []
    for i, original in enumerate(rows):
        row = dict(original)
        for pivot in sorted(echelon):
            if pivot in row:
                c = row[pivot]
                for j,a in echelon[pivot].items():
                    row[j] = (row.get(j,0)-c*a) % p
                    if not row[j]: del row[j]
        if row:
            pivot = min(row)
            inv = pow(row[pivot], -1, p)
            echelon[pivot] = {j:a*inv % p for j,a in row.items()}
            selected.append(i)
            if len(selected) == 291: break
    assert len(selected) == 291, ('unexpected L rank', len(selected))
    lu = lu_factor([[rows[i].get(j,0) for j in range(291)] for i in selected], p)
    det = 1
    for i in range(291): det = det * lu[0][i][i] % p
    inversions = sum(lu[1][i] > lu[1][j] for i in range(291) for j in range(i+1,291))
    if inversions % 2: det = -det % p
    assert det
    linear_u = {kind:evaluate(block['B'], tangent) for kind,block in blocks.items()}
    base = []
    for kind,block in blocks.items():
        base.extend(a for row in linear_u[kind] for a in row)
        base.extend(0 for row in block['D'] for _ in row)
    assert [dot(row,tangent) for row in rows] == base

    def apply_T(z):
        result = []
        for kind,block in blocks.items():
            u = linear_u[kind]
            for label in ['A_minus_identity', 'C']:
                m = evaluate(block[label], z)
                for row in m:
                    for j in range(len(u[0])):
                        result.append(sum(a*u[k][j] for k,a in enumerate(row)) % p)
        assert len(result) == 1650
        return result

    coefficients = [[0]*291, tangent]
    status = 'compatible_to_tested_order_only'
    defect = None
    tested = 1
    for order in range(2, args.max_order+1):
        if time.monotonic()-started > args.max_seconds:
            status = 'capped_before_next_order'
            break
        rhs = apply_T(coefficients[-1])
        z = lu_solve(lu, [rhs[i] for i in selected], p)
        failures = [(i,(dot(row,z)-rhs[i]) % p) for i,row in enumerate(rows)
                    if (dot(row,z)-rhs[i]) % p]
        tested = order
        if failures:
            status = 'FAILED_linear_U_ansatz'
            defect = {'order':order, 'nonzero_residual_count':len(failures),
                      'first_residuals': [{'row':i, 'location':labels[i], 'value_mod_p':a}
                                           for i,a in failures[:24]],
                      'candidate_coefficient':z}
            print('REJECT_LINEAR_U', 'order', order, 'residual_count', len(failures),
                  'first', defect['first_residuals'][0], flush=True)
            break
        coefficients.append(z)
        print('PASS_ALL_1650_LINEAR_U_COEFFICIENT_EQUATIONS', order, flush=True)
        if order == 292: status = 'COMPUTER_CERTIFIED_rational_closure_over_Fp'
    paths = [blockpath, chartpath, REPO/'equations/deformation_data.json', Path(__file__)]
    result = {
        'status':status, 'prime':p, 'tested_order':tested,
        'ansatz':'U(q)=q*B(t), using the averaged S3-equivariant central section',
        'lineage':'same normalized embedded first tangent; not the certified six-jet',
        'L_shape':[1650,291], 'L_selected_rows':selected,
        'L_selected_determinant_mod_p':det,
        'tangent_mod_p':tangent, 'U1_blocks_mod_p':linear_u,
        'compatible_z_coefficients_mod_p':coefficients, 'defect':defect,
        'rational_formula_if_certified':'z=q*(Id-q*J*T)^(-1)*t; J solves selected L rows',
        'closure_threshold_order':292,
        'smoothness':'NOT certified by this test',
        'input_sha256':{str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in paths},
        'elapsed_seconds':round(time.monotonic()-started,3)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(status, out, flush=True)


if __name__ == '__main__': main()
