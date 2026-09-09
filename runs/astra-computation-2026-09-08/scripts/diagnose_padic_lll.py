#!/usr/bin/env python3
"""Read-only checkpoint audit, optionally ONE authorized <=60s cubic resume.

The original recognition script and its hash are left unchanged. Default
mode only checks three saved bases, exact LLL potential decrease and a
25-step replay. --resume-iterations 10000 additionally resumes one cubic
probe, checking incremental GSO against a fresh computation every100
iterations. No added pi precision or new coordinate/degree probe is allowed.
All work uses exact integers/Fractions and the original library routines.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import recognize_padic_relative_degree as lib

RUN = Path(__file__).resolve().parents[1]


def potential(norms):
    prefix = Q(1)
    answer = 1
    for a in norms:
        prefix *= a
        assert prefix.denominator == 1, 'Gram prefix determinant is not integral'
        answer *= prefix.numerator
    return answer


def potential_record(value):
    # Hex avoids Python's decimal-string digit limit for this large integer.
    return {'integer_hex':hex(value), 'bit_length':value.bit_length()}


def describe(checkpoint):
    basis = checkpoint['basis']
    detu = lib.verify_transform(basis,checkpoint['unimodular_transform'],checkpoint['initial_basis'])
    mu,norms,size,lovasz = lib.lll_check(basis,Q(3,4))
    phi = potential(norms)
    return {'iterations':checkpoint['iterations'],'swaps':checkpoint['swaps'],
            'next_k':checkpoint['next_k'], 'transform_determinant':detu,
            'maximum_basis_integer_bits':max(abs(a).bit_length() for row in basis for a in row),
            'maximum_transform_integer_bits':max(abs(a).bit_length() for row in checkpoint['unimodular_transform'] for a in row),
            'minimum_squared_GSO_norm':lib.fraction_data(min(norms)),
            'unit_GSO_indices':[i for i,a in enumerate(norms) if a == 1],
            'size_reduced':size, 'Lovasz':lovasz,
            'failed_size_pairs':[[i,j] for i in range(len(basis)) for j in range(i)
                                  if abs(mu[i][j]) > Q(1,2)],
            'failed_Lovasz_indices':[i for i in range(1,len(basis))
                                     if norms[i] < (Q(3,4)-mu[i][i-1]**2)*norms[i-1]],
            'potential':potential_record(phi)}, phi


def drop_check(oldphi,newphi,swaps):
    assert swaps >= 0
    if swaps:
        valid = newphi*4**swaps < oldphi*3**swaps
    else:
        valid = newphi == oldphi
    assert valid, 'fresh exact LLL potential violates recorded swap progress'
    return {'swaps':swaps,'verified':True,
            'comparison':'Phi_new*4^swaps < Phi_old*3^swaps' if swaps else 'Phi_new=Phi_old'}


def audited_resume(checkpoint, output, max_iterations, max_seconds):
    original = checkpoint['initial_basis']
    basis = [row[:] for row in checkpoint['basis']]
    transform = [row[:] for row in checkpoint['unimodular_transform']]
    k = checkpoint['next_k']
    iterations = initial_iterations = checkpoint['iterations']
    swaps = checkpoint['swaps']
    reductions = checkpoint['size_reductions']
    mu,norms = lib.gram_schmidt(basis)
    oldphi = potential(norms)
    oldswaps = swaps
    started = time.monotonic()
    audits = []
    reason = 'iteration_limit'
    n = len(basis)

    def state(reason):
        return {'reason':reason,'basis':basis,'unimodular_transform':transform,
                'initial_basis':original,'next_k':k,'iterations':iterations,
                'swaps':swaps,'size_reductions':reductions,
                'theta_index_one_based':checkpoint['theta_index_one_based'],
                'relative_degree_bound':3,'uniformizer_precision':56,
                'input_hashes':checkpoint['input_hashes'],
                'elapsed_seconds':round(time.monotonic()-started,3)}

    def audit(reason):
        nonlocal oldphi,oldswaps
        freshmu,freshnorms = lib.gram_schmidt(basis)
        if freshmu != mu or freshnorms != norms:
            failure = state('FAILED_incremental_GSO_drift')
            failure['fresh_squared_norms'] = [lib.fraction_data(a) for a in freshnorms]
            failure['incremental_squared_norms'] = [lib.fraction_data(a) for a in norms]
            failure['first_mu_mismatches'] = [
                {'index':[i,j], 'fresh':lib.fraction_data(freshmu[i][j]),
                 'incremental':lib.fraction_data(mu[i][j])}
                for i in range(n) for j in range(i) if freshmu[i][j] != mu[i][j]][:8]
            (output/f'FAILED_GSO_iter{iterations:06d}.json').write_text(json.dumps(failure,indent=2)+'\n')
            raise AssertionError('FAILED incremental GSO drift; exact state preserved')
        phi = potential(freshnorms)
        drop = drop_check(oldphi,phi,swaps-oldswaps)
        entry = {'iterations':iterations,'next_k':k,'incremental_equals_fresh':True,
                 'potential':potential_record(phi),'drop_since_previous_audit':drop}
        audits.append(entry)
        oldphi,oldswaps = phi,swaps
        path = output/f'audited_resume_iter{iterations:06d}_{reason}.json'
        assert not path.exists()
        path.write_text(json.dumps(dict(state(reason),audit=entry),separators=(',',':'))+'\n')
        print('PASS_FRESH_GSO',iterations,'k',k,'seconds',round(time.monotonic()-started,3),flush=True)

    while k < n and iterations-initial_iterations < max_iterations:
        # Reserve five seconds for terminal verification and output.
        if time.monotonic()-started >= max_seconds-5:
            reason = 'time_limit'
            break
        if max(abs(a).bit_length() for row in basis+transform for a in row) > 16384:
            reason = 'integer_bit_limit'
            break
        iterations += 1
        for j in range(k-1,-1,-1):
            r = lib.nearest(mu[k][j])
            if r:
                basis[k] = [a-r*b for a,b in zip(basis[k],basis[j])]
                transform[k] = [a-r*b for a,b in zip(transform[k],transform[j])]
                for s in range(j): mu[k][s] -= r*mu[j][s]
                mu[k][j] -= r
                reductions += 1
        if norms[k] >= (Q(3,4)-mu[k][k-1]**2)*norms[k-1]:
            k += 1
        else:
            oldmu = mu[k][k-1]
            left,right = norms[k-1],norms[k]
            newleft = right+oldmu**2*left
            newmu = oldmu*left/newleft
            norms[k-1],norms[k] = newleft,left*right/newleft
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
        if (iterations-initial_iterations) % 100 == 0: audit('progress')
    if k == n: reason = 'LLL_completed'
    audit(reason)
    result = state(reason)
    values = checkpoint['monomial_residue_vectors']
    certificate = lib.summarize_basis(result,original,values,[100,1000])
    result.update(certificate)
    result['every100_steps_incremental_GSO_checked'] = True
    result['audits'] = audits
    (output/'audited_resume_result.json').write_text(json.dumps(result,indent=2)+'\n')
    return {'status':reason,'iterations_added':iterations-initial_iterations,
            'candidate_count':len(certificate['candidates']),
            'GSO_exclusions':certificate['GSO_exclusions'],
            'elapsed_seconds':round(time.monotonic()-started,3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=RUN/'data/padic_relative_degree_pi56')
    ap.add_argument('--theta',type=int,choices=[1,2],default=1)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--resume-iterations',type=int,choices=[0,10000],default=0)
    ap.add_argument('--max-seconds',type=float,default=60)
    args = ap.parse_args()
    assert 5 < args.max_seconds <= 60
    source,out = args.source.resolve(),args.output.resolve()
    assert source.is_relative_to(RUN) and out.is_relative_to(RUN)
    assert not out.exists(), 'preserve old outputs'
    out.mkdir(parents=True)
    prefix = f'theta{args.theta}_d3'
    files = [source/f'{prefix}_checkpoint00001_iter000025.json',
             source/f'{prefix}_checkpoint00200_iter005000.json',
             source/f'{prefix}_result.json']
    checkpoints = [json.loads(path.read_text()) for path in files]
    final = checkpoints[-1]
    oldhash = final['input_hashes']['scripts/recognize_padic_relative_degree.py']
    assert lib.sha256(Path(lib.__file__)) == oldhash, 'original recognition source changed'
    assert final['relative_degree_bound'] == 3 and final['uniformizer_precision'] == 56
    descriptions = []
    oldphi = potential(lib.gram_schmidt(final['initial_basis'])[1])
    oldswaps = 0
    for file,checkpoint in zip(files,checkpoints):
        record,phi = describe(checkpoint)
        record['source_file'] = str(file.relative_to(RUN))
        record['progress_certificate'] = drop_check(oldphi,phi,checkpoint['swaps']-oldswaps)
        descriptions.append(record)
        oldphi,oldswaps = phi,checkpoint['swaps']
    replayfile = source/f'{prefix}_checkpoint00399_iter009975.json'
    replaystart = json.loads(replayfile.read_text())
    replay = lib.lll(final['initial_basis'],resume=replaystart,max_iterations=25,max_seconds=5)
    replay_keys = ['basis','unimodular_transform','next_k','iterations','swaps','size_reductions']
    assert all(replay[key] == final[key] for key in replay_keys), 'fresh-GSO last25-step replay disagrees'
    summary = {'status':'PASS_EXACT_CHECKPOINT_PROGRESS_AND_LAST25_REPLAY',
               'theta_index_one_based':args.theta,'relative_degree_bound':3,
               'checkpoint_descriptions':descriptions,'fresh_GSO_last25_replay_equal':True,
               'original_source_hash':oldhash,
               'diagnostic_source_hash':lib.sha256(Path(__file__)),
               'actual_point_precision_increased':False,'new_probes_started':False}
    (out/'checkpoint_diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('PASS_CHECKPOINT_AUDIT',args.theta,'fresh_GSO_last25_matches',flush=True)
    if args.resume_iterations:
        summary['audited_resume'] = audited_resume(final,out,args.resume_iterations,args.max_seconds)
    else:
        summary['audited_resume'] = 'NOT_RUN'
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'status':summary['status'],'audited_resume':summary['audited_resume']}),flush=True)


if __name__ == '__main__': main()
