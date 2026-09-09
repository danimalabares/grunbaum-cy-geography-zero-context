#!/usr/bin/env python3
"""Independent tiny integer recheck of the 12 selected product-derivative rows.

No shared polynomial parser, pivot search, or determinant code is used.
The source coefficients are parsed as explicit sums of monomials, and each
selected entry is read by exponent subtraction rather than multiplication.
Only the saved 12x12 minor is checked; this is not another large rank job.
"""
import hashlib,json,os
from fractions import Fraction
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
CERT=RUN/'logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json'
SOURCE=REPO/'equations/deformation_data.json'
V='abcdefgh'

def parse(s):
    terms={}
    for term in s.replace('-','+-').split('+'):
        if not term: continue
        coefficient=1; exponents=[0]*8
        for factor in term.split('*'):
            if factor.startswith('-'):
                coefficient=-coefficient; factor=factor[1:]
            if factor in V and len(factor)==1:
                exponents[V.index(factor)]+=1
            elif '^' in factor:
                name,power=factor.split('^'); assert name in V
                exponents[V.index(name)]+=int(power)
            else: coefficient*=int(factor)
        key=tuple(exponents)
        terms[key]=terms.get(key,0)+coefficient
    return {m:c for m,c in terms.items() if c}

def monomials(d,n=8):
    if n==1: return [(d,)]
    return [(a,)+tail for a in range(d,-1,-1) for tail in monomials(d-a,n-1)]

def determinant(a):
    a=[[Fraction(x) for x in row] for row in a]; result=Fraction(1)
    for k in range(len(a)):
        j=next(j for j in range(k,len(a)) if a[j][k])
        if j!=k: a[j],a[k]=a[k],a[j];result=-result
        pivot=a[k][k]; result*=pivot
        for j in range(k+1,len(a)):
            factor=a[j][k]/pivot
            a[j]=[x-factor*y for x,y in zip(a[j],a[k])]
    assert result.denominator==1
    return int(result)

def main():
    certificate=json.loads(CERT.read_text()); data=json.loads(SOURCE.read_text())
    assert certificate['source_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    f=[parse(s) for s in data['generator_order']]
    assert all(len(row)==1 and list(row.values())==[1] for row in f)
    f=[next(iter(row)) for row in f]
    g=[parse(s) for s in data['first_order_corrections']]
    jet=[parse(s) for s in data['six_jet_coefficients'][1]]
    # Allow only the explicit parameter sign change, recording it below.
    sign=next((sign for sign in [1,-1] if all(
        {m:sign*c for m,c in a.items()}==b for a,b in zip(g,jet))),None)
    assert sign is not None, 'first-order/source-sixjet lineage mismatch'
    quadratics=monomials(2)
    pairs=[(i,j) for i in range(16) for j in range(i,16)]
    columns=[(i,j,m) for i,j in pairs for m in quadratics]
    central=[tuple(x+y+z for x,y,z in zip(f[i],f[j],m)) for i,j,m in columns]
    assert len(set(central))==1829
    rows=[tuple(m) for m in certificate['minor_rows_exponents']]
    assert len(set(rows))==12 and not set(rows).intersection(central)
    def entry(row,column):
        i,j,m=columns[column]
        left=tuple(x-y-z for x,y,z in zip(row,f[j],m))
        right=tuple(x-y-z for x,y,z in zip(row,f[i],m))
        return g[i].get(left,0)+g[j].get(right,0)
    matrix=[]
    for row in rows:
        values=[]
        for col in certificate['minor_columns']:
            c=col['index']; rep=col['central_representative_column']
            i,j,m=columns[c]
            assert [i+1,j+1]==col['generator_pair_1_based']
            assert list(m)==col['quadratic_monomial']
            assert central[c]==central[rep] and central.index(central[c])==rep
            values.append(entry(row,c)-entry(row,rep))
        matrix.append(values)
    assert matrix==certificate['first_order_schur_minor_integer_matrix']
    det=determinant(matrix)
    assert det==certificate['first_order_schur_minor_integer_determinant']==-(3**3)*(8**9)
    assert determinant([[sign*x for x in row] for row in matrix])==det
    result={'status':'COMPUTER-CERTIFIED independent exact minor verification',
      'integer_minor_determinant':det,'central_rank':1829,'extra_rank':12,
      'generic_product_rank_lower_bound':1841,
      'first_order_corrections_to_certified_sixjet_parameter_sign':sign,
      'method':'independent monomial parser, exponent-subtraction coefficients, rational Gaussian determinant',
      'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      'certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),
      'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'certificates'))
    out.mkdir(parents=True,exist_ok=True); dest=out/'independent_product_minor.json'
    if dest.exists(): assert json.loads(dest.read_text())==result
    else:dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2)); print(dest)

if __name__=='__main__':main()
