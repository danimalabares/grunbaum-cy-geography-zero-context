# Ranked routes to finite equations

The primary route has changed in response to the actual daytime
calculation. **PROVED:** one does not need to prove the full38-dimensional
P1 component to effectivize the equivariant smoothing. The finite fixed
chart in `FIXED_CHART.md` already supplies an algebraic curve with a
prescribed six-jet and smooth geometric generic fibre, subject to the
existing smoothness trust boundary. The remaining computational task is
to make that curve's field and a particular fibre manageable.

| Rank | Route and status | Plausibility / cost | Exact success / information | Principal failure mode |
|---|---|---|---|---|
| Primary | Fixed291-coefficient chart; constant270-pivot recurrence; rational reconstruction | Algebraic existence PROVED; low-degree rationality HEURISTIC. Modular orders24/32 inexpensive relative to universal lifting | Exact rational FR identity gives usable finite family; then certify fibre and Hodge data | Algebraic curve may not admit small rational coefficient functions |
| Backup1 | Algebraic elimination of the same fixed curve, after symmetry and linear-block reduction | PROVED finite algebraic system; computational cost uncertain, potentially large | Finite field extension or number-field point on origin branch, verified against all full equations | Degree/height explosion; extraneous remote components; unresolved branch isolation |
| Backup2 | P1 rank-one substitution before universal lifting, blockwise exact ideal identities | Plausible but OPEN all-orders; cost moderate-to-high even after reduction | A full38-parameter flat family of image dimension38 with smooth member proves Hilbert dimension94 and h21=31 | Package gauge mixes blocks at higher order; twelve reduced equations may persist |

No fourth priority route is queued. The alternatives below are triaged to
make the choice and its limitations explicit.

## Line-by-line audit of p1_universal_exact_test.m2

Source: frozen commit ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b,
`reconstruct/p1_universal_exact_test.m2`,78 lines.

| Lines | Mathematical assertion or operation | Actual scope / bottleneck |
|---|---|---|
| 1–3 | Comment promises full polynomial closure by orderfive | Stale: executable requests orderfour |
| 5–10 | Load package, define S,I,F0 | Eight projective variables,16 cubics |
| 11 | Hom(I,S/I)_0 basis |16×109; repeated recomputation unnecessary for saved-state test |
| 12–14 | Select53 intrinsic columns | Fixed complement, not canonical abstract coordinates |
| 15 | Complete degree-zero T2 basis |30×27; useful for new lifting, unnecessary to specialize saved matrices |
| 17–18 | Build universal deformation through order4 | Ring has8+53 variables; F1×16, R16×30, G27×1, C30×27; PolynomialCheck=false does not disable default SmartLift |
| 19 | Sum finite base terms | Tests only degrees through4, not the completed base |
| 20–27 | Save four coefficient lists | These already exist, total about1MB; source script would overwrite frozen files |
| 28–34 | Log finite base and list lengths | Output(5,5,3,3), base_zero=false is expected for universal obstructed base |
| 38–45 | Map53 parameters to one sparse q-line | Uses38 specified1s and15zeroes; distinct from final orbit weights1,...,10 |
| 46–50 | Test specialized G=0 and exact polynomial FR=0 | Sufficient presentation-closure check for this line only |
| 51–58 | Log residual | Stored result: base_zero=true, FR_zero=false; residual starts atq5 and reachesq8 |
| 61–69 | If exact, check central generators and full syzygy image; save | These plus FR would prove DVR-flatness by the explicit torsion argument |
| 70–77 | Record certificate | Does not test geometric generic smoothness, correct finite nonzero fibre, or full38-dimensional image |
| 78 | Exit | No continuation or full global FR+CG verification is executed |

**FAILED:** the fourth-order sparse polynomial presentation does not close.
This is a real exact negative test for that candidate, not a failure of
smoothing. **OPEN:** previous orderfive universal attempts timed out after
about40minutes; an orderfour global-check attempt stopped after15minutes.
These timeouts have no mathematical verdict. Serialized sparse jets reach
order30, still without an accepted finite smooth model. They are not the
generic equivariant six-jet used in the final theorem.

### Where time and memory go

**PROVED from installed package source inspection:** liftDeformation
forms the next FR coefficient, quotients by leading base equations,
reduces against the action of R0, swaps projective/base variables to
extract obstruction coefficients, and divides by F0 plus initial base
equations to lift relations. Default SmartLift additionally constructs
and uses a correction matrix from all pairs of53 parameters. Thus there
are Gröbner/module divisions and coefficient expansion in a61-variable
ring, not merely a53×53 linear solve. A full fourth-order FR product has
parameter degree up to8, while later universal orders grow combinatorially.
Applying substitutions only after expansion misses most savings.

The saved files are approximately F358KB, R556KB, G1.7KB, C84KB.
Rebuilding them for a line test is unnecessary. Re-running the original
script in its source cwd also violates today's read-only requirement.

## The requested reductions, with precise outcomes

