# Daytime research sprint —8September2026

The main deliverable is `OVERNIGHT_PROMPT.md`. Read this report,
`PICARD_HODGE_PLAN.md`, and `HILBERT_EXPLANATION.md` before Friday.
The short speaking notes are in `FRIDAY_BRIEF_DRAFT.md`.

## What changed mathematically today

**COMPUTER-CERTIFIED + PROVED:** we constructed a finite S3-fixed
Hilbert chart using normalized cubic generators and their30 linear
syzygies. It has291 generator coefficients,270 dependent directions,
and21 free directions; an exact270×270 Jacobian minor has determinant−1.
The accepted all-orders invariant unobstructedness theorem proves the
selected270 equations define the full fixed germ locally. This is a
different implicit-function argument from the earlier15-pivot P1 test:
the missing equations vanish here for a supplied all-orders reason.

**PROVED, conditional on the existing smoothing trust boundary:** fixing
the21 free coordinates to their normalized six-jet polynomials gives
finite algebraic equations for a pointed curve and a family with smooth
geometric generic fibre. The equations are saved in
`equations/fixed_curve_QQ.sing` and `.json`, with the origin branch
selector. The curve is étale over the q-line at its marked point.
Its function field is finite over Q(q). This strengthens the original
existential curve-selection result without assuming P1 survives universally.

**OPEN:** the resulting algebraic extension has not been reduced to a
practical field presentation, and a particular smooth closed fibre at
a specified nonzero parameter has not been extracted. Exact Hodge numbers,
Picard rank and the dimension94 equality remain open. The explicit
finite incidence system is not confused with a convenient fibre model.

**PROVED:** for a certified smooth fibre,

    h21=h0(N)−63=h4(P7,I²)−64,
    rho=h11=1+h3(P7,I²).

Only two untwisted ideal-square cohomology groups are needed. A partial
resolution of the ideal module through homological degree5 supplies
Ext3_0 and Ext4_0. A vanishing Ext4_0 at certified smooth reduction is
enough to prove characteristic-zero rho=1. A nonzero modular value is
only an upper bound. The supplied script avoids constructing whole Ext
modules and ranks only degree-zero dual matrices.

**PROVED:** Pic(X_M)=ZH, but this does not transfer automatically to
the generic fibre. In fact a normal projective complete-DVR smoothing
model cannot be Q-factorial: its20 central components give19 independent
vertical Weil-divisor classes, whereas Pic(total)=ZH. This rules out the
proposed global factoriality shortcut. The useful class-group target is
generation by H and vertical components after geometric divisor descent.

**COMPUTER-CERTIFIED + PROVED:** the actual proof tangent lies uniquely
on the top quadratic component P1³. The entire invariant ten-plane lies
there, with both rows equal in each2×6 matrix. The sparse direction in
the old universal test is not the final proof tangent. The full38-dimensional
component question remains open, so h21=31 is still conditional.

**COMPUTER-CERTIFIED + PROVED:** the older DGLA tangent and the
zero-context tangent share P1³ but are inequivalent under all projective
identifications of the special fibre and invertible reparametrizations.
The full53×53 transport is a permutation after an explicit vertex map;
a four-coordinate torus invariant distinguishes all six possible maps.
Thus older jets cannot be substituted into this proof. Common completed
Hilbert-component membership is still open for those two lineages.

**PROVED linkage triage:** the recorded(3,3,3,3) link has degree61.
Its residual has exactly four cubic generators spanning the original
complete intersection, so a second all-cubic link simply returns degree20.
The first distinct CI type gives degree at least47. There is no concrete
rational residual strategy warranting a heavy linkage search tonight.

## Exactly what was inspected

**COMPUTER-CERTIFIED provenance:** exact commits are recorded in
`SOURCE_MANIFEST.json` with selected input SHA256 hashes.

| Repository | Source commit / use |
|---|---|
| grunbaum-zero-context-proof | ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b; frozen primary proof |
| grunbaum-zero-context-proof-fable-max-audit | 9310cd9e3316c69f129d5588d65f0b91f37365b7; accepted trust boundary |
| grunbaum-cy-geography-zero-context | 4f75a9ae930a5cb645e06b4b8da79fa7b78a394a; starting geography HEAD |
| sr-project, restructure | ff2afbbb7a8b18e7c054d16292df8db02ca87f5c; distinct DGLA proof |
| grunbaum-cy-geography-fable-dgla | 3f7ef3da88fe963e10001fc66cbff4153d5fcb27; older tangent/link data |
| heap-project | 73c8d1df1d9800425fc2ce18870c25853ea4e9f5; Daniel's mathematical notes |

Read the primary FINAL/PROOF; P1 all-orders, Kuranishi and total-space
audits; the entire universal test and installed VersalDeformations
implementation of lifting; saved universal fourth-order data and failure
records; actual first-order basis and generic equivariant F/R six-jet;
equivariant integral extension and algebraization arguments. Read the
independent audit's VERDICT, EXECUTIVE_SUMMARY, CLAIM_LEDGER and
MISSING_EVIDENCE first. The earlier DGLA PDF/TeX and exact basis/link
certificates were inspected with relevant PDF pages rendered.

