#!/usr/bin/env python3
"""Genuine mixed-characteristic coefficient arithmetic modulo pi^14.

Recompute the original free-path formal curve through q13 over Z/(101^2),
with pivots selected modulo101 and inverses taken modulo10201. Check all
6960 Schur coefficients at every order. This does NOT reuse F101 jets.
Substitute q=pi, pi^7=101, so pi^14=0. Reconstruct the equivariant kernel
graphs in blocks21/13/32 and verify all1650 full block equations DIRECTLY
in (Z/10201)[pi]/(pi^7-101). The finite exact algebraic point is specified
by the exporter; this file computes and verifies its actual approximation.
"""
import hashlib, json, os, time
from fractions import Fraction as Q
from pathlib import Path
from build_fixed_chart import F0, times
from fixed_curve_lift import normalized_jet
from check_rational_closure import build_identity_operator

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
PRIME=101
MOD=101**2
ORDER=13

def unit_lu(a):
    a=[row[:] for row in a]; perm=list(range(len(a))); n=len(a)
    for k in range(n):
        hit=next(i for i in range(k,n) if a[i][k]%PRIME)
        a[k],a[hit]=a[hit],a[k]; perm[k],perm[hit]=perm[hit],perm[k]
        inverse=pow(a[k][k],-1,MOD)
        for i in range(k+1,n):
            if a[i][k]:
                c=a[i][k]*inverse%MOD; a[i][k]=c
                for j in range(k+1,n): a[i][j]=(a[i][j]-c*a[k][j])%MOD
    return a,perm

def solve(lu,b):
    a,perm=lu; v=[b[i]%MOD for i in perm]; n=len(a)
    for i in range(n): v[i]=(v[i]-sum(a[i][j]*v[j] for j in range(i)))%MOD
    for i in range(n-1,-1,-1):
        assert a[i][i]%PRIME
        v[i]=(v[i]-sum(a[i][j]*v[j] for j in range(i+1,n)))*pow(a[i][i],-1,MOD)%MOD
    return v

def coefficient(c):
    c=Q(c); assert c.denominator%PRIME
    return c.numerator*pow(c.denominator,-1,MOD)%MOD

def mm(a,b):
    out=[[0]*len(b[0]) for _ in a]
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(b[k]):
                    if y: out[i][j]+=x*y
    return [[v%MOD for v in row] for row in out]

def minus(a,b):
    return [[(x-y)%MOD for x,y in zip(row,other)] for row,other in zip(a,b)]

def radd(a,b,scale=1): return [(x+scale*y)%MOD for x,y in zip(a,b)]

def rmul(a,b):
    out=[0]*7
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    e=i+j; out[e%7]+=x*y*(PRIME if e>=7 else 1)
    return [x%MOD for x in out]

def fold(sequence):
    assert len(sequence)==14
    return [(sequence[i]+PRIME*sequence[i+7])%MOD for i in range(7)]

