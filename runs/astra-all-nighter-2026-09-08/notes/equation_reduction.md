# Coefficient reductions checked during the new run

Scope: a concrete alternative to repeating the failed selected-curve fits
or expanded elimination. The completed computation/daytime packets are
read-only. This note distinguishes a verified linear-algebra reduction
from a constructed smooth fibre. Mathematical-paper-audit targeted
verification conventions are used; no qualified-human verification is claimed.

## Explicit coordinate gauge, and why this alone is not a new search

**PROVED by the following exact derivative computation.** In the eight
coordinate variables the six displayed permutations have fourteen orbits
on ordered pairs. An equivariant infinitesimal coordinate change is a
constant matrix on each ordered-pair orbit. The three diagonal orbits are
`{a,c,g}`, `{b,e,h}`, `{d,f}`. Each diagonal change preserves the monomial
ideal and acts trivially on its normalized coefficient point. Every one
of the eleven off-diagonal orbits has a distinct unit coordinate in the
recorded twenty-one free coordinates. Thus the matrix action has rank
eleven and kernel dimension three. After projectivizing, the centralizer
has dimension thirteen, its stabilizer dimension two, and its orbit
dimension eleven. The fixed Hilbert tangent is twenty-one-dimensional,
so a transverse fixed slice has dimension ten, not eight.

The exact nonzero free-coordinate derivatives are listed below. Indices
are zero-based chart coordinates. In each row there is exactly one such
free coordinate and its coefficient is one. All other free derivatives
are zero. The ordered pair `ab`, for example, denotes the vector field
`b*d/da`.

| Coordinate | Ordered-pair orbit |
|---|---|
| 232 | ab, ah, ce, ch, gb, ge |
| 233 | ac, ag, ca, cg, ga, gc |
| 234 | ad, af, cd, cf, gd, gf |
| 196 | ae, cb, gh |
| 255 | ba, bg, ec, eg, ha, hc |
| 266 | bc, ea, hg |
| 256 | bd, bf, ed, ef, hd, hf |
| 203 | be, bh, eb, eh, hb, he |
| 281 | da, dc, dg, fa, fc, fg |
| 285 | db, de, dh, fb, fe, fh |
| 276 | df, fd |

To reproduce the argument, differentiate each of the sixteen displayed
squarefree cubics under these vector fields, discard the sixteen central
monomials (the generator normalization), and read the coefficient orbits
in `data/fixed_chart.json`. The table contains an identity submatrix,
which proves both independence and transversality. The diagonal orbit
directions exhaust the kernel because the source has dimension fourteen.

The ten remaining free coordinates are
`37,38,46,64,89,163,172,229,230,262`.
Imposing the eleven gauge coordinates to be zero defines a smooth formal
slice: choose the corresponding eleven matrix directions in an affine
neighborhood of the identity, act on the generators, invert their central
16-by-16 coefficient matrix to normalize them, and apply the formal
implicit function theorem to the eleven gauge coefficients. Its derivative
is the identity table above. This argument gives a local formal/étale
slice; it does not prove that the slice or the normalization map is rational.

**Negative practical conclusion.** The original first tangent already has
all eleven gauge coordinates zero. The completed linear-free-path
experiment set all their higher coefficients to zero as well. Repeating
that slice construction and its same linear path would repeat a completed
failure, not improve extraction. The selected six-jet path has nonzero
gauge acceleration beginning in order two, but removing it alone does not
establish a smaller number field.

## New bounded syzygy-graph locus computation

The failed packet experiment fixed the original single tangent `t` and
tried `U(q)=q B(t)`. It failed at order two. The new script
`scripts/equation_reduction_linear_u_locus.py` varies `t` in all ten
intrinsic invariant tangent directions simultaneously.

Write `A=Id+A0`, and define

```
L(z) = (B(z),D(z)),
T_t(z) = (A0(z)B(t),C(z)B(t)).
```

The full incidence identities under this graph ansatz are
`Lz=q(B(t),0)+q T_t(z)`. A rank-291 left inverse `J` of `L`
forces the single rational candidate

