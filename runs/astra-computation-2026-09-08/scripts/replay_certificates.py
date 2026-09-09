#!/usr/bin/env python3
"""The updated continuation starts with two small, sequential certificates.

This is not the exhausted curve/Padé controller. In a fresh evening run,
first copy the declared inputs and adapt ONLY that copy's guarded execution
window as described in OVERNIGHT_PROMPT.md. The resource guard remains
mandatory. No CAS, coefficient-field reconstruction or I-squared job is
silently launched. Default mode prints the two commands without running.
"""
import argparse
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    jobs = [('independent-integer-product-certificate', 'verify_product_minor.py'),
            ('independent-algebraic-coefficient-export', 'verify_ramified_export.py')]
    for tag, script in jobs:
        command = [sys.executable, '-B', str(RUN/'scripts/run_guarded.py'),
                   '--seconds', '300', '--memory-mb', '2800', '--tag', tag,
                   '--', sys.executable, '-B', str(RUN/'scripts'/script)]
        print(' '.join(command), flush=True)
        if args.run:
            completed = subprocess.run(command, cwd=RUN, check=False)
            if completed.returncode:
                sys.exit(completed.returncode)
    print('TWO_SMALL_CERTIFICATES_ONLY; NO_HEAVY_JOB_QUEUED', flush=True)


if __name__ == '__main__':
    main()
