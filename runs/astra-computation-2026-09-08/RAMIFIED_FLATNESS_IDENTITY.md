# A finite complete syzygy identity for the actual ramified fibre

8 September 2026. **PROVED under the accepted integral fixed-germ
identity theorem:** the sixteen exported cubics have a finite,
denominator-cleared16-by-30 matrix of exact linear syzygies. Its reduction
is the complete central first-syzygy module. This proves graded flatness,
not merely agreement to finite precision.

No new CAS normal-form calculation is claimed here. The matrix is given
by a finite determinant/adjugate circuit whose two block identities are
proved below. The nontrivial lower identity follows at the **selected
algebraic Hensel root** from the integral all-equations theorem, not from
the numerical checkpoint modulo pi14.

## 1. Fixed algebraic coefficients and indexing

Use exactly `data/ramified_fibre_coefficients.json`, SHA256

```
0e8c3bb4a62a77af4beb22182bc8e7dc771dabd09514a0597aaed5d8b61f0616
```

and its human-readable expansion `RAMIFIED_FIBRE_EQUATIONS.md`. The field is

\[
L=\mathbf Q(\pi,\theta_1,\ldots,\theta_{270})
\subset K=\mathbf Q_{101}(\pi),\qquad \pi^7=101.
\]

Let O=Z_101[pi], a complete DVR. The theta tuple is the unique solution of
the exported270 bordered-determinant equations with every theta_k in
pi O. Those finite equations, the Eisenstein equation, and the isolating
condition specify the numbers; no unspecified all-orders arc is an
additional part of their definition.

The JSON gives every lambda_j as either theta_k or a rational polynomial
in pi. Precisely, if `d[k]` is the k-th entry of
`dependent_coordinate_indices_zero_based` (k starting at zero), then

\[
\lambda_{d[k]+1}=\theta_{k+1}.
\]

For each of the21 indices in `free_coordinate_indices_zero_based`, use
the coefficient list `pi_polynomial_coefficients` in the corresponding
`lambda_definitions` entry, ordered from pi^0 through pi^6. These are
the original six-jet free paths. Every denominator is a101-unit.

Put `x=(a,b,c,d,e,f,g,h)`. The ordered central monomials are

```
(f1,...,f16)=(abf,abg,abh,acg,ach,adh,bdf,bdg,beg,cde,ceg,ceh,cfh,def,dfh,efg).
```

The exported `cubic_equations[i].terms` defines the finite cubic F_i by
its exponent vector and either constant coefficient1 or the indexed
lambda coefficient. Equivalently,

\[
F_i=f_i+\sum_{m\in\mathcal T_3}\lambda_{o(i,m)+1}m,
\]

where T3 is the list of104 cubic monomials other than the sixteen f_i,
and `o(i,m)` is the zero-based coefficient-orbit index in
`data/fixed_chart.json`. Thus F_i lies in L[x] and O[x].

## 2. The original multiplication matrix, without isotypic ambiguity

**PROVED finite specification.** Form the330-by-128 coefficient matrix

\[
\mu_{\alpha,(i,j)}=[x^\alpha](x_jF_i),
\qquad |\alpha|=4,\quad1\le i\le16,\quad1\le j\le8.
\]

Its original zero-based column number is `8*(i-1)+(j-1)`; this is the
`multiplication_columns` order. An entry is just the coefficient of
`x^(alpha-e_j)` in F_i, or zero if an exponent is negative. No polynomial
multiplication of high degree is needed to define any entry.

Order the first98 rows by `pivot_monomials` and the other232 rows by
`standard_quartics`, both as stored in `data/fixed_chart.json`. Order the
first98 columns by `pivot_columns` and the last30 by `extra_columns`.
These are exact lists, not a new pivot selection at the algebraic point.
They have the equivalent intrinsic definition: take one first-occurring
column for each distinct central monomial `x_j f_i`; the remaining
columns are the extras. In these reordered bases write

\[
\mu=\begin{pmatrix}A&B\\ C&D\end{pmatrix},
\]

with shapes `98x98`, `98x30`, `232x98`, `232x30` respectively.
Reduction at pi gives

\[
\bar A=1_{98},\quad\bar B=U_0,\quad\bar C=\bar D=0.
\]

Here U0 has one1 in each extra column, at the row for its central
monomial. In this **original** chart B need not reduce to zero. Do not
confuse it with the smaller isotypic kernel-graph matrices, where a
constant change of basis has already made their B blocks vanish at the
origin. Both describe the same multiplication map.

