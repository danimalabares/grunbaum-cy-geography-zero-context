#!/usr/bin/env python3
"""Bounded algebraic recognition from EXISTING order-32 checkpoints only.

Select eight dependent coordinates not rational at individual bounds
denominator<=4,numerator<=denominator+6. Test P(q,t) of t-degree2..4,
q-degree<=6 with <=28 coefficients and at least four excess equations.
Both raw z_j and z_j/q^valuation-leading_coefficient are tried, using
only genuinely available coefficients after division by q^valuation.
No finite series fit is an exact algebraic model or smoothness proof.

Optional reconstruction fits all291 coordinates as a polynomial in t
of degree<deg_t(P), coefficients in F_p[q] of degree<=6, divided by one
common polynomial D(q) of degree<=4 with D(0)=1. It is also ONLY a fit.
Exact Schur identities, branch control, and smoothness remain mandatory.
"""
import argparse, hashlib, json, os, time
from pathlib import Path
from check_rational_closure import solve_overdetermined, validate_checkpoint
from check_rational_closure_linear import validate_checkpoint as validate_linear
from fixed_curve_lift import normalized_jet

RUN=Path(__file__).resolve().parents[1]

def convolution(a,b,p,N):
    return [sum(a[i]*b[n-i] for i in range(n+1))%p for n in range(N+1)]

def powers(t,degree,p):
    N=len(t)-1; result=[[1]+[0]*N]
    for _ in range(degree): result.append(convolution(result[-1],t,p,N))
    return result

def rref(matrix,p,coefficient_columns=None):
    a=[row[:] for row in matrix]; nr=len(a)
    nc=len(a[0]) if coefficient_columns is None else coefficient_columns
    pivots=[]; row=0
    for col in range(nc):
        hit=next((i for i in range(row,nr) if a[i][col]%p),None)
        if hit is None: continue
        a[row],a[hit]=a[hit],a[row]
        inv=pow(a[row][col],-1,p); a[row]=[x*inv%p for x in a[row]]
        for i in range(nr):
            if i!=row and a[i][col]:
                c=a[i][col]; a[i]=[(x-c*y)%p for x,y in zip(a[i],a[row])]
        pivots.append(col); row+=1
        if row==nr: break
    return a,pivots

def nullspace(matrix,p):
    reduced,pivots=rref(matrix,p); n=len(matrix[0]); vectors=[]
    for free in range(n):
        if free in pivots: continue
        v=[0]*n; v[free]=1
        for row,col in enumerate(pivots): v[col]=-reduced[row][free]%p
        vectors.append(v)
    return len(pivots),vectors

def small_rational(sequence,p):
    N=len(sequence)-1
    for d in range(5):
        m=d+6
        rows=([sequence[n-k] for k in range(1,d+1)]+[-sequence[n]] for n in range(m+1,N+1))
        if solve_overdetermined(rows,d,p) is not None: return True
    return False

def series_columns(t,dt,dq,p):
    pw=powers(t,dt,p); N=len(t)-1
    monomials=[(e,k) for e in range(dt+1) for k in range(dq+1)]
    columns=[[0]*k+pw[e][:N+1-k] for e,k in monomials]
    return monomials,columns

def primitive_polynomial(vector,monomials,p):
    terms={(e,k):c for (e,k),c in zip(monomials,vector) if c}
    # Strip a common power of q and normalize one nonzero scalar. This is
    # not irreducible factorization or removal of general q-content.
    qpower=min(k for e,k in terms)
    terms={(e,k-qpower):c for (e,k),c in terms.items()}
    lead=terms[min(terms)]; inv=pow(lead,-1,p)
    return [[e,k,c*inv%p] for (e,k),c in sorted(terms.items())]

