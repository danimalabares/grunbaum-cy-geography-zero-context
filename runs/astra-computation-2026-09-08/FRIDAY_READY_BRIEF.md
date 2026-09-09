# Friday brief: the zero-context Grünbaum--Sreedharan smoothing

For the11 September2026 discussion with Grzegorz Kapustka and Sergey
Galkin. These are new conclusions of this repository run, **not a claim
of novelty in the literature**. The original zero-context computational
trust boundary remains explicit; qualified-human verification of the new
arguments is requested, not claimed.

## The two-minute statement

**PROVED within the accepted smoothing/certificate trust boundary:**
the selected zero-context smoothing has

\[
(h^{1,1},h^{2,1})=(1,31),\qquad \rho=1,\qquad e(X)=-60,
\]

\[
H^3=20,\qquad c_2\cdot H=56,\qquad
\dim\operatorname{Hilb}_{[X]}=94.
\]

The Hilbert scheme is smooth at the smooth fibre. The Picard group modulo
torsion is ZH. **OPEN:** Picard torsion, the fundamental group, and a
geometrically illuminating model.

**PROVED finite explicitness, in an algebraic-number representation:**
we also have sixteen finite cubic equations for an actual smooth fibre.
Their coefficients are a uniquely specified algebraic-number tuple,
selected using π^7=101 and a270-variable Hensel system. This is stronger
than a finite jet or an unspecified generic fibre. **OPEN practical
limitation:** the number-field degree and a small primitive-element
presentation have not been computed. The coefficients are exact, but
not yet convenient for arbitrary downstream CAS calculations.

## Why the Hodge calculation is small

**PROVED conceptual reduction.** Put

    n=h⁰(N_{X/P⁷}),       r=dim(I_X²)_8.

The self-dual resolution with ranks1,16,30,16,1 in shifts0,3,4,5,8
gives

\[
h^{1,1}=1748+n-r.
\]

This is not an empirical identity. Take the antisymmetric summand of
the tensor square of the free resolution, with the Koszul sign in the
factor exchange. On the smooth fibre its homology sheaves are
I/I² and Λ³(I/I²) in homological degrees1 and3. Only four terms have
ambient cohomology on P⁷. After duality their vector-space dimensions are

    692 -> 5760 -> 14796 -> 12672.

The first map is injective; the next rank is5068−n. Self-duality
identifies the cokernel of the last map, at the graded-module level,
with (I/I²)_8: the linear-syzygy relations present I and the polar
products impose I². Since dim I_8=4691, its rank is7981+r. The middle
cohomology is h²(I/I²)=h11−1, giving the displayed formula. The complete
signs and spectral-sequence justification are in
`DEGREE8_PICARD_FORMULA.md`.

**COMPUTER-CERTIFIED, with a small integer certificate:** consider the
degree-eight product matrix with columns x^αF_iF_j, |α|=2, i<=j.
The monomial special fibre supplies1829 unit pivots. In the remaining
first-order matrix there is a12×12 minor with exact determinant

\[
-3623878656=-3^3\,8^9\ne0.
\]

The full1841×1841 minor consequently has this leading coefficient at
q^12. Although that order exceeds six, it uses **only first-order
data**: the twelve residual entries are q-divisible and their leading
matrix is already known. Every unknown higher correction has higher
valuation and cannot change this coefficient. Thus r>=1841 on every
compatible smoothing. The tiny integer matrix is in
`PRODUCT_RANK_CERTIFICATE.md`; no resolution of I² was needed.

**PROVED conclusion:** the accepted bound n<=94 and the ample class give

\[
1\le h11=1748+n-r\le1748+94-1841=1.
\]

Hence n=94, r=1841, h11=1 and h21=31. This applies the conormal
formula only to smooth fibres. It does not assume that the ordinary
square I_M² or the singular conormal sheaf forms a flat family.

## Normal and conormal blackboard explanation

