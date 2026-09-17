#!/usr/bin/env python3
"""Write HASH_MANIFEST.json for this run directory (excluding the manifest itself)."""
import hashlib, json, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "HASH_MANIFEST.json")
entries = {}
for dp, dn, fn in os.walk(root):
    dn[:] = sorted(d for d in dn if not d.startswith("."))
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        if rel == "HASH_MANIFEST.json" or rel.startswith("."):
            continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        entries[rel] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(p)}
man = {"run": os.path.basename(root),
       "input_commit": "09953cefe987f304e1e8549a50df3b937747470c",
       "files": entries, "count": len(entries)}
with open(out, "w") as fh:
    json.dump(man, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("wrote", out, "with", len(entries), "entries")
