#!/usr/bin/env python3
"""Finite271-variable coefficient point and the actual16 cubic equations.

Use pi^7=101. The other270 variables are dependent normalized generator
coefficients. All21 free coordinates are the ORIGINAL rational sixjet
polynomials evaluated at pi. Eliminate syzygy auxiliaries by the bordered
determinants det[[A_r,B_r[:,j]],[C_r[i,:],D_r[i,j]]], of size at most33.
The shared exact linear-form factors prevent pointless determinant expansion.
The unique root has all270 dependent coordinates in pi*O_Q101(pi).
This is a finite algebraic-number representation, not a primitive element.
"""
import hashlib, json, os, time
from fractions import Fraction as Q
from pathlib import Path
from build_fixed_chart import F0, FWORDS, V, monomials, times
from fixed_curve_lift import normalized_jet

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]

def determinant_mod(a,p):
    a=[row[:] for row in a]; n=len(a); det=1
    for k in range(n):
        hit=next((i for i in range(k,n) if a[i][k]%p),None)
        if hit is None: return 0
        if hit!=k: a[k],a[hit]=a[hit],a[k]; det=-det
        pivot=a[k][k]%p; det=det*pivot%p; inv=pow(pivot,-1,p)
        for i in range(k+1,n):
            if a[i][k]:
                c=a[i][k]*inv%p
                for j in range(k+1,n): a[i][j]=(a[i][j]-c*a[k][j])%p
                a[i][k]=0
    return det%p

def monomial(m):
    return '*'.join(v+(f'^{n}' if n>1 else '') for v,n in zip(V,m) if n) or '1'

def univariate(coefficients):
    terms=[]
    for n,c in enumerate(coefficients):
        if not c: continue
        var=('pi' if n==1 else f'pi^{n}') if n else '1'
        terms.append(f'({c})*{var}')
    return ' + '.join(terms) or '0'

