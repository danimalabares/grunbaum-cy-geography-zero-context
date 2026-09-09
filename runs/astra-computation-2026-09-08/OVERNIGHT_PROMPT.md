# Paste at approximately21:00 on Tuesday8September2026

You are Astra Ultra continuing Daniel's Grünbaum--Sreedharan Calabi--Yau
research. The computational session has already produced an actual smooth
algebraic-number fibre and exact Picard/Hodge/Hilbert results. Your job is
to verify, make the results easier to use, and deliver a Friday-ready brief.
Do not repeat the obsolete daytime/overnight queue or manufacture a compact
field presentation. Daniel meets Grzegorz Kapustka and Sergey Galkin on
Friday11September; the Abel deadline is Tuesday15September.

## Workspace and permissions

The only writable repository is

    /Users/daniel/github/grunbaum-cy-geography-zero-context

The completed computational packet is

    /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-computation-2026-09-08

The older preparation is

    /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-daytime-2026-09-08

Treat both completed packets as frozen evidence. Create a fresh sibling
run `runs/astra-overnight-2026-09-08/`, choosing a new suffix if it already
exists. All other repositories and archives remain read-only; inspect only
the related proof/background sources. Preserve user changes. Do not push,
install large packages, send external messages, or start linkage,
global Q-factoriality, or skeletal-polytope searches.

The frozen source heads are:

    grunbaum-zero-context-proof
      ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b
    grunbaum-zero-context-proof-fable-max-audit
      9310cd9e3316c69f129d5588d65f0b91f37365b7
    grunbaum-cy-geography-zero-context, starting HEAD
      4f75a9ae930a5cb645e06b4b8da79fa7b78a394a
    sr-project, restructure
      ff2afbbb7a8b18e7c054d16292df8db02ca87f5c
    grunbaum-cy-geography-fable-dgla
      3f7ef3da88fe963e10001fc66cbff4153d5fcb27
    heap-project
      73c8d1df1d9800425fc2ce18870c25853ea4e9f5

Read the computation packet first:

1. `COMPUTATION_RESULTS.md` and `GEOGRAPHY_THEOREM.md`.
2. `DEGREE8_PICARD_FORMULA.md`, its independent review, and
   `PRODUCT_RANK_CERTIFICATE.md`.
3. `RAMIFIED_FIBRE_EQUATIONS.md`, `RAMIFIED_POINT_REVIEW.md`,
   `RAMIFIED_FLATNESS_IDENTITY.md`, and `RAMIFIED_ARITHMETIC.md`.
4. `BOUNDED_FIELD_SEARCH.md`, `EXTRACTION_NEXT.md`, `HEAVY_QUEUE.md`,
   `REPRODUCE.md`, and `FRIDAY_READY_BRIEF.md`.

Verify the two completed packets' `ARTIFACT_SHA256SUMS` and the source
manifest. The original existence audit is accepted with its precisely
recorded Singular chart-membership trust boundary. Do not repeat that
entire audit. Independently check the *new mathematical deductions* below;
agreement between models is not a proof or qualified-human verification.

## Resource limits

This remains a2-core Intel Mac with8GB RAM. Run exactly ONE substantial
arithmetic/CAS process at a time. Never parallelize M2, Singular, Sage,
GAP, Gröbner bases, or substantial Python exact-linear-algebra jobs.
Set all four variables to1:

    OMP_NUM_THREADS
    OPENBLAS_NUM_THREADS
    MKL_NUM_THREADS
    VECLIB_MAXIMUM_THREADS

Use a copy of `scripts/run_guarded.py` for every substantial process.
Retain its2800MiB process-group RSS cap, exclusive lock, pre-existing-CAS
check, fail-closed process monitoring and owned-process-only termination.
Never stop unrelated user processes. Downstream attempts are at most
3600s; every extension needs measured progress or a new mathematical
reduction. Communicate progress at least once a minute while working.

The completed runner deliberately stops at16:35 on8September. In your
NEW copy only, use apply_patch to change its two explicit deadlines to

    STOP_LAUNCH=datetime.datetime(2026,9,9,6,0,tzinfo=LOCAL_ZONE)
    STOP_WORK=datetime.datetime(2026,9,9,6,35,tzinfo=LOCAL_ZONE)

Retain the remaining guards. Save the old copy and both hashes. Verify
the resulting code before launching anything. Finish the report by06:45,
leaving the machine ready for daytime use. Do not launch a heavy job just
because an overnight window is available.

## Results now established — do not reset them to unknown

The immutable special ideal is

    (abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg).

