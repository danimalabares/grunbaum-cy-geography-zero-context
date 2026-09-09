#!/usr/bin/env python3
"""Write HASH_MANIFEST.json with sha256 of every file in this run directory (excluding itself)."""
import hashlib, json, os
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
for root, _, files in os.walk(RUN):
    for fn in sorted(files):
        p = os.path.join(root, fn); rel = os.path.relpath(p, RUN)
        if rel in ("HASH_MANIFEST.json", ".DS_Store") or "__pycache__" in rel: continue
        out[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
json.dump(out, open(os.path.join(RUN, "HASH_MANIFEST.json"), "w"), indent=1, sort_keys=True)
print("hashed", len(out), "files")
