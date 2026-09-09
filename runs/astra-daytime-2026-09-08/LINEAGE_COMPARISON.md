# Exact comparison with the earlier Fable–DGLA lineage

## Scope and source identities

**PROVED (source inspection).** This is a targeted comparison of tangent classes,
jets, and explicitness boundaries. It does not repeat either smoothing audit.
Only the named related repositories and the older geography's source archives
were inspected; all are read-only except this run directory.

| Repository | Inspected commit | Branch |
|---|---|---|
| `grunbaum-zero-context-proof` | `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b` | frozen source |
| `sr-project` | `ff2afbbb7a8b18e7c054d16292df8db02ca87f5c` | `restructure` |
| `grunbaum-cy-geography-fable-dgla` | `3f7ef3da88fe963e10001fc66cbff4153d5fcb27` | `main` |
| `grunbaum-cy-geography-zero-context` | `4f75a9ae930a5cb645e06b4b8da79fa7b78a394a` | working geography |

**COMPUTER-CERTIFIED.** The new comparison is in
`scripts/compare_lineage_tangents.py` and
`certificates/lineage_tangent_comparison.json`. It uses only Python's standard
library and exact rational arithmetic. Its decisive computation took 3–9
seconds on this Mac; no CAS process was run. The source basis exports are
hash-identified inside the JSON certificate.

## The two vectors, with actual bases

**PROVED (identified inputs).** In zero-context coordinates put

```
(f1,...,f16)=(abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg).
```

Let `b1,...,b109` be the exact `normalMatrix({0},F0)` columns, whose polynomial
images are printed in `../../equations/tangent_basis.md`. The intrinsic basis
`e1,...,e53` consists of columns

```
1,2,3,4,5,6,7,8,9,10,18,19,20,21,22,23,24,25,26,27,
35,36,37,38,39,47,48,49,50,51,66,67,68,69,70,
92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109.
```

The zero-context direction is

```
z=(1,2,3,4,5,6,6,7,7,6,1,5,4,3,2,2,3,5,1,4,3,4,1,5,2,4,1,
   5,3,2,3,2,5,1,4,8,9,9,8,10,10,9,8,8,9,8,9,10,10,10,9,10,8).
```

**PROVED (identified inputs).** The old proof uses the ordered generators

```
(m1,...,m16)=(678,468,378,357,348,278,257,256,
              247,246,146,145,138,136,135,125),
```

where `ijk` means `x_i*x_j*x_k`, and the 53 ordered columns of
`CT^1(0,gens ideal(m1,...,m16))` over `QQ` in VersalDeformations 3.0. Its full
16-by-53 polynomial basis is frozen in the older geography's
`equations/fable_T1_basis_QQ.txt`. In that basis, the vector from
`PROOF_DGLA.pdf`, printed/PDF page 8, equation (4.1), is

```
y=(1,3,1,2,6,1,1,1,1,1,21,28,1,5,10,55,66,15,1,18,2,
   35,42,1,4,10,1,25,12,30,5,33,44,1,6,3,14,7,1,9,1,6,
   12,20,1,4,22,1,15,1,1,8,11).
```

The old `rl` basis is a third basis. The old geography's
`equations/fable_to_rl_change_matrix_mod32003.txt` transports to it over
`GF(32003)`; it must not be mistaken for the characteristic-zero transport
constructed here. The older proof also records an independent historical
rational-complement permutation in
`sr-project/proofs/all-ones-versal-arc/certificates/t1_transport_QQ.txt`.

## A verified coordinate identification and complete basis transport

**COMPUTER-CERTIFIED.** One identification of special fibres is

\[
(x_1,x_2,x_3,x_4,x_5,x_6,x_7,x_8)_{old}=(b,e,a,d,g,f,c,h)_{zero}.
\]

It sends old generator indices to new ones by

```
(13,15,5,4,6,12,11,16,10,14,7,8,3,1,2,9).
```

Under this identification, old basis column `j` represents exactly `e[p_j]`
modulo coordinate derivations, where

