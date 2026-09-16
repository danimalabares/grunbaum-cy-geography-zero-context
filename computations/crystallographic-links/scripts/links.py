#!/usr/bin/env python3
"""Vertex links of CP^2_9 and CP^2_10: orbit representatives, exact isomorphism types,
f/h-vectors, Stanley--Reisner data (minimal nonfaces), Hilbert polynomials, PL-sphere
certificates (bistellar flips), automorphism groups, and the baseline identification of the
CP^2_9 link with the Bruckner--Gruenbaum sphere used by the sphere problem of this repository.
Writes data/links/*.txt and output/links.json."""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import simplicial as S  # noqa: E402

DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")
LINKDIR = os.path.join(DATA, "links")
os.makedirs(LINKDIR, exist_ok=True)

cp9 = S.parse_facets(open(os.path.join(DATA, "cp2_9_facets.txt")).read())
cp10 = S.parse_facets(open(os.path.join(DATA, "cp2_10_facets.txt")).read())
gs = S.parse_facets(open(os.path.join(DATA, "grunbaum_sphere_zero_context_packet.txt")).read())
assert len(cp9) == 36 and len(cp10) == 48 and len(gs) == 20

report = {}


def analyse_link(name, complex_facets, v, expected_orbit, aut_parent):
    lk = S.link(complex_facets, {v})
    lk = [frozenset(F) for F in lk]
    V = S.vertices(lk)
    n = len(V)
    fv = S.f_vector(lk)
    hv = S.h_vector(fv)
    hp = S.hilbert_polynomial(hv)
    info = {
        "vertex": v, "orbit_under_Aut_of_parent": expected_orbit,
        "link_vertices": V, "n": n, "facets": len(lk),
        "f_vector": fv, "h_vector": hv, "euler_characteristic": S.euler_characteristic(fv),
        "pure": S.is_pure(lk), "pseudomanifold": S.is_pseudomanifold(lk),
        "strongly_connected": S.is_strongly_connected(lk),
        "combinatorial_3_manifold": S.is_combinatorial_manifold_3(lk),
        "betti": S.betti_numbers(lk),
        "ambient_projective_space": f"P^{n-1}",
        "degree_of_SR_scheme": len(lk),
        "hilbert_polynomial_of_SR_ring": S.poly_str(hp),
        "hilbert_polynomial_coefficients": [str(c) for c in hp],
        "codimension": n - 1 - 3,
    }
    # Riemann--Roch reading (valid only if a smooth CY3 with the same Hilbert polynomial exists):
    # chi(O(k)) = (L^3/6) k^3 + (c2.L/12) k  =>  c2.L = 12 * coefficient of k.
    a3, a1 = hp[3], hp[1]
    info["RR_reading_if_smooth_CY3_fibre_existed"] = {"L^3": str(a3 * 6), "c2.L": str(a1 * 12),
                                                        "note": "hypothetical; no smooth fibre is asserted"}
    assert a3 * 6 == len(lk)
    mnf = S.minimal_nonfaces(lk)
    info["minimal_nonfaces_by_size"] = {k: sum(1 for m in mnf if len(m) == k) for k in sorted({len(m) for m in mnf})}
    info["minimal_nonfaces"] = [list(m) for m in mnf]
    auts = S.automorphism_group(lk)
    info["automorphism_group_order_of_link"] = len(auts)
    info["vertex_orbits_of_link_under_its_Aut"] = S.orbits(auts, V)
    # stabiliser of v in Aut(parent) restricted to the link
    stab = [a for a in aut_parent if a[v] == v]
    info["stabiliser_order_in_Aut_of_parent"] = len(stab)
    info["vertex_orbits_of_link_under_stabiliser"] = S.orbits(stab, V)
    ok, moves = S.certify_pl_sphere(lk)
    info["PL_sphere_certificate_found"] = ok
    info["bistellar_moves_to_boundary_of_4_simplex"] = [[list(A), list(B)] for A, B in moves] if ok else None
    with open(os.path.join(LINKDIR, f"{name}.txt"), "w") as fh:
        fh.write(f"# link of vertex {v} in {name.split('_link')[0]}; {len(lk)} facets on vertices {V}\n")
        for F in sorted(lk, key=sorted):
            fh.write(",".join(map(str, sorted(F))) + "\n")
        fh.write("# minimal nonfaces (generators of the Stanley--Reisner ideal):\n")
        for m in mnf:
            fh.write("# MNF " + ",".join(map(str, m)) + "\n")
    return lk, info


