# Algebraic field extraction after the rational-curve attempt

2026-09-08. This file concerns explicit equations; the separate degree-eight
rank argument has now addressed the Hodge/Picard-rank target. No claim here
identifies a finite smooth fibre until a particular root is checked.

## Current outcome after the ramified construction

**CONDITIONAL on the accepted source/chart computer-certificate boundary.**
A particular algebraic-number root is now specified by finite equations
and a unique ramified p-adic isolating condition. The actual 16 cubic
equations are displayed in `RAMIFIED_FIBRE_EQUATIONS.md`; the coefficient
presentation has 271 algebraic variables, including pi with pi^7=101, and
270 bordered determinants of size at most 33. The independent mathematical
review `RAMIFIED_POINT_REVIEW.md` accepts the argument that this root gives
a smooth characteristic-zero fibre. This bypasses primitive-element
extraction; the number field is not yet represented by a small minimal
polynomial.

**COMPUTER-CERTIFIED.** The export checks the selected Jacobian determinant
19 modulo 101, coefficient denominator units, and original central
generator/syzygy data. A genuine mixed-characteristic computation verifies
the actual root modulo pi^14 and then pi^56, with all 1650 full block
equations verified directly in each ramified quotient ring. The pi^56
run took 205.537 seconds and 63.9 MiB peak sampled RSS. Its exact point is
saved, not merely a guessed series fit. The
following failed rational and algebraic-series searches are preserved as
historical reductions, not as the current best existence argument.

**FAILED bounded field simplification.** At pi^56 precision, the first
basis coefficient of theta_1 has no rational representative with numerator
and denominator bounded by 10^7. The attempted low-height Q(pi)
presentation therefore stops immediately. This is not a proof that
L differs from Q(pi), much less a bound on the number-field degree.
`RAMIFIED_ARITHMETIC.md` gives the exact Euclidean rejection, commands,
resources, and distinction from the earlier F101(q) rational-curve fits.
The 271-variable finite algebraic-number presentation remains valid.

## Exact representation reduction

**PROVED.** The original 2940 syzygy-frame unknowns are unnecessary.
Let V=S_1, W=(I_M)_3, J=(I_M)_4, K=ker(V tensor W -> J), and
B=(S/I_M)_4. On the three conjugacy classes 1,(12),(123), their characters
and multiplicities are:

| Space | Character | Trivial multiplicity | Sign multiplicity | Standard multiplicity |
|---|---|---:|---:|---:|
| V | (8,2,2) | 3 | 1 | 2 |
| W | (16,4,1) | 5 | 1 | 5 |
| V tensor W | (128,8,2) | 26 | 18 | 42 |
| J | (98,8,2) | 21 | 13 | 32 |
| K | (30,0,0) | 5 | 5 | 10 |
| B | (232,12,7) | 47 | 35 | 75 |

The characters can be counted on the monomial permutation bases. For
example S4 has character (330,20,9), and J has (98,8,2); their difference
gives B. A rank-one standard representation has dimension two, so the
last column counts copies, not dimensions. K is five copies of the
regular representation.

**PROVED.** Replace the nonequivariant central section of multiplication
by the equivariant section that sends each quartic to the average of all
columns representing that quartic. This splits the source as J plus K.
The deformed map has blocks A,B,C,D with A(0)=I and B(0)=C(0)=D(0)=0.
Every generator coefficient orbit defines an equivariant perturbation.
Schur's lemma reduces its syzygy equations to three multiplicity blocks:

| Representation | A size | U size | Lower equation matrix D-CU |
|---|---|---|---|
| trivial | 21 by21 | 21 by5 | 47 by5 |
| sign | 13 by13 | 13 by5 | 35 by5 |
| standard | 32 by32 | 32 by10 | 75 by10 |

Thus there are only 490 auxiliary entries of U, and 1160 lower equations.
The full polynomial system is

    A_r(z) U_r = B_r(z),    D_r(z)-C_r(z) U_r=0

for the three representations r. The largest matrix inverse that would be
needed is 32 by 32, rather than 98 by 98. The equations are still bilinear;
no symbolic inverse is formed.