```
p=(26,29,28,27,30,6,8,10,9,7,13,11,12,14,15,32,31,34,33,35,
   22,25,21,24,23,16,18,19,17,20,2,4,1,5,3,50,49,46,47,44,
   45,48,52,41,38,39,40,37,36,51,42,53,43).
```

Thus the old tangent in the zero-context basis is

```
v=(44,5,6,33,1,1,1,1,1,1,28,1,21,5,10,10,12,1,25,30,
   42,2,4,1,35,1,2,1,3,6,66,55,1,15,18,15,1,1,4,22,20,
   1,11,9,1,7,1,6,14,3,1,12,8).
```

**PROVED from the displayed data.** `v` is not `z`, even up to a nonzero
scalar: for example `v6=v7=1`, whereas `z6=z7=6`, but `v1=44` and `z1=1`.
This is a difference in intrinsic classes, so an infinitesimal projective
coordinate change cannot repair it.

**COMPUTER-CERTIFIED.** Enumerating all `8!` vertex permutations produces
exactly six identifications of the two nonface sets:

```
(2,5,1,4,7,6,3,8)   (2,8,7,6,1,4,3,5)
(5,2,3,6,7,4,1,8)   (5,8,7,4,3,6,1,2)
(8,2,3,4,1,6,7,5)   (8,5,1,6,3,4,7,2).
```

None makes the intrinsic tangents proportional. The certificate includes
all six transported vectors and all six full sparse change-of-basis matrices.

## A short invariant excludes diagonal rescalings as well

**PROVED.** For a diagonal coordinate change the intrinsic representatives
are weight vectors. In particular

\[
e_1:f_1\mapsto ace,\quad e_3:f_1\mapsto c^2e,\quad
e_6:f_4\mapsto adf,\quad e_7:f_4\mapsto cdf.
\]

Their weights are the image monomial divided by the source monomial, and
`weight(e1)+weight(e7)=weight(e3)+weight(e6)`. Consequently

\[
R(t)=\frac{t_1t_7}{t_3t_6}
\]

is unchanged by diagonal projective rescalings and by simultaneous nonzero
rescaling of the tangent parameter. Here `t_i` denotes intrinsic position,
not a global normal-matrix column. We have `R(z)=1/3`.

**COMPUTER-CERTIFIED.** In the displayed order of the six vertex
identifications, the old vector has

\[
R(v)=22/3,\quad25/12,\quad2/21,\quad2/3,\quad5/22,\quad28/5.
\]

None equals `1/3`. These small rational inequalities are a human-checkable
certificate that no diagonal rescaling, vertex relabelling, infinitesimal
coordinate action, or invertible parameter change identifies the directions.

**PROVED, with the combinatorial input COMPUTER-CERTIFIED.** Every projective
automorphism preserving `X_M` is monomial. It permutes the twenty irreducible
coordinate `P^3` components, hence their zero-dimensional nonempty
intersections. Those intersections are precisely the eight coordinate
vertices: the script verifies that, for each vertex, the intersection of all
facets containing it is that singleton. Thus the automorphism permutes the
eight coordinate points, so its matrix is diagonal times a permutation.
The preceding obstruction therefore covers every projective identification
of the special fibres, not merely a selected list of coordinate changes.

**FAILED (precise attempted identification).** The zero-context and old
Fable tangent directions cannot be identified by a projective isomorphism of
their special fibres, an invertible reparametrization, and first-order
coordinate/generator gauge. A generator-basis change contributes zero to
`Hom(I,S/I)` and a syzygy-basis change does not alter the deformation class.
This failure does not imply that their eventual smooth fibres have different
Hodge numbers, lie on different Hilbert components, or cannot be isomorphic.

## They do lie on the same top quadratic component

**PROVED (explicit test).** Write `u_j` for global embedded normal-matrix
column `j`. The three top rank-one matrices, in consistent orders, are

