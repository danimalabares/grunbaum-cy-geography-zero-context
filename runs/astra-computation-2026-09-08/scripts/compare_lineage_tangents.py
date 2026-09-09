#!/usr/bin/env python3
"""Exact, small standard-library comparison of the two frozen tangent classes.

No CAS or Groebner basis is used. Sparse rational row reduction compares maps
I -> (S/I)_3 in the 16*104 dimensional ambient space. Enumerate all 8! vertex
permutations, retain precisely the isomorphisms of the two nonface sets, and
transport the complete older CT^1 basis into the frozen zero-context quotient
by coordinate derivations. Output JSON goes to stdout; inputs are read-only.
"""
import ast
from fractions import Fraction as F
from itertools import permutations, combinations
import hashlib
import json
import argparse
from math import lcm
import re
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
SIBLINGS = REPO.parent
DATA = REPO / "equations/deformation_data.json"
OLD_BASIS = SIBLINGS / "grunbaum-cy-geography-fable-dgla/equations/fable_T1_basis_QQ.txt"
QUADRICS = SIBLINGS / "grunbaum-zero-context-proof/gs_quadratic_base.m2"
OLD_Y = [1,3,1,2,6,1,1,1,1,1,21,28,1,5,10,55,66,15,1,18,2,
         35,42,1,4,10,1,25,12,30,5,33,44,1,6,3,14,7,1,9,1,6,
         12,20,1,4,22,1,15,1,1,8,11]
OLD_GENERATORS = ["678","468","378","357","348","278","257","256",
                  "247","246","146","145","138","136","135","125"]
ZERO = (0,) * 8
BLOCK_MATRICES = [[[1,4,66,67,96,99],[18,20,35,39,105,102]],
                  [[21,22,26,27,97,92],[50,51,69,70,108,100]],
                  [[2,3,47,48,106,95],[23,24,36,37,104,109]]]

def plus(a,b,c=F(1)):
    out = dict(a)
    for k,v in b.items():
        out[k] = out.get(k,F(0)) + c*v
        if not out[k]: del out[k]
    return out

def mul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f))
            out[g]=out.get(g,F(0))+c*d
    return {k:v for k,v in out.items() if v}

def polynomial(s):
    def rec(n):
        if isinstance(n,ast.Constant): return {} if n.value==0 else {ZERO:F(n.value)}
        if isinstance(n,ast.Name):
            j=int(n.id[2:])-1 if n.id.startswith("x_") else "abcdefgh".index(n.id)
            return {tuple(int(i==j) for i in range(8)): F(1)}
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):
            return {k:-v for k,v in rec(n.operand).items()}
        if isinstance(n,ast.BinOp):
            a=rec(n.left)
            if isinstance(n.op,ast.Pow):
                b={ZERO:F(1)}
                for _ in range(n.right.value): b=mul(b,a)
                return b
            b=rec(n.right)
            if isinstance(n.op,ast.Add): return plus(a,b)
            if isinstance(n.op,ast.Sub): return plus(a,b,F(-1))
            if isinstance(n.op,ast.Mult): return mul(a,b)
            if isinstance(n.op,ast.Div): return {k:v/b[ZERO] for k,v in a.items()}
        raise ValueError(ast.dump(n))
    return rec(ast.parse(s.replace("^","**"),mode="eval").body)

def exponent(digits): return tuple(int(str(i+1) in digits) for i in range(8))
def perm_exp(e,p):
    a=[0]*8
    for i,n in enumerate(e): a[p[i]]=n
    return tuple(a)
def json_number(v): return int(v) if v.denominator==1 else str(v)

