#!/usr/bin/env python3
"""Fixed exact two-jet, arbitrary linear/quadratic generator matrices.

For z2 fixed to the inherited normalized coefficient, try
z=(q*t+q^2*(z2+t*G1))*(Id+q*G1+q^2*G2)^(-1).
The q3 coefficient is -z2*G1-t*G2. Thus all51+51 equivariant entries
give a102-variable affine rational necessary test. No extra coefficient
search, jet extension, or all-orders claim is made by this script.
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
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    def gate():assert time.monotonic()-started<args.max_seconds,'internal time limit'
    base=json.loads(args.base.read_text())
    chartpath=OLD/'data/fixed_chart.json';blockpath=OLD/'data/equivariant_blocks_QQ.json'
    chart=json.loads(chartpath.read_text());blockdata=json.loads(blockpath.read_text())
    for f in [chartpath,blockpath]:
        assert base['input_sha256'][str(f.relative_to(REPO))]==hashlib.sha256(f.read_bytes()).hexdigest()
    t=[Q(a) for a in base['tangent']]
    z2=[Q(a) for a in base['particular_second_coefficient']]
    constants=[Q(row[-1]) for row in base['affine_equations_coefficients_then_constant']]
    F=[tuple(s.count(c) for c in chart['variables']) for s in chart['F0']]
    perms=[[chart['variables'].index(c) for c in g] for g in chart['group_images']]
    def act(m,p):
        n=[0]*8
        for i,a in enumerate(m):n[p[i]]=a
        return tuple(n)
    actions=[[F.index(act(m,p)) for m in F] for p in perms]
    pairs=set(product(range(16),repeat=2));orbits=[]
    while pairs:
        i,j=min(pairs);orbit=sorted({(p[i],p[j]) for p in actions})
        orbits.append(orbit);pairs.difference_update(orbit)
    assert len(orbits)==51
    D=[];labels=[]
    for kind,block in blockdata['blocks'].items():
        for i,row in enumerate(block['D']):
            for j,cell in enumerate(row):D.append({int(k):Q(a) for k,a in cell});labels.append([kind,i,j])
    assert labels==base['equation_locations'] and len(D)==1160
    allcols=[];allvectors=[]
    for prefix,coefficients in [('G1',z2),('G2',t)]:
        polys=[{} for _ in range(16)]
        for a,O in zip(coefficients,chart['coefficient_orbits']):
            if a:
                for i,m in O:polys[i][tuple(m)]=a
        for k,orbit in enumerate(orbits):
            gate();v=[{} for _ in range(16)]
            for i,j in orbit:add(v[j],polys[i],Q(1))
            z=[]
            for O in chart['coefficient_orbits']:
                vals={v[i].get(tuple(m),Q(0)) for i,m in O}
                assert len(vals)==1
                z.append(vals.pop())
            allvectors.append(z)
            col=[sum(a*z[j] for j,a in row.items()) for row in D]
            allcols.append(col)
            print('MATRIX_COLUMN',prefix,k+1,'NONZERO',sum(bool(a) for a in col),flush=True)
    assert len(allcols)==102
    equations=[[col[i] for col in allcols]+[constants[i]] for i in range(1160)]
    nvars=102;echelon={};contradiction=None
    for i,eq in enumerate(equations):
        gate();row={j:a for j,a in enumerate(eq) if a};combo={i:Q(1)}
        for pivot in sorted(echelon):
            if pivot not in row:continue
            a=row[pivot];old,tr=echelon[pivot]
            add(row,old,-a);add(combo,tr,-a)
        if not row:continue
        pivot=min(row);a=row[pivot]
        if pivot==nvars:
            check=[sum(w*equations[j][k] for j,w in combo.items()) for k in range(nvars+1)]
            assert check==[Q(0)]*nvars+[a]
            contradiction={'original_equation_combination':[[j,str(w)] for j,w in sorted(combo.items())],
                           'zero_variable_coefficients':True,'nonzero_constant':str(a),
                           'trigger_row':i,'trigger_location':labels[i]}
            break
        echelon[pivot]=({j:v/a for j,v in row.items()},{j:v/a for j,v in combo.items()})
    solution=None
    if contradiction is None:
        free_parameters=[j for j in range(nvars) if j not in echelon];vectors=[]
        for chosen in [None]+free_parameters:
            gate();x=[Q(0)]*nvars
            if chosen is not None:x[chosen]=Q(1)
            for pivot in sorted(echelon,reverse=True):
                row,_=echelon[pivot]
                x[pivot]=-sum(a*x[j] for j,a in row.items() if j<nvars and j!=pivot)
                if chosen is None:x[pivot]-=row.get(nvars,Q(0))
            assert all(sum(a*b for a,b in zip(eq[:nvars],x))+(eq[-1] if chosen is None else 0)==0 for eq in equations)
            vectors.append(x)
        solution={'free_parameter_indices':free_parameters,
                  'particular':[str(a) for a in vectors[0]],
                  'directions':[[str(a) for a in v] for v in vectors[1:]]}
    result={'status':'FAILED_exact_Q_order_three_contradiction' if contradiction else 'COMPUTER-CERTIFIED affine solution space; all-orders closure OPEN',
            'field':'Q','scope':'original exact first AND second normalized coefficients fixed; arbitrary51-dimensional G1 and G2',
            'endomorphism_basis_pair_orbits_zero_based_source_target':orbits,
            'normalized_z2G1_then_tG2_vectors':[[str(a) for a in z] for z in allvectors],
            'equation_column_order':'51 G1 entries,51 G2 entries,constant',
            'equation_formula':'C(t)B(z2)+C(z2)B(t)-C(t)A0(t)B(t)+D(z2*G1)+D(t*G2)=0',
            'rational_form':'z=(q*t+q^2*(z2+t*G1))*(Id+q*G1+q^2*G2)^(-1)',
            'raw_polynomial_generators':'Fraw=F0*(Id+q*G1+q^2*G2)+q*T+q^2*(Z2+T*G1)',
            'equations':[[str(a) for a in row] for row in equations],
            'equation_locations':labels,'elimination_pivots':list(echelon),
            'contradiction':contradiction,'affine_solution':solution,
            'limitation':'An exact contradiction excludes this fixed-twojet quadratic raw-generator ansatz over every characteristic-zero extension. A surviving affine solution has passed only orderthree and still needs full defining identities and smoothness.',
            'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [args.base.resolve(),chartpath,blockpath,Path(__file__)]},
            'seconds':time.monotonic()-started}
    (out/'linear_matrix_denominator_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('EXACT_Q3_102','INCONSISTENT' if contradiction else 'COMPATIBLE','PIVOTS',len(echelon),flush=True)
    if contradiction:print('CONTRADICTION',json.dumps(contradiction),flush=True)
    print('SECONDS',time.monotonic()-started,flush=True)


if __name__=='__main__':main()
