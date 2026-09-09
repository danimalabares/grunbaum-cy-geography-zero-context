# Picard certificates from the integral fixed chart

8 September 2026. Scope: the accepted zero-context smoothing and the new
integral pointed curve of the daytime run. No CAS was run by this
mathematical subtask. The daytime files are unchanged.

**COMPUTER-CERTIFIED new result:** the first-order product computation has
already found the required degree-eight rank certificate, with an exact
integer determinant. Thus neither rational reconstruction over Q nor a
finite-field fibre nor an I² resolution is now necessary for Picard rank
or the Hodge pair. The general modular bridges are retained below because
they explain precisely which transfers are valid and provide independent
verification routes once finite equations become convenient.

## 1. The bridge actually used by the new certificate

**PROVED mathematical reduction.** For any smooth CY fibre with the given
self-dual resolution, put n=h0(N) and r=dim(I²)_8. The new finite-complex
argument proves

\[
h^{1,1}=1748+n-r.
\]

Its full proof, including all tensor signs, the two hypercohomology
spectral sequences and the distinction between a graded conormal module
and its sheaf, is in `DEGREE8_PICARD_FORMULA.md`.

**COMPUTER-CERTIFIED exact matrix result.** The map whose columns are
x^α F_iF_j, |α|=2 and i≤j, has size6435×4896. At the special fibre
its monomial image has dimension1829. After eliminating one pivot column
for each central monomial, a12×12 minor of the first-order Schur matrix
has determinant

\[
-3623878656=-3^3\,8^9\ne0.
\]