For the standard block a rational primitive projector is

    e_plus = (1+tau)/2 - (sum_g g)/6.

Its image is the transposition-fixed line in each standard summand.
The companion line is obtained by applying r-r² for a3-cycle r. An
equivariant map has the same matrix on both lines; there is no square-root
extension or unrecorded complex representation basis. The basis vectors,
their rational transformations, and all A/B/C/D linear forms are retained.

**COMPUTER-CERTIFIED.** `scripts/build_equivariant_blocks.py` completed
under the root's single-process guard in 10.36 s, with 21.1 MiB sampled peak
RSS. It obtained exactly the block dimensions above and selected 270
independent lower equations with full rank modulo101 in the *same*
270 dependent generator coordinates as the daytime chart. Thus the same
21 free paths and the same normalized six-jet can be preserved. The exact
rational block data occupy only 200 KB:
`data/equivariant_blocks_QQ.json`. The log is
`logs/20260908T121826-equivariant-blocks.stdout`, with guard metadata in
the adjacent JSON file. No CAS ran.

## A reduced attempt, its exact result, and why it stopped

**COMPUTER-CERTIFIED finite reduction.** Substituting the prescribed free
six-jet polynomials leaves 760 variables other than q: 270 dependent z and
490 U entries, instead of 3210. The full block equations give 1650 nonzero
distinct polynomial equations with 83,843 terms over F101. Selecting 270
lower equations would give 760 equations, but the reduction retained all
full equations so that no remote selected-equation component was silently
accepted.

The new script `scripts/reduce_equivariant_system.py` performs only exact
local eliminations. If an equation is a*x-b with a(0)!=0, solving x=b/a
and clearing denominators in the other equations preserves the localized
origin branch. It records every numerator, denominator, and eliminated
variable. In the first run only constant a were permitted, so every
substitution was polynomial. It also attempts a constant-Jacobian
normalization and computes strongly connected components of the resulting
implicit dependency graph, subject to a term cap.

**COMPUTER-CERTIFIED outcome:** after 177.65 s and 181.6 MiB sampled peak RSS,
59 variables had been eliminated, leaving 701 variables and 1591 equations
with 298,949 terms. Every remaining eligible substitution would exceed the
300,000-total-term cap. The exact reduced equations and triangular
substitutions are in

    data/peeled_sixjet_p101_polynomial.json
    data/peeled_sixjet_p101_polynomial.sing

The Singular file is an input only: it contains no standard-basis or
elimination command. The SCC normalization was stopped by its own term
gate and gives no useful small decomposition in this run.

**FAILED as a practical field extraction:** direct polynomial peeling of
this particular free-coordinate curve has not produced a manageable field
or point. Expression size grew by more than a factor 3 while removing
fewer than 8% of the variables. This is a recorded computational failure
of that strategy within its size gate, not a failure of the finite family
or of generic smoothness. A Gröbner computation on the resulting 701-variable
input is not an assessed daytime job and has not been launched.

## Further controlled attempts: actual outcomes

**COMPUTER-CERTIFIED finite jets; FAILED bounded rational ansatz.** We
changed only the 21 free paths to their first-order terms, preserving the
original normalized tangent. The separate immutable script
`scripts/fixed_curve_lift_linear.py` was run through order 24, then resumed
through order 32. All 6960 Schur equations vanish through each order.
The first jet agrees with the original, but the six-jet does not, as
expected. Neither the original script nor the original checkpoints was
modified. Every new checkpoint records `free_path_order: 1` and hashes of
both the original and the actual variant. The separate closure checker
validates this metadata and verifies the first tangent and the absence
of higher free coefficients before accepting `--allow-other-sixjet`.

The order-24 job took 20.31 seconds (27.7 MiB sampled peak RSS); its Padé
screen took 2.383 seconds. The order-32 resume took 16.497 seconds
(28.2 MiB sampled peak RSS); its screen took 2.378 seconds. Every common
generator-and-syzygy denominator bound from 0 through 10 failed. Logs:

    logs/20260908T123845-linear-free-order24.stdout
    logs/20260908T123918-linear-free-pade24.stdout
    logs/20260908T123941-linear-free-order32.stdout
    logs/20260908T124106-linear-free-pade32-corrected-path.stdout

