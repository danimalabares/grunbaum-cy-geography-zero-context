#!/usr/bin/env python3
"""Record only in-scope repositories and selected immutable input hashes."""
import hashlib,json,subprocess
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]
PARENT=RUN.parents[2]
EXPECTED={
 'grunbaum-zero-context-proof':'ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b',
 'grunbaum-zero-context-proof-fable-max-audit':'9310cd9e3316c69f129d5588d65f0b91f37365b7',
 'grunbaum-cy-geography-zero-context':'4f75a9ae930a5cb645e06b4b8da79fa7b78a394a',
 'sr-project':'ff2afbbb7a8b18e7c054d16292df8db02ca87f5c',
 'heap-project':'73c8d1df1d9800425fc2ce18870c25853ea4e9f5',
 'grunbaum-cy-geography-fable-dgla':'3f7ef3da88fe963e10001fc66cbff4153d5fcb27'}
FILES={
 'grunbaum-zero-context-proof':['FINAL.md','PROOF.md','reconstruct/P1_ALL_ORDERS_AUDIT.md',
  'reconstruct/KURANISHI_AUDIT.md','reconstruct/TOTAL_SPACE_REGULARITY_AUDIT.md',
  'reconstruct/p1_universal_exact_test.m2','reconstruct/p1_quartic_component.m2',
  'reconstruct/p1_universal_order4_vF.txt','reconstruct/p1_universal_order4_vR.txt',
  'reconstruct/p1_universal_order4_vG.txt','reconstruct/p1_universal_order4_vC.txt',
  'deformation/generic_equivariant_state_F_order6.txt',
  'deformation/generic_equivariant_state_R_order6.txt','deformation/EQUIVARIANT_FORMAL_LIFT.md',
  'deformation/INTEGRAL_EQUIVARIANT_LIFT.md','enumerate/FORMAL_ALGEBRAIZATION.md'],
 'grunbaum-zero-context-proof-fable-max-audit':['VERDICT.md','EXECUTIVE_SUMMARY.md','CLAIM_LEDGER.md','MISSING_EVIDENCE.md'],
 'grunbaum-cy-geography-zero-context':['reports/DEFORMATION_EQUATIONS.md','reports/GEOGRAPHY.md','reports/ABEL_MATHEMATICAL_FACTS.md','equations/deformation_data.json'],
 'sr-project':['proofs/grunbaum-smoothing/fable-dgla-only/PROOF_DGLA.pdf'],
 'heap-project':['stanley-reisner.tex','deformations.tex','algebraic-geometry.tex']}

def main():
    data={}
    for repo,expected in EXPECTED.items():
        path=PARENT/repo
        def git(*a): return subprocess.check_output(['git',*a],cwd=path,text=True).strip()
        head=git('rev-parse','HEAD'); assert head==expected,(repo,head,expected)
        data[repo]={'head':head,'branch':git('branch','--show-current'),
          'tree':git('rev-parse','HEAD^{tree}'),
          'tracked_changes':git('diff','--name-only','HEAD'),
          'sha256':{f:hashlib.sha256((path/f).read_bytes()).hexdigest() for f in FILES.get(repo,[])}}
        assert not data[repo]['tracked_changes'], 'preserve and investigate changed source input'
    dest=RUN/'SOURCE_MANIFEST.json'
    if dest.exists(): assert json.loads(dest.read_text())==data
    else: dest.write_text(json.dumps(data,indent=2)+'\n')
    print('ALL_SIX_REPOSITORY_HEADS_AND_SELECTED_SOURCE_HASHES_VERIFIED')
    print(dest)

if __name__=='__main__': main()