## 3. A denominator-cleared finite kernel circuit

Define

\[
\Delta=\det A\in L\cap O,\qquad \Delta\equiv1\pmod\pi.
\]

It is a unit of O. Define the128-by-30 scalar matrix K in reordered
column coordinates by

\[
\boxed{K=\begin{pmatrix}-\operatorname{adj}(A)B\\
\Delta\,1_{30}\end{pmatrix}.}
\]

Restore each row of K to its original multiplication-column index. This
is a finite polynomial circuit in pi and theta: adjugate entries are
97-by-97 cofactors of the explicitly specified98-by-98 matrix A, and
Delta is its98-by-98 determinant. No matrix inverse or infinite series
occurs in K. Keeping these shared determinants unexpanded is an exact
finite representation and avoids irrelevant expression growth.

The defining rational-number constants already lie in Z_(101). If an
ordinary integer-polynomial circuit is desired, let b be a common
denominator of all entries of mu; b is prime to101. Replacing mu by
b mu replaces K by b^98 K. This clears those coefficient denominators
and rescales the central syzygy basis by a unit. Adjugation has already
cleared the potentially variable denominator det A.

Now define the actual linear syzygy matrix R by

\[
\boxed{R_{i,k}(x)=\sum_{j=1}^8 x_j\,
K_{\,8(i-1)+(j-1),\,k},
\qquad1\le i\le16,\ 1\le k\le30.}
\]

The row index of K in this formula is zero-based; the generator, variable
and syzygy indices are one-based. This specifies all480 linear entries of
R over the same number field L, without adding any algebraic unknowns.
Coefficient extraction identifies the quartic row vector `F R` with the
330-by-30 scalar coefficient matrix `mu K`.

## 4. Why the entire identity is exactly zero

**PROVED literal upper identity, over the polynomial coefficient ring:**

\[
A(-\operatorname{adj}(A)B)+B\Delta
=-(\Delta1_{98})B+B\Delta=0.
\]

The lower block is the finite polynomial matrix

\[
-C\operatorname{adj}(A)B+\Delta D
=\Delta\bigl(D-CA^{-1}B\bigr).
\]

**PROVED exact lower identity at the selected algebraic root:** all
232-by-30 Schur equations `D-CA^{-1}B=0` vanish there by the integral
fixed-germ theorem. More explicitly:

1. Before the ramified evaluation, the selected equations have a unique
   formal solution over Z_(101) in the21 free coordinates, because the
   selected constant Jacobian is a unit. The isotypic bordered equations
   in the actual export select the same local germ; their270-by-270
   Jacobian is19 modulo101.
2. The smooth fixed-germ theorem makes every omitted full multiplication
   relation vanish in the characteristic-zero formal coordinate ring.
   Their remainders are101-integral series, so they vanish already in
   Z_(101)[[free coordinates]].
3. Substituting the original free paths at pi converges in O. The result
   is the exported algebraic Hensel root by uniqueness. Consequently all
   full Schur equations vanish **in O**, not just modulo pi^7 or pi^14.
   The original A and the three smaller A blocks are invertible there.

Therefore the exact coefficient-field identities are

\[
\boxed{\mu K=0,\qquad(F_1,\ldots,F_{16})R=0\quad\text{in }L[x].}
\]

The distinction about the selected root is essential: no claim is made
that all omitted equations vanish on every remote global solution of
the270 bordered equations, or that a global ideal-membership normal
form has been computed. They vanish on the precisely selected algebraic
branch by the proved integral identity theorem.

## 5. Complete central syzygies, not merely thirty accidental relations

Modulo pi, Delta=1 and adj(A)=1, so K reduces to

\[
\bar K=\begin{pmatrix}-U_0\\1_{30}\end{pmatrix}.
\]

The thirty syzygy columns are the differences below. Here e_i denotes
the i-th formal generator slot, not a projective coordinate:

```
 1: f e2  - g e1          2: f e3  - h e1
 3: g e3  - h e2          4: b e4  - c e2
 5: b e5  - c e3          6: g e5  - h e4
 7: b e6  - d e3          8: c e6  - d e5
 9: a e7  - d e1         10: a e8  - d e2
11: f e8  - g e7         12: a e9  - e e2
13: d e9  - e e8         14: a e11 - e e4
15: b e11 - c e9         16: d e11 - g e10
17: a e12 - e e5         18: d e12 - h e10
19: g e12 - h e11        20: a e13 - f e5
21: e e13 - f e12        22: b e14 - e e7
23: c e14 - f e10        24: a e15 - f e6
25: b e15 - h e7         26: c e15 - d e13
27: e e15 - h e14        28: b e16 - f e9
29: c e16 - f e11        30: d e16 - g e14.
```

**COMPUTER-CERTIFIED combinatorics, with an explicit explanation:** their
extra-column entries form the30-by-30 identity, so these are independent
and form the entire degree-four kernel of the central multiplication
map, whose rank is98. The same list and its zero-based indices are
exported in `central_linear_syzygies`.

**PROVED using the accepted central resolution:** its first syzygy module
is generated by exactly thirty relations in shift4. Therefore a basis
of this degree-four kernel generates the **whole polynomial syzygy
module**. The known resolution, not the dimension count alone, is what
rules out missing higher-degree first generators.

## 6. Explicit DVR flatness argument

Let S=O[x] and I=(F_1,...,F_16). If `h=Fv` belongs to I and is divisible
by pi in S, then v modulo pi is a syzygy of the central generators.
By completeness above write

\[
\bar v=\bar R\,\bar w
\]

for a polynomial vector `bar w` over F101[x]. Lift its coefficients to
O. Then `v-Rw=pi v1` for a polynomial vector v1, and the exact FR=0
identity gives

\[
h=Fv=FRw+\pi Fv_1=\pi Fv_1\in\pi I.
\]

Thus

\[
\boxed{I\cap\pi S=\pi I.}
\]

Since S has no pi-torsion, the quotient S/I has no pi-torsion either.
A torsion-free module over a DVR is flat. Every graded piece is a
finite free O-module, so its generic and special dimensions agree.
This is full graded flatness, not only flatness in degrees three/four.

## 7. Hilbert series and Calabi–Yau consequences

**PROVED from graded flatness and the accepted special resolution:**
the generic coordinate ring has Hilbert series

\[
\frac{1-16t^3+30t^4-16t^5+t^8}{(1-t)^8}
=\frac{1+4t+10t^2+4t^3+t^4}{(1-t)^4}.
\]

It has affine dimension4, hence projective dimension3, and degree
`1+4+10+4+1=20`. Its Hilbert polynomial is

\[
P(m)=\frac{10}{3}m^3+\frac{14}{3}m.
\]

The full pure resolution lifts over the DVR by successive kernel
flatness and graded Nakayama. Its generic shifts and ranks remain
`0,3,4,5,8` and `1,16,30,16,1`; positive-degree entries admit no minimal
cancellation. Hence the generic coordinate ring is Cohen–Macaulay and
Gorenstein with canonical shift `8-8=0`. It is saturated, its dualizing
sheaf is O_X, and `H¹(O_X)=H²(O_X)=0`. These statements descend from
K to the number field L by field extension.

**PROVED conditional on the independently reviewed smoothness transport:**
the actual X_L is smooth, so its dualizing sheaf is its canonical line
bundle and `K_X=O_X`. This finishes the flatness/Hilbert/Calabi–Yau part
of the finite-fibre certificate. Smoothness is not inferred merely from
FR=0. The separate degree-eight minor then gives the stated Hodge pair
(1,31), as reviewed in `SPARSE_AND_RAMIFIED_REVIEW.md`.

## 8. Gauge and exact success criterion

The source six-jet is matched after its recorded parameter-dependent
generator-basis normalization `H(q) -> H(q)P(q)^(-1)` modulo q7,
with P(0)=identity and101-integral inverse. At q=pi this is a unit
generator-basis change modulo pi7 and preserves the ideal and Jacobian
Fitting ideal. The finite adjugate syzygies above are a fresh canonical
gauge; equality with the source's stored syzygy gauge is not required.
No equality of unspecified all-orders formal arcs is asserted.

**PROVED success criterion met by the algebraic argument:** the actual
finite16 cubics, together with the finite adjugate circuit R, satisfy
exact FR=0 over their specified number field; Delta is a unit; and the
central relations generate the full first-syzygy module. These are the
conditions needed for the displayed torsion/flatness proof. A large
denominator-cleared CAS normal-form check could provide another
certificate, but has not been run and is not being substituted for the
explicit mathematical identity argument above.
