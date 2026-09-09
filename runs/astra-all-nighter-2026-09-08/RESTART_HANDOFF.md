# Restart handoff

**Session finished with verified partial results. No background computation remains. No manageable exact model was obtained.** Read RESULTS.md, FIBRE_AUDIT.md, MODEL.md and NEW_GEOMETRY.md before continuing.

Budget: the user reported two banked resets and authorized at most one, only after current allowance exhaustion. Zero resets were attempted or redeemed by this run. Automatic redemption and balance reading are unavailable; manual activation is required. The second reset is reserved. Never purchase credits, switch accounts, use paid fallback, or retry an ambiguous redemption. BUDGET_STATE.json records the distinction between the user-reported balance and unavailable account verification.

Keep the original safeguards: one arithmetic job, 2,800 MiB process-group RSS, exclusive lock, all four thread controls set to one, unrelated CAS inspection, termination restricted to owned groups. Historical limits remain 2026-09-09 06:00 stop-launch, 06:30 stop-work, 06:45 report, America/Sao_Paulo. A later restart must not silently change the date. Frozen packets and other repositories are read-only. No commits, pushes, settings changes or external messages are authorized.

Completed mathematics:

- The finite fibre passes the targeted audit under the recorded original CAS assumptions. The arbitrary-rational-denominator gap is repaired by integral Hilbert pivots. Global degree of L remains unknown. No new p-adic precision was computed.
- Fifteen distinct isolated reduced (-1,-1) lines exist on the actual fibre, exhaust the facet-transverse reduction class, and persist on an open of the intended component. Boundary lines and the complete line scheme remain open.
- The 123-parameter quadratic raw-generator ansatz with the original first tangent is impossible over every characteristic-zero field. An independent replay verifies 979 row identities and 54 substitutions ending in 1. Degree-three/four/five fixed-jet matrix ansätze are also excluded by exact rational row sums.
- The 178-dependent-coordinate reduction is singular along P2_(b,e,h). This holds for the whole eight-parameter intrinsic slice excluding O2 and O4, with gauge free values zero at every order. Adding O2 or O4 restores all 270 dependent coordinates. A tangent-only vanishing condition does not imply this theorem.
- The local germ XY=t^(2N)W has simply connected regular locus. Global fundamental group and Picard torsion remain open.

Checkpoints and certificates:

- `data/combined_matrix_QQ/`: original 123-parameter system, G2 row certificates, all reverse substitutions, and complete QQ_checkpoint.json.
- `data/degree5_cas/` and `data/linear_unit_verification/`: saved rational systems and exact unit identities. Original failed exporter and timeout evidence are preserved.
- `data/singular_eight_parameter_slice_v3/`, `data/sparse_orbit_extensions/`, and `data/sparse_support_QQ/`: exact forcing, joint support, normal-order identities and universal quadratic map. Earlier v1/v2 failed checks are preserved and superseded by v3.
- `data/line_certificates_all/`, `data/facet_transverse_exhaustion/`: finite line certificates; exact algebraic line definitions and all-orders closure are in `notes/degeneration_lines.md`.

The final entry point is `scripts/reproduce_successes_v2.py`; all twelve checks passed in `data/reproduction_final/`. All 31 guarded jobs ended, and final process inspection found none remaining: `logs/final_state.json`. The source HEAD is still 4f75a9a, status `?? runs/`; both frozen manifests passed. Heap HEAD differs from the supplied preparation baseline, as recorded in `data/source_repositories.json`; no reset was performed.

Best next bounded equation computation: raw degree three with both lower coefficient orders free, using constant-block elimination. Paths in the fixed coordinate slice must activate O2 or O4 at some order. Geometry next: boundary line reductions. Do not repeat the completed sparse fits, graph-ray tests, or unchanged fixed-jet matrix searches.
