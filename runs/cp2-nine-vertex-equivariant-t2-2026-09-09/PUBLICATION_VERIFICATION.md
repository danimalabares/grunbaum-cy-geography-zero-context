# Publication verification pass — 2026-09-09

Independent re-run of the shipped verifiers before publishing this run. Nothing outside the run
directory was read except `../grunbaum-zero-context-proof` (not needed by these scripts). The
unfinished optional quadratic-obstruction cross-check (`scripts/quadric_rank_check.m2`) was **not**
restarted; the results below do not depend on it.

Environment: macOS (Darwin 21.6), Macaulay2 1.20 with VersalDeformations 3.0, Python 3.11.4.

## Pre-check

`HASH_MANIFEST.json` (37 entries) matched every file in the run directory before this pass began
(0 mismatches). `data/` and `certificates/` were snapshotted before the re-runs.

## Commands re-run, in order, all exit 0

| command | decisive output |
|---|---|
| `python3 -B scripts/verify_input.py` | `f_vector [9, 36, 84, 90, 36]`, `minimal_nonfaces_by_size {4: 36}`, `G_order 6`, `G_is_S3 True`, `Aut_order 54`, `G_equals_full_stabiliser_of_vertex_9 True`, `INPUT_VERIFIED` |
| `M2 --script scripts/t2_dims.m2` | `T1_shape 36×93`, `T2_shape 90×126`, Hilbert numerator `1+4T+10T²+20T³−T⁴+2T⁵`, `DIMS_DONE` |
| `python3 -B scripts/verify_certificate.py Aut54_generators 54` | `group_order 54`, `representation_property_all_pairs_T2 True`, `dim_T2_0_invariants 0`, `dim_T1_0_invariants 5`, `CERTIFICATE_REVERIFIED` |
| `M2 --script scripts/coordinate_orbit.m2 data/orbitals_Aut54.txt` | `coordinate_orbit_dimension_in_T1_0 72`, `dimT1_0 93`, `invariant_coordinate_directions_in_T1_0 3`, `COORDINATE_ORBIT_DONE` |
| `M2 --script scripts/coordinate_orbit.m2 data/orbitals_G_S3.txt` | `coordinate_orbit_dimension_in_T1_0 72`, `invariant_coordinate_directions_in_T1_0 17`, `COORDINATE_ORBIT_DONE` |
| `python3 -B scripts/verify_certificate.py G_S3 6` | `group_order 6`, `representation_property_all_pairs_T2 True`, `dim_T2_0_invariants 14`, `dim_T1_0_invariants 23`, `CERTIFICATE_REVERIFIED` |

Character data printed by both certificate re-verifications agreed with `RESULTS.md` §2 and §6.

## Post-check

After the re-runs, `diff -r` of `data/` and `certificates/` against the snapshot reported no
differences: every regenerated output file (`data/*.json`, `certificates/*_python_reverification.json`,
`certificates/*_coordinate_orbit_coords.txt`) is byte-identical to the shipped one.

## Derived numbers checked by hand

- Intrinsic graded cotangent: `93 − 72 = 21`.
- `Aut(Δ)`-invariant intrinsic directions: `5 − 3 = 2`; `G`-invariant intrinsic directions: `23 − 17 = 6`.
  (For a finite group in characteristic 0 the invariants functor is exact, so invariants of a
  quotient are the quotient of invariants.)
- `S_3` character check: `(126 + 3·(−12) + 2·(−3))/6 = 14` and `(93 + 3·9 + 2·9)/6 = 23`.
- Order-54 character check: `(126 − 9·12 − 6·3)/54 = 0` and `(93 + 9·9 + 6·9 + 14·3)/54 = 5`.

## Not re-run

- The Macaulay2 construction of the certificates (`scripts/equivariant_t2.m2`, ~2 min per group).
  The shipped certificates were instead re-verified independently in exact rational arithmetic by
  `verify_certificate.py`, which is the intended independent check.
- `scripts/quadric_rank_check.m2` (optional, unfinished, not needed).

## Text corrections made to `RESULTS.md` in this pass

Marked inline with **[corrected 2026-09-09]**; numerical content unchanged. The original text is
recoverable from the Git history of this file. Summary: embedded `Hom_S(I,A)₀` (93) distinguished
from intrinsic `T¹(A/QQ)₀` (21); removed the claim that no `S_3`-equivariant all-orders deformations
were established (the `Aut(Δ)`-equivariant ones are `S_3`-equivariant); `Proj` of the flat graded
families gives flat projective families, while identifying the whole Hilbert functor stays open;
explicit statement that no explicit two-parameter family and no smooth generic fibre is claimed.