def main():
    started=time.monotonic()
    chartpath=RUN/'data/fixed_chart.json'; blockpath=RUN/'data/equivariant_blocks_QQ.json'
    pointpath=RUN/'data/ramified_fibre_coefficients.json'
    chart=json.loads(chartpath.read_text()); blocks=json.loads(blockpath.read_text())
    point=json.loads(pointpath.read_text())
    assert point['certificate']['selected_jacobian_determinant_mod101']==19
    assert hashlib.sha256(chartpath.read_bytes()).hexdigest()==blocks['source_chart_sha256']
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/ramified_hensel_checkpoints')).resolve()
    assert out.is_relative_to(RUN); out.mkdir(parents=True,exist_ok=True)
    provenance={str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
                for path in [chartpath,blockpath,pointpath,REPO/'equations/deformation_data.json',
                             RUN/'scripts/fixed_curve_lift.py',RUN/'scripts/check_rational_closure.py',Path(__file__)]}
    raw,_=normalized_jet(chart); jet=[[coefficient(c) for c in row] for row in raw]
    dep=chart['dependent_coordinates']; free=chart['free_coordinates']
    selected=[30*i+j for i,j in chart['independent_equations']]
    jrows=[dict(row) for row in chart['linear_rows']]
    lu=unit_lu([[jrows[i].get(j,0)%MOD for j in dep] for i in selected])
    lin,edges=build_identity_operator(chart)
    lin=[{j:c for j,c in row.items() if c} for row in lin]
    assert lin[98*30:]==jrows
    cols=[tuple(c) for c in chart['multiplication_columns']]
    pivot_mons=[tuple(m) for m in chart['pivot_monomials']]
    U0=[[0]*30 for _ in range(98)]
    for k,c in enumerate(chart['extra_columns']):
        i,j=cols[c]; U0[pivot_mons.index(times(F0[i],j))][k]=1
    def mult(z,u):
        result=[[0]*30 for _ in range(330)]
        for r,c,k in edges:
            if z[k]:
                for j,b in enumerate(u[c]):
                    if b: result[r][j]+=z[k]*b
        return [[x%MOD for x in row] for row in result]
    zs=[[0]*291]; us=[U0]
    for n in range(1,ORDER+1):
        cross=[[0]*30 for _ in range(330)]
        for i in range(1,n):
            prod=mult(zs[i],us[n-i])
            cross=[[(a+b)%MOD for a,b in zip(row,other)] for row,other in zip(cross,prod)]
        z=[0]*291
        if n<=6:
            for j in free: z[j]=jet[n][j]
        rhs=[(cross[98+i//30][i%30]-sum(c*z[j] for j,c in jrows[i].items()))%MOD for i in selected]
        for j,c in zip(dep,solve(lu,rhs)): z[j]=c
        all_linear=[sum(c*z[j] for j,c in row.items())%MOD for row in lin]
        un=[[(all_linear[30*r+j]-cross[r][j])%MOD for j in range(30)] for r in range(98)]
        residual=[(all_linear[30*r+j]-cross[r][j])%MOD for r in range(98,330) for j in range(30)]
        assert not any(residual), ('nonzero Schur coefficient over Z/10201',n)
        if n<=6: assert z==jet[n], ('exact rational sixjet mismatch modulo10201',n)
        zs.append(z); us.append(un)
        checkpoint={'status':'COMPUTER-CERTIFIED formal coefficient jet over Z/(101^2)',
                    'residue_prime':PRIME,'coefficient_modulus':MOD,'q_order':n,
                    'z_coefficients':zs,'original_U_coefficients':us,
                    'all6960_Schur_equations_zero_through_q_order':n,'input_hashes':provenance}
        dest=out/f'formal_mod10201_q{n}.json'; assert not dest.exists()
        dest.write_text(json.dumps(checkpoint)+'\n')
        print('TRUE_MOD10201_ORDER',n,'ALL6960_ZERO','seconds',round(time.monotonic()-started,3),flush=True)
    # Rebuild the averaged-section U graphs without symbolic inverses.
    # A0=I means each coefficient is obtained by matrix convolution.
    block_series={}
    for kind,block in blocks['blocks'].items():
        ni,nk,nc=block['dimensions']; matrices={}
        for key in ['A_minus_identity','B','C','D']:
            encoded=block[key]
            matrices[key]=[[[sum(coefficient(c)*zs[n][j] for j,c in entry)%MOD for entry in row]
                            for row in encoded] for n in range(14)]
        ub=[]
        for n in range(14):
            value=[row[:] for row in matrices['B'][n]]
            for i in range(1,n+1): value=minus(value,mm(matrices['A_minus_identity'][i],ub[n-i]))
            ub.append(value)
            residual=[row[:] for row in matrices['D'][n]]
            for i in range(1,n+1): residual=minus(residual,mm(matrices['C'][i],ub[n-i]))
            assert not any(x for row in residual for x in row), ('block formal identity',kind,n)
        assert not any(x for row in ub[0] for x in row)
        block_series[kind]=ub
        print('TRUE_MOD10201_BLOCK',kind,'ALL_LOWER_Q_COEFFICIENTS_ZERO',flush=True)
    zpi=[fold([zs[n][j] for n in range(14)]) for j in range(291)]
    upi={kind:[[fold([series[n][i][j] for n in range(14)]) for j in range(len(series[0][0]))]
                for i in range(len(series[0]))] for kind,series in block_series.items()}
    assert all(value[0]%101==0 for value in zpi)
    # Verify the FULL equations by genuine ramified-ring operations, not
    # merely by re-reading the successful formal-q assertions above.
    equations_checked=0
    for kind,block in blocks['blocks'].items():
        ni,nk,nc=block['dimensions']; evaluated={}
        for key in ['A_minus_identity','B','C','D']:
            evaluated[key]=[[[sum(coefficient(c)*zpi[j][d] for j,c in entry)%MOD for d in range(7)]
                             for entry in row] for row in block[key]]
        A=evaluated['A_minus_identity']; U=upi[kind]
        for i in range(ni): A[i][i]=radd(A[i][i],[1,0,0,0,0,0,0])
        for i in range(ni):
            for j in range(nk):
                value=[0]*7
                for k in range(ni): value=radd(value,rmul(A[i][k],U[k][j]))
                value=radd(value,evaluated['B'][i][j],-1)
                assert not any(value), ('ramified top residual',kind,i,j,value)
                equations_checked+=1
        for i in range(nc):
            for j in range(nk):
                value=evaluated['D'][i][j][:]
                for k in range(ni): value=radd(value,rmul(evaluated['C'][i][k],U[k][j]),-1)
                assert not any(value), ('ramified lower residual',kind,i,j,value)
                equations_checked+=1
        print('DIRECT_RAMIFIED_RING_BLOCK',kind,'ALL_EQUATIONS_ZERO',flush=True)
    assert equations_checked==1650
    # Check the explicitly exported free-coordinate polynomials in this
    # ring, including their genuine coefficients modulo101^2.
    pi=[0,1,0,0,0,0,0]; powers=[[1,0,0,0,0,0,0]]
    for _ in range(7): powers.append(rmul(powers[-1],pi))
    assert powers[7]==[101,0,0,0,0,0,0]
    for item in point['lambda_definitions']:
        if 'pi_polynomial_coefficients' in item:
            value=[0]*7
            for n,c in enumerate(item['pi_polynomial_coefficients']):
                value=radd(value,[(coefficient(c)*x)%MOD for x in powers[n]])
            assert value==zpi[item['lambda_index_one_based']-1]
    result={'status':'COMPUTER-CERTIFIED actual ramified Hensel root approximation modulo pi^14',
            'ring':'(Z/10201Z)[pi]/(pi^7-101); pi^14=0',
            'coefficient_modulus':MOD,'ramification_degree':7,'uniformizer_precision':14,
            'basis':['1','pi','pi^2','pi^3','pi^4','pi^5','pi^6'],
            'representation':'each7-entry vector has canonical coefficients0..10200 in this basis',
            'lambda_values':zpi,'theta_values':[zpi[j] for j in dep],
            'averaged_section_U_values':upi,'all_full_block_equations_checked':equations_checked,
            'all_full_block_equations_zero_mod_pi14':True,
            'all6960_original_Schur_coefficients_zero_over_Z10201_through_q13':True,
            'original_exact_rational_sixjet_matches_mod10201':True,
            'not_reused_F101_order32_jet':True,
            'unique_exact_algebraic_point_presentation':str(pointpath.relative_to(RUN)),
            'exact_algebraic_point_exists_by':'unit-Jacobian Hensel theorem; approximation alone is not an all-orders proof',
            'input_hashes':provenance,'seconds':round(time.monotonic()-started,3)}
    dest=RUN/'data/ramified_hensel_pi14.json'; assert not dest.exists()
    dest.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('PASS_GENUINE_MIXED_CHARACTERISTIC_HENSEL_PI14',dest,flush=True)
    print('ALL1650_FULL_BLOCK_EQUATIONS_ZERO','seconds',round(time.monotonic()-started,3),flush=True)

if __name__=='__main__': main()