**PROVED normal calculation.** For a smooth fibre, K_X=O_X,
h¹(O_X)=h²(O_X)=0 and h⁰(O_X(1))=8. Kodaira vanishing gives
H^i(O_X(1))=0 for i>0. The restricted Euler sequence

\[
0\to O_X\to O_X(1)^8\to T_{\mathbf P^7}|_X\to0
\]

therefore gives h⁰(TP⁷|X)=64−1=63 and H¹(TP⁷|X)=0.
Contraction with a nonzero volume form identifies T_X with Ω_X²;
H⁰(T_X)=H^{2,0}(X)=0. The normal sequence

\[
0\to T_X\to T_{\mathbf P^7}|_X\to N\to0
\]

now gives h⁰(N)=63+h¹(T_X)=63+h21.

**PROVED conormal calculation.** Let C=I/I². The sequences

\[
0\to\Omega_{\mathbf P^7}|_X\to O_X(-1)^8\to O_X\to0,
\qquad
0\to C\to\Omega_{\mathbf P^7}|_X\to\Omega_X\to0
\]

give H¹(ΩP⁷|X)=k and H²(ΩP⁷|X)=0, by Serre duality and the
same Kodaira vanishings. The first group maps to H¹(Ω_X) as the
nonzero class c1(H). Thus h11=1+h²(C). Serre duality gives
h³(C)=h⁰(N)=n. Finally, on P⁷,

\[
0\to I^2\to I\to C\to0,\qquad
0\to I\to O_{\mathbf P^7}\to O_X\to0
\]

give h²(C)=h³(I²) and h³(C)=h⁴(I²)−1. This recovers the usual
conormal/square method h11=1+h³(I²), h21=h⁴(I²)−64, while the
degree-eight identity avoids its expensive full square resolution here.

**PROVED direct Hilbert smoothness.** Euler also gives H²(TP⁷|X)=k.
The normal sequence identifies H¹(N) with the kernel of
H²(T_X)→k. Its Serre-dual map is k→H¹(Ω_X), 1↦c1(H).
When h11=1 this is an isomorphism. Hence H¹(N)=0, so embedded
deformations are unobstructed and the Hilbert germ is smooth of
dimension94. No appeal to BTT is needed for this final step.

**PROVED Picard interpretation.** The exponential sequence, together
with H¹(O_X)=H²(O_X)=0 and GAGA, identifies Pic(X) with H²(X,Z).
Thus ρ=h11. Since H³=20, H cannot be a nontrivial multiple of another
integral divisor modulo torsion: such a multiple would have cube divisible
by an integer cube greater than1. Consequently Pic(X)/torsion=ZH.
This does not remove torsion or settle π1.

## The actual smooth algebraic-number fibre

**PROVED construction, with finite exported coefficients.** In the
S3-invariant normalized cubic chart there are291 coefficient coordinates.
Twenty-one are assigned their certified normalized six-jet polynomials
γ_j(q). The other270 are dependent. The equivariant multiplication
matrix splits into three blocks with invertible central A-blocks of
sizes21,13,32. For the selected270 entries, use the finite bordered
determinants

\[
\det\begin{pmatrix}A_r&B_{r,\bullet j}\\
C_{r,i\bullet}&D_{r,ij}\end{pmatrix}=0.
\]

These are polynomials, represented as determinants of size at most33;
expansion is unnecessary. Their270-square Jacobian determinant is19
modulo101, so it is a unit. The full fixed Hilbert germ is smooth of
dimension21, making the omitted equations consequences on the selected
local branch.

Take K_p=Q_101(π), π^7=101, O=Z_101[π]. Substitute q=π and
select the unique dependent tuple θ∈(πO)^270. Hensel uniqueness gives
it exactly, and the invertible polynomial Jacobian proves its coordinates
algebraic over Q(π). Set

    L=Q(π,θ_1,...,θ_270)⊂K_p.

