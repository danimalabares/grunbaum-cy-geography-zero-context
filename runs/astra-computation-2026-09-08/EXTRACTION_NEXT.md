# Bounded practical field extraction from the actual ramified point

2026-09-08. **PROVED already:** the finite algebraic-number tuple in
`RAMIFIED_FIBRE_EQUATIONS.md` defines an actual smooth fibre. This note
addresses only the **OPEN** practical problem of replacing the270-number
selector by a small coefficient field and short power-basis coordinates.
Failure here does not affect smoothness, finite explicitness, or geography.

**Status update:** the root reports completion of the trueπ56 Hensel
point (all1650 direct block identities zero), in205.537 seconds with
sampled peak memory63.9MiB. The bounded Q(π) rational reconstruction
failed already on the constant coefficient of θ1, whose residue is
5101489845552212 modulo101^8. This rejects that height<=10^7
coordinate reconstruction, not membership in Q(π) with larger heights.
The root subsequently ran the four bounded lattice probes and the two
explicitly authorized cubic diagnostic/resume jobs; outcomes are below.

## Gate zero: use the true point, and stop if degree seven already works

**Required input:** `data/ramified_hensel_pi56.json`, using the same keys
as `data/ramified_hensel_pi14.json`: `theta_values` has270 seven-entry
vectors, `lambda_values` has291, `uniformizer_precision` is56, and
`coefficient_modulus` is M=101^8. Each vector represents an element of

    O/(π^56) = (Z/MZ)[π]/(π^7−101).

These must be the actual mixed-characteristic Hensel coefficients, not
coefficients of a formal F101[[q]] series with q renamed π. Carries
π^7=101 matter. The existing Hensel job controls their computation and
the exact full-equation checks; this queue never requests more precision.

First attempt the already prepared coordinatewise rational reconstruction
over Q(π), with numerator and denominator bounds at most10^7. If all
generator coordinates reconstruct and the exact full Hilbert-chart
identities plus the original Hensel selector verify, the relative
extension is unnecessary: **do not run the lattice probes below**.

**HEURISTIC until exact verification:** small rational reconstructions
consistent with the modulus are candidates, not identities of algebraic
numbers. The full-point verification, not the coefficient height, is the
success criterion.

## Four probes only

**COMPUTER-CERTIFIED bounded probes, executed by the root:**
`scripts/recognize_padic_relative_degree.py` tries only θ1 and θ2,
each with relative T-degree at most2 and at most3. It uses exact integer
and Fraction arithmetic in standard Python; no GP, CAS or installation.
The two declared coefficient-height boxes are100 and1000. There is no
additional coordinate search, extra precision, larger degree or larger
height in this queue.

For one θ and degree d, write

    P(T)=sum_(j=0..d) sum_(r=0..6) c_(j,r) π^r T^j,
    c_(j,r)∈Z.

The search space is the full-rank lattice Λ⊂Z^n, n=7(d+1), defined by
P(θ)=0 modulo π^56. Its first7 basis rows are M times the coordinate
vectors in the constant coefficient block. For each j>=1 and r=0,...,6,
the next row has the negative seven-entry residue of π^rθ^j in the
constant block and1 in position(j,r). Consequently

    [Z^n:Λ]=M^7.

The script builds this basis exactly, carries out capped LLL with
δ=3/4, and retains its unimodular integer transformation. Every saved
candidate is re-evaluated modulo the **full** M. Dividing the polynomial
content by101 can lose precision, so a primitive normalization is accepted
only if that full-modulus recheck still vanishes.

## A rigorous negative certificate, not just an unsuccessful LLL search

**PROVED.** Let b_i be any full lattice basis and b_i* its exact
Gram--Schmidt orthogonal vectors. For v=sum a_i b_i∈Λ nonzero, choose
the largest i with a_i≠0. Projection onto b_i* has length
|a_i|·||b_i*||. Therefore

    ||v||² >= min_i ||b_i*||².

Every coefficient vector of height at most B has ||v||²<=nB².
Thus the strict inequality

    min_i ||b_i*||² > nB²

