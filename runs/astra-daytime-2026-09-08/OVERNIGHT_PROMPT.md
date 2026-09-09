# Paste this at about21:00 onTuesday8September2026

You are Astra Ultra continuing Daniel's Grünbaum–Sreedharan Calabi–Yau
research sprint. Work autonomously and produce mathematics, exact
certificates and a Friday-ready brief. Daniel meets Grzegorz Kapustka and
Sergey Galkin onFriday11September; the Abel deadline isTuesday15September.
Do not merely suggest a plan or repeat the daytime audit.

The only writable repository is

    /Users/daniel/github/grunbaum-cy-geography-zero-context

Today's completed run is

    /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-daytime-2026-09-08

All other repositories and archives are read-only. Inspect only the
related sources listed below. Preserve all user changes. Do not push,
install large software, send external messages, or run a broad linkage
or skeletal-polytope task. Store new narrative work in a fresh
`runs/astra-overnight-2026-09-08/` directory. The supplied guarded scripts
write immutable timestamped logs/checkpoints under the daytime run;
that is permitted. Never overwrite daytime evidence. If a script needs
changes, preserve its previous version/hash and explain why before resuming.

This remains a2-core Intel Mac with8GB RAM. Run at most ONE symbolic/CAS
job at a time, including substantial Python exact-linear-algebra work.
Never parallelize M2, Singular, Sage, GAP or Gröbner jobs. Set

    OMP_NUM_THREADS=1
    OPENBLAS_NUM_THREADS=1
    MKL_NUM_THREADS=1
    VECLIB_MAXIMUM_THREADS=1

Use `scripts/run_guarded.py` for every expensive process. Start with
2.8GB process-group RSS cap. It monitors RSS/time, records commands,
takes a lock, and refuses a pre-existing CAS process. Do not kill user
processes or bypass the one-job rule. A timeout/RSS cap has no
mathematical verdict. Communicate progress at least once per minute
while actively working; poll long jobs without launching a second one.

Read these first, in this order, under the daytime run:

1. DAYTIME_REPORT.md and FIXED_CHART.md.
2. FIXED_CHART_REVIEW.md and FIXED_CURVE_SCRIPT_REVIEW.md.
3. EXPLICITNESS_ROUTES.md and HEAVY_QUEUE.md.
4. PICARD_HODGE_PLAN.md and HILBERT_EXPLANATION.md.
5. LINEAGE_COMPARISON.md, LINKAGE_TRIAGE.md, REPRODUCE.md and CLAIM_LEDGER.md.

Verify SOURCE_MANIFEST.json and ARTIFACT_SHA256SUMS. The frozen heads are:

    grunbaum-zero-context-proof
      ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b
    grunbaum-zero-context-proof-fable-max-audit
      9310cd9e3316c69f129d5588d65f0b91f37365b7
    grunbaum-cy-geography-zero-context (daytime starting HEAD)
      4f75a9ae930a5cb645e06b4b8da79fa7b78a394a
    sr-project, branch restructure
      ff2afbbb7a8b18e7c054d16292df8db02ca87f5c
    grunbaum-cy-geography-fable-dgla
      3f7ef3da88fe963e10001fc66cbff4153d5fcb27
    heap-project
      73c8d1df1d9800425fc2ce18870c25853ea4e9f5

The primary zero-context existence proof is accepted conditional on its
precisely audited Singular chart-membership trust boundary. Do not
spend the night repeating those expensive second-engine checks.

## Today's actual mathematical advances—use these

The ideal, with this immutable order, is

    (abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg).

The selected tangent has intrinsic S3-orbit coefficients(1,...,10),
and the certified generic equivariant generator/syzygy six-jet is in
the frozen proof's `deformation/generic_equivariant_state_[F/R]_order6.txt`.
Do not use the distinct sparse line or a finite polynomial truncation.

1. The new finite fixed chart has291 invariant normalized generator
   coefficients. The degree-four multiplication matrix has size330×128,
   with98 central pivot columns and30 relations. In its block form
   [A B;C D], A(0)=identity, and E=D−CA^−1B has6960 entries.
   The exact constant Jacobian has rank270 with a270×270 minor−1.
   There are21 free coordinates:10 intrinsic plus11 coordinate-orbit.
   Their zero-based indices and all exact data are in data/fixed_chart.json.

2. This is an actual local Hilbert chart: full lifted first syzygies
   imply degreewise flatness. The fixed Hilbert germ is formally smooth
   by the complete invariant obstruction vanishing. Thus270 selected
   equations define the same local germ as all6960, not just a tangent
   approximation. The other equations vanish for this all-orders reason.

