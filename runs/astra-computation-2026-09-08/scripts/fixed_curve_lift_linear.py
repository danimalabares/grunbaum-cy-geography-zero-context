#!/usr/bin/env python3
"""Exact coefficientwise lifting in the finite invariant Hilbert chart.

The 21 free normalized generator coefficients follow ONLY the certified
first-order tangent: z_free(q)=q*z_free,1. Higher free coefficients are zero.
This is a deliberately different curve in the same fixed Hilbert germ. At every order ONLY the
same 270x270 constant matrix is solved. No versal or Groebner job occurs.
The other 6690 Schur equations are checked at every order. Finite order is
NOT exact polynomial closure. Default order6 is a cheap regression against
the supplied normalized six-jet; --order 24 is an overnight checkpoint job.

All computations use Python integers modulo a specified prime. No new
package, numerical matrix rank, or parallel process is used. The output
defines a NEW curve agreeing only with the normalized certified first jet.
The untouched original lift and this actual variant are both hashed.
"""
import argparse, hashlib, json, os, time
from fractions import Fraction as Q
from pathlib import Path
from build_fixed_chart import F0, V, monomials, times
from compare_lineage_tangents import polynomial

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]

def mm(a,b):
    out=[[Q(0) for _ in b[0]] for _ in a]
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(b[k]):
                    if y: out[i][j]+=x*y
    return out

def normalized_jet(chart):
    src=json.loads((REPO/'equations/deformation_data.json').read_text())
    H=[[polynomial(s) for s in row] for row in src['six_jet_coefficients']]
    mats=[[[H[d][i].get(m,Q(0)) for i in range(16)] for m in F0] for d in range(7)]
    ident=[[Q(int(i==j)) for j in range(16)] for i in range(16)]
    assert mats[0]==ident
    inv=[ident]
    for d in range(1,7):
        r=[[Q(0) for _ in range(16)] for _ in range(16)]
        for k in range(1,d+1):
            prod=mm(mats[k],inv[d-k])
            for i in range(16):
                for j in range(16): r[i][j]-=prod[i][j]
        inv.append(r)
    mons=monomials(3)
    normalized=[]
    for d in range(7):
        r=[[Q(0) for _ in range(16)] for _ in mons]
        for k in range(d+1):
            h=[[H[k][i].get(m,Q(0)) for i in range(16)] for m in mons]
            prod=mm(h,inv[d-k])
            for i in range(len(mons)):
                for j in range(16): r[i][j]+=prod[i][j]
        normalized.append(r)
    zi=[]
    for d in range(7):
        for j,m in enumerate(F0):
            assert normalized[d][mons.index(m)]==([Q(int(i==j)) for i in range(16)] if d==0 else [Q(0)]*16)
        coords=[]
        for orbit in chart['coefficient_orbits']:
            values={normalized[d][mons.index(tuple(m))][i] for i,m in orbit}
            assert len(values)==1, 'lost equivariance in normalization'
            coords.append(values.pop())
        zi.append(coords)
    return zi,inv

def lu_factor(a,p):
    a=[r[:] for r in a]; perm=list(range(len(a))); n=len(a)
    for k in range(n):
        i=next(i for i in range(k,n) if a[i][k]%p)
        a[k],a[i]=a[i],a[k]; perm[k],perm[i]=perm[i],perm[k]
        v=pow(a[k][k],-1,p)
        for i in range(k+1,n):
            if a[i][k]:
                c=a[i][k]*v%p; a[i][k]=c
                for j in range(k+1,n): a[i][j]=(a[i][j]-c*a[k][j])%p
    return a,perm

