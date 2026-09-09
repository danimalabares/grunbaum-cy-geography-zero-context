#!/usr/bin/env python3
"""Reduce an implicit quadratic system by acyclic rational circuits.

The graph search is heuristic; the final acyclic-order certificate is exact.
Self-dependence is linear, with denominator1 at the origin. No expanded
elimination or field-degree claim is made. The full map works for ANY of
the21 free paths, including the original selected ramified fibre.
"""
import argparse
import hashlib
import json
import random
import time
from fractions import Fraction as Q
from pathlib import Path

RUN=Path(__file__).resolve().parents[1]
REPO=RUN.parents[1]


def prune(edges,rev,live):
    todo=[i for i in live if not edges[i] or not rev[i]]
    while todo:
        i=todo.pop()
        if i not in live:continue
        live.remove(i)
        for j in edges[i]:
            rev[j].remove(i)
            if not rev[j]:todo.append(j)
        for j in rev[i]:
            edges[j].remove(i)
            if not edges[j]:todo.append(j)
        edges[i].clear();rev[i].clear()


def elimination_order(graph,core):
    todo=set(range(len(graph)))-set(core)
    order=[];known=set(core)
    while todo:
        ready=sorted(i for i in todo if graph[i]<=known)
        assert ready,'feedback set did not remove every directed cycle'
        order.extend(ready);known.update(ready);todo.difference_update(ready)
    return order


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,default=RUN/'data/sparse_support_QQ/support_closure.json')
    ap.add_argument('--seconds',type=int,default=90)
    ap.add_argument('--trials',type=int,default=12)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();start=time.monotonic()
    out=a.output.resolve();assert out.is_relative_to(RUN) and not out.exists()
    data=json.loads(a.input.read_text());assert data['field']=='Q'
    h=data['quadratic_map'];n=len(h);assert n==781
    graph=[];denominators=set()
    for i,row in enumerate(h):
        dependencies=set()
        for m,c in row:
            assert len(m)==2 and m[0]<291<=m[1]
            assert m.count(i)<=1,'nonlinear self term requires different elimination'
            dependencies.update(m);denominators.add(Q(c).denominator)
        dependencies.discard(i);graph.append(dependencies)
    assert all(d%101 for d in denominators)
    best=None;attempts=[]
    for trial in range(a.trials):
        if time.monotonic()-start>a.seconds:break
        edges=[set(e) for e in graph];rev=[set() for _ in graph]
        for i,row in enumerate(edges):
            for j in row:rev[j].add(i)
        live=set(range(n));core=[];rng=random.Random(1788910000+trial)
        noise={i:rng.random() for i in live}
        def score(i):
            indeg,outdeg=len(rev[i]),len(edges[i])
            if trial%4==0:v=indeg*outdeg
            elif trial%4==1:v=indeg*outdeg/(indeg+outdeg)
            elif trial%4==2:v=indeg
            else:v=indeg+outdeg
            return v*(1+(0 if trial<4 else .15*noise[i]))
        while live:
            prune(edges,rev,live)
            if not live:break
            i=max(live,key=lambda i:(score(i),-i));core.append(i)
            # Removing a feedback coordinate replaces it by an independent
            # input; all remaining equations may depend on that input.
            for j in edges[i]:rev[j].remove(i)
            for j in rev[i]:edges[j].remove(i)
            edges[i].clear();rev[i].clear();live.remove(i)
        # Remove redundant chosen vertices, checking the DAG exactly.
        for i in list(reversed(core)):
            try:elimination_order(graph,[j for j in core if j!=i])
            except AssertionError:continue
            core.remove(i)
        order=elimination_order(graph,core)
        attempts.append({'trial':trial,'core_count':len(core),'seconds':time.monotonic()-start})
        if best is None or len(core)<len(best):
            best=sorted(core)
            print('IMPROVED_CORE',len(best),'TRIAL',trial,'SECONDS',time.monotonic()-start,flush=True)
    assert best is not None
    order=elimination_order(graph,best)
    circuits=[]
    for i in order:
        self_terms=[];other_terms=[]
        for m,c in h[i]:
            if i in m:self_terms.append([m[1] if m[0]==i else m[0],c])
            else:other_terms.append([m,c])
        circuits.append({'variable':i,'forcing_coordinate':i,'numerator_quadratic_terms':other_terms,
                         'denominator_one_minus_linear_terms':self_terms})
    result={'status':'COMPUTER-CERTIFIED exact acyclic rational circuit reduction; field extraction OPEN',
            'scope':'full selected coefficient subsystem, for arbitrary21 prescribed free paths',
            'full_state_variables':781,'core_variables':best,'core_count':len(best),
            'core_variable_names':[data['variables'][i] for i in best],
            'eliminated_count':len(order),'elimination_order':order,'rational_circuits':circuits,
            'core_equations':'v_i - ell_i(q) - H_i(v(core,q)) = 0 for each retained core index i',
            'forcing_requirement':'ell_z,free=w; selectedD(ell_z)=0; ell_U=B(ell_z). For actual fibre use original21 free polynomials atpi.',
            'inverse_map':'retain the listed core coordinates of the original tuple; all other state coordinates reconstruct in elimination_order',
            'origin_units':'Every denominator is1 minus a linear combination of reconstructed state coordinates; at the chosen ramified root all state coordinates are inpiO.',
            'proof':'Acyclic order ensures each eliminated equation is linear only in its own variable and has no future dependence. Solve it by the saved circuit. Substitution preserves precisely the localized origin branch; all maps are mutual inverses there.',
            'not_claimed':'manageable exact coefficient field, primitive element, global degree, or all remote solutions',
            'rational_denominators':sorted(denominators),'attempts':attempts,
            'input_hashes':{str(f.resolve().relative_to(REPO)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [a.input,Path(__file__)]},
            'seconds':time.monotonic()-start}
    out.mkdir(parents=True)
    (out/'feedback_reduction.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('FINAL_CORE',len(best),'ELIMINATED',len(order),'SECONDS',result['seconds'],flush=True)


if __name__=='__main__':main()
