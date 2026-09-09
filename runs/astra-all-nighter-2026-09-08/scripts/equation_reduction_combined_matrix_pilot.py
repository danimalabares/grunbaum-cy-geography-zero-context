#!/usr/bin/env python3
"""Bounded bilinear q3 locus for all second-jet and matrix freedoms.

Field F101 only. z2=z20+sum(s_i*v_i), G1,G2 in End_S3(W), dim51 each.
The full123-variable necessary equations are
R(z2)+D(z2*G1)+D(t*G2)=0.
G2 has constant coefficients: tracked row operations remove its image,
leaving a quadratic locus in21 s+51 G1 variables and triangular G2 maps.
Only constant-unit polynomial substitutions are subsequently permitted.
No Groebner basis, CAS process, or higher jet computation is launched.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import time

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
OLD=RUN.parent/'astra-computation-2026-09-08'
P=101


class Cap(Exception):pass


def mod(a):
    a=Q(a)
    return a.numerator*pow(a.denominator,-1,P)%P


def plus(a,b,c=1):
    out=dict(a)
    for k,v in b.items():
        out[k]=(out.get(k,0)+c*v)%P
        if not out[k]:del out[k]
    return out


def enc(poly):return [[list(m),a] for m,a in sorted(poly.items())]
def dec(poly):return {tuple(m):a for m,a in poly}
def enc_linear(row):return [[j,a] for j,a in sorted(row.items())]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base',type=Path,default=RUN/'data/optimized_quadratic_generators/quadratic_generator_certificate.json')
    ap.add_argument('--matrix',type=Path,default=RUN/'data/linear_matrix_denominator/linear_matrix_denominator_certificate.json')
    ap.add_argument('--resume',type=Path)
    ap.add_argument('--max-seconds',type=float,default=180)
    ap.add_argument('--max-total-terms',type=int,default=100000)
    ap.add_argument('--max-polynomial-terms',type=int,default=2000)
    ap.add_argument('--max-degree',type=int,default=4)
    ap.add_argument('--max-peels',type=int,default=20)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    source_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    def gate():
        if time.monotonic()-started>args.max_seconds:raise Cap('internal_time_limit')
    def checkpoly(poly):
        if len(poly)>args.max_polynomial_terms:raise Cap('individual_polynomial_term_cap')
        if any(len(m)>args.max_degree for m in poly):raise Cap('polynomial_degree_cap')
    def dump(name,data):
        path=out/name
        assert not path.exists()
        path.write_text(json.dumps(data,separators=(',',':'))+'\n')
        return path
    def normalize(poly):
        if not poly:return poly
        key=min(poly,key=lambda m:(len(m),m))
        inv=pow(poly[key],-1,P)
        return {m:a*inv%P for m,a in poly.items()}
    def dedup(polys):
        seen=set();result=[]
        for poly in polys:
            if not poly:continue
            poly=normalize(poly);key=tuple(sorted(poly.items()))
            if key not in seen:seen.add(key);result.append(poly)
        return result
    if args.resume:
        checkpoint=json.loads(args.resume.read_text())
        assert checkpoint['script_sha256']==source_hash
        system_path=Path(checkpoint['system_path'])
        assert hashlib.sha256(system_path.read_bytes()).hexdigest()==checkpoint['system_sha256']
        system=json.loads(system_path.read_text())
    else:
        base=json.loads(args.base.read_text());matrix=json.loads(args.matrix.read_text())
        chartpath=OLD/'data/fixed_chart.json';blockpath=OLD/'data/equivariant_blocks_QQ.json'
        chart=json.loads(chartpath.read_text());blocks=json.loads(blockpath.read_text())
        for f in [chartpath,blockpath]:
            expected=hashlib.sha256(f.read_bytes()).hexdigest()
            assert base['input_sha256'][str(f.relative_to(REPO))]==expected
            assert matrix['input_sha256'][str(f.relative_to(REPO))]==expected
        assert matrix['input_sha256'][str(args.base.resolve().relative_to(REPO))]==hashlib.sha256(args.base.read_bytes()).hexdigest()
        basis=[[mod(a) for a in v] for v in base['second_coefficient_kernel_basis']]
        base_eq=[[mod(a) for a in row] for row in base['affine_equations_coefficients_then_constant']]
        matrix_eq=[[mod(a) for a in row] for row in matrix['equations']]
        assert len(basis)==21 and len(base_eq)==len(matrix_eq)==1160
        assert all(len(row)==23 for row in base_eq)
        assert all(len(row)==103 for row in matrix_eq)
        assert all(a[-1]==b[-1] for a,b in zip(base_eq,matrix_eq))
        generator_orbits=matrix['endomorphism_basis_pair_orbits_zero_based_source_target']
        F=[tuple(s.count(c) for c in chart['variables']) for s in chart['F0']]
        perms=[[chart['variables'].index(c) for c in g] for g in chart['group_images']]
        def act(m,p):
            n=[0]*8
            for i,a in enumerate(m):n[p[i]]=a
            return tuple(n)
        actions=[[F.index(act(m,p)) for m in F] for p in perms]
        pairs=set(product(range(16),repeat=2));recomputed=[]
        while pairs:
            i,j=min(pairs);orbit=sorted({(p[i],p[j]) for p in actions})
            recomputed.append([list(pair) for pair in orbit]);pairs.difference_update(orbit)
        assert recomputed==generator_orbits and len(generator_orbits)==51
        coeff_index={(i,tuple(m)):j for j,O in enumerate(chart['coefficient_orbits']) for i,m in O}
        D=[];labels=[]
        for kind,block in blocks['blocks'].items():
            for i,row in enumerate(block['D']):
                for j,cell in enumerate(row):
                    D.append({int(k):mod(a) for k,a in cell if mod(a)});labels.append([kind,i,j])
        assert labels==base['equation_locations']==matrix['equation_locations']
        # Original72-variable residual polynomials; G2 coefficients separate.
        polynomials=[]
        for a,b in zip(base_eq,matrix_eq):
            poly={():a[-1]} if a[-1] else {}
            poly.update({(j,):a[j] for j in range(21) if a[j]})
            poly.update({(21+j,):b[j] for j in range(51) if b[j]})
            polynomials.append(poly)
        for g,orbit in enumerate(generator_orbits):
            gate();by_target={j:[i for i,jj in orbit if jj==j] for j in range(16)}
            transformed=[]
            for O in chart['coefficient_orbits']:
                j,m=O[0];indices=[coeff_index[i,tuple(m)] for i in by_target[j]]
                transformed.append([sum(v[k] for k in indices)%P for v in basis])
            for row,poly in zip(D,polynomials):
                values=[0]*21
                for j,a in row.items():
                    values=[(x+a*y)%P for x,y in zip(values,transformed[j])]
                for s,a in enumerate(values):
                    if a:poly[s,21+g]=a
            print('BILINEAR_G1_COLUMN',g+1,'TOTAL_TERMS',sum(map(len,polynomials)),flush=True)
        system={'field':'F101','prime':P,'ansatz_variables':123,
                'residual_variable_names':['s'+str(i+1) for i in range(21)]+['g'+str(i+1) for i in range(51)],
                'second_generator_matrix_names':['h'+str(i+1) for i in range(51)],
                'equation_formula':'R(z20+sum(s_i*v_i))+D((z20+sum(s_i*v_i))*G1)+D(t*G2)=0',
                'rational_form':'z=(q*t+q^2*(z2+t*G1))*(Id+q*G1+q^2*G2)^(-1)',
                'scope':'necessary orderthree only; original first tangent fixed; all21 normalized second-order freedoms and both51 generator matrices allowed',
                'generator_matrix_pair_orbits':generator_orbits,
                'polynomials':list(map(enc,polynomials)),
                'G2_rows':[[[j,a] for j,a in enumerate(row[51:102]) if a] for row in matrix_eq],
                'locations':labels,
                'input_sha256':{str(f.relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest()
                                for f in [args.base.resolve(),args.matrix.resolve(),chartpath,blockpath,Path(__file__)]}}
        system_path=dump('original_bilinear_system.json',system)
        checkpoint=None
    polys=list(map(dec,system['polynomials']))
    g2rows=[dict(row) for row in system['G2_rows']]
    system_sha=hashlib.sha256(system_path.read_bytes()).hexdigest()
    # Constant Gaussian elimination of G2, preserving source combinations.
    echelon={};constraints=[];nextrow=0
    if checkpoint:
        echelon={int(p):(dict(h),dec(poly),dict(combo)) for p,h,poly,combo in checkpoint['G2_echelon']}
        constraints=[(i,dec(poly),dict(combo)) for i,poly,combo in checkpoint['constraints']]
        nextrow=checkpoint['next_original_row']
    def checkpoint_data(reason,next_index):
        return {'stage':'G2_elimination','reason':reason,'script_sha256':source_hash,
                'system_path':str(system_path),'system_sha256':system_sha,
                'next_original_row':next_index,
                'G2_echelon':[[p,enc_linear(h),enc(poly),enc_linear(combo)] for p,(h,poly,combo) in sorted(echelon.items())],
                'constraints':[[i,enc(poly),enc_linear(combo)] for i,poly,combo in constraints]}
    capped=None
    try:
        for i in range(nextrow,len(polys)):
            gate();h=dict(g2rows[i]);poly=dict(polys[i]);combo={i:1}
            for pivot in sorted(echelon):
                if pivot not in h:continue
                a=h[pivot];old,q,tr=echelon[pivot]
                h=plus(h,old,-a);poly=plus(poly,q,-a);combo=plus(combo,tr,-a)
                checkpoly(poly)
            if h:
                pivot=min(h);inv=pow(h[pivot],-1,P)
                entry=({j:a*inv%P for j,a in h.items()},
                       {m:a*inv%P for m,a in poly.items()},
                       {j:a*inv%P for j,a in combo.items()})
                projected=sum(len(q) for _,q,_ in constraints)+sum(len(q) for _,q,_ in echelon.values())+len(poly)
                if projected>args.max_total_terms:raise Cap('total_term_cap_during_G2_elimination')
                echelon[pivot]=entry
            elif poly:
                projected=sum(len(q) for _,q,_ in constraints)+sum(len(q) for _,q,_ in echelon.values())+len(poly)
                if projected>args.max_total_terms:raise Cap('total_term_cap_during_G2_elimination')
                constraints.append((i,poly,combo))
            nextrow=i+1
    except Cap as e:
        capped=str(e)
        dump('resume_checkpoint.json',checkpoint_data(capped,nextrow))
    if capped:
        dump('summary.json',{'status':'CAPPED_G2_elimination','reason':capped,'next_original_row':nextrow,
                             'G2_rank_so_far':len(echelon),'constraints_so_far':len(constraints),
                             'resume':'Pass --resume pointing to resume_checkpoint.json with a fresh --output.',
                             'seconds':time.monotonic()-started})
        print('CAPPED',capped,'NEXT_ROW',nextrow,flush=True);return
    # Independently verify each saved constant row-operation identity.
    for pivot,(h,poly,combo) in echelon.items():
        hh={};qq={}
        for i,a in combo.items():hh=plus(hh,g2rows[i],a);qq=plus(qq,polys[i],a)
        assert hh==h and qq==poly
    for _,poly,combo in constraints:
        hh={};qq={}
        for i,a in combo.items():hh=plus(hh,g2rows[i],a);qq=plus(qq,polys[i],a)
        assert not hh and qq==poly
    elimination=checkpoint_data('completed',len(polys))
    elimination.update(status='COMPUTER-CERTIFIED constant G2 elimination modulo101',
                       G2_rank=len(echelon),G2_free_indices=[j for j in range(51) if j not in echelon],
                       reconstruction='For pivot p, h_p= - polynomial - sum_{j>p} row_h[j]*h_j. Evaluate pivots in decreasing order; nonpivot h are unconstrained free parameters at this order.')
    dump('G2_elimination_certificate.json',elimination)
    # Reversible constant-unit polynomial peeling, with transactional caps.
    current=dedup([q for _,q,_ in constraints]);remaining=set(range(72));peels=[]
    trace=[];stop='no_eligible_constant_unit_equation'
    def multiply(a,b):
        outp={}
        for m,x in a.items():
            for n,y in b.items():
                key=tuple(sorted(m+n))
                if len(key)>args.max_degree:raise Cap('polynomial_degree_cap')
                outp[key]=(outp.get(key,0)+x*y)%P
                if not outp[key]:del outp[key]
            checkpoly(outp)
        return outp
    def substitute(poly,v,rhs):
        result={};powers=[{():1}]
        for monomial,a in poly.items():
            power=monomial.count(v)
            while len(powers)<=power:powers.append(multiply(powers[-1],rhs))
            rest=tuple(j for j in monomial if j!=v)
            term=multiply({rest:a},powers[power])
            result=plus(result,term);checkpoly(result)
        return result
    for stage in range(args.max_peels):
        try:gate()
        except Cap as e:stop=str(e);break
        if any(set(q)=={()} for q in current):stop='unit_equation_found';break
        occurrences={v:sum(sum(v in m for m in q) for q in current) for v in remaining}
        candidates=[]
        for i,q in enumerate(current):
            nonlinear={v for m in q if len(m)>1 for v in m}
            for m,a in q.items():
                if len(m)==1 and m[0] not in nonlinear:
                    v=m[0];candidates.append((occurrences[v]*max(1,len(q)-1),len(q),i,v,a))
        candidates.sort();accepted=False
        for _,_,i,v,a in candidates:
            if time.monotonic()-started>args.max_seconds:
                stop='internal_time_limit';break
            rhs={m:-b*pow(a,-1,P)%P for m,b in current[i].items() if m!=(v,)}
            try:
                proposed=[];count=0
                for j,q in enumerate(current):
                    if j==i:continue
                    new=substitute(q,v,rhs) if any(v in m for m in q) else q
                    count+=len(new)
                    if count>args.max_total_terms:raise Cap('total_term_cap_during_peeling')
                    proposed.append(new)
                proposed=dedup(proposed)
            except Cap:
                continue
            peels.append({'variable':v,'source_equation_at_stage':enc(current[i]),'rhs':enc(rhs)})
            current=proposed;remaining.remove(v);accepted=True
            record={'peel':len(peels),'eliminated_variable':v,'remaining_variables':len(remaining),
                    'equations':len(current),'total_terms':sum(map(len,current)),
                    'max_degree':max((len(m) for q in current for m in q),default=0)}
            trace.append(record);print('PEEL',json.dumps(record),flush=True)
            break
        if not accepted:
            if stop!='internal_time_limit':
                stop='all_constant_unit_substitutions_exceed_caps' if candidates else 'no_eligible_constant_unit_equation'
            break
    else:stop='max_peels_reached'
    names=system['residual_variable_names']
    def expression(poly):
        return '+'.join(str(a)+(''.join('*'+names[v] for v in m)) for m,a in sorted(poly.items())) or '0'
    ringvars=','.join(names[v] for v in sorted(remaining)) or 'dummy'
    sing=['// Necessary q3 locus overF101 only. No flat family or smooth fibre certified.',
          'ring r=101,('+ringvars+'),dp;',
          'ideal J='+(',\n'.join(expression(q) for q in current) or '0')+';',
          'print("INPUT_EQUATIONS"); size(J);',
          'ideal G=std(J);','print("GROEBNER_DIMENSION"); dim(G);',
          'print("GROEBNER_BASIS_SIZE"); size(G);','G;','quit;']
    (out/'necessary_locus.sing').write_text('\n'.join(sing)+'\n')
    final={'status':'COMPUTER-CERTIFIED polynomial reductions modulo101; only necessary orderthree locus',
           'system_path':str(system_path),'system_sha256':system_sha,
           'G2_elimination_certificate':'G2_elimination_certificate.json',
           'remaining_variable_indices':sorted(remaining),'remaining_variable_names':[names[v] for v in sorted(remaining)],
           'peeling_reconstruction_reverse_order':list(reversed(peels)),
           'equations':list(map(enc,current)),'trace':trace,'stop_reason':stop,
           'resume_note':'A later continuation can read the saved final equations and reverse-order reconstruction; this script --resume currently resumes the constant G2 stage only.',
           'field_scope':'F101; an empty affine modular locus alone does not rule out rational solutions with101-denominators.',
           'success_scope':'Surviving points pass onlyq3. All higher incidence identities, component selection and smoothness remain separate obligations.'}
    dump('reduced_locus.json',final)
    summary={'status':final['status'],'G2_rank':len(echelon),'G2_free_coordinates':51-len(echelon),
             'variables_before_peeling':72,'variables_after_peeling':len(remaining),
             'number_peels':len(peels),'number_equations':len(current),
             'total_terms':sum(map(len,current)),
             'max_polynomial_terms':max(map(len,current),default=0),
             'max_degree':max((len(m) for q in current for m in q),default=0),
             'unit_equation':any(set(q)=={()} for q in current),'stop_reason':stop,
             'seconds':time.monotonic()-started,'resource_limits':vars(args)|{'base':str(args.base),'matrix':str(args.matrix),'resume':str(args.resume) if args.resume else None,'output':str(args.output)}}
    dump('summary.json',summary);print('FINAL',json.dumps(summary),flush=True)


if __name__=='__main__':main()
