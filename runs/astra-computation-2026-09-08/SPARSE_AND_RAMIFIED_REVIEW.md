# Independent review: sparse routes and the ramified geography bridge

8 September 2026. Read-only mathematical review of
`DEGREE8_PICARD_FORMULA.md`, `GEOGRAPHY_THEOREM.md`, and
`RAMIFIED_POINT_CONSTRUCTION.md`. No substantial process was run for this
review. This records explicit checks, not an assertion of qualified-human
verification or an independent rerun of the original smoothness certificates.

## 1. Sparse experiments are separate

**PROVED rejection:** the two-orbit direction O3+O8 preserves the grading
with weight1 on b,e,h and weight0 on the other variables, with q fixed.
Its selected invariant linear-free curve contains a cubic threefold in
`{b=e=h=0}=P4`; it cannot be a connected smooth degree20 CY. See
`SPARSE_DIRECTION_REJECTED.md`. No lift was run for it.

**COMPUTER-CERTIFIED bounded attempt:** O3+O8+O10 has no nontrivial
diagonal grading fixing q and retains the unit product minor. Its
linear-free curve was lifted only modulo q33 over F101. All shared F/R
and generator-only fits with denominator degree≤10 and numerator bounds
d+1 or d+6 failed. See `SPARSE_THREE_ORBIT_ATTEMPT.md` and its immutable
checkpoints. This says nothing against the original six-jet curve used
in the ramified construction; it neither supplies nor refutes smoothness.

## 2. The ramified product-rank statement requires only the first jet

**PROVED directly over the DVR.** Let O be the complete DVR in
`RAMIFIED_POINT_CONSTRUCTION.md`, with uniformizer pi, residue field F101,
and `pi^7=101`. Suppose the actual algebraic coefficient point satisfies

\[
F_i=f_i+\pi g_i\pmod{\pi^2},
\]

in the identified normalized marked generator basis. The g_i here are
the original selected zero-context first-order polynomials, not either
sparse experiment. This congruence is part of its agreement with the
normalized six-jet modulo pi7. In fact first-order normalization makes
no change to those g_i because their coefficients at all sixteen pivot
monomials are zero.

Build the actual degree-eight product matrix M over O. Its reduction has
the same1829 monomial pivot columns and rows. Select these and the same
twelve additional rows/columns from `PRODUCT_RANK_CERTIFICATE.md`, and
subtract the corresponding central representative from each extra
column. The resulting1841-by-1841 matrix has blocks

\[
\begin{pmatrix}A&B\\ C&D\end{pmatrix},
\quad A\equiv1\pmod\pi,\quad B\equiv C\equiv0\pmod\pi,
\quad D\equiv\pi Q\pmod{\pi^2}.
\]

The determinant of the integer12-by-12 matrix Q is `−3³8⁹`, a unit of O.
Since A is invertible, its Schur complement is

\[
D-CA^{-1}B=\pi(Q+\pi E)
\]

for an actual matrix E over O. Therefore

\[
\det M_{\rm selected}=\det A\;\pi^{12}\det(Q+\pi E),
\qquad v_\pi(\det M_{\rm selected})=12.
\]

In particular the product rank over `Frac(O)` is at least1841.

**PROVED precision warning:** it would be invalid merely to substitute
q=pi into a statement about the full determinant modulo q7 and infer
a pi12 coefficient. The determinant is zero modulo pi7. The valid
argument divides the **twelve individual Schur rows/columns**, each known
to be pi-divisible in O, and computes their remaining determinant modulo
pi. First-order precision modulo pi2 is enough. No division is performed
inside a nilpotent quotient. The equality `101=pi7` causes no cancellation:
`det Q mod pi` is nonzero. The same proof remains valid after any further
ramified extension, with determinant valuation multiplied accordingly.

## 3. How the actual point enters the characteristic-zero component

**PROVED once the integral fixed-germ identity in the construction is
accepted.** Reducing to the same characteristic101 special fibre alone
would not identify characteristic-zero Hilbert components. The stronger
bridge is the actual integral coefficient series.

The selected implicit chart system has a unit constant Jacobian. Its
unique formal solution after prescribing the original21 free six-jet
paths has coefficients in `Z_(101)[[q]]`; the constant inverse used in
successive equations has101-integral entries. The entire curve lies in
the integral S3-fixed germ, whose characteristic-zero completion at the
origin is the smooth21-dimensional formal domain. It therefore shares
the characteristic-zero fixed component containing the original formal
smoothing, and hence its94-dimensional full Hilbert component C.

Substitution q=pi converges coefficientwise in O because all series
coefficients are101-integral. It satisfies the finite coefficient system
and the prescribed congruence, so Hensel uniqueness identifies its value
with the actual algebraic point constructed in
`RAMIFIED_POINT_CONSTRUCTION.md`.

