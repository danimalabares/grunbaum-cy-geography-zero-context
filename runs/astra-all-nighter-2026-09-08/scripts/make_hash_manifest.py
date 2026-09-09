#!/usr/bin/env python3
"""Seal final reports/evidence and the actually recorded read-only inputs."""
import datetime
import hashlib
import json
from pathlib import Path
import re

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    inputs = {}
    pattern = re.compile(r'"([^"\\]+)"\s*:\s*"([a-f0-9]{64})"')
    for record in RUN.rglob('*.json'):
        for name, expected in pattern.findall(record.read_text()):
            if '/' not in name:
                continue
            candidates = [Path(name)] if Path(name).is_absolute() else [REPO / name, RUN / name]
            path = next((p.resolve() for p in candidates if p.is_file()), None)
            if path is None or path.is_relative_to(RUN):
                continue
            actual = digest(path)
            assert actual == expected, (record, path, 'recorded input changed')
            inputs[str(path)] = actual
    # Proof documents explicitly inspected in the targeted audit. Code/data
    # dependencies are collected above from the executed certificate records.
    documents = {
        'astra-computation-2026-09-08': [
            'COMPUTATION_RESULTS.md', 'GEOGRAPHY_THEOREM.md', 'REPRODUCE.md',
            'RAMIFIED_FIBRE_EQUATIONS.md', 'RAMIFIED_POINT_CONSTRUCTION.md',
            'RAMIFIED_POINT_REVIEW.md', 'RAMIFIED_FLATNESS_IDENTITY.md', 'RAMIFIED_ARITHMETIC.md',
            'SPARSE_AND_RAMIFIED_REVIEW.md', 'BOUNDED_FIELD_SEARCH.md', 'EXTRACTION_NEXT.md',
            'DEGREE8_PICARD_FORMULA.md', 'PRODUCT_RANK_CERTIFICATE.md',
            'SPARSE_THREE_ORBIT_ATTEMPT.md', 'SPARSE_DIRECTION_REJECTED.md', 'ARTIFACT_SHA256SUMS'],
        'astra-daytime-2026-09-08': [
            'FIXED_CHART.md', 'FIXED_CHART_REVIEW.md', 'HILBERT_EXPLANATION.md',
            'PICARD_VERTICAL_CLASS_OBSTRUCTION.md', 'PICARD_HODGE_PLAN.md', 'ARTIFACT_SHA256SUMS'],
    }
    for packet, names in documents.items():
        for name in names:
            p = RUN.parent / packet / name
            if p.is_file():
                inputs[str(p)] = digest(p)
    for p in [Path('/Users/daniel/github/grunbaum-zero-context-proof/PROOF.md'),
              Path('/Users/daniel/github/heap-project/homological-algebra.tex'),
              Path('/Users/daniel/github/heap-project/AGENTS.md'),
              Path('/Users/daniel/.codex/skills/mathematical-paper-audit/SKILL.md'),
              Path('/Users/daniel/.codex/skills/.system/openai-docs/SKILL.md')]:
        if p.is_file():
            inputs[str(p)] = digest(p)
    target = RUN / 'INPUT_HASHES.json'
    assert not target.exists()
    target.write_text(json.dumps({'sha256': dict(sorted(inputs.items())),
                                 'note': 'Read-only source, code, data and instruction inputs; Heap is learning context, not mathematical authority.'}, indent=2) + '\n')
    manifest = RUN / 'HASH_MANIFEST.json'
    assert not manifest.exists()
    files = {str(p.relative_to(RUN)): {'sha256': digest(p), 'bytes': p.stat().st_size}
             for p in sorted(RUN.rglob('*'))
             if p.is_file() and p.name not in {'.cas.lock', 'HASH_MANIFEST.json'}
             and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                   'files': files, 'excluded': ['HASH_MANIFEST.json (self)', '.cas.lock', '__pycache__'],
                                   'scope': 'All final new evidence, including preserved failed attempts, immutable logs, scripts, reports and reproduction checkpoints.'}, indent=2) + '\n')
    print('SEALED', len(files), 'NEW_FILES', len(inputs), 'READ_ONLY_INPUTS')
    print('MANIFEST_SHA256', digest(manifest))


if __name__ == '__main__':
    main()
