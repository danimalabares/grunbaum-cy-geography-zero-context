# Strictly sequential overnight queue

Start about21:00 on8September2026. **HEURISTIC** estimates are resource
envelopes, not benchmarks or promises. Run exactly one job at a time,
including Python symbolic/rank jobs. Do not run a skeletal-polytope search
alongside this queue on the2-core/8GB Mac. Use one thread and a2.8GB
process-group RSS cap initially; a cap hit is a computational timeout,
not a mathematical negative answer. No large package installation or push.

All commands below are from
`/Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-daytime-2026-09-08`.
The guarded runner sets OMP/OPENBLAS/MKL/VECLIB thread counts to1,
refuses a pre-existing CAS process, takes a lock, records command/time/RSS,
and stops only its own process group. Logs and artifacts have unique
timestamped paths. RSS monitoring requires permission to execute `ps`;
it fails closed if unavailable. Do not remove a lock to bypass a running job.

## 0. Provenance and preflight — first

1. Question: are the equations and all source identities the prepared ones?
2. Command: `python3 scripts/record_provenance.py`, then verify
   `ARTIFACT_SHA256SUMS` with `shasum -a 256 -c ARTIFACT_SHA256SUMS`.
3. Inputs: six named repositories and the run manifest. Inspect current
   process list before any symbolic job; preserve any new user changes.
4. Estimate: seconds, below0.1GB.
5. Checkpoint: existing manifests and a fresh night worklog; do not overwrite
   daytime logs. At a changed source commit use the frozen objects or stop
   the dependent calculation until the mismatch is resolved.
6. Success: provenance only, not a mathematical theorem.
7. Failure: input/environment mismatch; do not silently compare unlike data.
8. Dependency: every later job.

## 1. Primary: the fixed algebraic curve, modular rational closure

1. Question: do the coefficient functions on today's specified algebraic
   curve have small common rational denominators, yielding usable equations?
2. Exact command at night:

       python3 scripts/night_primary.py --run

   The controller runs, strictly sequentially, these bounded stages:

       python3 scripts/run_guarded.py --seconds 1800 --memory-mb 2800 --tag night-curve-24 -- python3 scripts/fixed_curve_lift.py --order 24 --prime 101
       python3 scripts/run_guarded.py --seconds 1800 --memory-mb 2800 --tag night-closure-24 -- python3 scripts/check_rational_closure.py CHECKPOINT --max-denominator 10

   Here the controller supplies the actual checkpoint path returned by
   the preceding guarded run. If no exact rational model results, it resumes
   to32 and repeats the closure test. It stops there automatically.
3. Inputs: `data/fixed_chart.json`, the frozen geography JSON six-jet,
   `fixed_curve_lift.py`, and its parser/helper scripts. No universal
   versal calculation is rerun. The21 free paths are fixed degree-six
   polynomials; the270 dependent scalar pivots have determinant−1.
4. Estimate:5–20minutes total and normally below0.5GB. The daytime order6
   check took7.4s/28MB including rational normalization.32 is not benchmarked.
   Each stage has a30minute ceiling.
5. Checkpoint: one JSON per completed order, all6960 equations checked,
   normalized jet and hashes saved. Preserve each denominator-attempt log.
6. Success: an exact FR polynomial identity after clearing denominators,
   canonical special syzygies, and same normalized six-jet. This gives a
   finite rational family over F101 nearq=0. The separate integral chart
   proof supplies the relation to the characteristic-zero smoothing.
7. Failure: only the bounded common-denominator ansatz failed. The finite
   algebraic curve remains valid by `FIXED_CHART.md`. Do not go to order100,
   repeat the source's old order30 sparse arc, or evaluate a jet atq=1.
8. Dependency: enables2–5 in their easiest form. If no model, go to6A;
   retain independent six-jet rank option6B if algebraic elimination stalls.

## 2. Exact export and characteristic-zero reconstruction / branch selection

1. Question: can the modular model be realized over a manageable exact field,
   and can a smooth finite fibre be specified on the correct component?
2. Initial exact command, with MODEL the actual file emitted by job1:

       python3 scripts/run_guarded.py --seconds 300 --memory-mb 1800 --tag export-model -- python3 scripts/export_rational_model.py MODEL

   To obtain matching-prime data for rational reconstruction, run sequentially:

       python3 scripts/run_guarded.py --seconds 1800 --memory-mb 2800 --tag curve-p103 -- python3 scripts/fixed_curve_lift.py --order 24 --prime 103

   Then call `check_rational_closure.py` on its actual checkpoint. Use further
   small primes only when the denominator degrees and supports match.
   CRT/rational reconstruction and verification code must be saved before
   use; it is not supplied as a fictitiously completed QQ reconstruction.
