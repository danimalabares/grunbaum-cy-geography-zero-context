# Reproduce the daytime packet

All commands below run from:

```sh
cd /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-daytime-2026-09-08
```

Only this repository is writable. The six source commits and selected
source-file hashes are in SOURCE_MANIFEST.json. No installation is needed:
the Python scripts use the standard library. The inspected local CAS is
Macaulay2 1.20; Singular is used only for a construction/syntax check today.

## Verify before computing

```sh
python3 scripts/record_provenance.py
shasum -a 256 -c ARTIFACT_SHA256SUMS
```

These are read-only checks when the manifests already exist. A changed
HEAD, tracked source edit, input hash or script hash is a provenance gate,
not permission to reset another repository. Resolve it using frozen source
objects and newly named copies, preserving every user change.

## Cheap exact checks

Use one symbolic process at a time. `run_guarded.py` sets all four thread
variables to1, takes an exclusive lock, checks existing CAS processes and
monitors process-group RSS. It needs permission to run `ps`; failure to
monitor prevents launch. The limits below are daytime-safe.

```sh
python3 scripts/run_guarded.py --seconds 120 --memory-mb 1200 --tag reproduce-chart -- python3 scripts/build_fixed_chart.py
python3 scripts/run_guarded.py --seconds 120 --memory-mb 1200 --tag reproduce-sixjet -- python3 scripts/fixed_curve_lift.py --order 6 --prime 101
python3 scripts/run_guarded.py --seconds 120 --memory-mb 1200 --tag reproduce-curve-export -- python3 scripts/export_fixed_curve.py
python3 scripts/run_guarded.py --seconds 90 --memory-mb 1200 --tag reproduce-curve-load -- /usr/local/bin/Singular -q equations/fixed_curve_QQ.sing
python3 scripts/run_guarded.py --seconds 120 --memory-mb 1200 --tag reproduce-hodge-api -- /Applications/Macaulay2-1.20/bin/M2 --script scripts/smoke_hodge_maps.m2
```

The curve-load command constructs the finite incidence ideal only. It
does not compute a standard basis, eliminate variables, or find a point.
The Hodge smoke test uses a tiny unrelated test ideal to check the API;
it computes no Calabi–Yau Hodge number.

For the actual negative polynomial-closure check:

```sh
python3 scripts/run_guarded.py --seconds 120 --memory-mb 1200 --tag reproduce-negative-closure -- python3 scripts/check_rational_closure.py logs/20260908T111640-curve-sixjet-final.artifacts/fixed_curve_p101_order6.json --max-denominator 0
```

Expected result: exact coefficients0 through6 vanish; coefficient7 has
residue37 mod101 in quartic row0/relation column0. **FAILED** polynomial
pair closure is a successful negative regression, not a rejection of
smoothing or of all possible higher syzygies for those generators.

## Evidence already saved

Each stem below has `.json` resource/command metadata, `.stdout`, `.stderr`,
and, when applicable, a matching `.artifacts/` directory.

| Log stem | Check / observed result |
|---|---|
| logs/20260908T104521-fixed-chart |291 orbits, rank270, determinant−1 |
| logs/20260908T111640-curve-sixjet-final |final hashed checkpoint format; all6960 equations through q6;5.0s/27MB |
| logs/20260908T111721-sixjet-polynomial-negative |q7 exact residual;6.3s/25MB |
| logs/20260908T110146-export-curve |finite incidence export;3.7s/23MB |
| logs/20260908T112121-finite-curve-syntax |Singular load,11.1s/328MB, no solve |
| logs/20260908T112551-final-export-regression |corrected exporter reproduces both saved files exactly;2.6s/22MB |
| logs/20260908T105750-hodge-api |degree-zero dual-map smoke test,5.8s/83MB |

The earlier `20260908T105246-curve-sixjet` files predate provenance
hardening. They remain evidence but must not be resumed with the hardened
script. The final checkpoint above includes the input/script hashes and
all normalized source-jet checks. The overnight controller starts fresh
and uses the actual emitted paths when resuming its own order24 run.

`HILBERT_CHEAP_CHECK.txt` and `certificates/lineage_tangent_comparison.json`
record the independent tangent/component calculations. Their scripts are
`check_hilbert_tangent.py` and `compare_lineage_tangents.py`.
`FIXED_CURVE_SCRIPT_REVIEW.md` and its certificate files explain the
solver/closure positive and negative controls. The `fixtures/` directory
contains deliberately singular synthetic families, never usable smoothing
inputs. The public exporter rejects them by its selected-six-jet gate.
`review_export_rendering.py` records the repaired monomial-encoding issue;
the final export regression verifies the repaired JSON against its generator.
Do not use its one-time `--repair-json` option on frozen artifacts.
PDF-rendering helpers and saved pages document the primary-source checks;
they are not part of the symbolic overnight pipeline.

## Night launch and downstream gates

At about21:00 paste OVERNIGHT_PROMPT.md into Astra Ultra. Its initial
executable command is:

```sh
python3 scripts/night_primary.py --run
```

Do **not** run that now. It extends to order24, optionally32, and tests
exact bounded rational closure sequentially. No universal P1 calculation
or ideal-square resolution is launched by the controller.

Only an exact closure model may enter `export_rational_model.py`; its
output is over a finite field, not automatically over Q. Only a separately
certified finite smooth fibre and integral/component bridge may enter
`certify_fibre.m2` and `hodge_from_fibre.m2` with the documented environment
variables. Rational reconstruction and symmetry-reduced elimination have
explicit development gates in HEAVY_QUEUE.md: do not pretend those missing
backup programs already exist. Never evaluate a truncated series at q=1.

The final daytime hash inventory is created by `scripts/hash_run.py`.
After night artifacts are added, verify the existing inventory with
`shasum -c`; do not rerun the freezing script to overwrite it. Create a
separate overnight inventory for new work. No heavy computation was run
to prepare this packet.
