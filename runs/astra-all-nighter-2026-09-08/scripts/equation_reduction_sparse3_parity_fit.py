#!/usr/bin/env python3
"""Small untested algebraic fits on sparse3 after an exact parity reduction.

No jet extension. No model certification. Checks the exact first-direction
involution and the existing 32-jet, then fits bivariate polynomial relations
with >=4 holdout equations and forbids zero monomial columns. Runnable by
the root's resource guard; all source packets remain immutable.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import time

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
OLD = RUN.parent / 'astra-computation-2026-09-08'


def kernel(matrix,p):
    a = [r[:] for r in matrix]
    nr,nc = len(a),len(a[0])
    pivots = []
    for col in range(nc):
        j = next((j for j in range(len(pivots),nr) if a[j][col]), None)
        if j is None: continue
        i = len(pivots)
        a[i],a[j] = a[j],a[i]
        inv = pow(a[i][col],-1,p)
        a[i] = [x*inv%p for x in a[i]]
        for j in range(nr):
            if i != j and a[j][col]:
                c = a[j][col]
                a[j] = [(x-c*y)%p for x,y in zip(a[j],a[i])]
        pivots.append(col)
    null = []
    for col in range(nc):
        if col in pivots: continue
        v = [0]*nc
        v[col] = 1
        for row,i in enumerate(pivots): v[i] = -a[row][col]%p
        assert all(sum(x*y for x,y in zip(r,v))%p == 0 for r in matrix)
        null.append(v)
    return pivots,null


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    started=time.monotonic()
    pointpath = OLD/'logs/20260908T125753-sparse3-curve-32.artifacts/sparse3_curve_p101_order32.json'
    dirpath = OLD/'data/sparse3_direction_exact.json'
    chartpath = OLD/'data/fixed_chart.json'
    pt=json.loads(pointpath.read_text())
    direction=json.loads(dirpath.read_text())
    chart=json.loads(chartpath.read_text())
    p=pt['prime']
    assert p==101 and pt['order']==32
    weights=[0,0,0,1,0,1,0,0,1]
    assert all(sum(x*y for x,y in zip(row,weights))%2==0 for row in direction['weight_equations'])
    for permutation in chart['group_images']:
        assert all(weights[i]==weights['abcdefgh'.index(permutation[i])] for i in range(8))
    F=[tuple(s.count(c) for c in 'abcdefgh') for s in chart['F0']]
    parities=[]
    for O in chart['coefficient_orbits']:
        eps={sum((m[k]-F[i][k])*weights[k] for k in range(8))%2 for i,m in O}
        assert len(eps)==1
        parities.append(eps.pop())
    z=pt['z_coefficients']
    assert all(not row[j] or n%2==parities[j] for n,row in enumerate(z) for j in range(291))
    free=chart['free_coordinates']
    assert all(not z[1][j] or parities[j]==1 for j in free)
    assert all(z[n][j]==0 for n in range(2,len(z)) for j in free)
    attempts=[]
    # All three dependent valuation-one coordinates and the first two of
    # valuation two. This fixed set is declared before any fitting.
    coordinates=[7,101,109,35,39]
    for j in coordinates:
        valuation=next(n for n,row in enumerate(z) if row[j])
        assert valuation in [1,2]
        raw=[z[n][j] for n in range(valuation,len(z),2)]
        for normalization in ['remove_initial_q_power','remove_initial_q_power_then_constant_and_s_power']:
            series=raw[:]
            s_power_removed=0
            if normalization.endswith('_and_s_power'):
                series[0]=0
                s_power_removed=next(k for k,a in enumerate(series) if a)
                series=series[s_power_removed:]
            n=len(series)
            def multiply(a,b):
                return [sum(a[i]*b[k-i] for i in range(k+1))%p for k in range(n)]
            powers=[[1]+[0]*(n-1)]
            for degree in range(1,5):powers.append(multiply(powers[-1],series))
            for dt,ds in [(2,2),(2,3),(3,2),(4,1)]:
                mons=list(product(range(dt+1),range(ds+1)))
                record={'coordinate_zero_based':j,'q_valuation_removed':valuation,
                        's_valuation_removed_after_constant':s_power_removed,
                        'normalization':normalization,'series_s_coefficients':series,
                        'degree_T':dt,'degree_s':ds,'monomials_T_s':mons,
                        'number_equations':n,'number_unknowns':len(mons)}
                if len(mons)+4>n:
                    record['status']='SKIPPED_insufficient_holdout'
                    attempts.append(record);continue
                cols=[[0]*s+powers[t][:n-s] for t,s in mons]
                if any(not any(c) for c in cols):
                    record['status']='SKIPPED_zero_monomial_column'
                    attempts.append(record);continue
                M=[[col[i] for col in cols] for i in range(n)]
                pivots,null=kernel(M,p)
                record.update(rank=len(pivots),nullity=len(null),kernel_basis=null,
                              status='HEURISTIC_modular_relation_candidates' if null else 'FAILED_within_declared_support')
                attempts.append(record)
                print('FIT',j,normalization,dt,ds,'RANK',len(pivots),'NULLITY',len(null),flush=True)
    result={'status':'parity COMPUTER-CERTIFIED; algebraic candidates require exact identity verification',
            'prime':p,'involution_weights_a_to_h_q':weights,'coordinate_parities':parities,
            'scope':'sparse3 alternate linear-free path only; no original sixjet smoothness transfer',
            'root_uniqueness_argument':'The diagonal involution commutes with S3, preserves the normalized coefficient chart and its free/dependent split, and sends each prescribed free coefficient q*t_j to itself when q is negated. Uniqueness of the origin-selected solution forces the parity identity in characteristic zero and characteristic101.',
            'attempts':attempts,'seconds':time.monotonic()-started,
            'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [pointpath,dirpath,chartpath,Path(__file__)]}}
    (out/'parity_fit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('CANDIDATE_TESTS',sum(a.get('nullity',0)>0 for a in attempts), 'SECONDS',time.monotonic()-started)


if __name__=='__main__':main()
