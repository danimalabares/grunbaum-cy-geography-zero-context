#!/usr/bin/env python3
"""Quadratic polynomial generators with a full equivariant matrix denominator.

Uses the exact21-free second-order affine system in --base. The proposed
raw generators are F0*(Id+q^2*G2)+q*T+q^2*Z2, G2 in End_S3(W), dim51.
After central normalization z3=-t*G2, hence the q3 equations acquire
D(t*G2). This gives72 affine rational unknowns, not a nonlinear search.
Optional scalar q*Id denominator adds a73rd unknown d, already explained
by the base certificate, and is tested separately only when requested.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import time

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'


def add(a,b,c):
    for j,x in b.items():
        a[j]=a.get(j,Q(0))+c*x
        if not a[j]:del a[j]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base',type=Path,required=True)
    ap.add_argument('--max-seconds',type=float,default=120)
    ap.add_argument('--include-scalar-linear',action='store_true')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    base=json.loads(args.base.read_text())
    chartpath=OLD/'data/fixed_chart.json'
    blockpath=OLD/'data/equivariant_blocks_QQ.json'
    chart=json.loads(chartpath.read_text())
    blockdata=json.loads(blockpath.read_text())
    for f in [chartpath,blockpath]:
        assert base['input_sha256'][str(f.relative_to(REPO))]==hashlib.sha256(f.read_bytes()).hexdigest()
    t=[Q(a) for a in base['tangent']]
    equations0=[[Q(a) for a in row] for row in base['affine_equations_coefficients_then_constant']]
    assert all(len(row)==23 for row in equations0)
    F=[tuple(s.count(c) for c in chart['variables']) for s in chart['F0']]
    perms=[[chart['variables'].index(c) for c in g] for g in chart['group_images']]
    def act(m,p):
        n=[0]*8
        for i,a in enumerate(m):n[p[i]]=a
        return tuple(n)
    actions=[[F.index(act(m,p)) for m in F] for p in perms]
    pairs=set(product(range(16),repeat=2));orbits=[]
    while pairs:
        i,j=min(pairs)
        orbit=sorted({(p[i],p[j]) for p in actions})
        orbits.append(orbit);pairs.difference_update(orbit)
    assert len(orbits)==51
    tangent_polys=[{} for _ in range(16)]
    for a,O in zip(t,chart['coefficient_orbits']):
        if a:
            for i,m in O:tangent_polys[i][tuple(m)]=a
    D=[];labels=[]
    for kind,block in blockdata['blocks'].items():
        for i,row in enumerate(block['D']):
            for j,cell in enumerate(row):D.append({int(k):Q(a) for k,a in cell});labels.append([kind,i,j])
    assert labels==base['equation_locations'] and len(D)==1160
    columns=[];coefficient_vectors=[]
    for k,orbit in enumerate(orbits):
        assert time.monotonic()-started<args.max_seconds,'internal time limit'
        v=[{} for _ in range(16)]
        for i,j in orbit:add(v[j],tangent_polys[i],Q(1))
        z=[]
        for O in chart['coefficient_orbits']:
            vals={v[i].get(tuple(m),Q(0)) for i,m in O}
            assert len(vals)==1
            z.append(vals.pop())
        coefficient_vectors.append(z)
        col=[sum(a*z[j] for j,a in row.items()) for row in D]
        columns.append(col)
        print('G2_ORBIT',k+1,'PAIRS',len(orbit),'D_TG_NONZERO',sum(bool(a) for a in col),flush=True)
    equations=[[row[j] for j in range(21)]+[col[i] for col in columns]+[row[-2],row[-1]]
               for i,row in enumerate(equations0)]
    # The last two columns are optional scalar-linear d and constant.
    cases=[]
    for nvars in ([72,73] if args.include_scalar_linear else [72]):
        eqs=[row[:nvars]+[row[-1]] for row in equations]
        echelon={};contradiction=None
        for i,eq in enumerate(eqs):
            row={j:a for j,a in enumerate(eq) if a};combo={i:Q(1)}
            for pivot in sorted(echelon):
                if pivot not in row:continue
                a=row[pivot];old,tr=echelon[pivot]
                add(row,old,-a);add(combo,tr,-a)
            if not row:continue
            pivot=min(row);a=row[pivot]
            if pivot==nvars:
                check=[sum(w*eqs[j][k] for j,w in combo.items()) for k in range(nvars+1)]
                assert check==[Q(0)]*nvars+[a]
                contradiction={'original_equation_combination':[[j,str(w)] for j,w in sorted(combo.items())],
                               'zero_variable_coefficients':True,'nonzero_constant':str(a),
                               'trigger_row':i,'trigger_location':labels[i],
                               'same_combination_applied_to_scalar_d_column':str(sum(w*equations[j][72] for j,w in combo.items()))}
                break
            echelon[pivot]=({j:v/a for j,v in row.items()},{j:v/a for j,v in combo.items()})
        solution=None
        if contradiction is None:
            free_parameters=[j for j in range(nvars) if j not in echelon]
            vectors=[]
            for chosen in [None]+free_parameters:
                x=[Q(0)]*nvars
                if chosen is not None:x[chosen]=Q(1)
                for pivot in sorted(echelon,reverse=True):
                    row,_=echelon[pivot]
                    x[pivot]=-sum(a*x[j] for j,a in row.items() if j<nvars and j!=pivot)
                    if chosen is None:x[pivot]-=row.get(nvars,Q(0))
                assert all(sum(a*b for a,b in zip(eq[:nvars],x))+(eq[-1] if chosen is None else 0)==0 for eq in eqs)
                vectors.append(x)
            solution={'free_parameter_indices':free_parameters,
                      'particular':[str(a) for a in vectors[0]],
                      'directions':[[str(a) for a in v] for v in vectors[1:]]}
        cases.append({'number_unknowns':nvars,
                      'status':'FAILED_exact_Q_contradiction' if contradiction else 'PASS_necessary_order_three_only',
                      'elimination_pivots':list(echelon),'contradiction':contradiction,'affine_solution':solution})
        print('EXACT_Q3_MATRIX',nvars,'INCONSISTENT' if contradiction else 'COMPATIBLE',flush=True)
        if contradiction:print('CONTRADICTION',json.dumps(contradiction),flush=True)
    result={'status':'COMPUTER-CERTIFIED exact rational matrix-denominator necessary test',
            'field':'Q','first_tangent':'original source normalized tangent',
            'generator_matrix_endomorphism_dimension':51,
            'endomorphism_basis_pair_orbits_zero_based_source_target':orbits,
            'normalized_tG2_coefficients':[[str(a) for a in z] for z in coefficient_vectors],
            'equation_column_order':'21 second-order tangent freedoms,51 generator-matrix G2 coefficients,optional scalar-linear d,constant',
            'equation_formula':'C(t)B(z2)+C(z2)B(t)-C(t)A0(t)B(t)+D(t*G2)+d*C(t)B(t)=0',
            'rational_form':'z=(q*t+q^2*(z2+d*t))*(Id+d*q*Id+q^2*G2)^(-1); d=0 in72variable case',
            'equations':[[str(a) for a in row] for row in equations],
            'equation_locations':labels,'cases':cases,
            'limitation':'Necessary through orderthree only; full closure and smoothness need separate verification for every surviving candidate.',
            'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [args.base.resolve(),chartpath,blockpath,Path(__file__)]},
            'seconds':time.monotonic()-started}
    (out/'matrix_denominator_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SECONDS',time.monotonic()-started,flush=True)


if __name__=='__main__':main()
