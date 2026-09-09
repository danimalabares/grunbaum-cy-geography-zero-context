# Twelve first-order products certify the missing degree-eight rank

8 September 2026. **COMPUTER-CERTIFIED, with the small integer certificate
displayed below:** every formal generator lift with the specified zero-context
first-order term satisfies

\[
\dim_{\mathbf Q((q))}(I(q)^2)_8\ge 1841.
\]

**PROVED from this certificate:** the conclusion is over characteristic zero,
not merely over a finite field. It is independent of every unknown coefficient
of order two and higher. The finite field of 101 elements was used only to
locate a useful minor; the displayed minor and its determinant are integers.

The Picard/Hodge implication is a separate mathematical argument in
`DEGREE8_PICARD_FORMULA.md`, independently reviewed in
`DEGREE8_FORMULA_INDEPENDENT_REVIEW.md`. This document supplies its rank input;
it does not obtain a finite smooth fibre by truncating a formal series.

## 1. Exact input and normalization

**PROVED (identified input).** Work in the variables `(a,b,c,d,e,f,g,h)` and
the ordered generators

```
(f1,...,f16)=(abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg).
```

The calculation uses `Fi(q)=fi+q*gi+O(q^2)`, with the **plus** sign. The
polynomials `gi` are exactly the `first_order_corrections` in
`../../equations/deformation_data.json`; the same list occurs as coefficient
one of its stored six-jet. They come from frozen zero-context source commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`, not the older DGLA lineage.
The input JSON SHA256 is
`8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f`.

For complete reproducibility, here are the first-order polynomials. The
displayed minor itself uses only indices 1,2,3,4,5,7,8,9,11,12.

```
g1  = 10a^2c+ace+2bce+3c^2e+4ce^2+5cef+9ef^2+8f^2h
g2  = 8ade+8fgh
g3  = 8b^2d+9bde+9efh+8fh^2
g4  = 6adf+6cdf+7d^2f+7df^2+6dfg
g5  = 8bcd+8aef
g6  = 8bd^2+9d^2e+10a^2g+aeg+5deg+4e^2g+3eg^2+2egh
g7  = 10acd+10cfg
g8  = 8d^2e+10cg^2+2bch+3c^2h+5cdh+9d^2h+cgh+4ch^2
g9  = 8de^2+8b^2f+9deh+9bfh
g10 = 3a^2b+4ab^2+abc+10ac^2+5abd+9bd^2+2abe+8d^2h
g11 = 8bcf+8dgh
g12 = 9bef+8e^2f+9bdh+8dh^2
g13 = 9bf^2+8ef^2+4b^2g+bcg+10c^2g+5bfg+3bg^2+2bgh
g14 = 10acf+10adg
g15 = 10cdg+10afg
g16 = 8bf^2+10ag^2+3a^2h+2aeh+5afh+9f^2h+agh+4ah^2
```

These representatives specify the direction without any convention about a
tangent basis. To match the source basis explicitly, let `b1,...,b109` be the
columns of `normalMatrix({0},F0)` printed in
`../../equations/tangent_basis.md`. The 53 intrinsic columns, in order, are

```
1..10,18..27,35..39,47..51,66..70,92..109.
```

Their selected coefficient vector is

```
(1,2,3,4,5,6,6,7,7,6,1,5,4,3,2,2,3,5,1,4,3,4,1,5,2,4,1,
 5,3,2,3,2,5,1,4,8,9,9,8,10,10,9,8,8,9,8,9,10,10,10,9,10,8).