An intervening invocation used a mistyped checkpoint timestamp and exited
immediately with file-not-found. Its log is retained under
`20260908T124048-linear-free-pade32`; this is an invocation failure, not
mathematical evidence. The corrected invocation is listed above.

**PROVED limitation of the common-denominator test.** A small rational
generator matrix can have a canonical syzygy matrix with much larger
denominator: U=A(F)^(-1)B(F). Thus fitting a small shared denominator to
both F and U can miss an explicit low-degree F.

**FAILED generator-only rational screen.** To address that limitation,
`scripts/screen_generator_pade.py` used only the 291 generator coordinates
of both *existing* order-32 checkpoints. No additional jet was computed.
For the original six-jet curve, every denominator bound d=0,...,10 with
numerator bound d+6 was inconsistent. For the new linear-free curve, both
numerator bounds d+1 and d+6 were inconsistent for every d=0,...,10.
This exact linear-algebra screen took 2.44 seconds with 21.5 MiB sampled
peak RSS. All attempts are recorded in

    logs/20260908T124245-generator-only-existing32.stdout
    logs/20260908T124245-generator-only-existing32.artifacts/

No candidate existed, so no exact rational block-identity verification
was needed. These failures reject precisely the tested small rational
models, not higher-degree rationality, algebraic power series, other
free-coordinate paths, or the existence of a smooth fibre.

**FAILED bounded primitive-field recognition.** The structurally different
`scripts/recognize_primitive_field.py` then selected eight dependent
coordinates in each existing order-32 checkpoint, namely zero-based
indices 0,...,7. Each selected coordinate first failed every individual
rational fit with denominator degree at most 4 and numerator degree at
most d+6. For each coordinate the script tested both its raw series and
the valuation-removed series z_j/q^v minus its leading coefficient.
Polynomial relations had t-degree from 2 through 4 and q-degree at most
6, with at most 28 unknown coefficients and at least four more available
series equations than unknowns. Dividing by q^v correctly reduced the
available truncation order. Zero truncated monomial columns were forbidden.

