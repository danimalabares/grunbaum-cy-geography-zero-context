#!/usr/bin/env python3
"""Stage-1 audit driver: the 14 symmorphic ("linear") space groups of the 35-list.

Steps (all exact, pure Python 3; uses only scripts/sgcy3.py and the cached inputs in data/):
  A. read both crystallographic databases, derive lattices/primitive bases/point groups,
     cross-check spglib against GAP CrystCat coset by coset, certify symmorphic status;
  B. orbifold Hodge numbers of A_τ/G for the 14 linear cases (+ the 2 symmorphic controls
     I222 = 23 and I23 = 197 that complete the 16 Z-classes), with the DHVW Euler check;
  C. Z-class identification with explicit GL(3,Z)-conjugators against Donten-Bury's Table 1
     and Burek's list; Donten-Bury <-> Burek cross-identification; transpose (dual) control;
     setting-independence control for R32 (hexagonal vs rhombohedral axes);
  D. literature comparison of the Hodge numbers; 35-row machine-readable table.
Outputs: output/*.json, table/space_groups_35.{json,tsv}, output/run_all.log.
Run:  python3 scripts/run_all.py
"""
from __future__ import annotations
import json, sys, time
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sgcy3 as S

ROOT = S.ROOT
OUT = ROOT / "output"; TAB = ROOT / "table"
OUT.mkdir(exist_ok=True); TAB.mkdir(exist_ok=True)
LOG = []

def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

CONTROLS = [23, 197]
POINT_GROUP_TYPE = {"222": ("Z2xZ2", 4), "422": ("D4 (order 8)", 8), "312": ("S3", 6), "321": ("S3", 6), "32": ("S3", 6),
                    "622": ("D6 (order 12)", 12), "23": ("A4", 12), "432": ("S4", 24)}

def hm_point_group(short):
    import re
    s = re.sub(r"_\d", "", short)           # drop screw subscripts
    return s[1:]                             # drop the lattice letter

def small_generating_set(G):
    """Greedy small generating set of a finite matrix group (list of matrices)."""
    els = sorted(G, key=lambda g: -S.order(g))
    gens = []
    for g in els:
        if g == S.ident(3):
            continue
        if gens and S.key(g) in {S.key(x) for x in S.group_closure(gens)}:
            continue
        gens.append(g)
        if len(S.group_closure(gens)) == len(G):
            break
    assert len(S.group_closure(gens)) == len(G)
    return gens