The certificate is
`logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json`.
Its recorded input is `equations/deformation_data.json`, source commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`, input SHA256
`8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f`.

**PROVED interpretation.** Ordered into central pivot rows/columns,
the matrix has M0=[I B0;0 0], with one1 in each column of B0. Thus the
first Schur coefficient is M1_NE−M1_NP B0. This is exactly the
column-minus-representative expression certified by the script. The
corresponding full1841×1841 minor has leading term

\[
-3^3\,8^9 q^{12}+O(q^{13}).
\]

The pivot-block determinant is1+O(q), so it does not alter this leading
coefficient. All higher corrections are irrelevant. Although the search
selected pivots modulo101, the final small matrix and determinant were
recomputed over the integers. This is directly a characteristic-zero
rank certificate, not an assertion based on numerical agreement between
primes. The initial formal family need only have this first-order
generator direction, up to invertible generator/coordinate changes.

**PROVED under the accepted smoothing and Hilbert-bound trust boundary.**
r≥1841, n≤94, and h11≥1 imply

\[
1\le1748+n-r\le1748+94-1841=1.
\]

Hence r=1841,n=94,h11=1. The Euler/normal derivation gives h21=31;
the CY identities give rho=1 and Euler−60; smooth CY deformation
theory gives Hilbert-component dimension94. No premise of flatness of
I² has entered this argument: the only specialization was an explicit
matrix between free modules.

**OPEN unchanged:** torsion in Pic, simple connectedness, and concrete
coefficients for a selected nonzero closed fibre. Pic/torsion=Z·H
follows from rho=1 and H³=20, but Pic=Z·H still requires torsion-freeness.

## 2. Exact F101(q) equations would not need a rational Q lift

**PROVED conditional bridge.** Let A=Z_(101). The daytime chart has
finite polynomial equations and a selected Jacobian determinant−1 at
the origin. Set the21 free coordinates to their normalized six-jet
polynomials. On the specified local origin branch, the resulting base B
is a relative curve, étale over A[q] near(101,q=0). Its completed
local ring is Z_101[[q]], and the generators have the prescribed integral
formal expansion. All omitted chart equations vanish on this branch by
the integral implicit-function argument in the daytime
`FIXED_CHART_REVIEW.md`, §3. The chart's full first-syzygy lifting
argument supplies flatness.

The local ring B at the origin is regular and integral. Its height-one
prime(101) defines the characteristic101 branch. Localizing B at that
prime produces a DVR R with

\[
\operatorname{Frac}(R)=K_0,\qquad \kappa(R)=K_{101},
\]

where K0 is a finite extension of Q(q) and K101 is the function field
of the reduced characteristic101 origin curve. The smoothness certificate
already proves the generic fibre of the characteristic101 curve is
geometrically smooth. Projectivity and flatness then give a proper smooth
family over this DVR after the indicated localization.

Suppose a calculation finds rational functions z(q),U(q) over F101(q).
The checkable conditions identifying them with this residue fibre are:

1. Every denominator is a unit at q=0.
2. The coordinates have the specified origin and agree with the
   normalized certified first/six-jet as required by the selected free paths.
3. The21 free coordinates equal their specified polynomial paths exactly.
4. All top equations AU=B and all6960 bottom equations D−CU=0 hold
   exactly as rational functions, and det(A) is nonzero.
5. The origin Jacobian has the certified unit determinant. The implicit
   uniqueness theorem then identifies the rational-function solution with
   the characteristic101 local branch, not an unrelated component.
6. Flatness/Hilbert data and geometric generic smoothness are certified
   using this identification and the accepted source witnesses, or by an
   independent exact certificate.

**PROVED.** These conditions supply the residue fibre of the existing
mixed-characteristic DVR model. There is no requirement that z(q) be
the reduction of a rational function over Q(q). Its characteristic-zero
lift can remain algebraic over Q(q), as it already is in the implicit
chart. Rational reconstruction is a computational convenience, not a
logical prerequisite for the Picard bridge.

## 3. Why Ext4=0 on that residue fibre proves rho=1

**PROVED conditional implication.** Let X_R⊂P7_R be the proper smooth
model just described. The relative conormal sheaf C_R is locally free of
rank four on X_R. It is flat over R. Upper semicontinuity gives

\[
h^2(C_{K_0})\le h^2(C_{K_{101}}).
\]

The precise properness, finite-presentation and sheaf-flatness hypotheses
are those of [Stacks, Lemma36.32.1, tag0BDN](https://stacks.math.columbia.edu/tag/0BDN).
Smoothness makes the conormal sequence short exact; see
[Stacks, Section37.63(2), tag06BB](https://stacks.math.columbia.edu/tag/06BB).

For the residue fibre, the ideal sequence and its ACM vanishings
H2(I)=H3(I)=0 identify h2(C) with h3(I²). Graded local duality
identifies the latter with

\[
\dim_{K_{101}}\operatorname{Ext}^4_{K_{101}[a,\ldots,h]}
 (I^2,K_{101}[a,\ldots,h](-8))_0.
\]

The duality dependency is
[Stacks, Theorem47.18.3, tag0A84](https://stacks.math.columbia.edu/tag/0A84),
with the standard graded canonical module S(-8). Thus an exact zero
forces h2(C_K0)=0. The characteristic-zero conormal/Euler argument
then yields h11=rho=1. This does not identify characteristic-p Hodge
numbers with Picard rank or require Hodge symmetry in characteristic p.

If Ext4 is nonzero, its dimension gives only an upper bound for the
characteristic-zero h11−1. To obtain an exact Hodge pair from such
an upper bound needs a complementary lower bound or the new degree-eight
identity. The existing daytime script `hodge_from_fibre.m2` can compute
this Ext4 by a partial square resolution, but that computation is now
optional validation after the successful first-order certificate.

## 4. What a finite-field closed point must satisfy

**CONDITIONAL.** A point over F_(101^r) on the same origin branch can
replace its generic function field, but component identification is
essential. Satisfying the selected270 equations at an arbitrary remote
point does not identify the local branch.

A useful certificate consists of a map from an open subset of the
verified characteristic101 rational-function branch, a specified q0
where all denominators and chart determinants are nonzero, the resulting
point satisfying every full chart equation, and a smooth projective
fibre there. The selected relative Jacobian must remain invertible at
the point to obtain an étale lift. More generally one can use a verified
prime ideal of the integral origin component and a smooth point of its
reduction; mere membership in the global incidence equations is weaker.

Formal étaleness/Hensel lifting then lifts the point to an unramified
extension of Z_101, after choosing a lift of q0. Proper smoothness of
the resulting family makes its conormal flat, and Ext4=0 gives rho=1
for that characteristic-zero lift. One need not explicitly solve its
number-field coefficients to prove the implication. To transfer the
conclusion to the zero-context component, retain the origin-component
certificate. Over characteristic zero h11 is constant in a connected
smooth proper family, and h20=0 identifies it with Picard rank.

**OPEN if component membership is missing:** a smooth finite-field
solution of the global equations can belong to another component.
An existence statement about its lift would not determine the intended
zero-context smoothing's geography.

## 5. What a jet can and cannot do for conormal cohomology

**FAILED naive approach.** The conormal bundle is not flat through the
non-lci central fibre in general. Neither C_0=I_M/I_M² nor the ordinary
monomial ideal square can be inserted into a semicontinuity inequality
without a base-change/flatness theorem. Knowing the generators and
first syzygies through q6 does not supply that theorem.

**PROVED replacement.** The finite antisymmetric derived complex in
`DEGREE8_PICARD_FORMULA.md` is built from a free resolution of O_X and
is defined even at the singular central fibre. Its interpretation as
conormal cohomology is used only at the generic lci fibre. Its scalar
matrices are matrices of free modules, so nonzero leading minors survive
all compatible higher corrections without any conormal-flatness premise.
The last map's identification with C(8), together with Euler counting,
then reduces the entire task to degree-eight products of F. The first
jet already contains the successful twelve new pivots.

**PROVED scope of the coefficient certificate.** Any smoothing with the
same first-order embedded direction, after verified invertible generator
basis changes, projective-coordinate changes and a nonzero scalar
reparametrization, inherits the product-rank lower bound. Such changes
induce invertible transformations of the product matrix's source/target.
This can transfer the geography without identifying two all-orders arcs.
An old proof's direction must actually be compared in explicit bases
before using this observation; proof-lineage similarity alone is not
enough.

## 6. Evidence and remaining boundary

**PROVED within recorded analysis:** the degree-eight identity and the
free-matrix rank transfer. An independent mathematical review by the
Hilbert subtask checked the tensor signs, hypercohomology degrees and
graded-module cokernel identification. This is not qualified-human
verification.

**COMPUTER-CERTIFIED:** central product rank1829 and the exact integer
12×12 leading minor from the frozen first-order input. The full matrix
was not subjected to a blind Gröbner or ideal-square resolution.

**CONDITIONAL source boundary retained:** existence of the smooth
compatible continuation and the full embedded Kuranishi local dimension
bound94 are the accepted source/audit inputs. The new certificate proves
the missing numerical equalities from those inputs; it does not erase
their stated computer-algebra trust boundary.

**OPEN:** a finite closed smooth fibre with convenient displayed
coefficients, integral Picard torsion and fundamental group. These are
separate from the now-certified Picard rank and Hodge pair.
