#!/usr/bin/env python3
"""Prepare a finite-precision normal-rank computation, without any CAS.

The constant normal map is a signed graph-incidence matrix. A spanning forest
eliminates its 1555 dependent coordinates, leaving 109 free coordinates.
This script verifies the chosen checkpoint against the frozen normalized
six-jet, expands invariant coordinates to all 1664 cubic correction slots,
and writes a compact binary input plus a fully readable provenance sidecar.

Running this performs a several-second exact normalization; obtain the root
agent's single-process slot first. It never edits the frozen daytime packet.
"""
import argparse
from collections import deque
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode=True
RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
DAY=REPO/'runs/astra-daytime-2026-09-08'
sys.path.insert(0,str(DAY/'scripts'))
from build_fixed_chart import F0,times
from fixed_curve_lift import normalized_jet

def immutable(path,content):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): assert path.read_bytes()==content, 'existing artifact differs: '+str(path)
    else: path.write_bytes(content)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('checkpoint',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--order',type=int,default=6,choices=range(1,7))
    args=ap.parse_args(); output=args.output.resolve()
    assert output.is_relative_to(RUN), 'all output belongs in this computation run'
    chartpath=DAY/'data/fixed_chart.json'; chart=json.loads(chartpath.read_text())
    checkpoint=json.loads(args.checkpoint.read_text()); p=checkpoint['prime']; N=args.order
    assert p==101, 'this certificate uses the accepted 101-integral six-jet bridge'
    assert checkpoint['order']>=6 and checkpoint['all_schur_equations_verified_through']>=6
    for path in [chartpath,REPO/'equations/deformation_data.json',DAY/'scripts/fixed_curve_lift.py']:
        assert checkpoint['input_hashes'][str(path.relative_to(REPO))]==hashlib.sha256(path.read_bytes()).hexdigest()
    raw,_=normalized_jet(chart)
    selected=[[x.numerator*pow(x.denominator,-1,p)%p for x in row] for row in raw]
    assert checkpoint['z_coefficients'][:7]==selected, 'wrong normalized source six-jet'
    assert all(len(u)==98 and all(len(row)==30 for row in u) for u in checkpoint['U_coefficients'][:7])
    tails=[tuple(m) for m in chart['tail_monomials']]; tailindex={m:i for i,m in enumerate(tails)}
    columns=[tuple(c) for c in chart['multiplication_columns']]
    pivots=chart['pivot_columns']; extra=chart['extra_columns']
    mons=[tuple(m) for m in chart['pivot_monomials']+chart['standard_quartics']]
    monindex={m:i for i,m in enumerate(mons)}
    images=[times(F0[i],j) for i,j in columns]
    lookup={(i,tuple(m)):k for k,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    U0=[[0]*30 for _ in range(98)]
    for k,c in enumerate(extra): U0[monindex[images[c]]][k]=1
    assert checkpoint['U_coefficients'][0]==U0
    zbase=[[selected[n][lookup[i,m]] for i in range(16) for m in tails] for n in range(N+1)]
    wbase=[([0]*2940 if n==0 else [x for row in checkpoint['U_coefficients'][n] for x in row])
           for n in range(N+1)]
    assert zbase[0]==[0]*1664
    # L(delta z)=delta E-delta P*U0 on all 330*30 quartic relation entries.
    rows=[{} for _ in range(9900)]
    for k,c in enumerate(extra):
        for cc,sign in [(c,1),(images.index(images[c]),-1)]:
            i,j=columns[cc]
            for t,m in enumerate(tails):
                row=rows[30*monindex[times(m,j)]+k]; variable=104*i+t
                row[variable]=row.get(variable,0)+sign
    rows=[{k:v for k,v in row.items() if v} for row in rows]
    assert all(len(row)<=2 and all(abs(v)==1 for v in row.values()) for row in rows)
    assert all(len(row)!=2 or sum(row.values())==0 for row in rows)
    # Bottom rows are differences x_u-x_v or singleton equations x_u=0.
    # Add a distinguished zero vertex; a selected spanning forest has1555 edges.
    ZERO=1664; parent=list(range(1665)); adjacency=[[] for _ in parent]; chosen=[]
    def find(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]; v=parent[v]
        return v
    for r,row in enumerate(rows[2940:]):
        if not row: continue
        pairs=sorted(row.items()); u,cu=pairs[0]
        v=pairs[1][0] if len(pairs)==2 else ZERO
        ru,rv=find(u),find(v)
        if ru!=rv:
            parent[ru]=rv; chosen.append(r)
            # cu*(x_u-x_v)=rhs, hence x_v=x_u-cu*rhs.
            adjacency[u].append((v,r,-cu)); adjacency[v].append((u,r,cu))
    comps={}
    for i in range(1665): comps.setdefault(find(i),[]).append(i)
    zero_comp=find(ZERO)
    anchors=sorted(min(c) for k,c in comps.items() if k!=zero_comp)
    assert len(chosen)==1555 and len(anchors)==109 and len(comps)==110
    coordinate_component=[-1]*1664
    for j,a in enumerate(anchors):
        for i in comps[find(a)]: coordinate_component[i]=j
    tree=[]; visited=set()
    for root in [ZERO]+anchors:
        q=deque([root]); visited.add(root)
        while q:
            v=q.popleft()
            for child,row,sign in adjacency[v]:
                if child in visited: continue
                visited.add(child); q.append(child); tree.append((child,v,row,sign))
    assert len(tree)==1555 and len(visited)==1665
    remaining=[r for r in range(6960) if r not in set(chosen)]
    assert len(remaining)==5405
    linear=[]
    for row in rows:
        pairs=sorted(row.items())+[(-1,0)]*(2-len(row))
        linear.extend([pairs[0][0],pairs[1][0],pairs[0][1],pairs[1][1]])
    edges=[]
    for c,cc in enumerate(pivots):
        i,j=columns[cc]
        for t,m in enumerate(tails): edges.append((monindex[times(m,j)],c,104*i+t))
    assert len(edges)==10192
    header=[p,N,1664,109,9900,2940,6960,len(chosen),len(remaining),len(edges)]
    signed=linear+[x for r in tree for x in r]+anchors+coordinate_component+remaining+[x for r in edges for x in r]
    unsigned=[x for row in zbase for x in row]+[x for row in wbase for x in row]
    payload=b'GSNRANK1'+struct.pack('<10I',*header)+struct.pack('<'+str(len(signed))+'i',*signed)+struct.pack('<'+str(len(unsigned))+'I',*unsigned)
    immutable(output,payload)
    inputs=[args.checkpoint.resolve(),chartpath,REPO/'equations/deformation_data.json',
            DAY/'scripts/fixed_curve_lift.py',Path(__file__).resolve()]
    metadata={'status':'COMPUTER-CERTIFIED prepared graph elimination; generic rank not yet computed',
      'prime':p,'precision_mod_q_power':N+1,'constant_rank':1555,'constant_kernel_dimension':109,
      'remaining_shape':[5405,109],'coordinate_order':'generator-major, 104 tail monomials in frozen chart order',
      'source_sixjet_checked':True,'all_linear_rows_have_at_most_two_terms':True,
      'input_sha256':{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
      'binary_sha256':hashlib.sha256(payload).hexdigest(),'selected_bottom_rows':chosen,
      'remaining_bottom_rows':remaining,'free_coordinate_anchors':anchors,
      'tree_edges_child_parent_bottomrow_rhs_sign':tree,
      'constant_kernel_component_of_each_coordinate':coordinate_component,
      'tail_monomials':[list(m) for m in tails]}
    immutable(output.with_suffix('.json'),(json.dumps(metadata,indent=2)+'\n').encode())
    print('PREPARED',output,'bytes',len(payload))
    print('CONSTANT_RANK_1555_KERNEL_109_BY_SPANNING_FOREST')
    print('NO_GENERIC_RANK_OR_HODGE_EQUALITY_CLAIM')

if __name__=='__main__': main()
