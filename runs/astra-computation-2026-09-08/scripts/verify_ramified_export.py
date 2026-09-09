#!/usr/bin/env python3
"""Independent rendering, indexing, and Jacobian check of the closed-fibre data.

Does not import the exporter. Parses the displayed sixteen cubics back into
monomial/coefficient maps, checks their S3-orbit data, and recomputes the
270-square determinant by COLUMN elimination. This verifies the finite
presentation, not the accepted all-orders Hilbert-chart theorem or original
smoothness identities. The latter are explicit dependencies of the proof.
"""
import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
LETTERS = 'abcdefgh'


def exponent(word):
    answer = [0]*8
    for token in word.strip().split('*'):
        hit = re.fullmatch(r'([a-h])(?:\^(\d+))?', token)
        assert hit, ('bad monomial', word)
        answer[LETTERS.index(hit[1])] += int(hit[2] or 1)
    assert sum(answer) == 3
    return tuple(answer)


def det_columns(matrix, prime):
    a = [row[:] for row in matrix]
    result = 1
    for k in range(len(a)):
        j = next(j for j in range(k, len(a)) if a[k][j] % prime)
        if j != k:
            for row in a:
                row[k], row[j] = row[j], row[k]
            result = -result
        pivot = a[k][k] % prime
        result = result*pivot % prime
        inverse = pow(pivot, -1, prime)
        for j in range(k+1, len(a)):
            multiplier = a[k][j]*inverse % prime
            if multiplier:
                for i in range(k, len(a)):
                    a[i][j] = (a[i][j]-multiplier*a[i][k]) % prime
    return result


def main():
    datafile = RUN/'data/ramified_fibre_coefficients.json'
    docfile = RUN/'RAMIFIED_FIBRE_EQUATIONS.md'
    chartfile = RUN/'data/fixed_chart.json'
    data = json.loads(datafile.read_text())
    chart = json.loads(chartfile.read_text())
    assert data['prime'] == 101
    assert data['uniformizer_equation']['coefficients_low_to_high'] == [-101,0,0,0,0,0,0,1]
    assert len(data['coefficient_unknowns']) == 271
    dep = data['dependent_coordinate_indices_zero_based']
    free = data['free_coordinate_indices_zero_based']
    assert sorted(dep+free) == list(range(291))
    assert dep == chart['dependent_coordinates'] and free == chart['free_coordinates']
    lookup = {(i, tuple(m)): j+1 for j, orbit in enumerate(chart['coefficient_orbits'])
              for i, m in orbit}
    text = docfile.read_text()
    blocks = re.findall(r'```text\n(F_\d+ =.*?)\n```', text, re.S)
    assert len(blocks) == 16
    count = 0
    for i, (rendered, generator) in enumerate(zip(blocks, data['cubic_equations'])):
        central = rendered.splitlines()[0]
        hit = re.fullmatch(r'F_(\d+) = ([a-h*^\d]+)', central)
        assert hit and int(hit[1]) == i+1
        parsed = {exponent(hit[2]): ('constant', '1')}
        tail = '\n'.join(rendered.splitlines()[1:])
        terms = list(re.finditer(r'lambda_(\d+)\*\(([^()]*)\)', tail))
        remainder = re.sub(r'lambda_(\d+)\*\(([^()]*)\)', '', tail)
        assert set(remainder) <= set(' +\n')
        for term in terms:
            coefficient = int(term[1])
            for word in term[2].split('+'):
                m = exponent(word)
                assert m not in parsed
                assert lookup[i, m] == coefficient
                parsed[m] = ('lambda', coefficient)
        expected = {}
        for term in generator['terms']:
            m = tuple(term['monomial_exponents'])
            expected[m] = (('constant', term['coefficient_constant'])
                           if 'coefficient_constant' in term else
                           ('lambda', term['lambda_index_one_based']))
        assert parsed == expected and len(parsed) == 105
        count += len(parsed)
    for j, definition in enumerate(data['lambda_definitions']):
        assert definition['lambda_index_one_based'] == j+1
        if j in dep:
            assert definition['theta_index_one_based'] == dep.index(j)+1
        else:
            coefficients = definition['pi_polynomial_coefficients']
            assert len(coefficients) == 7 and Fraction(coefficients[0]) == 0
            assert all(Fraction(c).denominator % 101 for c in coefficients)
    jac = []
    for equation in data['bordered_determinant_equations']:
        block = data['shared_block_factors'][equation['block']]
        i, j = equation['bottom_row_zero_based'], equation['right_column_zero_based']
        assert equation['matrix_size'] == block['dimensions'][0]+1 <= 33
        row = {int(k): Fraction(v) for k, v in block['D'][i][j]}
        jac.append([(row.get(k, 0).numerator * pow(row.get(k, 0).denominator, -1, 101)) % 101
                    for k in dep])
    determinant = det_columns(jac, 101)
    assert determinant == 19 == data['certificate']['selected_jacobian_determinant_mod101']
    result = {'status': 'COMPUTER-CERTIFIED independent finite-presentation check',
              'displayed_cubics_checked': 16, 'monomial_coefficients_checked': count,
              'all_orbit_indices_match': True, 'selected_jacobian_determinant_mod101': determinant,
              'method': 'independent Markdown parse and modular column elimination',
              'inputs': {str(p.relative_to(RUN)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [datafile, docfile, chartfile, Path(__file__)]}}
    output = Path(os.environ.get('GS_RUN_OUTPUT', RUN/'certificates'))
    output.mkdir(exist_ok=True)
    dest = output/'independent_ramified_export.json'
    if dest.exists():
        assert json.loads(dest.read_text()) == result
    else:
        dest.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
