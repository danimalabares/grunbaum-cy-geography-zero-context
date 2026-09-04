#!/usr/bin/env python3
"""Create or verify the deterministic SHA-256 manifest of this workspace."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "computations" / "SHA256SUMS"


def entries() -> list[tuple[str, str]]:
    result = []
    for path in sorted(ROOT.rglob("*")):
        rel_path = path.relative_to(ROOT)
        if ".git" in rel_path.parts or not path.is_file() or path == MANIFEST:
            continue
        rel = rel_path.as_posix()
        result.append((hashlib.sha256(path.read_bytes()).hexdigest(), rel))
    return result


def rendered() -> str:
    return "".join(f"{digest}  {name}\n" for digest, name in entries())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.verify:
        if not MANIFEST.exists() or MANIFEST.read_text() != expected:
            raise SystemExit("WORKSPACE_MANIFEST_MISMATCH")
        print("WORKSPACE_MANIFEST_VERIFIED")
    else:
        MANIFEST.parent.mkdir(exist_ok=True)
        MANIFEST.write_text(expected)
        print(f"WROTE {MANIFEST.relative_to(ROOT)} with {len(entries())} entries")


if __name__ == "__main__":
    main()
