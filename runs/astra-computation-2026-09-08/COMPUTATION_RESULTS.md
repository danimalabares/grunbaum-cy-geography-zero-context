# Computational phase — 8 September 2026

Final computational handoff, completed at approximately 14:35 Rio time.
The Picard/Hodge theorem and a specified smooth number-field fibre are
established within the accepted source-certificate trust boundary. A bounded
attempt to use bounded-height coefficients in Q(pi) has failed; further
small relative-degree searches have the bounded outcomes below. Neither theorem
depends on those searches. All new artifacts are in this run. The frozen
daytime evidence remains unchanged. Qualified-human verification is not
claimed.

## Actual equations: a specified smooth algebraic-number fibre

**PROVED within the recorded trust boundary:** there is now a particular
smooth characteristic-zero fibre, with all sixteen cubic equations displayed
in [RAMIFIED_FIBRE_EQUATIONS.md](RAMIFIED_FIBRE_EQUATIONS.md). Its exact
machine-readable coefficients are in
[ramified_fibre_coefficients.json](data/ramified_fibre_coefficients.json).
This is a finite algebraic-number presentation, not a truncated family.

Here is its precise definition. Set

\[
\pi^7=101,\quad K_p=\mathbf Q_{101}(\pi),\quad
\mathcal O=\mathbf Z_{101}[\pi],\quad
L=\mathbf Q(\pi,\theta_1,\ldots,\theta_{270})\subset K_p.
\]

The ordered tuple theta is the **unique** solution in `(pi O)^270` of
the270 explicitly indexed bordered-determinant equations

\[
\det\begin{pmatrix}A_r(\lambda)&B_{r,\bullet j}(\lambda)\\
C_{r,i\bullet}(\lambda)&D_{r,ij}(\lambda)\end{pmatrix}=0.
\]

The three A-block sizes are21,13,32. All rational linear-form factors,
all270 selected row/column pairs, and the assignment of291 coefficients
lambda to the270 theta values and21 fixed polynomials in pi are in the
JSON. Each determinant is a finite polynomial of matrix size at most33;
it need not be expanded. The selected270-square Jacobian is19 modulo101.
Thus this is a precise isolated algebraic-number tuple, not an arbitrary
root of a coefficient scheme. The auxiliary syzygy numbers have been
eliminated entirely. In particular, this is not the old3210-equation
generic-curve system relabeled as a result.

With the immutable ordering

```
(f1,...,f16)=(abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg),
```

the actual equations are

\[
F_i=f_i+\sum_{m\in\mathcal B_3}
 \lambda_{\operatorname{orbit}(i,m)}m=0\qquad(1\le i\le16).
\]

Here B3 is the set of104 **cubic monomials not in I_M**, not an abstract
unknown deformation term. All1664 tail coefficients and the16 leading
coefficients are displayed individually in the linked equation document.
For example, one exact coefficient is

\[
\lambda_{38}=5\pi+8\pi^4+\frac{135295}{9}\pi^5
-\frac{26469644}{81}\pi^6.
\]

The other20 free values are equally explicit rational polynomials; the
remaining values are the individually indexed algebraic numbers theta.

**OPEN practical limitation:** the global degree `[L:Q]` and a compact
primitive-element/multiplication-table presentation have not been computed.
The field is **not** being identified with Q(pi) merely because its selected
completion has degree7. The equations are exact and specify a usable
mathematical example; they are not yet a conventional small-number-field
input for arbitrary CAS calculations.

### Why the selected fibre is flat and smooth

**PROVED:** the determinant-unit implicit chart has its unique integral
formal solution over `Z_(101)[[21 free coordinates]]`. All omitted Schur
equations vanish there by the accepted all-orders fixed-Hilbert-germ
theorem, not by a finite residual check. Substituting the ORIGINAL free
six-jet polynomials at pi converges in O and selects theta. The full
generator/syzygy identity is therefore exact. The thirty lifted linear
syzygies reduce to the complete central first-syzygy module. Consequently
`I intersect pi*S = pi*I`, giving O-flatness degree by degree. This
preserves the stated pure self-dual resolution and Hilbert series

