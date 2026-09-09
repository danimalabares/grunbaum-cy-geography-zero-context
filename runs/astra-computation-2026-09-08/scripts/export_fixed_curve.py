#!/usr/bin/env python3
"""Export FINITE exact equations for the pointed implicit algebraic curve.

The Singular file constructs equations only; it deliberately does not call
std, eliminate, minAssGTZ, or solve. There are 270 dependent z variables,
2940 auxiliary w variables, and q. The other 21 z variables are prescribed
degree-six polynomials. The branch selector is q=z=w=0. The family F is
encoded explicitly in JSON and as a formula in FIXED_CHART.md.
"""
import argparse, json
from pathlib import Path
from fractions import Fraction as Q
from build_fixed_chart import F0, FWORDS, times, name
from fixed_curve_lift import normalized_jet

RUN=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--prime',type=int,default=0)
    args=ap.parse_args(); p=args.prime
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    jet,_=normalized_jet(chart)
    dep=chart['dependent_coordinates']; free=chart['free_coordinates']
    def coefficient(v):
        if p: return str(v.numerator*pow(v.denominator,-1,p)%p)
        return str(v)
    def poly(j):
        terms=[f'({coefficient(jet[n][j])})*q^{n}' for n in range(1,7) if jet[n][j]]
        return '('+'+'.join(terms)+')' if terms else '0'
    z=[f'z{j+1}' if j in dep else poly(j) for j in range(291)]
    cols=[tuple(c) for c in chart['multiplication_columns']]
    piv=chart['pivot_columns']; extra=chart['extra_columns']
    mons=[tuple(m) for m in chart['pivot_monomials']+chart['standard_quartics']]
    idx={m:i for i,m in enumerate(mons)}
    tails=[tuple(m) for m in chart['tail_monomials']]
    lookup={(i,tuple(m)):k for k,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    images=[times(F0[i],j) for i,j in cols]
    lin=[{} for _ in range(9900)]
    for k,c in enumerate(extra):
        for cc,sign in [(c,1),(images.index(images[c]),-1)]:
            i,j=cols[cc]
            for m in tails:
                row=lin[30*idx[times(m,j)]+k]; zz=lookup[i,m]
                row[zz]=row.get(zz,0)+sign
    edges=[[] for _ in range(330)]
    for c,cc in enumerate(piv):
        i,j=cols[cc]
        for m in tails: edges[idx[times(m,j)]].append((c,lookup[i,m]))
    def w(r,k): return f'w{30*r+k+1}'
    selected=[(i,k) for i in range(98) for k in range(30)]
    selected += [(98+i,k) for i,k in chart['independent_equations']]
    equations=[]
    for r,k in selected:
        terms=[f'({a})*({z[j]})' for j,a in sorted(lin[30*r+k].items()) if a and z[j]!='0']
        if r<98: terms.append('-'+w(r,k))
        terms += [f'-({z[j]})*{w(c,k)}' for c,j in edges[r] if z[j]!='0']
        equations.append('+'.join(terms).replace('+-','-') or '0')
    variables=['q']+[f'z{j+1}' for j in dep]+[w(r,k) for r in range(98) for k in range(30)]
    text='// FINITE IMPLICIT CURVE; NO GROEBNER JOB. Select the germ at all variables zero.\n'
    text+=f'ring curveRing={p},('+','.join(variables)+'),dp;\n'
    text+='ideal curveEquations=\n'+',\n'.join(equations)+';\n'
    text+='print("FINITE_CURVE_LOADED_3210_EQUATIONS_3211_VARIABLES_NO_SOLVE");\n'
    label='QQ' if not p else f'F{p}'
    output=RUN/'equations'; output.mkdir(exist_ok=True)
    dest=output/f'fixed_curve_{label}.sing'
    if dest.exists(): assert dest.read_text()==text
    else: dest.write_text(text)
    model={'coefficient_field':label,'curve_file':dest.name,'branch':'q=z_dependent=w=0',
      'free_coordinates':[j+1 for j in free],
      'free_paths':{str(j+1):z[j] for j in free},
      'generator_F':[name(F0[i])+'+'+'+'.join(f'({z[lookup[i,m]]})*{name(m)}' for m in tails if z[lookup[i,m]]!='0') for i in range(16)],
      'U_description':'U=U0+w; U0[pivot_row_of_extra_column,k]=1; R_pivot=-U,R_extra=identity',
      'number_equations':len(equations),'number_variables':len(variables),
      'proof':'FIXED_CHART.md; full 6960 Schur equations vanish on selected local branch',
      'status':'finite algebraic pointed family; a finite-q smooth fibre is not yet selected'}
    destj=output/f'fixed_curve_{label}.json'
    if destj.exists(): assert json.loads(destj.read_text())==model
    else: destj.write_text(json.dumps(model,indent=2)+'\n')
    print(dest,len(text),'bytes')
    print('SELECTED_CONSTANT_JACOBIAN_UNIT',chart['jacobian_minor'])
    print('FINITE_ALGEBRAIC_FAMILY_WITH_BRANCH_SELECTOR; NO_FINITE_Q_FIBRE_CLAIM')

if __name__=='__main__': main()
