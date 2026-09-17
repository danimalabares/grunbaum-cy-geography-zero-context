#!/usr/bin/env python3
"""Recover the list of the 35 space groups of Figure 2.8 of Johnson–Burnett–Dunbar,
'Crystallographic Topology and Its Applications' (cached copy in sources/), from
the text layer of the PDF, and compare it with the list under audit.

Run:  python3 scripts/extract_jbd_list.py
Needs: sources/JohnsonEtAl-CrystallographicTopology.pdf (not committed; see
sources/MANIFEST.json for URL and SHA-256) and the `pypdf` package.  If the
cached PDF is absent the script only re-validates data/jbd_figure_2_8_groups.json.
Output: data/jbd_figure_2_8_groups.json
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "sources" / "JohnsonEtAl-CrystallographicTopology.pdf"
OUT = ROOT / "data" / "jbd_figure_2_8_groups.json"

CLAIMED = [16, 17, 21, 22, 24, 89, 90, 91, 93, 95, 97, 98, 149, 150, 151, 153, 155,
           177, 178, 179, 180, 181, 182, 195, 196, 198, 199, 207, 208, 209, 210, 211, 212, 213, 214]

# Hermann–Mauguin symbols of the 65 Sohncke groups, ITA numbering (used to validate labels).
SOHNCKE = {1: "P1", 3: "P2", 4: "P21", 5: "C2", 16: "P222", 17: "P2221", 18: "P21212", 19: "P212121",
    20: "C2221", 21: "C222", 22: "F222", 23: "I222", 24: "I212121", 75: "P4", 76: "P41", 77: "P42",
    78: "P43", 79: "I4", 80: "I41", 89: "P422", 90: "P4212", 91: "P4122", 92: "P41212", 93: "P4222",
    94: "P42212", 95: "P4322", 96: "P43212", 97: "I422", 98: "I4122", 143: "P3", 144: "P31", 145: "P32",
    146: "R3", 149: "P312", 150: "P321", 151: "P3112", 152: "P3121", 153: "P3212", 154: "P3221",
    155: "R32", 168: "P6", 169: "P61", 170: "P65", 171: "P62", 172: "P64", 173: "P63", 177: "P622",
    178: "P6122", 179: "P6522", 180: "P6222", 181: "P6422", 182: "P6322", 195: "P23", 196: "F23",
    197: "I23", 198: "P213", 199: "I213", 207: "P432", 208: "P4232", 209: "F432", 210: "F4132",
    211: "I432", 212: "P4332", 213: "P4132", 214: "I4132"}

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def extract() -> dict:
    from pypdf import PdfReader
    reader = PdfReader(str(PDF))
    pages = [(i + 1, p.extract_text() or "") for i, p in enumerate(reader.pages)]
    # Figure 2.8 is on the page whose text contains its caption.
    cap = "Singular sets for all 35 Euclidean"
    page_no, text = next((n, t) for n, t in pages if cap in t and "Figure 2.8" in t)
    # Labels in the figure are printed as "<number> <HM symbol>" (the symbol may be
    # split by a space, e.g. "F41 32").  Collect number/symbol pairs and validate them
    # against the Sohncke list.
    found = {}
    # Each label occupies its own line(s): "<number>\n<symbol>\n"; a symbol may contain
    # one internal space ("F41 32").  Newlines must not be swallowed into the symbol.
    for m in re.finditer(r"(?<!\d)(\d{1,3})\n([PCFIR][0-9]+(?: [0-9]+)*)(?=\n|$)", text):
        n = int(m.group(1)); sym = m.group(2).replace(" ", "")
        if n in SOHNCKE and SOHNCKE[n] == sym:
            found[n] = sym
    # The label "214 I4132" of the figure is printed on the same page as well.
    text_all = "\n".join(t for _, t in pages)
    ctx = {}
    for kw in ["35 with S3", "Fig. 2.8 shows the singular sets for all 35 Euclidean",
               "12 cubic orientable", "ten orbifolds in the bottom two rows"]:
        i = text_all.find(kw)
        if i >= 0:
            ctx[kw] = re.sub(r"\s+", " ", text_all[max(0, i - 200): i + 260])
    return {"page_of_figure": page_no, "groups": dict(sorted(found.items())), "context": ctx}

def main() -> None:
    if PDF.exists():
        res = extract()
        numbers = sorted(res["groups"])
        out = {
            "source": "C. K. Johnson, M. N. Burnett, W. D. Dunbar, Crystallographic Topology and Its Applications, Figure 2.8 and §2.9 (text layer of the cached PDF)",
            "pdf_sha256": sha256(PDF), "pdf_url": "https://ncatlab.org/nlab/files/JohnsonEtAl-CrystallographicTopology.pdf",
            "page_of_figure_2_8": res["page_of_figure"],
            "numbers_read_from_figure": numbers,
            "hermann_mauguin_read_from_figure": {str(k): v for k, v in res["groups"].items()},
            "count": len(numbers),
            "equals_list_under_audit": numbers == CLAIMED,
            "list_under_audit": CLAIMED,
            "context_quotes": res["context"],
        }
        OUT.write_text(json.dumps(out, indent=1))
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        out = json.loads(OUT.read_text())
        print("cached PDF absent; re-validating the recorded list only")
    print("numbers read:", out["numbers_read_from_figure"])
    print("count:", out["count"], " equals list under audit:", out["equals_list_under_audit"])
    if not out["equals_list_under_audit"] or out["count"] != 35:
        sys.exit("JBD list mismatch")

if __name__ == "__main__":
    main()
