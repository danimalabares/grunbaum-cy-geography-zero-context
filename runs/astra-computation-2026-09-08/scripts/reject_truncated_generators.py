#!/usr/bin/env python3
"""Bounded negative flatness checks for three finite generator candidates.

For 16 cubics the degree-four multiplication map has shape 330 x 128.
The prescribed central Hilbert function requires rank 98. A rank >=99
at q=1 or 2 modulo 101 proves a nonzero rational polynomial minor and
REJECTS generic degreewise flatness of that fixed generator candidate.
It does not reject other higher generator corrections. Rank 98 at the
test values is INCONCLUSIVE, never a flatness or smoothness certificate.

All input files are read-only. Only standard-library finite-field linear
arithmetic is used. No polynomial CAS, Groebner basis, or syzygy search.
The original selected 99 x 99 minor is verified independently of the
sparse pivot search by dense modular determinant elimination.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from itertools import combinations_with_replacement

sys.dont_write_bytecode = True
sys.setrecursionlimit(20000)
RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
SOURCE = REPO.parent / 'grunbaum-zero-context-proof'
PRIME = 101
ZERO = (0,) * 8


def add(a, b, scale=1):
    out = dict(a)
    for exponent, coefficient in b.items():
        value = (out.get(exponent, 0) + scale * coefficient) % PRIME
        if value:
            out[exponent] = value
        else:
            out.pop(exponent, None)
    return out


def multiply(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            exponent = tuple(x + y for x, y in zip(e, f))
            out[exponent] = (out.get(exponent, 0) + c * d) % PRIME
    return {e: c for e, c in out.items() if c}


def parse_polynomial(expression, values, denominators):
    """AST whitelist; never eval source code or permit arbitrary names."""
    def rec(node):
        if isinstance(node, ast.Constant):
            assert isinstance(node.value, int)
            return {ZERO: node.value % PRIME} if node.value % PRIME else {}
        if isinstance(node, ast.Name):
            if node.id in values:
                value = values[node.id] % PRIME
                return {ZERO: value} if value else {}
            assert node.id in 'abcdefgh' and len(node.id) == 1, node.id
            return {tuple(int(i == 'abcdefgh'.index(node.id)) for i in range(8)): 1}
        if isinstance(node, ast.UnaryOp):
            assert isinstance(node.op, (ast.USub, ast.UAdd))
            value = rec(node.operand)
            return {e: (-c) % PRIME for e, c in value.items()} if isinstance(node.op, ast.USub) else value
        assert isinstance(node, ast.BinOp), ast.dump(node)
        a = rec(node.left)
        if isinstance(node.op, ast.Pow):
            assert isinstance(node.right, ast.Constant)
            power = node.right.value
            assert isinstance(power, int) and 0 <= power <= 6
            value = {ZERO: 1}
            for _ in range(power):
                value = multiply(value, a)
            return value
        b = rec(node.right)
        if isinstance(node.op, ast.Add):
            return add(a, b)
        if isinstance(node.op, ast.Sub):
            return add(a, b, -1)
        if isinstance(node.op, ast.Mult):
            return multiply(a, b)
        if isinstance(node.op, ast.Div):
            # Only rational-number coefficients: disallow parameter-dependent
            # denominators even if they become scalars after specialization.
            denominator_node = node.right
            if isinstance(denominator_node, ast.UnaryOp):
                assert isinstance(denominator_node.op, (ast.USub, ast.UAdd))
                denominator_node = denominator_node.operand
            assert isinstance(denominator_node, ast.Constant)
            assert isinstance(denominator_node.value, int)
            # Source coefficient denominators must be nonzero scalars mod101.
            assert set(b) == {ZERO}, 'Nonconstant or zero coefficient denominator'
            denominator = b[ZERO]
            denominators.add(denominator)
            inverse = pow(denominator, -1, PRIME)
            return {e: c * inverse % PRIME for e, c in a.items()}
        raise AssertionError(ast.dump(node))
    return rec(ast.parse(expression.replace('^', '**'), mode='eval').body)


def matrix_entries(path):
    """Extract only the polynomial row in saved 1 x 16 M2 matrices."""
    raw = path.read_text()
    bodies = re.findall(r',\s*\{\{([^{}]*)\}\}\)', raw)
    entries = [body.split(',') for body in bodies]
    assert len(entries) == 5 and all(len(row) == 16 for row in entries)
    assert all(not re.search(r'[{};]', entry) for row in entries for entry in row)
    return entries


def evaluate(entries, values, denominators):
    result = [{} for _ in range(16)]
    for row in entries:
        for i, entry in enumerate(row):
            result[i] = add(result[i], parse_polynomial(entry.strip(), values, denominators))
    assert all(all(sum(e) == 3 for e in poly) for poly in result)
    return result


def modular_determinant(matrix):
    a = [row[:] for row in matrix]
    result = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j] % PRIME), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            result = -result
        value = a[j][j] % PRIME
        result = result * value % PRIME
        inverse = pow(value, -1, PRIME)
        for i in range(j + 1, len(a)):
            factor = a[i][j] * inverse % PRIME
            if factor:
                for k in range(j + 1, len(a)):
                    a[i][k] = (a[i][k] - factor * a[j][k]) % PRIME
            a[i][j] = 0
    return result % PRIME


def multiplication_rank_certificate(generators, stop_at=99):
    monomials = [tuple(c.count(i) for i in range(8))
                 for c in combinations_with_replacement(range(8), 4)]
    assert len(monomials) == 330
    indices = {m: i for i, m in enumerate(monomials)}
    columns = []
    for i in range(16):
        for j in range(8):
            column = {}
            for e, coefficient in generators[i].items():
                f = list(e)
                f[j] += 1
                column[indices[tuple(f)]] = coefficient
            columns.append(column)
    basis = {}
    chosen_columns, chosen_rows = [], []
    for c, original in enumerate(columns):
        current = dict(original)
        while current:
            pivot = min(current)
            if pivot not in basis:
                inverse = pow(current[pivot], -1, PRIME)
                basis[pivot] = {r: v * inverse % PRIME for r, v in current.items()}
                chosen_columns.append(c)
                chosen_rows.append(pivot)
                break
            coefficient = current[pivot]
            current = add(current, basis[pivot], -coefficient)
        if len(chosen_columns) >= stop_at:
            break
    minor = [[columns[c].get(r, 0) for c in chosen_columns] for r in chosen_rows]
    determinant = modular_determinant(minor)
    assert determinant
    exhaustive = c + 1 == len(columns)
    return {
        'rank_lower_bound': len(chosen_columns),
        'rank_exact': len(chosen_columns) if exhaustive else None,
        'columns_scanned': c + 1,
        'all_columns_scanned': exhaustive,
        'minor_rows_exponents': [monomials[r] for r in chosen_rows],
        'minor_columns_generator_variable_1_based': [[c // 8 + 1, c % 8 + 1] for c in chosen_columns],
        'minor_determinant_mod101': determinant,
        'minor_integer_residue_matrix_sha256': hashlib.sha256(json.dumps(minor, separators=(',', ':')).encode()).hexdigest(),
    }


def main():
    started = time.monotonic()
    output = Path(os.environ['GS_RUN_OUTPUT']).resolve()
    assert output.is_relative_to(RUN)
    output.mkdir(parents=True, exist_ok=True)
    json_path = REPO / 'equations/deformation_data.json'
    data = json.loads(json_path.read_text())
    assert data['source_commit'] == 'ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b'
    denominators = set()
    f0 = evaluate([data['generator_order']], {}, denominators)
    selected_tangent = evaluate([data['first_order_corrections']], {}, denominators)
    baseline = multiplication_rank_certificate(f0)
    assert baseline['rank_exact'] == 98
    sparse_path = SOURCE / 'reconstruct/p1_line_state_F_order4.txt'
    universal_path = SOURCE / 'reconstruct/p1_universal_order4_vF.txt'
    candidates = [
        ('raw_generic_six_jet', data['six_jet_coefficients'], json_path, 'generic_equivariant_six_jet'),
        ('saved_sparse_P1_F4', matrix_entries(sparse_path), sparse_path, 'sparse_P1_line_distinct_from_selected_tangent'),
        ('universal_F4_selected_S3_weights', matrix_entries(universal_path), universal_path, 'selected_tangent_unaveraged_universal_presentation'),
    ]
    results = []
    for label, entries, source, lineage in candidates:
        def value_at(q):
            if label == 'raw_generic_six_jet':
                value = [{} for _ in range(16)]
                for degree, row in enumerate(entries):
                    for i, entry in enumerate(row):
                        value[i] = add(value[i], parse_polynomial(entry, {}, denominators), pow(q, degree, PRIME))
                return value
            values = {'t_1': q} if label == 'saved_sparse_P1_F4' else {
                f't_{i + 1}': weight * q for i, weight in enumerate(data['selected_tangent_coordinates_53'])}
            return evaluate(entries, values, denominators)
        assert value_at(0) == f0
        tangent_values = {'t_1': 1} if label == 'saved_sparse_P1_F4' else {
            f't_{i + 1}': weight for i, weight in enumerate(data['selected_tangent_coordinates_53'])}
        tangent = evaluate([entries[1]], {} if label == 'raw_generic_six_jet' else tangent_values, denominators)
        matches = tangent == selected_tangent
        assert matches == (label != 'saved_sparse_P1_F4')
        attempts = []
        for q in (1, 2):
            certificate = multiplication_rank_certificate(value_at(q))
            certificate['q_value'] = q
            attempts.append(certificate)
            print(label, 'q=', q, 'RANK_AT_LEAST', certificate['rank_lower_bound'], flush=True)
            if certificate['rank_lower_bound'] > 98:
                break
        rejected = any(a['rank_lower_bound'] > 98 for a in attempts)
        results.append({
            'candidate': label, 'lineage': lineage, 'source_path': str(source),
            'prime': PRIME, 'matrix_shape': [330, 128], 'required_rank': 98,
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'special_fibre_matches': True, 'first_order_matches_selected_mod101': matches,
            'status': 'FAILED: polynomial generator candidate is generically nonflat over Q' if rejected else 'OPEN: sampled degree-four ranks are inconclusive',
            'rejected_generic_degreewise_flatness_over_Q': rejected,
            'attempts': attempts,
            'does_not_reject_higher_generator_corrections': True,
            'smoothness_claim': False,
        })
        checkpoint = output / f'truncated_{label}_degree4.json'
        with checkpoint.open('x') as stream:
            json.dump(results[-1], stream, indent=2)
            stream.write('\n')
        print('CANDIDATE_CHECKPOINT', checkpoint, flush=True)
    result = {
        'mathematical_test': 'degree-four multiplication map S1 tensor k16 -> S4',
        'matrix_shape': [330, 128], 'prime': PRIME, 'required_rank': 98,
        'source_commit': data['source_commit'], 'central_rank_certificate': baseline,
        'coefficient_denominator_residues': sorted(denominators),
        'all_denominators_checked_nonzero_mod101': True,
        'characteristic_zero_transfer': 'A nonzero evaluated minor mod101 is a nonzero minor of the fixed rational polynomial matrix in q; generic rank over Q(q) is at least that minor size.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'candidates': results, 'seconds': time.monotonic() - started,
    }
    destination = output / 'truncated_generator_degree4_ranks.json'
    with destination.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('CERTIFICATE', destination)
    print('SECONDS', result['seconds'])


if __name__ == '__main__':
    main()
