#!/usr/bin/env python3
"""Try a SMALL common denominator, then certify every exact FR identity.

This is a bounded rational-ansatz test, not algebraic reconstruction. A
failure says nothing against the algebraic implicit curve. Uses all saved
generator AND syzygy coefficients. Only an exact polynomial identity passes.
No evaluation of a truncation at q=1 is performed.
"""
import argparse, hashlib, json, os
from math import isqrt
from pathlib import Path
from build_fixed_chart import F0, times

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]

def save_immutable(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): assert json.loads(path.read_text())==data, 'existing result differs: '+str(path)
    else: path.write_text(json.dumps(data)+'\n')

def solve_overdetermined(rows,d,p):
    base={}
    for rr in rows:
        r=[x%p for x in rr]
        for k,b in sorted(base.items()):
            if r[k]:
                c=r[k]; r=[(a-c*v)%p for a,v in zip(r,b)]
        nz=next((j for j in range(d) if r[j]),None)
        if nz is None:
            if r[d]: return None
        else:
            inv=pow(r[nz],-1,p); base[nz]=[v*inv%p for v in r]
    # Consistent underdetermined fits are permitted, with free denominator
    # coefficients zero; exact FR verification remains the acceptance test.
    x=[0]*d
    for k,b in sorted(base.items(),reverse=True):
        x[k]=(b[d]-sum(b[j]*x[j] for j in range(k+1,d)))%p
    return x

def validate_checkpoint(state,chart):
    """Validate the origin and provenance needed for the local-flatness claim."""
    p=state['prime']; N=state['order']
    assert isinstance(p,int) and p>3 and all(p%d for d in range(2,isqrt(p)+1)), 'prime is not a prime >3'
    assert isinstance(N,int) and N>=6, 'need a checkpoint through at least order six'
    zs=state['z_coefficients']; us=state['U_coefficients']
    assert len(zs)==len(us)==N+1, 'checkpoint order/length mismatch'
    assert all(len(z)==291 for z in zs), 'wrong generator coefficient shape'
    assert all(len(u)==98 and all(len(row)==30 for row in u) for u in us), 'wrong syzygy coefficient shape'
    assert all(isinstance(x,int) and 0<=x<p for z,u in zip(zs,us)
               for x in z+[v for row in u for v in row]), 'coefficients must be canonical field residues'
    assert zs[0]==[0]*291, 'constant generators do not equal the marked SR generators'
    assert state['free_coordinates']==chart['free_coordinates'], 'free-coordinate convention mismatch'
    for path in [RUN/'data/fixed_chart.json',REPO/'equations/deformation_data.json',RUN/'scripts/fixed_curve_lift.py']:
        key=str(path.relative_to(REPO))
        assert state['input_hashes'].get(key)==hashlib.sha256(path.read_bytes()).hexdigest(), 'checkpoint provenance mismatch: '+key
    mons=[tuple(v) for v in chart['pivot_monomials']]
    cols=[tuple(c) for c in chart['multiplication_columns']]
    U0=[[0]*30 for _ in range(98)]
    for k,c in enumerate(chart['extra_columns']):
        i,j=cols[c]; U0[mons.index(times(F0[i],j))][k]=1
    assert us[0]==U0, 'constant syzygies do not give the complete canonical special relation basis'
    return p,N,zs,us

def build_identity_operator(chart):
    cols=[tuple(c) for c in chart['multiplication_columns']]
    piv=chart['pivot_columns']; extra=chart['extra_columns']
    mons=[tuple(v) for v in chart['pivot_monomials']+chart['standard_quartics']]
    idx={v:i for i,v in enumerate(mons)}
    tails=[tuple(v) for v in chart['tail_monomials']]
    lookup={(i,tuple(v)):k for k,O in enumerate(chart['coefficient_orbits']) for i,v in O}
    images=[times(F0[i],j) for i,j in cols]
    lin=[{} for _ in range(9900)]
    for k,c in enumerate(extra):
        for cc,sign in [(c,1),(images.index(images[c]),-1)]:
            i,j=cols[cc]
            for v in tails:
                row=lin[30*idx[times(v,j)]+k]; z=lookup[i,v]
                row[z]=row.get(z,0)+sign
    edges=[]
    for c,cc in enumerate(piv):
        i,j=cols[cc]
        for v in tails: edges.append((idx[times(v,j)],c,lookup[i,v]))
    return lin,edges

