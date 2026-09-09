# A degree-eight product rank determines the missing Hodge information

8 September 2026. **PROVED below, conditional only on the accepted smooth
CY fibre and its stated self-dual resolution.** This is a mathematical
derivation, not a claim of independent human verification. No CAS was run
to obtain this reduction.

For a smooth fibre X with h0(N)=n, let r=dim_k(I²)_8. Then

\[
\boxed{h^{1,1}(X)=1748+n-r.}
\]

Consequently, for the zero-context smoothing, the established n≤94 and
the ample class imply r≤1841. **A certified lower bound r≥1841 alone
proves**

\[
(h^{1,1},h^{2,1})=(1,31),\quad \rho=1,\quad
\chi_{\rm top}=-60,\quad \dim\operatorname{Hilb}_{[X]}=94.
\]

No explicit coefficient field, full resolution of I², or lifted third and
fourth differentials are needed to compute that lower bound: the matrix
consists only of products of the known generators and quadratic monomials.

**COMPUTER-CERTIFIED success, added after the derivation:**
`logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json`
contains an exact first-order12×12 Schur minor of determinant
−3623878656=−3³·8⁹. Its first3×3 diagonal block is upper triangular
with diagonal(−3,−3,−3); its bottom9×9 diagonal block has one+8
and eight−8 entries, and its top-right block is zero. Thus its
nonvanishing is human-checkable directly from the saved small matrix.
The full product minor has leading q12 term with this coefficient,
independent of all higher corrections. The displayed Hodge/Hilbert
conclusions therefore follow under the accepted source trust boundary.

## 1. Hypotheses and the finite complex

Let k have characteristic different from two. For the Hodge conclusions,
use characteristic zero and an embedding in C. Assume X⊂P7 is a smooth
threefold, K_X=O_X, h1(O_X)=h2(O_X)=0, and S/I has the self-dual
graded resolution P• with

\[
P_0=S,\quad P_1=S(-3)^{16},\quad P_2=S(-4)^{30},\quad
P_3=S(-5)^{16},\quad P_4=S(-8).
\]

Write d1=F, d2=R. Let C=I/I² be the conormal bundle. On P•⊗P•
use the chain involution

\[
\tau(u\otimes v)=(-1)^{ij}v\otimes u,
\qquad u\in P_i,\ v\in P_j.
\]

The idempotent (1−τ)/2 defines the antisymmetric summand G•. This
construction is a finite complex of free graded S-modules, not an
assumption that an ordinary symmetric-square resolution is exact.

**PROVED persistence in this formal family.** Over A=k[[q]], the
coordinate ring is degreewise A-flat. The ideal, then each successive
kernel in a lifted resolution, is A-flat: in each defining short exact
sequence the right-hand module is A-flat. Reduction therefore preserves
those kernels. Lift the sixteen cubic generators, thirty linear first
syzygies, sixteen linear next syzygies, and one cubic final syzygy from
the special resolution; degreewise Nakayama gives surjectivity at each
step. The remaining left kernel has zero reduction and is zero. This
constructs an exact resolution with the stated shifts over A. After
passing to its fraction field every matrix entry still has positive
x-degree, so no minimal-resolution cancellation is possible. The same
Betti format therefore holds on the formal generic fibre. Its
Gorenstein self-duality follows either by lifting the Gorenstein
resolution or by dualizing this pure resolution and using its canonical
module. In the algebraic chart one may equivalently shrink to the open
neighbourhood where this resolution and exactness persist.

**PROVED.** Locally on a smooth embedded X, a Koszul resolution for a
regular sequence identifies Tor_i^OP(O_X,O_X)=Λ^i C. On a degree-one
Tor generator represented in the tensor of two Koszul complexes by
e_j⊗1−1⊗e_j, τ acts by −1. Multiplicativity therefore makes its
action on Tor_i equal to (−1)^i. It follows that the homology sheaves
of G• are C in homological degree1 and Λ³C in degree3, with all
others zero. This statement is used only on the smooth generic fibre,
not on the non-lci special fibre.

The non-acyclic ambient terms are

\[
\begin{aligned}
G_4&=O(-8)^{692},\\
G_5&=O(-11)^{16}\oplus O(-9)^{480},\\
G_6&=O(-12)^{30}\oplus O(-10)^{136},\\
G_7&=O(-13)^{16}.
\end{aligned}
\]

Here 692=1+16²+binom(30,2). The omitted G1,G2,G3 are sums of
O(-d) with 0<d<8; G0=G8=0. Thus those omitted terms have no
ambient cohomology, and G4,...,G7 have only H7.

Set V_i=Hom_S(G_i,S(-8))_0, using the free graded modules before
sheafification. Serre duality on P7 gives the scalar cochain complex

