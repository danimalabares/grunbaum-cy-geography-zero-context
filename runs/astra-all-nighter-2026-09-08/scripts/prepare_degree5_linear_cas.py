#!/usr/bin/env python3
"""Prepare the degree5 rational linear system for a different exact CAS method.

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
        if degree < 5: continue
        columns=[col for k in range(degree,0,-1) for col in cache[k]]
        rhs=applyD(jet[degree+1]);nv=51*degree
        equations=[[col[i] for col in columns]+[rhs[i]] for i in range(len(rows))]
        result={'field':'Q','degree':degree,'unknowns':nv,'equations':[[str(c) for c in row] for row in equations],
                'equation_locations':labels,'basis_pair_orbits':basis,'input_hashes':hashes,
                'status':'exact next-order linear system; no elimination run by this script','seconds':time.monotonic()-start}
        (out/'degree5_linear_system.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
        names=['x'+str(i+1) for i in range(nv)]
        def expr(row):
            terms=['('+str(c)+')*'+names[j] for j,c in enumerate(row[:-1]) if c]
            if row[-1]:terms.append('('+str(row[-1])+')')
            return '+'.join(terms) or '0'
        script=['ring r=0,('+','.join(names)+'),dp;',
                'ideal I='+',\n'.join(expr(row) for row in equations)+';',
                'ideal G=std(I);',
                'print("STANDARD_BASIS_DONE");',
                'if (reduce(1,G)==0) {',
                '  matrix T=lift(I,ideal(1));',
                '  matrix C=I*T;',
                '  if(C[1,1]==1) {',
                '    print("EXACT_UNIT_RELATION");',
                '    for(int j=1;j<=size(I);j++) {',
                '      if(T[j,1]!=0) { print("WITNESS="+string(j-1)+":"+string(T[j,1])); }',
                '    }',
                '  } else { print("FAILED_WITNESS"); }',
                '} else { print("COMPATIBLE_LINEAR_SYSTEM"); print(dim(G)); }',
                'quit;']
        (out/'degree5_linear_system.sing').write_text('\n'.join(script)+'\n')
        print('PREPARED_EXACT_Q_DEGREE5_LINEAR_SYSTEM',nv,len(equations),'SECONDS',time.monotonic()-start,flush=True)
        return


if __name__=='__main__':main()
