#!/usr/bin/env python3
"""Run one job, with single-thread environment, lock, logs and hard time cap.

Authorized overnight session 2026-09-08 to 2026-09-09: <=7200 seconds per justified stage,
<=2800 MiB RSS; short pilots precede unknown-cost work.
No launches after06:00 Sao Paulo on September9; finish owned jobs by06:30.
Final handoff by06:45. Reserve the final45 minutes for verification. This never stops user processes.
Memory RSS polling needs permission to run ps; fail closed if unavailable.
The lock serializes jobs started through this runner, not unrelated tasks.
"""
import argparse, datetime, fcntl, json, os, signal, subprocess, sys, time
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL_ZONE=ZoneInfo('America/Sao_Paulo')
STOP_LAUNCH=datetime.datetime(2026,9,9,6,0,tzinfo=LOCAL_ZONE)
STOP_WORK=datetime.datetime(2026,9,9,6,30,tzinfo=LOCAL_ZONE)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seconds',type=int,required=True)
    ap.add_argument('--memory-mb',type=int,default=2800)
    ap.add_argument('--tag',required=True)
    ap.add_argument('command',nargs=argparse.REMAINDER)
    a=ap.parse_args(); cmd=a.command
    if cmd and cmd[0]=='--': cmd=cmd[1:]
    if not cmd: ap.error('command required after --')
    if not (0<a.seconds<=7200): ap.error('Session limit: 1..7200 seconds per attempt')
    if not (0<a.memory_mb<=2800): ap.error('Session RSS ceiling: 2800 MiB')
    now=datetime.datetime.now(LOCAL_ZONE)
    if now>=STOP_WORK: sys.exit('Session computation cutoff reached; no process started.')
    if now>=STOP_LAUNCH:
        sys.exit('No job launches after06:00 local; no process started.')
    effective_seconds=min(a.seconds,max(1,int((STOP_WORK-now).total_seconds())))
    run=Path(__file__).resolve().parents[1]
    logs=run/'logs'; logs.mkdir(exist_ok=True)
    lock=(run/'.cas.lock').open('a+')
    try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError: sys.exit('Another guarded job is running; no process started.')
    def processes():
        text=subprocess.check_output(['ps','-axo','pid=,pgid=,rss=,comm='],text=True)
        return [line.split(None,3) for line in text.splitlines() if line.strip()]
    try: before=processes()
    except Exception as e: sys.exit(f'Cannot inspect process/RSS state; no process started: {e}')
    cas={'M2','Singular','sage','sage-python','gap','Macaulay2'}
    active=[p for p in before if Path(p[3]).name in cas]
    if active: sys.exit(f'Existing CAS process(es); wait for user-owned job to end: {active}')
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key]='1'
    stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')
    stem=logs/f'{stamp}-{a.tag}'
    env['GS_RUN_OUTPUT']=str(stem)+'.artifacts'
    Path(env['GS_RUN_OUTPUT']).mkdir()
    metadata={'command':cmd,'cwd':str(run),'limits':vars(a),'start':stamp,
              'guard_sha256':__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest(),
              'sampling_note':'1-second RSS sampling can miss short-lived peaks',
              'single_thread':True,'output':env['GS_RUN_OUTPUT'],
              'effective_seconds':effective_seconds,'start_local':now.isoformat(),
              'absolute_computation_cutoff':STOP_WORK.isoformat(),
              'thread_environment':{key:env[key] for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']}}
    start=time.monotonic(); peak=0; reason='completed'
    with open(str(stem)+'.stdout','x') as out,open(str(stem)+'.stderr','x') as err:
        child=subprocess.Popen(cmd,cwd=run,env=env,stdout=out,stderr=err,start_new_session=True)
        try:
            while child.poll() is None:
                try: rss=sum(int(p[2]) for p in processes() if int(p[1])==child.pid)
                except Exception:
                    reason='RSS monitor unavailable'; break
                peak=max(peak,rss)
                if time.monotonic()-start>effective_seconds: reason='time limit'; break
                if rss>a.memory_mb*1024: reason='RSS limit'; break
                time.sleep(1)
        except KeyboardInterrupt: reason='interrupted'
        finally:
            if child.poll() is None:
                os.killpg(child.pid,signal.SIGTERM)
                try: child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid,signal.SIGKILL); child.wait()
    metadata.update(seconds=round(time.monotonic()-start,3),peak_rss_kb=peak,
                    reason=reason,exit_code=child.returncode)
    Path(str(stem)+'.json').write_text(json.dumps(metadata,indent=2)+'\n')
    with (run/'RUN_LOG.jsonl').open('a') as log: log.write(json.dumps(metadata)+'\n')
    print(json.dumps(metadata,indent=2))
    print('stdout:',str(stem)+'.stdout')
    sys.exit(child.returncode if reason=='completed' else 124)

if __name__=='__main__': main()
