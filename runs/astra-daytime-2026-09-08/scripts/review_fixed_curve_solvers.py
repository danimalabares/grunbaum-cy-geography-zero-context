#!/usr/bin/env python3
"""Small exact regression review of the lifting and Padé solver code.

This never runs a CAS or a nonconstant geometry computation. It checks pivot
signs against known modular linear solutions, and scalar constant/polynomial/
rational sequences against the bounded common-denominator fitter. It also
creates an immutable checkpoint for the constant Stanley--Reisner family and
runs the full rational-closure checker on that fixture. A successful constant
test proves no smoothness; it only checks the exact-identity control path.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO
from fixed_curve_lift import lu_factor, lu_solve
from check_rational_closure import solve_overdetermined, validate_checkpoint, verify_identity
from build_fixed_chart import F0, times

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]
P=101

def save_immutable(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): assert json.loads(path.read_text())==data
    else: path.write_text(json.dumps(data)+"\n")

def denominator_fit(sequence,d):
    m=d+6
    rows=([sequence[n-k] for k in range(1,d+1)]+[-sequence[n]]
          for n in range(m+1,len(sequence)))
    return solve_overdetermined(rows,d,P)

def main():
    matrices=[[[0,1],[1,1]],[[0,1,2],[0,0,1],[1,3,4]],
              [[2,4,1],[1,0,3],[0,2,1]]]
    for a in matrices:
        x=list(range(1,len(a)+1))
        b=[sum(c*v for c,v in zip(row,x))%P for row in a]
        assert lu_solve(lu_factor(a,P),b,P)==x
    assert solve_overdetermined([[0,1,2],[1,1,3]],2,P)==[1,2]
    assert solve_overdetermined([[1,1],[1,2]],1,P) is None
    rational=[pow(3,n,P) for n in range(13)]
    assert denominator_fit(rational,1)==[P-3]
    fibonacci=[1,1]
    for _ in range(11): fibonacci.append(sum(fibonacci[-2:])%P)
    assert denominator_fit(fibonacci,2)==[P-1,P-1]
    constant=[7]+[0]*12
    polynomial=[1,2,3,4,5,6,7]+[0]*6
    rank_deficient=solve_overdetermined([[1,1,3],[2,2,6]],2,P)
    results={
      "modular_lu_row_swaps_and_signs":"PASS",
      "overdetermined_unique_and_inconsistent_cases":"PASS",
      "geometric_denominator_one_minus_3q":"PASS",
      "fibonacci_denominator_one_minus_q_minus_q_squared":"PASS",
      "consistent_rank_deficient_result":rank_deficient,
      "constant_sequence_degree1_fit":denominator_fit(constant,1),
      "polynomial_degree6_sequence_degree1_fit":denominator_fit(polynomial,1),
      "zero_denominator_degree_test":denominator_fit(constant,0),
    }
    # A scalar rational relation embedded in the same array shapes checks
    # the nonlinear denominator-clearing sign independently of geometry:
    # z=q, W=q/(1+q), so z-W-zW=0. With common D=1+q, Z=q+q^2.
    toy_lin=[{} for _ in range(9900)]; toy_lin[0]={0:1}
    toy_operator=(toy_lin,[(0,0,0)])
    toy_num=[[0]*3231 for _ in range(3)]
    toy_num[1][0]=1; toy_num[2][0]=1; toy_num[1][291]=1
    capture=StringIO()
    with redirect_stdout(capture):
        assert verify_identity([1,1],toy_num,[[0]*30 for _ in range(98)],P,toy_operator) is None
        toy_bad=verify_identity([1,P-1],toy_num,[[0]*30 for _ in range(98)],P,toy_operator)
    assert toy_bad=={'q_degree':3,'quartic_row':0,'relation_column':0,'residue':P-2,
                     'all_lower_coefficients_zero':True}
    results['nonlinear_rational_identity_z_minus_W_minus_zW']='PASS'
    results['wrong_denominator_sign_detected']=toy_bad
    results['toy_identity_stdout']=capture.getvalue()
    chartfile=RUN/'data/fixed_chart.json'; chart=json.loads(chartfile.read_text())
    mons=[tuple(v) for v in chart['pivot_monomials']]
    cols=[tuple(v) for v in chart['multiplication_columns']]
    U0=[[0]*30 for _ in range(98)]
    for k,c in enumerate(chart['extra_columns']):
        i,j=cols[c]; U0[mons.index(times(F0[i],j))][k]=1
    N=10
    fixture={"prime":P,"order":N,"free_coordinates":chart['free_coordinates'],
             "input_hashes":{str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in [chartfile,REPO/'equations/deformation_data.json',RUN/'scripts/fixed_curve_lift.py']},
             "z_coefficients":[[0]*291 for _ in range(N+1)],
             "U_coefficients":[U0]+[[[0]*30 for _ in range(98)] for _ in range(N)],
             "all_schur_equations_verified_through":N,
             "status":"SYNTHETIC CONSTANT FAMILY; not a smoothing or the selected six-jet"}
    fixturepath=RUN/'fixtures/review_constant_family/checkpoint.json'
    # Include content hash in filename if the scripts' provenance changes.
    digest=hashlib.sha256(json.dumps(fixture,sort_keys=True).encode()).hexdigest()[:12]
    fixturepath=fixturepath.with_name('checkpoint-'+digest+'.json')
    save_immutable(fixturepath,fixture)
    checker_hash=hashlib.sha256((RUN/'scripts/check_rational_closure.py').read_bytes()).hexdigest()
    env=dict(os.environ,GS_RUN_OUTPUT=str(RUN/'fixtures/review_constant_family'/('output-'+checker_hash[:12])))
    completed=subprocess.run([sys.executable,str(RUN/'scripts/check_rational_closure.py'),
        str(fixturepath),'--max-denominator','2','--allow-other-sixjet'],env=env,capture_output=True,text=True,timeout=60)
    results['constant_family_checker_exit_code']=completed.returncode
    results['constant_family_checker_stdout']=completed.stdout
    results['constant_family_checker_stderr']=completed.stderr
    assert completed.returncode==0 and 'EXACT_RATIONAL_FAMILY' in completed.stdout
    negative=deepcopy(fixture)
    negative['z_coefficients'][1][chart['dependent_coordinates'][0]]=1
    negative['status']='SYNTHETIC NEGATIVE CONTROL: deliberately violates a first-order syzygy'
    negativepath=fixturepath.with_name('negative-'+digest+'.json'); save_immutable(negativepath,negative)
    env['GS_RUN_OUTPUT']=str(RUN/'fixtures/review_constant_family'/('negative-output-'+checker_hash[:12]))
    bad=subprocess.run([sys.executable,str(RUN/'scripts/check_rational_closure.py'),str(negativepath),
        '--max-denominator','2','--allow-other-sixjet'],env=env,capture_output=True,text=True,timeout=60)
    results['negative_control_exit_code']=bad.returncode
    results['negative_control_stdout']=bad.stdout
    results['negative_control_stderr']=bad.stderr
    assert bad.returncode==0 and bad.stdout.count('FAILED_EXACT_CLOSURE')==3
    assert 'EXACT_RATIONAL_FAMILY' not in bad.stdout
    for name,changed in [('wrong_origin',deepcopy(fixture)),('wrong_input_hash',deepcopy(fixture))]:
        if name=='wrong_origin': changed['z_coefficients'][0][0]=1
        else: changed['input_hashes'][next(iter(changed['input_hashes']))]='0'*64
        try: validate_checkpoint(changed,chart)
        except AssertionError as e: results[name+'_rejected']=str(e)
        else: raise AssertionError('failed to reject '+name)
    results['checker_sha256']=checker_hash
    digest=hashlib.sha256(json.dumps(results,sort_keys=True).encode()).hexdigest()[:12]
    resultfile=RUN/('certificates/fixed_curve_solver_review-'+digest+'.json')
    save_immutable(resultfile,results)
    print(json.dumps(results,indent=2))
    print('immutable_review_certificate='+str(resultfile))

if __name__=='__main__': main()