certifies that **no nonzero modular relation in that coefficient box
exists**, and hence no exact global integral-coefficient relation in that
same box can exist for the selected θ. This is an exhaustive bounded
exclusion, independent of the quality or completion of LLL.

The script stores the exact rational squared lengths, verifies that every
basis row belongs to Λ, checks the unimodular transformation, and checks
that the lattice determinant has absolute value M^7. A reviewer can
therefore reproduce the exclusion directly from the saved integer basis.

**INCONCLUSIVE otherwise:** absence of a short *basis vector* does not
exclude a short integer combination. If the GSO inequality fails and no
candidate is found, report only that this capped search found none. Even
an exhaustive height1000 exclusion does not rule out relative field
degree2 or3 with larger coefficients, denominators after clearing, or
a different primitive-element choice.

## Exact success gates for a short polynomial

**HEURISTIC candidate:** a small P(θ)=0 modulo π^56 is not an exact
global relation. Before replacing the current finite point presentation:

1. Regard P over the exact field Q(π), with π^7=101. Remove content,
   factor over that field if necessary, and choose the irreducible factor
   compatible with the selected local root. A reducible quotient ring is
   not an acceptable substitute for the intended coefficient field.
2. Verify a local root selector. A simple Hensel root suffices; otherwise
   use an explicit generalized Hensel/Newton bound with valuations and
   a proved resulting precision. Do not label a root merely by a floating
   approximation. Retain agreement with the original π-adic residue-zero
   selector, not merely some conjugate root of P.
3. Represent **all** generator coefficients (all291 λ values, with the
   twenty-one free ones already in Q(π)) in Q(π)[T]/P. A polynomial for
   θ1 alone may define only a proper subfield and proves nothing about
   the other coefficients. Reconstruction bounds must be declared before
   any enlarged search.
4. Verify all full Schur equations or the entire FR identity exactly in
   that number field, and verify invertibility of every denominator and
   A-block. The selected270 equations alone are not the global check.
5. Verify that the resulting tuple has the original Hensel residue class.
   Then uniqueness identifies it with the already certified actual point,
   so its smoothness, component and geography are inherited. Without this
   identity check, a different finite chart root requires separate
   geometric certification.

**PROVED success after these gates:** a practical exact field presentation
of the same actual fibre. An exact polynomial alone, with the remaining
coefficients unrepresented, is only partial progress and must be labelled
accordingly.

## Resource and checkpoint contract

The actual-point job requires root authorization and exclusive ownership
of the one substantial-process slot. It is sequential and sets all four
thread variables to1. Defaults are180 seconds per probe,900 seconds
globally,10000 LLL iterations per probe and a16384-bit arithmetic-growth
gate. The actual outer resource guard is2800MiB and900 seconds. The
largest lattice is28×28; the measured four-probe job used15.59MiB and
44.213 seconds. These measurements do not authorize a larger search.

An exact basis/transform checkpoint is written every25 iterations or ten
seconds, and at every terminal condition. Capped runs are preserved and
can still yield a rigorous GSO exclusion. A fresh output directory is
mandatory. Resume from a selected checkpoint into another fresh directory;
the source/input hashes must agree. Resuming does not authorize a larger
degree, height, precision or total research budget.

