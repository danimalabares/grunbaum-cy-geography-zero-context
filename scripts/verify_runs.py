#!/usr/bin/env python3
"""Verify every run manifest under runs/ against the files actually present.

Each run directory ships its own manifest (a flat `shasum -a 256` file
ARTIFACT_SHA256SUMS, or HASH_MANIFEST.json).  Some manifest-covered files are
deliberately not committed to the public repository; they are listed, with
their recorded SHA-256 and the reason, in runs/PUBLICATION_OMISSIONS.json.

For every manifest entry this script requires: present and hash-identical,
or absent and listed as an omission.  Anything else is a failure.  Files in a
run directory that no manifest covers are reported as extras (not a failure;
caches such as __pycache__, .cas.lock and .DS_Store are ignored).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
OMISSIONS = RUNS / "PUBLICATION_OMISSIONS.json"
IGNORED_PARTS = {"__pycache__", ".DS_Store", ".cas.lock"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(run: Path) -> tuple[str, dict[str, str]]:
    flat = run / "ARTIFACT_SHA256SUMS"
    js = run / "HASH_MANIFEST.json"
    if flat.exists():
        entries = {}
        for line in flat.read_text().splitlines():
            if not line.strip():
                continue
            digest, name = line.split(None, 1)
            entries[name.strip().lstrip("*")] = digest
        return flat.name, entries
    if js.exists():
        data = json.loads(js.read_text())
        files = data.get("files", data)
        entries = {k: (v["sha256"] if isinstance(v, dict) else v) for k, v in files.items()}
        return js.name, entries
    raise SystemExit(f"no manifest in {run}")


def main() -> None:
    omissions = json.loads(OMISSIONS.read_text())["files"] if OMISSIONS.exists() else {}
    failures: list[str] = []
    for run in sorted(p for p in RUNS.iterdir() if p.is_dir()):
        manifest_name, entries = load_manifest(run)
        ok = omitted = 0
        for rel, digest in entries.items():
            path = run / rel
            key = path.relative_to(ROOT).as_posix()
            if path.exists():
                if sha256(path) != digest:
                    failures.append(f"hash mismatch: {key}")
                else:
                    ok += 1
            elif key in omissions:
                if omissions[key]["sha256"] != digest:
                    failures.append(f"omission record disagrees with manifest: {key}")
                omitted += 1
            else:
                failures.append(f"missing and not a recorded omission: {key}")
        covered = set(entries) | {manifest_name}
        extras = [
            p.relative_to(run).as_posix()
            for p in run.rglob("*")
            if p.is_file()
            and not (set(p.relative_to(run).parts) & IGNORED_PARTS)
            and p.relative_to(run).as_posix() not in covered
        ]
        print(f"{run.name}: {manifest_name} entries={len(entries)} present_ok={ok} "
              f"omitted_documented={omitted} extras={len(extras)}")
        for e in extras[:20]:
            print(f"  extra (not manifest-covered): {e}")
    if failures:
        for f in failures:
            print("FAIL", f)
        raise SystemExit("RUN_MANIFESTS_FAILED")
    print("RUN_MANIFESTS_VERIFIED")


if __name__ == "__main__":
    main()
