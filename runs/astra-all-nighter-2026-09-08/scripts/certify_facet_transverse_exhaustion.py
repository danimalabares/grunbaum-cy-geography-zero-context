#!/usr/bin/env python3
"""Tiny exact exclusion of the other 17 facet-transverse line reductions.

Run under the root guard. This does not enumerate boundary reductions or
the complete line scheme. Characteristic-zero and characteristic101 checks
are both exact; all writes go to a fresh explicit run-owned directory.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp
import time

V = 'abcdefgh'


def parse(s):
    out = {}
    for term in s.replace('-', '+-').split('+'):
        if not term: continue
        c, e = 1, [0]*8
        for factor in term.split('*'):
            if factor.startswith('-'): c = -c; factor = factor[1:]
            if factor and factor[0] in V:
                name, _, degree = factor.partition('^')
                e[V.index(name)] += int(degree or 1)
            else: c *= int(factor)
        e = tuple(e); out[e] = out.get(e, 0) + c
    return {e:c for e,c in out.items() if c}


def laurent(numerator, denominator):
    den = [denominator.count(v) for v in V]
    return {tuple(a-b for a,b in zip(e,den)):c for e,c in parse(numerator).items()}


def encode(p): return [[list(e),c] for e,c in sorted(p.items())]


def det3(a):
    return sum((1 if (i-j)*(j-k)*(k-i)>0 else -1)*a[0][i]*a[1][j]*a[2][k]
               for i,j,k in itertools.permutations(range(3)))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args(); start=time.monotonic()
    run=Path(__file__).resolve().parents[1]; repo=run.parents[1]
    output=args.output.resolve(); assert output.is_relative_to(run) and not output.exists()
    source=repo/'equations/deformation_data.json'
    data=json.loads(source.read_text())
    central=[next(iter(parse(x))) for x in data['generator_order']]
    first=[parse(x) for x in data['six_jet_coefficients'][1]]
    assert first==[parse(x) for x in data['first_order_corrections']]
    supports=[{j for j,e in enumerate(m) if e} for m in central]
    facets=[set(F) for F in itertools.combinations(range(8),4)
            if not any(T<=set(F) for T in supports)]
    assert len(facets)==20
    # This explicit count also checks every triangle is shared by two facets.
    triangles={tuple(T) for F in facets for T in itertools.combinations(sorted(F),3)}
    assert all(sum(set(T)<=F for F in facets)==2 for T in triangles)
    ratios={}; monomial_exclusions=[]; remaining=[]
    for F in facets:
        name=''.join(V[j] for j in sorted(F)); outside=set(range(8))-F
        rows={}
        for v in sorted(outside):
            choices=[]
            for m,g in zip(central,first):
                os={j for j in outside if m[j]}
                restricted={e:c for e,c in g.items() if all(not e[j] for j in outside)}
                if len(os)>=2: assert not restricted
                if os=={v}:
                    choices.append({tuple(e[j]-m[j]+int(j==v) for j in range(8)):-c
                                    for e,c in restricted.items()})
            assert choices and all(p==choices[0] for p in choices)
            rows[V[v]]=choices[0]
        ratios[name]=rows
        witnesses=[]
        for outside_var,p in rows.items():
            if len(p)!=1: continue
            exponent,coefficient=next(iter(p.items()))
            poles=[j for j,n in enumerate(exponent) if n<0]
            if len(poles)==1 and exponent[poles[0]]==-1:
                assert coefficient and coefficient%101
                assert all(exponent[j]==0 for j in outside)
                witnesses.append({'outside_variable':outside_var,
                    'pole_face_coordinate':V[poles[0]],'coefficient':coefficient,
                    'laurent_exponents':list(exponent)})
        if witnesses: monomial_exclusions.append({'facet':name,'witness':witnesses[0]})
        else: remaining.append(name)
    assert len(monomial_exclusions)==15
    assert set(remaining)=={'abce','aegh','bcgh','bdeh','befh'}
    expected={
        'bdeh':{'a':laurent('-8*b*d-9*d*e','h'),
                'c':laurent('-9*b*d-8*d*h','e'),'f':{},
                'g':laurent('-8*d*e-9*d*h','b')},
        'befh':{'a':laurent('-9*e*f-8*f*h','b'),
                'c':laurent('-9*b*f-8*e*f','h'),'d':{},
                'g':laurent('-8*b*f-9*f*h','e')}}
    assert all(ratios[F]==rows for F,rows in expected.items())
    points={'bdeh':[[-9,8,0],[-8,0,9],[0,-9,8]],
            'befh':[[0,-8,9],[-8,9,0],[-9,0,8]]}
    cyclic=[]
    for F,p in points.items():
        d=det3(p); assert abs(d)==217 and d%101
        cyclic.append({'facet':F,'projected_coordinates':'b,e,h',
                       'three_required_points':p,'determinant':d,
                       'determinant_mod101':d%101})
    # Rational elimination in the remaining representative facet abce.
    w,z=sp.symbols('w z')
    u=-(4*w*w+w+10)/(3*w); v=(-2-4*z)/3
    C=(3+2*w)*v-(4+2*z)*u
    assert sp.cancel(3*w*C-2*(6*w*w-w+20-5*(w-2)*z))==0
    assert (6*2*2-2+20)==42 and 42%101
    zz=(6*w*w-w+20)/(5*(w-2)); vv=-2*(4*w*w+w+10)/(5*(w-2))
    boundary=sp.cancel(u*zz-vv*w)
    assert sp.cancel(boundary-(w-20)*(4*w*w+w+10)/(15*w*(w-2)))==0
    D=10*boundary**2-w*((3+u)*zz-(4+vv)*w)
    P2=19*w*w-2*w+40; P3=w**3-16*w*w-10*w-50
    claimed=2*(w-20)*P2*P3/(45*w*w*(w-2)**2)
    assert sp.cancel(D-claimed)==0
    excluded=w*(w-2)*(w-20)*(4*w*w+w+10)*(6*w*w-w+20)
    for modulus in [None,101]:
        kwargs={'domain':sp.QQ} if modulus is None else {'modulus':modulus}
        p=sp.Poly(P2*P3,w,**kwargs)
        assert sp.gcd(p,p.diff()).degree()==0
        assert sp.gcd(p,sp.Poly(excluded,w,**kwargs)).degree()==0
    assert sp.Poly(P2-19*(w-5)*(w-27),w,modulus=101).is_zero
    assert sp.Poly(P3-(w-9)*(w*w-7*w+28),w,modulus=101).is_zero
    assert not any((x*x-7*x+28)%101==0 for x in range(101))
    sigma=[0,7,6,5,4,3,2,1]; tau=[2,4,0,5,1,3,6,7]
    permutations=[list(range(8)),sigma,[tau[sigma[i]] for i in range(8)]]
    image_facets=[]
    for p in permutations:
        assert {frozenset(p[i] for i in T) for T in supports}==set(map(frozenset,supports))
        image_facets.append(''.join(sorted(V[p[V.index(v)]] for v in 'abce')))
    assert image_facets==['abce','aegh','bcgh']
    result={'status':'COMPUTER-CERTIFIED exhaustive facet-transverse first-order classification',
        'scope':'Only reductions in one coordinate facet meeting its four coordinate faces at distinct triangle-torus points; boundary reductions remain open.',
        'fields':['Q','algebraic closure of F101'],
        'facets':[''.join(V[j] for j in sorted(F)) for F in facets],
        'normal_ratios':{F:{v:encode(p) for v,p in rows.items()} for F,rows in ratios.items()},
        'fifteen_monomial_pole_exclusions':monomial_exclusions,
        'two_cyclic_collinearity_exclusions':cyclic,
        'remaining_facet_orbit':image_facets,
        'representative_equations':['2+3*v+4*z','10+w+3*u*w+4*w^2',
            '(3+2*w)*v-(4+2*z)*u','10*(u*z-v*w)^2-w*((3+u)*z-(4+v)*w)'],
        'representative_rational_solution':{'u':str(u),'v':str(vv),'z':str(zz)},
        'remaining_polynomials':[str(P2),str(P3)],
        'five_simple_transverse_solutions_per_remaining_facet':True,
        'first_order_facet_transverse_total':15,
        'actual_fibre_exhaustion_requires':['exact five Hensel line certificates and invariant fibre',
            'outside coordinates divisible by pi via central normal injectivity and minimum valuation',
            'Hensel uniqueness after any ramified coefficient extension'],
        'input_hashes':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [source,Path(__file__)]},
        'elapsed_seconds':round(time.monotonic()-start,3)}
    output.mkdir(parents=True)
    (output/'facet_transverse_exhaustion.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_20_FACETS_15_MONOMIAL_2_CYCLIC_3_FACETS_WITH_5_LINES_EACH',flush=True)
    print('PASS_CHAR0_AND_CHAR101_EXHAUSTION',output,'seconds',round(time.monotonic()-start,3),flush=True)


if __name__=='__main__': main()
