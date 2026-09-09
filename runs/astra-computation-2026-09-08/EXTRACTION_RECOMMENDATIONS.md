# Concrete extraction reductions after the geography certificate

2026-09-08. This note is mathematical preparation, not a claim that a
new closed fibre has been computed. The first-order degree-eight
certificate has settled the geography on the selected smoothing component.
The remaining objective is a usable exact closed fibre.

## 1. First capped probe: make the syzygy graph linear

**PROVED reduction; OPEN outcome.** In the rational equivariant blocks
of `data/equivariant_blocks_QQ.json`, the incidence equations are

    (Id+A(z)) U = B(z),       D(z)=C(z)U.

Here A,B,C,D are linear in the291 normalized generator coordinates and
U(0)=0 because the central section is equivariant. The three blocks have
image/kernel/cokernel multiplicities (21,5,47), (13,5,35), (32,10,75).
Thus U has490 entries and the lower equation has1160 entries.

Let t be the *normalized exact first tangent*, put U1=B(t), and try
U(q)=qU1. This is a distinct ansatz from imposing linear free generator
coordinates. Define constant linear maps

    L(z)=(B(z),D(z)) : k^291 -> k^1650,
    T(z)=(A(z)U1,C(z)U1).

Then the complete incidence system is simply

    Lz=q(U1,0)+qTz.

**PROVED:** L is injective. An element of its kernel is a normalized
generator perturbation annihilating every original linear first syzygy,
therefore an element of Hom_S(I_M,S)_0. Since grade(I_M)=4, applying
Hom(-,S) to 0->I_M->S->S/I_M->0 gives Hom_S(I_M,S)=S; the required
Ext^1(S/I_M,S)=0 follows from the displayed free resolution. The only
degree-zero map is scalar multiplication, removed by the pivot
normalization. The same argument works in characteristic101.

Choose291 independent scalar rows of L and let J be their exact left
inverse. Since L(t)=(U1,0), every solution is forced to be

    z(q)=q(Id-qJT)^(-1)t.

It remains to check (Id-LJ)T(JT)^k t=0. Cayley--Hamilton bounds the
necessary k by0,...,290. A failure at k=0 already rejects the entire
ansatz at order q². A success at all291 stages proves rational closure;
the minimal polynomial on the Krylov span can then replace the
291-dimensional denominator bound. No nonlinear elimination is needed.

`scripts/probe_linear_kernel_graph.py` is prepared, not run by its author.
Its default is the q² consistency test modulo101. Run only with the
root-coordinated sole substantial-process slot:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 runs/astra-computation-2026-09-08/scripts/probe_linear_kernel_graph.py --max-order 2 --max-seconds 120 --output runs/astra-computation-2026-09-08/data/linear_U_order2_101.json

**CONDITIONAL interpretation:** a modular failure, together with the
recorded unit determinant of the selected L rows, excludes the same
rational first-tangent ansatz in characteristic zero: the unique candidate
coefficient is101-integral and its residual cannot vanish over Q. A
modular success alone certifies only characteristic101. Transfer an exact
rational identity or independently construct a characteristic-zero
algebraic lift before advertising equations there.

## 2. Linear free generator paths are legitimate, but do not inherit smoothness

**PROVED:** the21-dimensional fixed embedded Hilbert germ is irreducible
and smooth. Its origin-selected component contains the already certified
smoothing arc, and hence maps into the established94-dimensional Hilbert
component. A smooth point of the latter has a smooth Hilbert germ, so the
fixed germ cannot be wholly contained in an intersection with a different
Hilbert component. Every new smooth fibre in this origin-selected fixed
component consequently has the established geography (1,31).

**OPEN for each candidate:** a prescribed linear free-coordinate path
may lie entirely in the singular-fibre discriminant. Having the same
first tangent does not exclude that possibility. The source smoothness
certificate is a six-jet certificate, and cannot be silently transferred
to a path changing orders2,...,6. A finite exact Jacobian/saturation
certificate is still necessary for any newly extracted closed fibre.
The global roots of a selected polynomial subsystem are not automatically
in the origin component: retain the local/étale branch selector and verify
all1650 reduced incidence equations or the full FR identity.

## 3. Remove eleven coordinate freedoms before a larger ansatz

**PROVED reduction; HEURISTIC computational advantage.** The coordinate
representation is 3·trivial + sign +2·standard. Its centralizer in PGL8
has dimension13. The invariant diagonal stabilizer at X_M has dimension2,
so its coordinate-orbit tangent has dimension11, leaving ten intrinsic
fixed directions. Compute these11 orbit vectors in the291 normalized
coefficient basis, choose eleven linear functionals nonsingular on that
orbit tangent, and impose that their values are zero. The resulting
transverse slice is formally smooth of dimension10.

One must explicitly normalize generators after a centralizer coordinate
change. Choose eleven group parameters transverse to the stabilizer;
the derivative of the eleven slice equations in those parameters must
have nonzero determinant. The implicit function theorem then supplies a
unique local coordinate transformation. Verify the transformed ideal,
not equality of a chosen syzygy frame. This can remove gauge acceleration
from low-degree ansätze, but does not make the intrinsic chart rational.