```
z(q) = q (Id-q J T_t)^(-1) t.
```

The necessary order-two obstruction is the 1650-entry homogeneous
quadratic vector `(LJ-Id)T_t(t)` in ten parameters. There are just 55
quadratic monomials. Computing these 55 coefficient columns, rather than
performing nonlinear elimination in 760 variables, gives a small exact
necessary locus. The script first works modulo 101, records the elementary
operations expressing `J` in original rows of `L`, checks `JL(t_i)=t_i`
for every source tangent, retains every residual coefficient, and outputs
a basis of the quadratic row span. It also retains the original product
minor as an exact rational 12-by-12 linear pencil in the ten parameters.

The generated Singular input computes the quadratic locus and its
intersection with the principal open set where the product minor is
nonzero. This latter condition supplies the inherited product-rank lower
bound when a full flat family actually exists. It is not itself a
smoothness test. Empty modular open locus only excludes this ansatz for
directions whose product minor remains a unit modulo 101; one cannot
silently infer all characteristic-zero directions are excluded when
the open condition may disappear in reduction. Empty entire projective
quadratic locus would exclude characteristic-zero directions by properness.

**Success gate.** For any candidate rational tangent the whole rational
function must satisfy all full incidence identities over Q. Equivalently,
test `(LJ-Id)T_t(JT_t)^k t=0` for `k=0,...,290`; Cayley-Hamilton
then supplies all orders. An actual smooth specialization still needs
a separate projective smoothness certificate. A rational graph ray with
a changed tangent does not inherit the recorded six-jet smoothness.

**COMPUTER-CERTIFIED outcome.** Root's J003 ran the modular pilot in
2.113 guarded seconds. The quadratic row span has rank 41 of 55.
`data/linear_u_locus_p101/necessary_locus.json` retains the whole system.
The first generated Singular command used an invalid `std` argument form;
the corrected `necessary_locus_fixed.sing` and builder `_v2.py` are separate
files, preserving the successful Python pilot's original source hash.
No mathematical assertion depends on running that Singular command.

**PROVED from an exact rational certificate.** Root's J005 ran
`equation_reduction_linear_u_QQ_certificate.py` in 1.063 guarded seconds
(0.676 internal seconds). Let `L_i` denote zero-based scalar row `i` of
`L=(B,D)` in the recorded block order, and `H_i` the corresponding row of
`T_t(t)`. The exact rational source matrices give

```
L_645 = (L_13-L_158)/2,
L_652 = 0,
(H_13-H_158)/2-H_645 = -t8^2,
-H_652 = t9^2.
```

Every order-two solution must therefore satisfy `t8=t9=0` over any
characteristic-zero field. The recorded product pencil has diagonal
`(-t3,-t3,-t3,-t8,-t8,-t8,t8,-t8,-t8,-t8,-t8,-t8)` and three
off-diagonal entries `-t2` at `(0,1),(1,2),(6,0)`. There is no off-diagonal
cycle in its determinant expansion, so its determinant is `-t3^3*t8^9`.
Consequently **every** graph ray of this ten-parameter ansatz misses the
recorded product-minor open set, over every characteristic-zero extension.
This is a global exact exclusion within the specified ansatz, independent
of coefficient-height bounds. It does not prove every such ray singular:
vanishing of one selected product minor is only a necessary failure of
that particular geography certificate.

The small proof objects, exact row combinations, four used quadratic RHS
rows, and source hashes are in
`data/linear_u_QQ_certificate/linear_u_QQ_certificate.json`.

## Sparse path parity and a separate bounded algebraic test

The completed sparse direction uses intrinsic orbits 3,8,10 with unit
weights. Its exact exponent equations show that simultaneous negation
of `d,f,q`, fixing the other six coordinate variables, preserves every
first-order cubic. This involution commutes with S3 and preserves the
normalized chart/free-coordinate split. All prescribed nonzero free
coefficients are odd multiples of `q`; the other free paths are zero.
Uniqueness of the origin-selected formal solution therefore implies