\[
\frac{1-16t^3+30t^4-16t^5+t^8}{(1-t)^8}.
\]

**PROVED transport:** `O/(pi^7) = F101[q]/(q^7)`, with q mapping to pi.
Thus the actual fibre agrees with the certified normalized embedded
six-jet modulo pi7. The frozen proof's complete stratified smoothness
cover uses q5 identities modulo q6, q4 modulo q5, and the triangle
critical-value identity at q2. All transport literally to this DVR.
A geometric singular point would extend by properness after a finite
ramified extension; its specialization lies in one of those strata.
Evaluation gives a unit times pi^e in `(pi^(e+1))`, or the contradictory
triangle critical zero. Hence the actual K_p fibre is geometrically smooth.
The invertible polynomial Jacobian makes theta algebraic over Q(pi), so
L is a finite number field; smoothness descends to L.

The result has dimension3, degree20, Hilbert polynomial
`(10/3)m^3+(14/3)m`, trivial canonical bundle, and h1(O)=h2(O)=0.
This lineage is the algebraic curve agreeing with the certified embedded
six-jet after an invertible generator-basis normalization. It is not an
assertion of equality with a uniquely specified all-orders arc. Convergent
integral component identities place it on the selected zero-context
Hilbert component; no older DGLA data are transferred.

The full argument and targeted review are in
[RAMIFIED_POINT_REVIEW.md](RAMIFIED_POINT_REVIEW.md), and the explicit
denominator-clearing flatness identity is in
[RAMIFIED_FLATNESS_IDENTITY.md](RAMIFIED_FLATNESS_IDENTITY.md).

**COMPUTER-CERTIFIED new arithmetic:** the coefficient presentation export
used2.490s/23.38MiB. A separate parser checked every one of the1680 displayed
monomial/coefficient pairs and recomputed the Jacobian by column elimination
(1.205s; too short for a reliable sampled peak). Genuine arithmetic over
`(Z/10201)[pi]/(pi^7-101)` verified all1650 block equations modulo pi14,
after recomputing q0..13 over Z/10201 and checking all6960 original Schur
coefficients at each order. This used12.187s/37.3MiB and did not reuse
the characteristic101 jet as though it supplied mixed-characteristic digits.
See `data/ramified_hensel_pi14.json`. These finite arithmetic checks validate
the implementation; the preceding algebraic argument proves exact closure
and smoothness.

**COMPUTER-CERTIFIED stronger arithmetic checkpoint:**
`data/ramified_hensel_pi56.json` gives the actual root modulo pi56.
It recomputed q0..55 over `Z/(101^8)`, then used
`q^(i+7k) -> 101^k*pi^i`. All6960 formal equations and all1650 directly
evaluated ramified-ring equations passed. Runtime205.537s,63.9MiB.
This is a new **mixed-characteristic point-field calculation**, not an
extension of the failed F101(q) rational-closure search.

**FAILED bounded small-field extraction:** the first dependent coefficient's
constant-basis residue is5101489845552212 modulo101^8. It has no rational
representative with both numerator and denominator of absolute value at
most10^7. Hence the attempted presentation of all theta values in the
power basis of Q(pi), with that height bound, fails. The condition
`2*(10^7)^2 < 101^8` makes rational reconstruction unique in this box.
This is **not** a proof that L differs from Q(pi); larger-height rational
coefficients or another small number field remain possible. No guessed
field model was sent to a smoothness or conormal routine.

## Executed primary controller: bounded rational closure failed

**FAILED bounded rational ansatz; not a failure of smoothing.** The prepared
controller was executed under the new authorization. The specified normalized
equivariant curve was lifted over F101 through order24 and then32. All6960
Schur equations passed at every completed order, and the certified embedded
six-jet was retained. No common denominator of the prescribed tested degrees
closed the model. At order32 every Padé system for denominator degree0..10,
numerator degree at most denominator degree+6, was inconsistent.

The field of this intermediate calculation is F101, with coefficients in
F101[q]/(q33); this is a jet, not a model over F101(q). No finite closed
fibre is claimed from this jet alone, and no further order is requested for
this rational-function ansatz. The actual fibre above uses a different,
rigorously justified ramified-point extraction.