## 4. What the old fifteen dependent coordinates now prove

**PROVED, using the established component dimension:** blow up the full
53-dimensional intrinsic tangent-coordinate space at the origin and use
the affine exceptional chart containing the chosen nonzero tangent.
Divide the full Kuranishi equations by q². The fifteen selected quadratic
rows have independent derivatives in fifteen transverse direction
coordinates at the marked exceptional point. They define a smooth
38-dimensional germ there. The strict transform of the actual
38-dimensional smoothing component is a closed subgerm of the same
dimension; a nonzero ideal in that regular local domain would lower
dimension. Hence the remaining full transformed equations vanish on this
germ. In particular the marked strict-transform germ is smooth.

**NOT PROVED:** that the raw quadratic P1³ equations are the full
Kuranishi equations, or that they yield finite cubics without corrections.
The selected fifteen equations still involve the *full* Kuranishi series.
To make this route executable, first express them in the finite cubic
incidence chart, eliminate its constant-Jacobian directions, and perform
the indicated blowup. The already available21-dimensional fixed chart
has fewer parameters and no remaining quadratic obstruction, so the
fifteen-coordinate route is not presently the cheaper extraction job.

## 5. Number-field points selected p-adically: a genuine but conditional fallback

**PROVED:** after setting q=101^N, the finite integral selected incidence
system has a unique solution congruent to the marked origin in Z_101,
by its unit Jacobian. Its coordinates are algebraic over Q, because the
specialized solution is an isolated nonsingular zero of a square
polynomial system. Thus a number-field tuple can be specified by the
finite equations plus the101-adic branch selector without computing a
primitive-element eliminant. This is a valid exact representation, but
the760-variable reduced incidence presentation is not a manageable
sixteen-equation field presentation.

**OPEN:** certify smoothness for the chosen integer N. Modular generic
smoothness alone is insufficient: a discriminant q(q-101) is generically
nonzero modulo101 but vanishes at q=101. A useful finite certificate is
an exact rational truncated Jacobian/Macaulay module computation showing
that its relevant largest invariant-factor valuation is small enough
that the unknown q^7 correction cannot affect the rank after q=101^N.
Equivalently, lift enough of the local q-power identities to Q with a
controlled101-adic denominator bound. The modular witnesses in the
source are not themselves such lifted identities. Do not declare a
particular101^N fibre smooth until this additional valuation check is
complete.

**Priority:** finish the currently running linear-free-path probe; then
run the two-minute linear-U rejection test; if both fail, retain the
finite algebraic curve and prepare the explicit ten-dimensional gauge
slice or controlled closed-point extraction. Do not inflate rational
Padé bounds indiscriminately or launch a global760-variable Gröbner basis.

## 6. Bounded low-degree algebraic fitting of the existing32-jet

**HEURISTIC discovery; exact verification is decisive.** For a candidate
primitive coefficient t(q), fit P(q,t)=0 and attempt to express every
z_j in the basis1,t,...,t^(d-1), with a small common denominator in q.
This is a plausible way to exploit the already computed jet without
repeating nonlinear elimination. The following guards are necessary.

- Through q^32 there are33 equations. A rectangular support with
  deg_t<=4, deg_q<=6 has35 coefficients and therefore always admits
  spurious relations. Useful first caps are (4,4), (3,6), and (2,6),
  with25,28,21 coefficients respectively. Reserve holdout coefficients.
- Remove polynomial content and factor P over F_101(q). Select the
  irreducible factor compatible with the jet. Exact identities must hold
  in that field, not only modulo a reducible product polynomial.
- If P_t(0,t(0))=0, ordinary simple-root Hensel is unavailable. Check
  v_q(P(t_trunc))>2v_q(P_t(t_trunc)) and use the resulting generalized
  Hensel precision to identify the branch and its six-jet. Order32 is
  enough for this inequality when the derivative valuation is at most16
  and the displayed residual vanishes through32.
- A regular coefficient need not lie in the integral power basis with
  a denominator D(0)=1. For example t²=q²(1+q) has t/q regular at the
  chosen branch. Normalize t by its initial q-valuation or permit a
  small explicitly bounded q-power denominator. Such a denominator is
  acceptable in the function field; verify cancellation at the origin.
- A coordinate may generate a proper subfield of the full coefficient
  field. Failure to express the other290 coefficients in its power
  basis rejects that primitive-element choice, not algebraicity of the
  curve. Try only a small predeclared set of generic linear combinations.
- Finally check every full incidence identity exactly, check det(A)
  nonzero, and identify the origin branch to the required jet order.
  If the six-jet is retained, the accepted generic smoothness certificate
  applies. A closed specialization still needs its own smoothness check.

**CONDITIONAL next payoff:** a verified finite-field algebraic model of
degree at most4 makes small closed-point searches inexpensive: specialize
q at a few allowed nonzero values, factor P(q,t), reconstruct all cubics,
and run the exact fibre certificate. A point with the relative selected
Jacobian invertible and good smooth reduction has an algebraic
characteristic-zero Hensel lift. `MODULAR_PICARD_BRIDGE.md` explains the
necessary origin-component and integral-model checks; no rational-function
reconstruction over Q is logically required for this lift.
