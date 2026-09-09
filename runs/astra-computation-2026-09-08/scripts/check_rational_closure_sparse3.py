#!/usr/bin/env python3
"""Bounded common F/R and generator-only Padé for ONE sparse3 checkpoint.

Shared exact FR verification is unchanged and hash-identified. A generator-
only fit is merely a candidate pending exact Schur verification. This
alternate tangent never inherits the original six-jet smoothness proof.
"""
import argparse,hashlib,json,os,sys
from pathlib import Path
sys.dont_write_bytecode=True
from fixed_curve_lift_sparse3 import RUN, DIRECTION, validate_sparse_checkpoint
from check_rational_closure import solve_overdetermined,build_identity_operator,verify_identity,save_immutable


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('checkpoint',type=Path)
    ap.add_argument('--max-denominator',type=int,default=10)
    args=ap.parse_args(); assert 0<=args.max_denominator<=10
    chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    state=json.loads(args.checkpoint.read_text()); p,N,zs,us=validate_sparse_checkpoint(state,chart)
    assert N>=6
    out=Path(os.environ['GS_RUN_OUTPUT']).resolve(); assert out.is_relative_to(RUN)
    out.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(args.checkpoint.read_bytes()).hexdigest()
    own=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    seq=[z+[a for row in u for a in row] for z,u in zip(zs,us)]
    operator=build_identity_operator(chart)
    attempts=[]; models=[]
    for kind,sequences in [('shared_F_R',seq),('generator_only',zs)]:
        found=False
        for excess in [1,6]:
            if found: break
            for d in range(min(args.max_denominator,(N-excess-1)//2)+1):
                m=d+excess
                rows=([sequences[n-k][j] for k in range(1,d+1)]+[-sequences[n][j]]
                      for n in range(m+1,N+1) for j in range(len(sequences[0])))
                coeff=solve_overdetermined(rows,d,p)
                print(kind,'D',d,'NUMERATOR',m,'FIT',coeff is not None,flush=True)
                attempt={'direction':DIRECTION,'kind':kind,'denominator_bound':d,'numerator_bound':m,
                         'prime':p,'fit_exists':coeff is not None,'checkpoint_sha256':digest,
                         'checker_sha256':own,'input_hashes':state['input_hashes'],
                         'matches_selected_normalized_firstjet':False,
                         'matches_selected_normalized_sixjet':False,'smoothness_certified':False}
                if coeff is None:
                    attempt['status']='FAILED: inconsistent bounded rational fit; not nonexistence'
                else:
                    den=[1]+coeff
                    num=[[sum(den[k]*sequences[n-k][j] for k in range(min(d,n)+1))%p
                          for j in range(len(sequences[0]))] for n in range(m+1)]
                    assert all(sum(den[k]*sequences[n-k][j] for k in range(min(d,n)+1))%p==
                               (num[n][j] if n<=m else 0)
                               for n in range(N+1) for j in range(len(sequences[0])))
                    attempt.update(denominator=den,numerator=num)
                    if kind=='generator_only':
                        attempt['status']='HEURISTIC rational generator candidate; exact Schur NOT checked'
                        found=True
                    else:
                        witness=verify_identity(den,num,us[0],p,operator)
                        attempt['exact_FR_first_nonzero_coefficient']=witness
                        if witness is not None:
                            attempt['status']='FAILED: fit has nonzero exact FR; higher bounds remain open'
                        else:
                            attempt['status']='COMPUTER-CERTIFIED exact rational flat family over finite field; smoothness and QQ realization OPEN'
                            znum=[row[:291] for row in num]
                            unum=[[row[291+30*i:291+30*(i+1)] for i in range(98)] for row in num]
                            model={'prime':p,'direction':DIRECTION,'denominator':den,'z_numerator':znum,'U_numerator':unum,
                                   'input_hashes':state['input_hashes'],'checkpoint_sha256':digest,'checker_sha256':own,
                                   'FR_identity_all_coefficients_zero':True,'complete_canonical_special_syzygies_verified':True,
                                   'matches_selected_normalized_firstjet':False,'matches_selected_normalized_sixjet':False,
                                   'smoothness_certified':False,'characteristic_zero_realization_certified':False,
                                   'status':attempt['status']}
                            model_path=out/f'sparse3_exact_family_p{p}.json'; save_immutable(model_path,model)
                            models.append(str(model_path)); found=True
                attempts.append(attempt)
                save_immutable(out/f'sparse3_{kind}_{digest[:12]}_e{excess}_d{d}.json',attempt)
                if found: break
    result={'direction':DIRECTION,'prime':p,'order':N,'checkpoint':str(args.checkpoint.resolve()),
            'checkpoint_sha256':digest,'checker_sha256':own,'attempts':attempts,'exact_family_models':models,
            'smoothness_certified':False,'characteristic_zero_realization_certified':False}
    dest=out/'sparse3_closure_summary.json'; save_immutable(dest,result)
    print('EXACT_FAMILY_MODELS',models)
    print('SUMMARY',dest)


if __name__=='__main__': main()