3. Inputs: exact modular rational model, new matching-prime checkpoints,
   and finite integral chart. Never lift modular integers by fiat.
4. Estimate:30–90minutes,0.5–2GB; cap each process30minutes and this route
   at90minutes without a shrinking reconstruction uncertainty.
5. Checkpoint: prime-by-prime model/denominator data; reconstructed rational
   coefficients; exact QQ residual identity; branch and denominator records.
6. Success: exact characteristic-zero F,R with FR=0, F(0)=F0, full special
   syzygies, and a verified jet/field comparison; then select a nonzero
   rational parameter avoiding denominators and certify that fibre in3.
7. Failure: rational reconstruction or parameter selection is unresolved.
   A modular model can still support the conditional Picard-bound route
   in4–5 after its integral formal spread is written and checked.
8. Dependency: QQ version enables exact Hodge numbers; modular version
   enables upper bounds and potentially an exact rho=1 conclusion.

## 3. Certify a finite fibre

1. Question: do finite equations define a smooth degree20 projective threefold
   in the intended family, rather than an invalid truncation?
2. After setting GS_FIBRE_INPUT to the actual exported finite input:

       python3 scripts/run_guarded.py --seconds 3600 --memory-mb 2800 --tag fibre-certificate -- M2 --script scripts/certify_fibre.m2

3. Inputs: S,I over QQ/a number field or a finite field, a proven flat family,
   and the chart/jet/component record. Use a fresh exact coefficient field.
4. Estimate: minutes–1hour,0.5–2.8GB, depending strongly on coefficients.
5. Checkpoint: Hilbert/saturation/resolution output and each selected-minor
   stage. Preserve the actual parameter, field polynomial and root selector.
6. Success: true Jacobian minors saturate to the unit ideal, plus correct
   degree/Hilbert sanity. Family flatness and lineage come from the separate
   exact presentation/curve proof; write `FIBRE_CERTIFICATE.md` collecting both.
7. Failure: subset-minor failure is inconclusive; a proved nonempty full
   singular locus rejects only that parameter. Try at most three specified
   small parameters, sequentially. A Hilbert/dimension failure rejects the
   proposed model and blocks downstream Hodge claims.
8. Dependency: mandatory for arbitrary finite-parameter equations. For a
   generic modular field F101(q), the matching-six-jet integral argument
   can provide generic smoothness without recomputing gigantic chart bases.

## 4. Normal space first

1. Question: what is h0(N), hence h21 and the smooth Hilbert dimension?
2. Set GS_FIBRE_INPUT, GS_FIBRE_CERTIFICATE, and a new absolute
   GS_HODGE_PREFIX to actual produced files; then run:

       env GS_HODGE_PHASE=normal python3 scripts/run_guarded.py --seconds 3600 --memory-mb 2800 --tag normal -- M2 --script scripts/hodge_from_fibre.m2

3. Inputs: finite certified fibre. For a good modular reduction additionally
   set GS_HODGE_MODULAR_BOUND=1 and supply its proven smooth lift/spread.
4. Estimate:5–60minutes,0.5–2.8GB; no benchmark on a new fibre exists.
5. Checkpoint: input hash, first syzygy size, exact degree-zero kernel size.
6. Success: in characteristic zero h21=h0N−63 and Hilbert dimension=h0N.
   A modular result is an upper bound until an opposite bound is proved.
7. Failure: timeout is no verdict. A QQ value above94 means a provenance,
   component, smoothness, or calculation assumption must be investigated.
8. Dependency: does not depend on I²; run it before5.

## 5. Targeted I² calculation

1. Question: do Ext4(I²,S(−8))_0 and Ext3(I²,S(−8))_0 determine rho and
   independently check h21?
2. With the same actual input/certificate variables and fresh prefix:

       env GS_HODGE_PHASE=square python3 scripts/run_guarded.py --seconds 7200 --memory-mb 2800 --tag ideal-square -- M2 --script scripts/hodge_from_fibre.m2

3. Inputs: certified smooth finite fibre; prefer a good modular model first.
4. Estimate:30minutes–several hours; memory may exceed2.8GB, so enforce the
   cap. No daytime I² resolution was run. Limit this attempt to2hours.
5. Checkpoint: partial ideal-module resolution through homological degree5,
   degrees and differentials; only the degree-zero dual matrices d3,d4,d5
   are subsequently ranked. If the resolution itself times out, no completed
   checkpoint is promised; retain its log rather than restart blindly.
