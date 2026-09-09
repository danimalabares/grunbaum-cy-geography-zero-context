# Independent targeted review of the finite fixed chart

Review date: 2026-09-08. Scope: the local mathematics of the new finite
chart and inspection of `scripts/build_fixed_chart.py` and
`scripts/fixed_curve_lift.py`. No script was executed by this reviewer and
no CAS was launched. The reported rank/minor computations are accepted as
exact computational input, not independently recomputed here. Human
verification is not claimed.

**PROVED, within the accepted source trust boundary:** the proposed chart
does give a finite algebraic pointed family whose geometric generic fibre
is smooth, provided the full first-syzygy lifting identification below is
included. This is stronger than another finite jet. It does not yet give a
chosen smooth fibre at a specified nonzero rational/algebraic value of q.
There is no need to solve the universal 38-parameter Kuranishi problem to
obtain this finite family.

## 1. The Schur chart represents the local fixed Hilbert functor

Let k be Q or F_101. Choose the ordered sixteen monomial generators f_i of
I_M. The degree-three monomials outside their span form a 104-element set
B_3. Every sufficiently near embedded deformation has a unique normalized
generator row

    F_i = f_i + sum_{m in B_3} c_(i,m) m.

**PROVED.** The normalization is legitimate: the coefficient matrix on the
sixteen chosen pivot cubics is the identity at the special point and remains
invertible on an open Grassmann chart. The special ideal has no generators
in other degrees, and its cohomology vanishings imply that a flat Hilbert
deformation over an Artin local base still has these sixteen cubic
generators, by base change and Nakayama. Uniqueness is matrix inversion,
not a choice of a new deformation direction.

The group permutes both the sixteen pivot monomials and B_3. A normalized
ideal is fixed precisely when the coefficient pairs (i,m) have constant
values on the group orbits. **COMPUTER-CERTIFIED:** the current chart has
291 such orbits. No syzygy-frame invariance assumption is needed.

Write the degree-four multiplication matrix, with its 128 columns x_jF_i
and 330 quartic rows, in the ordered block form

    mu_F = [ A  B ]     A:98x98, B:98x30,
           [ C  D ]     C:232x98, D:232x30.

At zero, A=I, C=D=0, and each column of B_0 has one entry 1. On det(A)!=0,

    U=A^(-1)B,
    E=D-CU,
    mu_F [-U; I_30]=0  iff E=0.

**PROVED.** The constant thirty relation columns specialize to a basis of
the degree-four relations of I_M. Each is the difference between a
nonpivot monomial product and the selected pivot product with the same
monomial. There are exactly 128-98=30 independent such differences. The
source resolution says that the *full* first-syzygy module is generated in
degree four by thirty generators; hence this basis generates that full
module. Merely knowing that there are thirty degree-four relations would
not suffice without this last resolution input.

**PROVED flatness.** Let T be a noetherian local base centered at the
specified special point and satisfying all E=0. Set M=T[x]/(F). The lifted
relations above generate the complete special kernel of the generator map.
For each degree d, write V_d -> I_d -> 0, with V_d the free degree-d
generator module and K_d its kernel. The image of
K_d tensor k in V_d tensor k contains all special syzygies. Thus
I_d tensor k -> T[x]_d tensor k is injective. In the exact sequence
0 -> I_d -> T[x]_d -> M_d -> 0 this gives Tor_1^T(M_d,k)=0. Since M_d is a
finite T-module, the local flatness criterion makes it free. Consequently
M is degreewise flat and Proj(M) is a flat projective family with the
specified Hilbert polynomial. This works over arbitrary noetherian local
bases, not just a DVR, and does not assume that a single truncated FR
identity proves flatness over an untruncated base.

Conversely, every local Hilbert deformation has normalized F and a free
98-dimensional degree-four ideal, hence satisfies E=0. The full Schur
incidence chart and the fixed Hilbert scheme therefore have the same
completed local functor. Openness supplies an algebraic neighborhood where
this description applies; it makes no assertion about arbitrary remote
components of the global polynomial incidence scheme.

## 2. Why 270 selected equations suffice locally

**COMPUTER-CERTIFIED input:** the linearization of the 6960 entries of E
has rank 270 on the 291 coefficient coordinates, and the selected square
minor in the 270 dependent coordinates is -1. The script's exact rational
elimination and independent determinant computation implement this claim;
`data/fixed_chart.json` records `linear_rank:270` and
`jacobian_minor:"-1"`.

**PROVED using the source obstruction calculation.** In characteristic
zero, the complete invariant obstruction space vanishes. The fixed Hilbert
germ is therefore formally smooth. Its tangent dimension is 21, as also
checked independently by the representation count 10 intrinsic + 11
coordinate-orbit directions in `HILBERT_EXPLANATION.md`.