```
z_j(q)=q^(epsilon_j) f_j(q^2), epsilon_j in {0,1},
```

where `epsilon_j` is the parity difference between the tail monomial and
its central generator in the variables `d,f`. This is an exact formal
identity in characteristic zero and characteristic 101, rather than
an observation from repeated jet coefficients. The script checks the
exponent equations, commuting action, all orbit parities, and every saved
coefficient through order 32. There are 127 nonzero coordinate series in
that saved jet; no assertion says the other 164 vanish identically.

**FAILED within declared finite supports.** Root's J004 ran
`equation_reduction_sparse3_parity_fit.py` in 1.052 guarded seconds
(0.027 internal seconds). It fitted exactly dependent coordinates
`7,101,109,35,39` after initial `q` valuation removal in the variable
`s=q^2`, and after further removing the constant and the next `s`
valuation. Rectangular supports were `(degree_T,degree_s)` equal to
`(2,2),(2,3),(3,2),(4,1)`. Each admissible support had at least four more
available equations than unknowns, and no zero monomial columns.
All 25 admissible matrices had full column rank; 15 requests were skipped
for insufficient holdout coefficients. No algebraic candidate was found.
No jet was extended. Full matrices can be rebuilt from the retained
series/supports and rank routine in
`data/sparse3_parity_algebraic/parity_fit.json`.

This differs from the completed packet: its algebraic fitting had tested
the original six-jet and original linear-free paths; the sparse path had
only undergone rational fitting. The new negative result still does not
exclude higher-degree or larger-support algebraic presentations.

## Optimizing all second-order freedoms

The next prepared exact test fixes the original first tangent but allows
all 21 second-order embedded invariant freedoms. The inherited exact
second coefficient `z2_0` satisfies `D(z2_0)=C(t)B(t)`. Since the chart's
linear tangent kernel has dimension 21 and the ten intrinsic directions
plus the eleven gauge vectors give a unit free-coordinate submatrix,
every possible `z2` is `z2_0` plus their arbitrary linear combination.

For `z(q)=q*t+q^2*z2`, flatness at order three requires the affine-linear
system

```
C(t)B(z2)+C(z2)B(t)-C(t)A0(t)B(t)=0.
```

The same script also treats
`z(q)=(q*t+q^2*(z2+d*t))/(1+d*q)`. Here `z3=-d*z2`, so the left side
acquires `d*D(z2)=d*C(t)B(t)`, another affine-linear column. Thus the
polynomial and rational ansätze require only 1160-by-21 and 1160-by-22
rational linear systems. This varies the entire second-order path,
instead of repeating a Padé fit to any fixed previously computed curve.
`scripts/equation_reduction_quadratic_generators.py` reconstructs the
exact normalized two-jet, checks all order-two identities, and preserves
either a direct rational contradiction or a complete affine solution
space. Its guarded execution belongs to root.

**PROVED, via COMPUTER-CERTIFIED exact rational identities.** Root's J009
completed in 3.695 internal seconds. Both optimized ansätze are excluded
over every characteristic-zero extension by a single equation: flattened
lower row 8, namely trivial block row 1, column 3 (all zero-based), is
the constant `-48` for every one of the 21 second-order freedoms and
for the additional scalar denominator. The certificate is
`data/optimized_quadratic_generators/quadratic_generator_certificate.json`.
The entire affine row is retained, and the contradiction combination is
just that original equation with coefficient one. This rules out the
specified freely optimized low-degree paths; it does not rule out short
cubics in a different generator normalization or longer rational paths.

## Polynomial generators before normalization

A scalar common denominator need not capture a short generator matrix.
The permutation representation on the sixteen central cubic generators
has 51 ordered-pair orbits, so its equivariant endomorphism algebra has
dimension 51. For an arbitrary such matrix `G2`, raw quadratic generators

```
Fraw = F0*(Id+q^2*G2)+q*T+q^2*Z2
```

