# Geography of the zero-context smoothing

**PROVED within the accepted zero-context smoothing trust boundary.**
Qualified-human verification of this new argument is not claimed.

Let X be a smooth complex fibre of the zero-context smoothing with the
certified first-order direction, or a smooth fibre on its Hilbert component.
Then

\[
(h^{1,1}(X),h^{2,1}(X))=(1,31),\qquad\rho(X)=1,
\qquad c_3(X)=\chi(X)=-60.
\]

The smoothing component has dimension94. The polarization satisfies the
previously known H³=20 and c2.H=56. Pic(X)/torsion=ZH; torsion and
simple connectedness are not settled.

## Blackboard proof

Put n=h0(N_{X/P7}) and r=dim(I_X²)_8. Three inputs suffice:

1. The accepted smoothing theorem and quadratic obstruction bound give
   n=63+h21≤94.
2. The self-dual resolution of ranks1,16,30,16,1 in shifts0,3,4,5,8
   gives the conormal identity h11=1748+n−r. Its complete derivation,
   including the two hypercohomology spectral sequences and differential
   signs, is in `DEGREE8_PICARD_FORMULA.md`.
3. The first-order generator corrections give an explicit1841-row/column
   product minor with leading term −3³8⁹ q12. The central1829 pivots
   are monomials; the remaining12×12 matrix is nearly diagonal and
   displayed in `PRODUCT_RANK_CERTIFICATE.md`. Hence r≥1841 for every
   higher continuation of the same first-order direction.

The ample class supplies h11≥1, so

\[
1\le h11=1748+n-r\le1748+94-1841=1.
\]

Therefore n=94,r=1841,h11=1 and h21=31. Since H2(O_X)=0,
all rational H² classes have type(1,1), and the exponential sequence
gives rho=h11. The following direct obstruction calculation identifies
n with the smooth Hilbert dimension; no BTT theorem is needed here.

## Direct Hilbert smoothness after Picard rank one

**PROVED.** Restricted Euler and Kodaira vanishing give

\[
0\to O_X\to O_X(1)^8\to T_{\mathbf P^7}|_X\to0,
\qquad H^1(T_{\mathbf P^7}|_X)=0,
\qquad H^2(T_{\mathbf P^7}|_X)\simeq H^3(O_X)\simeq k.
\]

The normal sequence therefore identifies

\[
H^1(N_{X/\mathbf P^7})=
\ker\bigl(H^2(T_X)\to H^2(T_{\mathbf P^7}|_X)\bigr).
\]

By Serre duality, the indicated map is dual to

\[
H^1(\Omega_{\mathbf P^7}|_X)\simeq k
\longrightarrow H^1(\Omega_X),\qquad 1\longmapsto c_1(H).
\]

The class is nonzero since H is ample (its cube has degree20). When
h11=1 this is an isomorphism, so H^1(N)=0. In fact the same calculation
gives h^1(N)=h11−1 for every smooth fibre satisfying these hypotheses.
For a smooth closed embedding, H^1(N) is an obstruction space for
embedded deformations and H^0(N) its tangent space. Hence the Hilbert
scheme is smooth at[X] of dimension h^0(N)=94.

## Exact scope

This is not a calculation on the ordinary square of the singular fibre
used as though conormal sheaves formed a flat family. The certificate is
a nonzero minor of a matrix BETWEEN FREE MODULES over the formal parameter
ring. Its leading coefficient is fixed by first-order data. The conormal
formula is applied only to the actual smooth characteristic-zero fibre.

The integer minor, source first-order coefficient, all144 entries and
determinant were independently rechecked without the discovery parser or
pivot-search routine. No agreement among agents is used as evidence.
The original theorem's stated Singular-certificate trust boundary remains;
the new arithmetic certificate itself can be checked by hand.

An actual94-dimensional component now exists, but equality of the complete
Kuranishi equations with the raw quadratic P1³ ideal is a stronger statement
and remains OPEN. An actual smooth closed fibre is now specified in
`RAMIFIED_FIBRE_EQUATIONS.md` by sixteen cubics over an algebraic-number
tuple selected by π^7=101 and Hensel uniqueness. A small power-basis
presentation of its coefficient field remains OPEN; that practical
extraction is distinct from the existence of the displayed finite point.
