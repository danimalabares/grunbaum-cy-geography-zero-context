#!/usr/bin/env python3
"""Necessary order-two locus of rational syzygy graph rays, not a fibre.

Root-coordinated sole arithmetic slot required.  Uses the ten exact source
intrinsic S3 tangent orbits. For U=q B(t), Lz=q(B(t),0)+q T_t(z),
L=(B,D).  A constant left inverse J forces z=q(I-qJT_t)^(-1)t.
This script computes every coefficient of (I-LJ)T_t(t), a system of
homogeneous quadrics in ten parameters, modulo a declared good prime.
It writes full residuals and their independently reconstructible row span.
Necessary only: no rational-family or smoothness assertion is made.
"""
import argparse
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
OLD = RUN.parent / 'astra-computation-2026-09-08'
sys.path.insert(0, str(OLD / 'scripts'))
from compare_lineage_tangents import polynomial, plus, mul


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prime', type=int, default=101)
    ap.add_argument('--max-seconds', type=float, default=120)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    started = time.monotonic()
    p = args.prime
    assert p > 3 and all(p % d for d in range(2, int(p**.5)+1))
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    def gate():
        assert time.monotonic() - started < args.max_seconds, 'internal time limit'
    def mod(a):
        a = Q(a)
        return a.numerator * pow(a.denominator, -1, p) % p
    chartpath = OLD / 'data/fixed_chart.json'
    blockpath = OLD / 'data/equivariant_blocks_QQ.json'
    sourcepath = REPO / 'equations/deformation_data.json'
    minorpath = OLD / 'logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json'
    chart = json.loads(chartpath.read_text())
    blockdata = json.loads(blockpath.read_text())
    source = json.loads(sourcepath.read_text())
    minor = json.loads(minorpath.read_text())
    assert hashlib.sha256(chartpath.read_bytes()).hexdigest() == blockdata['source_chart_sha256']
    exact_tangents = []
    polynomial_tangents = []
    for orbit in source['intrinsic_basis_orbits_1_based']:
        g = [{} for _ in range(16)]
        for j in orbit:
            col = source['intrinsic_columns_in_embedded_basis_1_based'][j-1]-1
            images = source['embedded_tangent_basis'][col]['images_in_generator_order']
            g = [plus(a, polynomial(s)) for a, s in zip(g, images)]
        z = []
        for O in chart['coefficient_orbits']:
            vals = {g[i].get(tuple(m), Q(0)) for i,m in O}
            assert len(vals) == 1
            z.append(vals.pop())
        assert all(sum(Q(a)*z[j] for j,a in row) == 0 for row in chart['linear_rows'])
        exact_tangents.append(z)
        polynomial_tangents.append(g)
    assert len(exact_tangents) == 10
    tangents = [[mod(a) for a in z] for z in exact_tangents]
    blocks = {}
    rows = []
    labels = []
    for kind, block in blockdata['blocks'].items():
        cv = {}
        for name in ['A_minus_identity', 'B', 'C', 'D']:
            cv[name] = [[{int(j): mod(a) for j,a in cell if mod(a)} for cell in row]
                        for row in block[name]]
        blocks[kind] = cv
        for name in ['B', 'D']:
            for i, row in enumerate(cv[name]):
                for j, cell in enumerate(row):
                    rows.append(cell)
                    labels.append([kind, name, i, j])
    assert len(rows) == 1650
    def dot(row,z):
        return sum(a*z[j] for j,a in row.items()) % p
    def evaluate(matrix,z):
        return [[dot(cell,z) for cell in row] for row in matrix]
    # Carry the exact elementary row operations as sparse combinations of
    # ORIGINAL L rows. They provide J and certificate data, avoiding a
    # numerical inverse or an untracked independent subsystem.
    ech = {}
    selected = []
    for i, original in enumerate(rows):
        row = dict(original)
        combo = {i: 1}
        for pivot in sorted(ech):
            if pivot not in row:
                continue
            a = row[pivot]
            old, trans = ech[pivot]
            for j,b in old.items():
                row[j] = (row.get(j,0)-a*b) % p
                if not row[j]: del row[j]
            for j,b in trans.items():
                combo[j] = (combo.get(j,0)-a*b) % p
                if not combo[j]: del combo[j]
        if row:
            pivot = min(row)
            inv = pow(row[pivot], -1, p)
            ech[pivot] = ({j:a*inv%p for j,a in row.items()},
                          {j:a*inv%p for j,a in combo.items()})
            selected.append(i)
            if len(ech) == 291:
                break
    assert sorted(ech) == list(range(291))
    def solve(rhs):
        x = [0]*291
        for pivot in range(290,-1,-1):
            row, trans = ech[pivot]
            x[pivot] = (sum(a*rhs[j] for j,a in trans.items()) -
                        sum(a*x[j] for j,a in row.items() if j != pivot)) % p
        return x
    for z in tangents:
        assert solve([dot(row,z) for row in rows]) == z
    evals = [{kind:{name:evaluate(m,z) for name,m in block.items()}
              for kind,block in blocks.items()} for z in tangents]
    # T_a(v_b) in row order (A(v_b) B(v_a), C(v_b) B(v_a)).
    def apply(a,b):
        result = []
        for kind in blocks:
            U = evals[a][kind]['B']
            for name in ['A_minus_identity','C']:
                M = evals[b][kind][name]
                for row in M:
                    for j in range(len(U[0])):
                        result.append(sum(c*U[k][j] for k,c in enumerate(row)) % p)
        assert len(result) == len(rows)
        return result
    monomials = list(combinations_with_replacement(range(10),2))
    residual_columns = []
    z2_columns = []
    for n,(a,b) in enumerate(monomials):
        gate()
        rhs = apply(a,b)
        if a != b:
            rhs = [(x+y)%p for x,y in zip(rhs, apply(b,a))]
        z = solve(rhs)
        residual = [(dot(row,z)-v)%p for row,v in zip(rows,rhs)]
        assert all(residual[i] == 0 for i in selected)
        residual_columns.append(residual)
        z2_columns.append(z)
        print('Q2_COLUMN', n+1, a+1,b+1, 'NONZERO',sum(bool(x) for x in residual),flush=True)
    residual_rows = [[col[i] for col in residual_columns] for i in range(len(rows))]
    qech = {}
    independent = []
    for i,original in enumerate(residual_rows):
        row = {j:a for j,a in enumerate(original) if a}
        for pivot in sorted(qech):
            if pivot in row:
                a = row[pivot]
                for j,b in qech[pivot].items():
                    row[j] = (row.get(j,0)-a*b)%p
                    if not row[j]: del row[j]
        if row:
            pivot = min(row)
            inv = pow(row[pivot],-1,p)
            qech[pivot] = {j:a*inv%p for j,a in row.items()}
            independent.append(i)
    # Original twelve product-rank rows, retaining their linear pencil.
    F = [polynomial(s) for s in source['generator_order']]
    gpairs = list(combinations_with_replacement(range(16),2))
    x2 = [tuple(c.count(i) for i in range(8)) for c in combinations_with_replacement(range(8),2)]
    pencils = []
    for g in polynomial_tangents:
        def derivative(c):
            i,j = gpairs[c//36]
            return mul({x2[c%36]:Q(1)}, plus(mul(g[i],F[j]),mul(F[i],g[j])))
        columns = [plus(derivative(c['index']),derivative(c['central_representative_column']),Q(-1))
                   for c in minor['minor_columns']]
        pencils.append([[str(col.get(tuple(m),Q(0))) for col in columns]
                        for m in minor['minor_rows_exponents']])
    def qpoly(row):
        return '+'.join(str(a)+'*t'+str(monomials[j][0]+1)+'*t'+str(monomials[j][1]+1)
                        for j,a in enumerate(row) if a) or '0'
    sing = ['// Necessary q^2 locus only. No finite fibre is produced.',
            'ring r='+str(p)+',('+','.join('t'+str(i+1) for i in range(10))+',w),dp;',
            'ideal J='+',\n'.join(qpoly(residual_rows[i]) for i in independent)+';',
            'matrix M[12][12];']
    for i,j in product(range(12),repeat=2):
        lin = [(mod(pencils[k][i][j]),k) for k in range(10)]
        terms = [str(a)+'*t'+str(k+1) for a,k in lin if a]
        if terms:
            sing.append('M['+str(i+1)+','+str(j+1)+']='+'+'.join(terms)+';')
    sing += ['poly delta=det(M);','print("PRODUCT_MINOR"); delta;',
             'ideal G=std(J);','print("QUADRATIC_LOCUS_DIM_WITH_EXTRA_W"); dim(G);',
             'print("QUADRATIC_LOCUS_BASIS"); G;',
             'ideal H=std(J,1-w*delta);',
             'print("PRODUCT_OPEN_LOCUS_DIM"); dim(H);',
             'print("PRODUCT_OPEN_LOCUS_BASIS"); H;','quit;']
    (out/'necessary_locus.sing').write_text('\n'.join(sing)+'\n')
    result = {
        'status':'COMPUTER-CERTIFIED necessary order-two equations modulo prime; no fibre',
        'prime':p,'tangent_parameters':'ten source intrinsic S3 orbits in recorded order',
        'exact_tangent_vectors':[[str(a) for a in z] for z in exact_tangents],
        'L_shape':[1650,291], 'L_selected_original_rows':selected,
        'L_echelon_and_transform':[[k,sorted(row.items()),sorted(tr.items())]
                                    for k,(row,tr) in sorted(ech.items())],
        'quadratic_monomials_zero_based':monomials,
        'quadratic_residual_rows':residual_rows,'residual_row_locations':labels,
        'quadratic_rank_mod_p':len(independent),'independent_original_residual_rows':independent,
        'quadratic_row_echelon':[[k,sorted(row.items())] for k,row in sorted(qech.items())],
        'forced_z2_columns_mod_p':z2_columns,
        'exact_product_minor_linear_pencil':pencils,
        'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                        for f in [chartpath,blockpath,sourcepath,minorpath,Path(__file__)]},
        'seconds':time.monotonic()-started,
        'remaining_success_gate':'A candidate must satisfy all Krylov residuals through k=290 exactly over Q; smoothness needs own certificate.'}
    (out/'necessary_locus.json').write_text(json.dumps(result,indent=2)+'\n')
    print('QUADRATIC_RANK',len(independent),'OF55','SECONDS',time.monotonic()-started,flush=True)
    print('SINGULAR_INPUT',out/'necessary_locus.sing',flush=True)


if __name__ == '__main__':
    main()