def main():
    started=time.monotonic(); p=101
    chartpath=RUN/'data/fixed_chart.json'
    blockpath=RUN/'data/equivariant_blocks_QQ.json'
    chart=json.loads(chartpath.read_text()); blocks=json.loads(blockpath.read_text())
    assert hashlib.sha256(chartpath.read_bytes()).hexdigest()==blocks['source_chart_sha256']
    assert chart['F0']==FWORDS
    jet,_=normalized_jet(chart)
    dep=blocks['dependent_coordinates']; free=blocks['free_coordinates']
    assert dep==chart['dependent_coordinates'] and free==chart['free_coordinates']
    assert len(dep)==270 and len(free)==21
    denoms=set()
    def modular(c):
        c=Q(c); denoms.add(c.denominator)
        assert c.denominator%101, ('nonintegral coefficient',c)
        return c.numerator*pow(c.denominator,-1,p)%p
    factors={}
    for kind,block in blocks['blocks'].items():
        ni,nk,nc=block['dimensions']
        factors[kind]={key:block[key] for key in ['dimensions','A_minus_identity','B','C','D']}
        for key in ['A_minus_identity','B','C','D']:
            for row in block[key]:
                for entry in row:
                    for j,c in entry:
                        assert 0<=j<291; modular(c)
        assert [ni,nk,nc] in [[21,5,47],[13,5,35],[32,10,75]]
    for row in jet:
        for c in row: modular(c)
    selected=[]; jac=[]
    for kind,i,j in blocks['selected_lower_equations']:
        block=factors[kind]; ni,nk,nc=block['dimensions']
        assert 0<=i<nc and 0<=j<nk
        selected.append({'block':kind,'bottom_row_zero_based':i,'right_column_zero_based':j,
                         'matrix_size':ni+1,
                         'polynomial':'det([[I+A_minus_identity,B[:,j]],[C[i,:],D[i,j]]])'})
        linear={k:modular(c) for k,c in block['D'][i][j]}
        jac.append([linear.get(k,0) for k in dep])
    assert len(selected)==270
    det=determinant_mod(jac,p); assert det
    # The original30 canonical monomial linear relations have disjoint
    # extra-column pivots. They form the complete degree4 kernel.
    columns=[tuple(c) for c in chart['multiplication_columns']]
    images=[times(F0[i],j) for i,j in columns]
    assert len(columns)==128 and len(set(images))==98
    extra=chart['extra_columns']; assert len(extra)==30
    syzygies=[]
    for col in extra:
        pivot=images.index(images[col]); assert col!=pivot
        assert pivot in chart['pivot_columns'] and pivot not in extra
        i,j=columns[col]; ii,jj=columns[pivot]
        assert times(F0[i],j)==times(F0[ii],jj)
        syzygies.append({'positive':[i,j],'negative':[ii,jj],
                         'positive_multiplication_column':col,'negative_multiplication_column':pivot})
    assert len({s['positive_multiplication_column'] for s in syzygies})==30
    lookup={(i,tuple(m)):j for j,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    tails=[tuple(m) for m in chart['tail_monomials']]
    assert len(tails)==104 and set(tails)|set(F0)==set(monomials(3))
    cubic_maps=[]
    for i in range(16):
        terms=[{'monomial_exponents':list(F0[i]),'coefficient_constant':'1'}]
        terms += [{'monomial_exponents':list(m),'lambda_index_one_based':lookup[i,m]+1} for m in tails]
        cubic_maps.append({'generator_index_one_based':i+1,'central_monomial':FWORDS[i],'terms':terms})
    lambdas=[]
    for j in range(291):
        if j in dep:
            lambdas.append({'lambda_index_one_based':j+1,'theta_index_one_based':dep.index(j)+1})
        else:
            lambdas.append({'lambda_index_one_based':j+1,
                            'pi_polynomial_coefficients':[str(jet[n][j]) for n in range(7)]})
    provenance={str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
                for path in [chartpath,blockpath,REPO/'equations/deformation_data.json',Path(__file__)]}
    result={'status':'COMPUTER-CERTIFIED finite coefficient presentation; smoothness by transported source certificates',
            'representation':'multivariate algebraic numbers with unique ramified p-adic isolating condition',
            'prime':101,'uniformizer_equation':{'coefficients_low_to_high':[-101,0,0,0,0,0,0,1]},
            'coefficient_unknowns':['pi']+[f'theta{j}' for j in range(1,271)],
            'field':'L=Q(pi,theta1,...,theta270) embedded in Q101(pi); degree need not equal7',
            'branch_selector':'pi^7=101; theta_i in pi*Z101[pi] for all1<=i<=270; unique root in this ball',
            'lambda_definitions':lambdas,'shared_block_factors':factors,
            'bordered_determinant_equations':selected,'projective_variables':list(V),
            'cubic_equations':cubic_maps,'central_linear_syzygies':syzygies,
            'dependent_coordinate_indices_zero_based':dep,'free_coordinate_indices_zero_based':free,
            'certificate':{'selected_jacobian_size':270,'selected_jacobian_determinant_mod101':det,
                           'block_central_values':'A=I; B=C=D=0',
                           'all_block_entries_are_linear_forms_without_constants':True,
                           'all_coefficient_denominators_are_101_units':True,
                           'denominators':sorted(denoms),'central_cubics_match_fixed_ideal':True,
                           'central_multiplication_rank':98,'central_degree4_kernel_rank':30,
                           'canonical_degree4_syzygies_verified':True,
                           'complete_first_syzygy_generation_uses':'frozen self-dual1,16,30,16,1 resolution trust boundary'},
            'input_hashes':provenance,'seconds':round(time.monotonic()-started,3)}
    dest=RUN/'data/ramified_fibre_coefficients.json'
    assert not dest.exists(), 'preserve existing coefficient presentation'
    dest.write_text(json.dumps(result,separators=(',',':'))+'\n')
    lines=['# The actual sixteen cubic equations: ramified algebraic-number presentation','',
           '**COMPUTER-CERTIFIED finite presentation.** The coefficient data are in',
           '`data/ramified_fibre_coefficients.json`. They specify 271 algebraic',
           'unknowns, not an uncomputed infinite series: pi and theta_1,...,theta_270.',
           'Smoothness uses the reviewed ramified transport of the original six-jet',
           'certificates; see `RAMIFIED_POINT_CONSTRUCTION.md` and the final review.','',
           '## Coefficient field and unique root','',
           'Take K=Q_101(pi), pi^7=101. Put O=Z_101[pi]. For each of the 270',
           'selected entries below impose the finite bordered determinant equation','',
           '    det([[A_r(lambda), B_r(lambda)[:,j]],',
           '         [C_r(lambda)[i,:], D_r(lambda)[i,j]]]) = 0.','',
           'Here A_r=I+A_minus_identity. The three shared matrices have A sizes',
           '21, 13, and 32, so each determinant has size at most 33. All rational',
           'linear-form factors and all 270 row/column selections are explicit',
           'in the JSON. This determinant representation is a finite polynomial',
           'equation; no determinant expansion or syzygy unknown is necessary.','',
           'Choose the unique solution with theta_i in pi O for all i.',
           f'The selected 270-by-270 Jacobian determinant is {det} modulo 101,',
           'so the root exists uniquely by Hensel lifting. All displayed rational',
           'denominators are units at 101. The coefficient field is',
           'L=Q(pi,theta_1,...,theta_270) inside K; its degree is **not** asserted',
           'to be 7. Smoothness descends from K to this number field.','',
           '## Exact indexing of the algebraic coefficients','',
           'In every polynomial below, lambda_j denotes the following exact',
           'algebraic number. For k=1,...,270 set lambda_(d_k)=theta_k, where',
           'the ordered list (d_1,...,d_270), with one-based indices, is:','',
           '```text',','.join(str(j+1) for j in dep),'```','',
           'The other 21 lambda values are these ORIGINAL six-jet polynomials,',
           'not the linear-path experiment:','', '```text']
    for j in free: lines.append(f'lambda_{j+1} = '+univariate([jet[n][j] for n in range(7)]))
    lines += ['```','', '## All sixteen cubic equations','',
              'The fibre is X=V(F_1,...,F_16) in P^7_L with coordinates a,...,h.',
              'Multiplication and exponents in the following code blocks have',
              'their ordinary polynomial meanings. Every summand is displayed.','']
    for i in range(16):
        groups={}
        for m in tails: groups.setdefault(lookup[i,m]+1,[]).append(monomial(m))
        terms=[f'lambda_{j}*('+ '+'.join(mons)+')' for j,mons in sorted(groups.items())]
        lines += [f'### F_{i+1}','', '```text',f'F_{i+1} = {monomial(F0[i])}']
        for j in range(0,len(terms),3): lines.append('  + '+' + '.join(terms[j:j+3]))
        lines += ['```','']
    lines += ['## Reproducibility and remaining representation work','',
              '**COMPUTER-CERTIFIED.** The exporter checks the original sixteen',
              'central cubics, the thirty canonical degree-four syzygies, central',
              'block values, all denominator units, and the selected Jacobian.',
              'The original resolution certifies that these linear relations',
              'generate the entire first-syzygy module; this retains the stated',
              'computer-algebra trust boundary of the source proof.','',
              '**OPEN convenience reduction.** A primitive element or a small',
              'multiplication table for L has not been extracted. Neither is',
              'needed to specify the finite algebraic numbers by the unique',
              'p-adic root above. The global coefficient zero locus can have',
              'other components; those are excluded by the isolating condition.','',
              'Reproduce under the sequential resource guard:', '',
              '    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag ramified-fibre-export -- python3 -B scripts/export_ramified_fibre.py','']
    report=RUN/'RAMIFIED_FIBRE_EQUATIONS.md'; assert not report.exists()
    report.write_text('\n'.join(lines))
    print('PASS_RAMIFIED_POINT_271_UNKNOWNS_270_BORDERED_DETERMINANTS',flush=True)
    print('JACOBIAN_DETERMINANT_MOD101',det,'DENOMINATORS',sorted(denoms),flush=True)
    print('CENTRAL16_CUBICS_30_LINEAR_SYZYGIES_VERIFIED',flush=True)
    print('JSON',dest,'bytes',dest.stat().st_size,flush=True)
    print('ALL16_CUBIC_EQUATIONS',report,'bytes',report.stat().st_size,flush=True)

if __name__=='__main__': main()
