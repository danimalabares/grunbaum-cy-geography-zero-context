# A finite algebraic fibre selected by ramified Hensel lifting

2026-09-08. This is a mathematical construction, not a claim that a small
primitive-element polynomial has been computed. It uses the original
six-jet free-coordinate curve, not the later linear-path experiment.

## Executed final presentation and independent review

**COMPUTER-CERTIFIED.** The actual exported presentation has only 271
algebraic variables: pi and the 270 dependent generator coefficients.
The 490 equivariant syzygy auxiliaries have been eliminated by 270
bordered determinants of sizes 22, 14, and 33. All shared rational matrix
factors, all 21 original free-coordinate polynomials, and the complete
16 cubic equations are explicit in `data/ramified_fibre_coefficients.json`
and `RAMIFIED_FIBRE_EQUATIONS.md`. The selected 270-square Jacobian has
determinant 19 modulo 101. The larger 3210-variable system below records
the initial proof construction; it is **not** the final export size.

**CONDITIONAL only on the stated source/chart certificate boundary.** The
independent mathematical review `RAMIFIED_POINT_REVIEW.md` accepts the
ramification, algebraicity, smoothness transport, and component arguments.
The construction is no longer merely awaiting its first independent
review. A primitive-element presentation of the number field remains open.

**COMPUTER-CERTIFIED genuine arithmetic.** A new computation over
Z/(101^2), followed by pi^7=101 substitution, has computed this root modulo
pi^14. All 1650 full equivariant block equations vanish in the actual
mixed-characteristic quotient ring. See `RAMIFIED_HENSEL_ARITHMETIC.md`
and `data/ramified_hensel_pi14.json`; no F101 order-32 jet was reused.

## The conclusion and completed export

**PROVED within the accepted chart and frozen smoothness-certificate
trust boundary; the targeted review is complete in
`RAMIFIED_POINT_REVIEW.md`.** A
genuine smooth fibre can be specified today by finite polynomial equations
for its algebraic coefficients and a unique, explicit p-adic branch
selector. It is unnecessary to eliminate hundreds of variables to a
single minimal polynomial first.

**COMPUTER-CERTIFIED completed reduction.** The final presentation is in
`data/ramified_fibre_coefficients.json` and all sixteen cubics are displayed
in `RAMIFIED_FIBRE_EQUATIONS.md`. It uses only270 dependent generator
coefficients, plus pi: the auxiliary syzygy variables below have been
eliminated exactly by bordered determinants of sizes22,14,33. The reduced
selected Jacobian determinant is19 modulo101. The earlier3210-variable
description below explains the construction but is not the final export.

The essential choice is a *ramified* parameter:

    pi^7 = 101,
    K = Q_101(pi),
    O = Z_101[pi].

The polynomial T^7-101 is Eisenstein. Thus O is a complete discrete
valuation ring with uniformizer pi and residue field F101, and

    O/(pi^7) = F101[q]/(q^7),    pi <-> q.

In particular, the entire certified six-jet can be interpreted literally
over O/(pi^7), while the generic field K has characteristic zero. Taking
q=101 would not have this property and is not the proposed construction.

## Finite equations for the coefficients

**PROVED from the fixed-chart construction.** Let z_1,...,z_291 be the
normalized invariant cubic-generator coefficients, with 21 free and 270
dependent coordinates as stored in `data/fixed_chart.json`. For each free
coordinate j, prescribe

    z_j = sum_(n=1)^6 c_(j,n) pi^n,

where c_(j,n) are the *exact rational* normalized six-jet coefficients
computed from `equations/deformation_data.json`. Their denominators are
prime to 101. The 16 cubic generators are the finite expressions

    F_i = f_(0,i) + sum_(tail monomials m) z_(orbit(i,m)) m.

Let A(z), B(z), C(z), D(z) be the original marked degree-four chart blocks.
Use the finite polynomial equations

    A(z) U = B(z),
    [D(z)-C(z)U]_(selected 270 entries) = 0.

There are 2940 auxiliary U entries and 270 dependent z entries. At the
origin, A=I, U=U_0, and the coefficient Jacobian determinant is a unit:
after eliminating the linear U block its remaining determinant is -1.
The exact coordinates and selected rows are part of the saved finite data.
The rational Schur formulation is equivalent on det(A)!=0.

**PROVED by multivariate Hensel lifting.** This finite system has a unique
solution satisfying

    z_dependent in pi O^270,    U-U_0 in pi O^2940.

