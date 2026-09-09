#!/usr/bin/env python3
"""Independent F101 replay and bounded exact-Q preparation of the same locus.

Rebuilds the123-variable necessary equations overQ from frozen inputs;
compares their reduction with J016, independently checks all G2 row
identities and all20 polynomial peels, and checks the Singular export.
Then performs constant G2 elimination and bounded constant-unit peeling
overQ. It never runs CAS. The generated Singular file uses explicit
sum I[j]*T[j,1], never Singular's misleading ideal*matrix operation.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import time

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'


class Limit(Exception):pass


class Arithmetic:
    def __init__(self,p=0):self.p=p
    def scalar(self,x):
        a=Q(x)
        return a.numerator*pow(a.denominator,-1,self.p)%self.p if self.p else a
    def reduce(self,x):return x%self.p if self.p else x
    def inverse(self,x):return pow(x,-1,self.p) if self.p else 1/x
    def add(self,a,b,c=1):
        z=dict(a)
        for m,v in b.items():
            z[m]=self.reduce(z.get(m,0)+c*v)
            if not z[m]:del z[m]
        return z
    def scale(self,a,c):return {m:self.reduce(v*c) for m,v in a.items() if self.reduce(v*c)}
    def normalize(self,a):
        if not a:return a
        first=min(a,key=lambda m:(len(m),m))
        return self.scale(a,self.inverse(a[first]))
    def unique(self,polys):
        seen=set();out=[]
        for poly in polys:
            if not poly:continue
            q=self.normalize(poly);key=tuple(sorted(q.items()))
            if key not in seen:seen.add(key);out.append(q)
        return out
    def multiply(self,a,b,max_terms=2000,max_degree=4):
        out={}
        for m,x in a.items():
            for n,y in b.items():
                k=tuple(sorted(m+n))
                if len(k)>max_degree:raise Limit('degree_cap')
                out[k]=self.reduce(out.get(k,0)+x*y)
                if not out[k]:del out[k]
            if len(out)>max_terms:raise Limit('polynomial_term_cap')
        return out
    def substitute(self,q,v,rhs,max_terms=2000,max_degree=4):
        powers=[{():self.scalar(1)}];out={}
        for m,a in q.items():
            k=m.count(v)
            while len(powers)<=k:powers.append(self.multiply(powers[-1],rhs,max_terms,max_degree))
            rest=tuple(j for j in m if j!=v)
            out=self.add(out,self.multiply({rest:a},powers[k],max_terms,max_degree))
            if len(out)>max_terms:raise Limit('polynomial_term_cap')
        return out


def encode(q):return [[list(m),str(a)] for m,a in sorted(q.items())]
def decode(q,ar):return {tuple(m):ar.scalar(a) for m,a in q}
def elinear(row):return [[j,str(a)] for j,a in sorted(row.items())]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--modular',type=Path,default=RUN/'data/combined_matrix_necessary')
    ap.add_argument('--max-seconds',type=float,default=120)
    ap.add_argument('--max-total-terms',type=int,default=100000)
    ap.add_argument('--max-polynomial-terms',type=int,default=2000)
    ap.add_argument('--max-degree',type=int,default=4)
    ap.add_argument('--max-peels',type=int,default=72)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    ar=Arithmetic();fp=Arithmetic(101)
    def gate():
        if time.monotonic()-started>args.max_seconds:raise Limit('internal_time_limit')
    def dump(name,data):
        p=out/name;assert not p.exists()
        p.write_text(json.dumps(data,separators=(',',':'))+'\n');return p
    source_files=[args.modular/'original_bilinear_system.json',args.modular/'G2_elimination_certificate.json',
                  args.modular/'reduced_locus.json',args.modular/'necessary_locus.sing']
    original=json.loads(source_files[0].read_text());elim=json.loads(source_files[1].read_text())
    reduced=json.loads(source_files[2].read_text())
    basepath=RUN/'data/optimized_quadratic_generators/quadratic_generator_certificate.json'
    matrixpath=RUN/'data/linear_matrix_denominator/linear_matrix_denominator_certificate.json'
    chartpath=OLD/'data/fixed_chart.json';blockpath=OLD/'data/equivariant_blocks_QQ.json'
    for p in [basepath,matrixpath,chartpath,blockpath]:
        assert original['input_sha256'][str(p.relative_to(REPO))]==hashlib.sha256(p.read_bytes()).hexdigest()
    base=json.loads(basepath.read_text());matrix=json.loads(matrixpath.read_text())
    chart=json.loads(chartpath.read_text());blocks=json.loads(blockpath.read_text())
    basis=[[Q(a) for a in v] for v in base['second_coefficient_kernel_basis']]
    beq=[[Q(a) for a in row] for row in base['affine_equations_coefficients_then_constant']]
    meq=[[Q(a) for a in row] for row in matrix['equations']]
    orbits=matrix['endomorphism_basis_pair_orbits_zero_based_source_target']
    assert orbits==original['generator_matrix_pair_orbits']
    lookup={(i,tuple(m)):j for j,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    D=[]
    for block in blocks['blocks'].values():
        D.extend({int(j):Q(a) for j,a in cell} for row in block['D'] for cell in row)
    polynomials=[]
    for a,b in zip(beq,meq):
        assert a[-1]==b[-1]
        q={():a[-1]} if a[-1] else {}
        q.update({(i,):a[i] for i in range(21) if a[i]})
        q.update({(21+i,):b[i] for i in range(51) if b[i]})
        polynomials.append(q)
    # Independent construction: first multiply each of the21 tangent rows
    # by each generator endomorphism; then apply the original linear D.
    for k,orbit in enumerate(orbits):
        gate();transformed=[]
        for O in chart['coefficient_orbits']:
            target,m=O[0]
            indices=[lookup[i,tuple(m)] for i,j in orbit if j==target]
            transformed.append([sum(v[j] for j in indices) for v in basis])
        for row,q in zip(D,polynomials):
            for s in range(21):
                a=sum(c*transformed[j][s] for j,c in row.items())
                if a:q[s,21+k]=a
    hrows=[{j:a for j,a in enumerate(row[51:102]) if a} for row in meq]
    ppolys=[{m:fp.scalar(a) for m,a in q.items() if fp.scalar(a)} for q in polynomials]
    phrows=[{j:fp.scalar(a) for j,a in row.items() if fp.scalar(a)} for row in hrows]
    assert ppolys==[decode(q,fp) for q in original['polynomials']]
    assert phrows==[dict(row) for row in original['G2_rows']]
    exact_path=dump('original_system_QQ.json',{
        'field':'Q','variable_names':original['residual_variable_names'],
        'G2_names':original['second_generator_matrix_names'],
        'polynomials':list(map(encode,polynomials)),'G2_rows':list(map(elinear,hrows)),
        'formula':original['equation_formula'],'scope':original['scope'],
        'input_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in [basepath,matrixpath,chartpath,blockpath,Path(__file__)]}})
    # Check every stored constant-operation certificate by direct summation.
    for _,h,q,combo in elim['G2_echelon']:
        hh={};qq={}
        for i,a in combo:hh=fp.add(hh,phrows[i],a);qq=fp.add(qq,ppolys[i],a)
        assert hh==dict(h) and qq==decode(q,fp)
    constraints=[]
    for _,q,combo in elim['constraints']:
        gate();hh={};qq={}
        for i,a in combo:hh=fp.add(hh,phrows[i],a);qq=fp.add(qq,ppolys[i],a)
        assert not hh and qq==decode(q,fp);constraints.append(qq)
    current=fp.unique(constraints);remaining=set(range(72))
    for peel in reversed(reduced['peeling_reconstruction_reverse_order']):
        gate();v=peel['variable'];source=decode(peel['source_equation_at_stage'],fp)
        rhs=decode(peel['rhs'],fp);assert source in current
        assert (v,) in source and all(v not in m for m in source if m!=(v,))
        expected=fp.scale({m:a for m,a in source.items() if m!=(v,)},-fp.inverse(source[v,]))
        assert expected==rhs
        skipped=False;nextpolys=[]
        for q in current:
            if not skipped and q==source:skipped=True;continue
            nextpolys.append(fp.substitute(q,v,rhs,args.max_polynomial_terms,args.max_degree))
        current=fp.unique(nextpolys);remaining.remove(v)
    assert current==[decode(q,fp) for q in reduced['equations']]
    assert sorted(remaining)==reduced['remaining_variable_indices']
    names=original['residual_variable_names']
    def expr(q):
        return '+'.join('('+str(a)+')'+''.join('*'+names[v] for v in m) for m,a in sorted(q.items())) or '0'
    # Compare exact generator text with the actual CAS input, not just JSON.
    old_expr=lambda q:'+'.join(str(a)+''.join('*'+names[v] for v in m) for m,a in sorted(q.items())) or '0'
    text=source_files[3].read_text()
    assert 'ring r=101,('+','.join(names[v] for v in sorted(remaining))+'),dp;' in text
    assert 'ideal J='+',\n'.join(old_expr(q) for q in current)+';' in text
    assert text.count('ideal J=')==1 and 'ideal G=std(J);' in text
    expected_script='\n'.join([
        '// Necessary q3 locus overF101 only. No flat family or smooth fibre certified.',
        'ring r=101,('+','.join(names[v] for v in sorted(remaining))+'),dp;',
        'ideal J='+',\n'.join(old_expr(q) for q in current)+';',
        'print("INPUT_EQUATIONS"); size(J);','ideal G=std(J);',
        'print("GROEBNER_DIMENSION"); dim(G);',
        'print("GROEBNER_BASIS_SIZE"); size(G);','G;','quit;'])+'\n'
    assert text==expected_script
    fp_report={'status':'COMPUTER-CERTIFIED independent replay of original equations,allG2row identities,all20peels,andCASgenerators',
               'G2_rows_checked':len(elim['G2_echelon']),'constraint_rows_checked':len(elim['constraints']),
               'peels_checked':len(reduced['peeling_reconstruction_reverse_order']),
               'final_equations_checked':len(current),
               'constant_one_explanation':'Each nonzero constant is the first coefficient in normalization and is divided out as a nonzero scalar; this does not discard other monomials.',
               'polynomials_with_constant_one':sum(q.get(())==1 for q in current),
               'unit_polynomial_before_CAS':any(set(q)=={()} for q in current),
               'claim_scope':'Together with a valid Singular unit certificate this excludesF101 solutions, and characteristic-zero solutions integral at101 in these123 parameters. It does not exclude arbitrary bad-denominatorQ solutions.',
               'input_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
               'seconds':time.monotonic()-started}
    dump('independent_F101_replay.json',fp_report)
    print('PASS_INDEPENDENT_F101_REPLAY','SECONDS',time.monotonic()-started,flush=True)
    # New exact rational reduction, with no inference from the modular answer.
    qe={};qc=[];nextrow=0;phase='QQ_G2';stop=None;qpeels=[];qremaining=set(range(72));qcurrent=[]
    try:
        for i,(h0,q0) in enumerate(zip(hrows,polynomials)):
            gate();h=dict(h0);q=dict(q0);combo={i:Q(1)}
            for pivot in sorted(qe):
                if pivot not in h:continue
                a=h[pivot];old,p,tr=qe[pivot]
                h=ar.add(h,old,-a);q=ar.add(q,p,-a);combo=ar.add(combo,tr,-a)
                if len(q)>args.max_polynomial_terms:raise Limit('QQ_G2_polynomial_cap')
            if h:
                pivot=min(h);inv=1/h[pivot]
                qe[pivot]=(ar.scale(h,inv),ar.scale(q,inv),ar.scale(combo,inv))
            elif q:qc.append((i,q,combo))
            nextrow=i+1
            if sum(len(p) for _,p,_ in qc)+sum(len(p) for _,p,_ in qe.values())>args.max_total_terms:
                raise Limit('QQ_G2_total_term_cap')
        # Direct independent summation verifies every rational row relation.
        for _,(h,q,combo) in qe.items():
            gate();hh={};qq={}
            for i,a in combo.items():hh=ar.add(hh,hrows[i],a);qq=ar.add(qq,polynomials[i],a)
            assert hh==h and qq==q
        for _,q,combo in qc:
            gate();hh={};qq={}
            for i,a in combo.items():hh=ar.add(hh,hrows[i],a);qq=ar.add(qq,polynomials[i],a)
            assert not hh and qq==q
        dump('G2_elimination_QQ.json',{
            'status':'COMPUTER-CERTIFIED exactQ constant elimination; every row identity directly checked',
            'original_system':str(exact_path),'rank':len(qe),
            'free_G2_indices':[j for j in range(51) if j not in qe],
            'echelon':[[p,elinear(h),encode(q),elinear(tr)] for p,(h,q,tr) in sorted(qe.items())],
            'constraints':[[i,encode(q),elinear(tr)] for i,q,tr in qc],
            'reconstruction':'h_p=-q_p-sum_{j>p} a_pj*h_j; evaluate pivotindices in decreasing order, leaving nonpivotG2 free.'})
        phase='QQ_peeling';qcurrent=ar.unique([q for _,q,_ in qc])
        for stage in range(args.max_peels):
            gate()
            if any(set(q)=={()} for q in qcurrent):stop='exact_Q_unit_equation';break
            occurrences={v:sum(sum(v in m for m in q) for q in qcurrent) for v in qremaining}
            candidates=[]
            for i,q in enumerate(qcurrent):
                nonlinear={v for m in q if len(m)>1 for v in m}
                for m,a in q.items():
                    if len(m)==1 and m[0] not in nonlinear:
                        candidates.append((occurrences[m[0]]*max(1,len(q)-1),len(q),i,m[0],a))
            accepted=False
            for _,_,i,v,a in sorted(candidates):
                gate();rhs=ar.scale({m:b for m,b in qcurrent[i].items() if m!=(v,)},-1/a)
                try:
                    proposed=[];total=0
                    for j,q in enumerate(qcurrent):
                        if j==i:continue
                        new=ar.substitute(q,v,rhs,args.max_polynomial_terms,args.max_degree)
                        total+=len(new)
                        if total>args.max_total_terms:raise Limit('QQ_peel_total_term_cap')
                        proposed.append(new)
                except Limit:continue
                qpeels.append({'variable':v,'source':encode(qcurrent[i]),'rhs':encode(rhs)})
                qcurrent=ar.unique(proposed);qremaining.remove(v);accepted=True
                print('QQ_PEEL',len(qpeels),'VARS',len(qremaining),'EQUATIONS',len(qcurrent),
                      'TERMS',sum(map(len,qcurrent)),flush=True)
                break
            if not accepted:stop='no_constant_unit_peel_within_caps';break
        else:stop='max_peels_reached'
    except Limit as e:
        stop=str(e)
    # Even a cap preserves the exact current state; no partial result becomes
    # a nonexistence theorem. OriginalQ equations are already independently saved.
    state={'phase':phase,'stop_reason':stop,'next_original_row':nextrow,
           'G2_rank':len(qe),'original_system':str(exact_path),
           'G2_echelon':[[p,elinear(h),encode(q),elinear(tr)] for p,(h,q,tr) in sorted(qe.items())],
           'constraints':[[i,encode(q),elinear(tr)] for i,q,tr in qc],
           'current_equations':list(map(encode,qcurrent)),
           'remaining_variables':sorted(qremaining),'reverse_peel_reconstruction':list(reversed(qpeels))}
    dump('QQ_checkpoint.json',state)
    if phase=='QQ_peeling':
        ringvars=','.join(names[v] for v in sorted(qremaining)) or 'dummy'
        lines=['// ExactQ necessary orderthree locus. G2/peel maps are separately certified.',
               'ring r=0,('+ringvars+'),dp;',
               'ideal I='+(',\n'.join(expr(q) for q in qcurrent) or '0')+';',
               'matrix T=lift(I,ideal(1));',
               'poly value=0;',
               'for(int j=1;j<=nrows(T);j++){value=value+I[j]*T[j,1];}',
               'print("EXACT_IDENTITY_VALUE"); value;',
               'if(value==1){print("CERTIFIED_UNIT_IDENTITY");',
               'for(int k=1;k<=nrows(T);k++){if(T[k,1]!=0){print("WITNESS_INDEX_"+string(k));print(string(T[k,1]));}}',
               '}else{print("NO_UNIT_IDENTITY_CERTIFIED");}',
               'quit;']
        (out/'necessary_locus_QQ_lift.sing').write_text('\n'.join(lines)+'\n')
        dump('reduced_locus_QQ.json',{
            'field':'Q','variable_names':[names[v] for v in sorted(qremaining)],
            'variable_indices':sorted(qremaining),'equations':list(map(encode,qcurrent)),
            'reverse_peel_reconstruction':list(reversed(qpeels)),
            'G2_certificate':'G2_elimination_QQ.json',
            'unit_polynomial_present':any(set(q)=={()} for q in qcurrent),
            'scope':'Any exact unit identity here excludes the entire original123-parameter quadratic raw-generator ansatz over every characteristic-zero field. All eliminations divide only by nonzero rational constants.'})
    summary={'status':'EXACT_Q_UNIT_FOUND' if any(set(q)=={()} for q in qcurrent) else 'EXACT_Q_PREPARATION_ONLY',
             'independent_F101_replay':'PASS','phase':phase,'stop_reason':stop,'G2_rank':len(qe),
             'peels':len(qpeels),'remaining_variables':len(qremaining),
             'equations':len(qcurrent),'terms':sum(map(len,qcurrent)),
             'max_terms':max(map(len,qcurrent),default=0),
             'seconds':time.monotonic()-started,'CAS_launched':False,
             'witness_caution':'Ideal-times-matrix multiplication is not the coordinate sum inSingular. The generated script uses nrows(T) and an explicit scalar sum; independent witness verification remains required.'}
    dump('summary.json',summary);print('FINAL',json.dumps(summary),flush=True)


if __name__=='__main__':main()