**PROVED finite-order reduction:** the three P1 matrices are printed in
`HILBERT_EXPLANATION.md`. Parametrize each by rows(u1,...,u6) and
r(u1,...,u6), using7 parameters on the chart where the first row is
nonzero. With17 free variables this uses38 coordinates. A globally
surjective cone parametrization uses two row scalars and six column
scalars per block, with a scalar redundancy. At the selected tangent
use t=qv and invert a leading first-row coordinate, not q in an Artin
quotient. Substitution before forming large FR coefficients kills all
minors identically and removes quotient Gröbner operations by P1.

**PROVED through degree4 only:** every added quartic term is a scalar
times a missing determinantal minor. For example in blockA the scalar
is t6+t42*t47. The three blocks are related by renaming. Reducing one
block's determinantal relations, keeping cross-block coefficients as
scalars, proves the displayed27 equations vanish. It does not prove
that higher corrections remain blockwise. No universal all-orders
determinantal identity was found today.

**PROVED S3 reduction:** on the fixed ten-plane all18 vertically paired
entries coincide. The complete invariant obstruction space is zero, so
the invariant formal problem is unobstructed. Raw package coordinates
need not linearize the action beyond first order; simply imposing equal
t_i in every unaveraged higher-order presentation is not justified.
The normalized invariant generator chart enforces the actual action.

**PROVED 15-coordinate limitation:** after blowing up t=qv, the existing
15×15 minor solves15 dependent coordinates. Its twelve complementary
obstruction coordinates still need to vanish or admit a curve. The
projected quadratic term on ker(dG2) vanishes for determinantal reasons,
so the old proposed rank12 implicit-function argument at that weight
does not finish the problem. By contrast the new270-pivot construction
uses all-orders unobstructedness of the fixed germ to dispose of its
remaining equations.

**HEURISTIC sparse-line option:** preserve exactly the current first-order
direction by setting the21 free normalized chart coordinates to their
linear terms only. This defines an algebraic curve, but its smoothing
requires a new certificate; agreement through first order is insufficient.
Keeping the six-jet free paths costs little more and retains the existing
smoothness proof, so the supplied recurrence makes that choice.

**PROVED marked-chart choice:** the cubic Grassmann chart with the30
lifted linear syzygies is finite and local-flat by syzygy lifting. A
term-order marked Gröbner chart may be too restrictive; a general
Gotzmann Grassmannian chart or a20-dimensional Artinian border-basis
construction introduces additional regularity/linear-section choices.
These are credible constructions but currently less economical.

**OPEN polynomial/algebraic ansatz:** finite-order vanishing is never
termination. For polynomial F,R verify exact FR=0; for rational entries
clear all denominators and verify every coefficient, with denominator
nonzero at0 and complete central syzygies. For algebraic coefficients
specify their finite equations, the origin branch, exact ideal membership
of FR, and the generic dimension/field. The new implicit chart does this
locally; extracting a small field or a numerical parameter remains open.

**FAILED cheap test today:** the normalized generator six-jet and its
canonical syzygy six-jet, regarded as a polynomial pair, have first nonzero FR coefficient
at q7: residue37 modulo101 in quartic row0/relation column0. All entries
through q6 are zero. This is saved in the sixjet-polynomial-negative log;
it rejects this truncated pair and leaves the implicit continuation intact.
It does not by itself rule out higher-degree or rational syzygies for
the same degree-six generator polynomials; no such stronger claim is made.

## Four inequivalent success levels

| Output | Level | Verification needed |
|---|---|---|
| Literally the exact formal continuation |1 | Equality of all coefficients in a fixed gauge, or an exact all-orders identity; the source does not select a unique continuation |
| New curve with the prescribed embedded six-jet |2 | Normalize generator pivot matrix; compare moduloq7; record invertible generator/syzygy changes; preserve101-integrality for inherited certificate |
| New curve with the same tangent only |3 | Equality in Hom(I,S/I)_0, or equality modulo coordinate orbit if that is the stated equivalence; new smoothness argument |
| Another smoothing through X_M |4 | Exact flatness, central fibre, generic smoothness; component relation must be supplied independently |

Our primary and backup1 are level2. A P1 universal family restricted to
an arbitrary line is generally level3 or4, until its higher coefficients
are matched. A smoothing on the same localized smooth S3-fixed germ is
on the zero-context component even without jet equality; this component
argument is proved in `HILBERT_EXPLANATION.md` and is stronger than
merely sharing P1 in the tangent cone.

For a proposed coordinate/reparametrization identification write
x↦A(q)x, q↦c1q+... with det A(0)≠0,c1≠0, and generator and
syzygy matrices P(q),Q(q) with unit constant determinants. Check
F_new=F_old(A(q)x,phi(q))P(q) and the corresponding syzygy equality
coefficientwise to the claimed order, or equality of ideals plus explicit
inverse membership matrices. Equality in T1 alone is the quotient test
modulo the64 coordinate-derivation columns. The older-data packet gives
an exact instance where tangents share P1 but fail that equivalence.