Read all three named geography reports. Inspected the named heap notes,
including the old determinantal speculation in stanley-reisner.tex.
No local fausk.tex was found in the in-scope repositories; Fausk's primary
thesis PDF was inspected instead, with the exact locator and limitation
recorded in PICARD_HODGE_PLAN. No unrelated repository was inspected.
Related archive member lists were read only to locate the requested old
notes. Sergey's REPORT.md/notes.md were not located; no lineage attribution
was invented for an unavailable file.

Primary source verification followed the internal mathematical discovery
phase. The useful determinantal reference is Kapustka–Kapustka,
arXiv0802.3669v3, Theorem3.8 and Proposition3.10, proving(2,34).
Bertin's earlier preprint actually prints conflicting Hodge claims and
is not valid support for that pair. Hartshorne's connectedness statement
is Corollary5.9 of the1966 paper, not an irreducibility theorem.
Full source ledgers and links are in the mathematical memos.

## Cheap calculations and resource record

| Check | Result / scope | Observed resource information |
|---|---|---|
| P1 tangent/orbit integer check |45 minors zero; all block entries nonzero; correct fixed-plane identification | subsecond-to1s, tiny RAM |
| Older basis transport | all six vertex maps, full53-coordinate transport, quotient/orbit and torus-invariant tests |3–9s, standard Python |
| New fixed chart |291 coefficient orbits, linear rank270, determinant−1 |1.3s; sampling interval too coarse for meaningful peak |
| Normalized curve six-jet | exact rational generator normalization; full6960 equations and all291 jet coefficients agree mod101 throughq6 |7.4s, sampled28MB |
| Finite curve export |3210 finite polynomial equations and sixteen generator formulae; no Gröbner operation |3.7s, sampled23MB |
| Hodge API smoke test |degree-zero dual-map/basis operations, including zero terminal modules | M2,5.8s, sampled83MB |
| Solver/rational-identity controls |constant/polynomial success, nonflat negative controls, sign/provenance checks | cheap standard Python; see FIXED_CURVE_SCRIPT_REVIEW |
| Actual six-jet polynomial-pair closure | **FAILED:** first residual at q7, quartic row0/relation column0, coefficient37 mod101; all lower coefficients zero |6.3s, sampled25MB; this rejects this truncated F,R pair, not all possible syzygies for its F |
| Singular finite-equation load |3210 equations load without syntax errors; construction only, no standard basis |11.1s, sampled328MB |

The final provenance-hardened six-jet regression took5.0s/27MB;
use the `20260908T111640-curve-sixjet-final` checkpoints for resumption,
not the earlier pre-hardening copies. Exact log paths are in REPRODUCE.md.

**PROVED resource compliance:** no heavy universal deformation, I²
resolution, Gröbner search, broad linkage job or skeletal-polytope task
was launched. At most one CAS process ran at any time. Every guarded
symbolic job used one thread and hard limits; the actual CAS work was
only the tiny API/syntax checks recorded in logs. Default Python has no
NumPy or SymPy; the new scripts need only its standard library. No large
package was installed, no source/archive was changed, and nothing was pushed.

**FAILED attempts retained:** the existing source's sparse orderfour
FR residual; old universal timeouts; the already rejected truncation;
an initial rational-test implementation rejected constant families and
stopped too early after one failed fit—both defects were repaired and
tested on explicit controls. Final review also repaired compact cubic
words in executable export strings, with a separate rendering regression
and exact re-export check. PDF-render and process-monitor permissions
are recorded in the subtask reports. Synthetic rational test models
are explicitly singular controls, not discovered smooth fibres.

## Best routes and what waits for tonight

**HEURISTIC primary computation:** extend today's fixed chart curve
mod101 to order24, at most32, using the same270 scalar pivots. Fit
small common rational denominators and verify exact FR after clearing
them. The supplied overnight controller runs these jobs sequentially
and stops at the stated ansatz boundary. If successful, use exact
reconstruction and a finite-fibre certificate, then normal-space and I²
calculations. The full queue has explicit input gates and stopping rules.

**OPEN backup:** symmetry-reduced algebraic field extraction from the
already finite implicit curve. Do not start a3210-variable Gröbner
elimination. A second backup targets the full P1 component only after
rank-one substitution and blockwise identities. Its extra payoff would
be dimension94 and h21=31, but it is not needed for today's finite family.

**HEURISTIC best Picard computation:** a good-prime conormal vanishing
on a certified smooth model, before attempting a characteristic-zero
I² resolution. The degeneration alternative now has the correct vertical
class-group target. Fundamental group and torsion remain open.

The mathematical-paper-audit skill was used in targeted verification
mode to maintain the claim/dependency ledger and source boundaries.
The existence theorem was not re-audited in full. Its four Singular
chart-membership certificates retain precisely the accepted software
trust boundary; no second-engine rerun was attempted today.
