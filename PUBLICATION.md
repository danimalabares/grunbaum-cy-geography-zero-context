# Publication-readiness record

Publication target: `danimalabares/grunbaum-cy-geography-zero-context`.

## Pre-publication backup

- Location: `/private/tmp/grunbaum-cy-geography-zero-context-pre-publication-20260904T194805Z.tar.gz`
- SHA-256: `0bc2eb029b7303dc7977f2811727abe8e0b22efe7eb272374f1845f844b9a5ac`
- Size: 180 KiB
- Scope: the complete workspace before publication-safe edits and before Git initialization

The archive was listed successfully after creation. It contains all 53 files
then present in the workspace, including equations, computation outputs,
reports, ledgers, scripts, the prior SHA-256 manifest, and failed-computation
records.

## Publication-safe changes

- Replaced personal absolute source paths in scripts and records with the
  sibling default `../grunbaum-zero-context-proof` and the configurable
  environment variable `GS_ZERO_CONTEXT_SOURCE`.
- Strengthened the README disclaimer and the hypotheses on the local-Hilbert
  and known-family comparison.
- Added a deterministic whole-workspace publication audit and `.gitignore` for
  future transient editor, Python-cache, and environment files.
- Preserved every mathematical equation, certificate hash, computation log,
  failed computation, provenance commit/tree, and claim ledger entry.

No existing research file was excluded or removed. No credential, secret,
private key, session transcript, non-UTF-8 file, symlink, or oversized file is
part of the publication set.

## License

No license is present, and none was added during publication preparation.

## 2026-09-09 addendum — historical runs

- Committed: `runs/astra-daytime-2026-09-08`, `runs/astra-computation-2026-09-08`, `runs/astra-all-nighter-2026-09-08`, `runs/cp2-nine-vertex-equivariant-t2-2026-09-09`, excluding `__pycache__`, `.cas.lock` and `.DS_Store`.
- Not committed but published as a Release asset: 1431 large search-checkpoint files (`runs/PUBLICATION_OMISSIONS.json`, disposition `release-asset`).
- Withheld: a machine process listing (`logs/environment.json`), a session budget file (`BUDGET_STATE.json`), one compiled binary (`artifacts/render_lineage_pdf`; sources published) and three rendered pages of third-party documents (disposition `withheld`).
- The historical runs' frozen metadata contains absolute paths of the original machine; they were not rewritten. `scripts/publication_audit.py` now reports, rather than enforces, the machine-path check for those three directories, skips the omitted files and local caches, and still enforces the secret, size, binary and file-name checks everywhere.
- Run documents also name the author's collaborators and a meeting date in planning notes (`OVERNIGHT_PROMPT.md`, `FRIDAY_*BRIEF*.md`). These were kept as part of the frozen record.