Recorded actual-point command, already executed by the root; a rerun
requires a fresh output directory and renewed slot ownership:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 runs/astra-computation-2026-09-08/scripts/recognize_padic_relative_degree.py --point runs/astra-computation-2026-09-08/data/ramified_hensel_pi56.json --theta 1 2 --degree 2 3 --height 100 1000 --per-probe-seconds 180 --max-total-seconds 900 --max-iterations 10000 --output runs/astra-computation-2026-09-08/data/padic_relative_degree_pi56
```

Only the tiny integer-lattice smoke test is authorized in preparation:

```sh
python3 runs/astra-computation-2026-09-08/scripts/recognize_padic_relative_degree.py --smoke-test
```

**COMPUTER-CERTIFIED smoke success:** three integer lattices of dimensions
3,3,2 passed, with determinants−3,101,10000. Exact unimodular transforms,
fresh versus incremental Gram--Schmidt, size reduction and Lovasz were
checked; the scaled identity also checked the bounded-exclusion formula.
The captured values are in `data/padic_relative_degree_smoke.json`.
The actual project point was not read by this smoke test.

**Stop rule:** after these four probes, synthesize their exact scope and
return to the existing finite coefficient presentation. Do not escalate
precision or start a broad number-field search during this daytime run.

## Measured result and narrowly authorized diagnostic

**COMPUTER-CERTIFIED bounded exclusion:** both relative-degree-at-most2
probes completed LLL, and their fresh exact Gram--Schmidt certificates
exclude every nonzero polynomial with the stated integral coefficient
height at most1000 (hence at most100). This does not rule out quadratic
relative field degree with larger defining coefficients.

**Original INCONCLUSIVE capped cubic probes:** both degree-at-most3 probes reached
10000 iterations, found no displayed short candidate, and have no GSO
exclusion certificate. The complete four-probe process took44.213 seconds
and15.59MiB by the root's guard. Source summaries and certificates are
in `data/padic_relative_degree_pi56/`.

The quadratic probes themselves required6961 and7195 iterations. The
cubic probes ended at LLL indices13 and22 after5031 and5025 swaps.
Their fresh GSO minima equal1, consistent with a partially processed
tail of the initial basis; this observation alone does not certify
progress or exclude a bookkeeping defect.

**PROVED diagnostic invariant:** put Φ=∏_i det Gram(b_1,...,b_i), an
exact positive integer. A size reduction preserves Φ. At a Lovasz swap,
Φ is multiplied by (B_k+μ²B_(k−1))/B_(k−1), strictly less than3/4.
Thus saved checkpoints with s intervening swaps must satisfy

    4^s Φ_after < 3^s Φ_before.

`scripts/diagnose_padic_lll.py` leaves the original recognition source
and hash unchanged. It freshly checks bases at iterations25,5000,10000,
verifies the above progress inequality, and replays the last25 steps
from fresh GSO to compare with the saved final state. The root authorized
one existing cubic checkpoint at a time to resume for at most60 seconds
and10000 further iterations. Those instrumented resumes compared
incremental against fresh exact GSO every100 steps. They added no
coordinate, degree, height box or π-adic precision.

**COMPUTER-CERTIFIED diagnostic outcome:** θ1's diagnostic passed the
exact potential and fresh25-step replay checks in1.197 seconds. Its
audited resume completed after1084 additional iterations (4.792 seconds
under the root guard), with no GSO drift. θ2's saved audited-resume
summary also records completion, after1356 additional iterations and
3.689 internal seconds. Both cubic probes rigorously exclude height
at most100; neither GSO minimum alone excludes height1000, and neither
produced a short modular candidate. The height1000 cubic cases remained
**OPEN at this intermediate stage** and were subsequently settled by
the exhaustive searches below. See `data/lll_theta1_cubic_audited_resume/` and
`data/lll_theta2_cubic_audited_resume/`.

## Completed next method: exact sphere enumeration

**COMPUTER-CERTIFIED, executed by the root for θ1:**
`scripts/enumerate_padic_height_box.py` performs exact Fincke--Pohst
enumeration on the completed θ1 cubic lattice. This is not a change of
LLL parameters. It uses the already certified28×28 basis and the same
π56 point. It searches the full sphere

    ||v||² <= 28·1000² = 28000000.

Every vector whose28 polynomial coefficients have absolute value at
most1000 lies in that sphere. Write v=sum a_i b_i. Exact GSO gives

    ||v||² = sum_k B_k (a_k + sum_(i>k) μ_(i,k)a_i)².

The explicit DFS stack assigns a_i from the largest index downward.
For center c=C/D and remaining squared allowance t, admissible integers
a satisfy (aD+C)²<=tD². Taking an exact integer square root of
floor(tD²) therefore gives the complete integer interval, with no
floating-point rounding. The implementation uses no additional box
pruning. At each complete vector it checks both the exact Euclidean
norm and the actual28 coefficient heights, and independently rechecks
modular membership.

**PROVED interpretation:** if the search exhausts the sphere and finds
no nonzero vector, there is no relation in the height1000 box. More
generally, if every nonzero vector in the exhausted sphere is outside
that box, the same bounded exclusion follows. If the100000-node or
900-second limit is reached, the result is **OPEN**, with the explicit
unprocessed DFS stack preserved. Resume never resets the cumulative node
count or requests more π-adic precision. A found modular vector is only
**HEURISTIC** as a global polynomial identity; the full field/Schur and
Hensel identification gates above remain necessary.

**Cost estimate from saved GSO data:** all squared GSO lengths for θ1
exceed28000000 except zero-based index24, approximately24257948.
In particular indices25,26,27 exceed the radius and their coefficients
are initially forced to zero. Only the±1 alternatives at index24 can
start a nonzero branch. A heuristic suffix-ellipsoid-volume estimate is
about29 nodes in total; this is not a runtime or completeness bound.
An execution lasting seconds is plausible. The hard caps remain100000
candidate assignments,900 internal seconds and the root's2800MiB outer
guard. The θ2 search was not an automatic follow-up; it received separate
explicit authorization and used the wrapper described below.

**COMPUTER-CERTIFIED preparation test:** three tiny integer lattices
were compared with exhaustive coefficient-box enumeration with proved
sufficient bounds. The two-dimensional examples have24 and12 nonzero
sphere vectors, and the three-dimensional example has56. Exact counts,
uniqueness and interrupted-stack resumption all agreed in a process
lasting0.485 seconds. The actual project point was not enumerated.
Results are saved in `data/padic_sphere_smoke.json`.

Recorded θ1 command, executed after root authorization:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 runs/astra-computation-2026-09-08/scripts/enumerate_padic_height_box.py --basis runs/astra-computation-2026-09-08/data/lll_theta1_cubic_audited_resume/audited_resume_result.json --original-probe runs/astra-computation-2026-09-08/data/padic_relative_degree_pi56/theta1_d3_result.json --max-nodes 100000 --max-seconds 900 --output runs/astra-computation-2026-09-08/data/theta1_cubic_height1000_enumeration
```