3. Normalize the source generator row by its16×16 pivot coefficient
   matrix P(q): F→FP^−1 and R→PR. Prescribe the21 free coefficients
   to their normalized six-jet polynomials, setting their coefficients
   beyond order6 to zero. The implicit-function minor−1 gives a unique
   Z_(101)-integral formal solution. It agrees with the certified embedded
   six-jet and inherits generic smoothness from the accepted certificate.

4. Finite algebraic equations for that pointed curve and family ALREADY
   EXIST in equations/fixed_curve_QQ.sing and .json:3210 equations in
   q plus3210 dependent variables (270 generator coordinates and2940
   auxiliary syzygy coordinates). Choose the germ at q=z=W=0. It is
   an algebraic curve étale over q at0, with function field finite overQ(q).
   Its geometric generic fibre is smooth. What remains is a manageable
   field presentation or a specified smooth fibre at a nonzero algebraic
   parameter. Do not start a blind3210-variable Gröbner elimination.

5. The tested modular recurrence factors the SAME270×270 scalar matrix
   once, solves only270 new generator coefficients at each order, obtains
   the syzygy coefficients from A(0)=I, and checks all6960 equations.
   Order6 matched the certified normalized jet in7.4s/~28MB, using only
   standard Python. No NumPy/SymPy installation is needed.
   A final provenance-hardened regression took5s/27MB. Treating that
   six-jet as a polynomial pair FAILED exactly at q7 (residue37 mod101
   in row0/column0). Do not repeat that truncation attempt. The finite
   implicit Singular equations loaded in11s/328MB without any Gröbner job.
   The negative test rejects that F,R pair only; it does not exclude
   higher syzygy corrections for the same truncated generator polynomials.

6. On any certified smooth characteristic-zero fibre:

       h21 = h0(N)−63 = h4(P7,I²)−64,
       rho = h11 = 1+h3(P7,I²).

   The ideal-module resolution of I² through homological degree5 suffices:
   compute Ext3(I²,S(−8))_0 and Ext4(I²,S(−8))_0 using only three scalar
   degree-zero dual maps. The supplied M2 script is prepared and its API
   was smoke-tested. A vanishing Ext4 at certified smooth reduction proves
   characteristic-zero rho=1; nonzero modular values are only bounds.
   For a rational model overF101(q), a carefully documented integral
   formal chart at the prime(101) may supply the smooth spread needed
   for the same semicontinuity argument. Verify that bridge explicitly.

7. Pic(X_M)=ZH, and Pic(total overC[[q]])=ZH, but the20 central prime
   divisors contribute a rank19 vertical subgroup of Cl(total). Thus
   this total space CANNOT be Q-factorial. Do not try to prove its local
   class groups vanish. The useful alternative is Cl(total)_Q generated
   by H and vertical components, with geometric descent and global
   compatibility. The six-jet does not determine these completed class groups.

8. The actual tangent lies uniquely in the top P1³ quadratic component;
   the entire invariant ten-plane has identical rows in all three rank-one
   blocks.38=17+3×7 and94=56+38 remain an upper-bound calculation.
   Proving an actual94-dimensional smoothing component would implyh21=31.
   The fixed smooth21-dimensional germ lies on the zero-context smoothing
   component, but does not establish its dimension94.

9. The older DGLA tangent shares P1³ but is inequivalent under all
   projective special-fibre identifications and invertible reparametrizations.
   Its common completed-component relation is OPEN. The older proof does
   not supply usable finite smooth-fibre equations. Do not transfer its
   jets, Hodge assignments, or component claims.

10. The known determinantal degree20 family has(2,34) and Hilbert
    dimension97: Kapustka–Kapustka0802.3669v3, Theorem3.8/Proposition3.10.
    Bertin's earlier preprint prints conflicting Hodge claims and is not
    the reference to use. The94 bound excludes that component throughX_M.
    Hilbert connectedness is Hartshorne1966 Corollary5.9, not irreducibility
    or connectedness of the smooth CY locus.

## Execute the optimized queue

Follow HEAVY_QUEUE.md in strict priority order. From the daytime directory,
start the primary controller only now, at night:

    python3 scripts/night_primary.py --run

It lifts the specified fixed curve modulo101 to order24, tries small
common rational denominators, and verifies exact FR after denominator
clearing. If needed it resumes only to32 and repeats, then stops.
The initial block is estimated at5–20minutes and below0.5GB, with
hard30minute/2.8GB limits per stage. Estimates are not measurements.
Use actual emitted checkpoint/model paths, not invented output filenames.

