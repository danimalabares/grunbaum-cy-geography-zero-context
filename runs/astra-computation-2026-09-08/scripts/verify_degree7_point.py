#!/usr/bin/env python3
"""Exact prospective Q(pi) verification; pi^7=101.

Run only after ALL dependent Hensel coefficient entries reconstruct.
This performs exact Schur solves in Q[T]/(T^7-101), checks ALL1650 block
equations and the p-adic root selector. A passed fit alone is never used
as a certificate. Rational coefficient growth is explicitly bounded.
"""
import argparse, hashlib, json, time
from fractions import Fraction as Q
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]
ZERO=(Q(0),)*7
ONE=(Q(1),)+(Q(0),)*6

class ArithmeticGrowth(Exception): pass

def add(a,b,scale=1): return tuple(x+scale*y for x,y in zip(a,b))

def mul(a,b):
    out=[Q(0)]*7
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    e=i+j; out[e%7]+=x*y*(101 if e>=7 else 1)
    return tuple(out)

def gate(v,bits):
    if any(max(abs(x.numerator).bit_length(),x.denominator.bit_length())>bits for x in v):
        raise ArithmeticGrowth('exact number-field rational coefficient exceeded bit gate')

def inverse(v,bits):
    assert any(v), 'division by zero in Q(pi)'
    cols=[]
    for j in range(7):
        col=[Q(0)]*7
        for i,x in enumerate(v):
            e=i+j; col[e%7]=x*(101 if e>=7 else 1)
        cols.append(col)
    matrix=[[cols[j][i] for j in range(7)]+[Q(int(i==0))] for i in range(7)]
    for k in range(7):
        hit=next(i for i in range(k,7) if matrix[i][k])
        matrix[k],matrix[hit]=matrix[hit],matrix[k]
        pivot=matrix[k][k]; matrix[k]=[x/pivot for x in matrix[k]]
        for i in range(7):
            if i!=k and matrix[i][k]:
                c=matrix[i][k]; matrix[i]=[x-c*y for x,y in zip(matrix[i],matrix[k])]
                gate(matrix[i],bits)
    result=tuple(matrix[i][7] for i in range(7)); gate(result,bits)
    assert mul(v,result)==ONE
    return result

def solve(A,B,bits):
    n=len(A); nk=len(B[0]); mat=[row[:]+rhs[:] for row,rhs in zip(A,B)]
    for k in range(n):
        hit=next(i for i in range(k,n) if any(mat[i][k]))
        mat[k],mat[hit]=mat[hit],mat[k]
        inv=inverse(mat[k][k],bits)
        for j in range(k,n+nk): mat[k][j]=mul(mat[k][j],inv); gate(mat[k][j],bits)
        assert mat[k][k]==ONE
        for i in range(k+1,n):
            c=mat[i][k]
            if any(c):
                for j in range(k+1,n+nk): mat[i][j]=add(mat[i][j],mul(c,mat[k][j]),-1); gate(mat[i][j],bits)
                mat[i][k]=ZERO
    U=[[ZERO for _ in range(nk)] for _ in range(n)]
    for i in range(n-1,-1,-1):
        for j in range(nk):
            value=mat[i][n+j]
            for k in range(i+1,n): value=add(value,mul(mat[i][k],U[k][j]),-1)
            gate(value,bits); U[i][j]=value
    return U

def verify(candidate,max_bits=16384):
    started=time.monotonic()
    pointpath=RUN/'data/ramified_fibre_coefficients.json'
    point=json.loads(pointpath.read_text())
    z=[tuple(Q(c) for c in row) for row in candidate['lambda_coefficients_QQ_pi_basis']]
    assert len(z)==291 and all(len(v)==7 for v in z)
    assert all(c.denominator%101 for v in z for c in v)
    assert all(v[0].numerator%101==0 for v in z), 'wrong p-adic origin branch'
    for item in point['lambda_definitions']:
        if 'pi_polynomial_coefficients' in item:
            assert z[item['lambda_index_one_based']-1]==tuple(Q(c) for c in item['pi_polynomial_coefficients'])
    def linear(encoded):
        result=ZERO
        for j,c in encoded: result=add(result,tuple(Q(c)*x for x in z[j]))
        gate(result,max_bits); return result
    count=0; solved={}
    for kind,block in point['shared_block_factors'].items():
        ni,nk,nc=block['dimensions']
        matrices={key:[[linear(entry) for entry in row] for row in block[key]]
                  for key in ['A_minus_identity','B','C','D']}
        A=matrices['A_minus_identity']
        for i in range(ni): A[i][i]=add(A[i][i],ONE)
        U=solve(A,matrices['B'],max_bits)
        for i in range(ni):
            for j in range(nk):
                value=ZERO
                for k in range(ni): value=add(value,mul(A[i][k],U[k][j]))
                assert value==matrices['B'][i][j], ('exact top residual',kind,i,j)
                count+=1
        for i in range(nc):
            for j in range(nk):
                value=matrices['D'][i][j]
                for k in range(ni): value=add(value,mul(matrices['C'][i][k],U[k][j]),-1)
                assert value==ZERO, ('exact Schur residual',kind,i,j)
                count+=1
        solved[kind]=[[[str(c) for c in entry] for entry in row] for row in U]
        print('EXACT_DEGREE7_BLOCK',kind,'ALL_IDENTITIES_ZERO',flush=True)
    assert count==1650
    return {'status':'COMPUTER-CERTIFIED exact coefficient point over Q(pi), pi^7=101',
            'field_degree_over_Q':7,'lambda_coefficients_QQ_pi_basis':[[str(c) for c in row] for row in z],
            'averaged_section_U_QQ_pi_basis':solved,'all1650_full_block_identities_exact':True,
            'origin_Hensel_branch_verified':True,'identification_with_exact_root':'unit-Jacobian Hensel uniqueness',
            'point_presentation_sha256':hashlib.sha256(pointpath.read_bytes()).hexdigest(),
            'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'max_bits':max_bits,'seconds':round(time.monotonic()-started,3)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('candidate',type=Path)
    ap.add_argument('--output',type=Path,required=True); ap.add_argument('--max-bits',type=int,default=16384)
    a=ap.parse_args(); assert not a.output.exists()
    candidate=json.loads(a.candidate.read_text()); result=verify(candidate,a.max_bits)
    result['candidate_sha256']=hashlib.sha256(a.candidate.read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('EXACT_DEGREE7_POINT_VERIFIED',a.output,flush=True)

if __name__=='__main__': main()