Each curve supplied 297 admissible tests. Every coefficient matrix had
nullity zero; no candidate and no automatic-nullspace skip occurred. The
whole run took 3.52 seconds and 23.2 MiB sampled peak RSS. It therefore
did not attempt all-coordinate field reconstruction or an exact Schur
verification. Complete ranks and bidegrees are retained in

    logs/20260908T125017-primitive-field-existing32.stdout
    logs/20260908T125017-primitive-field-existing32.artifacts/*_FINAL.json

The optional reconstruction code is prepared for a future *actual*
candidate: it fits all 291 coordinates as a polynomial in t of degree
below deg_t(P), with q-numerator degree at most 6 and one common
q-denominator of degree at most 4. Even such a fit would not constitute
an exact family without algebraic identity and branch verification.

**CONDITIONAL new finite-point route.** Subsequent mathematical inspection
suggested avoiding primitive-element extraction altogether. The finite
chart's coefficient equations can select a unique ramified p-adic
algebraic-number point with pi^7=101. Its truncation modulo pi^7 is the
original certified six-jet, so the finite smoothness certificates may
transport directly to characteristic zero. See
`RAMIFIED_POINT_CONSTRUCTION.md` for the complete argument and independent
review obligations. This is not another rational/series fit.

## Ranked next reductions

1. **HEURISTIC, structurally different cheap screen:** prescribe the
   equivariant kernel graph U(q)=q U_1 in the averaged section. Then the
   full equations are linear in the 291 generator coefficients over
   F101(q). The order-two consistency test can reject this restrictive
   ansatz before any field arithmetic. The separately prepared
   `scripts/probe_linear_kernel_graph.py` and
   `EXTRACTION_RECOMMENDATIONS.md` contain the exact recipe. This probe
   was prepared by the Picard/Hodge agent and is not included in the
   executions listed above.
2. **HEURISTIC, field rather than rational-function recognition:** seek a
   low-degree algebraic relation P(q,t)=0 for a primitive normalized
   generator coefficient and express all other coefficients in
   F101(q)[t]/(P). A finite-order fit is only a candidate. Acceptance
   requires the full FR identity modulo P, a denominator nonzero on the
   origin branch, and branch/irreducibility control. This could reduce
   field extraction to two variables even when no rational curve was
   found. With only 33 coefficients, do not fit a general bidegree (4,6)
   polynomial: its 35 coefficients guarantee a spurious nullspace.
   Use a genuinely overdetermined fit and reserve holdout coefficients.
   No such certificate has yet been obtained in this reduction work.
3. **HEURISTIC, bounded algebraic backup:** on the linear-path block
   system try polynomial peeling, followed by origin-unit rational
   peeling only if the term count decreases. Stop at the current term/RAM
   gates; do not feed hundreds of variables to an unassessed Gröbner job.

**PROVED component bridge for changed paths:** the localized S3-fixed
Hilbert germ is smooth and irreducible, and the certified smoothing arc
passes through it. It lies in one completed Hilbert component meeting the
smooth-fibre locus. Any smooth fibre produced on this same fixed germ has
the zero-context component's Hodge data. This permits changed paths
without asserting equality of six-jets or all-orders arcs. Smoothness
of the changed path still needs proof; component membership alone does
not make every curve a smoothing.

An additional geometric gauge is available but **OPEN computationally**:
the centralizer of S3 in PGL8 has dimension 13, with a 2-dimensional
stabilizer at the monomial point. Fixing an 11-dimensional coordinate-orbit
slice would leave ten intrinsic free parameters. This changes the
coefficient gauge by a projective transformation and must preserve its
invertibility and integrality. A slice may simplify equations; its
existence does not imply that the 10-dimensional germ is rational.

## Commands and size gates

Only the root controller may allocate a substantial process slot. Never
run these simultaneously with any other substantial task.

Rebuild the exact blocks:

    python3 scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag equivariant-blocks -- python3 -B scripts/build_equivariant_blocks.py

The completed six-jet polynomial-peeling run was:

    python3 scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag equivariant-polynomial-peel -- python3 -B scripts/reduce_equivariant_system.py --prime 101 --path sixjet --max-seconds 240 --max-terms 5000 --max-total-terms 300000

The completed linear-free curve experiment started with:

    python3 -B scripts/run_guarded.py --seconds 1800 --memory-mb 2800 --tag linear-free-order24 -- python3 -B scripts/fixed_curve_lift_linear.py --order 24 --prime 101

The order-32 job resumed the actual order-24 artifact, and every guarded
job's adjacent metadata JSON retains its exact command and input paths.
To reproduce the generator-only rejection from the existing immutable
checkpoints without extending either jet:

    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag generator-only-existing32 -- python3 -B scripts/screen_generator_pade.py logs/20260908T121301-night-curve-32.artifacts/fixed_curve_p101_order32.json logs/20260908T123941-linear-free-order32.artifacts/fixed_curve_p101_order32.json --max-denominator 10

A new linear-path polynomial attempt, after a slot is allocated:

    python3 scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag equivariant-linear-peel -- python3 -B scripts/reduce_equivariant_system.py --prime 101 --path linear --max-seconds 240 --max-terms 5000 --max-total-terms 300000

For an origin-unit rational attempt add `--rational` and use a fresh output
path/tag. Every command refuses conflicting existing output. All matrix
and polynomial operations are exact; no CAS is invoked by these scripts.
Actual reduced sizes, not the availability of a Singular input file,
determine whether a subsequent Gröbner job is sensible.

**OPEN presentation simplification:** a small primitive element,
multiplication table, or rational model for the already specified number
field. The ramified construction has now supplied the previously missing
finite parameter/root, exact algebraic coefficient equations, flatness,
and transported projective smoothness certificate, subject to the stated
source/chart trust boundary. No failed finite-series fit is being promoted
to an exact family.