normalize to `z=(q*t+q^2*z2)*(Id+q^2*G2)^(-1)`. Their third normalized
coefficient is `-t*G2`, so the preceding affine system acquires 51 columns
`D(t*G2)`. This is a 72-variable affine rational test; its matrix
endomorphism directions and exact source/tail coefficient maps are built
by `scripts/equation_reduction_matrix_denominator.py`. Optional scalar
linear matrix coefficient `d*Id` gives a separate 73-variable test.

The preceding row-8 obstruction predicts a precise limitation: its linear
form is `D_8=-z_155+z_215`. Representatives of these coefficient orbits
are respectively the `b^3` tail of generator `abg` and the `gh^2` tail
of generator `acg`. Neither tail monomial appears in any first-order
correction `T_i`; hence both remain absent in every `T*G2` and this
particular matrix normalization cannot repair row 8. They do appear in
the union of second-order correction monomials, so a general linear
matrix coefficient `G1` can potentially repair it. With `z2` fixed to
the inherited second coefficient, the condition for denominator
`Id+q*G1+q^2*G2` becomes the still affine 102-variable system

```
residual(z2)+D(z2*G1)+D(t*G2)=0.
```

This last display is implemented in the syntax-checked, unexecuted
`scripts/equation_reduction_linear_matrix_denominator.py`. Its required
`--base` argument is the J009 certificate above; the declared internal
limit is 120 seconds. It preserves a complete rational affine solution
space or a direct exact contradiction. Allowing all 21 `z2` freedoms
together with all `G1` entries would introduce bilinear terms and is a
different problem.

Budget handoff: after preparing this 102-variable pilot, this agent stopped
further exploration as instructed. Root owns its possible execution.
No process was left running by this agent.

## Requested continuation after the measured 102-variable failure

Root reports J012 inconsistent over Q: 59 pivots precede a direct
contradiction `-50075/38`. The new bounded continuation combines the
previously separate freedoms, keeping the original first tangent and
writing `z2=z2_0+sum(s_i*v_i)` with all 21 embedded invariant directions.
Together with arbitrary equivariant `G1,G2`, the necessary order-three
system has 123 variables and formula

```
R(z2_0+sum(s_i*v_i))
  + D((z2_0+sum(s_i*v_i))*G1) + D(t*G2) = 0.
```

The `G2` matrix still enters by a constant 1160-by-51 linear map. Thus
constant Gaussian elimination removes its image exactly, leaving
quadratic equations in the 72 variables `(s,G1)`. If that constant map
has rank below 51, the unused `G2` parameters remain free at this order;
they must be preserved in the reconstruction rather than falsely
reported as uniquely eliminated. Triangular back substitution recovers
all pivot `G2` entries from the quadratic residual polynomials and these
free `G2` parameters.

Prepared, not run by this agent:
`scripts/equation_reduction_combined_matrix_pilot.py`. It uses only F101,
reconstructs the 21-by-51 bilinear columns from the exact chart and matrix
orbits, records the entire original system, and checks every saved
constant row-operation identity directly against the original equations.
After removing `G2`, it performs only substitutions `x=-f/a` where `a`
is a nonzero field constant and `f` does not involve `x`. These
substitutions are polynomial isomorphisms of the corresponding zero
sets, with the inverse maps retained in reverse reconstruction order.
No parameter-dependent denominator, Gröbner basis, or CAS job is used.

Defaults are 180 internal seconds, 100000 total terms, 2000 terms per
polynomial, degree at most 4, and 20 substitutions. Each proposed
substitution is computed transactionally and discarded if it exceeds
the caps. Original equations, the constant-elimination certificate,
remaining equations, reconstruction maps, size measurements, and a
separate Singular input are saved. A capped constant-elimination stage
has an executable `--resume` checkpoint; a completed peeling stage saves
its equations and reconstruction for a later explicit continuation.

This remains a necessary F101 locus. Empty affine reduction modulo 101
does not by itself exclude characteristic-zero solutions with
101-denominators. A surviving point needs every higher incidence identity,
an appropriate branch/component connection, and geometric smoothness.
Following the explicit budget instruction, this agent again stops after
supplying this bounded pilot. Root owns its execution and any subsequent
CAS pilot justified by the measured size.