\[
0\longrightarrow V_4\xrightarrow{\delta_4}V_5
\xrightarrow{\delta_5}V_6\xrightarrow{\delta_6}V_7
\longrightarrow0,
\]

with dimensions

\[
692,\qquad5760,\qquad14796,\qquad12672.
\]

The dimensions are respectively
692,
16 binom(10,7)+480 binom(8,7),
30 binom(11,7)+136 binom(9,7),
16 binom(12,7).

## 2. The spectral-sequence step, including the possible differentials

**PROVED.** Regard G_i as cohomological degree −i. The second
hypercohomology spectral sequence has only the rows

\[
E_2^{p,-1}=H^p(C),\qquad E_2^{p,-3}=H^p(\Lambda^3 C).
\]

Both sheaves have support dimension three. In total degree one, the
only possible nonzero term is H2(C); the other candidate would be
H4(Λ³C)=0. The only potential outgoing higher differential is d3
from H2(C) to H5(Λ³C), which is zero. There is no possible incoming
differential. Therefore hyper-H1(G)=H2(C). Similarly,
hyper-H2(G)=H3(C), and hyper-H3(G)=0.

Comparing with the first spectral sequence, whose sole surviving row is
H7 of the G_i, proves

\[
\delta_4\text{ is injective},
\]

\[
\dim H^3(C)=5760-692-\operatorname{rank}\delta_5,
\]

\[
\dim H^2(C)=14796-\operatorname{rank}\delta_5-
\operatorname{rank}\delta_6.
\]

Since C*=N and K_X=O_X, Serre duality gives h3(C)=h0(N)=n.
Consequently rank δ5=5068−n. The independently proved conormal/Euler
formula gives h2(C)=h11−1.

This calculation also supplies an alternative direct certificate: rank
lower bounds for δ5 and δ6 summing to14796 force h2(C)=0, because
δ6δ5=0 supplies the matching upper bound. Its large matrices are no
longer the recommended implementation; the next step eliminates them.

## 3. The final map presents C(8)

**PROVED.** Use the self-duality of the resolution to identify
P3 with P1*(-8), P2 with P2*(-8), and P4 with S(-8).
After compatible invertible constant-in-x changes of basis, d4=F^t
up to a harmless sign and the transpose of d3 is d2 composed with an
invertible middle-basis matrix. Such basis changes preserve all ranks.

Under these identifications the final dual map before taking degree zero
has target P1(8). Its first summand is the presentation map
R(8):P2(8)→P1(8). Its second summand is the polar-product map

\[
\operatorname{Sym}^2(P_1)(8)\longrightarrow P_1(8),
\qquad u\odot v\longmapsto F(u)v+F(v)u,
\]

up to a nonzero scalar and sign. Modulo im(R), identify P1/im(R)
with I. The polar map then sends u⊙v to 2F(u)F(v). Since two is
invertible, its image is exactly I². Thus coker δ6, at the module
level and before taking degree zero, is C(8). Equivalently, the
antisymmetric relations F_i e_j−F_j e_i are already syzygies and the
symmetric relations generate all products after passing to I.

Hence, at degree zero,

\[
\operatorname{rank}\delta_6=12672-\dim C_8
=12672-\dim I_8+\dim(I^2)_8.
\]

The Hilbert function of the given resolution gives

\[
\dim I_8=\binom{15}{7}-1744=6435-1744=4691,
\]

so rank δ6=7981+r. Substitution into §2 yields

\[
h^{1,1}-1=14796-(5068-n)-(7981+r)=1747+n-r.
\]

This proves the boxed formula. The self-dual basis need not be computed:
it is used only to prove a rank-preserving identification. The algorithm
below uses the original generator basis directly.

## 4. The proposed computation uses the generator six-jet alone

**PROVED matrix specification.** Build

\[
M_8(q):k[[q]]^{4896}\longrightarrow k[[q]]^{6435}
\]

whose columns are x^α F_i(q)F_j(q), with |α|=2 and 0≤i≤j<16,
and whose rows are all degree-eight monomials. The counts are
4896=36·136 and6435=binom(15,7). Its generic rank is r.
The known F modulo q7 determines M8 modulo q7 by truncated convolution.
It does not require lifting the higher resolution maps.

**COMPUTER-CERTIFIED small combinatorial count:** for the sixteen supplied
monomial generators, the distinct products x^α f_i f_j number1829.
Each central matrix column is one standard basis vector, so central rank
is1829. Choose one column for each distinct monomial as a pivot. Other
columns with the same central monomial become zero after subtraction.
Eliminating the unit pivot block leaves a 4606×3067 q-divisible Schur
matrix. Only twelve new independent q-adic pivots are needed to reach1841.
The generator normalization and alternative choices of monomial pivots do
not change that rank.

