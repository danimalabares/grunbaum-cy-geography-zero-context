# Persistence of the fifteen lines on the intended component

**PROVED, conditional only on the audited fifteen-line theorem:** a nonempty
Zariski open subset of the intended complex Hilbert component parametrizes
smooth threefolds containing at least fifteen distinct isolated reduced
lines with normal bundle O_P1(−1)⊕O_P1(−1). The open subset contains the
selected fibre after choosing an embedding of its coefficient field into C.
Because the intended component is irreducible, this is a statement about
a general member of that component. It is not a statement about every
member, the total number of lines, or the dimension of the entire line
scheme.

The input is `notes/degeneration_lines.md`, independently checked in
`notes/line_independent_review.md`, with the executed certificate
`data/line_certificates_all/line_certificates.json`. No new arithmetic,
CAS calculation, or literature search is needed for this deformation
argument. It is mathematical analysis, not qualified-human verification.

Let C be the intended Hilbert component over C and x its selected smooth
threefold point. Shrink to an open U⊂C containing x on which the universal
projective family X_U→U is smooth. This is possible because the universal
family is flat and projective: the closed nonsmooth locus has closed image,
and that image omits x. Let F→U be the relative scheme of lines, a closed
subscheme of Gr(2,8)×U, and let ℓ1,…,ℓ15 be the constructed geometric
points above x.

For each ℓi⊂X_x, the embedded relative deformation problem has tangent
space H0(N_ℓi/X_x) and obstruction space H1(N_ℓi/X_x). These statements can
be seen directly by locally lifting the regular immersion through a
square-zero extension: differences of local lifts are sections of N
tensored with the square-zero ideal, and their gluing obstruction is the
corresponding H1 class. Here both groups vanish because

    N_ℓi/X_x = O(−1)⊕O(−1).

Consequently a base deformation of X has a unique embedded deformation of
the line locally on the Artinian base. Thus F→U is formally étale at ℓi.
Since the relative Hilbert scheme is locally of finite presentation, its
projection is étale in a neighborhood of ℓi. This argument does not assume
that U itself is smooth or use Hilbert smoothness to prove itself.

Consider the ordered distinct-line incidence

    P = (F ×_U ··· ×_U F) \ ⋃_(i<j) {ℓi=ℓj},
                     fifteen factors.

The removed diagonals are closed because the Grassmannian is separated.
The selected tuple p=(ℓ1,…,ℓ15) lies in P. By the preceding étaleness and
stability of étale morphisms under products and restriction, there is an
open neighborhood V⊂P of p such that V→U is étale.

We may also require every line represented by V to have normal bundle
O(−1)⊕O(−1). Indeed, along the universal line the relative normal bundle
is a rank-two vector bundle near each selected point. Its degree is locally
constant and is −2 there, and upper semicontinuity makes H0(N)=H1(N)=0
an open condition. After shrinking V, every geometric normal bundle has
degree −2 and no sections; splitting on P¹ forces O(−1)⊕O(−1). Equivalently,
one can use the smooth Calabi–Yau family and adjunction for the degree.

An étale morphism is open. Therefore

    W = image(V→U)

is a nonempty Zariski open subset containing x. Every geometric point of W
has a preimage after extending its residue field to an algebraic closure,
and hence has an ordered tuple of fifteen distinct lines. At each such
line the relative line scheme is étale over U, so its fibre local ring is
reduced and zero-dimensional. Each line is therefore isolated and reduced
in the full fibre line scheme, even if other components of that scheme
have positive dimension.

The ordered-incidence construction is essential to the precise statement:
one need not find fifteen pairwise disjoint Zariski neighborhoods inside
F, and no assertion of fifteen globally labeled sections over W is made.
The ordered lines do exist after the étale base change V→W. Collisions and
failure of isolation outside W, as well as additional lines anywhere,
remain possible.