The self-dual resolution has ranks1,16,30,16,1 and shifts0,3,4,5,8.
The zero-context first-order corrections and certified six-jet are in
repository `equations/deformation_data.json`, SHA256

    8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f.

### Exact geography

For a smooth fibre, write n=h0(N) and r=dim(I²)_8. The newly derived
identity is

    h11 = 1748+n-r.

The antisymmetric summand of the tensor square of the given self-dual
resolution has homology sheaves C=I/I² and exterior³C in degrees1 and3.
Only four terms have ambient cohomology; their dual scalar dimensions
are692,5760,14796,12672. The terminal cokernel is the **graded module**
C(8), not an assumed saturated substitute: syzygies present I and the
polar-product map imposes2I². This gives the identity. Read and verify
the signs and spectral-sequence argument, not merely the final formula.

The degree-eight product matrix has6435 rows and4896 columns. Its
monomial central rank is1829. Twelve first-order residual columns give
the explicit integer matrix

    diag(-3,-3,-3,-8,-8,-8,8,-8,-8,-8,-8,-8)
      -2E12-2E23-2E71,

whose determinant is−3³8⁹=−3623878656. The full1841-minor begins with
that coefficient times q12. Structural q-divisibility means that **only
first-order data** determine it, despite valuation12. No unknown higher
correction can cancel it. The entries were independently rechecked.

With the accepted n<=94 and the ample class,

    1 <= h11 =1748+n-r <=1748+94-1841 =1.

Hence

    rho=h11=1, h21=31, r=1841, h0(N)=94, Euler=c3=−60,
    H³=20, c2.H=56.

Normal/Euler and conormal/Euler yield n=63+h21 and
rho=1+h3(P7,I²). No ordinary-square semicontinuity at the singular
special fibre is used. Moreover H1(N)=h11−1=0: the relevant dual
cohomology map sends1 to c1(H) and is an isomorphism when h11=1.
Thus the Hilbert scheme is smooth of dimension94 at the smooth fibre,
without needing a new BTT invocation. Pic/torsion=ZH; Picard torsion,
Pic=ZH and pi1 remain open.

The central numbers are109 embedded tangent directions,56 coordinate-orbit
dimensions,53 intrinsic tangent directions, and top quadratic dimension
38=17+3*7. The component now actually has94=56+38 dimensions; the
smooth coordinate orbit has dimension63, leaving31 abstract moduli.
Do not upgrade this to equality of the raw full Kuranishi ideal with P1³.
Do not identify the distinct older DGLA arc or component without its missing
comparison. The known general determinantal degree20 family has(2,34)
and Hilbert dimension97, so it is not this smooth component.

### An actual smooth fibre with finite algebraic coefficients

All sixteen cubics are now displayed in `RAMIFIED_FIBRE_EQUATIONS.md`.
Their exact coefficient presentation is
`data/ramified_fibre_coefficients.json`, SHA256

    0e8c3bb4a62a77af4beb22182bc8e7dc771dabd09514a0597aaed5d8b61f0616.

Take pi7=101, Kp=Q101(pi), O=Z101[pi]. The291 invariant normalized
cubic coefficients consist of21 ORIGINAL six-jet free polynomials at pi
and270 dependent algebraic numbers theta. They solve270 explicit bordered
determinants, with shared A-block sizes21,13,32 and selected Jacobian
determinant19 modulo101. All denominators are101-units. Select the unique
root theta in(pi O)^270. This gives a finite number field

    L=Q(pi,theta1,...,theta270) inside Kp.

It is NOT established that L=Q(pi), that[L:Q]=7, or that a small primitive
element is known. The finite multivariate algebraic-number presentation
is exact but not a conventional compact CAS coefficient field.

The exactness proof is important. Integral implicit-function uniqueness
and formal smoothness of the21-dimensional fixed Hilbert germ make ALL
omitted Schur equations vanish on the selected branch. Evaluation at pi
converges. The finite syzygy circuit

    Delta=det(A98),
    K=[-adj(A98)B; Delta*I30],
    R_ik=sum_j x_j K_(i,j),k

therefore satisfies FR=0 exactly after denominator clearing. The central
thirty linear syzygies generate the full special module, giving
I intersect pi*S = pi*I and full graded O-flatness.

Crucially, O/(pi7)=F101[q]/q7. The original smoothness witnesses use
q5 modulo q6 or lower orders on a complete stratified cover. They transfer
literally to this actual mixed-characteristic family and exclude every
geometric singular point by properness and a valuation contradiction.
This is not a guessed numeric specialization of a merely generic smooth
family. Jacobian-isolatedness makes the coefficient tuple algebraic over
Q(pi), and smoothness descends from Kp to L. The actual point lies on the
selected zero-context component by convergent integral component identities.
It comes from a curve agreeing with the embedded six-jet after a generator
basis change, not a purported uniquely specified all-orders arc.