\[
A=\begin{pmatrix}u_1&u_4&u_{66}&u_{67}&u_{96}&u_{99}\\
u_{18}&u_{20}&u_{35}&u_{39}&u_{105}&u_{102}\end{pmatrix},
\]
\[
B=\begin{pmatrix}u_{21}&u_{22}&u_{26}&u_{27}&u_{97}&u_{92}\\
u_{50}&u_{51}&u_{69}&u_{70}&u_{108}&u_{100}\end{pmatrix},\qquad
C=\begin{pmatrix}u_2&u_3&u_{47}&u_{48}&u_{106}&u_{95}\\
u_{23}&u_{24}&u_{36}&u_{37}&u_{104}&u_{109}\end{pmatrix}.
\]

**COMPUTER-CERTIFIED.** Every one of the 45 minors vanishes on `z` and on
each transported old vector; every block entry is nonzero. Thus both
directions are in the open coordinate torus of `P1^3`. On this torus five
of the nine block equations solve all second-row entries as one common
multiple of the first row, so the torus belongs exclusively to the rank-one
component. This verifies the common quadratic component, not just its
ambient quadratic equations.

The script also checks that all 27 quadrics read directly from the frozen
`gs_quadratic_base.m2` lie in the rational linear span of these 45 displayed
minors, and that the frozen first-order generator corrections equal the
intrinsic-basis linear combination defined by `z`.

**OPEN.** Belonging to the same quadratic component does not identify a
minimal prime of the completed Hilbert local ring. Higher equations may cut
or split branches with the same tangent cone. A sufficient stronger result
would be an explicit irreducible algebraic Hilbert chart component through
both constructed families, or a proof that the relevant strict transform of
the completed Hilbert germ is irreducible along a connected open subset
containing both lifted points. Merely finding a 94-dimensional component
with this tangent cone does not prove that both unspecified all-orders
extensions factor through it.

## Reproducible comparison algorithm and stronger jet tests

**PROVED (algorithm and criterion).** Use the 104 standard cubic monomials
of `S/I_M` as a basis. Then each map from 16 generators to `(S/I_M)_3`
becomes a vector in `QQ^1664`. Form the 64 coordinate-derivative columns
`x_j partial(f_i)/partial(x_k)` and select a basis `D` of their rank-56
span. Let `E` be the 53 frozen intrinsic columns. Transport the old cubics
and their generator order and solve exactly

\[
T_{old}=D A+E B.
\]

Reconstruct each ambient column to verify this identity, and verify
`rank[D E]=109` and `rank B=53`. This is the algorithm executed by the
script. For any vectors `y,z`, equality modulo orbit is exactly
`rank[D,T_old y-Ez]=rank D`; equality up to invertible parameter change
allows an additional scalar `c != 0` multiplying one tangent.

**PROVED (jet criterion).** To identify generator rows through order `q^6`,
one must exhibit an invertible parameter series
`s(q)=c1*q+...+c6*q^6`, `c1!=0`, a matrix `G(q)` in `GL8(QQ[q]/q^7)`,
and an invertible `16x16` generator matrix `U(q)` such that

\[
F_{zero}(q,x)=F_{old}(s(q),G(q)x)\,U(q)\pmod{q^7}.
\]

Here `U(0)` implements the special generator correspondence. For first
syzygies, exhibit an invertible `30x30` matrix `V(q)` with

\[
Q_{zero}(q)=U(q)^{-1}Q_{old}(s(q),G(q)x)V(q)\pmod{q^7},
\]

or verify equality of the generated relation modules when the chosen
representatives require an additional relation gauge. Verify all identities
coefficientwise and determinant units, rather than comparing printed
polynomial strings. This stronger test already fails at order one for the
two directions above. The old proof in any event does not supply a fixed
six-jet for its final formal family.

## What the earlier finite polynomials actually define

**PROVED (source inspection).** Old `PROOF_DGLA.pdf`, Theorem 1.1, page 2;
equation (4.1), page 8; Lemma 6.2, page 12; Remark 6.4 and Lemma 7.1,
page 13, have the following exact scope:

- The printed two-jet is over `QQ[s]/(s^3)`.
- A package-selected three-jet is over `QQ[s]/(s^4)`.
- The all-orders induction may change the coefficient of `s^3` at its
  first step. It preserves only the two-jet.
- The equations called “honest polynomials” in Lemma 7.1 are polynomials
  in the eight projective coordinates, with unspecified coefficients in
  `QQ[[s]]`. They are not finite polynomials in `s` over `QQ`.
- They define a projective scheme over `Spec QQ[[s]]`, not an explicitly
  specified finite-type algebraic family over a rational affine curve.

**FAILED.** Reading the title “The algebraic family over `QQ[[s]]`” as a
certificate of finite equations for a rational `s=1` smooth fibre is invalid.
No map from `QQ[s]/(s^n)` to `QQ` sends `s` to 1. For a general formal
power series, evaluation at 1 is also undefined.

**PROVED (source inspection).** The older `rl` exact colon test in
`sr_environment.sage:1225` operates on a selected *finite-field polynomial
reinterpretation* of a three-jet. It tests `(J:t)=J` for that candidate. It
does not identify the Fable all-orders family. The older geography explicitly
records changes of basis and different higher-order choices. No finite
smooth characteristic-zero equations transferable to zero-context were found.

## Sergey records, rendering, and limitations

**OPEN (source unavailable in searched scope).** No Sergey-attributed
`REPORT.md` or `notes.md` was found in the named proof/geography directories,
the relevant `heap-project` filename search, or the three older geography
archives' member lists. No such document has been used or assigned a lineage.
The available `no-Linfty-audits/*/AUDIT_REPORT.md` files name the Fable–DGLA
proof and are model audits, not evidence of Sergey's authorship.

**COMPUTER-CERTIFIED (provenance).** SHA-256 of the inspected old PDF is
`cb341f2c340c8688aabd46d8bb947c56e89692836862dd56f03625943ed4e9dd`;
its TeX source is
`90b96427faf5620c08860e68d0f759b28add840bc816d2b479a8410e3b98c7cb`.
The old frozen two-jet hash is
`40e64e61674b6a4e61f1ea6822dc79327bf4ba397285f84ed8738c4c18cd1795`.
PDF pages 8 and 13 were extracted, rendered using the supplied CoreGraphics C
script, and visually checked against the TeX statements. Images are in
`artifacts/pdf-pages/`.

**FAILED, then repaired.** `pdftotext`/`pdftoppm` were unavailable; a Swift
renderer attempted unavailable module-cache output and was stopped. A small
CoreGraphics C renderer succeeded. An initial handwritten placement of two
entries in each of the B/C rank-one matrices produced inconsistent tests;
checking against `gs_quadratic_base.m2` corrected the placement before the
final certificate was generated. No mathematical conclusion relies on that
discarded test. No heavy computation or CAS ran for this comparison.

## Claim ledger and dependencies

| ID | Normalized claim | State | Evidence / consequence |
|---|---|---|---|
| D1 | The two special ideals agree after the displayed permutation | **COMPUTER-CERTIFIED** | Exact monomial-set comparison; permits D2 and the transported link |
| D2 | The old basis transports by the displayed positive permutation modulo orbit | **COMPUTER-CERTIFIED** | 109-dimensional sparse rational reconstruction; permits D3/D4 |
| D3 | No projective special-fibre isomorphism and invertible base change identify the tangents | **PROVED** from exact certificate | Torus invariant and component-intersection argument; blocks any six-jet identification |
| D4 | Both tangent directions lie on the same unique top quadratic component | **COMPUTER-CERTIFIED** | All 45 minors vanish and all entries are nonzero |
| D5 | The old proof supplies finite rational smooth-fibre equations | **FAILED** | Lemma 7.1 has formal coefficient ring; no transferable equations |
| D6 | The two smoothings lie on the same completed Hilbert component | **OPEN** | D4 alone does not establish this |

Evidence is exact computation, direct mathematical derivation, source text,
and checked PDF rendering. Confidence is high within these stated boundaries;
qualified-human verification is not claimed. No broad proof-audit conclusion
is drawn.