def main():
    t0 = time.time()
    spg_version, spg = S.load_spglib()
    gap_versions, cc = S.load_crystcat()
    lit = json.loads((ROOT / "data" / "literature_zclasses.json").read_text())
    jbd = json.loads((ROOT / "data" / "jbd_figure_2_8_groups.json").read_text())
    log(f"spglib {spg_version}; GAP {gap_versions}")
    log(f"JBD Figure 2.8 list read from the cached PDF: {jbd['count']} groups; equals the list under audit: {jbd['equals_list_under_audit']}")
    assert jbd["equals_list_under_audit"] and jbd["numbers_read_from_figure"] == S.ALL35

    # ---------------- A. crystallographic data, cross-check, symmorphic certification ----------------
    cryst = {}
    for n in S.ALL35 + CONTROLS:
        choice = "H" if n == 155 else ""
        entry = spg[(n, choice)]
        ops = entry["ops"]
        centrings, B = S.conventional_lattice(ops)
        cosets = S.to_primitive(ops, B)
        Gmats = S.point_group_matrices(cosets)
        # CrystCat closure in the same primitive basis
        gens_cc = cc[n]["gens"]
        cc_cosets = S.closure_cosets([(S.as_int(S.mm(S.mm(S.inv(B), R), B)), S.mv(S.inv(B), t)) for R, t in gens_cc])
        agree = cc_cosets == cosets
        symm = S.is_symmorphic_at_origin(cosets)
        pg = hm_point_group(entry["meta"]["international_short"])
        cryst[n] = {"meta": entry["meta"], "hm_short": entry["meta"]["international_short"],
                    "hm_full": entry["meta"]["international_full"], "hall": entry["meta"]["hall_symbol"],
                    "point_group_hm": pg, "point_group_type": POINT_GROUP_TYPE[pg][0], "point_group_order": len(cosets),
                    "arithmetic_class": pg + entry["meta"]["international_short"][0],
                    "lattice_letter": entry["meta"]["international_short"][0],
                    "centring_vectors_conventional": centrings, "primitive_basis_columns_conventional": B,
                    "index_conventional_in_full_lattice": len(centrings),
                    "point_group_matrices_primitive": Gmats,
                    "translation_parts_primitive_mod_1": [list(cosets[S.key(g)]) for g in Gmats],
                    "symmorphic_at_ITA_origin_spglib": symm, "symmorphic_crystcat": cc[n]["meta"]["is_symmorphic_crystcat"],
                    "crystcat_settings_available": cc[n]["meta"]["settings"],
                    "spglib_vs_crystcat_cosets_agree": agree, "n_operations_spglib": len(ops)}
        assert agree, f"database mismatch for group {n}"
        assert len(cosets) == POINT_GROUP_TYPE[pg][1] == cc[n]["meta"]["point_group_order"]
        assert symm == cc[n]["meta"]["is_symmorphic_crystcat"]
        log(f"[A] {n:3d} {entry['meta']['international_short']:10s} pg {pg:3s} |G|={len(cosets):2d} centrings={len(centrings)} "
            f"symmorphic={symm} spglib==crystcat: {agree}")
    symm_list = [n for n in S.ALL35 if cryst[n]["symmorphic_at_ITA_origin_spglib"]]
    log(f"[A] symmorphic members of the 35-list: {symm_list}")
    assert symm_list == S.LINEAR14, "the symmorphic subset differs from the proposed 14"
    assert all(cryst[n]["symmorphic_at_ITA_origin_spglib"] for n in CONTROLS)
    (OUT / "crystallographic_data.json").write_text(json.dumps(S.jsonable(cryst), indent=1))

    # ---------------- B. orbifold Hodge numbers ----------------
    results = {}
    for n in S.LINEAR14 + CONTROLS:
        G = cryst[n]["point_group_matrices_primitive"]
        assert all(all(x == 0 for x in s) for s in cryst[n]["translation_parts_primitive_mod_1"])
        res = S.orbifold_hodge(G)
        results[n] = res
        assert res["euler_check"], f"DHVW Euler check failed for {n}"
        assert res["h10"] == 0 and res["h20"] == 0 and res["h30"] == 1
        log(f"[B] {n:3d} {cryst[n]['hm_short']:10s} untwisted (h11,h21)=({res['untwisted_h_pq'][1][1]},{res['untwisted_h_pq'][2][1]})"
            f"  total (h11,h21)=({res['h11']},{res['h21']})  e={res['euler_from_hodge']} DHWV e={res['euler_DHVW']} "
            f"|pi1(A/G)|={res['pi1_order_of_A_mod_G']} axis index={res['axis_index']}")
    (OUT / "hodge_numbers_linear.json").write_text(json.dumps(S.jsonable({str(k): v for k, v in results.items()}), indent=1))

    # ---------------- C. Z-class identification ----------------
    DB = lit["donten_bury"]["classes"]; BU = lit["burek"]["groups"]
    db_groups = {lab: S.group_closure(c["generators"]) for lab, c in DB.items()}
    bu_groups = {lab: S.group_closure(g["generators"]) for lab, g in BU.items()}
    for lab, g in db_groups.items():
        assert all(S.det(x) == 1 for x in g)
    for lab, g in bu_groups.items():
        assert all(S.det(x) == 1 for x in g)
    matching = {}
    for n in S.LINEAR14 + CONTROLS:
        G = cryst[n]["point_group_matrices_primitive"]
        gens = small_generating_set(G)
        GT = [S.transpose(g) for g in G]
        gensT = [S.transpose(g) for g in gens]
        rec = {"generators_primitive": gens, "donten_bury": {}, "burek": {}, "transpose_control_donten_bury": {}}
        for lab, H in db_groups.items():
            if len(H) != len(G):
                continue
            r = S.find_conjugator(G, gens, H)
            if isinstance(r, tuple) and len(r) == 3:
                P, phi, rk = r
                rec["donten_bury"][lab] = {"conjugator_P": P, "det_P": S.det(P), "intertwiner_rank": rk, "conjugate": True}
            else:
                rec["donten_bury"][lab] = {"conjugate": False, "note": None if r is None else r[0], "intertwiner_rank": None if r is None else r[1]}
            rT = S.find_conjugator(GT, gensT, H)
            rec["transpose_control_donten_bury"][lab] = bool(isinstance(rT, tuple) and len(rT) == 3)
        for lab, H in bu_groups.items():
            if len(H) != len(G):
                continue
            r = S.find_conjugator(G, gens, H)
            if isinstance(r, tuple) and len(r) == 3:
                P, phi, rk = r
                rec["burek"][lab] = {"conjugator_P": P, "det_P": S.det(P), "intertwiner_rank": rk, "conjugate": True}
            else:
                rec["burek"][lab] = {"conjugate": False, "note": None if r is None else r[0], "intertwiner_rank": None if r is None else r[1]}
        db_hits = [lab for lab, v in rec["donten_bury"].items() if v["conjugate"]]
        bu_hits = [lab for lab, v in rec["burek"].items() if v["conjugate"]]
        dbT_hits = [lab for lab, v in rec["transpose_control_donten_bury"].items() if v]
        assert len(db_hits) == 1 and len(bu_hits) == 1, (n, db_hits, bu_hits)
        rec["donten_bury_class"] = db_hits[0]; rec["burek_group"] = bu_hits[0]; rec["transpose_matches_donten_bury"] = dbT_hits
        matching[n] = rec
        log(f"[C] {n:3d} {cryst[n]['hm_short']:10s} = Donten-Bury {db_hits[0]:6s} = Burek G_{bu_hits[0]:5s}; transpose matches {dbT_hits}")
    # each Z-class hit exactly once by the 16 symmorphic groups
    db_used = [matching[n]["donten_bury_class"] for n in S.LINEAR14 + CONTROLS]
    bu_used = [matching[n]["burek_group"] for n in S.LINEAR14 + CONTROLS]
    assert sorted(db_used) == sorted(DB) and sorted(bu_used) == sorted(BU), "the 16 symmorphic groups do not biject onto the 16 published classes"
    log("[C] bijection 16 symmorphic Sohncke groups (non-cyclic point group) <-> 16 Donten-Bury classes <-> 16 Burek groups: verified")
    # Donten-Bury <-> Burek direct cross-identification
    db_bu = {}
    for lab, H in db_groups.items():
        gens = small_generating_set(H)
        hits = []
        for lab2, H2 in bu_groups.items():
            if len(H2) != len(H):
                continue
            r = S.find_conjugator(H, gens, H2)
            if isinstance(r, tuple) and len(r) == 3:
                hits.append((lab2, r[0]))
        assert len(hits) == 1, (lab, hits)
        db_bu[lab] = {"burek_group": hits[0][0], "conjugator_P": hits[0][1]}
        # consistency with the space-group route
        for n in S.LINEAR14 + CONTROLS:
            if matching[n]["donten_bury_class"] == lab:
                assert matching[n]["burek_group"] == hits[0][0], (n, lab, hits)
    log("[C] Donten-Bury -> Burek identification: " + ", ".join(f"{a}->G_{b['burek_group']}" for a, b in db_bu.items()))
    # duality control: the transposed group of a space group in a dual pair must match the dual class
    dual_of = {}
    for a, b in lit["donten_bury"]["duality"]["dual_pairs"]:
        dual_of[a] = b; dual_of[b] = a
    for a in lit["donten_bury"]["duality"]["self_dual"]:
        dual_of[a] = a
    for n in S.LINEAR14 + CONTROLS:
        lab = matching[n]["donten_bury_class"]
        assert matching[n]["transpose_matches_donten_bury"] == [dual_of[lab]], (n, lab, matching[n]["transpose_matches_donten_bury"])
    log("[C] transpose control: rho(G)^T is conjugate exactly to the Donten-Bury dual class in every case")
    # setting-independence control for R32: rhombohedral-axes setting
    ops_R = spg[(155, "R")]["ops"]
    centr_R, B_R = S.conventional_lattice(ops_R)
    cos_R = S.to_primitive(ops_R, B_R)
    G_R = S.point_group_matrices(cos_R)
    assert S.is_symmorphic_at_origin(cos_R) and len(centr_R) == 1
    r = S.find_conjugator(G_R, small_generating_set(G_R), cryst[155]["point_group_matrices_primitive"])
    assert isinstance(r, tuple) and len(r) == 3
    resR = S.orbifold_hodge(G_R)
    assert (resR["h11"], resR["h21"]) == (results[155]["h11"], results[155]["h21"])
    log(f"[C] R32 setting control: rhombohedral-axes point group conjugate to the hexagonal-axes one (P = {r[0]}); same Hodge numbers")
    # C'. pairwise non-conjugacy of the 16 point-group representations, independently of the literature:
    #     either by GL(3,Z)-invariants (per-class fixed-locus data, axis index, |Λ/S_Λ|) or, when the
    #     invariants coincide, by the exhaustive intertwiner search (complete when every isomorphism has
    #     an intertwiner module of rank <= 1, i.e. for absolutely irreducible representations).
    def invariants(n):
        r = results[n]
        per_class = sorted((t["order"], t["class_size"], t["centraliser_order"], tuple(t["invariant_factors_of_(g-1)_on_L"]),
                            t["centraliser_orbits"], t["orbits_with_elliptic_quotient"]) for t in r["twisted_sectors"])
        return (r["order"], tuple(per_class), r["axis_index"], r["Lambda_mod_S_index"])
    pairwise = []
    sixteen = S.LINEAR14 + CONTROLS
    for i in range(len(sixteen)):
        for j in range(i + 1, len(sixteen)):
            a, b = sixteen[i], sixteen[j]
            if invariants(a) != invariants(b):
                pairwise.append({"pair": [a, b], "distinguished_by": "invariants"})
                continue
            Ga = cryst[a]["point_group_matrices_primitive"]; Gb = cryst[b]["point_group_matrices_primitive"]
            r = S.find_conjugator(Ga, small_generating_set(Ga), Gb)
            assert not (isinstance(r, tuple) and len(r) == 3), f"groups {a} and {b} are conjugate"
            rank = None if r is None else r[1]
            assert rank is not None and rank <= 1, f"pair {a},{b}: equal invariants and intertwiner rank {rank} (search not exhaustive)"
            pairwise.append({"pair": [a, b], "distinguished_by": "exhaustive intertwiner search (rank <= 1)", "max_intertwiner_rank": rank})
    log(f"[C'] pairwise non-conjugacy of the 16 symmorphic point-group representations certified: "
        f"{sum(1 for p in pairwise if p['distinguished_by']=='invariants')} pairs by invariants, "
        f"{sum(1 for p in pairwise if p['distinguished_by']!='invariants')} pairs by exhaustive search "
        f"({[p['pair'] for p in pairwise if p['distinguished_by']!='invariants']})")
    matching_out = {"space_groups": {str(k): v for k, v in matching.items()}, "donten_bury_to_burek": db_bu,
                    "pairwise_nonconjugacy_of_the_16": pairwise,
                    "R32_rhombohedral_setting_conjugator": r[0], "duality_used": lit["donten_bury"]["duality"]}
    (OUT / "zclass_matching.json").write_text(json.dumps(S.jsonable(matching_out), indent=1))

    # ---------------- D. literature comparison and the 35-row table ----------------
    comparison = {}
    for n in S.LINEAR14 + CONTROLS:
        lab = matching[n]["donten_bury_class"]; blab = matching[n]["burek_group"]
        db_h = (DB[lab]["h11_from_b2"], DB[lab]["h21_from_b3"]); bu_h = (BU[blab]["h11"], BU[blab]["h21"])
        mine = (results[n]["h11"], results[n]["h21"])
        aw = (20, 6) if lab == "S4(1)" else None
        comparison[n] = {"computed_h11_h21": mine, "donten_bury_class": lab, "donten_bury_betti": DB[lab]["betti"],
                         "donten_bury_h11_h21": db_h, "burek_group": blab, "burek_h11_h21": bu_h,
                         "andreatta_wisniewski_h11_h21": aw,
                         "agree_donten_bury": mine == db_h, "agree_burek": mine == bu_h,
                         "agree_andreatta_wisniewski": (None if aw is None else mine == aw)}
        assert mine == db_h == bu_h, (n, mine, db_h, bu_h)
        log(f"[D] {n:3d} {cryst[n]['hm_short']:10s} computed {mine} = Donten-Bury {lab} {db_h} = Burek G_{blab} {bu_h}" + (f" = AW {aw}" if aw else ""))
    (OUT / "literature_comparison.json").write_text(json.dumps(S.jsonable(comparison), indent=1))

    rows = []
    for n in S.ALL35:
        c = cryst[n]
        # generators of the space group modulo Λ, in the primitive basis: pairs (M | t), t mod Z^3;
        # together with the three primitive lattice translations they generate the space group.
        tr_of = {S.key(g): t for g, t in zip(c["point_group_matrices_primitive"], c["translation_parts_primitive_mod_1"])}
        gens_str = "; ".join("[" + ",".join(",".join(map(str, r)) for r in g) + " | " + ",".join(str(x) for x in tr_of[S.key(g)]) + "]"
                             for g in small_generating_set(c["point_group_matrices_primitive"]))
        row = {"ita_number": n, "hermann_mauguin": c["hm_full"], "hall_symbol": c["hall"],
               "setting": "ITA standard setting (spglib Hall number %d%s); origin: ITA standard origin" % (c["meta"]["hall_number"], ", hexagonal axes" if n == 155 else ""),
               "primitive_basis_columns_in_conventional_coordinates": "; ".join(",".join(str(x) for x in col) for col in zip(*c["primitive_basis_columns_conventional"])),
               "centring_vectors": "; ".join(",".join(str(x) for x in v) for v in c["centring_vectors_conventional"]),
               "in_jbd_figure_2_8": n in jbd["numbers_read_from_figure"],
               "point_group_hm": c["point_group_hm"], "point_group_type": c["point_group_type"], "point_group_order": c["point_group_order"],
               "arithmetic_class": c["arithmetic_class"], "lattice_index_conventional_in_full": c["index_conventional_in_full_lattice"],
               "symmorphic": c["symmorphic_at_ITA_origin_spglib"],
               "stage1_status": "audited (linear/symmorphic)" if n in results else "pending (non-symmorphic; translations retained; not computed in stage 1)",
               "generators_primitive_basis": gens_str,
               "h11": results[n]["h11"] if n in results else None, "h21": results[n]["h21"] if n in results else None,
               "euler": results[n]["euler_from_hodge"] if n in results else None,
               "resolution_status": ("crepant projective resolution exists (BKR Thm 1.2, G-Hilb); Hodge numbers = orbifold Hodge numbers (Yasuda Thm 1.5 / Batyrev Thm 7.5); strict CY (h10=h20=0)" if n in results else "pending"),
               "literature_match": (f"Donten-Bury {matching[n]['donten_bury_class']} (Table 1/2, arXiv:0812.3758); Burek G_{matching[n]['burek_group']} (arXiv:2112.03970)" + ("; Andreatta-Wisniewski §4.2 octahedral" if matching[n]['donten_bury_class'] == 'S4(1)' else "")) if n in results else "pending (no individual literature search performed in stage 1)",
               "literature_h11_h21": list(comparison[n]["donten_bury_h11_h21"]) if n in results else None,
               "agrees_with_literature": (comparison[n]["agree_donten_bury"] and comparison[n]["agree_burek"]) if n in results else None,
               "pi1_order_A_mod_G": results[n]["pi1_order_of_A_mod_G"] if n in results else None,
               "evidence": ("output/hodge_numbers_linear.json, output/zclass_matching.json, output/literature_comparison.json, output/crystallographic_data.json" if n in results else "output/crystallographic_data.json (generators only)")}
        rows.append(row)
    (TAB / "space_groups_35.json").write_text(json.dumps(S.jsonable(rows), indent=1))
    cols = list(rows[0].keys())
    with open(TAB / "space_groups_35.tsv", "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join("" if r[k] is None else json.dumps(S.jsonable(r[k])) if isinstance(r[k], (list, dict)) else str(r[k]) for k in cols) + "\n")
    log(f"[D] wrote table/space_groups_35.json and .tsv ({len(rows)} rows: {sum(1 for r in rows if r['h11'] is not None)} audited, {sum(1 for r in rows if r['h11'] is None)} pending)")
    log(f"total time {time.time() - t0:.1f}s")
    (OUT / "run_all.log").write_text("\n".join(LOG) + "\n")
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