def main():
    data=json.loads(DATA.read_text())
    monomials=[next(iter(polynomial(s))) for s in data["generator_order"]]
    old_monomials=list(map(exponent,OLD_GENERATORS))
    gen_index={m:i for i,m in enumerate(monomials)}
    nonfaces=[{i for i,e in enumerate(m) if e} for m in monomials]
    faces=[set(c) for n in range(9) for c in combinations(range(8),n)
           if not any(m.issubset(c) for m in nonfaces)]
    facets=[s for s in faces if not any(s<t for t in faces)]
    assert len(facets)==20 and all(len(f)==4 for f in facets)
    vertex_intersections=[set.intersection(*(f for f in facets if v in f)) for v in range(8)]
    assert vertex_intersections==[{v} for v in range(8)]
    def reduce_images(images):
        return {(i,e):c for i,p in enumerate(images) for e,c in p.items()
                if not any(all(a<=b for a,b in zip(m,e)) for m in monomials)}
    intrinsic=data["intrinsic_columns_in_embedded_basis_1_based"]
    new_basis=[reduce_images([polynomial(s) for s in
                data["embedded_tangent_basis"][j-1]["images_in_generator_order"]])
               for j in intrinsic]
    new_y=list(map(F,data["selected_tangent_coordinates_53"]))
    raw_z={}
    for i,b in enumerate(new_basis): raw_z=plus(raw_z,b,new_y[i])
    assert raw_z==reduce_images([polynomial(s) for s in data["first_order_corrections"]])
    # Independently compare the recorded 27 quadratic expressions with the
    # linear span of the 45 minors. This guards matrix-entry transcription.
    minor_span={}
    def reduce_quadratic(v):
        while v and min(v) in minor_span:
            p=min(v); v=plus(v,minor_span[p],-v[p])
        return v
    for a,b in BLOCK_MATRICES:
        for i,j in combinations(range(6),2):
            v=plus({tuple(sorted((a[i],b[j]))):F(1)},
                   {tuple(sorted((a[j],b[i]))):F(1)},F(-1))
            v=reduce_quadratic(v)
            if v:
                c=v[min(v)]; minor_span[min(v)]={k:x/c for k,x in v.items()}
    q_text=QUADRICS.read_text().split("J=ideal(",1)[1].split(");",1)[0]
    q_rows=q_text.replace("\n","").replace(" ","").split(",")
    assert len(q_rows)==27
    for expression in q_rows:
        terms=re.findall(r"([+-]?)(t\d+)\*(t\d+)",expression)
        assert "".join(sign+a+"*"+b for sign,a,b in terms)==expression
        v={}
        for sign,a,b in terms:
            v=plus(v,{tuple(sorted((int(a[1:]),int(b[1:])))):F(-1 if sign=="-" else 1)})
        assert not reduce_quadratic(v), "A source quadric is outside the proposed minors"
    old_basis=[]
    for j,line in enumerate(OLD_BASIS.read_text().splitlines()):
        fields=line.split("|"); assert int(fields[0])==j and len(fields)==17
        old_basis.append([polynomial(s) for s in fields[1:]])
    assert len(old_basis)==53
    # An echelon row carries its expression in the original 109-row basis.
    echelon={}; original=[]
    def insert(v):
        j=len(original); original.append(v); coeff={j:F(1)}
        while v:
            pivot=min(v)
            if pivot not in echelon:
                c=v[pivot]
                echelon[pivot]=({k:w/c for k,w in v.items()},
                                {k:w/c for k,w in coeff.items()})
                return True
            c=v[pivot]; row,track=echelon[pivot]
            v=plus(v,row,-c); coeff=plus(coeff,track,-c)
        original.pop()
        return False
    derivation_labels=[]
    for source in range(8):
        for target in range(8):
            images=[]
            for m in monomials:
                if m[source]:
                    e=list(m); e[source]-=1; e[target]+=1
                    images.append({tuple(e):F(m[source])})
                else: images.append({})
            if insert(reduce_images(images)):
                derivation_labels.append([source+1,target+1])
    orbit_rank=len(original); assert orbit_rank==56
    for b in new_basis: assert insert(b)
    assert len(original)==109
    weights=[]
    for b in new_basis:
        ws={tuple(e[k]-monomials[g][k] for k in range(8)) for g,e in b}
        assert len(ws)==1
        weights.append([1,*next(iter(ws))])  # initial 1 permits parameter rescaling
    def torus_obstruction(source,target):
        """Find a violated integer character relation for target/source.

        A relation among (1,weight) vectors must give product ratios^n=1
        under any diagonal coordinate change and nonzero parameter scaling,
        over any algebraically closed characteristic-zero field.
        """
        rows={}
        ratios=[target[i]/source[i] for i in range(53)]
        for i,w in enumerate(weights):
            v={j:F(x) for j,x in enumerate(w) if x}; relation={i:F(1)}
            while v:
                pivot=min(v)
                if pivot not in rows:
                    c=v[pivot]
                    rows[pivot]=({k:x/c for k,x in v.items()},
                                 {k:x/c for k,x in relation.items()})
                    break
                c=v[pivot]; row,track=rows[pivot]
                v=plus(v,row,-c); relation=plus(relation,track,-c)
            if not v:
                den=lcm(*(c.denominator for c in relation.values()))
                n={j:int(c*den) for j,c in relation.items()}
                product=F(1)
                for j,c in n.items(): product*=ratios[j]**c
                if product!=1:
                    return {"positions_and_exponents":[[j+1,c] for j,c in sorted(n.items())],
                            "ratio_product":str(product),"required_ratio_product":"1"}
        return None
    def coordinates(v):
        out={}
        while v:
            pivot=min(v); assert pivot in echelon, "Not in the Hilbert tangent space"
            c=v[pivot]; row,track=echelon[pivot]
            v=plus(v,row,-c); out=plus(out,track,c)
        # Independently reconstruct the actual ambient correction vector.
        reconstructed={}
        for j,c in out.items(): reconstructed=plus(reconstructed,original[j],c)
        return [out.get(56+j,F(0)) for j in range(53)], reconstructed
    def block_minors(y):
        t=dict(zip(intrinsic,y))
        # Actual normalMatrix column labels; all three matrices reproduce
        # the nine quadrics of the corresponding block upon taking minors.
        return [[json_number(t[a[i]]*t[b[j]]-t[a[j]]*t[b[i]])
                 for i,j in combinations(range(6),2)] for a,b in BLOCK_MATRICES]
    results=[]
    for p in permutations(range(8)):
        if {perm_exp(m,p) for m in old_monomials} != set(monomials): continue
        gen_perm=[gen_index[perm_exp(m,p)] for m in old_monomials]
        transformed=[]; matrix=[]
        for basis in old_basis:
            images=[{} for _ in range(16)]
            for i,poly in enumerate(basis):
                images[gen_perm[i]]={perm_exp(e,p):c for e,c in poly.items()}
            raw=reduce_images(images)
            c,reconstructed=coordinates(raw); assert raw==reconstructed
            transformed.append(raw); matrix.append(c)
        positions=[]
        for c in matrix:
            support=[i for i,v in enumerate(c) if v]
            assert len(support)==1 and c[support[0]]==1
            positions.extend(support)
        assert sorted(positions)==list(range(53))
        old_y=[sum(F(OLD_Y[j])*matrix[j][i] for j in range(53)) for i in range(53)]
        ratios=[old_y[i]/new_y[i] for i in range(53)]
        mismatch=[i+1 for i in range(53) if old_y[i]!=new_y[i]]
        results.append({
          "old_x_to_new_one_based":[i+1 for i in p],
          "old_generator_to_new_one_based":[i+1 for i in gen_perm],
          "old_y_in_zero_context_basis":[json_number(v) for v in old_y],
          "equal_mod_orbit":not mismatch,
          "proportional_mod_orbit":len(set(ratios))==1,
          "diagonal_torus_and_parameter_rescaling_obstruction":torus_obstruction(old_y,new_y),
          "mismatch_positions":mismatch,
          "P1_block_minors":block_minors(old_y),
          "basis_change_columns_sparse":[[[i+1,json_number(v)] for i,v in enumerate(c) if v]
                                          for c in matrix]})
    assert len(results)==6
    assert all(all(v==0 for v in block) for block in block_minors(new_y))
    # Reproduce the four link combinations in the first coordinate choice.
    gp=results[0]["old_generator_to_new_one_based"]
    link_indices=[[gp[i] for i in range(r,16,4)] for r in range(4)]
    result={"status":"COMPUTER-CERTIFIED", "arithmetic":"QQ using fractions.Fraction",
        "input_sha256":{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (DATA,OLD_BASIS,QUADRICS)},
        "orbit_rank":orbit_rank,"combined_basis_rank":len(original),
        "coordinate_vertices_are_component_intersections":True,
        "all_27_source_quadrics_in_span_of_45_displayed_minors":True,
        "zero_context_first_order_corrections_match_selected_vector":True,
        "zero_context_y":data["selected_tangent_coordinates_53"],
        "zero_context_P1_block_minors":block_minors(new_y),
        "number_of_vertex_identifications":len(results),
        "old_link_generator_indices_under_first_identification":link_indices,
        "comparisons":results}
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.output:
        output=args.output.resolve()
        assert output.is_relative_to(HERE.parents[1]), "Output must stay in this run directory"
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(result,indent=2)+"\n")
        print("certificate="+str(output))
        print("orbit_rank=56; combined_basis_rank=109; vertex_identifications=6")
        for r in results:
            print("permutation="+str(r["old_x_to_new_one_based"])+
                  "; proportional_mod_orbit="+str(r["proportional_mod_orbit"])+
                  "; P1_nonzero_minors="+str([sum(v!=0 for v in b) for b in r["P1_block_minors"]])+
                  "; torus_obstruction="+str(r["diagonal_torus_and_parameter_rescaling_obstruction"]))
        print("first_transported_tangent="+str(results[0]["old_y_in_zero_context_basis"]))
        print("first_basis_permutation="+str([c[0][0] for c in results[0]["basis_change_columns_sparse"]]))
    else: print(json.dumps(result,indent=2))

if __name__=="__main__": main()