def verify_identity(den,num,U0,p,operator):
    """Clear D^2 in E(z)-P(z)U and check every resulting coefficient.

    Return an exact first nonzero coefficient witness, or None for success.
    Here m>=deg(D), so checking degrees 0..2m is exhaustive.
    """
    lin,edges=operator
    m=len(num)-1; degreeD=len(den)-1
    assert den[0]==1 and degreeD<=m
    znum=[r[:291] for r in num]
    unum=[[r[291+30*i:291+30*(i+1)] for i in range(98)] for r in num]
    # W=U_num-D*U0, so residual is D*(L(z_num)-inclusion(W))-M(z_num)*W.
    w=[[[ (a-(den[n]*U0[i][j] if n<=degreeD else 0))%p
          for j,a in enumerate(row)] for i,row in enumerate(mat)] for n,mat in enumerate(unum)]
    lz=[[sum(a*z[j] for j,a in r.items())%p for r in lin] for z in znum]
    for n in range(2*m+1):
        result=[0]*9900
        for k,dk in enumerate(den):
            i=n-k
            if 0<=i<=m:
                for r in range(330):
                    for c in range(30):
                        value=lz[i][30*r+c]-(w[i][r][c] if r<98 else 0)
                        result[30*r+c]+=dk*value
        for i in range(max(0,n-m),min(n,m)+1):
            j=n-i
            for r,c,k in edges:
                a=znum[i][k]
                if a:
                    for cc,b in enumerate(w[j][c]):
                        if b: result[30*r+cc]-=a*b
        if any(v%p for v in result):
            row=next(i for i,v in enumerate(result) if v%p)
            return {'q_degree':n,'quartic_row':row//30,'relation_column':row%30,
                    'residue':result[row]%p,'all_lower_coefficients_zero':True}
        print('EXACT_FR_COEFFICIENT',n,'ZERO',flush=True)
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('checkpoint',type=Path)
    ap.add_argument('--max-denominator',type=int,default=10)
    ap.add_argument('--allow-other-sixjet',action='store_true',
                    help='allow a different verified origin jet; intended only for controls or a deliberately different curve')
    args=ap.parse_args()
    assert args.max_denominator>=0
    state=json.loads(args.checkpoint.read_text())
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    p,N,zs,us=validate_checkpoint(state,chart)
    from fixed_curve_lift import normalized_jet
    rawjet,_=normalized_jet(chart)
    selected=[[x.numerator*pow(x.denominator,-1,p)%p for x in row] for row in rawjet]
    sixjet_matches=zs[:7]==selected
    assert sixjet_matches or args.allow_other_sixjet, 'checkpoint does not match the selected normalized six-jet'
    seq=[z+[x for row in u for x in row] for z,u in zip(zs,us)]
    operator=build_identity_operator(chart)
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/rational_default'))
    out=out.resolve(); assert out.is_relative_to(RUN), 'output must stay inside this run directory'
    out.mkdir(parents=True,exist_ok=True)
    checkpoint_hash=hashlib.sha256(args.checkpoint.read_bytes()).hexdigest()
    checker_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for d in range(0,min(args.max_denominator,(N-6)//2)+1):
        m=d+6
        rows=([seq[n-k][j] for k in range(1,d+1)]+[-seq[n][j]]
              for n in range(m+1,N+1) for j in range(len(seq[0])))
        coeff=solve_overdetermined(rows,d,p)
        print('DENOMINATOR',d,'NUMERATOR_BOUND',m,'FIT',coeff is not None,flush=True)
        attempt={'checkpoint_sha256':checkpoint_hash,'checker_sha256':checker_hash,
                 'prime':p,'denominator_bound':d,'numerator_bound':m,'fit_exists':coeff is not None,
                 'matches_selected_normalized_sixjet':sixjet_matches}
        attempt_path=out/f'attempt_p{p}_{checkpoint_hash[:12]}_{checker_hash[:12]}_d{d}.json'
        if coeff is None:
            attempt['status']='FAILED: inconsistent linear Padé fit at these bounds'
            save_immutable(attempt_path,attempt)
            continue
        den=[1]+coeff
        num=[[sum(den[k]*seq[n-k][j] for k in range(min(d,n)+1))%p
              for j in range(len(seq[0]))] for n in range(m+1)]
        # Explicitly verify the rational model agrees with every supplied coefficient.
        assert all(sum(den[k]*seq[n-k][j] for k in range(min(d,n)+1))%p==
                   (num[n][j] if n<=m else 0)
                   for n in range(N+1) for j in range(len(seq[0])))
        witness=verify_identity(den,num,us[0],p,operator)
        attempt['denominator']=den
        if witness is not None:
            attempt.update(status='FAILED: selected Padé fit has a nonzero exact FR coefficient',first_nonzero_coefficient=witness)
            save_immutable(attempt_path,attempt)
            print('FAILED_EXACT_CLOSURE',json.dumps(witness),'CONTINUING_TO_LARGER_BOUND',flush=True)
            continue
        attempt['status']='COMPUTER-CERTIFIED exact rational identity'; save_immutable(attempt_path,attempt)
        znum=[r[:291] for r in num]
        unum=[[r[291+30*i:291+30*(i+1)] for i in range(98)] for r in num]
        model={'prime':p,'denominator':den,'z_numerator':znum,'U_numerator':unum,
               'checkpoint':str(args.checkpoint.resolve()),'checkpoint_sha256':checkpoint_hash,
               'checker_sha256':checker_hash,'input_hashes':state['input_hashes'],
               'matches_selected_normalized_sixjet':sixjet_matches,
               'status':'COMPUTER-CERTIFIED rational family over finite field, flat near q=0 after shrinking; not characteristic-zero equations',
               'FR_identity_all_coefficients_zero':True,
               'complete_canonical_special_syzygies_verified':True,
               'smoothness_certified':False}
        dest=out/f'rational_family_p{p}.json'; save_immutable(dest,model)
        print('EXACT_RATIONAL_FAMILY',dest)
        print('Next: export finite equations; certify intended smooth generic fibre and characteristic-zero realization before Hodge claims.')
        return
    print('FAILED_BOUNDED_COMMON_RATIONAL_ANSATZ: no exact family found among the selected fits. '
          'Other underdetermined fits, larger bounds, and algebraic curves remain open.',flush=True)

if __name__=='__main__': main()
