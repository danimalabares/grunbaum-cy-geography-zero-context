#!/usr/bin/env python3
"""Separately authorized theta2 wrapper around the unchanged exact enumerator.

Only the completed theta2 cubic lattice and existing pi56 point are used.
At most100000 DFS assignments and120 internal seconds; use an outer guard
of at most300 seconds and2800MiB. No source from the theta1 job is changed.
The original exact enumerate_sphere routine supplies the search and stack.
"""
import argparse
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import enumerate_padic_height_box as engine
import recognize_padic_relative_degree as lib

RUN = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    ap.add_argument('--resume',type=Path)
    ap.add_argument('--max-nodes',type=int,default=100000)
    ap.add_argument('--max-seconds',type=float,default=120)
    ap.add_argument('--smoke-test',action='store_true')
    args = ap.parse_args()
    if args.smoke_test:
        assert args.output is None and args.resume is None
        engine.smoke()
        print('PASS_THETA2_WRAPPER_USING_UNCHANGED_GENERIC_ENGINE')
        return
    assert args.output is not None
    assert 1 <= args.max_nodes <= 100000 and 1 <= args.max_seconds <= 120
    started = time.monotonic()
    basispath = RUN/'data/lll_theta2_cubic_audited_resume/audited_resume_result.json'
    probepath = RUN/'data/padic_relative_degree_pi56/theta2_d3_result.json'
    pointpath = RUN/'data/ramified_hensel_pi56.json'
    source = json.loads(basispath.read_text())
    original = json.loads(probepath.read_text())
    point = json.loads(pointpath.read_text())
    assert source['theta_index_one_based'] == original['theta_index_one_based'] == 2
    assert source['relative_degree_bound'] == original['relative_degree_bound'] == 3
    assert source['uniformizer_precision'] == original['uniformizer_precision'] == 56
    assert source['reason'] == 'LLL_completed'
    assert source['input_hashes'] == original['input_hashes']
    assert source['initial_basis'] == original['initial_basis']
    assert point['uniformizer_precision'] == 56 and point['coefficient_modulus'] == lib.MODULUS
    assert point['ramification_degree'] == 7
    assert lib.sha256(pointpath) == original['input_hashes']['data/ramified_hensel_pi56.json']
    assert lib.sha256(Path(lib.__file__)) == original['input_hashes']['scripts/recognize_padic_relative_degree.py']
    # Reconstruct the original kernel lattice directly from theta2, not only
    # from a stored matrix. This independently checks coordinate selection.
    rebuilt,values = lib.make_lattice(point['theta_values'][1],3)
    assert rebuilt == original['initial_basis']
    assert values == original['monomial_residue_vectors']
    basis = source['basis']
    assert len(basis) == 28
    lib.verify_transform(basis,source['unimodular_transform'],rebuilt)
    assert all(not any(lib.relation_residue(row,values)) for row in basis)
    assert abs(lib.determinant(basis)) == lib.MODULUS**7
    mu,norms = lib.gram_schmidt(basis)
    input_hashes = {str(path.resolve().relative_to(RUN)):lib.sha256(path)
                    for path in [basispath,probepath,pointpath,Path(__file__),
                                 Path(engine.__file__),Path(lib.__file__)]}
    out = args.output.resolve()
    assert out.is_relative_to(RUN) and not out.exists()
    resume = None
    if args.resume:
        path = args.resume.resolve()
        assert path.is_relative_to(RUN)
        resume = json.loads(path.read_text())
        assert resume['input_hashes'] == input_hashes
        assert resume['theta_index_one_based'] == 2
        assert resume['height_bound'] == 1000 and resume['radius_squared'] == 28000000
        assert resume['search_reason'] != 'FOUND_modular_height_box_candidate'
    out.mkdir(parents=True)
    metadata = {'input_hashes':input_hashes,'theta_index_one_based':2,
                'relative_degree_bound':3,'uniformizer_precision':56,
                'height_bound':1000,'radius_squared':28000000,'lattice_dimension':28,
                'basis':basis,'unimodular_transform':source['unimodular_transform'],
                'initial_basis':rebuilt,'all_basis_rows_verified_in_kernel':True,
                'verified_lattice_index':str(lib.MODULUS**7),
                'gram_schmidt_squared_norms':[engine.encode_fraction(a) for a in norms],
                'gram_schmidt_mu':[[engine.encode_fraction(a) for a in row] for row in mu]}
    observed = resume.get('observed_vectors',[]) if resume else []
    candidates = resume.get('candidates',[]) if resume else []
    outside = [resume.get('outside_box_vectors',0) if resume else 0]
    serial = [0]

    def found(coefficients,vector,norm_squared):
        assert not any(lib.relation_residue(vector,values))
        height = max(map(abs,vector))
        record = {'basis_coefficients':coefficients,'integer_polynomial_coefficients':vector,
                  'squared_norm':norm_squared,'coefficient_height':height}
        if len(observed) < 12: observed.append(record)
        if height <= 1000:
            record['status'] = 'HEURISTIC_modular_relation_NOT_verified_global_equation'
            record['coefficients_by_T_degree'] = [vector[j:j+7] for j in range(0,28,7)]
            candidates.append(record)
            return True
        outside[0] += 1
        return False

    def checkpoint(state):
        serial[0] += 1
        path = out/f'checkpoint{serial[0]:05d}_nodes{state["nodes"]:06d}.json'
        assert not path.exists()
        path.write_text(json.dumps(dict(metadata,**state,observed_vectors=observed,
                           candidates=candidates,outside_box_vectors=outside[0]),separators=(',',':'))+'\n')
        print('THETA2_SPHERE_CHECKPOINT',state['search_reason'],'nodes',state['nodes'],
              'depth',len(state['DFS_stack']),'seconds',state['search_elapsed_seconds'],flush=True)

    budget = max(0.01,args.max_seconds-10-(time.monotonic()-started))
    result = engine.enumerate_sphere(basis,mu,norms,28000000,max_nodes=args.max_nodes,
                  max_seconds=budget,resume=resume,checkpoint=checkpoint,on_vector=found)
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
                  candidates=candidates,outside_box_vectors=outside[0],
                  exact_global_polynomial_verified=False,
                  scope='theta2 only, relative degree<=3, integral pi-basis coefficient height<=1000',
                  elapsed_process_seconds=round(time.monotonic()-started,6))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(status,'nodes',result['nodes'],'nonzero_vectors',result['nonzero_vectors'],flush=True)


if __name__ == '__main__': main()
