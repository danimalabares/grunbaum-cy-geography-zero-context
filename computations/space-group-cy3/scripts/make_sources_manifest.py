#!/usr/bin/env python3
"""Create or verify sources/MANIFEST.json: URL, SHA-256, size and retrieval date of every cached
third-party document.  The documents themselves are NOT committed (repository convention for
third-party material, cf. runs/PUBLICATION_OMISSIONS.json); the manifest is.

Run:  python3 scripts/make_sources_manifest.py            (write, needs the cached files)
      python3 scripts/make_sources_manifest.py --verify   (verify the cached files against the manifest)
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
MAN = SRC / "MANIFEST.json"
RETRIEVED = "2026-09-17"

URLS = {
    "JohnsonEtAl-CrystallographicTopology.pdf": "https://ncatlab.org/nlab/files/JohnsonEtAl-CrystallographicTopology.pdf",
}
ARXIV = {"0804.4611": "Andreatta–Wiśniewski, On the Kummer construction",
         "0812.3758": "Donten-Bury, On Kummer 3-folds",
         "2112.03970": "Burek, Zeta function of some Kummer Calabi–Yau 3-folds",
         "1209.3906": "Fischer–Ratz–Torrado–Vaudrevange, Classification of symmetric toroidal orbifolds",
         "1409.7601": "Hashimoto–Kanazawa, Calabi–Yau threefolds of type K (I)",
         "math/9803071": "Batyrev, Non-Archimedean integrals and stringy Euler numbers of log-terminal pairs",
         "math/9908027": "Bridgeland–King–Reid, The McKay correspondence as an equivalence of derived categories",
         "math/0110228": "Yasuda, Twisted jets, motivic measures and orbifold cohomology",
         "math/9903187": "Denef–Loeser, Motivic integration, quotient singularities and the McKay correspondence"}
for aid, title in ARXIV.items():
    n = aid.replace("/", "_")
    URLS[f"arxiv_{n}.pdf"] = f"https://arxiv.org/pdf/{aid}"
    URLS[f"arxiv_{n}_src"] = f"https://arxiv.org/e-print/{aid}"
    URLS[f"arxiv_{n}_abs.html"] = f"https://arxiv.org/abs/{aid}"

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def build() -> dict:
    files = {}
    for name, url in sorted(URLS.items()):
        p = SRC / name
        if not p.exists():
            raise SystemExit(f"missing cached file {p}")
        files[name] = {"url": url, "sha256": sha256(p), "bytes": p.stat().st_size, "retrieved": RETRIEVED}
    for aid, title in ARXIV.items():
        n = aid.replace("/", "_")
        files[f"arxiv_{n}_src"]["title"] = title
    return {"about": "Third-party documents cached locally for this audit. Not committed (repository convention for third-party material); "
                     "listed here with URL and SHA-256 so that the cache can be re-created and verified. The *_tex directories are the "
                     "unpacked e-print sources and *.txt files are text layers extracted with pypdf; both derive from the listed files.",
            "bilbao_note": "The Bilbao Crystallographic Server (GENPOS) could not be read programmatically (human-verification wall on 2026-09-17); "
                           "the crystallographic data were therefore taken from two independent ITA-derived databases (spglib 2.7.0 Hall-symbol "
                           "database; GAP 4.14.0 packages Cryst 4.1.27 / CrystCat 1.1.10) and cross-checked against each other.",
            "files": files}

def main() -> None:
    if "--verify" in sys.argv:
        man = json.loads(MAN.read_text())
        bad = []
        for name, rec in man["files"].items():
            p = SRC / name
            if not p.exists():
                bad.append(f"missing {name}")
            elif sha256(p) != rec["sha256"]:
                bad.append(f"sha256 mismatch {name}")
        if bad:
            raise SystemExit("SOURCES_MANIFEST_MISMATCH: " + "; ".join(bad))
        print(f"SOURCES_MANIFEST_VERIFIED ({len(man['files'])} files)")
    else:
        man = build()
        MAN.write_text(json.dumps(man, indent=1))
        print(f"wrote {MAN.relative_to(ROOT)} ({len(man['files'])} files)")

if __name__ == "__main__":
    main()