Crucially, O/(π^7)≅F101[q]/q^7. Thus the actual fibre has precisely
the certified six-jet modulo π^7. The original smoothness witnesses use
q^5 modulo q^6, or lower powers, on a complete stratified cover. They
transport literally to this mixed-characteristic DVR and exclude every
geometric singular point by the same valuation contradiction. Smoothness
then descends from K_p to L. This is why the particular number-field
fibre is known smooth, despite not having reduced L to a power basis.

All sixteen cubics and the exact coefficient indexing are displayed in
`RAMIFIED_FIBRE_EQUATIONS.md`; the machine-readable presentation is
`data/ramified_fibre_coefficients.json`. See
`RAMIFIED_POINT_REVIEW.md` for the transfer, flatness, component and
algebraicity checks. The field degree is **not** claimed to be7.

## Where this sits in the Hilbert scheme

**PROVED under the recorded source calculations:** at X_M the embedded
tangent dimension is109. Its coordinate orbit has dimension56, leaving
53 intrinsic tangent directions. The top quadratic component has

    38=17+3·7,

because each rank-one2×6 determinantal cone has dimension2+6−1=7.
Adding the coordinate orbit gives94=56+38. The chosen smoothing
direction lies on that top component. The new rank certificate makes
94 an actual smoothing-component dimension, not merely an upper bound.
The38 here is not the smooth fibre's abstract moduli dimension: the
coordinate orbit grows from56 at the singular monomial fibre to63 at a
smooth fibre, whose infinitesimal automorphisms vanish. Thus the generic
abstract dimension is94−63=31, equivalently38−7. The numbers109 and53
are tangent dimensions at the singular point, not dimensions of a smooth
Calabi--Yau moduli space.
**OPEN stronger claim:** the raw quadratic P1³ ideal need not equal
the full Kuranishi ideal without corrections.

**PROVED literature comparison, not a novelty claim:** the general
degree20 submaximal-minor determinantal threefold has pair(2,34), hence
Hilbert dimension97=63+34, by Kapustka--Kapustka, *A cascade of
determinantal Calabi--Yau threefolds*, Theorem3.8 and Proposition3.10
([primary paper](https://arxiv.org/pdf/0802.3669)). Its smooth fibres
cannot be points of this94-dimensional smooth Hilbert component.
Connectedness of the Hilbert scheme permits chains of intersecting
components through singular members; it does not identify their smooth
loci or Hodge numbers.

## Five precise questions for Grzegorz and Sergey

1. Can you check the antisymmetric tensor-square argument, especially
   the graded-module identification of the terminal cokernel with
   (I/I²)_8 and the absence of relevant hypercohomology differentials?
   Is there a shorter established formulation of h11=1748+n−r?
2. Does this rank-one-cone tangent geometry or the S3 representation
   suggest a determinantal, unprojection, Pfaffian-related or other
   structural model that rationalizes the21-dimensional fixed chart,
   or produces a much smaller coefficient field for one smooth point?
3. What concrete geometric construction could settle Picard torsion
   and π1, given that ρ=1 is now known but the central divisor-class
   extension argument cannot use a Q-factorial total space?
4. How should the94-dimensional smoothing component be related
   geometrically to other degree20 Hilbert components, particularly
   the97-dimensional general determinantal component? Is a specific
   common singular degeneration or controlled transition known?
5. For the Abel proposal, what is the strongest defensible framing of
   the certified smoothing, pair(1,31), and ramified finite equations,
   while separating literature novelty, remaining structural geometry,
   and the explicitly stated computer-algebra trust boundary?

## What Daniel should have open during the call

`GEOGRAPHY_THEOREM.md` for the short proof,
`PRODUCT_RANK_CERTIFICATE.md` for the small integer matrix, and
`RAMIFIED_FIBRE_EQUATIONS.md` for the actual coefficient presentation.
The derivation and ramified review are supporting references if a
specific proof step needs discussion.