6. Success: over characteristic zero, rho=h11=1+Ext4_0,
   h21=Ext3_0−64, Euler=2(h11−h21). At a certified smooth reduction,
   Ext4_0=0 already proves characteristic-zero rho=1 by semicontinuity.
7. Failure: nonzero modular Ext4 gives only an upper bound. A stalled
   resolution suggests degree-strand methods or a geometric description;
   it does not justify reading Picard rank from the original Betti table.
8. Dependency: requires3's input gate. It does not settle torsion or
   Pic(X)=ZH unless torsion is independently excluded.

## 6. Backups after failed rational closure

### 6A. Algebraic field representation, with a size gate

1. Question: reduce the finite implicit curve to an exact field/point.
2. Preparation command (no Gröbner basis):

       python3 scripts/run_guarded.py --seconds 300 --memory-mb 1800 --tag finite-curve-mod101 -- python3 scripts/export_fixed_curve.py --prime 101

   The resulting equations are explicit inputs, not authorization to run
   `std` on3210 unknowns. First implement and verify the equivariant central
   section/isotypic splitting described in FIXED_CHART.md, remove solved
   linear variables, and save `scripts/reduced_curve_elimination.sing`.
   Only once its exact input and size are recorded is the command:

       python3 scripts/run_guarded.py --seconds 3600 --memory-mb 2800 --tag reduced-curve-elimination -- Singular -q scripts/reduced_curve_elimination.sing

   **OPEN implementation:** the reduced elimination script does not yet
   exist; do not claim the displayed final command is executable before
   constructing it. The finite uneliminated equations do exist.
3. Inputs: `equations/fixed_curve_QQ.sing/.json`, mod101 export, selected
   Jacobian data, origin branch selector. Keep all2940 syzygy variables
   out of a blind global elimination.
4. Estimate:1–3hours including reduction; a reduced Gröbner job can still
   exceed limits. Require a concrete forecast from its actual sizes first.
5. Checkpoint: each exact linear elimination/basis transformation, reduced
   variable counts, original-to-reduced maps, verified inverse identities.
6. Success: manageable primitive element or algebraic point on the origin
   branch, verified in full equations. Return to3–5 immediately.
7. Failure: retain today's finite algebraic family; report effective
   field/fibre extraction OPEN. No unbounded elimination restart.
8. Dependency: independent of rationality; uses job1's finite chart data.

### 6B. Geography from six-jet rank, then universal P1 only if justified

1. Question: can a leading minor force h0N<94, or can an exact38-parameter
   identity prove the opposite lower bound94?
2. There is no already-certified generic normal-rank script. Build one
   from the precise6960×1664 normal map in PICARD_HODGE_PLAN.md, first
   eliminate1555 constant pivots, and save all row/column maps. The guarded
   command after this preparation is

       python3 scripts/run_guarded.py --seconds 3600 --memory-mb 2800 --tag jet-normal-rank -- M2 --script scripts/jet_normal_rank.m2

   **OPEN implementation:** do not run or cite a nonexistent script.
   This is an explicitly gated development job, not a promised certificate.
3. Inputs: the certified F/R six-jet, standard monomial frames, and exact
   precision accounting. Alternatively restrict saved universal data to
   the rank-one parametrizations before any new lifting.
4. Estimate:1–2hours development/computation, up to2.8GB; stop at1hour
   computation. P1 universal continuation is lower priority than finite fibre.
5. Checkpoint: constant pivots,5405×109 residual map, q-valuations, actual
   nonzero minors. Do not just record a modular numerical rank.
6. Success: extra pivots improve upper bounds; a compatible full kernel or
   proven38-dimensional algebraic family supplies equality. P1 membership
   through any fixed degree alone does not prove94.
7. Failure: no new bound; six-jet vanishing is not all-orders vanishing.
8. Dependency: can proceed without finite equations, but after the primary
   explicitness attack has a recorded stopping result.

## Explicitly not queued

**FAILED/OPEN:** blind universal orderfive calculation; repeated old
certificate-engine audits; full q30 truncation evaluation; a heavy I_M²
resolution used as if it were the smooth conormal; a class-group-zero or
Q-factorial-total-space search; and broad linkage. The second all-cubic
link merely returns degree20, and no rational residual route is known.

Reserve the final45–60minutes for independent identity checks and the
Friday brief. Stop new heavy jobs by about06:00; finish synthesis before
Daniel's daytime use. If a process reaches a cap, record the exact reason
and continue only with a different justified route. Never trade away
verification merely to start another experiment.