True mixed-characteristic arithmetic has checked all1650 full block
equations modulo pi14 and pi56, recomputing coefficients over Z/101²
and Z/101^8 respectively. The pi56 job took205.537s/63.9MiB. Do not
reinterpret an F101 series as those mixed-characteristic digits.

### Failed searches — do not repeat unchanged

The original controller ran through order24 and32 modulo101 and failed
every prescribed bounded common rational denominator. All6960 equations
passed at every order, but no model over F101(q) resulted. The linear
free-path and sparse-three-orbit variants also failed their bounded fits.
Raw polynomial truncations were rejected by exact99-minors in degree4.
A linear kernel-graph ansatz failed at q². Polynomial peeling expanded
to nearly300000 terms and stopped after eliminating59 variables.

At the actual pi56 point, bounded Q(pi) reconstruction failed on theta1's
constant-basis coefficient at numerator/denominator bound10^7. The small
relative-degree lattice searches and exact enumeration have the final
scopes recorded in `BOUNDED_FIELD_SEARCH.md`. These are bounded exclusions,
not a field-degree theorem. Do not increase precision, repeat completed
LLL, or expand another huge coefficient ideal without a new reduction.

## Execute the useful continuation

First, in your fresh run, copy these exact inputs from the computation
packet, preserving their relative paths and recording their hashes:

    scripts/run_guarded.py
    scripts/replay_certificates.py
    scripts/verify_product_minor.py
    scripts/verify_ramified_export.py
    data/fixed_chart.json
    data/ramified_fibre_coefficients.json
    RAMIFIED_FIBRE_EQUATIONS.md
    logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json

Do not modify the copied mathematical verifiers or input data. Adapt only
the new guard's overnight dates as above. Then, from the NEW run, execute

    python3 -B scripts/replay_certificates.py --run

This runs the two independent small certificate checks sequentially and
records fresh logs. It does NOT launch the old Padé controller. If either
check fails, stop relying on the affected new claim and resolve the exact
discrepancy; preserve all failed evidence. A source/hash mismatch is not
permission to overwrite a certificate.

Next review the two new mathematical arguments in detail: the derived
degree-eight identity and the ramified-point construction. Explain their
complete hypotheses and dependencies in language Daniel can defend on a
blackboard. The original CAS trust boundary remains visible. If a genuine
gap is found, identify exactly which conclusion becomes conditional and
repair it if possible. Do not use model agreement as validation.

Only then consider compactifying the coefficient field. Read the exact
block data and completed bounded-search certificates. A productive new
attempt needs a real reduction of the270-number presentation, a viable
primitive-element candidate, or a structural geometric ansatz. Write the
reduced equations, variable count, field, denominator conditions, exact
success criterion and memory/time estimate BEFORE starting a heavy job.
Use at most3600s/2800MiB per attempt, sequentially, with checkpoints.

Success requires representing ALL sixteen cubics over a genuine exact
field and verifying all full Schur/FR identities plus the original Hensel
selector. A single modular algebraic relation is not enough. Matching the
selector proves this is the already certified fibre, so the known geography
transfers. A different free path or tangent needs a separate lineage and
smoothness argument. Never silently replace the target.

If no new reduction is found, **there is no justified mandatory heavy job**.
Use the finite coefficient presentation and finish the mathematical brief.
Do not resolve I² or compute a normal space merely to reconfirm results
already proved by the small rank argument. The compact field, Picard torsion
and fundamental group can honestly remain open.

## Deliver before morning

Reserve at least45minutes for verification and synthesis. Produce in the
fresh run:

- `OVERNIGHT_RESULTS.md`: actual checks, any new equations/field, resources,
  failed attempts, and exact remaining obstacles.
- `FRIDAY_READY_BRIEF.md`: the two-minute statement, complete blackboard
  proof outline, honest explicitness/trust boundaries, and five precise
  questions for Grzegorz and Sergey. Use today's brief as the starting point.
- A short theorem/proof note suitable for Daniel to adapt to the Abel
  proposal, with no unverified novelty or torsion claim.
- Exact scripts, immutable logs/checkpoints and a final hash manifest.

Use PROVED, COMPUTER-CERTIFIED, CONDITIONAL, HEURISTIC, FAILED and OPEN
accurately. End by stating whether the compact coefficient-field problem
improved, whether any new proof gap was found, and what Daniel can now
assert. Do not obscure the difference between exact algebraic-number
equations and a small CAS-ready power-basis presentation.
