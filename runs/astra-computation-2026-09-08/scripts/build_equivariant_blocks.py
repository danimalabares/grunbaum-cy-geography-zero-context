#!/usr/bin/env python3
"""Exact S3 multiplicity blocks of the finite cubic Hilbert chart.

Uses an equivariant averaged section of central quartic multiplication.
No CAS, no Groebner basis. All changes of basis are rational and preserved.
The standard-representation block is computed on its transposition-fixed
line; equivariance supplies the identical companion block automatically.
Run only under the root-coordinated single-process resource guard.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parents[1]
DAY = RUN.parent / 'astra-daytime-2026-09-08'
sys.path.insert(0, str(DAY / 'scripts'))
from build_fixed_chart import F0, V, PERMS, act, monomials, times


def add(out, v, scalar=Q(1)):
    if scalar:
        for k, a in v.items():
            out[k] = out.get(k, Q(0)) + scalar*a
            if not out[k]: del out[k]
    return out


class Basis:
    """Sparse independent original vectors with an exact coordinate decoder."""
    def __init__(self, candidates):
        self.original = []
        self.echelon = {}
        for original in candidates:
            v = dict(original); expression = {}
            for pivot in sorted(self.echelon):
                if pivot in v:
                    a = v[pivot]; row, combo = self.echelon[pivot]
                    add(v, row, -a); add(expression, combo, -a)
            if not v: continue
            j = len(self.original); self.original.append(dict(original))
            expression[j] = Q(1)
            pivot = min(v); a = v[pivot]
            self.echelon[pivot] = ({k: c/a for k,c in v.items()},
                                    {k: c/a for k,c in expression.items()})

    def coordinates(self, original):
        v = dict(original); result = {}
        for pivot in sorted(self.echelon):
            if pivot in v:
                a = v[pivot]; row, combo = self.echelon[pivot]
                add(v, row, -a); add(result, combo, a)
        assert not v, ('vector outside multiplicity space', v)
        return result


def module_actions(objects, operation):
    lookup = {v:i for i,v in enumerate(objects)}
    return [[lookup[operation(v,p)] for v in objects] for p in PERMS]


def move(v, perm):
    return {perm[i]:a for i,a in v.items()}


def parity(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1


SIGNS = [parity(p) for p in PERMS]
TAU = 1
assert SIGNS[TAU] == -1


def project(v, actions, kind):
    average = {}
    for j,p in enumerate(actions):
        add(average, move(v,p), Q(SIGNS[j] if kind=='sign' else 1,6))
    if kind in ['trivial','sign']: return average
    assert kind == 'standard'
    out = {i:a/2 for i,a in v.items()}
    add(out, move(v,actions[TAU]), Q(1,2))
    return add(out, average, -1)


def encode_vector(v):
    return [[k,str(a)] for k,a in sorted(v.items())]


def new_matrix(n,m):
    return [[{} for _ in range(m)] for _ in range(n)]


def encode_matrix(matrix):
    return [[encode_vector(v) for v in row] for row in matrix]


def choose_independent_rows(rows, columns, p=101):
    basis = {}; selected = []
    for i, r in enumerate(rows):
        row = {j:(r.get(c,Q(0)).numerator *
                   pow(r.get(c,Q(0)).denominator,-1,p))%p
               for j,c in enumerate(columns)}
        row = {j:a for j,a in row.items() if a}
        for pivot in sorted(basis):
            if pivot in row:
                a = row[pivot]
                for j,b in basis[pivot].items():
                    row[j] = (row.get(j,0)-a*b)%p
                    if not row[j]: del row[j]
        if row:
            pivot=min(row); inv=pow(row[pivot],-1,p)
            basis[pivot]={j:a*inv%p for j,a in row.items()}
            selected.append(i)
    assert len(selected)==270, len(selected)
    return selected


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=RUN/'data/equivariant_blocks_QQ.json')
    args=ap.parse_args(); started=time.monotonic()
    chartpath=DAY/'data/fixed_chart.json'
    chart=json.loads(chartpath.read_text())
    columns=[tuple(v) for v in chart['multiplication_columns']]
    ideal_mons=[tuple(v) for v in chart['pivot_monomials']]
    std_mons=[tuple(v) for v in chart['standard_quartics']]
    quartics=ideal_mons+std_mons; quartic_index={m:i for i,m in enumerate(quartics)}
    images=[times(F0[i],j) for i,j in columns]
    representing=[[c for c,m in enumerate(images) if m==v] for v in ideal_mons]
    col_actions=module_actions(columns,lambda v,p:(F0.index(act(F0[v[0]],p)),p[v[1]]))
    ideal_actions=module_actions(ideal_mons,act)
    std_actions=module_actions(std_mons,act)
    kernel=[{c:Q(1),images.index(images[c]):Q(-1)} for c in chart['extra_columns']]
    tails=[tuple(v) for v in chart['tail_monomials']]
    coefficient={(i,tuple(m)):k for k,O in enumerate(chart['coefficient_orbits']) for i,m in O}

    def section(v):
        out={}
        for i,a in v.items():
            for c in representing[i]: out[c]=a/len(representing[i])
        return out

    def perturb(v):
        out={}
        for c,a in v.items():
            i,j=columns[c]
            for m in tails:
                z=coefficient[i,m]; r=quartic_index[times(m,j)]
                add(out.setdefault(z,{}),{r:a})
        return {z:r for z,r in out.items() if r}

    blocks={}; linear_rows=[]; row_locations=[]
    expected={'trivial':(21,5,47),'sign':(13,5,35),'standard':(32,10,75)}
    for kind,(ni,nk,nc) in expected.items():
        ib=Basis(project({j:Q(1)},ideal_actions,kind) for j in range(98))
        kb=Basis(project(v,col_actions,kind) for v in kernel)
        cb=Basis(project({j:Q(1)},std_actions,kind) for j in range(232))
        assert tuple(len(b.original) for b in [ib,kb,cb])==(ni,nk,nc)
        A=new_matrix(ni,ni); B=new_matrix(ni,nk)
        C=new_matrix(nc,ni); D=new_matrix(nc,nk)
        # Check the section and kernel on central monomials exactly.
        for v in ib.original:
            s=section(v); image={}
            for c,a in s.items(): add(image,{ideal_mons.index(images[c]):a})
            assert image==v
        for v in kb.original:
            image={}
            for c,a in v.items(): add(image,{ideal_mons.index(images[c]):a})
            assert not image
        for label,inputs,upper,lower in [('image',[section(v) for v in ib.original],A,C),
                                          ('kernel',kb.original,B,D)]:
            for col,v in enumerate(inputs):
                for z,w in perturb(v).items():
                    wi={i:a for i,a in w.items() if i<98}
                    wc={i-98:a for i,a in w.items() if i>=98}
                    for row,a in ib.coordinates(wi).items(): upper[row][col][z]=a
                    for row,a in cb.coordinates(wc).items(): lower[row][col][z]=a
        for i,row in enumerate(D):
            for j,e in enumerate(row):
                row_locations.append([kind,i,j]); linear_rows.append(e)
        blocks[kind]={'dimensions':[ni,nk,nc],
             'image_basis':[encode_vector(v) for v in ib.original],
             'kernel_basis_in_128_columns':[encode_vector(v) for v in kb.original],
             'standard_quartic_basis':[encode_vector(v) for v in cb.original],
             'A_minus_identity':encode_matrix(A),'B':encode_matrix(B),
             'C':encode_matrix(C),'D':encode_matrix(D)}
        print('BLOCK',kind,'DIMENSIONS',ni,nk,nc,'seconds',round(time.monotonic()-started,3),flush=True)
    selected=choose_independent_rows(linear_rows,chart['dependent_coordinates'])
    data={'status':'exact rational S3 multiplicity blocks; no fibre selected',
          'source_chart':str(chartpath),'source_chart_sha256':hashlib.sha256(chartpath.read_bytes()).hexdigest(),
          'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'section':'average all central column representatives of each quartic',
          'standard_primitive_projector':'(1+tau)/2 - (sum_g g)/6',
          'blocks':blocks,'free_coordinates':chart['free_coordinates'],
          'dependent_coordinates':chart['dependent_coordinates'],
          'selected_lower_equations':[row_locations[i] for i in selected],
          'lower_linear_rows':[encode_vector(v) for v in linear_rows],
          'rank_certificate_prime':101,'selected_rank_mod101':270,
          'auxiliary_variables':490,'full_lower_equations':1160,
          'selected_system_variables_without_q':760,
          'elapsed_seconds':round(time.monotonic()-started,3)}
    output=args.output.resolve(); assert output.is_relative_to(RUN)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():
        old=json.loads(output.read_text()); old.pop('elapsed_seconds',None)
        compare=dict(data); compare.pop('elapsed_seconds',None)
        assert old==compare, 'different existing block data; preserve it'
    else: output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print('PASS_EXACT_BLOCKS_AUX490_LOWER1160_RANK270',output,flush=True)


if __name__=='__main__': main()
