# Picard and Hodge decision tree

Date: 8 September 2026. Scope: the zero-context smoothing, not the older
DGLA lineage. **PROVED** below means a derivation recorded here; it is not
a claim of independent human verification. The smoothing input remains
**CONDITIONAL** on the audited computer-algebra trust boundary. No CAS or
resolution of an ideal square was run during this subtask.

The two most useful reductions are

\[
 h^{2,1}=h^0(N)-63,
 \qquad
 h^{1,1}=1+h^3(\mathbf P^7,\mathcal I^2).
\]

Once a finite smooth fibre is certified, compute its normal-space dimension
first, then the single cohomology group on the right. A good prime with
vanishing of that group already proves Picard rank one in characteristic
zero, provided the equations define a smooth integral model at that prime.
The degeneration route has a serious new obstruction: its total space
cannot be Q-factorial. The correct class-group target is generation by
the hyperplane and vertical components, not factoriality.

## 1. Inputs and decision tree

**PROVED: required hypotheses for the numerical formulae.** Work over C,
or over an exact characteristic-zero field followed by an embedding in C.
Let X be a smooth geometrically connected projective threefold with
K_X=O_X, H^1(O_X)=H^2(O_X)=0, and the complete very ample embedding
X⊂P7 defined by H, with H³=20 and h0(H)=8. These are the smooth-fibre
consequences supplied by the zero-context proof. Set S=k[a,...,h],
I⊂S the homogeneous ideal, and write script I² for the ordinary ideal
square; its associated sheaf is the sheaf square used below.

| Available input | Next exact computation | What it can establish |
|---|---|---|
| Finite algebraic curve in the certified Hilbert chart | Find and certify a smooth fibre, retaining the chart/jet certificate | An actual fibre in the required lineage |
| Certified finite smooth characteristic-zero fibre | Degree-zero kernel of the first-syzygy dual map | Exact h21 and dimension of its smooth Hilbert germ |
| The same rational fibre with certified smooth reduction at p | Degree-zero Ext4(I_p²,S_p(-8)) | Zero proves rho=1 in characteristic zero; nonzero gives an upper bound |
| Exact I² partial resolution in characteristic zero | Degree-zero dual maps d3,d4,d5 | Exact h11, h21 and Euler number |
| Only a compatible six-jet | q-adic rank certificates on fixed finite free matrices | Generic rank lower bounds and corresponding cohomology upper bounds; equality needs a second bound |
| Only abstract smoothing plus degeneration | Global class group modulo vertical components | Potential Picard-rank proof; still OPEN |

**PROVED within the accepted source trust boundary:** today's fixed-chart
construction now supplies a finite algebraic pointed family with smooth
geometric generic fibre; see `FIXED_CHART_REVIEW.md`. It uses 291 invariant
normalized cubic coefficients, 270 independent local equations and 21
free coordinates, with the chosen polynomial paths matching the six-jet.
**OPEN:** the resulting algebraic coefficient field has not yet been
made computationally convenient, nor has a smooth closed fibre at a
specified nonzero algebraic/rational q been selected. Either an exact
coefficient-field model of the generic fibre or such a closed fibre is
valid input below. A specialization of the six-jet polynomial at q=1 is
not. The normal and square scripts must not be fed that truncation.

## 2. Complete derivation of h0(N)=63+h21

**PROVED.** Kodaira vanishing, applied to K_X⊗H=H, gives H^i(H)=0
for i>0. Connectedness gives H0(O_X)=C, and the CY vanishings give
H1(O_X)=H2(O_X)=0. The restricted Euler sequence is

\[
0\longrightarrow O_X\longrightarrow O_X(H)^{\oplus8}
\longrightarrow T_{\mathbf P^7}|_X\longrightarrow0.
\]

Its H0/H1 part is

\[
0\longrightarrow\mathbf C\longrightarrow\mathbf C^{64}
\longrightarrow H^0(T_{\mathbf P^7}|_X)\longrightarrow0,
\qquad H^1(T_{\mathbf P^7}|_X)=0.
\]

The first map is injective because it is the Euler map on global sections.
Hence h0(TP7|X)=64−1=63. For the H1 vanishing, both
H1(O_X(H)) and H2(O_X) are zero. No claim that H2(TP7|X)=0
is needed; in fact H2(TP7|X)≅H3(O_X)≅C.