Measured guarded times: order24,20.247s/28736KB sampled RSS; closure24,
2.362s/24120KB; continuation24→32,17.833s/28912KB; closure32,
2.378s/24376KB. All stages respected their1800s/2800MiB ceilings.

Checkpoints: `logs/20260908T121238-night-curve-24.artifacts/` and
`logs/20260908T121301-night-curve-32.artifacts/`. Exact failed fit records
are in the corresponding closure artifact directories. Input/script hashes
are embedded in every checkpoint.

## New mathematical reduction for Picard and Hodge numbers

**PROVED, conditional on the accepted smooth-fibre and resolution inputs:**
if n=h0(N) and r=dim(I²)_8 on a smooth characteristic-zero fibre, then

    h11=1748+n−r.

The derivation is in `DEGREE8_PICARD_FORMULA.md`. The antisymmetric summand
of the tensor square of the length4 self-dual resolution has homology
sheaves C=I/I² and Λ³C in degrees1 and3. Ambient Serre duality reduces
the needed conormal H2 to a four-term scalar complex. Self-duality identifies
its final cokernel with the graded module C(8), giving the displayed formula.
There is no assumption that an ordinary square resolution stays exact at
the singular special fibre.

**PROVED within the accepted smoothing trust boundary:**

\[
\rho=h^{1,1}=1,\qquad h^{2,1}=31,\qquad
\chi_{\rm top}=c_3=-60,\qquad\dim\mathrm{Hilb}_{[X]}=94.
\]

**COMPUTER-CERTIFIED and independently rechecked over the integers:**
twelve first-order product pivots give a minor with determinant
−3³·8⁹=−3623878656. The full product-matrix minor has leading term
q12 times that nonzero integer; all unknown higher corrections contribute
only later powers. Thus r≥1841 already follows from the first-order
direction, without characteristic-zero reconstruction or I² semicontinuity.

The conclusion is the short chain

\[
1\le h^{1,1}=1748+n-r\le1748+94-1841=1.
\]

All inequalities are equalities: r=1841,n=94,h11=1. The normal Euler
sequence gives n=63+h21, hence h21=31. There is also a direct obstruction
calculation: H1(N) is the kernel of H2(T_X) -> H2(TP7|X)=k. The dual
map sends1 to c1(H) in H1(Omega_X); when h11=1 it is an isomorphism.
Thus H1(N)=0, and the local Hilbert scheme is smooth of dimension n=94. Its
component specializes to X_M. This proves an actual94-dimensional
smoothing component, not merely the old upper bound. It does not assert
that the full Kuranishi equations vanish on the raw P1³ parametrization.

Because H1(O_X)=H2(O_X)=0, the exponential sequence identifies Pic(X)
with H²(X,Z); its rank is h11. This does not remove torsion. The ample
class generates Pic(X) modulo torsion (its cube20 precludes a nontrivial
integral multiple in a rank-one lattice). Thus Pic(X)/torsion=ZH;
torsion, Pic(X)=ZH, and the fundamental group remain OPEN.

The product matrix has6435
rows and4896 columns; its central monomial rank is1829. Only12 additional
q-adic pivots were needed. The search found them modulo101 and then
computed their exact INTEGER minor, removing even the modular-transfer
obligation. The rank certificate is in `PRODUCT_RANK_CERTIFICATE.md` and
`logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json`.
An independent parser, exponent-subtraction calculation and rational Gaussian
determinant verify all144 entries in `certificates/independent_product_minor.json`.
The source first-order corrections agree exactly with the certified six-jet
coefficient, with no reparametrization or coordinate identification needed.

The pivot search itself took0.189s (guard wall1.316s); its one-second
RSS sampler missed the short-lived peak. The independent recheck took0.657s.
No heavy I² resolution or higher resolution-map lifting was needed.

For the actual ramified point, same-component membership and smooth-proper
Hodge constancy give the identical pair. Independently, its first jet
modulo pi² gives the same product minor as pi12 times a unit, by eliminating
the1829 central unit pivots before dividing the remaining12 columns by pi.
There is no unjustified transport of a degree12 determinant through only
six-jet precision. See `SPARSE_AND_RAMIFIED_REVIEW.md`.

