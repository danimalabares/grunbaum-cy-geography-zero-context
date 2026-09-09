#!/usr/bin/env python3
"""Check saved rational contradictions by direct summation; no CAS import."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import time

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    start = time.monotonic()
    inputs = [Path(__file__)]
    results = []
    for degree in [3, 4, 5]:
        p = RUN / ('data/higher_matrix_degrees/degree%d.json' % degree if degree < 5
                   else 'data/degree5_cas/degree5_linear_system.json')
        inputs.append(p)
        data = json.loads(p.read_text())
        equations = data['equations']
        if degree < 5:
            weights = {int(i): Q(c) for i, c in data['contradiction']['rows']}
            expected = Q(data['contradiction']['constant'])
        else:
            log = RUN / 'logs/20260908T230258417055-degree5-singular-witness-v2.stdout'
            inputs.append(log)
            text = log.read_text()
            assert 'EXACT_UNIT_RELATION' in text and 'FAILED' not in text and '? ' not in text
            weights = {}
            for line in text.splitlines():
                if line.startswith('WITNESS='):
                    i, c = line.removeprefix('WITNESS=').split(':', 1)
                    assert int(i) not in weights
                    weights[int(i)] = Q(c)
            expected = Q(1)
        value = [Q(0)] * len(equations[0])
        for i, c in weights.items():
            assert 0 <= i < len(equations)
            for j, a in enumerate(equations[i]):
                value[j] += c * Q(a)
        assert not any(value[:-1]) and value[-1] == expected and expected != 0
        results.append({'degree': degree, 'field': 'Q', 'unknowns': data['unknowns'],
                        'equation_count': len(equations), 'witness_support': len(weights),
                        'weights': [[i, str(c)] for i, c in sorted(weights.items())],
                        'verified_sum': [str(c) for c in value],
                        'status': 'COMPUTER-CERTIFIED exact affine inconsistency'})
    result = {'checks': results, 'seconds': time.monotonic() - start,
              'proof': 'The saved weighted sum of all variable coefficients is zero and the constant is nonzero.',
              'input_hashes': {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in inputs}}
    out.mkdir(parents=True)
    (out / 'linear_unit_certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
    for row in results:
        print('VERIFIED', row['degree'], row['unknowns'], row['witness_support'], row['verified_sum'][-1])


if __name__ == '__main__':
    main()
