#!/usr/bin/env python3
"""Seek12 new degree-eight I^2 pivots from the certified first-order jet.

This is exact sparse arithmetic, not a CAS job. The central multiplication
map S_2 tensor Sym^2(k^16) -> S_8 has monomial columns. Eliminate one column
per central monomial. On the remaining rows/columns, the q coefficient is
M1[:,c]-M1[:,representative(c)]. A nonzero12x12 minor implies generic image
rank >=1829+12, independently of all unknown higher corrections.

The Picard/Hodge implication is a separate mathematical theorem; this
script certifies only the product rank and its explicit leading minor.
"""
import hashlib,json,os,sys,time
from itertools import combinations_with_replacement
from pathlib import Path
sys.dont_write_bytecode=True
from compare_lineage_tangents import polynomial

RUN=Path(__file__).resolve().parents[1]; REPO=RUN.parents[1]
def addexp(a,b): return tuple(x+y for x,y in zip(a,b))
def monomials(d):
    return [tuple(c.count(i) for i in range(8)) for c in combinations_with_replacement(range(8),d)]
def plus(a,b,c=1):
    out=dict(a)
    for k,v in b.items():
        out[k]=out.get(k,0)+c*v
        if not out[k]: del out[k]
    return out
def determinant_bareiss(matrix):
    a=[r[:] for r in matrix]; sign=1; previous=1
    for k in range(len(a)-1):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator=a[k][k]*a[i][j]-a[i][k]*a[k][j]
                assert numerator%previous==0
                a[i][j]=numerator//previous
        previous=a[k][k]
        for i in range(k+1,len(a)):a[i][k]=0
    return sign*a[-1][-1]
def main():
    started=time.monotonic();p=101
    source=REPO/'equations/deformation_data.json';data=json.loads(source.read_text())
    f0=[next(iter(polynomial(s))) for s in data['generator_order']]
    g=[]
    for s in data['first_order_corrections']:
        poly=polynomial(s);assert all(c.denominator==1 for c in poly.values())
        g.append({m:int(c) for m,c in poly.items()})
    m2=monomials(2);m8=monomials(8);assert len(m2)==36 and len(m8)==6435
    columns=[(i,j,m) for i,j in combinations_with_replacement(range(16),2) for m in m2]
    images=[addexp(addexp(f0[i],f0[j]),m) for i,j,m in columns]
    reps={}
    for c,m in enumerate(images):reps.setdefault(m,c)
    central=set(reps);extra=[c for c,m in enumerate(images) if reps[m]!=c]
    assert len(columns)==4896 and len(reps)==1829 and len(extra)==3067
    assert len(m8)-len(reps)==4606
    def coefficient(c):
        i,j,m=columns[c]
        one={addexp(addexp(a,f0[j]),m):v for a,v in g[i].items()}
        two={addexp(addexp(f0[i],a),m):v for a,v in g[j].items()}
        return {e:v for e,v in plus(one,two).items() if e not in central}
    cache={}
    def residual(c):
        rep=reps[images[c]]
        if rep not in cache:cache[rep]=coefficient(rep)
        return plus(coefficient(c),cache[rep],-1)
    basis={};chosen=[];pivot_rows=[];units=[]
    for counter,c in enumerate(extra):
        r={m:v%p for m,v in residual(c).items() if v%p}
        while r:
            pivot=min(r)
            if pivot not in basis:
                unit=r[pivot];inv=pow(unit,-1,p)
                basis[pivot]={m:v*inv%p for m,v in r.items()}
                chosen.append(c);pivot_rows.append(pivot);units.append(unit)
                print('NEW_Q1_PRODUCT_PIVOT',len(chosen),'COLUMN',c,'MONOMIAL',pivot,'UNIT',unit,flush=True)
                break
            a=r[pivot]
            for m,v in basis[pivot].items():
                r[m]=(r.get(m,0)-a*v)%p
                if not r[m]:del r[m]
        if len(chosen)==12:break
    # Verify the original first-order Schur submatrix, not just its reduced columns.
    matrix=[[residual(c).get(m,0) for c in chosen] for m in pivot_rows]
    det=determinant_bareiss(matrix) if chosen else 1
    assert det%p!=0
    rank=1829+len(chosen)
    result={'status':'COMPUTER-CERTIFIED degree-eight ideal-square image rank lower bound',
      'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'source_commit':data['source_commit'],'prime':p,
      'matrix_shape':[6435,4896],'central_rank':1829,'schur_shape':[4606,3067],
      'extra_q1_rank_lower_bound':len(chosen),'generic_product_rank_lower_bound':rank,
      'all_extra_columns_scanned':counter+1==len(extra),'extra_columns_scanned':counter+1,
      'first_order_schur_minor_integer_matrix':matrix,
      'first_order_schur_minor_integer_determinant':det,
      'full_minor_leading_q_valuation':len(chosen),
      'minor_rows_exponents':pivot_rows,
      'minor_columns':[{'index':c,'generator_pair_1_based':[columns[c][0]+1,columns[c][1]+1],
                        'quadratic_monomial':columns[c][2],
                        'central_representative_column':reps[images[c]]} for c in chosen],
      'pivot_units_mod101':units,
      'independent_of_unknown_higher_corrections':True,
      'picard_hodge_theorem_is_separate':True,
      'seconds':time.monotonic()-started}
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/product-first-order')).resolve()
    assert out.is_relative_to(RUN);out.mkdir(parents=True,exist_ok=True)
    dest=out/'product_first_order_rank.json'
    if dest.exists():assert json.loads(dest.read_text())==result
    else:dest.write_text(json.dumps(result,indent=2)+'\n')
    print('GENERIC_PRODUCT_RANK_AT_LEAST',rank)
    print('INTEGER_MINOR_DETERMINANT',det)
    print('CERTIFICATE',dest)
    print('SECONDS',result['seconds'])
if __name__=='__main__':main()
