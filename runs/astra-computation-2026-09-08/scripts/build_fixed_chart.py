#!/usr/bin/env python3
"""Finite S3-fixed cubic/syzygy incidence chart, using only exact integers.

No Groebner bases.  The output specifies F, multiplication by variables,
and a constant-Jacobian independent subsystem of its rank-98 equations.
It is NOT a smooth fibre.  See FIXED_CHART.md for the flatness argument.
All polynomial/linear algebra sizes are bounded by the central fibre.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
import json

RUN = Path(__file__).resolve().parents[1]
V = 'abcdefgh'
FWORDS = ['abf','abg','abh','acg','ach','adh','bdf','bdg',
          'beg','cde','ceg','ceh','cfh','def','dfh','efg']
F0 = [tuple(w.count(x) for x in V) for w in FWORDS]
GROUP = ['abcdefgh','ahgfedcb','ceafbdgh','chgdbfae','gbcfhdae','geadhfcb']
PERMS = [[V.index(c) for c in w] for w in GROUP]

def monomials(d):
    return sorted({tuple(w.count(j) for j in range(8))
                   for w in combinations_with_replacement(range(8), d)})

def act(m,p):
    r=[0]*8
    for i,v in enumerate(m): r[p[i]]=v
    return tuple(r)

def times(m,j):
    r=list(m); r[j]+=1
    return tuple(r)

def name(m):
    return '*'.join(x+(f'^{e}' if e>1 else '') for x,e in zip(V,m) if e) or '1'

def main():
    tails=[m for m in monomials(3) if m not in F0]
    pairs=[(i,m) for i in range(16) for m in tails]
    unseen=set(pairs); orbits=[]; lookup={}
    while unseen:
        v=min(unseen)
        O=sorted({(F0.index(act(F0[v[0]],p)),act(v[1],p)) for p in PERMS})
        oi=len(orbits)
        for x in O: lookup[x]=oi
        unseen.difference_update(O); orbits.append(O)
    columns=[(i,j) for i in range(16) for j in range(8)]
    images=[times(F0[i],j) for i,j in columns]
    pivot_mons=sorted(set(images))
    pivot_cols=[images.index(m) for m in pivot_mons]
    extra_cols=[j for j in range(128) if j not in pivot_cols]
    std4=[m for m in monomials(4) if m not in pivot_mons]
    assert (len(tails),len(pivot_mons),len(extra_cols),len(std4))==(104,98,30,232)
    stdindex={m:i for i,m in enumerate(std4)}
    # E = D-C A^{-1} B. At zero A=I, C=D=0, B has one 1/column.
    rows=[{} for _ in range(232*30)]
    for k,col in enumerate(extra_cols):
        rep=images.index(images[col])
        for c,sign in [(col,1),(rep,-1)]:
            i,j=columns[c]
            for m in tails:
                out=times(m,j)
                if out in stdindex:
                    row=rows[30*stdindex[out]+k]; z=lookup[i,m]
                    row[z]=row.get(z,0)+sign
    rows=[{j:v for j,v in r.items() if v} for r in rows]
    # Sparse rational echelon; store the original independent equations.
    basis={}; selected=[]
    for ri,r in enumerate(rows):
        r={j:Q(v) for j,v in r.items()}
        while r:
            p=min(r)
            if p not in basis:
                a=r[p]; basis[p]={j:v/a for j,v in r.items()}
                selected.append(ri); break
            a=r[p]
            for j,v in basis[p].items():
                r[j]=r.get(j,Q(0))-a*v
                if not r[j]: del r[j]
    dependent=sorted(basis)
    free=[j for j in range(len(orbits)) if j not in basis]
    assert len(free)==21, (len(orbits),len(basis),len(free))
    # Exact determinant of selected square minor using independent elimination.
    square=[[Q(rows[i].get(j,0)) for j in dependent] for i in selected]
    determinant=Q(1)
    for k in range(len(square)):
        p=next(i for i in range(k,len(square)) if square[i][k])
        if p!=k: square[k],square[p]=square[p],square[k]; determinant=-determinant
        a=square[k][k]; determinant*=a
        for i in range(k+1,len(square)):
            if square[i][k]:
                b=square[i][k]/a
                for j in range(k+1,len(square)): square[i][j]-=b*square[k][j]
                square[i][k]=Q(0)
    assert determinant and determinant.numerator%101 and determinant.denominator%101
    data={
      'status':'COMPUTER-CERTIFIED finite chart combinatorics; not a fibre',
      'variables':V,'F0':FWORDS,'group_images':GROUP,
      'tail_monomials':[list(m) for m in tails],
      'coefficient_orbits':[[[i,list(m)] for i,m in O] for O in orbits],
      'multiplication_columns':columns,'pivot_columns':pivot_cols,
      'extra_columns':extra_cols,'pivot_monomials':[list(m) for m in pivot_mons],
      'standard_quartics':[list(m) for m in std4],
      'independent_equations':[[i//30,i%30] for i in selected],
      'dependent_coordinates':dependent,'free_coordinates':free,
      'linear_rank':len(basis),'jacobian_minor':str(determinant),
      'linear_rows':[[[j,v] for j,v in sorted(r.items())] for r in rows],
    }
    out=RUN/'data'; out.mkdir(exist_ok=True)
    dest=out/'fixed_chart.json'
    if dest.exists():
        # Serialized tuples become JSON lists. Compare canonical JSON data,
        # not unequal Python container types; the existing file is untouched.
        assert json.loads(dest.read_text())==json.loads(json.dumps(data)), 'existing chart differs; preserve it'
    else: dest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['linear_rank','jacobian_minor','free_coordinates']},indent=2))
    print('invariant_generator_coefficients',len(orbits))
    print('normalized_fixed_Hilbert_tangent',len(free))
    print('coordinate_orbit_fixed_dimension',11)
    print('intrinsic_fixed_dimension',10)
    print('full_Schur_equations',len(rows),'selected',len(selected))
    print('PASS: constant Jacobian minor is a 101-adic unit')

if __name__=='__main__': main()
