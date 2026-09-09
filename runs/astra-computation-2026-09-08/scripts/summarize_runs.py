#!/usr/bin/env python3
"""Inventory immutable guarded process records; never infer mathematical success.

Only completed wrapper metadata are read. A process exit code is NOT a
geometric certificate. RSS is the maximum of one-second group samples, not
an operating-system high-water mark. This script performs no CAS work.
"""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]


def main():
    rows = []
    for path in sorted((RUN / 'logs').glob('*.json')):
        item = json.loads(path.read_text())
        if not {'command', 'seconds', 'peak_rss_kb', 'reason'} <= item.keys():
            continue
        rows.append((path.name, item))
    print('# Measured guarded jobs\n')
    print('COMPUTER-CERTIFIED process metadata, not mathematical verdicts. ')
    print('RSS is a one-second process-group sample maximum; very short jobs ')
    print('may finish between samples. Limits were checked before launching.\n')
    print('| Record | Seconds | Sampled MiB | Exit | Stop reason |')
    print('|---|---:|---:|---:|---|')
    for name, item in rows:
        print(f"| [{name}](logs/{name}) | {item['seconds']:.3f} | "
              f"{item['peak_rss_kb']/1024:.2f} | {item['exit_code']} | "
              f"{item['reason']} |")
    print('\nTotal recorded wrapper time: '
          f"{sum(item['seconds'] for _, item in rows):.3f} seconds. "
          'This is not total research-session wall time.')


if __name__ == '__main__':
    main()