Its Jacobian is still a unit because its reduction is the central one.
This is a precise algebraic-number branch selector, not an unbounded
choice of a formal arc. The normalized certified six-jet solves the
system modulo pi^7, so uniqueness gives equality with that six-jet modulo
pi^7. Polynomial denominators originally inverted in Z_(101) remain units.

**PROVED using the omitted-equation identity already established for the
fixed chart.** All other Schur equations also vanish. Their formal
remainders are zero in Z_(101)[[z_free]]; substitution of the prescribed
free coordinates in pi O converges in O. Consequently the lifted 30
canonical linear syzygies are exact. Reduction gives the complete central
linear-syzygy module, so the degreewise syzygy flatness argument applies
over the DVR O. This is the same mathematical flatness argument as in
`FIXED_CHART.md`, not a new inference from the finite truncation alone.

## Why these are algebraic numbers

**PROVED.** Regard pi as the specified root of T^7-101 and the solution
coordinates as elements of K. The coefficient Jacobian is invertible at
this solution, so the corresponding fibre of the finite system over
Q(pi) is etale of relative dimension zero at the chosen point. Its residue
field

    L = Q(pi, z_dependent, U)

is therefore a finite extension of Q(pi), embedded in K by the specified
Hensel branch. The F_i are 16 finite cubic equations over the number field
L. A primitive element and multiplication table would make this field
representation more convenient, but are not required to define the
algebraic numbers uniquely.

There may be other global solutions or positive-dimensional remote
components of the finite equations. They are not silently included:
the congruence conditions above select the unique O-valued Hensel root.
The intended presentation is an algebraic-number system with a p-adic
isolating condition, not the full global zero locus of the coefficient
equations.

## Transport of the smoothness certificates

**PROVED transfer, conditional on the accepted source certificates;
checked against the source in `RAMIFIED_POINT_REVIEW.md`.** The
frozen proof `PROOF.md`, section 4, uses only the following finite
characteristic-101 tests (source lines 235-301):

1. On the chart orbits represented by a=1 and d=1, q^5 belongs to the ideal
   of the equations and selected genuine fourth Jacobian minors modulo
   q^6. Equivariance covers a,c,g,d,f.
2. On the remaining triangle torus {b,e,h}, the leading Morse coefficient
   is q^2 times a polynomial p whose three polynomials p,p_u,p_v generate
   the unit ideal. The dead/critical linearizations and node coefficient
   are units on that torus.
3. On the remaining edge orbit, a localized q^4 identity holds modulo q^5.
4. At the remaining vertex orbit, (y_2-33)q^5 belongs to the selected
   singularity module modulo q^6, and y_2-33 is a unit at the vertex.

All these statements transport to O modulo pi^6 (or a smaller power)
because O/(pi^7) identifies with the certified truncated coefficient ring.
Normalization changes generator bases by a matrix that is a unit over O;
the full Fitting/Jacobian singularity ideal is invariant under this change.
The source certificates and exact basis change justify transporting the
identities rather than assuming individual chosen minors remain unchanged.

If the generic fibre had a geometric singular point, properness would
extend it after a finite extension of K to an integral section over the
corresponding DVR. Its special point lies in one of the four kinds of
strata above. Evaluation of the transported identity would put a unit
times pi^e in (pi^(e+1)), also after arbitrary ramification, a valuation
contradiction. On the triangle torus the same division and reduction uses
the displayed critical-value Bezout identity. This excludes every
geometric generic singular point.

Thus the fibre over K is smooth. Since the finite equations have
coefficients in L and K/L is faithfully flat, smoothness descends to L.
The special Hilbert polynomial and self-dual resolution then give a smooth
Calabi-Yau threefold of the required polarization type. Its membership in
the selected zero-context Hilbert component must be justified by the
existing fixed-germ component bridge, not by equality of all formal arcs.

## What remains computationally useful

**OPEN representation simplification.** Produce a compact primitive
element, a rational univariate representation, or a smaller triangular
presentation of L if desired for subsequent arithmetic. This is a
convenience and reproducibility improvement over the finite multivariate
presentation, not an additional existence argument if the construction
above is accepted.

**COMPUTER-CERTIFIED and mathematically reviewed in this run.** The exact
finite-chart flatness/localization argument and source smoothness orders
were checked in `RAMIFIED_POINT_REVIEW.md`; the denominator units and
Hensel-system data were exported and the displayed cubics independently
parsed back into their coefficient maps. Genuine mixed-characteristic
arithmetic modulo pi14 is in `data/ramified_hensel_pi14.json`.
Qualified-human verification remains appropriate. No claim is made that
an unramified specialization or a different first-order-only curve
inherits the six-jet smoothness certificate.
