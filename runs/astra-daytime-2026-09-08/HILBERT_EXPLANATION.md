# The Hilbert-scheme picture

This is a targeted verification for the Friday discussion, not a new audit of
the smoothing theorem. **COMPUTER-CERTIFIED** below includes inherited exact
computations accepted within the frozen proof/audit's stated software trust
boundary. **PROVED** denotes the mathematical deductions recorded here;
qualified human verification is not claimed.

## Blackboard explanation

**COMPUTER-CERTIFIED.** At the Stanley–Reisner point the Hilbert tangent space
is
\[
T_{[X_M]}\operatorname{Hilb}^{P}(\mathbf P^7)
 =\operatorname{Hom}_S(I_M,S/I_M)_0,\qquad \dim=109.
\]
The infinitesimal change-of-projective-coordinates subspace has dimension 56.
Indeed \(\dim PGL_8=63\), and the special monomial scheme has a
seven-dimensional diagonal stabilizer. The exact rank computation shows
there are no further infinitesimal stabilizer directions. Thus
\[
109=56+53.
\]
The 53 is the dimension of an intrinsic tangent quotient, with a chosen
linear complement; it is not a dimension of a smooth moduli space.

**COMPUTER-CERTIFIED + PROVED.** The 27 quadratic obstruction equations
involve 36 of these 53 coordinates. Their ideal is the sum of three ideals
in disjoint sets of 12 coordinates. A block has three irreducible components,
of dimensions 7, 6, 6. The unique largest component \(P_1\) is the locus
of rank at most one in a \(2\times6\) matrix. Writing a nonzero matrix as
\(u v^t\) gives \(2+6\) parameters and one scalar redundancy, hence
\(\dim P_1=7\). There are 17 quadratically unrestricted coordinates, so
\[
\boxed{38=17+3\cdot7},\qquad \boxed{94=56+38}.
\]
More precisely, if \(A\) is the completed local Hilbert ring, its associated
graded ideal contains those quadrics. Consequently
\[
\dim A=\dim\operatorname{gr}_{\mathfrak m}A
 \le (109-36)+3\cdot7=94.
\]
This is an upper bound for every Hilbert component through this point.

**PROVED, using the smooth Calabi–Yau deformation theorem.** At a smooth
fibre \(X\), the stabilizer has zero tangent space, and the normal and Euler
sequences give
\[
h^0(N_{X/\mathbf P^7})=63+h^{2,1}(X).
\]
Bogomolov–Tian–Todorov, the vanishings \(H^1(\mathcal O_X)=
H^2(\mathcal O_X)=0\), and openness of very ampleness make this Hilbert
germ smooth of that dimension. Therefore any such smoothing through
\(X_M\) has \(h^{2,1}\le31\). See `PICARD_HODGE_PLAN.md` for every
vanishing. The dimension 38 at the singular point does not predict
\(h^{2,1}=38\): the projective orbit grows from 56 to 63 on a smooth fibre.

**OPEN.** The 38-dimensional quadratic component is not yet established as
an actual miniversal component. **CONDITIONAL.** If a corresponding
94-dimensional Hilbert component has a smooth Calabi–Yau member, then its
smooth locus has dimension 94 and necessarily
\(h^{2,1}=94-63=31\). A single smoothing curve does not prove this component
dimension.