A finite jet, a Padé fit, or a vanishing finite residual is NOT closure.
Only the exact coefficientwise FR identity, denominators nonzero at0,
and the full canonical central syzygies pass. The hardened checker
records unsuccessful degrees and checks the selected normalized six-jet.
`fixtures/` contains deliberately singular synthetic controls; none is
an overnight smoothing model. Never enable --allow-other-sixjet for
the primary run or feed synthetic models to Hodge scripts.

If a verified modular rational model appears:

- Export it with scripts/export_rational_model.py. Record that its field
  isF101(q), notQ. Try matching-prime rational reconstruction only with
  consistent denominator structure, and verify any reconstructed QQ
  F,R identity exactly. Save the reconstruction code and all primes.
- Prefer a small rational/algebraic nonzero parameter once QQ equations
  exist. Prove flatness from exact syzygies, preserve lineage/jet comparison,
  and certify degree/Hilbert data and projective smoothness. The prepared
  certify_fibre.m2 uses subsets of genuine minors; positive saturation is
  decisive, subset failure is inconclusive. Do not assumeq=1 works.
- Run normal-space computation before I². With a characteristic-zero
  fibre this gives exacth21 and Hilbert dimension. Then run the targeted
  square calculation; prioritize a good modular vanishing certificate forrho1.
- Use h11/h21 to computec3=Euler=2(h11−h21). Distinguish Picard rank from
  torsion and from Pic=ZH. Evenrho1 leaves torsion and fundamental group open.

If low-degree rational closure fails:

- Preserve the already proved finite implicit algebraic family. Attempt
  algebraic field/point extraction only after exact symmetry and linear
  reduction of its size. An equivariant section sends each central
  quartic to the average of its representing columns, splitting the128
  source into image98 and kernel30. Use S3 representation blocks before
  symbolic matrix inversion or elimination. Record every basis change.
  The reduced elimination script must be written and validated before
  the gated command in the queue; it was not fictitiously prepared today.
- A six-jet normal-rank calculation is a separate fallback: form the
  correct6960×1664 map, eliminate1555 constant pivots, and study the
  q-divisible5405×109 residual. A first nonzero coefficient proves a
  rank lower bound. Leading minors can have valuation greater than6
  when structural q-divisibility fixes their leading term; track precision
  under every division. Equality needs a complementary bound/kernel.
- Only after these routes have a stopping result consider full P1.
  Substitute rank-one parametrizations BEFORE constructing universal
  expressions, treat identical blocks once, and keep cross-block scalars.
  The existing15-pivot minor leaves12 residual equations. Do not infer
  their vanishing from degree4 compatibility or a long sparse jet.

No linkage job is queued: the verified(3,3,3,3) residual has degree61,
and any second all-cubic CI returns the starting degree20 scheme. The
first distinct CI can give47, but no rationality/descent mechanism is
known. Reopen linkage only for explicit colon inputs plus a concrete
useful geometric payoff.

## Stopping, verification and final artifacts

Checkpoint every completed order, prime, exact matrix rank, eliminated
block and certified ideal identity. Hash inputs/outputs and save commands,
software versions, elapsed time, sampled RSS, random seeds if any, and
all negative results. Stop an unproductive job at its cap; do not restart
the same computation without a mathematically explained reduction.
Do not spend the entire night accumulating coefficients.

Keep enough context and at least45–60minutes for verification and prose.
Stop launching heavy work by about06:00 and finish before daytime use.
Use PROVED, COMPUTER-CERTIFIED, CONDITIONAL, HEURISTIC, FAILED and OPEN
on every substantive conclusion. Human mathematical explanations must
state why the certificates imply flatness, smoothness, rank or component
claims; “the script says so” is not an explanation.

Produce, in the new overnight directory:

- OVERNIGHT_REPORT.md with exact successes, failures and remaining gates.
- EQUATIONS_AND_CERTIFICATE.md, even if the outcome is only the finite
  implicit algebraic family; state the field and branch precisely.
- HODGE_PICARD_RESULTS.md with exact values versus bounds and hypotheses.
- HILBERT_COMPONENT_RESULTS.md distinguishing upper bounds from equality.
- FRIDAY_READY_BRIEF.md: a concise explanation Daniel can give Grzegorz
  and Sergey, the strongest verified equations/geography, the accepted
  trust boundary, what is still open, and five precise discussion questions.
- Reproduction commands, code, immutable logs, and a final hash manifest.

The final reply should say what Daniel can now assert, give any exact
equations/Hodge pair or explain precisely what prevents them, and link
the Friday brief. Do not manufacture an exact Picard rank, identify
unrelated arcs, or call a truncated polynomial family a smooth fibre.