def lu_solve(lu,b,p):
    a,perm=lu; v=[b[i]%p for i in perm]; n=len(a)
    for i in range(n): v[i]=(v[i]-sum(a[i][j]*v[j] for j in range(i)))%p
    for i in range(n-1,-1,-1):
        v[i]=(v[i]-sum(a[i][j]*v[j] for j in range(i+1,n)))*pow(a[i][i],-1,p)%p
    return v

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--order',type=int,default=6)
    ap.add_argument('--prime',type=int,default=101)
    ap.add_argument('--resume',type=Path)
    args=ap.parse_args(); p=args.prime
    assert p>3 and all(p%d for d in range(2,int(p**.5)+1))
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    rawjet,inv=normalized_jet(chart)
    modular=lambda x: x.numerator*pow(x.denominator,-1,p)%p
    jet=[[modular(x) for x in r] for r in rawjet]
    output=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/fixed_curve_default'))
    output.mkdir(parents=True,exist_ok=True)
    jetfile=output/'normalized_sixjet.json'
    jetdata={'z_jet':[[str(x) for x in r] for r in rawjet],
        'generator_basis_inverse':[[[str(x) for x in r] for r in m] for m in inv]}
    if jetfile.exists(): assert json.loads(jetfile.read_text())==jetdata
    else: jetfile.write_text(json.dumps(jetdata,indent=2)+'\n')
    input_hashes={str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [RUN/'data/fixed_chart.json',REPO/'equations/deformation_data.json',RUN/'scripts/fixed_curve_lift.py',Path(__file__)]}
    dep=chart['dependent_coordinates']; free=chart['free_coordinates']
    selected=[30*i+j for i,j in chart['independent_equations']]
    jrows=[dict(r) for r in chart['linear_rows']]
    lu=lu_factor([[jrows[i].get(j,0)%p for j in dep] for i in selected],p)
    cols=[tuple(c) for c in chart['multiplication_columns']]
    piv=chart['pivot_columns']; extra=chart['extra_columns']
    mons=[tuple(m) for m in chart['pivot_monomials']+chart['standard_quartics']]
    mindex={m:i for i,m in enumerate(mons)}
    lookup={(i,tuple(m)):k for k,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    tails=[tuple(m) for m in chart['tail_monomials']]
    images=[times(F0[i],j) for i,j in cols]
    # Full linear relation rows, including the 98 pivot monomials.
    lin=[{} for _ in range(330*30)]
    for k,c in enumerate(extra):
        for cc,sign in [(c,1),(images.index(images[c]),-1)]:
            i,j=cols[cc]
            for m in tails:
                row=lin[30*mindex[times(m,j)]+k]; z=lookup[i,m]
                row[z]=row.get(z,0)+sign
    lin=[{j:v for j,v in r.items() if v} for r in lin]
    assert lin[98*30:]==jrows
    edges=[]
    for c,cc in enumerate(piv):
        i,j=cols[cc]
        for m in tails: edges.append((mindex[times(m,j)],c,lookup[i,m]))
    def mult(z,u):
        out=[[0]*30 for _ in range(330)]
        for r,c,k in edges:
            a=z[k]
            if a:
                ur=u[c]; rr=out[r]
                for j,b in enumerate(ur):
                    if b: rr[j]+=a*b
        return [[x%p for x in r] for r in out]
    U0=[[0]*30 for _ in range(98)]
    for k,c in enumerate(extra): U0[mindex[images[c]]][k]=1
    zs=[[0]*291]; us=[U0]
    if args.resume:
        previous=json.loads(args.resume.read_text())
        assert previous['prime']==p and previous['free_coordinates']==free
        assert previous['input_hashes']==input_hashes, 'checkpoint input provenance mismatch'
        zs=previous['z_coefficients']; us=previous['U_coefficients']
        assert len(zs)==len(us)==previous['order']+1
        assert us[0]==U0 and zs[0]==jet[0]
        assert previous['free_path_order']==1
        assert zs[1]==jet[1]
        assert all(zs[n][j]==0 for n in range(2,len(zs)) for j in free)
    started=time.monotonic()
    for n in range(len(zs),args.order+1):
        cross=[[0]*30 for _ in range(330)]
        for i in range(1,n):
            prod=mult(zs[i],us[n-i])
            for r in range(330):
                cross[r]=[(a+b)%p for a,b in zip(cross[r],prod[r])]
        z=[0]*291
        if n==1:
            for j in free: z[j]=jet[1][j]
        rhs=[(cross[98+i//30][i%30]-sum(a*z[j] for j,a in jrows[i].items()))%p for i in selected]
        solution=lu_solve(lu,rhs,p)
        for j,a in zip(dep,solution): z[j]=a
        all_linear=[sum(a*z[j] for j,a in row.items())%p for row in lin]
        un=[[ (all_linear[30*r+k]-cross[r][k])%p for k in range(30)] for r in range(98)]
        residual=[(all_linear[30*r+k]-cross[r][k])%p for r in range(98,330) for k in range(30)]
        assert not any(residual), ('residual equations nonzero',n,next(i for i,v in enumerate(residual) if v))
        if n==1: assert z==jet[1], ('first-jet mismatch',n)
        zs.append(z); us.append(un)
        checkpoint={'prime':p,'order':n,'free_coordinates':free,'input_hashes':input_hashes,
            'free_path_order':1,'curve_definition':'z_free(q)=q*z_free,1; same certified tangent; higher jet differs',
            'z_coefficients':zs,'U_coefficients':us,'all_schur_equations_verified_through':n,
            'status':'COMPUTER-CERTIFIED finite jet; polynomial/rational closure NOT tested'}
        dest=output/f'fixed_curve_p{p}_order{n}.json'
        if dest.exists(): assert json.loads(dest.read_text())==checkpoint
        else: dest.write_text(json.dumps(checkpoint)+'\n')
        print('ORDER',n,'ALL_6960_EQUATIONS_ZERO','seconds',round(time.monotonic()-started,2),flush=True)
    print('NORMALIZED_FIRSTJET_MATCH',args.order>=1)
    print('NORMALIZED_SIXJET_MATCH',zs[:7]==jet)
    print('FREE_PATH_ORDER',1)
    print('NO_POLYNOMIAL_CLOSURE_CLAIM',flush=True)

if __name__=='__main__': main()
