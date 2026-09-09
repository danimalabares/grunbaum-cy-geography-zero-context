#!/usr/bin/env python3
"""Exact capped Fincke--Pohst enumeration for ONE completed cubic lattice.

Target only theta1, relative degree<=3, existing pi56 precision, coefficient
height<=1000. No CAS, installs, new point/precision or extra LLL parameters.
Actual-point enumeration requires root approval and the sole process slot.

Enumerate the Euclidean sphere ||v||^2<=28*1000^2 in the full integer
coefficient lattice. Every vector in the height box lies in this sphere.
Gram--Schmidt centers and interval endpoints are exact Fractions/integers.
The explicit DFS stack is checkpointed. At most100000 candidate assignments
and900 internal seconds are permitted in total, including resumed search.

An exhausted sphere gives an exact negative height-box certificate after
checking every nonzero vector found. A stopped search is INCONCLUSIVE.
A vector in the box is only a modular relation, hence HEURISTIC as a global
equation until the complete field representation and Hilbert identities
are verified with the original Hensel selector.
"""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from math import isqrt
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import recognize_padic_relative_degree as lib

RUN = Path(__file__).resolve().parents[1]
HEIGHT = 1000
DIMENSION = 28
RADIUS_SQUARED = DIMENSION*HEIGHT**2


def encode_fraction(a):
    return [str(a.numerator),str(a.denominator)]


def decode_fraction(a):
    return Q(int(a[0]),int(a[1]))


