#!/usr/bin/env python3
"""Bounded relative-degree recognition for the ACTUAL ramified point.

Standard-library Python only; exact integer/Fraction LLL. NO CAS, installs,
extra precision or parallel work. Actual-point execution requires the root's
sole substantial-process slot. Default probes: theta1/theta2, degree2/3.

The input is the true pi56 Hensel point, not an F101[[q]] jet: coefficients
are seven-entry vectors modulo M=101^8 in pi^7=101. For degree d, construct
the full rank7(d+1) integer lattice of coefficient vectors c with
sum(c[j,r]*pi^r*theta^j)=0 mod pi56. Its index is M^7.

Short vectors are HEURISTIC polynomial candidates, never exact global
relations. A different output is rigorous: if min(||b_i*||^2)>n*H^2,
there is NO nonzero coefficient vector of height<=H in the lattice. This
rules out that bounded integral coefficient ansatz, not the field degree.

Checkpoints contain the integer basis, unimodular transform and LLL state.
The exact final checker verifies B=U*B_initial, det(U)=+/-1, modular
membership of every row, fresh positive GSO lengths and LLL inequalities
when completion is claimed. No floating-point norm or rank is used.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
RUN = Path(__file__).resolve().parents[1]
P = 101
E = 7
PRECISION = 56
MODULUS = P**8


class Gate(Exception):
    pass


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_data(a):
    a = Q(a)
    return {'numerator':str(a.numerator), 'denominator':str(a.denominator)}


def ring_mul(a, b, modulus=MODULUS):
    out = [0]*E
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    s = i+j
                    out[s % E] += x*y*(P if s >= E else 1)
    return [v % modulus for v in out]


def pi_shift(a, r, modulus=MODULUS):
    out = [0]*E
    for i,x in enumerate(a):
        s = i+r
        out[s % E] = x*(P if s >= E else 1) % modulus
    return out


def monomial_values(theta, degree, modulus=MODULUS):
    powers = [[1]+[0]*(E-1)]
    for _ in range(degree): powers.append(ring_mul(powers[-1], theta, modulus))
    return [pi_shift(powers[j], r, modulus)
            for j in range(degree+1) for r in range(E)]


def relation_residue(coefficients, values, modulus=MODULUS):
    return [sum(c*v[r] for c,v in zip(coefficients,values)) % modulus
            for r in range(E)]


def make_lattice(theta, degree, modulus=MODULUS):
    values = monomial_values(theta, degree, modulus)
    n = E*(degree+1)
    basis = []
    for r in range(E):
        row = [0]*n
        row[r] = modulus
        basis.append(row)
    for j in range(1,degree+1):
        for r in range(E):
            index = E*j+r
            residues = [a if a <= modulus//2 else a-modulus for a in values[index]]
            row = [-a for a in residues]+[0]*(n-E)
            row[index] = 1
            basis.append(row)
    assert len(basis) == n
    assert all(not any(relation_residue(row,values,modulus)) for row in basis)
    return basis, values


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def gram_schmidt(basis, check=None):
    """Exact GSO using the integer Gram matrix, without real embeddings."""
    n = len(basis)
    mu = [[Q(0) for _ in range(n)] for _ in range(n)]
    norms = [Q(0)]*n
    for i in range(n):
        if check: check()
        for j in range(i):
            mu[i][j] = (Q(dot(basis[i],basis[j]))-
                         sum(mu[i][k]*mu[j][k]*norms[k] for k in range(j)))/norms[j]
        norms[i] = Q(dot(basis[i],basis[i]))-sum(mu[i][j]**2*norms[j] for j in range(i))
        assert norms[i] > 0, 'dependent or invalid lattice basis'
    return mu, norms


def nearest(a):
    # Exact nearest integer; half-integer ties go towards positive infinity.
    return (2*a.numerator+a.denominator)//(2*a.denominator)


def determinant(matrix):
    """Bareiss exact determinant, with exact divisions and row pivoting."""
    a = [row[:] for row in matrix]
    n = len(a)
    if not n: return 1
    denominator = 1
    sign = 1
    for k in range(n-1):
        pivot = next((i for i in range(k,n) if a[i][k]), None)
        if pivot is None: return 0
        if pivot != k:
            a[k],a[pivot] = a[pivot],a[k]
            sign = -sign
        leading = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = a[i][j]*leading-a[i][k]*a[k][j]
                assert numerator % denominator == 0
                a[i][j] = numerator//denominator
            a[i][k] = 0
        denominator = leading
    return sign*a[-1][-1]


def verify_transform(basis, transform, original):
    n = len(basis)
    assert all(len(row) == n for row in basis+transform+original)
    for i in range(n):
        assert basis[i] == [sum(transform[i][k]*original[k][j] for k in range(n))
                            for j in range(n)]
    detu = determinant(transform)
    assert abs(detu) == 1, 'recorded transform is not unimodular'
    assert abs(determinant(basis)) == abs(determinant(original))
    return detu


def lll_check(basis, delta):
    mu, norms = gram_schmidt(basis)
    size = all(abs(mu[i][j]) <= Q(1,2) for i in range(len(basis)) for j in range(i))
    lovasz = all(norms[i] >= (delta-mu[i][i-1]**2)*norms[i-1]
                 for i in range(1,len(basis)))
    return mu, norms, size, lovasz


def lll(original, *, delta=Q(3,4), max_seconds=180, max_iterations=10000,
        max_bits=16384, checkpoint=None, resume=None, global_deadline=None):
    """Exact incremental LLL; completed bases are freshly rechecked."""
    start = time.monotonic()
    deadline = min(start+max_seconds, global_deadline or float('inf'))
    n = len(original)
    if resume:
        basis = [row[:] for row in resume['basis']]
        transform = [row[:] for row in resume['unimodular_transform']]
        k = int(resume['next_k'])
        iterations = int(resume['iterations'])
        swaps = int(resume['swaps'])
        reductions = int(resume['size_reductions'])
        verify_transform(basis,transform,original)
    else:
        basis = [row[:] for row in original]
        transform = [[int(i == j) for j in range(n)] for i in range(n)]
        k,iterations,swaps,reductions = 1,0,0,0
    iteration_start = iterations

    def gate():
        if time.monotonic() > deadline: raise Gate('time_limit')
        if iterations-iteration_start >= max_iterations: raise Gate('iteration_limit')

    def state(reason):
        return {'reason':reason, 'basis':basis, 'unimodular_transform':transform,
                'next_k':k, 'iterations':iterations, 'swaps':swaps,
                'size_reductions':reductions, 'delta':fraction_data(delta),
                'elapsed_seconds':round(time.monotonic()-start,3)}

    # Initial GSO is also subject to the wall-clock gate. If it is capped,
    # the unchanged integer basis remains a valid resumable checkpoint.
    try:
        mu,norms = gram_schmidt(basis,gate)
        last_checkpoint = time.monotonic()
        while k < n:
            gate()
            if max(abs(v).bit_length() for row in basis+transform for v in row) > max_bits:
                raise Gate('integer_bit_growth_limit')
            if max(max(a.numerator.bit_length(),a.denominator.bit_length())
                   for row in mu for a in row) > max_bits:
                raise Gate('fraction_bit_growth_limit')
            iterations += 1
            for j in range(k-1,-1,-1):
                r = nearest(mu[k][j])
                if r:
                    basis[k] = [a-r*b for a,b in zip(basis[k],basis[j])]
                    transform[k] = [a-r*b for a,b in zip(transform[k],transform[j])]
                    for s in range(j): mu[k][s] -= r*mu[j][s]
                    mu[k][j] -= r
                    reductions += 1
            if norms[k] >= (delta-mu[k][k-1]**2)*norms[k-1]:
                k += 1
            else:
                oldmu = mu[k][k-1]
                oldleft,oldright = norms[k-1],norms[k]
                newleft = oldright+oldmu**2*oldleft
                newmu = oldmu*oldleft/newleft
                norms[k-1] = newleft
                norms[k] = oldleft*oldright/newleft
                for j in range(k-1): mu[k][j],mu[k-1][j] = mu[k-1][j],mu[k][j]
                mu[k][k-1] = newmu
                for i in range(k+1,n):
                    old = mu[i][k]
                    mu[i][k] = mu[i][k-1]-oldmu*old
                    mu[i][k-1] = old+newmu*mu[i][k]
                basis[k],basis[k-1] = basis[k-1],basis[k]
                transform[k],transform[k-1] = transform[k-1],transform[k]
                swaps += 1
                k = max(k-1,1)
            if checkpoint and (iterations % 25 == 0 or time.monotonic()-last_checkpoint >= 10):
                checkpoint(state('progress'))
                last_checkpoint = time.monotonic()
        # Exact recomputation catches sign/index errors in incremental updates.
        freshmu,freshnorms,size,lovasz = lll_check(basis,delta)
        assert freshmu == mu and freshnorms == norms, 'incremental GSO mismatch'
        assert size and lovasz
        result = state('LLL_completed')
    except Gate as exc:
        result = state(str(exc))
    if checkpoint: checkpoint(result)
    return result


def candidate_rows(basis, values, height, modulus=MODULUS):
    out = []
    seen = set()
    for i,row in enumerate(basis):
        divisor = 0
        for a in row: divisor = gcd(divisor,abs(a))
        assert divisor
        primitive = [a//divisor for a in row]
        if next(a for a in reversed(primitive) if a) < 0: primitive = [-a for a in primitive]
        # Dividing content containing101 can lose precision. Never silently
        # promote such a vector: recheck the primitive vector at FULL modulus.
        if any(relation_residue(primitive,values,modulus)): continue
        if max(map(abs,primitive)) > height: continue
        degree = max(j//E for j,a in enumerate(primitive) if a)
        if degree == 0: continue
        key = tuple(primitive)
        if key in seen: continue
        seen.add(key)
        out.append({'status':'HEURISTIC_modular_relation_not_exact_global_equation',
                    'basis_row':i, 'effective_T_degree':degree,
                    'height':max(map(abs,primitive)), 'content_divided':divisor,
                    'coefficients_by_T_degree':[primitive[j:j+E] for j in range(0,len(primitive),E)],
                    'full_modulus_residue':[0]*E})
    return out


def summarize_basis(result, original, values, heights, modulus=MODULUS):
    basis = result['basis']
    detu = verify_transform(basis,result['unimodular_transform'],original)
    assert all(not any(relation_residue(row,values,modulus)) for row in basis)
    mu,norms,size,lovasz = lll_check(basis,Q(3,4))
    if result['reason'] == 'LLL_completed': assert size and lovasz
    minimum = min(norms)
    n = len(basis)
    exclusions = []
    for height in heights:
        excludes = minimum > n*height*height
        exclusions.append({'height_bound':height, 'squared_threshold':n*height*height,
                           'status':('COMPUTER_CERTIFIED_no_nonzero_bounded_modular_relation'
                                     if excludes else 'INCONCLUSIVE_GSO_lower_bound'),
                           'exhaustive_exclusion':excludes})
    return {'verified_unimodular_determinant':detu,
            'verified_lattice_index':str(abs(determinant(basis))),
            'expected_lattice_index':str(modulus**E),
            'all_basis_rows_verified_in_modular_kernel':True,
            'gram_schmidt_squared_norms':[fraction_data(a) for a in norms],
            'minimum_squared_GSO_norm':fraction_data(minimum),
            'GSO_exclusions':exclusions,
            'size_reduced':size, 'Lovasz_3_over_4':lovasz,
            'candidates':candidate_rows(basis,values,max(heights),modulus)}


def smoke_test():
    # Only tiny known INTEGER lattices; no project point or CAS is used.
    examples = [[[1,1,1],[-1,0,2],[3,5,6]],
                [[101,0,0],[-7,1,0],[-49,0,1]],
                [[100,0],[0,100]]]
    records = []
    for basis in examples:
        result = lll(basis,max_seconds=5,max_iterations=500)
        assert result['reason'] == 'LLL_completed'
        detu = verify_transform(result['basis'],result['unimodular_transform'],basis)
        _,norms,size,lovasz = lll_check(result['basis'],Q(3,4))
        assert size and lovasz
        records.append({'dimension':len(basis), 'determinant':determinant(basis),
                        'transform_determinant':detu, 'iterations':result['iterations'],
                        'reduced_basis':result['basis'],
                        'GSO_squared_norms':[fraction_data(a) for a in norms]})
    assert min(gram_schmidt(examples[-1])[1]) > len(examples[-1])*10**2
    print(json.dumps({'status':'PASS_TINY_INTEGER_LLL_SMOKE', 'tests':records},indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point',type=Path,default=RUN/'data/ramified_hensel_pi56.json')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--theta',type=int,choices=[1,2],nargs='+',default=[1,2])
    ap.add_argument('--degree',type=int,choices=[2,3],nargs='+',default=[2,3])
    ap.add_argument('--height',type=int,choices=[100,1000],nargs='+',default=[100,1000])
    ap.add_argument('--per-probe-seconds',type=float,default=180)
    ap.add_argument('--max-total-seconds',type=float,default=900)
    ap.add_argument('--max-iterations',type=int,default=10000)
    ap.add_argument('--max-bits',type=int,default=16384)
    ap.add_argument('--resume',type=Path)
    ap.add_argument('--smoke-test',action='store_true')
    args = ap.parse_args()
    if args.smoke_test:
        assert args.output is None and args.resume is None
        smoke_test()
        return
    assert args.output is not None, '--output must be a fresh checkpoint directory'
    assert 0 < args.max_total_seconds <= 900
    assert 0 < args.per_probe_seconds <= 900
    assert 1 <= args.max_iterations <= 10000
    assert 1024 <= args.max_bits <= 16384
    started = time.monotonic()
    deadline = started+args.max_total_seconds
    pointpath = args.point.resolve()
    assert pointpath.is_relative_to(RUN)
    point = json.loads(pointpath.read_text())
    assert point['uniformizer_precision'] == PRECISION, 'only the preauthorized pi56 precision is supported'
    assert point['coefficient_modulus'] == MODULUS
    assert point['ramification_degree'] == E
    assert len(point['theta_values']) == 270 and len(point['lambda_values']) == 291
    assert all(len(v) == E and all(isinstance(a,int) and 0 <= a < MODULUS for a in v)
               for v in point['theta_values'])
    out = args.output.resolve()
    assert out.is_relative_to(RUN)
    assert not out.exists(), 'preserve existing results; choose a new output directory'
    out.mkdir(parents=True)
    input_hashes = {str(pointpath.relative_to(RUN)):sha256(pointpath),
                    str(Path(__file__).resolve().relative_to(RUN)):sha256(Path(__file__))}
    probes = [(theta,degree) for theta in sorted(set(args.theta)) for degree in sorted(set(args.degree))]
    resume = None
    if args.resume:
        resumepath = args.resume.resolve()
        assert resumepath.is_relative_to(RUN)
        resume = json.loads(resumepath.read_text())
        assert resume['input_hashes'] == input_hashes
        probes = [(resume['theta_index_one_based'],resume['relative_degree_bound'])]
    assert len(probes) <= 4
    results = []
    for theta_index,degree in probes:
        # Reserve up to30 seconds for exact final checks and checkpoint output.
        if time.monotonic()+30 >= deadline:
            results.append({'theta_index_one_based':theta_index,'relative_degree_bound':degree,
                            'status':'NOT_RUN_global_time_gate'})
            continue
        theta = point['theta_values'][theta_index-1]
        original,values = make_lattice(theta,degree)
        meta = {'theta_index_one_based':theta_index,'relative_degree_bound':degree,
                'integer_lattice_dimension':E*(degree+1),
                'coefficient_order':'c[j,r] at position7*j+r; polynomial=sum c[j,r]*pi^r*T^j',
                'input_hashes':input_hashes,'uniformizer_precision':PRECISION,
                'coefficient_modulus':MODULUS,'theta_residue':theta,
                'monomial_residue_vectors':values,'initial_basis':original}
        counter = [0]

        def checkpoint(state):
            counter[0] += 1
            file = out/f'theta{theta_index}_d{degree}_checkpoint{counter[0]:05d}_iter{state["iterations"]:06d}.json'
            assert not file.exists()
            file.write_text(json.dumps(dict(meta,**state),separators=(',',':'))+'\n')
            print('CHECKPOINT',file.name,'reason',state['reason'],'k',state['next_k'],
                  'iterations',state['iterations'],'seconds',state['elapsed_seconds'],flush=True)

        result = lll(original,max_seconds=args.per_probe_seconds,
                     max_iterations=args.max_iterations,max_bits=args.max_bits,
                     checkpoint=checkpoint,resume=resume,global_deadline=deadline-30)
        # A capped LLL run can still yield a valid exact exclusion certificate.
        certification = summarize_basis(result,original,values,sorted(set(args.height)))
        assert certification['verified_lattice_index'] == certification['expected_lattice_index']
        final = dict(meta,**result,**certification)
        final['status'] = 'EXACT_MODULAR_LATTICE_ANALYSIS_global_algebraic_relations_NOT_verified'
        finalpath = out/f'theta{theta_index}_d{degree}_result.json'
        finalpath.write_text(json.dumps(final,indent=2)+'\n')
        results.append({'theta_index_one_based':theta_index,'relative_degree_bound':degree,
                        'LLL_status':result['reason'],'result_file':finalpath.name,
                        'candidate_count':len(certification['candidates']),
                        'GSO_exclusions':certification['GSO_exclusions']})
        print('PROBE_DONE',theta_index,degree,result['reason'],
              'candidate_count',len(certification['candidates']),flush=True)
    summary = {'status':'BOUNDED_EXTRACTION_PROBES_ONLY', 'input_hashes':input_hashes,
               'probes':results,'elapsed_seconds':round(time.monotonic()-started,3),
               'precision_increased':False,'CAS_used':False,
               'global_polynomial_identity_verified':False,
               'negative_result_scope':'only explicit GSO certificates exclude the stated coefficient-height boxes',
               'candidate_success_gate':'represent every generator coefficient over the proposed exact number field, verify all full Schur/FR identities, and verify the original Hensel selector'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('FINISHED_BOUNDED_RELATIVE_DEGREE_RECOGNITION',out/'summary.json',flush=True)


if __name__ == '__main__': main()
