# Proof index

Every mathematical result held in this repository, with its statement, where the
argument or computation lives, the certificates behind it, how to reproduce it,
and its status. Status words are those used by the documents themselves and are
**not** upgraded here:

- **established / COMPUTER-CERTIFIED** — exact computation reproduced in this workspace, with certificate files.
- **PROVED (within a stated trust boundary)** — a written derivation whose hypotheses include results accepted from the source packet (typically its all-orders equivariant lift and its Singular smoothness certificates). Qualified-human verification is not claimed anywhere in this repository.
- **CONDITIONAL** — a deduction that is correct given an explicitly named unverified input.
- **OPEN / not established** — no argument is offered.
- **FAILED / REJECTED** — an approach that was tried and shown not to work, kept as a negative result.

Two different objects appear. The **sphere problem** concerns the Stanley–Reisner
ring of the Grünbaum–Sreedharan eight-vertex 3-sphere, its `X ⊂ P⁷` and the claimed
smooth degree-20 Calabi–Yau threefold. The **CP²₉ calculation** concerns the nine-vertex
triangulation of `CP²`, a non-Cohen–Macaulay fourfold in `P⁸`; it borrows only a lemma
and says nothing about the threefold.

## 0. External sources (read-only, hash-locked)

| Repository | Commit | Role | Public link |
|---|---|---|---|
| `grunbaum-zero-context-proof` | `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b` (tag `ultra-01-original`) | the zero-context proof packet; the *only* mathematical authority used | [tree](https://github.com/danimalabares/grunbaum-zero-context-proof/tree/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b) · [FINAL.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/FINAL.md) · [PROOF.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/PROOF.md) · [FORMAL_SMOOTHING_THEOREM.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/FORMAL_SMOOTHING_THEOREM.md) · [EQUIVARIANT_FORMAL_LIFT.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/deformation/EQUIVARIANT_FORMAL_LIFT.md) · [INTEGRAL_EQUIVARIANT_LIFT.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/deformation/INTEGRAL_EQUIVARIANT_LIFT.md) · [FORMAL_ALGEBRAIZATION.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/enumerate/FORMAL_ALGEBRAIZATION.md) · [GENERIC_SMOOTHNESS_AUDIT.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/GENERIC_SMOOTHNESS_AUDIT.md) |
| `grunbaum-zero-context-proof-fable-max-audit` | `9310cd9e3316c69f129d5588d65f0b91f37365b7` | independent hostile audit of the packet; part of the "accepted trust boundary" named by the 2026-09-08 runs | [tree](https://github.com/danimalabares/grunbaum-zero-context-proof-fable-max-audit/tree/9310cd9e3316c69f129d5588d65f0b91f37365b7) |
| `sr-project` | `ff2afbbb7a8b18e7c054d16292df8db02ca87f5c` (branch `restructure`) | the **distinct** DGLA proof variant; consulted only for a tangent-class comparison, never as an input | [PROOF_DGLA.pdf](https://github.com/danimalabares/sr-project/blob/ff2afbbb7a8b18e7c054d16292df8db02ca87f5c/proofs/grunbaum-smoothing/fable-dgla-only/PROOF_DGLA.pdf) |
| `grunbaum-cy-geography-fable-dgla` | `3f7ef3da88fe963e10001fc66cbff4153d5fcb27` | older tangent/link data of the DGLA lineage; comparison only | [tree](https://github.com/danimalabares/grunbaum-cy-geography-fable-dgla/tree/3f7ef3da88fe963e10001fc66cbff4153d5fcb27) |
| `heap-project` | `73c8d1df1d9800425fc2ce18870c25853ea4e9f5` (drifted to `5ea857c8139530a68f3d040b35ffc3e061130152` by the night run) | the author's background notes; "learning context, not mathematical authority" | [tree](https://github.com/danimalabares/heap-project/tree/73c8d1df1d9800425fc2ce18870c25853ea4e9f5) |

All six commits were confirmed present on GitHub on 2026-09-09. The packet's two oversized Singular
modules are in no Git history; see the packet's own [LARGE_FILES.md](https://github.com/danimalabares/grunbaum-zero-context-proof/blob/ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b/LARGE_FILES.md). Nothing in
this repository reads them. The zero-context lineage and the DGLA lineage are **not identified**:
claim D15 below shows their first-order tangent classes are inequivalent.

## 1. Sphere problem — core workspace (2026-09-04)

Reproduce this section with `python3 scripts/run_checks.py` (about 5 minutes; needs Macaulay2 1.20 and
the source checkout as `../grunbaum-zero-context-proof` or `GS_ZERO_CONTEXT_SOURCE`), then
`python3 scripts/make_manifest.py --verify`. Claim ids are those of
[`ledger/CLAIMS.yaml`](ledger/CLAIMS.yaml); dependency order is in
[`ledger/DEPENDENCIES.md`](ledger/DEPENDENCIES.md).

| Id | Statement | Proof / computation | Certificates | Status |
|---|---|---|---|---|
| DEF-001 | `normalMatrix({0},F0)` is 16 × 109: the embedded graded tangent space has dimension 109 | [`scripts/extract_deformation.m2`](scripts/extract_deformation.m2) | [`equations/tangent_basis.md`](equations/tangent_basis.md), [`computations/extract_deformation.stdout.txt`](computations/extract_deformation.stdout.txt) | established |
| DEF-002 | The coordinate orbit has dimension 56; the listed 53 columns are its complement | [`scripts/verify_coordinate_split.m2`](scripts/verify_coordinate_split.m2) | [`computations/verify_coordinate_split.stdout.txt`](computations/verify_coordinate_split.stdout.txt) | established |
| DEF-003 | The ten `S₃`-orbits with weights 1..10 give the stated 53-vector and the sixteen cubics `g_i` | [`reports/DEFORMATION_EQUATIONS.md`](reports/DEFORMATION_EQUATIONS.md) | [`equations/deformation_data.json`](equations/deformation_data.json), [`equations/first_order.md`](equations/first_order.md) | established |
| DEF-004 | The recomputed `g_i` equal the `q`-coefficients of the packet's stored equivariant six-jet | same | [`computations/extract_deformation.stdout.txt`](computations/extract_deformation.stdout.txt), [`equations/six_jet.tsv`](equations/six_jet.tsv) | established |
| DEF-005 | The packet gives an explicit six-jet, an abstract all-orders lift and an existential algebraization, but **no finite explicit algebraic smoothing**; its quarantined order-4 truncation is nonflat (dimension 0, degree 567 over `F₁₀₁`) | [`reports/DEFORMATION_EQUATIONS.md`](reports/DEFORMATION_EQUATIONS.md), [`scripts/verify_failed_truncation.m2`](scripts/verify_failed_truncation.m2) | [`computations/failed_truncation.stdout.txt`](computations/failed_truncation.stdout.txt), [`computations/explicitness.stdout.txt`](computations/explicitness.stdout.txt) | established (explicitness boundary) |
| GEO-001 | Special fibre: degree 20, Hilbert polynomial `(10/3)m³ + (14/3)m`, resolution (1,16,30,16,1) | [`scripts/verify_geography.m2`](scripts/verify_geography.m2), [`scripts/verify_formulas.py`](scripts/verify_formulas.py) | [`computations/geography.stdout.txt`](computations/geography.stdout.txt) | established |
| GEO-002 | Local embedded Hilbert dimension at the Stanley–Reisner point ≤ 94 | [`scripts/verify_full_kuranishi.m2`](scripts/verify_full_kuranishi.m2) | [`computations/full_kuranishi.stdout.txt`](computations/full_kuranishi.stdout.txt) | established, **conditional** on the VersalDeformations package returning the complete order-two obstruction equations |
| GEO-003 | Any smooth nearby fibre has `K = 0`, `H³ = 20`, `c₂·H = 56`, complete `|H|` embedding | [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md) | derivation | established, **hypothesis: a smooth fibre exists** |
| GEO-004 | Every smooth fibre on a component through the point has `h²¹ ≤ 31` | [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md) | derivation | established given GEO-002, GEO-003 |
| GEO-005 | `H` is primitive | [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md) | derivation | established |
| LIT-001 | The known determinantal degree-20 family with Hodge pair (2,34) and Hilbert dimension 97 cannot contain this point | [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md), [`reports/LITERATURE_SOURCES.md`](reports/LITERATURE_SOURCES.md) | primary source arXiv:1609.01195 | established, same condition as GEO-002 |
| OPEN-001 | Exact Hodge numbers, Picard group, fundamental group, rational liaison | [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md) | — | **unresolved** in the core workspace (partly addressed, under a trust boundary, in §3) |

Failed development attempts and the negative control are kept in
[`computations/DEVELOPMENT_FAILURES.md`](computations/DEVELOPMENT_FAILURES.md).

## 2. Sphere problem — daytime run (2026-09-08)

Directory [`runs/astra-daytime-2026-09-08/`](runs/astra-daytime-2026-09-08/). Read
[`DAYTIME_REPORT.md`](runs/astra-daytime-2026-09-08/DAYTIME_REPORT.md) first; the atomic ledger is
[`CLAIM_LEDGER.md`](runs/astra-daytime-2026-09-08/CLAIM_LEDGER.md) (claims D01–D17). Inputs and the six
source commits: [`SOURCE_MANIFEST.json`](runs/astra-daytime-2026-09-08/SOURCE_MANIFEST.json). Integrity:
`ARTIFACT_SHA256SUMS` (100 files). Reproduction: [`REPRODUCE.md`](runs/astra-daytime-2026-09-08/REPRODUCE.md)
(its commands are written for the original machine; run them from the run directory. Its guarded runner
is tied to the 2026-09-08 daytime window and refuses to launch afterwards, by design.)

| Id | Statement | Proof / computation | Certificates | Status (as recorded) |
|---|---|---|---|---|
| D01 | An `A₁₀₁`-integral equivariant smoothing with the prescribed six-jet exists | accepted from the packet | packet certificates | **CONDITIONAL** (accepted trust boundary) |
| D02 | 291 normalized invariant cubic coefficients; 270 independent equations; a 270 × 270 minor of determinant −1 | [`FIXED_CHART.md`](runs/astra-daytime-2026-09-08/FIXED_CHART.md), `scripts/build_fixed_chart.py` | [`data/fixed_chart.json`](runs/astra-daytime-2026-09-08/data/fixed_chart.json) | COMPUTER-CERTIFIED |
| D03 | The full Schur equations give the fixed Hilbert completion | [`FIXED_CHART.md`](runs/astra-daytime-2026-09-08/FIXED_CHART.md) | — | PROVED |
| D04 | Selected 270 and full 6960 equations have the same 21-dimensional local germ | [`FIXED_CHART.md`](runs/astra-daytime-2026-09-08/FIXED_CHART.md) | D02 + accepted `T²^G = 0` | PROVED (uses the accepted invariant unobstructedness) |
| D05 | The displayed finite pointed curve has smooth geometric generic fibre | [`FIXED_CHART.md`](runs/astra-daytime-2026-09-08/FIXED_CHART.md) | [`equations/fixed_curve_QQ.sing`](runs/astra-daytime-2026-09-08/equations/fixed_curve_QQ.sing), `.json` | **CONDITIONAL** on D01 |
| D06 | A particular finite-`q` smooth fibre with manageable exact coefficients | — | — | OPEN in this run (see C06 in §3) |
| D07 | `h⁰(N) = 63 + h²¹`, `h¹¹ = 1 + h³(I²)`, `h²¹ = h⁴(I²) − 64` | [`PICARD_HODGE_PLAN.md`](runs/astra-daytime-2026-09-08/PICARD_HODGE_PLAN.md) | — | PROVED |
| D08 | `Pic(X_M) = ZH` and Pic of the complete DVR total space is `ZH` | [`PICARD_HODGE_PLAN.md`](runs/astra-daytime-2026-09-08/PICARD_HODGE_PLAN.md) | — | PROVED |
| D09 | No DVR smoothing total space is `Q`-factorial; vertical class rank 19 | [`PICARD_VERTICAL_CLASS_OBSTRUCTION.md`](runs/astra-daytime-2026-09-08/PICARD_VERTICAL_CLASS_OBSTRUCTION.md) | — | PROVED ("pending independent human review") |
| D10 | Geometric generic Picard rank = 1 | — | — | OPEN in this run (settled under a trust boundary in §3, C05) |
| D11 | The actual tangent lies uniquely in the top `P1³` stratum | [`HILBERT_EXPLANATION.md`](runs/astra-daytime-2026-09-08/HILBERT_EXPLANATION.md) | 45-minor check | COMPUTER-CERTIFIED + PROVED |
| D12 | Local Hilbert dimension ≤ 94 and `h²¹ ≤ 31` | as GEO-002/GEO-004 | — | CONDITIONAL |
| D13 | The smoothing component has dimension exactly 94 | — | — | OPEN in this run (settled under a trust boundary in §3, C05) |
| D14 | The determinantal degree-20 family has (2,34), Hilbert dimension 97 | [`LINKAGE_TRIAGE.md`](runs/astra-daytime-2026-09-08/LINKAGE_TRIAGE.md), literature | primary source | PROVED |
| D15 | Old (DGLA) and new (zero-context) tangent classes are projectively equivalent | [`LINEAGE_COMPARISON.md`](runs/astra-daytime-2026-09-08/LINEAGE_COMPARISON.md) | six exact transport matrices | **FAILED** — the statement is false at tangent level |
| D16 | Old and new arcs lie on the same completed Hilbert component | — | — | OPEN |
| D17 | A useful low-degree rational second complete-intersection link exists | [`LINKAGE_TRIAGE.md`](runs/astra-daytime-2026-09-08/LINKAGE_TRIAGE.md) | existing certificate | OPEN (first distinct link has degree ≥ 47) |

Frozen discovery snapshots made *before* literature was consulted:
[`HILBERT_DISCOVERY_FREEZE.md`](runs/astra-daytime-2026-09-08/HILBERT_DISCOVERY_FREEZE.md),
[`PICARD_HODGE_DISCOVERY.md`](runs/astra-daytime-2026-09-08/PICARD_HODGE_DISCOVERY.md). Independent
targeted reviews (no script executed by the reviewer):
[`FIXED_CHART_REVIEW.md`](runs/astra-daytime-2026-09-08/FIXED_CHART_REVIEW.md),
[`FIXED_CURVE_SCRIPT_REVIEW.md`](runs/astra-daytime-2026-09-08/FIXED_CURVE_SCRIPT_REVIEW.md).

## 3. Sphere problem — computation run (2026-09-08)

Directory [`runs/astra-computation-2026-09-08/`](runs/astra-computation-2026-09-08/). Read
[`COMPUTATION_RESULTS.md`](runs/astra-computation-2026-09-08/COMPUTATION_RESULTS.md) (ledger C01–C07 near its
end). Inputs: [`inputs/SOURCE_MANIFEST.json`](runs/astra-computation-2026-09-08/inputs/SOURCE_MANIFEST.json)
and a frozen copy of the daytime manifest. Integrity: `ARTIFACT_SHA256SUMS` (1943 files; 1431 large
search-checkpoint files live in the Release asset, see §6). Reproduction:
[`REPRODUCE.md`](runs/astra-computation-2026-09-08/REPRODUCE.md). The two small independent checks run
directly from the run directory with Python 3 only and were re-run on 2026-09-09 with identical output:

```sh
GS_RUN_OUTPUT=/some/fresh/dir python3 -B scripts/verify_product_minor.py
GS_RUN_OUTPUT=/some/fresh/dir python3 -B scripts/verify_ramified_export.py
```

| Id | Statement | Proof / computation | Certificates | Status (as recorded) |
|---|---|---|---|---|
| C01 | The prepared curve jet satisfies all equations through order 32 | [`EXECUTION_RECORD.md`](runs/astra-computation-2026-09-08/EXECUTION_RECORD.md) | guarded logs under `logs/` | COMPUTER-CERTIFIED |
| C02 | The bounded common rational ansatz closes | [`SPARSE_THREE_ORBIT_ATTEMPT.md`](runs/astra-computation-2026-09-08/SPARSE_THREE_ORBIT_ATTEMPT.md), [`SPARSE_DIRECTION_REJECTED.md`](runs/astra-computation-2026-09-08/SPARSE_DIRECTION_REJECTED.md) | exact inconsistent systems | **FAILED** (no nonexistence claim outside the bounds) |
| C03 | `h¹¹ = 1748 + h⁰(N) − dim(I²)₈` | [`DEGREE8_PICARD_FORMULA.md`](runs/astra-computation-2026-09-08/DEGREE8_PICARD_FORMULA.md), [review](runs/astra-computation-2026-09-08/DEGREE8_FORMULA_INDEPENDENT_REVIEW.md) | — | PROVED, conditional on a smooth fibre with the self-dual resolution |
| C04 | `dim(I(q)²)₈ ≥ 1841` via an explicit integer 12 × 12 minor of determinant `−3³·8⁹` | [`PRODUCT_RANK_CERTIFICATE.md`](runs/astra-computation-2026-09-08/PRODUCT_RANK_CERTIFICATE.md) | [`certificates/independent_product_minor.json`](runs/astra-computation-2026-09-08/certificates/independent_product_minor.json) | COMPUTER-CERTIFIED (re-run 2026-09-09, identical) |
| C05 | `(h¹¹, h²¹) = (1, 31)`, `ρ = 1`, `χ = −60`, smoothing component of dimension 94, `Pic/torsion = ZH` | [`GEOGRAPHY_THEOREM.md`](runs/astra-computation-2026-09-08/GEOGRAPHY_THEOREM.md) | C03 + C04 + accepted `h⁰(N) ≤ 94` | **PROVED within the accepted zero-context smoothing trust boundary**; torsion and `π₁` open |
| C06 | A specified smooth closed fibre over a number field `L ⊂ Q₁₀₁(π)`, `π⁷ = 101`, with all sixteen cubics displayed | [`RAMIFIED_FIBRE_EQUATIONS.md`](runs/astra-computation-2026-09-08/RAMIFIED_FIBRE_EQUATIONS.md), [`RAMIFIED_POINT_CONSTRUCTION.md`](runs/astra-computation-2026-09-08/RAMIFIED_POINT_CONSTRUCTION.md), [`RAMIFIED_FLATNESS_IDENTITY.md`](runs/astra-computation-2026-09-08/RAMIFIED_FLATNESS_IDENTITY.md), [review](runs/astra-computation-2026-09-08/RAMIFIED_POINT_REVIEW.md) | [`data/ramified_fibre_coefficients.json`](runs/astra-computation-2026-09-08/data/ramified_fibre_coefficients.json), independent export check (re-run 2026-09-09, identical) | **PROVED within the accepted boundary**; a finite algebraic presentation, not a truncated family |
| C07 | A compact primitive-element presentation of the coefficient field | [`BOUNDED_FIELD_SEARCH.md`](runs/astra-computation-2026-09-08/BOUNDED_FIELD_SEARCH.md) | LLL checkpoints (Release asset) | **OPEN**; the bounded search FAILED, no non-membership theorem |
| — | Three truncated-generator candidates are nonflat | [`TRUNCATED_GENERATOR_REJECTIONS.md`](runs/astra-computation-2026-09-08/TRUNCATED_GENERATOR_REJECTIONS.md) | exact | COMPUTER-CERTIFIED (negative) |

## 4. Sphere problem — overnight run (2026-09-08/09)

Directory [`runs/astra-all-nighter-2026-09-08/`](runs/astra-all-nighter-2026-09-08/). Read
[`RESULTS.md`](runs/astra-all-nighter-2026-09-08/RESULTS.md); headline: **no manageable new exact
polynomial model was obtained.** Detailed proofs are the notes under
[`notes/`](runs/astra-all-nighter-2026-09-08/notes/). Jobs J001–J031:
[`JOBS.md`](runs/astra-all-nighter-2026-09-08/JOBS.md), `RUN_LOG.jsonl`. Integrity: `HASH_MANIFEST.json`
(270 files; two withheld, see §6). Reproduction: [`REPRODUCE.md`](runs/astra-all-nighter-2026-09-08/REPRODUCE.md),
one entry point running twelve finite checks in about 32 s. Its guard is deliberately tied to the
2026-09-09 06:00 (America/Sao_Paulo) session window and refuses to launch afterwards ("Session
computation cutoff reached", confirmed 2026-09-09). The recorded passing run is
[`data/reproduction_final/`](runs/astra-all-nighter-2026-09-08/data/reproduction_final/).

| Statement | Proof / computation | Certificates | Status (as recorded) |
|---|---|---|---|
| The inherited finite fibre (C06) passes a targeted audit; a genuine local-denominator gap is repaired by integral Hilbert pivots | [`FIBRE_AUDIT.md`](runs/astra-all-nighter-2026-09-08/FIBRE_AUDIT.md), [`notes/closure_audit.md`](runs/astra-all-nighter-2026-09-08/notes/closure_audit.md), [`notes/smoothness_audit.md`](runs/astra-all-nighter-2026-09-08/notes/smoothness_audit.md) | `scripts/audit_export_exact.py` output under `data/` | PROVED within the accepted boundary; COMPUTER-CERTIFIED finite checks |
| The selected fibre contains exactly 15 isolated reduced facet-transverse lines, each with normal bundle `O(−1) ⊕ O(−1)`; they persist on a nonempty open of the intended component | [`NEW_GEOMETRY.md`](runs/astra-all-nighter-2026-09-08/NEW_GEOMETRY.md), [`notes/degeneration_lines.md`](runs/astra-all-nighter-2026-09-08/notes/degeneration_lines.md), [`notes/line_persistence.md`](runs/astra-all-nighter-2026-09-08/notes/line_persistence.md), [review](runs/astra-all-nighter-2026-09-08/notes/line_independent_review.md) | [`data/line_certificates_all/`](runs/astra-all-nighter-2026-09-08/data/line_certificates_all/), [`data/facet_transverse_exhaustion/`](runs/astra-all-nighter-2026-09-08/data/facet_transverse_exhaustion/) | PROVED under the audited finite-fibre assumptions; line-scheme dimension/length and conics **OPEN** |
| The 123-parameter quadratic raw-generator ansatz has no solution over any characteristic-zero field; degree 3/4/5 fixed-jet ansätze fail exact next-order tests | [`MODEL.md`](runs/astra-all-nighter-2026-09-08/MODEL.md), [`notes/combined_locus_QQ_verdict.md`](runs/astra-all-nighter-2026-09-08/notes/combined_locus_QQ_verdict.md) | [`data/combined_matrix_QQ/`](runs/astra-all-nighter-2026-09-08/data/combined_matrix_QQ/), [`data/degree5_cas/`](runs/astra-all-nighter-2026-09-08/data/degree5_cas/) | **FAILED** ansätze (exact exclusions; not general nonexistence) |
| The 178-coordinate sparse support reduction, and the whole eight-parameter intrinsic slice excluding orbits 2 and 4, are singular along `P²_(b,e,h)` | [`MODEL.md`](runs/astra-all-nighter-2026-09-08/MODEL.md), [`notes/singular_slice_review.md`](runs/astra-all-nighter-2026-09-08/notes/singular_slice_review.md) | [`data/singular_eight_parameter_slice_v3/`](runs/astra-all-nighter-2026-09-08/data/singular_eight_parameter_slice_v3/) | PROVED / COMPUTER-CERTIFIED, **rejected** as a smoothing route |
| Local total-space germ `XY = q²W` at a triangle point; regular locus simply connected after base change | [`notes/topology_reduction.md`](runs/astra-all-nighter-2026-09-08/notes/topology_reduction.md) | — | PROVED, restricted scope; global `π₁` and Picard torsion **OPEN** |

## 5. CP²₉ fourfold — equivariant obstruction computation (2026-09-09)

Directory [`runs/cp2-nine-vertex-equivariant-t2-2026-09-09/`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/).
Statement, proofs and caveats: [`RESULTS.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/RESULTS.md).
Reproduction: [`REPRODUCE.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/REPRODUCE.md) (about five
minutes; Macaulay2 1.20 + Python 3). Independent re-run record:
[`PUBLICATION_VERIFICATION.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/PUBLICATION_VERIFICATION.md).

| Statement | Certificates | Status |
|---|---|---|
| `dim Hom_S(I,A)₀ = 93`, intrinsic `T¹(A/Q)₀ = 21`, `dim (T²_A)₀ = 126` | `logs/t2_dims.log`, `logs/coordinate_orbit_*.log` | established (Macaulay2, re-run) |
| `S₃`-invariant obstructions: 14; `Aut(Δ)`-invariant (order 54): 0 | `certificates/G_S3_certificate.json`, `certificates/Aut54_generators_certificate.json` and their Python re-verifications | established (Macaulay2 + exact Python) |
| 5 `Aut(Δ)`-invariant embedded tangent directions, 3 coordinate changes, 2 genuine | `certificates/*_coordinate_orbit_coords.txt` | established |
| Each genuine invariant direction extends to an all-orders `Aut(Δ)`-equivariant (hence `S₃`-equivariant) flat graded deformation; `Proj` gives a flat formal projective family | the packet's lemma applied with `T²^{Aut} = 0` | established (existence only) |
| Explicit equations, an explicit two-parameter family, a smooth generic fibre, the full Hilbert functor at `Proj A`, the fate of the other `S₃`-invariant directions | — | **not established / undecided** |
| Rank of the second-order Kuranishi quadrics (optional cross-check) | `logs/quadric_rank_check.log` | unfinished, not used |

## 8. Sphere problem — Kapustka degree-20 comparison (2026-09-17)

Directory [`runs/kapustka-degree20-comparison-2026-09-11/`](runs/kapustka-degree20-comparison-2026-09-11/).
Read [`REPORT.md`](runs/kapustka-degree20-comparison-2026-09-11/REPORT.md); literature
ledger [`SOURCES.md`](runs/kapustka-degree20-comparison-2026-09-11/SOURCES.md); gaps
[`OPEN_QUESTIONS.md`](runs/kapustka-degree20-comparison-2026-09-11/OPEN_QUESTIONS.md);
reproduction [`REPRODUCE.md`](runs/kapustka-degree20-comparison-2026-09-11/REPRODUCE.md)
(two exact Python checks in seconds, then a Macaulay2 1.20 chain of about 25 minutes over
`F₃₂₀₀₃`). Input commit `09953cefe987f304e1e8549a50df3b937747470c`. This section changes
no status label of §1–§7.

| Id | Statement | Proof / computation | Certificates | Status |
|---|---|---|---|---|
| K01 | Rows 1–8 of Table 1 of [arXiv:1010.3895v5] are reproduced exactly (nodes, `H³`, `h⁰(H)`, `c₂·H`, and both Euler numbers of the paired rows) from a Thom–Porteous node count, `deg Ȳ = deg X' + deg D`, and `χ(Y_t) = χ(X) − 2χ(D) + χ(V)` | `scripts/verify_kapustka_table1.py` | `logs/verify_kapustka_table1.log` | established (exact integer arithmetic) |
| K02 | The comparison family is Table 1 No. 8: `D = P¹×P¹` doubly projected into `P⁶`, 44 nodes, `(H³,c₂·H,h⁰(H),h¹¹,h¹²,χ,ρ) = (20,56,8,1,31,−60,1)`. The "resp." pairing printed inside the proof of Kapustka's Theorem 5.1 is transposed | `REPORT.md` §2, §3 | `logs/k01_surface.log`, `logs/k11_ci.log` | established |
| K03 | `S = ~~D₈ ⊂ P⁶` has Betti table `(1; 3; 14,53,68,43,14,2)`, `h¹(I_S(1)) = 2` and `h¹(I_S(k)) = 0` otherwise; a general `(2,2,3)` complete intersection through it has exactly 44 singular points, a reduced scheme | `scripts/k01_surface.m2`, `scripts/k11_ci.m2` | `logs/k01_surface.log`, `logs/k11_ci.log` | COMPUTER-CERTIFIED (Macaulay2, `F₃₂₀₀₃`) |
| K04 | `Hom_{O_{X'}}(I_S,O_{X'})` is generated in degrees `0,1,2,2`; the unprojection `Y ⊂ P⁷` has degree 20, two quadrics and Hilbert polynomial `(10/3)n³+(14/3)n−2`; the normal model is `Ȳ ⊂ P(1⁸,2²)` with Hilbert function `1,8,36,104,232,440` and 2 quadrics, 16 cubics, 3 quartics | `scripts/k14_unproj.m2`, `scripts/k15_models.m2`, `scripts/k16_ybar.m2` | `logs/k14_unproj.log`, `logs/k15_models.log`, `logs/k16_ybar.log`, `data/IY.m2`, `data/IYbar.m2` | COMPUTER-CERTIFIED |
| K05 | `(Ȳ,P)` is analytically `({xy = zw} ⊂ A⁴)/±1`: multiplicity 8, embedding dimension 9. Hence `Ȳ ⊄ P⁷` and [arXiv:0707.2488, Lem. 2.2] — the tool giving the aG models in `P⁷` in the degree-17 and -18 members of the same construction — does not apply | `REPORT.md` §4 | derivation | PROVED |
| K06 | **Reduction.** Every smoothing of `SR(M)` is an embedded smoothing in `P⁷` whose smooth fibres are arithmetically Gorenstein of degree 20 with h-vector `(1,4,10,4,1)`. Hence a Kapustka-family smoothing of `SR(M)` exists only if Kapustka's general member is arithmetically Gorenstein in `P⁷` (property `(★)`) | `REPORT.md` §5 | `scripts/verify_sphere.py`, `logs/verify_sphere.log` | PROVED (flatness, Hochster, semicontinuity only — no trust boundary) |
| K07 | `(★)` fails **to first order**: the `2×2` matrix of `y`-coefficients acquired by the two degree-2 equations of `Ȳ ⊂ P(1⁸,2²)` has rank `≤ 1`, because `(I_Ȳ)₂` is a 2-plane in a 3-dimensional `Λ` whose relevant kernel `Λ₀ ⊂ Λ` has codimension 1. In the local model of the smoothing the rank stays 1 at all orders | `REPORT.md` §7, `scripts/verify_local_model.py` | `logs/verify_local_model.log` | PROVED (first order); all-orders statement only in the local model |
| K08 | `(★)` itself, hence the answer to the question | — | — | **unresolved**; the next invariant is the second-order term `C₂` (see `OPEN_QUESTIONS.md`) |

Recorded but not used as evidence: CGKK 2016 §4.9 ("in degree 20 only one example is
known", the determinantal one with `h¹¹ = 2`) and KKRSSY Memoirs AMS 2026 Question 8.5
both omit a degree-20 arithmetically Gorenstein family with `h¹¹ = 1`; quotations in
`SOURCES.md`. No weight degeneration was searched for: Kapustka's construction produces
no ideal in the Hilbert scheme that contains `[SR(M)]` (K04), which is a structural
obstruction rather than a failed search.

## 6. Integrity, omissions and the Release asset

- Core workspace: `python3 scripts/make_manifest.py --verify` (covers everything outside `runs/`).
- Every run: `python3 scripts/verify_runs.py` checks each run's own manifest against the files present
  and requires every absent file to be listed in
  [`runs/PUBLICATION_OMISSIONS.json`](runs/PUBLICATION_OMISSIONS.json) with the manifest's SHA-256.
- **Release asset.** 1431 manifest-covered files of `astra-computation-2026-09-08` (about 116 MB
  uncompressed: 55 `π⁵⁶` approximation checkpoints, 1374 LLL search checkpoints, two byproducts of the
  abandoned peeling route) are not in Git. They are packaged unchanged, with their original paths, in
  the GitHub Release `historical-runs-2026-09-08-large-artifacts`, asset
  `astra-computation-2026-09-08-large-artifacts.tar.gz`; its SHA-256 is recorded in
  `runs/PUBLICATION_OMISSIONS.json`. Extract from the repository root with `tar -xzf` and the manifests
  verify completely. No result depends on these files; they are resumable search state.
- **Withheld** (six files, never published): a process listing of the author's machine, a session
  budget bookkeeping file, one compiled binary whose sources are published, and three rendered page
  images of third-party documents. Their hashes remain in the manifests and in the omissions list.
- The historical runs' guarded-job metadata records absolute paths of the machine they ran on. They are
  frozen records and were not rewritten; `scripts/publication_audit.py` reports rather than enforces the
  machine-path check for those three directories. The runs' `REPRODUCE.md` files likewise keep their
  original `cd` lines; the repository-relative equivalents are given above.
- Historical status labels were not changed. The one set of textual corrections made at publication
  time is in the CP²₉ `RESULTS.md`, marked inline and described in its `PUBLICATION_VERIFICATION.md`.

## 7. Crystallographic quotients, vertex links and SR smoothings (2026-09-11 … 2026-09-16)

Directory [`computations/crystallographic-links/`](computations/crystallographic-links/). Read
[`REPORT.md`](computations/crystallographic-links/REPORT.md) first; sources and search log in
[`SOURCES.md`](computations/crystallographic-links/SOURCES.md); gaps in
[`OPEN_QUESTIONS.md`](computations/crystallographic-links/OPEN_QUESTIONS.md). Reproduction: `python3 scripts/run_all.py`
inside the directory (about 3 minutes of exact Python plus about 1 minute of Macaulay2 1.20; the recorded
outputs are in `output/`). Nothing in this section is used by the sphere problem or by the `CP²₉` calculation.

| Statement | Proof / computation | Certificates | Status |
|---|---|---|---|
| Theorem 1 of Kaneko–Tokunaga–Yoshida lists exactly the six groups `(2,1)₀, (3,1)₀, (4,1)₀, (6,1)₀, (4,2)₁, (3,3)₀`, the rows of type `(1,1,1)` of Table II of Part I | read from both sources | `SOURCES.md` items 1–2 | cited (checked against both tables) |
| Morin–Yoshida's `Γ = L[h] ⋊ G₆` is affinely conjugate to `(3,3)₀` at `τ = ω`, by `diag(1,−1)` and the similarity `(ω²−ω)⁻¹`; `G(3,3,2) ≅ S₃` | `scripts/verify_33_identification.py` (exact arithmetic in `Q(ω)`) | `output/verify_33_identification.log` | established |
| `CP²₉` regenerated from Morin–Yoshida's orbit description equals the Kühnel–Banchoff table and the stored Chapoton–Manivel transcription; `Aut` of order 54; all vertex links isomorphic PL 3-spheres, isomorphic to the packet's Grünbaum sphere by an explicit relabelling | `scripts/build_complexes.py`, `scripts/links.py` | `output/build_complexes.json`, `output/links.json` | established |
| `(S²×S²)₁₆` and `CP²₁₀` regenerated from Bagchi–Datta's basic facets; f-vectors `(16,84,216,240,96)`, `(10,45,110,120,48)`; `Aut` orders 24, 12; each of the 16 product cells carries a geometric triangulation of `Δ₂×Δ₂`; the swap acts purely; `CP²₁₀ = (S²×S²)₁₆/swap`; no odd index permutation is an automorphism | `scripts/build_complexes.py` | `output/build_complexes.json` | established |
| For `m = 2,3,4,6` an explicit `G(m,1,2) ⋉ L(τ_m)²`-invariant rectilinear triangulation `K̃_m` of `C²` (vertex set: cone-point pairs, plus one barycentre orbit for `m ≠ 2`) has a regular action and a simplicial quotient isomorphic to `CP²₁₀`; stabiliser orders of the ten vertices recorded | `scripts/lifts.py` (finite torus cover `N = 2`) | `output/lifts.json`, `data/lifts/`, `data/cp2_10_crystallographic_markings.tsv` | established (computer-certified on the cover; descent argument in `REPORT.md` §3.1) |
| `CP²₁₀` has two link types: `L10a` (`f = (9,36,54,27)`, neighbourly, `|Aut| = 6`) at `x_ii` and `L10b` (`f = (9,31,44,22)`, `|Aut| = 2`) at `x_ij`; both PL 3-spheres (bistellar certificates); minimal nonfaces, h-vectors, Hilbert polynomials `(9/2)k³+(9/2)k`, `(11/3)k³+(16/3)k` | `scripts/links.py`, `scripts/link_t1_t2.m2` | `output/links.json`, `data/links/`, `output/m2/*.log` | established |
| Degree-0 deformation data: `Hom_S(I,A)₀ = 109/126/135`, intrinsic `T¹₀ = 53/54/63`, `T²₀ = 27/63/21`, `Aut`-invariant `T²₀ = 0/11/11` for `ℳ`, `L10a`, `L10b`; the `T¹` values agree with Altmann–Christophersen's Theorem 4.6 implemented from Definition 4.4 | `scripts/link_t1_t2.m2`, `scripts/link_equivariant.m2`, `scripts/t1_formula.py` | `output/m2/*.log`, `output/t1_formula.json` | established (exact over `Q`) |
| Smoothability of `Proj k[L10a] ⊂ P⁸` and `Proj k[L10b] ⊂ P⁸` to Calabi–Yau threefolds; their Hodge numbers | — | search log in `SOURCES.md` | **OPEN** (not found in the literature; nothing asserted here) |
| Row `(4,2)₁`: the `CP²₁₀`-lift is not `diag(i,i)`-invariant; `K̃₄` restricted to the index-4 conjugate of `(4,2)₁` has a non-simplicial quotient (19 vertices, 192 facets, doubled edges); the vertex-minimal product cell structure admits no regular invariant diagonalisation with simplicial quotient (48 facets on 9 vertices forces `f₁ = 42 > 36`) | `scripts/lifts.py`, `scripts/four_two_one_counting.py`, `scripts/four_two_one_search.py` (capped, 45 h, corroboration only) | `output/lifts.json`, `output/four_two_one_counting.json`, `output/four_two_one_search.json` | established (negative); a `(4,2)₁`-compatible triangulation with more vertices is **OPEN** |
| The recomputed `(T²₀)^{S₃} = 0` and the ten genuine `S₃`-invariant intrinsic first-order directions for the Grünbaum sphere agree with the packet's hypothesis (D04) and DEF-003 | `scripts/link_equivariant.m2` | `output/m2/L9_equivariant.log` | established; changes no status of §1–§4 |

