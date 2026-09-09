#!/usr/bin/env python3
"""Raw polynomial generators of degree3..5 inq with optimized matrix bases.

Preserve the original normalizedD-jet. A raw degreeD row and basis matrix
P=Id+qG1+...+q^D GD force z_(D+1)=-sum z_i G_(D+1-i).
The next lower Schur coefficient is therefore a constant rational linear
test, with51D unknowns. Stop at the first compatible degree; do not infer
full flatness from that test.
"""
import argparse
from fractions import Fraction as Q
import hashlib
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


def add(a,b,c):
    for j,x in b.items():
        a[j]=a.get(j,Q(0))+c*x
        if not a[j]:del a[j]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=240)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    start=time.monotonic();out=a.output.resolve();assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    def gate():assert time.monotonic()-start<a.seconds,'internal time gate'
    paths=[OLD/'data/fixed_chart.json',OLD/'data/equivariant_blocks_QQ.json',
           RUN/'data/linear_matrix_denominator/linear_matrix_denominator_certificate.json',
           REPO/'equations/deformation_data.json',OLD/'scripts/fixed_curve_lift.py',Path(__file__)]
    chart,blocks,old=[json.loads(p.read_text()) for p in paths[:3]]
    jet,_=normalized_jet(chart);basis=old['endomorphism_basis_pair_orbits_zero_based_source_target'];assert len(basis)==51
    rows=[];labels=[]
    for kind,b in blocks['blocks'].items():
        for i,row in enumerate(b['D']):
            for j,cell in enumerate(row):rows.append({k:Q(c) for k,c in cell});labels.append([kind,i,j])
    def applyD(z):return [sum(c*z[j] for j,c in row.items()) for row in rows]
    # Previousexact two-order pencil is an independently cross-checked input.
    cache={1:[],2:[]}
    previous=[[Q(x) for x in row] for row in old['normalized_z2G1_then_tG2_vectors']]
    for i,z in enumerate(previous):cache[2 if i<51 else 1].append(applyD(z))
    assert [cache[2][j][i] for j in range(51) for i in [8]] == [Q(old['equations'][8][j]) for j in range(51)]
    assert applyD(jet[3])==[Q(row[-1]) for row in old['equations']]
    hashes={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    summaries=[]
    for degree in [3,4,5]:
        gate();polys=[{} for _ in range(16)]
        for c,orb in zip(jet[degree],chart['coefficient_orbits']):
            if c:
                for i,m in orb:polys[i][tuple(m)]=c
        cache[degree]=[]
        for orb in basis:
            v=[{} for _ in range(16)]
            for i,j in orb:add(v[j],polys[i],Q(1))
            z=[]
            for O in chart['coefficient_orbits']:
                vals={v[i].get(tuple(m),Q(0)) for i,m in O};assert len(vals)==1;z.append(vals.pop())
            cache[degree].append(applyD(z))
        columns=[col for k in range(degree,0,-1) for col in cache[k]]
        rhs=applyD(jet[degree+1]);nv=51*degree
        equations=[[col[i] for col in columns]+[rhs[i]] for i in range(len(rows))]
        ech={};contradiction=None
        for i,eq in enumerate(equations):
            gate();row={j:c for j,c in enumerate(eq) if c};combo={i:Q(1)}
            for j in sorted(ech):
                if j in row:
                    c=row[j];r,tr=ech[j];add(row,r,-c);add(combo,tr,-c)
            if not row:continue
            j=min(row);c=row[j]
            if j==nv:
                check=[sum(v*equations[k][j] for k,v in combo.items()) for j in range(nv+1)]
                assert check==[Q(0)]*nv+[c]
                contradiction={'rows':[[k,str(v)] for k,v in sorted(combo.items())],
                               'constant':str(c),'trigger_location':labels[i]};break
            ech[j]=({k:v/c for k,v in row.items()},{k:v/c for k,v in combo.items()})
        solution=None
        if contradiction is None:
            free=[j for j in range(nv) if j not in ech];vectors=[]
            for chosen in [None]+free:
                gate();x=[Q(0)]*nv
                if chosen is not None:x[chosen]=Q(1)
                for pivot in sorted(ech,reverse=True):
                    row,_=ech[pivot]
                    x[pivot]=-sum(c*x[j] for j,c in row.items() if j<nv and j!=pivot)
                    if chosen is None:x[pivot]-=row.get(nv,Q(0))
                assert all(sum(c*v for c,v in zip(row[:-1],x))+(row[-1] if chosen is None else 0)==0 for row in equations)
                vectors.append([str(v) for v in x])
            solution={'free_indices':free,'particular':vectors[0],'directions':vectors[1:]}
        result={'status':'FAILED_exact_rational_necessary_condition' if contradiction else 'COMPATIBLE_next_order_only',
                'degree':degree,'unknowns':nv,'field':'Q','preserves_original_normalized_jet_through':degree,
                'tested_order':degree+1,'equations':[[str(c) for c in row] for row in equations],
                'equation_locations':labels,'pivot_count':len(ech),'contradiction':contradiction,'affine_solution':solution,
                'basis_pair_orbits':basis,'formula':'D(sum_(i=1..D) z_i*G_(D+1-i) + source_z_(D+1))=0',
                'input_hashes':hashes,'elapsed_seconds':time.monotonic()-start}
        (out/f'degree{degree}.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
        summaries.append({k:result[k] for k in ['status','degree','unknowns','pivot_count','elapsed_seconds']})
        (out/'checkpoint_summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
        print('DEGREE',degree,'UNKNOWNS',nv,'PIVOTS',len(ech),result['status'],'SECONDS',time.monotonic()-start,flush=True)
        if not contradiction:break


if __name__=='__main__':main()