# ---------------------------------------------------------------------------
# CP^2_9: all nine links, isomorphism classes, identification with the Bruckner--Gruenbaum sphere
# ---------------------------------------------------------------------------
aut9 = S.automorphism_group(cp9)
links9 = {v: [frozenset(F) for F in S.link(cp9, {v})] for v in range(1, 10)}
classes9 = []
for v in range(1, 10):
    for cls in classes9:
        if S.isomorphism(links9[cls[0]], links9[v]) is not None:
            cls.append(v)
            break
    else:
        classes9.append([v])
report["cp2_9"] = {"automorphism_group_order": len(aut9), "link_isomorphism_classes": classes9}
lk9, info9 = analyse_link("cp2_9_link_v9", cp9, 9, S.orbits(aut9, range(1, 10))[0], aut9)
phi = S.isomorphism(lk9, gs)
info9["isomorphic_to_zero_context_packet_sphere"] = phi is not None
info9["relabelling_link_vertex_to_packet_vertex"] = {str(k): v for k, v in sorted(phi.items())} if phi else None
# check the relabelled facets literally
if phi:
    assert {frozenset(phi[v] for v in F) for F in lk9} == set(gs)
# neighbourly: all 28 edges, and any two facets meet (Bagchi--Datta 1994 characterisation)
info9["neighbourly"] = info9["f_vector"][1] == 28
info9["any_two_facets_intersect"] = all(F & G for F in lk9 for G in lk9)
report["cp2_9"]["link"] = info9

# ---------------------------------------------------------------------------
# CP^2_10: two vertex orbits, links of 1 = x11 and 2 = x12
# ---------------------------------------------------------------------------
aut10 = S.automorphism_group(cp10)
orbs10 = S.orbits(aut10, range(1, 11))
links10 = {v: [frozenset(F) for F in S.link(cp10, {v})] for v in range(1, 11)}
classes10 = []
for v in range(1, 11):
    for cls in classes10:
        if S.isomorphism(links10[cls[0]], links10[v]) is not None:
            cls.append(v)
            break
    else:
        classes10.append([v])
report["cp2_10"] = {"automorphism_group_order": len(aut10), "vertex_orbits": orbs10,
                    "link_isomorphism_classes": classes10}
lkA, infoA = analyse_link("cp2_10_link_v1_x11", cp10, 1, orbs10[0], aut10)
lkB, infoB = analyse_link("cp2_10_link_v2_x12", cp10, 2, orbs10[1], aut10)
infoA["isomorphic_to_other_orbit_link"] = S.isomorphism(lkA, lkB) is not None
report["cp2_10"]["link_x11"] = infoA
report["cp2_10"]["link_x12"] = infoB
# cross-check: neither CP^2_10 link is isomorphic to the CP^2_9 link (different vertex counts anyway)
report["cp2_10"]["links_vs_cp2_9_link"] = {"same_number_of_vertices": False}
# all CP^2_10 links are PL 3-spheres => CP^2_10 is a combinatorial 4-manifold
report["cp2_10"]["all_vertex_links_certified_PL_spheres"] = all(S.certify_pl_sphere(links10[v])[0] for v in range(1, 11))
report["cp2_9"]["all_vertex_links_certified_PL_spheres"] = all(S.certify_pl_sphere(links9[v])[0] for v in range(1, 10))

json.dump(report, open(os.path.join(OUT, "links.json"), "w"), indent=1, default=str)
# concise console summary
for key in ("cp2_9", "cp2_10"):
    print(f"== {key}: |Aut| = {report[key]['automorphism_group_order']}, link isomorphism classes = {report[key]['link_isomorphism_classes']}")
for label, info in (("CP2_9 link v9", info9), ("CP2_10 link x11", infoA), ("CP2_10 link x12", infoB)):
    print(f"-- {label}: n={info['n']} f={info['f_vector']} h={info['h_vector']} deg={info['degree_of_SR_scheme']} "
          f"P(k)={info['hilbert_polynomial_of_SR_ring']} |Aut(link)|={info['automorphism_group_order_of_link']} "
          f"stab={info['stabiliser_order_in_Aut_of_parent']} MNF={info['minimal_nonfaces_by_size']} "
          f"3-manifold={info['combinatorial_3_manifold']} betti={info['betti']['Q']} PL-cert={info['PL_sphere_certificate_found']}")
print("CP2_9 link == packet Gruenbaum sphere:", info9["isomorphic_to_zero_context_packet_sphere"], info9["relabelling_link_vertex_to_packet_vertex"])
print("CP2_10 links isomorphic to each other:", infoA["isomorphic_to_other_orbit_link"])
print("all links PL-certified:", report["cp2_9"]["all_vertex_links_certified_PL_spheres"], report["cp2_10"]["all_vertex_links_certified_PL_spheres"])