def fit_coordinates(t,zs,dt,p):
    """Common-D reconstruction by quotienting the numerator column span."""
    N=len(t)-1; monomials,columns=series_columns(t,dt-1,6,p)
    nc=len(columns)
    if nc>N-3: return {'status':'SKIPPED: fewer than four excess numerator equations'}
    mat=[[columns[j][n] for j in range(nc)]+[int(i==n) for i in range(N+1)] for n in range(N+1)]
    reduced,pivots=rref(mat,p,nc); rank=len(pivots)
    transform=[row[nc:] for row in reduced]
    # Each target column and its shifts are reduced once. All dependent
    # rows then impose a small COMMON denominator linear system.
    transformed=[]
    for j in range(291):
        seq=[zs[n][j] for n in range(N+1)]
        shifted=[[0]*k+seq[:N+1-k] for k in range(5)]
        transformed.append([[sum(a*b for a,b in zip(row,s))%p for row in transform] for s in shifted])
    for d in range(5):
        equations=([transformed[j][k][i] for k in range(1,d+1)]+[-transformed[j][0][i]]
                   for j in range(291) for i in range(rank,N+1))
        solution=solve_overdetermined(equations,d,p)
        if solution is None: continue
        den=[1]+solution; numerators=[]
        for j in range(291):
            transformed_target=[sum(den[k]*transformed[j][k][i] for k in range(d+1))%p for i in range(N+1)]
            assert not any(transformed_target[rank:])
            coeff=[0]*nc
            for i,pivot in enumerate(pivots): coeff[pivot]=transformed_target[i]
            numerators.append(coeff)
        return {'status':'HEURISTIC: all291 coordinates have a common-denominator finite SERIES fit',
                'denominator':den,'numerator_monomials_t_q':monomials,'numerator_coefficients':numerators,
                'numerator_column_rank':rank,'verified_through_order':N,'exact_identity_verified':False}
    return {'status':'FAILED: no all-coordinate representation at q-numerator<=6 and common denominator<=4',
            'numerator_column_rank':rank,'verified_through_order':N}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('checkpoints',nargs='+',type=Path)
    ap.add_argument('--coordinates',type=int,default=8)
    ap.add_argument('--try-representation',action='store_true')
    ap.add_argument('--max-seconds',type=int,default=240)
    a=ap.parse_args(); started=time.monotonic()
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    raw,_=normalized_jet(chart)
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/primitive_field_screen')).resolve()
    assert out.is_relative_to(RUN); out.mkdir(parents=True,exist_ok=True)
    for path in a.checkpoints:
        state=json.loads(path.read_text()); linear=state.get('free_path_order')==1
        p,N,zs,_=(validate_linear if linear else validate_checkpoint)(state,chart)
        assert N==32, 'this experiment is restricted to existing order32 data'
        expected=[[x.numerator*pow(x.denominator,-1,p)%p for x in row] for row in raw]
        assert zs[1]==expected[1]
        if linear: assert all(zs[n][j]==0 for n in range(2,N+1) for j in chart['free_coordinates'])
        else: assert zs[:7]==expected
        chosen=[]
        for j in chart['dependent_coordinates']:
            sequence=[row[j] for row in zs]
            if not small_rational(sequence,p): chosen.append(j)
            if len(chosen)==a.coordinates: break
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        result={'checkpoint':str(path.resolve()),'checkpoint_sha256':digest,
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'input_hashes':state['input_hashes'],'prime':p,'order':N,
                'free_path_order':1 if linear else 6,'chosen_coordinate_indices_zero_based':chosen,
                'selection':'first dependent coordinates failing individual rational den<=4,num<=d+6',
                'max_unknown_polynomial_coefficients':28,'minimum_excess_equations':4,
                'probes':[],'candidates':[],'exact_family_claim':False}
        print('CURVE','linear' if linear else 'sixjet','CHOSEN_COORDINATES_ZERO_BASED',chosen,flush=True)
        for j in chosen:
            sequence=[row[j] for row in zs]; valuation=next(n for n,x in enumerate(sequence) if x)
            variants=[('raw',sequence,0,0)]
            if valuation>0:
                normalized=sequence[valuation:]; leading=normalized[0]
                normalized=normalized[:]; normalized[0]=0
                variants.append(('valuation_removed',normalized,valuation,leading))
            for kind,t,v,leading in variants:
                available=len(t)
                for dt in range(2,5):
                    for dq in range(7):
                        unknowns=(dt+1)*(dq+1)
                        if unknowns>min(28,available-4): continue
                        if time.monotonic()-started>a.max_seconds:
                            result['stop_reason']='internal time gate'; break
                        monomials,columns=series_columns(t,dt,dq,p)
                        probe={'coordinate_zero_based':j,'variant':kind,'valuation_removed':v,
                               'subtracted_leading_coefficient':leading,'t_degree_bound':dt,'q_degree_bound':dq,
                               'unknown_coefficients':unknowns,'known_series_coefficients':available,
                               'excess_equations':available-unknowns}
                        if any(not any(c) for c in columns):
                            probe['status']='SKIPPED: zero truncated monomial column would create automatic nullspace'
                            result['probes'].append(probe); continue
                        matrix=[[col[n] for col in columns] for n in range(available)]
                        rank,basis=nullspace(matrix,p)
                        probe.update(rank=rank,nullity=len(basis),
                                     status='FAILED: no polynomial relation at this bidegree' if not basis else 'HEURISTIC: nonzero finite-series relation space')
                        result['probes'].append(probe)
                        if not basis: continue
                        print('RELATION_SPACE','coordinate',j,kind,'degree',dt,dq,'rank',rank,'nullity',len(basis),flush=True)
                        # Prefer a basis vector with unit dP/dt at the marked
                        # origin. Linear combinations cannot make this a unit
                        # if it is zero on every basis vector.
                        ordered=sorted(basis,key=lambda b:not any(e==1 and k==0 and c for (e,k),c in zip(monomials,b)))
                        for vector in ordered[:3]:
                            terms=primitive_polynomial(vector,monomials,p)
                            actual_dt=max(e for e,k,c in terms)
                            if actual_dt<2: continue
                            derivative=next((c for e,k,c in terms if e==1 and k==0),0)
                            candidate={'coordinate_zero_based':j,'variant':kind,'valuation_removed':v,
                                       'subtracted_leading_coefficient':leading,'polynomial_terms_t_q_coeff':terms,
                                       'actual_t_degree':actual_dt,'unit_t_derivative_at_origin':bool(derivative),
                                       't_derivative_at_origin':derivative,'verified_series_order':available-1,
                                       'status':'HEURISTIC candidate only; no irreducibility, branch, or exact Schur certificate'}
                            # Check the relation independently after removing q
                            # content, through exactly the order still implied.
                            pp=powers(t,actual_dt,p)
                            values=[sum(c*pp[e][n-k] for e,k,c in terms if k<=n)%p for n in range(available)]
                            original_q_content=min(k for (e,k),c in zip(monomials,vector) if c)
                            assert not any(values[:available-original_q_content])
                            candidate['verified_series_order']=available-original_q_content-1
                            if a.try_representation and derivative:
                                candidate['all_coordinate_representation']=fit_coordinates(t,zs,actual_dt,p)
                            result['candidates'].append(candidate)
                            # One preferred vector is enough for a first exact
                            # verification attempt; do not flood with multiples.
                            if derivative: break
                    if result.get('stop_reason'): break
                if result.get('stop_reason'): break
            dest=out/f'primitive_p{p}_{digest[:12]}_after_z{j}.json'
            assert not dest.exists(); dest.write_text(json.dumps(result)+'\n')
            print('COORDINATE_DONE',j,'candidate_count',len(result['candidates']),
                  'seconds',round(time.monotonic()-started,2),flush=True)
            if result.get('stop_reason'): break
        result.setdefault('stop_reason','completed prescribed finite search')
        result['seconds']=round(time.monotonic()-started,3)
        result['status']='HEURISTIC algebraic candidates; exact identity needed' if result['candidates'] else 'FAILED bounded primitive-algebraic recognition; no exact model found'
        dest=out/f'primitive_p{p}_{digest[:12]}_FINAL.json'
        assert not dest.exists(); dest.write_text(json.dumps(result)+'\n')
        print('FINAL',dest,result['status'],flush=True)
        if result['stop_reason']=='internal time gate': break

if __name__=='__main__': main()