**PROVED, primary-literature input.** The generic degree-20 threefold
defined by \(3\times3\) minors of a \(4\times4\) matrix of linear forms in
\(\mathbf P^7\) has Hodge pair \((2,34)\): Kapustka–Kapustka,
*A cascade of determinantal Calabi–Yau threefolds*, Theorem 3.8 and
Proposition 3.10 ([arXiv:0802.3669v3](https://arxiv.org/pdf/0802.3669)). Its
smooth Hilbert germ therefore has dimension \(97=63+34\). Its Hilbert
component cannot contain \([X_M]\), because that would give local dimension
at least 97 there, contradicting 94. This exclusion requires the verified
quadrics to be genuine embedded Kuranishi initial equations and compares
the same Hilbert polynomial and embedding in \(\mathbf P^7\). The audited
zero-context calculation supplies this input. A matching Betti table alone
does not identify a family.

## Which quadratic component contains the proof direction?

**PROVED, with a new cheap exact check.** It is definitely the unique top
component \(P_1^3\); in fact the whole \(S_3\)-fixed intrinsic ten-plane
lies in it. This does not identify a completed Hilbert component.

Use the one-based 53 intrinsic positions from
`deformation/build_equivariant_sixjet.m2`, not the full 109-column indices.
The positions correspond to the ordered global columns
\[
(1,\ldots,10;18,\ldots,27;35,\ldots,39;47,\ldots,51;
66,\ldots,70;92,\ldots,109).
\]
Explicit rank-one matrices for the three blocks are
\[
M_A=\begin{pmatrix}t_1&t_4&t_{43}&t_{40}&t_{31}&t_{32}\\
t_{11}&t_{13}&t_{46}&t_{49}&t_{21}&t_{25}\end{pmatrix},
\]
\[
M_B=\begin{pmatrix}t_{19}&t_{20}&t_{36}&t_{41}&t_{14}&t_{15}\\
t_{34}&t_{35}&t_{44}&t_{52}&t_{29}&t_{30}\end{pmatrix},\quad
M_C=\begin{pmatrix}t_{26}&t_{27}&t_{50}&t_{39}&t_2&t_3\\
t_{22}&t_{23}&t_{48}&t_{53}&t_{16}&t_{17}\end{pmatrix}.
\]
Every vertically paired pair of positions lies in the same invariant orbit.
Thus each matrix has identical rows on the fixed ten-plane, so all 45 minors
vanish identically there. For the proof tangent with orbit coefficients
\((1,2,\ldots,10)\), the rows are
\[
M_A=M_B=\begin{pmatrix}1&4&8&10&3&2\\1&4&8&10&3&2\end{pmatrix},\quad
M_C=\begin{pmatrix}4&1&10&8&2&3\\4&1&10&8&2&3\end{pmatrix}.
\]

**PROVED.** This direction lies on no other quadratic component. Here is a
human-checkable reason stronger than merely counting minors. On the torus
where all block entries are invertible, five of the nine A-block equations
give
\[
\frac{t_{11}}{t_1}=\frac{t_{13}}{t_4}
=\frac{t_{46}}{t_{43}}=\frac{t_{49}}{t_{40}}
=\frac{t_{21}}{t_{31}}=\frac{t_{25}}{t_{32}}.
\]
These follow from equations 1, 2, 3, 8, 9 of KA in
`reconstruct/p1_quartic_component.m2`; the remaining equations follow from
the ratios. The other blocks have the same argument after relabeling.
Therefore the localized quadratic scheme itself is the smooth rank-one
prime. All entries at the proof direction are nonzero. In particular its
quadratic branch is unambiguous even though the full completed branch is
unknown.

**PROVED distinction.** The sparse all-ones-on-38-positions direction has
invariant orbit coefficients
\((1,1,1,1,0,0,1,1,0,1)\), whereas the proof uses \((1,\ldots,10)\).
They belong to the same top quadratic component but are distinct tangents.
The determinant-one 15-coordinate implicit-function minor was checked at
the sparse direction. Its numerical value is not automatically one at the
proof direction. The stored nonaveraged sparse two-jet fails invariance at
the five nonidentity group elements; see
`reconstruct/audit_p1_twojet_equivariance_output.txt`. It must not be
substituted for the proof's generic equivariant six-jet.

## What would turn the quadratic branch into a Hilbert component?

**PROVED, new useful distinction.** The fixed embedded Hilbert germ has a
different dimension: 21. The vertex permutation representation is
\(3\mathbf1\oplus\mathrm{sign}\oplus2\mathrm{std}\), so its centralizer
in \(PGL_8\) has dimension \(3^2+1^2+2^2-1=13\). The invariant part of
the special diagonal stabilizer has dimension \(3-1=2\), giving 11
invariant coordinate-orbit directions. Taking invariants is exact in
characteristic zero, hence the fixed embedded tangent has dimension
\(11+10=21\). The source's complete obstruction calculation
\((T^2)^{S_3}=0\) makes the fixed embedded deformation germ formally smooth.
The present run's separate chart computation confirms 291 invariant cubic
coefficients, linearization rank 270, and a dependent-coordinate minor of
determinant -1; see `data/fixed_chart.json` and the main explicitness report.
This supports an explicit fixed-family route without establishing dimension
38 for the full intrinsic germ.

**PROVED, conditional on the accepted equivariant smoothing theorem.** This
smooth fixed formal germ is irreducible and lies on exactly one completed
Hilbert component: it contains the certified equivariant smoothing arc, whose
generic Hilbert point is smooth and therefore lies on only one component.
Algebraically, if two ambient minimal primes were contained in the kernel
of the fixed-germ quotient, both would be contained in the prime of that
generic arc, contradicting regularity there. Consequently smooth fibres
constructed on this same localized fixed algebraic germ belong to the
zero-context smoothing component and have its Hodge numbers. This is a
component argument, not equality of arcs or six-jets. It requires the actual
fixed germ through the origin, not an arbitrary component of a polynomial
incidence scheme away from that germ. The nonaveraged sparse line does not
meet its invariance hypothesis.

**COMPUTER-CERTIFIED.** All degree-at-most-four Kuranishi equations vanish
on \(P_1^3\), and the source provides a determinant-one 15-by-15 Jacobian
minor at the sparse point. These are statements about a finite truncation.

**OPEN.** A sufficient next result is a compatible all-orders family over
the 38-dimensional rank-one base whose map into the intrinsic formal
deformation base has dimension 38, together with a smooth-fibre certificate.
For example, in a verified Kuranishi coordinate system, proving that every
full Kuranishi equation lies in \(P_1^3\) gives a 38-dimensional formal
subscheme; the upper bound forces its prime to be a component. A component
of the tangent cone need not itself be an actual branch, and distinct
completed branches can have the same quadratic component.

**PROVED limitation.** After the usual blow-up substitution \(t=qv+\cdots\),
the 15 independent equations solve 15 coordinates formally near the
specified leading point. The other 12 equations may still impose higher
relations on the 38 free coordinates. Proving that these residual
relations vanish is the missing component statement. Producing one curve
on their zero locus is enough for explicit smoothing equations, but not
for dimension 94. For the latter, a full parameter family or another lower
dimension certificate is required. If the new family does not reproduce
the certified six-jet, its generic smoothness needs its own argument.

The quadratic component counts are **COMPUTER-CERTIFIED + PROVED** from
the block decomposition:

| Top rank-one factors | Number of quadratic components | Intrinsic dimension | With 56 orbit directions |
|---:|---:|---:|---:|
| 3 | 1 | 38 | 94 |
| 2 | 6 | 37 | 93 |
| 1 | 12 | 36 | 92 |
| 0 | 8 | 35 | 91 |

**OPEN.** The other 26 components cannot be excluded from smoothing merely
because their leading vertex Jacobians have smaller rank. Higher-order
coefficients can restore generic rank; \(\operatorname{diag}(q,q,q^2,q^3)\)
is the elementary model of that phenomenon.

## Connectedness and what it permits

**PROVED, primary-theorem input.** Hartshorne's *Connectedness of the Hilbert
scheme*, Publ. Math. IHÉS 29 (1966), Corollary 5.9 (printed paper p.48,
journal p.304; PDF page45 including its cover), states the connectedness
of \(\operatorname{Hilb}^{P}(\mathbf P^r_S/S)\) when \(S\) is a connected
noetherian scheme; it also gives the geometrically connected and linearly
connected variants. Theorem 5.8 is the preceding functor statement. Thus
for \(S=\operatorname{Spec}\mathbf C\), fixed \(r=7\), and the fixed
polynomial here, the Hilbert scheme is nonempty and connected.
([Primary paper](https://www.numdam.org/article/PMIHES_1966__29__5_0.pdf))

**PROVED.** Connectedness permits a finite chain of irreducible components
\(C_0,\ldots,C_r\) with consecutive nonempty intersections. It does not
imply that a single component contains two chosen points. An integral
parameter curve has irreducible image closure, so a family over an integral
curve cannot have its general fibres successively in two different
components. The precise replacement for "jumping" is to specialize within
one component to a point in an intersection and then deform within another,
or to use a connected reducible base. Hartshorne's theorem allows singular,
reducible, and nonreduced intermediate subschemes and does not assert
connectedness of the smooth Calabi–Yau locus, the aG locus, or a fixed
Betti-table locus. It therefore gives no shortcut around the 94-versus-97
exclusion and no explicit transition between the two smooth families. A
point common to two different Hilbert components cannot itself be a smooth
Calabi–Yau threefold of the stated type, since its Hilbert germ would then
be smooth and irreducible. Any such component chain must leave that smooth
Calabi–Yau locus.

## Source and claim ledger

**PROVED provenance.** Source HEADs read on 2026-09-08:

| Repository | Exact HEAD |
|---|---|
| zero-context proof, frozen input | `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b` |
| independent audit | `9310cd9e3316c69f129d5588d65f0b91f37365b7` |
| geography, before this run | `4f75a9ae930a5cb645e06b4b8da79fa7b78a394a` |

Internal discovery was frozen in `HILBERT_DISCOVERY_FREEZE.md` before the
external source phase. No CAS was run for this task. The only exact check
was the subsecond integer/orbit script `scripts/check_hilbert_tangent.py`.
Its input SHA-256 values and output are in `HILBERT_CHEAP_CHECK.txt`.

| ID | Atomic conclusion | State / evidence | Downstream use |
|---|---|---|---|
| HC1 | 109 tangent directions; orbit rank 56 | COMPUTER-CERTIFIED, source/audit exact ranks; not rerun | 53 intrinsic directions |
| HC2 | three quadratic blocks, each dimensions 7/6/6 | COMPUTER-CERTIFIED, KURANISHI_AUDIT and quartic script | 38 and 94 |
| HC3 | generic proof tangent lies only in top quadratic component | PROVED + COMPUTER-CERTIFIED, explicit matrices, ratio proof, integer script | prioritizes P1; no full component identification |
| HC4 | local Hilbert dimension at most 94 | PROVED given certified initial equations | h21 bound; determinantal exclusion |
| HC5 | actual 94-dimensional smoothing component exists | OPEN | would give h21=31 |
| HC6 | generic determinantal pair (2,34) | PROVED in cited primary results, inspected | 97-dimensional smooth Hilbert germ |
| HC7 | fixed-polynomial Hilbert scheme connected | PROVED in cited primary theorem, inspected | component-chain statement only |
| HC8 | fixed embedded formal germ smooth of dimension21; unique containing completed Hilbert component meeting the certified arc | PROVED from equivariant obstruction vanishing, representation calculation, and the accepted smoothing; chart tangent independently COMPUTER-CERTIFIED in this run | transfers Hodge data between smooth fibres on that fixed germ; does not prove dimension94 |

The dependency chain is HC1+HC2 -> HC4 -> h21<=31; HC4+HC6 ->
determinantal exclusion. HC3 does not imply HC5. HC7 does not imply HC5 or
any connection inside the smooth locus. All source proof states used here
are accepted within the audit boundary; the missing HC5 has proof state
`incomplete` and claim state `unresolved`, not `false`.

External source inspection (2026-09-08):

| Reference | State | Exact inspected location / scope |
|---|---|---|
| Kapustka–Kapustka, arXiv:0802.3669v3 | inspected-primary | Theorem 3.8 (PDF p.8) gives Picard rank 2; Proposition 3.10 (pp.10–11) gives h12=34 for generic 4-by-4 submaximal-minor threefolds; relevant proofs read, not re-audited |
| CGKK, arXiv:1609.01195v1 | inspected-primary | Table 1 no.11 (PDF p.3), §4.9 (p.12), Problem 3.1 (p.3): degree20, pair (2,34), determinantal equations; classification in degrees18–20 posed as a problem |
| Hartshorne (1966) | inspected-primary | Theorem 5.8 and Corollary 5.9 (PDF pp.44–45), including assumptions and variants; chapter argument not re-audited |
| Bertin, arXiv:math/0701511v1 | inspected-primary | §4.1.5 and Remark7, PDF pp.18–19; p.19 also rendered and visually checked; construction source only, not support for the pair (2,34) |

**FAILED citation route.** The inspected Bertin preprint text claims
\(\rho=1\), \(h^{1,2}=33\) for this degree-20 construction, unlike the
later primary Kapustka–Kapustka results. It therefore cannot support the
\((2,34)\) attribution. This report uses Theorem3.8/Proposition3.10 of the
latter paper, not the earlier preprint's Hodge claim. The rendered page also
prints 16/3 for the linear Hilbert-polynomial coefficient while stating
c2.H=56; neither that transcription nor that numerical line is used here.
The render is `artifacts/reference-pages/bertin-0701511-page19.png` (SHA-256
`36fca1dd61306ca89b40fa4991279f4347b9f2b9e19ec1aec4e6d1f73024836f`).
The downloaded 273KB source remains separately in
`/private/tmp/astra-daytime-hilbert-bertin-0701511.pdf` (SHA-256
`f76f8d5e8715d2b6db4c585fac338d829518097a6a16a59407be38cb652d6ca6`).
The default Python had no PDF renderer; built-in macOS PDFKit via the
provided Swift script produced the image. Its first invocation built a
Swift standard-library cache under `/private/tmp`; the process completed.
No package was installed. This report does not attempt a paper-wide Bertin
audit. The CGKK table itself explicitly leaves degree20
classification open, so it must not be presented as a completeness theorem.

Confidence is high for the internal component-location derivation and for
the cited numerical/theorem statements; exact Hodge equality for the
zero-context smoothing remains open. There is no second-engine replay or
qualified-human verification in this daytime subtask.
