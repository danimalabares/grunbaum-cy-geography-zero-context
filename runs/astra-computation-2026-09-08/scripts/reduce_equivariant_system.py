#!/usr/bin/env python3
"""Build and safely peel the small S3-block algebraic curve, with no CAS.

All arithmetic is exact modulo a prime. Eliminations divide only by
polynomials nonzero at the marked origin; every substitution is retained.
No Groebner basis is launched. The final Singular file is an INPUT ONLY.
Use --path sixjet to retain the existing smoothness certificate. --path
linear changes the curve inside the same fixed germ and needs a fresh
smoothness certificate for any resulting finite fibre.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
RUN=Path(__file__).resolve().parents[1]
DAY=RUN.parent/'astra-daytime-2026-09-08'
sys.path.insert(0,str(DAY/'scripts'))
from fixed_curve_lift import normalized_jet


class Growth(Exception): pass


def add(a,b,p,scale=1,cap=1000000):
    out=dict(a)
    for m,c in b.items():
        out[m]=(out.get(m,0)+scale*c)%p
        if not out[m]: del out[m]
    if len(out)>cap: raise Growth('polynomial term cap')
    return out


def mul(a,b,p,cap):
    if len(a)*len(b)>30*cap: raise Growth('product expansion gate')
    out={}
    for m,c in a.items():
        for n,d in b.items():
            k=tuple(sorted(m+n)); out[k]=(out.get(k,0)+c*d)%p
            if not out[k]: del out[k]
        if len(out)>cap: raise Growth('product term cap')
    return out


def canonical(a,p):
    if not a: return a
    inv=pow(a[min(a)],-1,p)
    return {m:c*inv%p for m,c in a.items()}


def unique(equations,p):
    seen=set(); out=[]
    for e in equations:
        if not e: continue
        e=canonical(e,p); key=tuple(sorted(e.items()))
        if key not in seen: seen.add(key); out.append(e)
    return out


def substitute(poly,x,num,den,p,cap):
    degree=max((m.count(x) for m in poly),default=0)
    if not degree: return poly
    np=[{():1}]; dp=[{():1}]
    for k in range(degree):
        np.append(mul(np[-1],num,p,cap)); dp.append(mul(dp[-1],den,p,cap))
    out={}
    for mon,c in poly.items():
        n=mon.count(x); tail=tuple(v for v in mon if v!=x)
        term=mul(np[n],dp[degree-n],p,cap)
        term={tuple(sorted(m+tail)):c*a%p for m,a in term.items()}
        out=add(out,term,p,cap=cap)
    return out


def encode(poly): return [[list(m),c] for m,c in sorted(poly.items())]


def split(poly,x,p):
    a={}; b={}
    for m,c in poly.items():
        degree=m.count(x)
        if degree>1: return None
        if degree: a[tuple(v for v in m if v!=x)]=c
        else: b[m]=c
    if not a.get((),0): return None
    num={m:(-c)%p for m,c in b.items()}
    if len(a)==1:
        inv=pow(a[()],-1,p); num={m:c*inv%p for m,c in num.items()}; a={():1}
    return num,a


def strongly_connected(graph):
    counter=0; stack=[]; onstack=set(); index={}; low={}; components=[]
    def visit(v):
        nonlocal counter
        index[v]=low[v]=counter; counter+=1; stack.append(v); onstack.add(v)
        for w in graph[v]:
            if w not in index: visit(w); low[v]=min(low[v],low[w])
            elif w in onstack: low[v]=min(low[v],index[w])
        if low[v]==index[v]:
            component=[]
            while True:
                w=stack.pop(); onstack.remove(w); component.append(w)
                if w==v: break
            components.append(sorted(component))
    for v in graph:
        if v not in index: visit(v)
    return components


def implicit_scc(equations,remaining,p,cap):
    """Exact constant-Jacobian normalization, then RHS dependency SCCs."""
    basis={}; remaining=set(remaining)
    for original in equations:
        row=dict(original)
        for pivot in sorted(basis):
            c=row.get((pivot,),0)
            if c: row=add(row,basis[pivot],p,-c,cap)
        pivots=[v for v in remaining if row.get((v,),0)]
        if pivots:
            pivot=min(pivots); inv=pow(row[(pivot,)],-1,p)
            basis[pivot]={m:c*inv%p for m,c in row.items()}
    assert len(basis)==len(remaining), ('remaining Jacobian rank',len(basis),len(remaining))
    for pivot in sorted(basis,reverse=True):
        for earlier in sorted(basis):
            if earlier>=pivot: break
            c=basis[earlier].get((pivot,),0)
            if c: basis[earlier]=add(basis[earlier],basis[pivot],p,-c,cap)
    graph={v:set() for v in remaining}
    for v,row in basis.items():
        for m,c in row.items():
            if m!=(v,): graph[v].update(w for w in m if w in remaining)
    return strongly_connected(graph), {str(v):sorted(w) for v,w in graph.items()}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prime',type=int,default=101)
    ap.add_argument('--path',choices=['sixjet','linear'],default='sixjet')
    ap.add_argument('--rational',action='store_true')
    ap.add_argument('--max-steps',type=int,default=760)
    ap.add_argument('--max-terms',type=int,default=5000)
    ap.add_argument('--max-total-terms',type=int,default=300000)
    ap.add_argument('--max-seconds',type=int,default=240)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args(); p=args.prime; started=time.monotonic()
    assert p>3 and all(p%d for d in range(2,int(p**.5)+1))
    blockpath=RUN/'data/equivariant_blocks_QQ.json'
    data=json.loads(blockpath.read_text())
    chart=json.loads((DAY/'data/fixed_chart.json').read_text())
    assert hashlib.sha256((DAY/'data/fixed_chart.json').read_bytes()).hexdigest()==data['source_chart_sha256']
    jet,_=normalized_jet(chart)
    modular=lambda a: a.numerator*pow(a.denominator,-1,p)%p
    dep=data['dependent_coordinates']; free=data['free_coordinates']
    names=['q']+[f'z{j+1}' for j in dep]
    z={j:{(i+1,):1} for i,j in enumerate(dep)}
    for j in free:
        z[j]={(0,)*n:modular(jet[n][j]) for n in range(1,7 if args.path=='sixjet' else 2) if modular(jet[n][j])}
    def linear(encoded):
        out={}
        for j,c in encoded: out=add(out,z[j],p,modular(Q(c)))
        return out
    equations=[]; u_map={}
    for kind,block in data['blocks'].items():
        ni,nk,nc=block['dimensions']
        u=[[None]*nk for _ in range(ni)]
        for i in range(ni):
            for j in range(nk):
                v=len(names); names.append(f'u_{kind}_{i}_{j}'); u[i][j]=v
                u_map[f'{kind},{i},{j}']=v
        A=[[linear(v) for v in row] for row in block['A_minus_identity']]
        B=[[linear(v) for v in row] for row in block['B']]
        C=[[linear(v) for v in row] for row in block['C']]
        D=[[linear(v) for v in row] for row in block['D']]
        for i in range(ni):
            for j in range(nk):
                e=add({(u[i][j],):1},B[i][j],p,-1)
                for k in range(ni):
                    e=add(e,{tuple(sorted(m+(u[k][j],))):c for m,c in A[i][k].items()},p)
                equations.append(e)
        for i in range(nc):
            for j in range(nk):
                e=D[i][j]
                for k in range(ni):
                    e=add(e,{tuple(sorted(m+(u[k][j],))):c for m,c in C[i][k].items()},p,-1)
                equations.append(e)
    assert len(names)==761 and len(equations)==1650
    equations=unique(equations,p)
    print('INITIAL','variables',760,'nonzero_distinct_equations',len(equations),
          'terms',sum(map(len,equations)),flush=True)
    history=[]; eliminated=set(); blocked=set(); stop='no eligible elimination'
    while len(history)<args.max_steps:
        if time.monotonic()-started>args.max_seconds: stop='internal time gate'; break
        occurrences={}
        for e in equations:
            for v in {x for m in e for x in m if x}: occurrences[v]=occurrences.get(v,0)+1
        candidates=[]
        for i,e in enumerate(equations):
            if len(e)>80: continue
            for v in sorted({x for m in e for x in m if x}):
                if v in blocked: continue
                pair=split(e,v,p)
                if pair is None: continue
                n,d=pair
                if len(d)>1 and not args.rational: continue
                score=(len(n)+len(d)-1)*occurrences[v]+(10000 if len(d)>1 else 0)
                candidates.append((score,i,v,n,d))
        if not candidates: break
        success=False
        for _,i,v,n,d in sorted(candidates,key=lambda x:x[:3]):
            try:
                trial=[substitute(e,v,n,d,p,args.max_terms) for j,e in enumerate(equations) if j!=i]
                trial=unique(trial,p)
                if sum(map(len,trial))>args.max_total_terms: raise Growth('total term cap')
            except Growth:
                blocked.add(v); continue
            # A nonzero q-only equation would contradict the known etale germ.
            assert all(any(x for m in e for x in m) for e in trial), 'nonzero parameter-only equation'
            equations=trial; eliminated.add(v)
            history.append({'variable':v,'name':names[v],'numerator':encode(n),'denominator':encode(d)})
            success=True
            if len(history)%20==0:
                print('PEELED',len(history),'remain',760-len(history),'eq',len(equations),
                      'terms',sum(map(len,equations)),'seconds',round(time.monotonic()-started,2),flush=True)
            break
        if not success: stop='all remaining candidates hit growth gates'; break
    if len(history)==args.max_steps: stop='step gate'
    remaining=[i for i in range(1,761) if i not in eliminated]
    scc=[]; graph={}; scc_status='not attempted after time gate'
    if time.monotonic()-started<args.max_seconds:
        try:
            scc,graph=implicit_scc(equations,remaining,p,args.max_terms)
            scc_status='exact constant-Jacobian normalization'
        except Growth: scc_status='normalization polynomial term gate'
    result={'status':'exact local rational elimination; no Groebner computation or fibre claim',
            'prime':p,'path':args.path,'preserves_certified_sixjet':args.path=='sixjet',
            'input_sha256':hashlib.sha256(blockpath.read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'variable_names':names,'original_z_polynomials':{str(j):encode(v) for j,v in z.items()},
            'auxiliary_variable_indices':u_map,'remaining_variables':remaining,
            'elimination_history':history,'equations':[encode(e) for e in equations],
            'all_elimination_denominators_are_origin_units':True,
            'stop_reason':stop,'SCC_status':scc_status,'SCCs':scc,'dependency_graph':graph,
            'seconds':round(time.monotonic()-started,3)}
    output=(args.output or RUN/f'data/peeled_{args.path}_p{p}_{"rational" if args.rational else "polynomial"}.json').resolve()
    assert output.is_relative_to(RUN)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists(): raise FileExistsError('preserve existing output: '+str(output))
    output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    def expr(e):
        return '+'.join(str(c)+''.join('*'+names[v] for v in m) for m,c in sorted(e.items())) or '0'
    sing='// INPUT ONLY: origin branch, q parameter; no std/eliminate command.\n'
    sing+=f'ring reduced=({p},q),('+','.join(names[v] for v in remaining)+'),dp;\n'
    sing+='ideal curve=\n'+',\n'.join(expr(e) for e in equations)+';\n'
    sing+='print("REDUCED_LOCAL_CURVE_LOADED_NO_GROEBNER_JOB");\n'
    target=output.with_suffix('.sing'); assert not target.exists(); target.write_text(sing)
    print('FINAL','eliminated',len(history),'remaining',len(remaining),'eq',len(equations),
          'terms',sum(map(len,equations)),'SCC_sizes',sorted(map(len,scc),reverse=True),
          'stop',stop,'output',output,flush=True)


if __name__=='__main__': main()
