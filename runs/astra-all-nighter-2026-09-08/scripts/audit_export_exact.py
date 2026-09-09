#!/usr/bin/env python3
"""Independent exact block transport, normalization, and saved pi56 checks.

This imports none of the construction scripts. Finite arithmetic supports
the exported identities; exact all-orders closure is a separate argument.
"""
import hashlib
import json
import os
import re
import time
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
OLD = RUN.parent / 'astra-computation-2026-09-08'
P = 101
MOD = P**8
V = 'abcdefgh'


def parse(s):
    out = defaultdict(Q)
    for t in re.findall(r'[+-]?[^+-]+', s.replace(' ', '')):
        c = Q(-1 if t.startswith('-') else 1)
        t = t.lstrip('+-')
        m = [0]*8
        for a in t.split('*'):
            if a and a[0] in V:
                v, _, n = a.partition('^')
                m[V.index(v)] += int(n or '1')
            else:
                c *= Q(a.strip('()'))
        out[tuple(m)] += c
    return {m:c for m,c in out.items() if c}


def add(out, key, value):
    out[key] = out.get(key, Q(0)) + value
    if not out[key]:
        del out[key]


def basis(rows):
    return [dict((i,Q(c)) for i,c in row) for row in rows]


def rank_mod(rows):
    piv = {}
    for row in rows:
        v = {j: int(c.numerator*pow(c.denominator,-1,P)) % P
             for j,c in row.items() if c}
        for j in sorted(piv):
            if v.get(j,0):
                a = v[j]
                for k,c in piv[j].items():
                    v[k] = (v.get(k,0)-a*c) % P
                    if not v[k]:
                        del v[k]
        if v:
            j = min(v); inv = pow(v[j],-1,P)
            piv[j] = {k:c*inv % P for k,c in v.items()}
    return len(piv)