**PROVED precision logic.** An exact q-adic rank lower bound from the
matrix modulo q7 holds for every compatible higher continuation. Track
precision lost after division by q. A determinant valuation can exceed six
if its leading coefficient is still fixed by structural divisibility of
all entries. Do not invert q in the nilpotent quotient itself.

**PROVED conditional modular transfer.** If those extra pivots are found
modulo101, they certify rank≥1841 on the characteristic-zero implicit
curve as well: the integral generator matrix lives over Z_(101)[[q]],
and a minor whose reduction has a nonzero series coefficient is nonzero
integrally and after characteristic-zero scalar extension. This rank
bridge does not require flatness of I² or identification of its special
fibre. It is a statement about a matrix between free modules. The
characteristic-zero geometry is used only after the rank certificate.

## 5. Success and failure meanings

**CONDITIONAL exact success:** r≥1841 combines with n≤94 and h11≥1
to give n=94,r=1841,h11=1,h21=31, Euler−60. This proves the generic
fibre's Hodge data, and every smooth complex fibre on the same smoothing
component has the same pair. It still does not prove torsion-free Picard
group or simple connectedness, and it does not display a finite closed
fibre's coefficients.

**OPEN if the rank lower bound is smaller.** Twelve invisible pivots do
not imply their eventual absence. If rank is only certified≥1840, the
formula gives h11≤n−92 and n≥93, but exact possibilities need further
rank information. If exact r=1840 and n=94 were independently proved,
the pair would be(2,31); if n=93, it would be(1,30).

**FAILED prerequisite check if rank>1841:** this would contradict the
accepted component bound, smoothness, and resolution hypotheses together.
Before interpreting it, verify matrix construction, q-adic precision,
lineage, and the derived-complex argument independently.

As a consistency prediction, the known determinantal family with
h0(N)=97 and Hodge pair(2,34) would have r=1843. This prediction has
not been used as proof and was not computationally tested.

## 6. Direct embedded unobstructedness once h11=1

**PROVED; no BTT dependency.** Kodaira vanishing gives H^i(O_X(1))=0
for i>0, while H^1(O_X)=H^2(O_X)=0 and H^3(O_X)=k. Consequently
the restricted tangent Euler sequence gives

\[
H^1(T_{\mathbf P^7}|_X)=0,\qquad
H^2(T_{\mathbf P^7}|_X)\simeq H^3(O_X)\simeq k.
\]

The normal exact sequence then yields

\[
0\to H^1(N)\to H^2(T_X)
\longrightarrow H^2(T_{\mathbf P^7}|_X).
\]

Serre duality with K_X=O_X identifies the dual of the last arrow with

\[
H^1(\Omega_{\mathbf P^7}|_X)=k\longrightarrow H^1(\Omega_X),
\qquad 1\longmapsto c_1(O_X(1)).
\]

The Euler connecting class is the hyperplane class, which is nonzero:
its cube has degree20. Hence this dual map is injective, and generally
h^1(N)=h11−1. Our established h11=1 makes it an isomorphism and gives
H^1(N)=0. Since X is a smooth closed subvariety, H^1(N) is an
embedded-deformation obstruction space. The Hilbert scheme is therefore
smooth at[X], with tangent dimension h^0(N)=94. This proves the Hilbert
conclusion directly, without invoking abstract Calabi--Yau deformation
unobstructedness.

## Appendix: differential signs for an independent implementation

These maps are not needed for the product-matrix job, but make the
derived-complex argument directly checkable. For i<j choose the basis
element [u,v]=u⊗v−(−1)^(ij)v⊗u. In odd degree3, use
u⊗v+v⊗u for u<v and u⊗u for a diagonal symmetric basis element.
The tensor differential is d(u⊗v)=du⊗v+(−1)^i u⊗dv.

With G7=P3⊗P4, G6=(P2⊗P4)⊕Sym²P3 and
G5=(P1⊗P4)⊕(P2⊗P3), one obtains

- d7([u,v])=[d3u,v]−(u⊗d4v+d4v⊗u). In the symmetric
  basis the diagonal coefficient in the second term has a factor2.
- d6([a,v])=[d2a,v]+[a,d4v] for a∈P2,v∈P4.
- d6(u⊗u)=[d3u,u].
- d6(u⊗v+v⊗u)=[d3u,v]+[d3v,u] for distinct u,v∈P3.

The composites vanish using d2d3=0 and d3d4=0. Dualizing the first
formula gives the linear-syzygy part plus the negative polar-product
part; changing that summand's sign or scaling its diagonal basis by2
does not change image or cokernel in characteristic≠2. This is the
precise source of the polar map used in §3.