A nowhere-vanishing volume form identifies T_X with Ω_X². Hodge
symmetry and H2(O_X)=0 give H0(T_X)=H0(Ω_X²)=0.
Also H1(T_X)=H1(Ω_X²), of dimension h21. Smoothness of X in
the smooth ambient space makes the normal sequence exact as vector bundles:

\[
0\longrightarrow T_X\longrightarrow T_{\mathbf P^7}|_X
\longrightarrow N_{X/\mathbf P^7}\longrightarrow0.
\]

Thus its cohomology gives the short exact sequence

\[
0\longrightarrow\mathbf C^{63}\longrightarrow H^0(N)
\longrightarrow H^1(T_X)\longrightarrow0,
\]

proving h0(N)=63+h21. The 63 is the dimension of PGL8, and
H0(T_X)=0 says the smooth fibre has no infinitesimal automorphisms.
This should not be confused with the 56-dimensional orbit of the singular
monomial point, whose stabilizer has dimension seven.

**PROVED, using standard CY deformation theory.** BTT gives an
unobstructed abstract deformation space of dimension h21. H2(O_X)=0
removes the obstruction to extending H, and H1(O_X)=0 gives uniqueness.
Vanishing of higher cohomology of H makes its eight sections extend;
very ampleness is open. Projective frames add 63 dimensions. Consequently
the Hilbert germ at the smooth fibre is smooth of dimension h0(N).
It is legitimate to conclude component dimension from h0(N) here;
at the singular special fibre, tangent dimension 109 is not local dimension.

## 3. Conormal and Euler sequences: only two groups of I²

**PROVED.** Put C=I/I² as a sheaf on X and E=Ω_P7|X. The conormal
sequence is short exact because X is smooth:

\[
0\longrightarrow C\longrightarrow E\longrightarrow Ω_X
\longrightarrow0.
\]

