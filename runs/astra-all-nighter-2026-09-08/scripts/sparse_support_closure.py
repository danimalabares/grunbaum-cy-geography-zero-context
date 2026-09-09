#!/usr/bin/env python3
"""Exact sparse support closure for the quadratic implicit coefficient map.

Use a modular pilot, then rational arithmetic only if the pilot reduces the
state. No infinite vanishing is inferred from a finite jet.
"""
import argparse
import hashlib
import json
import os
import time
from fractions import Fraction as Q
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prime',type=int,default=101)
    ap.add_argument('--seconds',type=int,default=120)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();start=time.monotonic();p=a.prime
    out=a.output.resolve();assert out.is_relative_to(RUN) and not out.exists()
    def norm(x):return x%p if p else x
    def coeff(x):
        q=Q(x)
        return q.numerator*pow(q.denominator,-1,p)%p if p else q
    def inv(x):return pow(x,-1,p) if p else 1/x
    def add(x,y,c=1):
        for k,b in y.items():
            x[k]=norm(x.get(k,0)+c*b)
            if not x[k]:del x[k]
    def gate():assert time.monotonic()-start<a.seconds,'internal time gate'
    inputs=[OLD/'data/equivariant_blocks_QQ.json',OLD/'data/sparse3_direction_exact.json',Path(__file__)]
    data,direction=[json.loads(f.read_text()) for f in inputs[:-1]]
    dep=data['dependent_coordinates'];free=data['free_coordinates']
    blocks={};ids={};names=['z'+str(j+1) for j in range(291)]
    for kind,b in data['blocks'].items():
        ni,nk,nc=b['dimensions']
        ids[kind]=[[len(names)+i*nk+j for j in range(nk)] for i in range(ni)]
        names.extend('U_'+kind+'_'+str(i)+'_'+str(j) for i in range(ni) for j in range(nk))
        blocks[kind]={k:[[{j:coeff(c) for j,c in cell if coeff(c)} for cell in row] for row in b[k]]
                      for k in ['A_minus_identity','B','C','D']}
    assert len(names)==781
    # Every right side is a sparse quadratic in the OLD state coordinates.
    def product_row(kind,key,i,j):
        result={}
        for k,form in enumerate(blocks[kind][key][i]):
            for v,c in form.items():add(result,{(v,ids[kind][k][j]):c})
        return result
    ech={}
    for kind,i,j in data['selected_lower_equations']:
        gate()
        row={v:c for v,c in blocks[kind]['D'][i][j].items() if v in dep}
        rhs=product_row(kind,'C',i,j)
        for k in sorted(ech):
            if k in row:
                c=row[k];r,b=ech[k];add(row,r,-c);add(rhs,b,-c)
        assert row
        k=min(row);v=inv(row[k]);ech[k]=({j:norm(c*v) for j,c in row.items()},
                                       {j:norm(c*v) for j,c in rhs.items()})
    assert sorted(ech)==dep
    h=[{} for _ in range(781)]
    for k in sorted(ech,reverse=True):
        row,rhs=ech[k];val=dict(rhs)
        for j,c in row.items():
            if j!=k:add(val,h[j],-c)
        h[k]=val
    for kind,b in blocks.items():
        for i,row in enumerate(ids[kind]):
            for j,v in enumerate(row):
                for k,c in b['B'][i][j].items():add(h[v],h[k],c)
                add(h[v],product_row(kind,'A_minus_identity',i,j),-1)
    t=[coeff(c) for c in direction['chart_tangent_z']]
    v1=t[:]
    for kind,b in blocks.items():
        for row in b['B']:
            for cell in row:v1.append(norm(sum(c*t[k] for k,c in cell.items())))
    assert len(v1)==781
    active={i for i,x in enumerate(v1) if x};history=[len(active)]
    while True:
        gate()
        added={i for i,poly in enumerate(h) if i not in active and any(v in active and w in active for v,w in poly)}
        if not added:break
        active.update(added);history.append(len(active))
    assert all(not any(v in active and w in active for v,w in h[i]) for i in range(781) if i not in active)
    activez=sorted(active.intersection(range(291)))
    activeu=sorted(active.difference(range(291)))
    # The tangent satisfies all full central equations. The explicit map
    # solves the chosen subsystem, whose implicit Jacobian is identity.
    for kind,b in blocks.items():
        assert all(norm(sum(c*t[k] for k,c in cell.items()))==0 for row in b['D'] for cell in row)
    result={'status':'COMPUTER-CERTIFIED support closure of the selected implicit map',
            'field':'F'+str(p) if p else 'Q','prime':p,
            'direction':'sparse3, original free paths q*t and all other free coefficients zero',
            'variables':names,'linear_q_coefficient':[str(x) for x in v1],
            'quadratic_map':[[[list(m),str(c)] for m,c in sorted(poly.items())] for poly in h],
            'support_closure_size_history':history,'active_z_indices':activez,'active_U_indices':activeu,
            'inactive_z_indices':[i for i in range(291) if i not in active],
            'selected_active_dependent_z':[i for i in dep if i in active],
            'nonzero_quadratic_terms':sum(map(len,h)),
            'proof':'Restriction to the coordinate subspace with inactive coordinates zero preserves v=q*v1+H(v); uniqueness of the implicit origin branch proves all inactive coordinates vanish identically over the stated field.',
            'limitation':'Modular closure does not prove rational closure; this is an alternate path with no inherited six-jet smoothness certificate.',
            'input_hashes':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs},
            'seconds':time.monotonic()-start}
    out.mkdir(parents=True)
    (out/'support_closure.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('SUPPORT_HISTORY',history,'ACTIVE_Z',len(activez),'ACTIVE_U',len(activeu),
          'ACTIVE_DEPENDENT_Z',len(result['selected_active_dependent_z']),
          'TOTAL_MAP_TERMS',result['nonzero_quadratic_terms'],'SECONDS',result['seconds'],flush=True)


if __name__=='__main__':main()
