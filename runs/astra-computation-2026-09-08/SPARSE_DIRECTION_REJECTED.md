# A sparse direction rejected geometrically before lifting

8 September 2026. **FAILED as a smoothing route; PROVED geometric
obstruction.** The proposed S3-orbit weights

```
(0,0,1,0,0,0,0,1,0,0)
```

preserve an extra grading. The uniquely selected linear-free-coordinate
curve therefore cannot have a connected smooth degree-20 Calabi–Yau
fibre. No lifting job was run for this direction.

## Exact source direction

**PROVED by the specified basis sums.** In the frozen 53-dimensional
intrinsic basis, sum the vectors with indices

```
O3 = {3,14,17,21,29,31},
O8 = {36,39,43,44,46,53}.
```

These are source intrinsic positions, not indices in the109-dimensional
embedded tangent basis. The lookup and exact polynomial images are in
`../../equations/deformation_data.json`. This definition does not select
terms by filtering their old numeric coefficients.

With the usual ordered generators f1,...,f16, the resulting first-order
corrections are

```
g1  = c^2e + f^2h           g2  = ade + fgh
g3  = b^2d + fh^2          g4  = 0
g5  = bcd + aef            g6  = bd^2 + eg^2
g7  = 0                   g8  = d^2e + c^2h
g9  = de^2 + b^2f          g10 = a^2b + d^2h
g11 = bcf + dgh           g12 = e^2f + dh^2
g13 = ef^2 + bg^2         g14 = 0
g15 = 0                  g16 = bf^2 + a^2h.
```

This is a valid invariant first-order tangent because it is a sum of the
specified intrinsic orbit vectors. Its validity as a tangent does not
make its selected higher-order curve a smoothing.

## Nine-variable weight calculation, by hand

**PROVED.** Give a,...,h weights u_a,...,u_h and q weight v. Equality of
weights in `fi+q gi` gives, from the six distinct O8 relations,

```
u_f+u_h-u_a-u_b+v = 0
u_d+u_e-u_b-u_g+v = 0
u_b+u_d-u_a-u_h+v = 0
u_e+u_f-u_c-u_h+v = 0
u_b+u_f-u_e-u_g+v = 0
u_d+u_h-u_c-u_e+v = 0.
```

Their solution is

```
u_b=u_e=u_h=B,
u_a=u_c=u_g=A,
u_d=u_f=A-v.
```

For example the equations first give `u_e+u_h=2u_b` and
`u_b+u_e=2u_h`, hence equality of those three weights in characteristic
zero. The O3 term `c²e` in the `abf` generator gives

```
2u_c+u_e-u_a-u_b-u_f+v = 2v = 0.
```

Thus v=0, and the complete nine-weight kernel is two-dimensional:
ordinary projective scaling, and the additional grading

```
(u_a,...,u_h,v)=(0,1,0,0,1,0,0,1,0).
```

All24 correction monomials visibly have the same B-degree as their
central generator. Both source S3 generators preserve the partition
`{b,e,h} | {a,c,d,f,g}`, so this torus commutes with S3.

The normalized fixed chart inherits this diagonal action, and its free
coordinates are weight eigenvectors. The linear free paths are invariant:
their nonzero coefficients have weight zero, and all other prescribed
coefficients are zero. Uniqueness of the implicit solution in the smooth
fixed germ forces the entire selected curve to be torus invariant, not
just its first-order term. This conclusion uses the unique linear-free
curve; it does not constrain arbitrary higher free-coordinate choices.

## Elementary cubic-component obstruction

**PROVED.** Among the sixteen central generators, only `f4=acg` has
B-degree zero. Their B-degrees, in generator order, are

```
1,1,2,0,1,1,1,1,2,1,1,2,1,1,1,1.
```

On the torus-invariant normalized curve each lifted generator retains
its central B-degree. Restrict to

```
P4 = {b=e=h=0} in P7.
```

The other fifteen generators vanish identically there. The restriction
of F4 is one cubic, nonzero on the generic fibre because its central
term is acg. Thus the family contains a cubic hypersurface in this P4,
of dimension three. A connected smooth threefold is irreducible; it
cannot contain such a three-dimensional closed subvariety without
coinciding with an irreducible component of it. That would force degree
at most three, contrary to degree20 (and contradict nondegeneracy).
If the cubic vanished at an exceptional parameter, containment of the
whole P4 would contradict three-dimensional flatness even sooner.

The alternative vector-field proof is consistent: the additional
nontrivial G_m acts on a nondegenerate fibre, whereas a smooth CY of this
type has H0(T_X)=H0(Omega²_X)=0. The cubic-component argument avoids
needing that Hodge-theoretic fact.

**PROVED caution about the product rank.** The twelve product minor from
`PRODUCT_RANK_CERTIFICATE.md` becomes diagonal with eleven entries−1
and one+1 in the recorded positions; explicitly
its diagonal is `(-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1)`, determinant−1.
Thus the product-rank lower bound can hold along an everywhere-singular
curve. The degree-eight Hodge formula requires a smooth lci fibre and
must not be applied without it.

## The one subsequent candidate

**PROVED removal of this specific obstruction:** adding O10 with weight1
adds `a²c` to the `abf` generator. In the preceding two-parameter weight
kernel its equality of weights forces `3A=2A+B`, hence A=B. Only scalar
projective grading remains. This does not itself prove irreducibility
or smoothness.

The resulting single three-orbit experiment, with all other orbit
weights zero, is recorded in `SPARSE_THREE_ORBIT_ATTEMPT.md`. No other
weight choices were tested.
