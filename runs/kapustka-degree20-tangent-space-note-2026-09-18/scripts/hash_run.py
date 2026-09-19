#!/usr/bin/env python3
"""Write HASH_MANIFEST.json for this run directory (excluding the manifest itself and TeX byproducts)."""
import hashlib, json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "HASH_MANIFEST.json")
SKIP_EXT = {".aux", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz"}
entries = {}
for dp, dn, fn in os.walk(root):
    dn[:] = sorted(d for d in dn if not d.startswith("."))
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        if rel == "HASH_MANIFEST.json" or rel.startswith(".") or os.path.splitext(f)[1] in SKIP_EXT:
            continue
        if rel == "DANI_NOTE.log":
            continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        entries[rel] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(p)}
man = {"run": os.path.basename(root),
       "input_commit": "ff3c5040257cca9161dbb76795b7d9a240f31374",
       "files": entries, "count": len(entries)}
with open(out, "w") as fh:
    json.dump(man, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("wrote", out, "with", len(entries), "entries")