def mulpi(a,b):
    c = [0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[(i+j)%7] += x*y*(P if i+j >= 7 else 1)
    return [x % MOD for x in c]


def main():
    start = time.monotonic()
    paths = [OLD/'data/fixed_chart.json', OLD/'data/equivariant_blocks_QQ.json',
             OLD/'data/ramified_fibre_coefficients.json', OLD/'data/ramified_hensel_pi56.json',
             REPO/'equations/deformation_data.json', Path(__file__)]
    chart, blocks, exp, checkpoint, src = [json.loads(p.read_text()) for p in paths[:-1]]
    hashes = {str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert hashes[str(paths[2].relative_to(REPO))] == '0e8c3bb4a62a77af4beb22182bc8e7dc771dabd09514a0597aaed5d8b61f0616'
    assert hashes[str(paths[3].relative_to(REPO))] == '693a9a4636d7f8fcf472c61a95202fa3ed783950b9539853d9b218d5a5c6aef2'
    f0 = [tuple(w.count(v) for v in V) for w in chart['F0']]
    assert f0 == [next(iter(parse(w))) for w in src['generator_order']]
    assert chart['F0'] == ['abf','abg','abh','acg','ach','adh','bdf','bdg','beg','cde','ceg','ceh','cfh','def','dfh','efg']
    tails = [tuple(m) for m in chart['tail_monomials']]
    mons = f0 + tails
    assert len(set(mons)) == 120 and all(sum(m)==3 for m in mons)
    lookup = {(i,tuple(m)):k for k,orb in enumerate(chart['coefficient_orbits']) for i,m in orb}
    assert len(lookup) == 1664
    perms = [[V.index(v) for v in w] for w in chart['group_images']]
    def act(m,p):
        out = [0]*8
        for i,n in enumerate(m): out[p[i]] = n
        return tuple(out)
    for (i,m),k in lookup.items():
        for p in perms:
            assert lookup[f0.index(act(f0[i],p)),act(m,p)] == k
    # Independently normalize by coefficient recursion H=F*P, so no inverse
    # construction from the original exporter is reused.
    raw = [[parse(s) for s in row] for row in src['six_jet_coefficients']]
    lead = [[[raw[n][i].get(m,Q(0)) for i in range(16)] for m in f0] for n in range(7)]
    assert lead[0] == [[Q(int(i==j)) for j in range(16)] for i in range(16)]
    norm = []
    for n in range(7):
        row = [dict(v) for v in raw[n]]
        for k in range(n):
            for j in range(16):
                for i in range(16):
                    c = lead[n-k][i][j]
                    if c:
                        for m,a in norm[k][i].items(): add(row[j],m,-a*c)
        for i in range(16):
            assert [row[i].get(m,Q(0)) for m in f0] == [Q(int(n==0 and i==j)) for j in range(16)]
        norm.append(row)
    zjet = []
    for n in range(7):
        z = []
        for orb in chart['coefficient_orbits']:
            values = {norm[n][i].get(tuple(m),Q(0)) for i,m in orb}
            assert len(values)==1
            z.append(values.pop())
        assert all(c.denominator % P for d in norm[n] for c in d.values())
        zjet.append(z)
    for item in exp['lambda_definitions']:
        j = item['lambda_index_one_based']-1
        if 'pi_polynomial_coefficients' in item:
            assert [Q(c) for c in item['pi_polynomial_coefficients']] == [zjet[n][j] for n in range(7)]
        else:
            assert chart['dependent_coordinates'][item['theta_index_one_based']-1] == j
    print('PASS_ORBIT_INDEXING_AND_INDEPENDENT_NORMALIZATION',flush=True)

    # Verify all291 coefficient operators directly in the supplied bases.
    cols = [tuple(c) for c in chart['multiplication_columns']]
    quartics = [tuple(m) for m in chart['pivot_monomials']+chart['standard_quartics']]
    qindex = {m:i for i,m in enumerate(quartics)}
    def times(m,j):
        n=list(m); n[j]+=1; return tuple(n)
    central = [qindex[times(f0[i],j)] for i,j in cols]
    assert len(set(central))==98
    fibres = [[c for c,r in enumerate(central) if r==i] for i in range(98)]
    all_j=[]; all_k=[]; all_b=[]
    tensor_entries = 0
    for kind,block in blocks['blocks'].items():
        ni,nk,nc = block['dimensions']
        eb=exp['shared_block_factors'][kind]
        for key in ['dimensions','A_minus_identity','B','C','D']: assert block[key]==eb[key]
        jb = basis(block['image_basis']); kb = basis(block['kernel_basis_in_128_columns']); bb = basis(block['standard_quartic_basis'])
        section=[]
        for v in jb:
            s={}
            for i,a in v.items():
                for c in fibres[i]: s[c]=a/len(fibres[i])
            section.append(s)
        for k in kb:
            im={}
            for c,a in k.items(): add(im,central[c],a)
            assert not im
        for c,v in enumerate(section+kb):
            actual={}
            for col,a in v.items():
                i,j=cols[col]
                for m in tails: add(actual,(qindex[times(m,j)],lookup[i,m]),a)
            expected={}
            top=block['A_minus_identity'] if c<ni else block['B']
            bottom=block['C'] if c<ni else block['D']
            cj=c if c<ni else c-ni
            for r,target in enumerate(jb):
                for k,a in top[r][cj]:
                    for mon,b in target.items(): add(expected,(mon,k),Q(a)*b)
            for r,target in enumerate(bb):
                for k,a in bottom[r][cj]:
                    for mon,b in target.items(): add(expected,(98+mon,k),Q(a)*b)
            assert actual==expected, ('basis transport mismatch',kind,c)
            tensor_entries += len(actual)
        all_j.extend(jb);all_k.extend(kb);all_b.extend(bb)
        if kind=='standard':
            # r-r² gives the independent companion line in each standard copy.
            p=next(p for p in perms if p!=list(range(8)) and all(p[p[p[i]]]==i for i in range(8)))
            p2=[p[p[i]] for i in range(8)]
            def companion(v,objects,operation):
                idx={m:i for i,m in enumerate(objects)}; out={}
                for i,a in v.items():
                    add(out,idx[operation(objects[i],p)],a)
                    add(out,idx[operation(objects[i],p2)],-a)
                return out
            all_j.extend(companion(v,quartics[:98],act) for v in jb)
            all_b.extend(companion(v,quartics[98:],act) for v in bb)
            def colact(c,p): return (f0.index(act(f0[c[0]],p)),p[c[1]])
            all_k.extend(companion(v,cols,colact) for v in kb)
        print('PASS_EXACT_BLOCK_TRANSPORT',kind,flush=True)
    assert [rank_mod(v) for v in [all_j,all_k,all_b]] == [98,30,232]
    # Every coefficient and supplied basis denominator is a101-unit.
    denoms=set()
    for block in blocks['blocks'].values():
        for key in ['A_minus_identity','B','C','D']:
            for row in block[key]:
                for entry in row:
                    for _,c in entry: denoms.add(Q(c).denominator)
        for key in ['image_basis','kernel_basis_in_128_columns','standard_quartic_basis']:
            for v in block[key]:
                for _,c in v: denoms.add(Q(c).denominator)
    assert all(d%P for d in denoms)
    assert [(e['block'],e['bottom_row_zero_based'],e['right_column_zero_based']) for e in exp['bordered_determinant_equations']] == [tuple(x) for x in blocks['selected_lower_equations']]

    zpi=checkpoint['lambda_values']; upi=checkpoint['averaged_section_U_values']
    assert checkpoint['coefficient_modulus']==MOD and checkpoint['uniformizer_precision']==56
    assert checkpoint['theta_values']==[zpi[j] for j in chart['dependent_coordinates']]
    assert all(v[0]%P==0 for v in zpi)
    def residue(c): c=Q(c);return c.numerator*pow(c.denominator,-1,MOD)%MOD
    for item in exp['lambda_definitions']:
        if 'pi_polynomial_coefficients' in item:
            assert zpi[item['lambda_index_one_based']-1] == [residue(c) for c in item['pi_polynomial_coefficients']]
    count=0
    for kind,block in blocks['blocks'].items():
        ni,nk,nc=block['dimensions']; mats={}
        for key in ['A_minus_identity','B','C','D']:
            mats[key]=[[[sum(residue(c)*zpi[k][d] for k,c in entry)%MOD for d in range(7)] for entry in row] for row in block[key]]
        U=upi[kind]
        for top,rows,key1,key2 in [(True,ni,'A_minus_identity','B'),(False,nc,'C','D')]:
            for i in range(rows):
                for j in range(nk):
                    value=[-v for v in mats[key2][i][j]]
                    if top: value=[a+b for a,b in zip(value,U[i][j])]
                    for k in range(ni): value=[a+b for a,b in zip(value,mulpi(mats[key1][i][k],U[k][j]))]
                    assert not any(a%MOD for a in value),('pi56 block residual',kind,top,i,j)
                    count+=1
    assert count==1650
    result={'status':'COMPUTER-CERTIFIED exact export/source agreement and saved mixed-characteristic identities',
            'coefficient_orbits_checked':291,'normalized_jet_orders_checked':7,
            'free_polynomial_coefficients_checked':147,'basis_transport_nonzero_tensor_entries_checked':tensor_entries,
            'full_basis_ranks_mod101':[98,30,232],'basis_and_block_denominators':sorted(denoms),
            'selected_equation_indices_checked':270,'mixed_characteristic_full_identities_checked':1650,
            'precision':'pi56 in (Z/101^8)[pi]/(pi^7-101)',
            'does_not_prove':'exact omitted-equation closure, algebraic equality from finite precision, or source smoothness identities',
            'input_hashes':hashes,'seconds':time.monotonic()-start}
    out=Path(os.environ['GS_RUN_OUTPUT'])/'exact_export_audit.json'
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