Let J_sel be the ideal of the selected 270 entries, and J_full that of all
6960 entries. The implicit-function theorem gives

    Q[[z_1,...,z_291]]/J_sel = Q[[w_1,...,w_21]].

The full quotient is a formally smooth ring of dimension21 and is a
quotient of this domain. A nonzero ideal in a regular local domain lowers
dimension. Hence J_sel=J_full in the completed local ring. Faithful
flatness of completion gives the corresponding equality in the local
algebraic ring. In particular all 6690 omitted equations vanish locally.
This conclusion uses the complete obstruction theorem and the local
Hilbert identification, not merely the rank of the Jacobian.

**OPEN globally.** The 270 equations can have other components or points
away from this neighborhood on which omitted equations do not vanish.
Exports should retain all full equations or explicitly specify the unique
local branch through the stated origin and the determinant localizations.
A numerical root of the selected equations alone is not automatically a
flat member of the intended family.

## 3. Integral continuation and the prime101 certificate

Let A_101=Z_(101). The normalization of the certified six-jet has
coefficients in A_101: the inverse of an I+O(q) matrix is formed by
additions and products of its coefficients and introduces no new prime
denominators. Fix each of the 21 free coordinates equal to its normalized
six-jet polynomial, with higher coefficients zero.

**PROVED.** The constant selected Jacobian determinant -1 yields a unique
formal solution for all dependent coordinates in A_101[[q]]. The solution
agrees with the normalized certified six-jet modulo q^7: the latter is
already a solution of the selected equations modulo q^7, and formal
implicit uniqueness holds to each order.

There are two valid justifications for omitted equations integrally:

1. **PROVED from the source's integral obstruction theory**, when stated
   for the relative fixed Hilbert functor: the complete invariant
   obstruction space in characteristic101 is zero, and the tangent
   dimension21 has good base change. Together with an A_101-valued origin
   this gives relative formal smoothness of dimension21.
2. **PROVED by a shorter route avoiding that extension of wording:** first
   solve the selected subsystem over A_101[[w]] using its unit minor. Its
   residual full equations vanish after embedding into Q[[w]] by §2. The
   map A_101[[w]] -> Q[[w]] is injective, so they already vanish over
   A_101[[w]]. This proves the required integral identity directly.

The second route is recommended. It needs the characteristic-zero fixed
smoothness result, the integral polynomial chart, and the unit determinant;
it does not require a new computation of an integral universal Kuranishi
map. Flatness over A_101[[q]] then follows from the first-syzygy argument
and the A_101-flat special fibre, or degreewise from the local criterion.

**PROVED under the existing smoothness-certificate trust boundary.** The
new curve has the same ideal modulo q^7 as the certified generic six-jet,
up to a generator-basis matrix equal to I modulo q. This transformation is
independent of the projective coordinates, so the relative Jacobian matrix
transforms by the same invertible generator matrix. Cauchy–Binet shows that
the ideal generated by the appropriate Jacobian minors is unchanged.
Thus the source's characteristic101 valuative certificates transfer to
this new continuation. They give a geometrically smooth generic fibre in
characteristic101, and the source's properness/closed nonsmooth-locus
argument transfers smoothness to characteristic zero.

The determinant -1 alone does not prove smoothness of any fibre; its roles
are integral uniqueness and the persistence of the six-jet. The source
smoothness certificates do the remaining work. A future choice of a prime
other than101 is useful reconnaissance, but the existing certificates do
not automatically apply at that other prime.

## 4. What finite equations now mean

**PROVED.** Introduce the 2940 entries of U as auxiliary coordinates.
Then

    A(z)U=B(z),
    D(z)-C(z)U=0,
    z_free=gamma_free(q),
    F_i(x,z)=0,

are finite polynomial equations with coefficients in A_101 (clear the
known six-jet denominators if desired). Each Schur equation has been
replaced by polynomial equations bilinear in z,U. Include det(A)!=0 and
specify the point q=0,z=0,U=U0. The base has a unique curve germ over Q at
that point; over A_101 it is a relative curve germ. Equivalently, solve all
top equations and the selected270 bottom equations and retain the origin
branch; its other bottom equations vanish by §2–3.

This is an explicit finite algebraic pointed family, not merely an
existence theorem for algebraization. Its function field K is a finite
extension of Q(q): the curve is étale over the q-line near the origin.
The sixteen cubics F_i over K define an actual smooth generic Calabi–Yau
threefold. The origin identifies the intended algebraic branch without
claiming equality to the unspecified all-orders zero-context arc. It
agrees with its normalized six-jet, and its smooth fibres lie on the same
localized fixed germ and hence the same smoothing component.

