#!/usr/bin/env python3
"""One authorized alternate direction: S3 orbit weights 3=8=10=1.

Linear paths in the 21 free chart coordinates; dependent coefficients
are solved exactly using the existing constant270 minor. This changes
the first tangent, not merely higher jets. No six-jet smoothness claim.
Every order is checkpointed with actual helper/input hashes. Hard limit32.
"""
import argparse, hashlib, json, os, sys, time
from fractions import Fraction as Q
from pathlib import Path
sys.dont_write_bytecode = True
from build_fixed_chart import F0, times
from fixed_curve_lift import lu_factor, lu_solve
from check_rational_closure import build_identity_operator

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
DIRECTION = 'S3_orbits_3_8_10_unit_linear_free'


def input_hashes():
    paths = [RUN/'data/fixed_chart.json', RUN/'data/sparse3_direction_exact.json',
             REPO/'equations/deformation_data.json', Path(__file__),
             RUN/'scripts/fixed_curve_lift.py', RUN/'scripts/check_rational_closure.py',
             RUN/'scripts/build_fixed_chart.py', RUN/'scripts/check_sparse_direction_weights.py']
    return {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def origin(chart):
    columns = [tuple(c) for c in chart['multiplication_columns']]
    monomials = [tuple(m) for m in chart['pivot_monomials']]
    u0 = [[0]*30 for _ in range(98)]
    for k,c in enumerate(chart['extra_columns']):
        i,j = columns[c]
        u0[monomials.index(times(F0[i],j))][k] = 1
    return u0


def tangent(p):
    d = json.loads((RUN/'data/sparse3_direction_exact.json').read_text())
    assert d['direction']=='three-orbit-proposed'
    assert d['orbit_weights']==[0,0,1,0,0,0,0,1,0,1]
    assert d['weight_rank']==8 and d['same_product_minor_determinant']==-1
    assert d['all_6960_standard_linear_tangent_equations_zero']
    assert not d['preserves_bad_B_grading']
    assert d['source_sha256']==hashlib.sha256((REPO/'equations/deformation_data.json').read_bytes()).hexdigest()
    assert d['chart_sha256']==hashlib.sha256((RUN/'data/fixed_chart.json').read_bytes()).hexdigest()
    return [Q(a).numerator*pow(Q(a).denominator,-1,p)%p for a in d['chart_tangent_z']]


def validate_sparse_checkpoint(state,chart):
    p,N = state['prime'],state['order']
    assert p>3 and all(p%d for d in range(2,int(p**.5)+1))
    assert 1<=N<=32 and state['direction']==DIRECTION and state['free_path_order']==1
    assert state['input_hashes']==input_hashes()
    assert state['free_coordinates']==chart['free_coordinates']
    zs,us = state['z_coefficients'],state['U_coefficients']
    assert len(zs)==len(us)==N+1
    assert all(len(z)==291 for z in zs)
    assert all(len(u)==98 and all(len(row)==30 for row in u) for u in us)
    assert all(isinstance(a,int) and 0<=a<p for z,u in zip(zs,us) for a in z+[a for row in u for a in row])
    assert zs[0]==[0]*291 and us[0]==origin(chart)
    assert zs[1]==tangent(p)
    assert all(zs[n][j]==0 for n in range(2,N+1) for j in chart['free_coordinates'])
    assert state['all_schur_equations_verified_through']==N
    return p,N,zs,us


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--order',type=int,choices=range(1,33),default=24)
    ap.add_argument('--prime',type=int,default=101)
    ap.add_argument('--resume',type=Path)
    args=ap.parse_args(); p=args.prime
    assert p>3 and all(p%d for d in range(2,int(p**.5)+1))
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    t=tangent(p); dep=chart['dependent_coordinates']; free=chart['free_coordinates']
    selected=[30*i+j for i,j in chart['independent_equations']]
    jrows=[dict(row) for row in chart['linear_rows']]
    lu=lu_factor([[jrows[i].get(j,0)%p for j in dep] for i in selected],p)
    lin,edges=build_identity_operator(chart)
    lin=[{j:a for j,a in row.items() if a} for row in lin]
    assert lin[98*30:]==jrows
    def multiply(z,u):
        out=[[0]*30 for _ in range(330)]
        for r,c,j in edges:
            if z[j]:
                for k,b in enumerate(u[c]):
                    if b: out[r][k]+=z[j]*b
        return [[a%p for a in row] for row in out]
    zs=[[0]*291]; us=[origin(chart)]
    if args.resume:
        previous=json.loads(args.resume.read_text())
        rp,_,zs,us=validate_sparse_checkpoint(previous,chart)
        assert rp==p
    output=Path(os.environ['GS_RUN_OUTPUT']).resolve()
    assert output.is_relative_to(RUN)
    output.mkdir(parents=True,exist_ok=True)
    hashes=input_hashes(); started=time.monotonic()
    for n in range(len(zs),args.order+1):
        cross=[[0]*30 for _ in range(330)]
        for i in range(1,n):
            prod=multiply(zs[i],us[n-i])
            for r in range(330): cross[r]=[(a+b)%p for a,b in zip(cross[r],prod[r])]
        z=[0]*291
        if n==1:
            for j in free: z[j]=t[j]
        rhs=[(cross[98+i//30][i%30]-sum(a*z[j] for j,a in jrows[i].items()))%p for i in selected]
        solution=lu_solve(lu,rhs,p)
        for j,a in zip(dep,solution): z[j]=a
        linear=[sum(a*z[j] for j,a in row.items())%p for row in lin]
        un=[[(linear[30*r+k]-cross[r][k])%p for k in range(30)] for r in range(98)]
        residual=[(linear[30*r+k]-cross[r][k])%p for r in range(98,330) for k in range(30)]
        assert not any(residual),('nonzero full Schur coefficient',n,next(i for i,a in enumerate(residual) if a))
        if n==1: assert z==t
        zs.append(z); us.append(un)
        state={'prime':p,'order':n,'direction':DIRECTION,'free_path_order':1,
               'curve_definition':'free chart paths linear; alternate orbit weights3=8=10=1',
               'free_coordinates':free,'input_hashes':hashes,
               'z_coefficients':zs,'U_coefficients':us,'all_schur_equations_verified_through':n,
               'matches_selected_normalized_firstjet':False,'matches_selected_normalized_sixjet':False,
               'smoothness_certified':False,
               'status':'COMPUTER-CERTIFIED finite jet only; closure and smoothness unproved'}
        dest=output/f'sparse3_curve_p{p}_order{n}.json'
        with dest.open('x') as stream: json.dump(state,stream); stream.write('\n')
        print('ORDER',n,'ALL_6960_SCHUR_ZERO','Z_NONZERO',sum(bool(a) for a in z),
              'U_NONZERO',sum(bool(a) for row in un for a in row),
              'seconds',round(time.monotonic()-started,3),flush=True)
    print('NO_SIXJET_SMOOTHNESS_INHERITANCE')
    print('NO_CLOSURE_CLAIM')


if __name__=='__main__': main()