**COMPUTER-CERTIFIED final outcomes:** both θ1 and θ2 exhausted the
entire squared-radius28000000 sphere after exactly34 assignments,
with only the zero leaf. Hence both relative-degree-at-most3,
integer pi-power-basis height-at-most1000 polynomial ansätze are excluded.
The θ1 search took0.003950 seconds and its Python process0.186176
seconds. The separately authorized θ2 search took0.002029 seconds,
its process0.173800 seconds, and its guard1.197 seconds.

The θ2 wrapper `scripts/enumerate_theta2_height_box.py` imports the
unchanged generic exact enumerator. It verifies all input hashes,
rebuilds the lattice from the actual θ2 approximation, and checks
the unimodular transform, determinant and modular membership before
enumeration. Its tiny exhaustive/resume tests passed in0.417 seconds.
The recorded actual launch was

```sh
python3 scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag theta2-cubic-height1000-enumeration -- python3 scripts/enumerate_theta2_height_box.py --max-nodes 100000 --max-seconds 120 --output data/theta2_cubic_height1000_enumeration
```

The working directory was this computation run. The first sandboxed
attempt failed closed on process/RSS inspection and launched nothing;
approval for the same guarded command enabled the successful run.
See `logs/20260908T142128-theta2-cubic-height1000-enumeration.json`.

The two authoritative final summaries are
`data/theta1_cubic_height1000_enumeration/summary.json` and
`data/theta2_cubic_height1000_enumeration/summary.json`.
`BOUNDED_FIELD_SEARCH.md` gives a short proof from coarse exact GSO
inequalities and three integer basis-vector norms that independently
explains the34-node outcomes. No actual-point job remains running.

**Stop:** the declared bounded searches are complete. The existence,
smoothness and geography of the finite Hensel-selected fibre are unchanged.
A smaller field presentation remains **OPEN** outside the explicitly
excluded coefficient-height boxes. No further search follows automatically.