To see component membership algebraically, let h be any rational
polynomial equation of C in the relevant affine Hilbert chart. Its
pullback to the preceding formal curve is zero in Q[[q]]. Multiply h by
a nonzero integer to clear its finitely many coefficient denominators;
this integer may contain powers of101. The resulting identity lies in
`Z_(101)[[q]]` and converges to zero at pi. Since that nonzero integer
remains nonzero in the characteristic-zero field, h also vanishes at
the actual point. Localized chart denominators have unit constant terms
and are units at the selected p-adic root. Thus the actual point lies
on C after field extension. This is a convergent identity argument, not
an unsupported specialization-of-components inference.

## 4. Resolution and smoothness hypotheses must still be supplied

**PROVED resolution persistence, conditional on actual graded flatness:**
over any DVR O, if the graded coordinate algebra is degreewise O-flat
with the stated special fibre, each successive kernel in a lifted graded
free resolution is O-flat. Reduction preserves the kernels. Lifting the
special generators and successive syzygies and applying Nakayama in each
graded degree gives an exact resolution with shifts0,3,4,5,8 and ranks
1,16,30,16,1. Its final zero-reduction kernel vanishes. All differentials
have positive x-degree, so no generic minimal cancellation occurs. The
last free rank1 and Cohen–Macaulay resolution give the Gorenstein
self-duality used in the degree-eight argument.

This applies to the ramified point only after the full Schur identities
and exact canonical syzygies establish graded O-flatness. A finite jet
alone does not give it. Likewise, smoothness must come from the separate
transport of the original singularity certificates, with the actual
generator normalization checked. This review does not replace
`RAMIFIED_POINT_REVIEW.md` or the source trust boundary for that step.

**PROVED field-of-definition transfer:** once the point is defined over
the finite number field L and its base change to `Frac(O)` is smooth,
smoothness descends along that field extension. Dimensions of proper
coherent cohomology, graded vector-space ranks, and exactness of the
displayed free resolution are preserved under further field extension.
Consequently the characteristic-zero computations apply to every complex
embedding of L. No finite-field Hodge symmetry is being assumed.

## 5. Checks of the degree-eight formula

**PROVED within its stated smooth hypotheses:** the antisymmetric
summand of P tensor P has homology C in degree1 and exterior³C in
degree3. The graded flip acts on local Koszul Tor_i by `(−1)^i`.
The ambient terms in degrees4,...,7 and dimensions
`692,5760,14796,12672` are correct. The other terms have no projective
cohomology. For the terms H²(C) and H³(C), the only potential higher
differentials target H5/H6 of exterior³C and vanish by support dimension.
This yields the two rank expressions in the formula document.

After self-duality, the final dual differential presents `(I/I²)(8)`:
the linear syzygies identify the target with I, and the polar-product
map has image2I²=I² in characteristic zero. This identification is made
before sheafification and does not assume I² is saturated or flat.
The value `dim I8=4691` follows from the displayed resolution, so the
formula `h11=1748+h0(N)−dim(I²)8` is justified.

The conormal/Euler step uses the nonzero hyperplane class, not an
unproved vanishing of H¹(C): the map `H¹(OmegaP7|X)=k -> H¹(OmegaX)`
sends1 to c1(H) and is injective because H is ample. Its adjacent
H²(OmegaP7|X) vanishes. Thus `h11=1+h²(C)`.

**PROVED Hilbert-smoothness check:** restricted Euler gives
`H¹(TP7|X)=0` and `H²(TP7|X)=k`, using the positive-twist vanishings.
The normal sequence identifies H¹(N) with the kernel of
`H²(TX)->k`. By Serre duality this is dual to the preceding nonzero
hyperplane-class map, and `dim H²(TX)=h11`. Hence `h¹(N)=h11−1`.
After h11=1 is obtained, H¹(N)=0 proves embedded Hilbert smoothness
directly. This last implication does not require BTT.

## 6. Upper bounds and the final conclusion

**PROVED logical separation:** dimension94 of a component alone does
not bound the tangent dimension at an arbitrary possibly singular
Hilbert point. For the ramified point, first establish smoothness of the
fibre and the same-component bridge above. The open locus of smooth
fibres in an irreducible projective Hilbert component is connected;
Hodge numbers are constant in its smooth proper complex family. Thus
the known original bound h21≤31, and consequently
`h0(N)=63+h21≤94`, transfer to this actual smooth point. Alternatively,
one can explicitly invoke unobstructedness of polarized CY deformations
to identify its Hilbert tangent dimension with component dimension.

Now the direct pi-adic minor gives r≥1841 and the formula gives

\[
1\le h11=1748+n-r\le1748+94-1841=1.
\]

Thus the actual smooth characteristic-zero fibre has `(h11,h21)=(1,31)`,
Picard rank1, Euler characteristic−60 and smooth Hilbert dimension94.
Its Picard group modulo torsion is ZH; torsion and fundamental group
remain outside this argument.

**Expository scope check:** the self-dual Betti format is proved on the
DVR family and an appropriate chart neighbourhood, not automatically at
every remote smooth point of the component. The Hodge theorem extends
to those other smooth points by smooth-proper deformation, not by silently
applying the resolution formula where its Betti hypotheses were not
checked. No mathematical defect was found after these hypotheses and
the ramified component bridge are kept explicit.