def interval(center, squared_bound):
    """All integers a with (a+center)^2 <= squared_bound, exactly."""
    assert squared_bound >= 0
    c,d = center.numerator,center.denominator
    numerator = squared_bound.numerator*d*d
    denominator = squared_bound.denominator
    width = isqrt(numerator//denominator)
    lower = -((width+c)//d)  # ceil((-width-c)/d)
    upper = (width-c)//d
    return lower,upper


def serialize_stack(stack):
    return [dict(frame,center=encode_fraction(frame['center']),
                 remaining=encode_fraction(frame['remaining'])) for frame in stack]


def deserialize_stack(stack):
    return [dict(frame,center=decode_fraction(frame['center']),
                 remaining=decode_fraction(frame['remaining'])) for frame in stack]


def enumerate_sphere(basis, mu, norms, radius_squared, *, max_nodes=100000,
                     max_seconds=900, resume=None, checkpoint=None, on_vector=None):
    n = len(basis)
    start = time.monotonic()
    prior_seconds = resume.get('search_elapsed_seconds',0) if resume else 0
    coefficients = resume['basis_coefficients'][:] if resume else [0]*n
    nodes = resume['nodes'] if resume else 0
    leaves = resume['leaves'] if resume else 0
    nonzero = resume['nonzero_vectors'] if resume else 0

    def frame(k,remaining):
        center = sum((coefficients[i]*mu[i][k] for i in range(k+1,n)),Q(0))
        lower,upper = interval(center,remaining/norms[k])
        return {'k':k,'center':center,'remaining':remaining,
                'lower':lower,'upper':upper,'next_integer':lower}

    stack = deserialize_stack(resume['DFS_stack']) if resume else [frame(n-1,Q(radius_squared))]

    def state(reason):
        return {'search_reason':reason,'basis_coefficients':coefficients[:],
                'DFS_stack':serialize_stack(stack),'nodes':nodes,'leaves':leaves,
                'nonzero_vectors':nonzero,
                'search_elapsed_seconds':round(prior_seconds+time.monotonic()-start,6)}

    # On resume, certify that every stored frame is exactly the frame implied
    # by its already assigned higher coefficients. A checkpoint is not a new
    # mathematical input trusted without its interval/precision checks.
    for stored in stack:
        k = stored['k']
        used = sum((norms[j]*(coefficients[j]+sum(
                    (coefficients[i]*mu[i][j] for i in range(j+1,n)),Q(0)))**2
                    for j in range(k+1,n)),Q(0))
        expected = frame(k,Q(radius_squared)-used)
        for key in ['k','center','remaining','lower','upper']: assert stored[key] == expected[key]
        assert stored['lower'] <= stored['next_integer'] <= stored['upper']+1
    assert all(stack[i]['k'] == n-1-i for i in range(len(stack)))
    last_checkpoint = time.monotonic()
    reason = 'EXHAUSTED_full_sphere'
    while stack:
        if nodes >= max_nodes:
            reason = 'CAPPED_node_limit'
            break
        if prior_seconds+time.monotonic()-start >= max_seconds:
            reason = 'CAPPED_time_limit'
            break
        current = stack[-1]
        k = current['k']
        if current['next_integer'] > current['upper']:
            stack.pop()
            coefficients[k] = 0
            continue
        a = current['next_integer']
        current['next_integer'] += 1
        coefficients[k] = a
        nodes += 1
        term = norms[k]*(a+current['center'])**2
        assert 0 <= term <= current['remaining']
        remaining = current['remaining']-term
        if k:
            stack.append(frame(k-1,remaining))
        else:
            leaves += 1
            if any(coefficients):
                nonzero += 1
                vector = [sum(coefficients[i]*basis[i][j] for i in range(n)) for j in range(n)]
                norm_squared = sum(a*a for a in vector)
                assert norm_squared == Q(radius_squared)-remaining
                assert 0 < norm_squared <= radius_squared
                if on_vector and on_vector(coefficients[:],vector,norm_squared):
                    reason = 'FOUND_modular_height_box_candidate'
                    break
        if checkpoint and (nodes % 1000 == 0 or time.monotonic()-last_checkpoint >= 10):
            checkpoint(state('progress'))
            last_checkpoint = time.monotonic()
    result = state(reason)
    if checkpoint: checkpoint(result)
    return result


def brute_vectors(basis,radius_squared,bound):
    n = len(basis)
    result = set()
    for coefficients in product(range(-bound,bound+1),repeat=n):
        vector = tuple(sum(coefficients[i]*basis[i][j] for i in range(n)) for j in range(n))
        if 0 < sum(a*a for a in vector) <= radius_squared: result.add(vector)
    return result


def smoke():
    # Bounds are proved from the inverse bases: for the first two matrices,
    # radius sqrt20 gives |a_i|<4; the triangular3x3 example at radius sqrt5
    # gives |a_i|<=sqrt15<4. Thus [-4,4]^n is exhaustive, not sampling.
    cases = [([[2,1],[1,2]],20,4),([[3,0],[1,2]],20,4),
             ([[1,1,0],[0,1,1],[0,0,1]],5,4)]
    reports = []
    for basis,radius,bound in cases:
        mu,norms = lib.gram_schmidt(basis)
        visited = []
        state = enumerate_sphere(basis,mu,norms,radius,max_nodes=100000,max_seconds=5,
                  on_vector=lambda a,v,n: visited.append(tuple(v)) and False)
        assert state['search_reason'] == 'EXHAUSTED_full_sphere'
        brute = brute_vectors(basis,radius,bound)
        assert len(set(visited)) == len(visited), 'duplicate lattice vector'
        assert set(visited) == brute
        # Also check explicit-stack continuation across a very small node cap.
        first = enumerate_sphere(basis,mu,norms,radius,max_nodes=3,max_seconds=5)
        resumed = []
        second = enumerate_sphere(basis,mu,norms,radius,max_nodes=100000,max_seconds=5,
                  resume=first,on_vector=lambda a,v,n: resumed.append(tuple(v)) and False)
        complete_prefix = []
        enumerate_sphere(basis,mu,norms,radius,max_nodes=3,max_seconds=5,
                         on_vector=lambda a,v,n: complete_prefix.append(tuple(v)) and False)
        assert second['search_reason'] == 'EXHAUSTED_full_sphere'
        assert set(complete_prefix+resumed) == brute
        reports.append({'dimension':len(basis),'radius_squared':radius,
                        'nodes':state['nodes'],'nonzero_vector_count':len(brute),
                        'brute_force_coefficient_bound':bound,'resume_matches':True})
    print(json.dumps({'status':'PASS_EXACT_TINY_SPHERE_ENUMERATION','cases':reports},indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--basis',type=Path,default=RUN/'data/lll_theta1_cubic_audited_resume/audited_resume_result.json')
    ap.add_argument('--original-probe',type=Path,default=RUN/'data/padic_relative_degree_pi56/theta1_d3_result.json')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--resume',type=Path)
    ap.add_argument('--max-nodes',type=int,default=100000)
    ap.add_argument('--max-seconds',type=float,default=900)
    ap.add_argument('--smoke-test',action='store_true')
    args = ap.parse_args()
    if args.smoke_test:
        assert args.output is None and args.resume is None
        smoke()
        return
    assert args.output is not None
    assert 1 <= args.max_nodes <= 100000 and 1 <= args.max_seconds <= 900
    started = time.monotonic()
    basispath,probepath = args.basis.resolve(),args.original_probe.resolve()
    out = args.output.resolve()
    assert all(path.is_relative_to(RUN) for path in [basispath,probepath,out])
    assert not out.exists(), 'preserve all previous checkpoints'
    source = json.loads(basispath.read_text())
    original = json.loads(probepath.read_text())
    assert source['theta_index_one_based'] == original['theta_index_one_based'] == 1
    assert source['relative_degree_bound'] == original['relative_degree_bound'] == 3
    assert source['uniformizer_precision'] == original['uniformizer_precision'] == 56
    assert source['reason'] == 'LLL_completed'
    assert source['input_hashes'] == original['input_hashes']
    basis = source['basis']
    assert len(basis) == DIMENSION
    lib.verify_transform(basis,source['unimodular_transform'],source['initial_basis'])
    assert source['initial_basis'] == original['initial_basis']
    values = original['monomial_residue_vectors']
    assert all(not any(lib.relation_residue(row,values)) for row in basis)
    assert abs(lib.determinant(basis)) == lib.MODULUS**lib.E
    mu,norms = lib.gram_schmidt(basis)
    input_hashes = {str(path.relative_to(RUN)):lib.sha256(path)
                    for path in [basispath,probepath,Path(__file__).resolve(),Path(lib.__file__).resolve()]}
    resume = None
    if args.resume:
        resumepath = args.resume.resolve()
        assert resumepath.is_relative_to(RUN)
        resume = json.loads(resumepath.read_text())
        assert resume['input_hashes'] == input_hashes
        assert resume['height_bound'] == HEIGHT and resume['radius_squared'] == RADIUS_SQUARED
        assert resume['search_reason'] != 'FOUND_modular_height_box_candidate'
    out.mkdir(parents=True)
    metadata = {'input_hashes':input_hashes,'theta_index_one_based':1,
                'relative_degree_bound':3,'uniformizer_precision':56,
                'height_bound':HEIGHT,'radius_squared':RADIUS_SQUARED,
                'lattice_dimension':DIMENSION,'basis':basis,
                'unimodular_transform':source['unimodular_transform'],
                'gram_schmidt_squared_norms':[encode_fraction(a) for a in norms],
                'gram_schmidt_mu':[[encode_fraction(a) for a in row] for row in mu]}
    observed = resume.get('observed_vectors',[]) if resume else []
    candidates = resume.get('candidates',[]) if resume else []
    outside_box = resume.get('outside_box_vectors',0) if resume else 0
    checkpoints = [0]

    def found(coefficients,vector,norm_squared):
        nonlocal outside_box
        assert not any(lib.relation_residue(vector,values))
        height = max(map(abs,vector))
        record = {'basis_coefficients':coefficients,'integer_polynomial_coefficients':vector,
                  'squared_norm':norm_squared,'coefficient_height':height}
        if len(observed) < 12: observed.append(record)
        if height <= HEIGHT:
            record['status'] = 'HEURISTIC_modular_relation_NOT_verified_global_equation'
            record['coefficients_by_T_degree'] = [vector[j:j+7] for j in range(0,DIMENSION,7)]
            candidates.append(record)
            return True
        outside_box += 1
        return False

    def checkpoint(state):
        checkpoints[0] += 1
        record = dict(metadata,**state,observed_vectors=observed,
                      candidates=candidates,outside_box_vectors=outside_box)
        path = out/f'checkpoint{checkpoints[0]:05d}_nodes{state["nodes"]:06d}.json'
        assert not path.exists()
        path.write_text(json.dumps(record,separators=(',',':'))+'\n')
        print('SPHERE_CHECKPOINT',state['search_reason'],'nodes',state['nodes'],
              'depth',len(state['DFS_stack']),'seconds',state['search_elapsed_seconds'],flush=True)

    # Reserve15 seconds of the process budget for input checks and final output.
    search_budget = max(0.01,args.max_seconds-15-(time.monotonic()-started))
    result = enumerate_sphere(basis,mu,norms,RADIUS_SQUARED,max_nodes=args.max_nodes,
               max_seconds=search_budget,resume=resume,checkpoint=checkpoint,on_vector=found)
    if result['search_reason'] == 'EXHAUSTED_full_sphere':
        assert not candidates
        status = ('COMPUTER_CERTIFIED_no_nonzero_lattice_vector_in_full_radius'
                  if result['nonzero_vectors'] == 0 else
                  'COMPUTER_CERTIFIED_no_modular_relation_in_height_box_after_full_sphere_check')
    elif candidates:
        status = 'HEURISTIC_modular_polynomial_candidate_found'
    else:
        status = 'OPEN_enumeration_capped_no_exclusion_certificate'
    summary = dict(metadata,**result,status=status,observed_vectors=observed,
                   candidates=candidates,outside_box_vectors=outside_box,
                   exact_global_polynomial_verified=False,
                   scope='only theta1, relative degree<=3, integer pi-power-basis coefficient height<=1000',
                   elapsed_process_seconds=round(time.monotonic()-started,6))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(status,'nodes',result['nodes'],'nonzero_vectors',result['nonzero_vectors'],flush=True)


if __name__ == '__main__': main()