## Algebraic extraction after failed rational closure

**COMPUTER-CERTIFIED reduction:** the equivariant central multiplication
map splits into three representation blocks. The image/kernel/standard-row
multiplicities are (21,5,47),(13,5,35),(32,10,75). Auxiliary syzygy
coordinates reduce from2940 to490, and lower equations from6960 to1160.
The largest inversion block is32 rather than98. Exact rational basis maps
are saved in `data/equivariant_blocks_QQ.json`. Construction used10.36s
and about21MiB sampled RSS. Polynomial elimination removed59 variables,
but grew from83843 to298949 terms and stopped at the planned300000-term
gate:701 dependent variables and1591 equations remained. This used177.653s
and181.61MiB. No blind large Gröbner calculation was launched. The later
bordered-determinant formulation eliminates all490 auxiliaries without
expanding expressions, leaving only270 dependent coefficient numbers.

## Other failed attempts and their exact meanings

| Attempt | Result and legitimate conclusion |
|---|---|
| Same first-order direction, linear free path | **FAILED** shared and generator-only rational fits through32 at the recorded bounds; no claim about all rational presentations. |
| Primitive coordinate recognition on the two original32-jets | **FAILED** all297 overdetermined probes per curve: degree in the tested coordinate2..4, q-degree<=6, at most28 unknown monomials. No small algebraic relation in this specified window. |
| Raw six-jet or either saved F<=4 truncation treated as polynomial generators | **FAILED** flatness: actual99-minors in degree-four multiplication are nonzero modulo101; the required central rank is98. This rejects these generator truncations even with arbitrary corrected syzygies. |
| Linear equivariant kernel graph U=qU1 | **FAILED** at q², with700 nonzero residual entries. |
| Two-orbit sparse direction O3=O8=1 | **FAILED before lifting:** a preserved diagonal grading forces a cubic threefold component in the coordinate P4. No computation was wasted on this nonsmoothing path. |
| Three-orbit O3=O8=O10=1 | Tangent and degree8 minor checks **COMPUTER-CERTIFIED**, all6960 coefficients vanish through32; every tested shared/generator-only Padé fit **FAILED**. It has a different tangent and was not silently substituted for the target. |
| Direct polynomial peeling | **FAILED as a practical field extraction** at its expression-growth gate; exact59-variable reduction retained. |
| True pi56 relative-degree recognition | **COMPUTER-CERTIFIED:** for both theta1 and theta2, there is no nonzero relation of relative degree<=3 with integral pi-basis coefficient height<=1000. Exact lattice reduction followed by exhaustive sphere enumeration supplies the bounded exclusion. This is not a theorem about the unbounded field degree. |

Exact inputs, degree bounds and residuals are retained in the timestamped
logs and `ALGORITHMIC_REDUCTION.md`, `TRUNCATED_GENERATOR_REJECTIONS.md`,
`EXTRACTION_RECOMMENDATIONS.md`, `SPARSE_DIRECTION_REJECTED.md`, and
`SPARSE_THREE_ORBIT_ATTEMPT.md`. None disproves the algebraic curve or the
smoothing. The primary chart recurrence was never increased past order32.
The precise field-height scopes and exact Gram--Schmidt exclusion argument
are in `BOUNDED_FIELD_SEARCH.md`. Its initial four-probe job used44.213s
and15.59MiB. The two cubic iteration caps were continued only after exact
potential-decrease and checkpoint-replay checks proved measured progress;
the audited completions used4.792s and5.306s. The final height1000 sphere
enumerations used1.216s and1.197s under the guard, respectively. Each
exhausted its sphere in34 assignments and found only the zero vector.
The sphere of squared radius28,000,000 contains the entire cubic height
box, so this is a rigorous negative result, not merely failure to find a
short LLL basis vector. No extra pi precision was requested, and no
modular short vector was promoted to a global equation.

## Resource and provenance record

All100 daytime artifact hashes and the six frozen source HEADs verified.
Scripts were copied into this run. The copied runner enforces single-thread
settings, one exclusive computational lock, monitored process-group RSS≤
2800MiB, attempt≤3600s, no long launches after16:00 and owned-process
cutoff16:35, reserving the16:45 handoff. It never kills unrelated processes.
The copied primary controller retains1800s stages; only its superseded
night-only time gate was removed. Python used is3.13.7.

