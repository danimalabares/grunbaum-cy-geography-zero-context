#!/usr/bin/env python3
"""Read-only source/process inspection; write only fresh final evidence here."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    started = time.monotonic()
    dest = RUN / 'logs/final_state.json'
    assert not dest.exists()
    packets = []
    for name in ['astra-computation-2026-09-08', 'astra-daytime-2026-09-08']:
        base = RUN.parent / name
        manifest = base / 'ARTIFACT_SHA256SUMS'
        bad = []
        files = 0
        size = 0
        for line in manifest.read_text().splitlines():
            sha, relative = line.split(maxsplit=1)
            p = base / relative.lstrip('*')
            assert p.resolve().is_relative_to(base.resolve())
            if not p.is_file() or digest(p) != sha:
                bad.append(relative)
            files += 1
            if p.is_file():
                size += p.stat().st_size
        packets.append({'packet': name, 'manifest_sha256': digest(manifest),
                        'files_checked': files, 'bytes_checked': size, 'mismatches': bad})
    assert all(not p['mismatches'] for p in packets)
    raw = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,pgid=,rss=,comm=,args='], text=True)
    processes = [line.split(None, 5) for line in raw.splitlines() if line.strip()]
    ancestors = {os.getpid()}
    parent = os.getppid()
    bypid = {int(p[0]): p for p in processes}
    while parent and parent not in ancestors:
        ancestors.add(parent)
        parent = int(bypid[parent][1]) if parent in bypid else 0
    script_names = [p.name for p in (RUN / 'scripts').glob('*.py')]
    owned = []
    cas = []
    for row in processes:
        pid = int(row[0])
        if pid in ancestors:
            continue
        command = row[5] if len(row) > 5 else ''
        if RUN.name in command or any('scripts/' + n in command for n in script_names):
            owned.append({'pid': pid, 'pgid': int(row[2]), 'rss_kib': int(row[3]), 'command': command})
        if Path(row[4]).name in {'Singular', 'M2', 'sage', 'sage-python', 'gap', 'Macaulay2'}:
            cas.append({'pid': pid, 'rss_kib': int(row[3]), 'executable': row[4]})
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    status = subprocess.check_output(['git', 'status', '--short'], cwd=REPO, text=True)
    initial = json.loads((RUN / 'SOURCE_STATE.json').read_text())
    assert head == initial['head'] and status == initial['status']
    guarded = []
    for p in sorted((RUN / 'logs').glob('*.json')):
        d = json.loads(p.read_text())
        if isinstance(d, dict) and 'guard_sha256' in d and 'limits' in d:
            guarded.append(d)
    result = {'event': 'final_source_and_process_audit',
              'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'command': ['python3', '-B', str(Path(__file__).relative_to(REPO))],
              'head': head, 'working_tree_status': status,
              'source_state_matches_start': True, 'frozen_packets': packets,
              'owned_background_processes': owned, 'other_visible_CAS_processes': cas,
              'guarded_jobs_completed': len(guarded),
              'guarded_jobs_time_limited': sum(d.get('reason') == 'time limit' for d in guarded),
              'maximum_sampled_group_RSS_KiB': max(d['peak_rss_kb'] for d in guarded),
              'maximum_guarded_job_seconds': max(d['seconds'] for d in guarded),
              'sampling_limit': 'One-second sampling can miss short-lived peaks; this is not an exact high-water mark.',
              'seconds': time.monotonic() - started,
              'redemptions_attempted': 0, 'redemptions_confirmed': 0,
              'script_sha256': digest(Path(__file__))}
    dest.write_text(json.dumps(result, indent=2) + '\n')
    with (RUN / 'RUN_LOG.jsonl').open('a') as log:
        log.write(json.dumps(result) + '\n')
    print(json.dumps(result, indent=2))
    assert not owned, 'Inspect owned process report; no process was terminated by this audit.'


if __name__ == '__main__':
    main()
