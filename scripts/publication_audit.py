#!/usr/bin/env python3
"""Fail on common publication hazards anywhere in the workspace."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_GITHUB_FILE_SIZE = 100 * 1024 * 1024
FORBIDDEN_NAMES = {
    ".DS_Store", ".env", ".env.local", "id_rsa", "id_ed25519",
    "credentials", "cookies", "history", "session", "transcript",
}
FORBIDDEN_SUFFIXES = {".key", ".pem", ".p12", ".pfx", ".swp", ".tmp", ".bak"}

# Assemble sensitive literals so this audit does not flag its own source.
SECRET_PATTERNS = {
    "private-key-block": re.compile(r"BEGIN " + r"(?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    "github-token": re.compile(r"github" + r"_pat_[A-Za-z0-9_]{20,}|gh" + r"[pousr]_[A-Za-z0-9_]{20,}"),
    "aws-access-key": re.compile(r"A" + r"(?:KI|SI)A[0-9A-Z]{16}"),
    "google-api-key": re.compile(r"AI" + r"za[0-9A-Za-z_-]{30,}"),
    "bearer-token": re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    "credential-assignment": re.compile(
        r"(?i)(?:password|passwd|api[_-]?key|client[_-]?secret)\s*[:=]\s*[\"'][^\"']{4,}"
    ),
}
MACHINE_PATH_PATTERNS = {
    "mac-user-path": re.compile(r"/" + r"Users/[A-Za-z0-9._-]+/"),
    "linux-home-path": re.compile(r"/" + r"home/[A-Za-z0-9._-]+/"),
    "mac-private-var": re.compile(r"/private/" + r"var/"),
    "mac-var-folders": re.compile(r"/var/" + r"folders/"),
    "local-file-uri": re.compile(r"file:" + r"//"),
}


def workspace_files() -> list[Path]:
    return [
        item for item in sorted(ROOT.rglob("*"))
        if item.is_file() and ".git" not in item.relative_to(ROOT).parts
    ]


def main() -> None:
    problems: list[str] = []
    files = workspace_files()
    max_size = 0
    max_name = ""

    for item in sorted(ROOT.rglob("*")):
        if ".git" in item.relative_to(ROOT).parts:
            continue
        if item.is_symlink():
            problems.append(f"symlink: {item.relative_to(ROOT)}")

    for item in files:
        rel = item.relative_to(ROOT).as_posix()
        size = item.stat().st_size
        if size > max_size:
            max_size, max_name = size, rel
        if size >= MAX_GITHUB_FILE_SIZE:
            problems.append(f"GitHub-size-limit: {rel} ({size} bytes)")
        if item.name in FORBIDDEN_NAMES or item.suffix.lower() in FORBIDDEN_SUFFIXES or item.name.endswith("~"):
            problems.append(f"temporary-or-private-name: {rel}")
        raw = item.read_bytes()
        if b"\x00" in raw:
            problems.append(f"binary-or-NUL: {rel}")
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"non-UTF8: {rel}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                problems.append(f"{label}: {rel}")
        for label, pattern in MACHINE_PATH_PATTERNS.items():
            if pattern.search(content):
                problems.append(f"{label}: {rel}")

    licenses = [item.relative_to(ROOT).as_posix() for item in files if item.name.upper().startswith("LICENSE")]
    if problems:
        print("PUBLICATION_AUDIT_FAILED")
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("PUBLICATION_AUDIT_PASSED")
    print(f"files_inspected={len(files)}")
    print(f"largest_file={max_name}")
    print(f"largest_file_bytes={max_size}")
    print(f"license_files={licenses}")


if __name__ == "__main__":
    main()
