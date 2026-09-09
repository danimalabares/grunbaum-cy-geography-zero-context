#!/usr/bin/env python3
"""Exact rational dual-row certificates for two graph-ray obstructions.

Reconstructs the selected L left inverse from rational source blocks;
checks exact row identities and computes only the needed quadratic rows.
No inference from modular vanishing to rational vanishing is used.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import time

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'


def add(target,source,scalar):
    for j,a in source.items():
        target[j]=target.get(j,Q(0))+scalar*a
        if not target[j]:del target[j]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pilot',type=Path,default=RUN/'data/linear_u_locus_p101/necessary_locus.json')
    ap.add_argument('--max-seconds',type=float,default=120)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    pilot=json.loads(args.pilot.read_text())
    blockpath=OLD/'data/equivariant_blocks_QQ.json'
    data=json.loads(blockpath.read_text())
    assert pilot['input_sha256'][str(blockpath.relative_to(REPO))]==hashlib.sha256(blockpath.read_bytes()).hexdigest()
    tangents=[[Q(a) for a in z] for z in pilot['exact_tangent_vectors']]
    blocks={}
    rows=[];labels=[]
    for kind,block in data['blocks'].items():
        cv={name:[[{int(j):Q(a) for j,a in cell if Q(a)} for cell in row] for row in block[name]]
            for name in ['A_minus_identity','B','C','D']}
        blocks[kind]=cv
        for name in ['B','D']:
            for i,row in enumerate(cv[name]):
                for j,cell in enumerate(row):rows.append(cell);labels.append([kind,name,i,j])
    assert labels==pilot['residual_row_locations']
    selected=pilot['L_selected_original_rows']
    echelon={}
    for i in selected:
        assert time.monotonic()-started<args.max_seconds
        row=dict(rows[i]);combo={i:Q(1)}
        for pivot in sorted(echelon):
            if pivot not in row:continue
            a=row[pivot];old,tr=echelon[pivot]
            add(row,old,-a);add(combo,tr,-a)
        assert row
        pivot=min(row);a=row[pivot]
        echelon[pivot]=({j:b/a for j,b in row.items()},{j:b/a for j,b in combo.items()})
    assert sorted(echelon)==list(range(291))
    # Evaluate each coefficient block once in the ten exact source directions.
    evals=[]
    for z in tangents:
        evals.append({kind:{name:[[sum(a*z[j] for j,a in cell.items()) for cell in row] for row in matrix]
                                  for name,matrix in block.items()}
                      for kind,block in blocks.items()})
    monomials=list(combinations_with_replacement(range(10),2))
    def rhs_polynomial(i):
        kind,name,r,c=labels[i]
        left='A_minus_identity' if name=='B' else 'C'
        n=len(evals[0][kind]['B'])
        q=[]
        for a,b in monomials:
            v=sum(evals[b][kind][left][r][k]*evals[a][kind]['B'][k][c] for k in range(n))
            if a!=b:v+=sum(evals[a][kind][left][r][k]*evals[b][kind]['B'][k][c] for k in range(n))
            q.append(v)
        return q
    cache={}
    results=[]
    for target in [645,652]:
        row=dict(rows[target]);combo={}
        for pivot in sorted(echelon):
            if pivot not in row:continue
            a=row[pivot];old,tr=echelon[pivot]
            add(row,old,-a);add(combo,tr,a)
        assert not row
        exact_identity={}
        for i,a in combo.items():add(exact_identity,rows[i],a)
        assert exact_identity==rows[target]
        residual=[Q(0)]*55
        rhs_weights=dict(combo)
        rhs_weights[target]=rhs_weights.get(target,Q(0))-1
        for i,a in rhs_weights.items():
            assert time.monotonic()-started<args.max_seconds
            if not a:continue
            if i not in cache:cache[i]=rhs_polynomial(i)
            residual=[x+a*y for x,y in zip(residual,cache[i])]
        mod=lambda a:a.numerator*pow(a.denominator,-1,101)%101
        assert [mod(a) for a in residual]==pilot['quadratic_residual_rows'][target]
        terms=[{'coefficient':str(a),'parameters_one_based':[monomials[j][0]+1,monomials[j][1]+1]}
               for j,a in enumerate(residual) if a]
        results.append({'target_row':target,'location':labels[target],
                        'L_target_as_exact_combination_of_selected_rows':[[i,str(a)] for i,a in sorted(combo.items())],
                        'exact_residual_terms':terms})
        print('EXACT_RESIDUAL',target,json.dumps(terms),flush=True)
    assert results[0]['exact_residual_terms']==[{'coefficient':'-1','parameters_one_based':[8,8]}]
    assert results[1]['exact_residual_terms']==[{'coefficient':'1','parameters_one_based':[9,9]}]
    pencil=pilot['exact_product_minor_linear_pencil']
    cells={(i,j):[(k+1,Q(pencil[k][i][j])) for k in range(10) if Q(pencil[k][i][j])]
           for i in range(12) for j in range(12)}
    nonzero={ij:t for ij,t in cells.items() if t}
    allowed={(i,i) for i in range(12)}|{(0,1),(1,2),(6,0)}
    assert set(nonzero)==allowed
    assert all(nonzero[i,i]==[(3,Q(-1))] for i in range(3))
    assert all(nonzero[i,i]==[(8,Q(1 if i==6 else -1))] for i in range(3,12))
    assert all(nonzero[ij]==[(2,Q(-1))] for ij in [(0,1),(1,2),(6,0)])
    result={'status':'COMPUTER-CERTIFIED exact rational necessary obstructions; PROVED deductions stated separately',
            'field':'Q','ansatz':'U(q)=q B(t), t in all ten source intrinsic invariant directions',
            'equations':results,'quadratic_monomials_zero_based':monomials,
            'exact_rhs_polynomials_used':[[i,[str(a) for a in q]] for i,q in sorted(cache.items())],
            'product_minor':'-t3^3*t8^9',
            'determinant_argument':'Offdiagonal positions are only(0,1),(1,2),(6,0), which form no directed cycle. Hence the identity permutation is the only nonzero determinant term and the determinant is the product of the listed diagonal entries.',
            'proved_deduction':'Every rational graph-ray family in this ansatz has t8=t9=0, hence the recorded12-pivot product minor vanishes. There is no direction in the principal open t3*t8!=0 in this ansatz, over any characteristic-zero extension field.',
            'limitation':'A zero selected product minor does not prove singularity or exclude a different product-rank certificate. This excludes the recorded useful open set of graph rays, not all smooth fibres.',
            'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [args.pilot.resolve(),blockpath,Path(__file__)]},
            'seconds':time.monotonic()-started}
    (out/'linear_u_QQ_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PROVED_NO_GRAPH_RAY_IN_PRODUCT_OPEN','SECONDS',time.monotonic()-started,flush=True)


if __name__=='__main__':main()
