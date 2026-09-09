#!/usr/bin/env python3
"""Exact order-three tests for optimized polynomial and rational paths.

The original first tangent is fixed. Every possible second coefficient is
z2=z2_original+ker(D), with all21 invariant embedded tangent directions.
For z=q*t+q^2*z2, the q^3 Schur equation is affine-linear in those21
parameters. Also tests numerator degree2, denominator1 by adding one scalar
d with z3=-d*z2; its q3 term is d*D(z2), where D(z2)=C(t)B(t) is fixed.
Produces exact rational contradictions or complete affine solution spaces.
Neither finite closure nor smoothness is inferred from passing this test.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode=True
RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'
sys.path.insert(0,str(OLD/'scripts'))
from fixed_curve_lift import normalized_jet


def mm(a,b):
    out=[[Q(0)]*len(b[0]) for _ in a]
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if not x:continue
            for j,y in enumerate(b[k]):
                if y:out[i][j]+=x*y
    return out


def madd(a,b,c=Q(1)):
    return [[x+c*y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]


def sparse_add(a,b,c):
    for j,x in b.items():
        a[j]=a.get(j,Q(0))+c*x
        if not a[j]:del a[j]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pilot',type=Path,default=RUN/'data/linear_u_locus_p101/necessary_locus.json')
    ap.add_argument('--max-seconds',type=float,default=120)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    def gate():assert time.monotonic()-started<args.max_seconds,'internal time limit'
    chartpath=OLD/'data/fixed_chart.json'
    blockpath=OLD/'data/equivariant_blocks_QQ.json'
    sourcepath=REPO/'equations/deformation_data.json'
    chart=json.loads(chartpath.read_text())
    blockdata=json.loads(blockpath.read_text())
    pilot=json.loads(args.pilot.read_text())
    for f in [chartpath,blockpath,sourcepath]:
        assert pilot['input_sha256'][str(f.relative_to(REPO))]==hashlib.sha256(f.read_bytes()).hexdigest()
    jet,_=normalized_jet(chart)
    t,z2=jet[1:3]
    basis=[[Q(a) for a in z] for z in pilot['exact_tangent_vectors']]
    names=['intrinsic_orbit_'+str(i+1) for i in range(10)]
    V=chart['variables']
    perms=[[V.index(c) for c in g] for g in chart['group_images']]
    pairs=set(product(range(8),repeat=2));orbits=[]
    while pairs:
        a,b=min(pairs)
        orbit=sorted({(perm[a],perm[b]) for perm in perms})
        orbits.append(orbit);pairs.difference_update(orbit)
    F=[tuple(s.count(c) for c in V) for s in chart['F0']]
    tails=set(map(tuple,chart['tail_monomials']))
    for orbit in orbits:
        poly={}
        for a,b in orbit:
            for i,m in enumerate(F):
                if not m[a]:continue
                n=list(m);n[a]-=1;n[b]+=1;n=tuple(n)
                if n in tails:poly[i,n]=poly.get((i,n),Q(0))+m[a]
        if not poly:continue
        z=[]
        for O in chart['coefficient_orbits']:
            values={poly.get((i,tuple(m)),Q(0)) for i,m in O}
            assert len(values)==1
            z.append(values.pop())
        basis.append(z)
        names.append('coordinate_orbit_'+','.join(V[a]+V[b] for a,b in orbit))
    assert len(basis)==21
    # A unit coordinate submatrix proves these directions span the entire
    # 21-dimensional tangent, whose dimension is already certified by the
    # chart's constant-Jacobian rank270.
    free=chart['free_coordinates']
    projected=[[b[j] for j in free] for b in basis]
    assert all(sum(bool(a) for a in row)==1 and sum(row)==1 for row in projected)
    assert all(sum(bool(projected[i][j]) for i in range(21))==1 for j in range(21))
    assert all(sum(Q(a)*b[j] for j,a in row)==0 for b in basis for row in chart['linear_rows'])
    blocks={}
    for kind,block in blockdata['blocks'].items():
        blocks[kind]={name:[[{int(j):Q(a) for j,a in cell} for cell in row] for row in block[name]]
                      for name in ['A_minus_identity','B','C','D']}
    def evaluate(z):
        return {kind:{name:[[sum(a*z[j] for j,a in cell.items()) for cell in row] for row in mat]
                      for name,mat in block.items()} for kind,block in blocks.items()}
    e1=evaluate(t);e2=evaluate(z2)
    constants=[];labels=[];denominator_column=[]
    for kind in blocks:
        b1=e1[kind]['B'];c1=e1[kind]['C'];a1=e1[kind]['A_minus_identity']
        assert not any(x for row in e1[kind]['D'] for x in row)
        assert e2[kind]['D']==mm(c1,b1)
        denominator_column.extend(x for row in e2[kind]['D'] for x in row)
        u2=madd(e2[kind]['B'],mm(a1,b1),Q(-1))
        q3=madd(mm(c1,u2),mm(e2[kind]['C'],b1))
        for i,row in enumerate(q3):
            for j,x in enumerate(row):constants.append(x);labels.append([kind,i,j])
    assert len(constants)==1160
    columns=[]
    for n,b in enumerate(basis):
        gate();eb=evaluate(b);col=[]
        for kind in blocks:
            assert not any(x for row in eb[kind]['D'] for x in row)
            mat=madd(mm(e1[kind]['C'],eb[kind]['B']),mm(eb[kind]['C'],e1[kind]['B']))
            col.extend(x for row in mat for x in row)
        assert len(col)==1160
        columns.append(col)
        print('Q3_FREE_COLUMN',n+1,'NONZERO',sum(bool(x) for x in col),flush=True)
    columns.append(denominator_column)
    equations=[[col[i] for col in columns]+[constants[i]] for i in range(1160)]
    cases=[]
    for nvars,ansatz in [(21,'z(q)=q*t+q^2*z2'),
                         (22,'z(q)=(q*t+q^2*(z2+d*t))/(1+d*q)')]:
        eqs=[row[:nvars]+[row[-1]] for row in equations]
        echelon={};contradiction=None
        for i,eq in enumerate(eqs):
            row={j:a for j,a in enumerate(eq) if a};combo={i:Q(1)}
            for pivot in sorted(echelon):
                if pivot not in row:continue
                a=row[pivot];old,tr=echelon[pivot]
                sparse_add(row,old,-a);sparse_add(combo,tr,-a)
            if not row:continue
            pivot=min(row);a=row[pivot]
            if pivot==nvars:
                check=[sum(w*eqs[j][k] for j,w in combo.items()) for k in range(nvars+1)]
                assert check==[Q(0)]*nvars+[a]
                contradiction={'original_equation_combination':[[j,str(w)] for j,w in sorted(combo.items())],
                               'zero_variable_coefficients':True,'nonzero_constant':str(a),
                               'trigger_row':i,'trigger_location':labels[i]}
                break
            echelon[pivot]=({j:v/a for j,v in row.items()},{j:v/a for j,v in combo.items()})
        solution=None
        if contradiction is None:
            free_parameters=[j for j in range(nvars) if j not in echelon]
            vectors=[]
            for free_choice in [None]+free_parameters:
                x=[Q(0)]*nvars
                if free_choice is not None:x[free_choice]=Q(1)
                for pivot in sorted(echelon,reverse=True):
                    row,_=echelon[pivot]
                    x[pivot]=-sum(a*x[j] for j,a in row.items() if j<nvars and j!=pivot)
                    if free_choice is None:x[pivot]-=row.get(nvars,Q(0))
                assert all(sum(a*b for a,b in zip(eq[:nvars],x))+(eq[nvars] if free_choice is None else 0)==0
                           for eq in eqs)
                vectors.append(x)
            solution={'free_parameter_indices':free_parameters,
                      'particular':[str(a) for a in vectors[0]],
                      'directions':[[str(a) for a in v] for v in vectors[1:]]}
        cases.append({'ansatz':ansatz,'number_affine_unknowns':nvars,
                      'status':'FAILED_exact_Q_contradiction' if contradiction else 'PASS_necessary_order_three_only',
                      'elimination_pivots':list(echelon),
                      'contradiction':contradiction,'affine_solution':solution})
        print('EXACT_Q3',nvars,'INCONSISTENT' if contradiction else 'COMPATIBLE',
              'PIVOTS',len(echelon),flush=True)
        if contradiction:print('CONTRADICTION',json.dumps(contradiction),flush=True)
    result={'status':'COMPUTER-CERTIFIED exact rational order-three optimization tests',
            'field':'Q','scope':'original first tangent; all21 second-order freedoms; optional scalar linear denominator',
            'tangent':[str(a) for a in t],'particular_second_coefficient':[str(a) for a in z2],
            'second_coefficient_kernel_basis':[[str(a) for a in b] for b in basis],
            'basis_labels':names,'all_order_two_Schur_equations_zero':True,
            'equation_formula':'C(t)*(B(z2)-A0(t)*B(t))+C(z2)*B(t)+d*D(z2)=0, D(z2)=C(t)B(t) fixed',
            'equation_column_order':'21 second-order kernel freedoms, denominator d, constant',
            'affine_equations_coefficients_then_constant':[[str(a) for a in row] for row in equations],
            'equation_locations':labels,'cases':cases,
            'interpretation':'Each exact contradiction excludes its entire optimized ansatz over every characteristic-zero extension. Otherwise only compatibility through orderthree is established.',
            'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [chartpath,blockpath,sourcepath,args.pilot.resolve(),Path(__file__),OLD/'scripts/fixed_curve_lift.py']},
            'seconds':time.monotonic()-started}
    (out/'quadratic_generator_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SECONDS',time.monotonic()-started,flush=True)


if __name__=='__main__':main()
