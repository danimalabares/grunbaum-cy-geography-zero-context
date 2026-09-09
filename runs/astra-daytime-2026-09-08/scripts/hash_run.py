#!/usr/bin/env python3
"""Freeze a SHA256 inventory of the daytime packet without changing sources.

Run once after final edits. Existing manifests must match exactly; this
never silently updates a frozen inventory. Night artifacts use new paths.
Transient Python caches, the advisory lock and this manifest are excluded.
"""
import hashlib
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
DEST = RUN / 'ARTIFACT_SHA256SUMS'

def main():
    files = sorted(p for p in RUN.rglob('*') if p.is_file()
                   and p != DEST and '__pycache__' not in p.parts
                   and p.name not in {'.cas.lock', '.DS_Store'}
                   and p.suffix != '.pyc')
    lines = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(RUN)}'
             for p in files]
    content = '\n'.join(lines) + '\n'
    if DEST.exists():
        assert DEST.read_text() == content, 'Frozen inventory differs; preserve it and investigate'
    else:
        DEST.write_text(content)
    print(f'FROZEN_DAYTIME_FILES {len(files)}')
    print(DEST)

if __name__ == '__main__':
    main()
