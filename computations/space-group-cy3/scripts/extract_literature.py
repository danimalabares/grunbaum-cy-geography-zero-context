#!/usr/bin/env python3
"""Transcribe, by parsing the cached LaTeX sources, the published data used for the
comparison:

* M. Donten-Bury, *On Kummer 3-folds* (arXiv:0812.3758): Table 1 (generators of the
  16 Z-classes of finite non-cyclic subgroups of SL(3,Z)) and Table 2 (Poincaré
  polynomials of the Kummer 3-folds), and Proposition 1.7 (dual pairs).
* D. Burek, *Zeta function of some Kummer Calabi–Yau 3-folds* (arXiv:2112.03970):
  the 16 groups G_{n.k} (Tahara's representatives) with their generators and the
  Hodge numbers (h^{1,1}, h^{2,1}) of Kum_3(E, G).
* M. Andreatta, J. Wiśniewski, *On the Kummer construction* (arXiv:0804.4611):
  the Poincaré polynomial of the crepant resolution of A^3/S_4 (octahedral group).

Run:  python3 scripts/extract_literature.py
Needs the cached sources in sources/ (not committed; see sources/MANIFEST.json).
Output: data/literature_zclasses.json (committed).
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "sources"
OUT = ROOT / "data" / "literature_zclasses.json"

ARRAY = re.compile(r"\\begin\{array\}\{rrr\}(.*?)\\end\{array\}", re.S)

def parse_array(body: str) -> list[list[int]]:
    rows = [r for r in re.split(r"\\\\", body) if r.strip()]
    M = [[int(x.strip()) for x in r.split("&")] for r in rows]
    assert len(M) == 3 and all(len(r) == 3 for r in M), body
    return M

def donten_bury() -> dict:
    tex = (SRC / "arxiv_0812.3758_tex" / "kummer.tex").read_text()
    # Table 1 --------------------------------------------------------------
    t1_start = tex.index(r"\textbf{group} & \textbf{generators}")
    t1_end = tex.index(r"\caption{$\Z$-classes of finite non-cyclic subgroups", t1_start)
    table1 = tex[t1_start:t1_end]
    rows = re.split(r"\\hline", table1)
    classes = {}
    order_in_table = []
    for row in rows:
        m = re.search(r"\$([A-Z])_\{?(\d+)\}?(?:\((\d)\))?\$\s*&", row)
        if not m:
            continue
        label = f"{m.group(1)}{m.group(2)}" + (f"({m.group(3)})" if m.group(3) else "")
        mats = [parse_array(b) for b in ARRAY.findall(row)]
        assert len(mats) == 2, (label, row)
        classes[label] = {"generators": mats}
        order_in_table.append(label)
    assert len(classes) == 16, order_in_table
    # Table 2 --------------------------------------------------------------
    t2_start = tex.index(r"\textbf{group} & \textbf{section} & \textbf{polynomial}")
    t2_end = tex.index(r"\caption{Poincar\'e polynomials of Kummer 3-folds}", t2_start)
    table2 = tex[t2_start:t2_end]
    for m in re.finditer(r"\$([A-Z])_\{?(\d+)\}?(?:\((\d)\))?\$\s*&\s*\\ref\{(\w+)\}\s*&\s*\$([^$]*)\$", table2):
        label = f"{m.group(1)}{m.group(2)}" + (f"({m.group(3)})" if m.group(3) else "")
        poly = m.group(5).replace(" ", "")
        coeffs = {}
        for term in re.finditer(r"([+-]?)(\d*)t\^(\d)|([+-]?)(\d+)(?![t^\d])", poly):
            if term.group(3):
                c = int((term.group(1) or "") + (term.group(2) or "1")); coeffs[int(term.group(3))] = c
            else:
                coeffs[0] = int((term.group(4) or "") + term.group(5))
        b = [coeffs.get(i, 0) for i in range(7)]
        assert b[0] == 1 and b[6] == 1 and b[1] == 0 and b[5] == 0 and b[2] == b[4], (label, poly, b)
        classes[label]["poincare_polynomial"] = poly
        classes[label]["betti"] = b
        classes[label]["section_label"] = m.group(4)
        # For a Calabi–Yau threefold with h^{1,0}=h^{2,0}=0: b2 = h^{1,1}, b3 = 2 + 2 h^{2,1}.
        assert (b[3] - 2) % 2 == 0
        classes[label]["h11_from_b2"] = b[2]
        classes[label]["h21_from_b3"] = (b[3] - 2) // 2
    assert all("betti" in c for c in classes.values())
    # Dual pairs (Proposition on duality) ------------------------------------
    dual = {"self_dual": [], "dual_pairs": []}
    m = re.search(r"each of the following classes is dual to itself: (.*?);", tex, re.S)
    dual["self_dual"] = [x.replace("$", "").replace("_", "").replace("{", "").replace("}", "").strip()
                         for x in m.group(1).split(",")]
    m = re.search(r"there are four pairs of dual classes: (.*?)\.\s*\\end\{itemize\}", tex, re.S)
    for pair in re.split(r",\s*", m.group(1)):
        a, b_ = [x.replace("$", "").replace("_", "").replace("{", "").replace("}", "").strip() for x in pair.split(" and ")]
        dual["dual_pairs"].append([a, b_])
    return {"source": "M. Donten-Bury, On Kummer 3-folds, arXiv:0812.3758 (LaTeX source kummer.tex); Table 1 (generators), Table 2 (Poincaré polynomials), Proposition on dual classes",
            "matrix_convention": "matrices act on Z^3 (column vectors); A^3 = Z^3 ⊗_Z A (introduction of the paper)",
            "table_order": order_in_table, "classes": classes, "duality": dual}

def burek() -> dict:
    tex = (SRC / "arxiv_2112.03970_tex" / "D.Burek_-_revision.tex").read_text()
    groups = {}
    # Definitions have the form  G_{n.k}\colon\;\; [$$] \left\langle (matrix), (matrix) \right\rangle\simeq <type>
    # (the hyperlinked labels in the list of invariant divisors do not match this form).
    for m in re.finditer(r"G_\{(\d+\.\d)\}\\colon\\;\\;\s*\$*\s*\\left\\langle(.*?)\\right\\rangle\\simeq\s*(\\ZZ_2\\oplus\s*\\ZZ_2|[A-Z]_\{?\d+\}?)(.{0,120})", tex, re.S):
        label, body, iso, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        mats = [parse_array(b) for b in ARRAY.findall(body)]
        assert len(mats) == 2, (label, body)
        iso = iso.replace("\\ZZ_2\\oplus", "Z2+").replace("\\ZZ_2", "Z2").replace(" ", "").replace("{", "").replace("}", "").replace("_", "")
        tahara = re.search(r"the group \$W_\{?(\d+)\}?\$ in Prop\. (\d+) of \\cite\{[Tt]ahara\}", tail)
        entry = {"generators": mats, "isomorphism_type": iso}
        if tahara:
            entry["tahara_label"] = f"W_{tahara.group(1)} in Prop. {tahara.group(2)} of Tahara"
        if label not in groups:
            groups[label] = entry
    assert len(groups) == 16, sorted(groups)
    # Hodge numbers: chains  h^{p,q}(\kum_{3}(E, G_{a.b}))=...=N
    HTERM = re.compile(r"h\^\{([12]),([12])\}(?:\\left)?\(\\kum_\{3\}\(E,\s*G_\{(\d+\.\d)\}\)(?:\\right)?\)")
    ARITH = re.compile(r"[0-9]+(?:\s*\+\s*[0-9]+)*")
    pos = 0
    hodge = {}
    while True:
        m = HTERM.search(tex, pos)
        if not m:
            break
        p, q = m.group(1), m.group(2)
        labels = [m.group(3)]
        i = m.end()
        value = None
        while True:
            j = i
            while j < len(tex) and tex[j] in " \n\t":
                j += 1
            if j < len(tex) and tex[j] == "=":
                j += 1
                while j < len(tex) and tex[j] in " \n\t":
                    j += 1
                mh = HTERM.match(tex, j)
                if mh and (mh.group(1), mh.group(2)) == (p, q):
                    labels.append(mh.group(3)); i = mh.end(); continue
                ma = ARITH.match(tex, j)
                if ma:
                    value = sum(int(x) for x in ma.group(0).replace(" ", "").split("+")); i = ma.end(); continue
            break
        pos = i
        if value is None:
            continue
        key = "h11" if (p, q) == ("1", "1") else "h21"
        for lab in labels:
            hodge.setdefault(lab, {})
            assert hodge[lab].get(key, value) == value, (lab, key, hodge[lab], value)
            hodge[lab][key] = value
    for lab in groups:
        assert lab in hodge and set(hodge[lab]) == {"h11", "h21"}, (lab, hodge.get(lab))
        groups[lab]["h11"] = hodge[lab]["h11"]; groups[lab]["h21"] = hodge[lab]["h21"]
    return {"source": "D. Burek, Zeta function of some Kummer Calabi–Yau 3-folds, arXiv:2112.03970 (LaTeX source); §4 and §5 (Examples), Appendix",
            "matrix_convention": "finite subgroup G of SL_3(Z) acting on E^3 through the endomorphism ring (column vectors)",
            "groups": groups}

def andreatta_wisniewski() -> dict:
    tex = (SRC / "arxiv_0804.4611_tex" / "main.tex").read_text()
    m = re.search(r"The Poincar\\'e polynomial of a crepant resolution of \$A\^3/S_4\$,\s*\$X \\ra A\^3/S_4\$, is\s*\$\$P_X\(t\)=([^$]*)\$\$", tex)
    poly = m.group(1).replace("\\,", "").replace(" ", "").rstrip(".")
    m2 = re.search(r"which have, respectively, \$(\d),\\ (\d),\\ (\d)\$ and (\d) conjugacy classes in\s*\$GL\(3,\\Z\)\$", tex)
    return {"source": "M. Andreatta, J. Wiśniewski, On the Kummer construction, arXiv:0804.4611 (LaTeX source); §4.2 (octahedral group) and Proposition on subgroups of SL(3,Z)",
            "octahedral_S4_poincare_polynomial": poly,
            "octahedral_S4_h11_h21": [20, 6],
            "numbers_of_GL3Z_conjugacy_classes_dihedral_D2a_for_a_2_3_4_6": [int(m2.group(i)) for i in range(1, 5)],
            "A4_classes": 3, "S4_classes": 3}

def main() -> None:
    out = {"donten_bury": donten_bury(), "burek": burek(), "andreatta_wisniewski": andreatta_wisniewski()}
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT.relative_to(ROOT)}")
    for lab, c in out["donten_bury"]["classes"].items():
        print(f"DB {lab:7s} betti={c['betti']} h11={c['h11_from_b2']} h21={c['h21_from_b3']}")
    for lab, g in out["burek"]["groups"].items():
        print(f"Burek G_{lab:5s} {g['isomorphism_type']:6s} h11={g['h11']:2d} h21={g['h21']:2d} {g.get('tahara_label','')}")
    print("AW:", out["andreatta_wisniewski"])
    print("DB duality:", out["donten_bury"]["duality"])

if __name__ == "__main__":
    main()