```

The existing extraction script `../../scripts/extract_deformation.m2`
explicitly multiplies that vector by the intrinsic basis, recomputes the
first-order deformation, and compares it with the stored
`deformation/generic_equivariant_state_F_order6.txt` in the frozen proof.
Thus no coordinate permutation, generator gauge, or parameter redefinition
is being silently introduced here. The rank calculation itself uses only
the displayed integral polynomials, and does not rerun that CAS extraction.

## 2. The monomial block and why only first order is needed

**PROVED.** Let

\[
M(q):S_2\otimes\operatorname{Sym}^2(\mathbf Q[[q]]^{16})
\longrightarrow S_8[[q]],\qquad
m\otimes e_i e_j\longmapsto mF_i(q)F_j(q).
\]

Its shape is `6435 x 4896`: `dim S8=binom(15,7)=6435`, while
`dim S2 * dim Sym²(Q16)=36*136=4896`. Its image is precisely `(I(q)^2)_8`
because the sixteen cubic generators generate the ideal in question.

At order zero each column is a monomial with coefficient one.
**COMPUTER-CERTIFIED monomial enumeration:** the set

\[
\mathcal C=\{m f_i f_j:1\le i\le j\le16,\ \deg m=2\}
\]

contains exactly 1829 distinct monomials. This is a finite enumeration of
4896 exponent vectors, not a Gröbner-basis or numerical-rank calculation.
It follows directly that `rank M(0)=1829`. One representative column per
element of this set gives an identity block, using those same monomials as
rows. There remain 3067 other columns and 4606 other rows.

For a remaining column `c`, subtract the selected representative `r(c)`
with the same central monomial. The first-order coefficient of the resulting
column, projected onto the noncentral rows, is

\[
\pi\bigl(M_1(:,c)-M_1(:,r(c))\bigr),
\qquad
[q](mF_iF_j)=m(g_if_j+f_ig_j).
\]

Here `pi` simply discards monomials in `C`. The twelve column differences
and twelve noncentral rows selected below define a 12-by-12 integer matrix
`Q`. Include them with the 1829 representative rows and columns to obtain
an actual 1841-by-1841 submatrix of `M(q)`; the indicated column subtractions
do not change its determinant. After subtraction, its block form is

\[
\begin{pmatrix}
\mathbf1_{1829}+O(q)&O(q)\\
O(q)&qQ+O(q^2)
\end{pmatrix}.
\]

Its Schur complement is `qQ+O(q²)`: the product of the off-diagonal blocks
starts only at order two. Therefore

\[
\det M_{\rm selected}(q)=q^{12}\det Q+O(q^{13}).
\]

**PROVED precision statement.** Even though the full determinant begins in
degree twelve, its leading coefficient is completely determined by the
first-order jet. No degree-twelve jet is required: all twelve noncentral
rows/columns vanish at order zero, so any use of an unknown order-two
coefficient raises total degree to at least thirteen. This remains true
for arbitrary higher-order formal corrections.

## 3. Human-readable twelve-column certificate

**COMPUTER-CERTIFIED entries; directly checkable by multiplication.** In the
following table, take the coefficient of `q` in each column expression.
The matrix entry `Qij` is the coefficient of the monomial in row `i` in
the expression of column `j`. All listed row monomials lie outside `C`.
Every column expression has constant coefficient zero as an ordinary
polynomial, including the differently weighted column seven.

| Index | Row monomial | Column expression |
|---:|---|---|
| 1 | b³c²deg | b²(F2 F7 − F1 F8) |
| 2 | b²c³deg | bc(F2 F7 − F1 F8) |
| 3 | bc⁴deg | c²(F2 F7 − F1 F8) |
| 4 | a⁴cdeh | a²(F3 F4 − F2 F5) |
| 5 | a³cde²h | ae(F3 F4 − F2 F5) |
| 6 | a²cde³h | e²(F3 F4 − F2 F5) |
| 7 | b⁴cdeg | bc F3 F9 − b² F2 F12 |
| 8 | acde⁴h | e²(F3 F11 − F2 F12) |
| 9 | cefg⁴h | g²(F4 F9 − F2 F11) |
| 10 | cefg³h² | gh(F4 F9 − F2 F11) |
| 11 | cefg²h³ | h²(F4 F9 − F2 F11) |
| 12 | cefgh⁴ | h²(F5 F9 − F2 F12) |

For example, the first row/column entry is `−3`: in
`b²(g2 f7+f2 g7−g1 f8−f1 g8)`, the only contribution to
`b³c²deg` is `−b²*(3c²e)*(bdg)`. It is important to subtract both
products' first derivatives, not simply inspect one product.

The complete sparse matrix is

\[
\boxed{Q=\operatorname{diag}(-3,-3,-3,-8,-8,-8,8,-8,-8,-8,-8,-8)
-2E_{1,2}-2E_{2,3}-2E_{7,1}.}
\]

Its first three rows are upper triangular, row seven's extra entry does
not contribute to a different nonzero permutation term, and all other
rows have only their diagonal entry. Consequently the determinant is
visibly the product of its diagonal entries:

\[
\boxed{\det Q=-3^3\,8^9=-3623878656\ne0.}
\]

The script additionally computes that determinant by exact fraction-free
integer elimination on the original minor. The modulo-101 pivot search
stopped at twelve new pivots, after 1311 of 3067 extra columns: it proved a
lower bound, not an exhaustive rank determination. The geometric upper
bound below is separate.

## 4. Geometric consequence and its boundary

**PROVED from the displayed determinant:** the generic degree-eight
product rank is at least 1841 for every formal lift having this exact
first-order direction. In particular, this applies to the established
zero-context all-orders smoothing and survives its algebraization.
Invertible generator changes do not change the image rank; a rescaling
`q -> lambda*q`, with `lambda != 0`, multiplies the displayed leading
coefficient by `lambda^12` and cannot make it zero.

**PROVED under the accepted smoothing hypotheses and the separately
derived degree-eight formula:** write `n=h0(N)` and `r=dim(I²)8` for the
smooth generic fibre. The formula and the established Hilbert bound give

\[
1\le h^{1,1}=1748+n-r\le1748+94-1841=1.
\]

All inequalities are therefore equalities. Thus

\[
\rho=h^{1,1}=1,\quad h^{2,1}=31,\quad n=94,\quad r=1841,
\quad \chi_{\rm top}=-60,
\]

and the smooth embedded fibre lies on a 94-dimensional Hilbert component.
These Hodge invariants are constant in its connected smooth proper
family. The assertion does not identify this arc with the older DGLA arc,
does not produce finite algebraic coefficients for a fibre, and does not
determine Picard torsion or the fundamental group.

## 5. Stage-one artifacts and replay

**COMPUTER-CERTIFIED execution:** the successful run used only standard
Python sparse integer arithmetic and an integer determinant. It took
0.189 seconds in the mathematical script, 1.316 seconds including the
guard. No CAS process was run. The guard's sampled RSS of 388 KB missed
the short-lived Python peak and is **not** a valid peak-memory estimate.
The resource caps were 300 seconds and 2800 MB, one thread. The preceding
sandbox attempt failed closed because process inspection was unavailable;
the recorded successful run had that read-only monitoring permission.

Exact stage-one files, relative to this run:

```
scripts/picard_product_first_order.py
logs/20260908T122310-picard-product-q1.json
logs/20260908T122310-picard-product-q1.stdout
logs/20260908T122310-picard-product-q1.stderr
logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json
```

Script SHA256 at execution:
`417266f19741bd74f0dfa8d0a1f4d9f42f8e80580c34cc1e772ee842dd6c2e7f`.
The JSON records the source hash, all row exponent vectors, original
column numbers and representatives, the full 12-by-12 integer matrix,
the integer determinant, and the stopping point. A new guard invocation
uses a fresh timestamped output directory; it never replaces this record.

```
cd /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-computation-2026-09-08
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_guarded.py \
  --seconds 300 --memory-mb 2800 --tag picard-product-q1 \
  -- python3 scripts/picard_product_first_order.py
```

The guard supplies the four one-thread environment variables and serial
execution lock. During Daniel's daytime use, only run this command when
the root process coordinator has granted the single computation slot.
