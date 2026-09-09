#!/usr/bin/env python3
"""OVERNIGHT ONLY: two bounded modular stages, strictly sequential.

The agent should read HEAVY_QUEUE.md first. This controller ends after a
verified modular rational model or the order32 ansatz limit. It does not
start a giant elimination or assert a characteristic-zero Hodge pair.
"""
import argparse,datetime,json,subprocess,sys
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]

def job(tag,seconds,command):
    cmd=[sys.executable,'scripts/run_guarded.py','--seconds',str(seconds),
         '--memory-mb','2800','--tag',tag,'--']+command
    result=subprocess.run(cmd,cwd=RUN,text=True,capture_output=True)
    print(result.stdout,flush=True)
    if result.returncode:
        print(result.stderr,file=sys.stderr); sys.exit(result.returncode)
    metadata,_=json.JSONDecoder().raw_decode(result.stdout)
    return Path(metadata['output'])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run',action='store_true')
    a=ap.parse_args()
    if not a.run: sys.exit('Prepared only. At about21:00, run with --run after reading the queue.')
    hour=datetime.datetime.now().hour
    if 8<=hour<21: sys.exit('Daytime guard: primary overnight controller will not run before21:00.')
    previous=None
    for order in [24,32]:
        cmd=[sys.executable,'scripts/fixed_curve_lift.py','--order',str(order),'--prime','101']
        if previous: cmd+=['--resume',str(previous)]
        stage=job(f'night-curve-{order}',1800,cmd)
        previous=stage/f'fixed_curve_p101_order{order}.json'
        closure=job(f'night-closure-{order}',1800,[sys.executable,
            'scripts/check_rational_closure.py',str(previous),'--max-denominator','10'])
        models=list(closure.glob('rational_family_p*.json'))
        if models:
            print('EXACT_MODULAR_MODEL_READY',models[0])
            print('Follow queue gates for exact export, smoothness, spread, normal space, and I-squared.')
            return
    print('STOP: bounded common rational ansatz exhausted at order32; retain the finite implicit algebraic curve.')
    print('Proceed to the symmetry-reduced algebraic option only after a concrete size assessment.')

if __name__=='__main__': main()
