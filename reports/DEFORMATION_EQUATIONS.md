# Deformation equations

## Frozen input and conventions

All calculations in this report use only the clean source tree at commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`. The coefficient field is
`QQ`, and

\[
(a,b,c,d,e,f,g,h)=(x_1,x_2,x_3,x_4,x_5,x_6,x_7,x_8).
\]

The sixteen special-fiber generators, in immutable order, are

\[
\begin{aligned}
(f_1,\ldots,f_{16})={}&(abf,abg,abh,acg,ach,adh,bdf,bdg,\\
&beg,cde,ceg,ceh,cfh,def,dfh,efg).
\end{aligned}
\]

Vertex labels `1,...,8` correspond to `a,...,h`. The symmetry generators are

\[
\sigma=(2\ 8)(3\ 7)(4\ 6),\qquad
\tau=(1\ 3)(2\ 5)(4\ 6),
\]

and generate a group of order six, isomorphic to (S_3).

## The 109-dimensional embedded tangent basis

Let

\[
T_{\mathrm{all}}=\operatorname{normalMatrix}(\{0\},F_0),
\qquad F_0=(f_1,\ldots,f_{16}).
\]

Macaulay2 returns a (16\times109) matrix. Its one-based column order is
the embedded tangent basis used throughout the packet. Every column,
recorded as its images of the sixteen ordered generators, is printed in
[`equations/tangent_basis.md`](../equations/tangent_basis.md) and serialized
in [`equations/deformation_data.json`](../equations/deformation_data.json).
This is the actual `normalMatrix` order; no identification with any basis in
another repository is assumed.

The coordinate-action calculation uses the 64 columns
(x_j\partial f_i/\partial x_k). Their image in the normal space has rank
56. Pivot rows select those 56 embedded tangent columns, leaving the
following ordered complement:

```text
1,2,3,4,5,6,7,8,9,10,
18,19,20,21,22,23,24,25,26,27,
35,36,37,38,39,
47,48,49,50,51,
66,67,68,69,70,
92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109
```

Thus (109=56+53). The 53 basis vectors are denoted here by
(e_1,\ldots,e_{53}) in exactly the displayed order; (e_j) is not column
(j) of the 109-basis unless the displayed lookup says so.

## Ten intrinsic (S_3)-orbits and selected vector

The signed-permutation calculation has positive signs and gives these ten
orbits on intrinsic positions (1,\ldots,53):

```text
O1  = {1,11,19,23,27,34}
O2  = {2,15,16,25,30,32}
O3  = {3,14,17,21,29,31}
O4  = {4,13,20,22,26,35}
O5  = {5,12,18,24,28,33}
O6  = {6,7,10}
O7  = {8,9}
O8  = {36,39,43,44,46,53}
O9  = {37,38,42,45,47,51}
O10 = {40,41,48,49,50,52}
```

The final generic-invariant argument assigns coefficient (k) to every
position in (O_k). Its explicit ordered 53-vector is

```text
(1,2,3,4,5,6,6,7,7,6,1,5,4,3,2,2,3,5,1,4,3,4,1,5,2,4,1,
 5,3,2,3,2,5,1,4,8,9,9,8,10,10,9,8,8,9,8,9,10,10,10,9,10,8).
```

## Exact map (y\mapsto T_1y\mapsto(g_1,\ldots,g_{16}))

The extractor sets (T_1=T_{\mathrm{all}}[:,\text{intrinsic}]), forms the
column (y) above, and computes (T_1y) over (mathbb Q). It then calls
`versalDeformation` only to first order to obtain the compatible generator
and relation lift. The resulting generator correction is exactly the
16-entry column (T_1y).

The sixteen polynomials (F_i^{(1)}=f_i+qg_i) are printed verbatim in
[`equations/first_order.md`](../equations/first_order.md), with parallel
exports in:

- [`equations/first_order.tex`](../equations/first_order.tex) — LaTeX;
- [`equations/first_order.m2`](../equations/first_order.m2) — Macaulay2;
- [`equations/deformation_data.json`](../equations/deformation_data.json) — JSON.

The generated Macaulay2 files parse successfully in Macaulay2 1.20.

## Six-jet

Write the stored generator jet as

\[
F_i(q)=\sum_{r=0}^{6}q^r H_{r,i}\pmod {q^7}.
\]

All (7\times16) cubic coefficients are retained in:

- [`equations/deformation_data.json`](../equations/deformation_data.json),
  field `six_jet_coefficients`;
- [`equations/six_jet.tsv`](../equations/six_jet.tsv), a simple tab-separated
  format;
- [`equations/six_jet.m2`](../equations/six_jet.m2), an executable
  Macaulay2 representation.

The independent first-order rerun proves coefficientwise that

\[
(H_{1,1},\ldots,H_{1,16})=(g_1,\ldots,g_{16}).
\]

The source packet also stores the matching first-syzygy jet. This workspace
hash-locks that source file and independently verifies coefficientwise that
the stored generator--relation product vanishes through order \(q^6\). The
machine export focuses on the sixteen requested generators.

## Explicitness boundary

The packet supplies:

1. an explicit first-order embedded deformation;
2. an explicit equivariant generator/first-syzygy six-jet through (q^6);
3. an abstract obstruction-theoretic theorem extending the prescribed
   equivariant finite jet to compatible all orders over
   (mathbb Z_{(101)}[[q]]), hence over (mathbb C[[q]]);
4. an existential Hilbert-scheme curve-selection algebraization;
5. no explicit finite algebraic curve or finite set of sixteen polynomial
   equations for a smooth characteristic-zero fiber.

The all-orders statement is not obtained by extrapolating the six-jet. The
finite q-adic smoothness certificates are stable under any permitted
all-orders continuation of that jet, but they do not make the six-jet itself
a polynomial family.

The packet's proposed exact polynomial-family artifacts are absent, as
checked by `scripts/audit_explicitness.py`. Its quarantined order-four
matrix specializes at (q=1) over (mathbb F_{101}) to affine dimension
zero and degree 567. `scripts/verify_failed_truncation.m2` reproduces this
negative control exactly. It is nonflat and is not a smoothing.

To obtain finite equations for an actual smooth fiber one still needs either:

- effective curve selection on an explicit affine Hilbert chart, followed
  by extraction of the universal sixteen equations; or
- a terminating polynomial/algebraic-power-series lift with an exact
  generator-relation identity.

Any candidate must then pass, exactly: correct reduction at (q=0),
flatness (not merely agreement modulo (q^7)), projective dimension three,
degree 20, and emptiness of the saturated projective singular locus for a
specified nonzero fiber. No evaluation of the present truncation at (q=1)
is admissible.

## Reproduction

```sh
python3 scripts/verify_source.py
python3 scripts/build_outputs.py
M2 --script equations/first_order.m2
M2 --script equations/six_jet.m2
```

The first two commands fail on a changed source commit/tree/status, changed
six-jet hash, dimensions other than 109/56/53, a changed intrinsic order,
an invalid orbit partition, a changed generator order, or any coefficient
mismatch.
