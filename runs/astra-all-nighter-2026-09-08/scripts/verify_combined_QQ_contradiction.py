#!/usr/bin/env python3
"""Independent exact replay of necessary constraints and polynomial eliminations.

Imports none of the equation constructors or elimination implementation.
An inclusion in the original ideal suffices: every final constraint is a
necessary equation, and each substitution divides only by a rational unit.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import time

RUN = Path(__file__).resolve().parents[1]
Q = Fraction


def decode(data):
    return {tuple(m): Q(a) for m, a in data}


def canonical(poly):
    poly = {m: c for m, c in poly.items() if c}
    if not poly:
        return ()
    lead = poly[min(poly)]
    return tuple(sorted((m, c / lead) for m, c in poly.items()))


def substitute(poly, variable, rhs):
    answer = defaultdict(Q)
    for monomial, coefficient in poly:
        copies = monomial.count(variable)
        remaining = tuple(x for x in monomial if x != variable)
        # Cartesian expansion differs from the constructor's recursive
        # polynomial-power substitution. Repeated monomials accumulate.
        for factors in itertools.product(tuple(rhs.items()), repeat=copies):
            m = list(remaining)
            c = coefficient
            for f, a in factors:
                m.extend(f)
                c *= a
            answer[tuple(sorted(m))] += c
    return canonical(answer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    out.mkdir(parents=True)
    start = time.monotonic()
    base = RUN / 'data/combined_matrix_QQ'
    paths = [base / 'original_system_QQ.json', base / 'G2_elimination_QQ.json',
             base / 'reduced_locus_QQ.json', Path(__file__)]
    original, elimination, reduced = [json.loads(p.read_text()) for p in paths[:3]]
    polynomials = list(map(decode, original['polynomials']))
    linear = [{int(i): Q(c) for i, c in row} for row in original['G2_rows']]
    constraints = []
    for number, encoded, weights in elimination['constraints']:
        actual = defaultdict(Q)
        h = defaultdict(Q)
        for i, w in weights:
            w = Q(w)
            for m, c in polynomials[i].items():
                actual[m] += w * c
            for j, c in linear[i].items():
                h[j] += w * c
        assert not any(h.values()), number
        assert {m: c for m, c in actual.items() if c} == decode(encoded), number
        constraints.append(canonical(actual))
    current = set(constraints) - {()}
    print('VERIFIED_ORIGINAL_ROW_COMBINATIONS', len(constraints), flush=True)
    remaining = set(range(72))
    history = []
    for stage, peel in enumerate(reversed(reduced['reverse_peel_reconstruction']), 1):
        v = peel['variable']
        source = decode(peel['source'])
        rhs = decode(peel['rhs'])
        key = canonical(source)
        assert v in remaining and key in current
        coefficient = source[(v,)]
        assert coefficient != 0
        assert all(v not in m for m in source if m != (v,))
        assert rhs == {m: -c / coefficient for m, c in source.items() if m != (v,)}
        current.remove(key)
        current = {substitute(q, v, rhs) for q in current} - {()}
        remaining.remove(v)
        assert all(v not in m for q in current for m, c in q)
        history.append({'step': stage, 'variable': v, 'equations': len(current),
                        'terms': sum(map(len, current)), 'seconds': time.monotonic() - start})
        with (out / 'steps.jsonl').open('a') as f:
            f.write(json.dumps(history[-1]) + '\n')
        if stage % 10 == 0:
            print('VERIFIED_PEELS', stage, flush=True)
    assert remaining == set(reduced['variable_indices'])
    assert current == {canonical(decode(p)) for p in reduced['equations']}
    assert (((), Q(1)),) in current
    result = {'status': 'COMPUTER-CERTIFIED exact characteristic-zero contradiction',
              'original_unknowns': 123, 'original_equations': len(polynomials),
              'necessary_row_combinations_verified': len(constraints),
              'constant_unit_eliminations_verified': len(history),
              'remaining_variables': len(remaining), 'remaining_equations': len(current),
              'literal_one_verified': True, 'seconds': time.monotonic() - start,
              'proof': 'Every initial constraint is a checked rational linear combination of the original equations with G2 canceled. At each step a present equation solves one variable with a nonzero rational constant coefficient; substitution is exact. The final necessary equations include 1=0.',
              'input_hashes': {str(p.relative_to(RUN.parents[1])): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in paths}}
    (out / 'contradiction_verified.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