The hypothesis for this injectivity is made explicit in
[Stacks, Section 37.63(2), tag 06BB](https://stacks.math.columbia.edu/tag/06BB).
It does not hold automatically for the singular special fibre.
The cotangent Euler sequence is

\[
0\longrightarrow E\longrightarrow O_X(-H)^{\oplus8}
\longrightarrow O_X\longrightarrow0.
\]

By Serre duality and Kodaira vanishing, H^i(O_X(-H))=0 for i=0,1,2,
and H3(O_X(-H))≅H0(O_X(H))^*, of dimension eight. Therefore

\[
(h^0(E),h^1(E),h^2(E),h^3(E))=(0,1,0,63).
\]

For the last entry, the map H3(O(-H))^8→H3(O) is surjective:
its Serre-dual map is the injective Euler map C→C64. Hence its
kernel has dimension 63.

H0(Ω_X)=0 by Hodge symmetry and H1(O_X)=0. The map
H1(E)=C→H1(Ω_X) sends the Euler extension class to c1(H).
This class is nonzero: c1(H)³ evaluates to 20. The conormal long exact
sequence now gives

\[
H^0(C)=H^1(C)=0,
\qquad
0\longrightarrow\mathbf C\longrightarrow H^1(Ω_X)
\longrightarrow H^2(C)\longrightarrow0.
\]

Thus h11=1+h2(C). Moreover H3(Ω_X)=h13=h20=0, so

\[
0\longrightarrow H^2(Ω_X)\longrightarrow H^3(C)
\longrightarrow\mathbf C^{63}\longrightarrow0,
\]

giving h3(C)=63+h21. This also agrees with Serre duality
H3(C)^*≅H0(N).

**PROVED.** Regard all ideal sheaves as sheaves on P7 and use

\[
0\longrightarrow\mathcal I\longrightarrow O_{\mathbf P^7}
\longrightarrow O_X\longrightarrow0,
\qquad
0\longrightarrow\mathcal I^2\longrightarrow\mathcal I
\longrightarrow C\longrightarrow0.
\]

At twist zero, H^j(I)=0 for j≠4 and H4(I)=C. This follows directly
from the first sequence, the CY cohomology of O_X and the cohomology of
O_P7; it does not require resolving I. In the second sequence, support
dimension three gives H4(C)=0, so

\[
H^2(C)\simeq H^3(\mathcal I^2),
\qquad
0\longrightarrow H^3(C)\longrightarrow H^4(\mathcal I^2)
\longrightarrow\mathbf C\longrightarrow0.
\]

Consequently

\[
\boxed{h^{1,1}=1+h^3(\mathcal I^2)},\qquad
\boxed{h^{2,1}=h^4(\mathcal I^2)-64}.
\]

No twists other than zero are required. The first of these is the primary
Picard computation; the second independently checks the cheaper normal
calculation. By duality, also h1(N)=h11−1. Thus a smooth Hilbert germ
does not force H1(N)=0: a nonzero obstruction *space* can carry an
identically zero obstruction map.

## 4. What Fausk's method contributes, and what it does not

**PROVED: methodological transfer.** The relevant primary passage is
Fausk, *Pfaffian Calabi–Yau threefolds, Stanley–Reisner schemes and mirror
symmetry*, arXiv:1205.4871, Lemma 3.5.3 and Proposition 3.5.4,
printed pp.44–46. It constructs a resolution of the square of the ideal
for a specific complete-intersection fibre in P6 and combines its
cohomology with the Euler and conormal sequences. This is precisely the
method generalized above to P7. Its particular resolution and numerical
Hodge pair belong to that fibre and cannot be transferred here.
[Primary PDF](https://arxiv.org/pdf/1205.4871#page=44)

**OPEN: local source limitation.** A local fausk.tex was not found in the
named heap/sr/zero-context/geography repositories, including ignored files.
The web PDF text was inspected directly. The screenshot wrapper returned
reference strings, without viewable raster content. An apparent shift
multiplicity inconsistency in the extracted Fausk resolution was therefore
not adjudicated; none of its shift multiplicities or numerical calculations
is used here. The P7 formulae above were independently derived before this
source-verification phase.

**PROVED: input dependence.** The Betti table 1,16,30,16,1 in shifts
0,3,4,5,8 supplies the Hilbert series, degree, linearly normal ACM
embedding and the dimensions of the first normal-space matrix. Together
with smoothness it supports the known CY vanishings. It does not supply
the Betti table of I² or the ranks of its differential maps. Even a fixed
Betti table for I² supplies dimensions of cohomology-vector-space terms,
not in general the ranks of the intervening maps. The original fibre's
equations determine the products f_i f_j and all their relations.
Fausk's complete-intersection square resolution used additional structure
that is absent from a bare codimension-four Gorenstein Betti table.

## 5. Exact computations and cost reductions

**PROVED.** Given an actual fibre, a first-syzygy matrix d2 gives

\[
\operatorname{Hom}_S(I,S/I)_0=
\ker\big((S/I)_3^{16}\longrightarrow(S/I)_4^{30}\big).
\]

The map is the transpose of d2 modulo I, with the indicated grading
shifts. Here dim R3=104 and dim R4=232, so the scalar matrix is
6960×1664. A homogeneous-kernel computation avoids materializing its
dense scalar form. The script uses core M2 `Hom`, retaining shifts.
In the ACM neighbourhood, graded degree-zero Hom agrees with H0(N).

**PROVED.** Graded local duality over the eight-variable polynomial ring
gives, at degree zero,

\[
H^3(\widetilde{I^2})^*\simeq
\operatorname{Ext}^4_S(I^2,S(-8))_0,
\quad
H^4(\widetilde{I^2})^*\simeq
\operatorname{Ext}^3_S(I^2,S(-8))_0.
\]

Equivalently use Ext5 and Ext4 of S/I². The local-duality dependency is
[Stacks, Theorem 47.18.3, tag 0A84](https://stacks.math.columbia.edu/tag/0A84);
the displayed shifts are the standard graded specialization to S with
canonical module S(-8).

Let F•→I² be a graded free resolution, and set
V_i=Hom_S(F_i,S(-8))_0. The induced maps δ_i:V_i→V_(i+1) give

\[
e_3=\dim V_3-\operatorname{rank}\delta_2-
\operatorname{rank}\delta_3,
\quad
e_4=\dim V_4-\operatorname{rank}\delta_3-
\operatorname{rank}\delta_4.
\]

Then h21=e3−64 and h11=1+e4. Resolving the *ideal module* through
F5 is sufficient. There is no need to construct whole Ext modules or
resolve farther. A summand S(-d) of F_i contributes S_(d−8) to V_i;
summands with d<8 contribute zero. Maps in irrelevant degrees can be
discarded after the resolution, and scalar ranks are computed exactly.
The script saves the partial resolution's module degrees/differential
entries and the three degree-zero scalar matrices.

**CONDITIONAL script:** `scripts/hodge_from_fibre.m2` has two phases:
`GS_HODGE_PHASE=normal` and `GS_HODGE_PHASE=square`. Its syntax was
inspected against installed M2 1.20 source files `Core/ext.m2`,
`Core/matrix1.m2`, `Core/basis.m2`, and the `LengthLimit` documentation.
The root agent then ran a tiny exact API smoke check, including zero
terminal modules: `logs/20260908T105750-hodge-api.stdout` reports
`HODGE_DEGREE_ZERO_MAP_API_OK` (about 5.8 seconds, 83 MB). The fibre
script itself has not been run on a new smooth GS fibre. Use the run's bounded
sequential runner and existing single-thread environment. Its required
input is an .m2 file defining S and I and a separate certificate file.
The script checks Hilbert sanity, but does not prove that certificate.

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 VECLIB_MAXIMUM_THREADS=1 \
 GS_FIBRE_INPUT=/absolute/path/to/certified_fibre.m2 \
 GS_FIBRE_CERTIFICATE=/absolute/path/to/fibre_certificate.md \
 GS_HODGE_PHASE=normal GS_HODGE_PREFIX=/absolute/path/to/checkpoint \
 M2 --script runs/astra-daytime-2026-09-08/scripts/hodge_from_fibre.m2
```

For the square calculation replace `normal` by `square`. The absolute
input paths are deliberately not invented: the overnight equation job
must first produce them. A rational-function or algebraic-number field is
acceptable if exact, but rational specialization generally reduces cost.

**HEURISTIC resource envelopes, not benchmarks.** Normal computation:
minutes to about an hour, perhaps 0.5–2 GB for sparse rational input.
I² partial resolution: tens of minutes to several hours and potentially
more than 3 GB; start over a good finite field and enforce the queue's
memory/time cap. If no checkpoint appears before the cap, stop and retain
input/logs. Do not run another CAS or skeletal-polytope job simultaneously.

## 6. A modular vanishing can prove rho=1

**CONDITIONAL, with an exact implication.** Suppose the finite rational
equations extend to a projective smooth model over Z_(p), with the stated
Hilbert/CY data on its fibres. Smoothness must be certified at p and the
integral flat family must be established; reducing arbitrary equations
modulo p is insufficient. The relative conormal bundle is then locally
free, hence flat over the base. Upper semicontinuity
([Stacks, Lemma 36.32.1, tag 0BDN](https://stacks.math.columbia.edu/tag/0BDN)) gives

\[
h^2(C_{\mathbf Q})\le h^2(C_{\mathbf F_p}).
\]

The ideal sequences compute the right side as
dim Ext4(I_p²,S_p(-8))_0. If this is zero, h11(X_Q)=1 follows from
the characteristic-zero formula and the ample class. This is a complete
Picard-rank certificate without a rational I² resolution. Nonzero output
is only an upper bound. It does not establish that the generic rank equals
the reduced rank. `GS_HODGE_MODULAR_BOUND=1` enables the script's finite
field mode and labels every output accordingly. The resulting finite-field
cohomology is not identified with the Picard group in characteristic p.

**OPEN:** obtaining h21 exactly from a modular upper bound needs a
matching lower bound (for example, a proved 94-dimensional smoothing
component), or an exact characteristic-zero normal calculation. Several
primes agreeing is evidence for a conjecture, not that missing lower bound.

## 7. What the six-jet can certify

**PROVED: finite-determinacy of nonzero minors, with an important refinement.**
Let A(q) be a finite matrix over k[[q]], with entries known modulo q7.
Any minor whose first nonzero coefficient occurs at order ≤6 has that
coefficient fixed in every higher lift. Hence its nonvanishing certifies
a generic rank lower bound. Zero modulo q7 does not prove the minor
vanishes formally. The same statement applies to a finite complex that is
known to calculate the desired cohomology on the generic fibre.

Orders greater than six can sometimes also be certified. Eliminate
constant unit pivots, and suppose an r×r residual matrix has all entries
divisible by q. Then

\[
\det(qB_1+q^2B_2+\cdots)=q^r\det(B_1)+O(q^{r+1}).
\]

Nonzero det(B1) proves the leading q^r term even when r>6, because
the structural divisibility of *every* entry prevents omitted higher
terms from contributing at order r. More general q-adic pivot valuations
must track the precision loss in divisions. A raw truncate-and-invert-q
operation is invalid: q is nilpotent in k[q]/(q7).

**PROVED: normal-space application.** Along the compatible formal family,
the degree-three and degree-four coordinate pieces have free monomial
frames around the special fibre. The known generators and first syzygies
therefore define the 6960×1664 matrix D(q) modulo q7. At q=0 its
rank is 1664−109=1555. Eliminate those constant pivots once. The
Schur complement has size 5405×109 and is divisible by q. Compute
successive constant pivot blocks in its q-adic coefficients, keeping exact
row/column data. Fifteen additional pivots would recover the known
h0(N)≤94 bound; more would strictly improve it. In a suitable local
Hilbert chart, the existing rank-15 quadratic Jacobian already explains
why that first bound is expected.

**OPEN: equality.** A rank lower bound r gives h0(N)≤1664−r and
h21≤1601−r. To prove equality, supply either a formal kernel of the
complementary rank or a matching lower bound on the component dimension.
The smooth generic fibre then has Hilbert-component dimension h0(N).
A six-jet alone does not turn an upper bound into equality. In particular,
the dimension-38 quadratic component gives an upper bound until its full
branch is established; it is not the missing lower bound.

**OPEN: conormal application.** One could build a finite complex for the
generic conormal cohomology using products of the six-jet generators and
bounded-degree presentations. The decisive extra obligations are a
justified degree/regularity bound, compatibility of the presentation with
the actual formal lift, and a finite free cohomology complex. No such
certified conormal complex has yet been produced. The existing F/R jet
does not itself provide a flat resolution of I².

**FAILED: naive semicontinuity from the monomial square.** Flatness of
S/I over the smoothing parameter does not imply flatness of S/I² or of
I/I². The special fibre is not lci. Although an ideal square inside the
torsion-free ambient DVR algebra is itself DVR-flat, its tensor reduction
need not inject into the ambient special fibre; it can have extra kernel.
Thus its reduction need not be the ordinary monomial square I_M².
Computing h3(I_M²)=0, if that happened, would not establish h11=1 for
the smoothing without a separate base-change/flatness argument.

## 8. Picard rank, the Picard group and torsion

**PROVED.** The analytic exponential sequence and GAGA give

\[
H^1(O_X)\longrightarrow\operatorname{Pic}(X)
\xrightarrow{c_1}H^2(X,\mathbf Z)\longrightarrow H^2(O_X).
\]

Both outer terms vanish. Hence Pic(X)≅H2(X,Z), including torsion,
and Pic0(X)=0. Hodge decomposition and h20=h02=0 imply that the
rank of this group is b2=h11. Therefore rho(X)=h11(X).

**PROVED.** If H=nL modulo torsion, then 20=H³=n³L³. No integer
n>1 has n³ dividing 20. Thus H is primitive even in Pic modulo torsion.
If rho=1 is proved, it follows that Pic(X)/torsion=Z·H. It does not
follow that torsion is zero. Pic(X)=Z·H additionally requires absence
of torsion, equivalently absence of torsion in H2(X,Z); the latter is
related by universal coefficients to torsion in H1(X,Z). Neither
simple connectedness nor torsion-freeness follows from the present
Stanley–Reisner degeneration argument. No claim on the full Picard group
should be hidden inside a Picard-rank computation.

## 9. The special Picard group: a conceptual computation

**PROVED.** Write X_M=∪_σ P³_σ over its twenty tetrahedral facets.
Every nonempty intersection of components is a coordinate projective
space. The augmented Cech complex of the constant sheaves on these
closed components is exact: at a point its stalk is the augmented
cochain complex of the simplex of components containing that point.
The associated spectral sequence is

\[
E_1^{p,q}=\bigoplus_{\sigma_0<\cdots<\sigma_p}
 H^q(P_{\sigma_0}\cap\cdots\cap P_{\sigma_p},\mathbf Z)
\Longrightarrow H^{p+q}(X_M,\mathbf Z).
\]

The q=0 row computes the cohomology of the facet nerve. The nerve
lemma for the cover of the triangulated sphere by its simplices identifies
its homotopy type with |M|≅S³. Thus E2^(1,0)=E2^(2,0)=0.
Odd q rows vanish. The E2^(0,2) term consists of compatible degree
classes on the P³ components. Two classes must agree whenever their
intersection has dimension at least one. Adjacency across triangles is
connected in this triangulated sphere, so this group is Z.

The only potentially nonzero outgoing differential from that term is
d3:E3^(0,2)→E3^(3,0). The actual global class c1(O_X_M(1))
restricts to degree one on every component, so the generator survives:
d3=0. There are no other total-degree-two terms. Therefore
H2(X_M,Z)=Z, with generator H. The audited ACM/CY cohomology gives
H1(O_X_M)=H2(O_X_M)=0. Exponential and GAGA yield

\[
\operatorname{Pic}(X_M)=\mathbf Z H.
\]

This is an integral result, not just a computation of a rational rank.
Its use of the sphere property is explicit; the numerical f-vector alone
would not suffice.

## 10. Precise extension theorem and the Q-factorial obstruction

**PROVED.** Let Y→Spec C[[q]] be a projective DVR smoothing with
this special fibre and geometrically connected smooth generic fibre.
For the successive thickenings X_n, the square-zero ideal in
X_n⊂X_(n+1) is O_X_M. The exact obstruction sequence for line
bundles gives Pic(X_(n+1))≅Pic(X_n), because H1 and H2 of that
ideal vanish. This is precisely
[Stacks, Lemma 37.4.1, tag 0C6R](https://stacks.math.columbia.edu/tag/0C6R).
Grothendieck existence for a projective scheme over a complete Noetherian
ring algebraizes the compatible line bundles; full faithfulness gives
uniqueness. See
[Stacks, Lemma 30.24.3, tag 0885](https://stacks.math.columbia.edu/tag/0885).
Local freeness holds near the special fibre by Nakayama, and properness
excludes a nonempty closed non-locally-free locus disjoint from that fibre.
Thus Pic(Y)=Pic(X_M)=Z·H.

This proves extension *from the special fibre to Y*. It does not prove
that every generic-fibre divisor extends as a Cartier divisor.

**PROVED.** Y is normal. Flatness lifts Cohen–Macaulayness from the
special fibre; codimension-one points are either in the smooth generic
fibre or are generic points of its reduced central components, where the
morphism is smooth. Thus S2 and R1 hold. Apply
[Stacks, Lemma 10.157.4, tag 031S](https://stacks.math.columbia.edu/tag/031S).

**CONDITIONAL abstract criterion.** On a normal model, taking closures
extends generic divisors as Weil divisors. Local factoriality would make
them Cartier; Q-factoriality would make positive multiples Cartier and
would suffice for a rational rank argument. The factorial case is made
precise in
[Stacks, Lemma 31.28.7, tag 0BE9](https://stacks.math.columbia.edu/tag/0BE9).
For geometric Picard rank one would also need a finite base extension over
which the geometric Neron–Severi classes descend. Factoriality must be
checked on the resulting model, not silently assumed after ramification.

**FAILED, for this degeneration: the criterion cannot hold globally.**
Let D1,...,D20 be the central prime divisors. If mD1 were Cartier,
its line bundle would be nH on Y. Its generic restriction is trivial,
so ampleness gives n=0. Hence mD1=div(g). On the normal proper
generic fibre, g has no zeros or poles, and is therefore an invertible
global function. Geometric connectedness makes g an element of C((q))*.
Its divisor is ord_q(g)(D1+...+D20), since the special fibre is reduced.
This cannot equal mD1. Thus Y is not Q-factorial. The proof survives
every finite ramified base change, which has the same reduced special fibre.

More precisely, closure of generic divisors gives

\[
0\longrightarrow\mathbf Z(1,\ldots,1)
\longrightarrow\mathbf Z^{20}\longrightarrow\operatorname{Cl}(Y)
\longrightarrow\operatorname{Pic}(Y_\eta)\longrightarrow0.
\]

The rank-19 vertical subgroup meets Pic(Y)=Z·H trivially. It is
unavoidable non-Cartier divisor information. A separate complete proof is
saved in `PICARD_VERTICAL_CLASS_OBSTRUCTION.md`.

**OPEN replacement criterion.** After an extension splitting geometric
Neron–Severi classes, prove
Cl(Y)_Q is generated by H and the central D_i. Then the exact sequence
above proves rho(Y_geometric_eta)=1. Local computations must retain
the classes of incident vertical components. One needs a single globally
compatible linear combination of those components that cancels the local
class of every generic divisor closure. Merely knowing separate local
generating sets does not supply that compatibility.

## 11. Which completed local rings are needed

**PROVED input description; OPEN class groups.** For each coordinate
vertex v, the relevant completed four-dimensional normal local ring is

\[
A_v=\mathbf C[[q,z_j:j\ne v]]/
\big(F_i(q,x_v=1,x_j=z_j):1\le i\le16\big).
\]

Here F is the actual all-orders lifted family, with its actual parameter,
not the polynomial truncation. Under q=s^e, replace q by s^e and use
the resulting normal model. The known S3 action can reduce equivariant
vertex calculations to chart representatives a,b,d. The classes to track
include the height-one primes
(q,z_j:j∉σ) for central facets σ containing v. Their sum is div(q).
Other singular strata must be examined too: the existing total-space audit
proves generic regularity on facets and singularity at all eight vertices;
it does not prove the vertices exhaust the total singular locus.

**COMPUTER-CERTIFIED source result.** The source audit finds every
generator differential, including derivatives in all 109 embedded tangent
directions, zero at every coordinate vertex. A DVR total space has local
dimension four and ambient embedding dimension eight there, so it is
singular. Higher base terms cannot change that first differential.

**PROVED additional obstruction.** In chart d=1 the central ideal has
the seven minimal monomial generators

\[
(ah,bf,bg,ce,ef,fh,acg)\subset\mathbf C[[a,b,c,e,f,g,h]].
\]

Its height is four, so it is not a complete intersection. Were the total
local ring lci, its quotient by the regular parameter q would also be
lci; contradiction. Thus a local complete-intersection parafactoriality
theorem cannot be applied at this vertex.

**OPEN.** The six-jet determines A_v/(q7), not A_v. There is no
proved finite-determinacy theorem here identifying class groups from that
truncation, and the non-isolated central singularities make such a theorem
especially nonautomatic. No inference of factoriality, Q-factoriality or
Picard rank from the six-jet local equations is currently justified.

## 12. Claim ledger, dependencies and remaining obligations

| Claim | State | Evidence / downstream use |
|---|---|---|
| h0N=63+h21 | PROVED | Euler + normal sequence; exact h21 and smooth Hilbert dimension |
| h11=1+h3(I²), h21=h4(I²)−64 | PROVED | Two ideal sequences + conormal + Euler; optimized scripts |
| Pic(X_M)=ZH integrally | PROVED | Closed-component spectral sequence + sphere + exponential |
| Pic(Y)=ZH for the complete DVR model | PROVED | H1/H2 vanishing + 0C6R + Grothendieck existence |
| Every such Y fails Q-factoriality | PROVED | Twenty vertical divisors versus Pic(Y); eliminates that route |
| Good-prime Ext4 vanishing implies rho=1 | CONDITIONAL | Requires certified smooth integral model; exact semicontinuity implication |
| Existing six-jet determines exact generic normal rank | OPEN | Need decisive ranks and matching lower bound |
| Existing six-jet determines local class groups | OPEN | No finite-determinacy input |
| Special I_M² can be used by naive semicontinuity | FAILED | Conormal/square base change is not automatic at nonlci fibre |
| Picard rank / full Picard group of the new smoothing | OPEN | No fibre-specific rank certificate yet; torsion separate |

Dependencies: smooth CY input → Euler/normal/conormal formulae → exact
matrix targets; finite smooth fibre → normal/square input; smooth integral
model → modular semicontinuity; sphere + special O-cohomology → special
Pic → formal Pic → vertical Q-factorial obstruction. No arrow goes from
special Pic directly to generic Pic.

Primary-source phase: the cited Stacks passages were directly inspected
8 September 2026 (`inspected-primary`). Fausk's mathematical passage was
read in primary PDF extraction, with the rendering limitation explicitly
recorded above. The independent deductions were frozen before that source
phase in `PICARD_HODGE_DISCOVERY.md` (SHA256
`0220ce0ee8131505ac77b67520540ca696162b850ea2e04096d819631a26c1f3`).
The later vertical-divisor deduction is separately timestamped by this
run's artifacts and supersedes the discovery freeze's merely conditional
factoriality suggestion. The requested targeted-verification skill
influenced the separation of discovery, source verification, and proof
obligations; no paper-wide proof re-audit was attempted.
