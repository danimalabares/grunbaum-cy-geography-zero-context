#!/usr/bin/env python3
"""Cheap exporter syntax controls and one strictly scoped mechanical repair.

Only --repair-json updates the generated fixed_curve_QQ.json, replacing its
sixteen initial cubic words by explicit multiplication. All other bytes and
JSON data must remain unchanged. No CAS is run. The rational exporter's
public CLI still rejects synthetic models.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from build_fixed_chart import F0,FWORDS,name
from export_rational_model import render_m2

RUN=Path(__file__).resolve().parents[1]

def sha(s): return hashlib.sha256(s).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repair-json',action='store_true'); args=ap.parse_args()
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    control={'prime':101,'denominator':[1], 'z_numerator':[[0]*291],
             'FR_identity_all_coefficients_zero':True,'matches_selected_normalized_sixjet':False}
    text=render_m2(control,chart)
    assert 'F=matrix{{'+','.join(name(m) for m in F0)+'}};' in text
    assert not any(re.search(r'\b'+word+r'\b',text) for word in FWORDS)
    assert 'Qq=ZZ/101[q]; K=frac Qq;' in text
    selected=render_m2(control,chart,2); assert 'q=sub(2,K)' in selected
    bad=deepcopy(control); bad['denominator']=[1,100]
    try: render_m2(bad,chart,1)
    except AssertionError: pass
    else: raise AssertionError('denominator-zero specialization was accepted')
    fixture=RUN/'fixtures/review_export_rendering'; fixture.mkdir(parents=True,exist_ok=True)
    fixturefile=fixture/'synthetic_rejected_model.json'
    if fixturefile.exists(): assert json.loads(fixturefile.read_text())==control
    else: fixturefile.write_text(json.dumps(control)+'\n')
    result=subprocess.run([sys.executable,str(RUN/'scripts/export_rational_model.py'),str(fixturefile)],
        capture_output=True,text=True,timeout=10)
    assert result.returncode!=0 and 'synthetic controls are not smoothing inputs' in result.stderr
    report={'constant_generator_rendering':'PASS','generic_finite_field_ring_rendering':'PASS',
            'nonzero_parameter_rendering':'PASS','zero_denominator_rejected':'PASS',
            'public_cli_synthetic_gate':'PASS','synthetic_gate_stderr':result.stderr}
    if args.repair_json:
        path=RUN/'equations/fixed_curve_QQ.json'; before=path.read_bytes(); old=json.loads(before)
        assert len(old['generator_F'])==16
        patched=before.decode(); count=0
        for word,mono in zip(FWORDS,F0):
            patched,n=re.subn(r'(?m)^(\s*")'+word+r'\+',lambda m:m.group(1)+name(mono)+'+',patched)
            count+=n
        assert count in (0,16), 'partial/unexpected artifact state; preserve it'
        new=json.loads(patched)
        expected=deepcopy(old)
        if count:
            expected['generator_F']=[name(F0[i])+s[len(FWORDS[i]):]
                                     for i,s in enumerate(old['generator_F'])]
        assert new==expected
        assert all(s.startswith(name(F0[i])+'+') for i,s in enumerate(new['generator_F']))
        after=patched.encode()
        if count: path.write_bytes(after)
        report['mechanical_repair']={'replacements':count,'old_sha256':sha(before),'new_sha256':sha(after),
                                     'changed_only_sixteen_initial_monomial_tokens':True}
    digest=sha(json.dumps(report,sort_keys=True).encode())[:12]
    output=RUN/('certificates/export_rendering_review-'+digest+'.json')
    if output.exists(): assert json.loads(output.read_text())==report
    else: output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2)); print(output)

if __name__=='__main__': main()
