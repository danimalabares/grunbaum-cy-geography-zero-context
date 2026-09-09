#!/usr/bin/env python3
"""Bounded GENERATOR-ONLY rational screen of existing exact checkpoints.

Canonical syzygies may have much larger denominators than generators.
Therefore a failed common F/R fit does not reject a small rational F.
This script changes the test, never extends the jet, and never treats a
Padé fit as an exact family. A candidate must next pass exact Schur
identities in the rational 21/13/32 multiplicity blocks.
"""
import argparse, hashlib, json, os
from pathlib import Path
from check_rational_closure import solve_overdetermined, validate_checkpoint
from check_rational_closure_linear import validate_checkpoint as validate_linear
from fixed_curve_lift import normalized_jet

RUN=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('checkpoints',nargs='+',type=Path)
    ap.add_argument('--max-denominator',type=int,default=10)
    a=ap.parse_args()
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    raw,_=normalized_jet(chart)
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/generator_pade'))
    assert out.resolve().is_relative_to(RUN)
    out.mkdir(exist_ok=True,parents=True)
    for path in a.checkpoints:
        state=json.loads(path.read_text()); linear=state.get('free_path_order')==1
        p,N,zs,_=(validate_linear if linear else validate_checkpoint)(state,chart)
        expected=[[x.numerator*pow(x.denominator,-1,p)%p for x in row] for row in raw]
        assert zs[1]==expected[1]
        if linear:
            assert all(zs[n][j]==0 for n in range(2,N+1) for j in chart['free_coordinates'])
        else: assert zs[:7]==expected
        attempts=[]
        # The second linear bound allows the same flexibility as the sixjet
        # screen, avoiding a false comparison due merely to numerator bounds.
        for excess in ([1,6] if linear else [6]):
            for d in range(a.max_denominator+1):
                m=d+excess
                assert m<N
                rows=([zs[n-k][j] for k in range(1,d+1)]+[-zs[n][j]]
                      for n in range(m+1,N+1) for j in range(291))
                coeff=solve_overdetermined(rows,d,p)
                print('CURVE','linear' if linear else 'sixjet','F_ONLY_DEN',d,
                      'NUM',m,'FIT',coeff is not None,flush=True)
                result={'denominator_bound':d,'numerator_bound':m,'fit_exists':coeff is not None}
                if coeff is not None:
                    den=[1]+coeff
                    num=[[sum(den[k]*zs[n-k][j] for k in range(min(d,n)+1))%p
                          for j in range(291)] for n in range(m+1)]
                    assert all(sum(den[k]*zs[n-k][j] for k in range(min(d,n)+1))%p==
                               (num[n][j] if n<=m else 0)
                               for n in range(N+1) for j in range(291))
                    result.update(denominator=den,z_numerator=num,
                                  status='HEURISTIC rational candidate; exact Schur identity NOT yet checked')
                else: result['status']='FAILED: inconsistent generator-only rational fit at these bounds'
                attempts.append(result)
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        result={'checkpoint':str(path.resolve()),'checkpoint_sha256':digest,
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'prime':p,'order':N,'free_path_order':1 if linear else 6,
                'input_hashes':state['input_hashes'],'attempts':attempts,
                'exact_family_claim':False}
        dest=out/f'generator_only_p{p}_{digest[:12]}.json'
        assert not dest.exists(); dest.write_text(json.dumps(result)+'\n')
        print('SCREEN_SAVED',dest,flush=True)

if __name__=='__main__': main()