**OPEN concrete specialization.** No numerical q0, number field K0, and
root z0 of the finite system have yet been selected and certified to
produce a smooth fibre. There is a nonempty open subset of the origin
component with smooth fibres, so such algebraic closed points exist; this
does not identify one. Overnight output should distinguish this current
finite family/smooth generic fibre from a displayed smooth fibre with
specific finite coefficients. It must verify the origin branch, all full
equations, flatness/Hilbert data, and smoothness for any chosen root.

## 5. Script inspection

**PROVED code correspondence by inspection.** `build_fixed_chart.py`
constructs monomial multiplication, chooses one representative column
per central quartic, and forms the linearization
D_1-C_1B_0 of E. Its orbit construction agrees with fixed normalized ideals.
The rational elimination retains original independent equations; the
determinant is computed separately on their original coefficient rows.
The file writer refuses to replace an incompatible existing chart.

**PROVED recurrence by inspection.** Write mu_P for the pivot columns and
mu_E for the extra columns. From mu_E-mu_P U=0, order n gives

    L(z_n) - mu_P(0) U_n
      - sum_{i=1}^{n-1} mu_P(z_i) U_(n-i) = 0.

The script uses the lower232 rows to solve the same selected270 linear
equations for z_dep,n, the upper98 rows to recover U_n, and checks all
6960 lower residuals. Its signs agree with this equation. Its generator
normalization H(q)P(q)^(-1) is on the correct side and checks all pivot
coefficients and orbit equalities through order6.

**OPEN validation boundary.** This review did not execute either script.
Modular jets beyond order6 are exact finite checks only; they do not
independently certify polynomial/rational termination or a characteristic-
zero nonzero determinant. The finite-family argument above is independent
of eventual termination of the coefficient series.

**HEURISTIC resource assessment.** For order24 the retained arrays are
small (roughly 25*(291+2940) field entries plus chart metadata); Python
loop time is the more likely bottleneck than memory. The convolution costs
quadratically many matrix multiplications in the order. The script avoids
large symbolic expression expansion and refactors the 270-by-270 matrix
only once.

**OPEN reproducibility hardening at review snapshot.** The resume code
checks the prime and free-coordinate list, but not input hashes, full
checkpoint provenance, old residuals, or the first six coefficients.
`NORMALIZED_SIXJET_MATCH` is printed from the requested order and is not
proof that an untrusted resumed prefix was verified. The normalized jet
file is written unconditionally. Recommended repairs are to record and
validate chart/source/script hashes, validate checkpoint shapes and the
six-jet prefix, and refuse to replace a different existing normalized-jet
file. These concern checkpoint reliability, not the fresh-run recurrence.

## Ledger and version boundary

| Claim | State | Exact dependency / limitation |
|---|---|---|
| Full Schur germ equals fixed Hilbert germ | PROVED | all thirty special linear syzygies generate the full module; flatness argument §1 |
| Selected subsystem equals full locally | PROVED | computed rank/minor + full invariant unobstructedness, not finite jets alone |
| Integral unique curve matching six-jet | PROVED | minor is a101-unit; normalized coefficients integral; injection into Q[[w]] |
| Smooth generic fibre of finite algebraic family | CONDITIONAL | accepted source smoothness-certificate software boundary |
| A chosen finite-q smooth fibre displayed | OPEN | no root/specialization yet |
| Fresh coefficient recurrence implements equations | PROVED by inspection | not independently executed here |
| Untrusted checkpoint resume is independently certified | OPEN | repairs above requested |

Dependency chain: full special syzygies -> flat Schur chart -> fixed Hilbert
identification; invariant obstruction vanishing + rank/minor -> selected/full
local equality -> integral unique free-coordinate curve -> six-jet agreement
-> inherited smoothness certificate -> smooth generic fibre. None of these
arrows proves full Hilbert-component dimension94 or Picard rank1.

Reviewed file SHA-256 values (later edits require a fresh diff review):

    14b7162301e15cf612238a23c00f7b2469fc8bcc89afe711f3b27b3cad7b5950  scripts/build_fixed_chart.py
    2a9c4dbe267b2beeea1e8f97bc0c17ab35e25e7b9eb7d0f86e5e976d5f1c9b5b  scripts/fixed_curve_lift.py
    74c2059066518c95a5b4f3f46427aa7731ce705062b6d858db12bbc1bd9523fd  data/fixed_chart.json

External-source phase: none was needed for this local review. Standard
local flatness/faithful-completion facts are used as mathematical
dependencies; the supplied proof's integral-syzygy and equivariant-lifting
audits were inspected for their precise scope. Confidence is high in the
local derivation; the concrete specialization and independent execution
remain unfinished.
