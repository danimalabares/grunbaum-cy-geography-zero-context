#!/usr/bin/env python3
"""Replay successful finite checks sequentially under this run's resource guard.

One entry point; default starts the preserved overnight guard. --child is
only for its own monitored subprocess. Outputs must be fresh and in this run.
The fixed historical calendar deadlines are intentionally not bypassed.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parents[1]
OLD = RUN.parent / 'astra-computation-2026-09-08'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--child', action='store_true')
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists(), 'Use a fresh output directory within this run.'
    if not args.child:
        cmd = [sys.executable, '-B', str(RUN / 'scripts/run_guarded.py'),
               '--seconds', '180', '--memory-mb', '2800', '--tag', 'reproduce-successes',
               '--', sys.executable, '-B', str(Path(__file__).resolve()),
               '--child', '--output', str(out)]
        raise SystemExit(subprocess.call(cmd, cwd=RUN))
    assert os.environ.get('GS_RUN_OUTPUT'), 'The child must run through the guard.'
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        assert os.environ.get(key) == '1'
    out.mkdir(parents=True)
    jobs = [
        ('export', OLD / 'scripts/verify_ramified_export.py', []),
        ('independent-audit', RUN / 'scripts/audit_export_exact.py', []),
        ('smoothness', RUN / 'scripts/check_smoothness_transfer.py', [str(out / 'smoothness.json')]),
        ('lines', RUN / 'scripts/certify_degeneration_lines_v2.py', ['--output', str(out / 'lines')]),
        ('facet-exhaustion', RUN / 'scripts/certify_facet_transverse_exhaustion.py', ['--output', str(out / 'facets')]),
        ('local-topology', RUN / 'scripts/check_topology_local_point.py', [str(out / 'topology.json')]),
        ('support-Q', RUN / 'scripts/sparse_support_closure.py', ['--prime', '0', '--seconds', '60', '--output', str(out / 'support')]),
        ('graph-exclusion-Q', RUN / 'scripts/equation_reduction_linear_u_QQ_certificate.py', ['--output', str(out / 'graph')]),
        ('degree345-unit-identities', RUN / 'scripts/verify_linear_unit_relations.py', ['--output', str(out / 'units')]),
        ('combined-Q-unit', RUN / 'scripts/verify_combined_QQ_contradiction.py', ['--output', str(out / 'combined-unit')]),
        ('seven-orbit-extensions', RUN / 'scripts/check_sparse_orbit_extensions.py', ['--output', str(out / 'orbit-extensions')]),
        ('singular-eight-slice', RUN / 'scripts/certify_singular_eight_parameter_slice_v3.py', ['--output', str(out / 'singular-slice')]),
    ]
    for tag, script, extra in jobs:
        env = os.environ.copy()
        artifacts = out / (tag + '.artifacts')
        artifacts.mkdir()
        env['GS_RUN_OUTPUT'] = str(artifacts)
        cmd = [sys.executable, '-B', str(script), *extra]
        started = time.monotonic()
        with (out / (tag + '.stdout')).open('x') as stdout, (out / (tag + '.stderr')).open('x') as stderr:
            process = subprocess.run(cmd, cwd=RUN, env=env, stdout=stdout, stderr=stderr)
        row = {'tag': tag, 'command': cmd, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'seconds': time.monotonic() - started, 'exit_code': process.returncode,
               'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest()}
        with (out / 'steps.jsonl').open('a') as log:
            log.write(json.dumps(row) + '\n')
        print(tag, 'PASS' if process.returncode == 0 else 'FAIL', flush=True)
        if process.returncode:
            raise SystemExit(process.returncode)
    (out / 'SUCCESS.json').write_text(json.dumps({'checks': len(jobs), 'status': 'all passed'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