**FAILED then repaired preflight:** the chart builder's repeat-input
assertion compared tuples against JSON lists. Canonical JSON comparison
fixed that serialization-only issue; the existing chart was untouched and
the chart and six-jet regressions then passed. All failed logs are retained.
The first mixed-characteristic invocation likewise stopped before lifting
on sparse dictionaries retaining zero entries; cleaning those entries
repaired the representation-only assertion. Its failed source and log
are preserved. One closure invocation used an incorrect timestamped path;
the file-not-found log and corrected invocation are both preserved.

All successful substantial stages took under3.5minutes and
under182MiB sampled RSS, despite the broader authorization. No CAS or
Gröbner process, I² resolution, package installation, push, linkage search,
or skeletal-polytope computation has been launched. Process metadata can
be inventoried with `python3 scripts/summarize_runs.py`.
The37 guarded records total592.041 seconds of wrapper time; this includes
failed attempts and is not the full research-session wall time.

## Claim/dependency ledger

| ID | Claim | Status / dependency |
|---|---|---|
| C01 | The prepared curve jet satisfies all equations through32 | COMPUTER-CERTIFIED; normalized six-jet and frozen chart |
| C02 | The prescribed bounded common rational ansatz closes | FAILED; exact inconsistent fit systems, no nonexistence claim outside bounds |
| C03 | h11=1748+h0N−dim(I²)_8 | PROVED within analysis; smooth CY/self-dual resolution, explicit derived-complex argument |
| C04 | Degree8 product rank≥1841 | COMPUTER-CERTIFIED; explicit integer minor and independent recheck |
| C05 | rho1,Hodge(1,31),Hilbert dimension94 | PROVED within accepted smoothing boundary; C04+C03+accepted h0N≤94 |
| C06 | A specified smooth closed fibre over a number field | PROVED within the accepted boundary; finite271-variable coefficient-point export, Hensel selector, transported smoothness identities |
| C07 | Compact primitive-element field presentation | OPEN; bounded Q(pi) coefficient-height extraction FAILED, no nonmembership theorem |

Dependency chain: integral normalized jet -> exact matrix-rank lower bound
-> C04; C03+C04+known n≤94+h11≥1 -> C05. Effective field/point extraction
and the ramified transport of the existing smoothness certificates -> C06.
C05 does not require C06. C07 is a practical field-representation problem,
not a remaining existence, smoothness, or Picard-rank obligation.

## Completed handoff and tonight

The final independent replay passed both checks at14:29: the integer
product certificate in1.189s and the algebraic-coefficient export check
in1.190s. These short jobs finished between RSS samples, so their tiny
sampled values are not meaningful peak-memory estimates. No owned
computational process remains running. The original100-file daytime
manifest was reverified unchanged; this packet is frozen separately in
`ARTIFACT_SHA256SUMS`.

The updated standalone instructions are in `OVERNIGHT_PROMPT.md`, with
the strict queue in `HEAVY_QUEUE.md`. The first continuation command, in
a fresh run with the copied guard's dates adapted as specified, is

    python3 -B scripts/replay_certificates.py --run

It executes only the two small independent checks. There is **no justified
mandatory heavy job left in the prepared queue**: the Picard/Hodge problem
was solved by a smaller exact argument, and the prescribed rational and
bounded field ansätze were exhausted. A further field-extraction job needs
a genuinely new reduction before launch. Do not restart the exhausted
Padé controller or resolve I² just to reconfirm the established invariants.
Picard torsion, the fundamental group, a compact coefficient field, and
literal equality with the raw full P1³ Kuranishi ideal remain OPEN.

For Friday, read this report, `GEOGRAPHY_THEOREM.md`, and
`FRIDAY_READY_BRIEF.md`; keep `RAMIFIED_FIBRE_EQUATIONS.md` available for
the actual coefficients. The targeted mathematical-paper-audit procedure
kept the new proofs, exact certificates, original trust boundary, and
bounded failures separate; it is not an assertion of human verification.
