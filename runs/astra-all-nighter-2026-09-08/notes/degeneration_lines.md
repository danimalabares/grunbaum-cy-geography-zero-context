# Five line branches on one facet; fifteen by symmetry

This is a degeneration calculation for the actual audited ramified fibre,
not a calculation requiring a new manageable presentation of its coefficient
field. The finite checks are implemented in
`scripts/certify_degeneration_lines.py` and the root's version with a corrected
metadata label. All five branch checks passed; their exact certificate is
`data/line_certificates_all/line_certificates.json`. Thus the fifteen-line
existence and normal-bundle conclusions are **PROVED under the audited
finite-fibre assumptions, with COMPUTER-CERTIFIED finite minors**. The
additional exhaustive facet classification in §6 passed the separate
J013 check; its exact output is data/facet_transverse_exhaustion/facet_transverse_exhaustion.json. The algebraic derivation and exact equations are supplied here.
No statement about the complete scheme of lines, its dimension, total length,
or a Gromov–Witten invariant is made.

## 1. Lines crossing the double locus: the first-order calculation

Let F_i(q)=f_i+q g_i+O(q²), using the actual source six-jet q coefficient.
The stored `first_order_corrections` and `six_jet_coefficients[1]` agree.
Pivot normalization only subtracts combinations of central generators at
first order, so restriction of g_i to a central facet is unchanged.

Take the facet P³_abce and the Grassmann chart

```text
a=s, b=t, c=u*s+v*t, e=w*s+z*t;
(d,f,g,h)=q*(Y_d(s,t),Y_f(s,t),Y_g(s,t),Y_h(s,t)).
```

Here each Y is linear in s,t. On the central line require

```text
u*v*w*z*(u*z-v*w) != 0.
```

Together with det(a,b)=1 these are all six pairwise nonzero determinants
of its four support-coordinate linear forms. Thus the line meets all four
coordinate faces in distinct points in their triangle tori. It certainly
does not avoid the double locus. All four crossings are explicitly included.

For a generator with exactly one outside variable x_j, the coefficient of
q in containment is (its support quadratic)*Y_j+g_i|_abce. Generators with
two or more outside variables have both contributions zero. Direct sparse
restriction gives the uniquely forced rational normal functions

```text
Y_g=Y_h=0,
Y_d=−N/(c*e),   N=3*a²*b+4*a*b²+a*b*c+10*a*c²+2*a*b*e,
Y_f=−M/(a*b),   M=10*a²*c+a*c*e+2*b*c*e+3*c²*e+4*c*e².
```

These expressions are consistent for every generator with the same outside
variable. A first-order line lift exists precisely when both rational
functions restrict to binary linear polynomials. Since the four denominator
zeros are pairwise distinct, this is precisely pole cancellation at the
four crossings. Removing only nonzero support-coordinate factors gives

```text
A = 2+3*v+4*z = 0,                                      (a=0)
B = 10+w+3*u*w+4*w² = 0,                                (b=0)
C = (3+2*w)*v−(4+2*z)*u = 0,                            (c=0)
D = 10*(u*z-v*w)²−w*((3+u)*z−(4+v)*w) = 0.             (e=0)
```

On this open set w is nonzero. Solve B for u, A for v and then C for z.
The would-be exceptional w=2 gives 42=0 and is impossible in characteristic
zero or 101. No division by z+2 is used, so the legitimate w=−3/2 case is
not silently discarded. The result is

```text
u = −(4*w²+w+10)/(3*w),
v = −2*(4*w²+w+10)/(5*(w−2)),
z = (6*w²−w+20)/(5*(w−2)),
u*z−v*w = (w−20)*(4*w²+w+10)/(15*w*(w−2)).
```

After substitution the last equation factors exactly as

```text
D = 2*(w−20)*(19*w²−2*w+40)*(w³−16*w²−10*w−50)
       / (45*w²*(w−2)²).
```

The root w=20 makes c and e proportional and is excluded. The remaining
five roots are the two roots of P2=19w²−2w+40 and the three roots of
P3=w³−16w²−10w−50. Both polynomials are irreducible over Q (the quadratic
has negative discriminant, and the cubic has no rational root). The script
checks all denominator and boundary gcds and verifies every one of the
64 first-order binary-cubic coefficients exactly in Q[w]/(P2) and
Q[w]/(P3). Therefore these are five genuine first-order lifts, and exhaust
this specific facet-transverse chart at first order. That last restricted
statement does not classify boundary lines or the complete line scheme.

The uniquely forced normal coefficients are

```text
d_s = −10*u/w, d_t = 0,
f_s = −(10*v+u*z+v*w+2*u*w+3*u²*z+6*u*v*w+8*u*w*z+4*v*w²),
f_t = −(v*z+2*u*z+2*v*w+6*u*v*z+3*v²*w+4*u*z²+8*v*w*z),
g_s=g_t=h_s=h_t=0.
```

At 101, P2 has roots 5,27; P3 has root 9 and its remaining roots are
alpha and 7−alpha in F101[alpha]/(alpha²−7alpha+28). That quadratic is
irreducible. These five roots are distinct. The script checks every
boundary determinant modulo 101 at all five roots, not just over Q.

## 2. The finite line equations over the actual fibre

Let L and O be the already audited coefficient field and ramified DVR,
with pi^7=101, and let F_i denote the actual exact cubics over L∩O.
Use twelve unknowns in this precise order:

```text
u,v,w,z,d_s,d_t,f_s,f_t,g_s,g_t,h_s,h_t.
```

Define a rank-two line by the exact formulas

```text
a=s, b=t, c=u*s+v*t, e=w*s+z*t,
d=pi*(d_s*s+d_t*t), f=pi*(f_s*s+f_t*t),
g=pi*(g_s*s+g_t*t), h=pi*(h_s*s+h_t*t).
```

For each i=0,...,15 and k=0,...,3 put

```text
E_(4*i+k) = coefficient of s^(3−k)*t^k in F_(i+1)(line) / pi.
```

These are finite polynomials in the twelve unknowns with coefficients in
L∩O: every central monomial has an outside variable and every noncentral
coefficient is in pi O. This integrality is the reason to divide by pi
*before* Hensel lifting. Modulo pi, E is exactly the first-order system
computed in §1, including the chosen normal coefficients.

For each of the five residue points, the certificate supplies a list of
twelve zero-based indices `selected_residual_indices_zero_based`. Impose
those twelve E equations and select the unique solution congruent to the
twelve displayed residue coordinates. Use O for the three F101 points,
and the integers O2 in the unramified quadratic extension of Q101(pi) for
the other two. The saved 12-by-12 Jacobian determinant must be a unit;
the script computes it in the relevant residue field. Multivariate Hensel
then supplies a unique solution in the stated residue class.

This is an exact algebraic line specification: finite equations, the
existing exact fibre coefficients, and an isolating residue condition.
The line's field is

```text
M=L(u,v,w,z,d_s,d_t,f_s,f_t,g_s,g_t,h_s,h_t)
```

inside the chosen p-adic field. It is finite over L: differentiating the
twelve selected polynomial identities over L and using their invertible
Jacobian kills all field differentials; characteristic zero identifies
their dimension with transcendence degree. Its global degree is not
asserted to equal the residue-field or completion degree. This construction
does not make L or M a practical power-basis field presentation.

## 3. Why all omitted line equations vanish exactly

This is the key closure argument. It uses the audited exact syzygy matrix
R, not a guessed extension from a first-order line.

Substitute the line into the exact identity F R=0 and divide by pi. The
64-dimensional column E therefore satisfies 150 linear equations

```text
T(line)*E=0.
```

Rows are indexed by a syzygy column (30 choices) and a binary quartic
coefficient (5 choices). Columns are the 16 binary cubics' coefficients
(4 each). At the central residue line, R reduces to the canonical 30
linear monomial syzygies. Thus T is an explicit 150-by-64 matrix whose
entries are the support-coordinate line coefficients, with their recorded
syzygy signs.

For each residue point the script selects a nonzero 52-by-52 minor. Let
P be its 52 column indices and J the 12 complementary indices. The Hensel
system of §2 is exactly E_J=0. The 52 minor rows of T E=0 now say
T_(rows,P) E_P=0. This square matrix stays invertible because its determinant
is a unit modulo pi. Consequently E_P=0 as well, proving all 64 containment
equations in O or O2, and hence in M. No obstruction-space vanishing for
lines is assumed. An arbitrary invertible minor of a selected incidence
subsystem would not suffice without these syzygies.

The expected rank has a geometric explanation, although the exact minor
is the finite certificate. Along a facet-transverse line the special
threefold is a local complete intersection: at each boundary point only
the two adjacent facets meet. The normal rational functions have pole
orders determined by the number d_v of adjacent faces assigned to each
outside vertex. On abce these are d_d=d_f=2 and d_g=d_h=0. The compatible
binary-cubic residual space therefore has dimension
sum_v(2+d_v)=4+4+2+2=12. The explicit rank computation confirms the actual
generator/syzygy presentation realizes exactly that space.

The script also verifies T*J_full=0 for the entire 64-by-12 first-order
Jacobian. This follows by differentiating the exact relation at E=0 and
catches generator order, signs, and coefficient-order mismatches separately
from the two nonsingularity checks.

## 4. Isolation, reducedness, and the normal bundle

At the actual characteristic-zero line the twelve selected divided
equations have an invertible Jacobian in the twelve scaled parameters.
The true Grassmann coordinates use the eight outside coefficients
D=pi*Y. If J is the divided Jacobian, the corresponding 12-by-12 minor
of the ordinary cubic containment equations is

```text
pi^12 * det(J) * pi^(−8) = pi^4 * det(J),
```

which is nonzero. Thus the line scheme's Zariski tangent space is zero:
H0(N_line/X)=0. This proves the line is isolated and reduced in the full
line scheme near that point, not merely isolated in a chosen search.
The Grassmann chart is an open neighborhood because a=s,b=t.

On the audited smooth Calabi–Yau threefold, adjunction gives a rank-two
normal bundle of degree −2. Over an algebraic closure it splits on P¹;
vanishing of H0 forces both summand degrees negative, hence

```text
N_line/X ≅ O_P1(−1) ⊕ O_P1(−1).
```

The five residue lines have distinct w values and so yield five distinct
actual geometric lines. The invariant fibre is preserved by
sigma=(b h)(c g)(d f) and tau=(a c)(b e)(d f). Apply the identity, sigma,
and tau∘sigma to the five lines. Their reduction facets are respectively
abce, aegh, and bcgh. Full four-coordinate support makes the three groups
disjoint. Thus successful certificates prove **at least fifteen distinct
isolated reduced lines, each with normal bundle O(−1)⊕O(−1), on the selected
finite algebraic fibre**. They do not exclude other isolated lines or
positive-dimensional components elsewhere in the line scheme.

## 5. Reproduction target and trust boundary

The guarded job's target is five first-order line branches over exact
degree-2/3 fields and modulo 101, together with five 52-by-52 syzygy minors
and five 12-by-12 Jacobian minors. Its unknowns are the twelve line
parameters above; its equations are 64 q-divided binary-cubic coefficients
and 150 linear syzygy relations. A 300-second pilot with
`--only-rational-residues` tests the three F101 roots. The full job adds
two points over F101². Success requires all residual, boundary, rank,
Jacobian, and derivative-syzygy checks, not merely a polynomial root.

```text
python3 -B scripts/certify_degeneration_lines.py --output <fresh artifact directory>
```

The output `line_certificates.json` records exact first-order field
representations, all selected row and column indices, the determinants,
residue coordinates, source hashes, script hash, and elapsed time. A
reproduction recomputes the finite matrices from the frozen sources.
This subtask launches no unreported process.

Remaining assumptions are the audited selected cubics, their exact FR=0
with the recorded central syzygies, integral six-jet matching, and geometric
smoothness/Calabi–Yau property of the actual fibre. The Hensel and linear
closure arguments above supply the missing all-orders line theorem; a
finite jet alone is not substituted for it. This is mathematical analysis
with exact computational evidence, not qualified-human verification.

## 6. Exhaustion of the facet-transverse reduction class

The separate tiny script `scripts/certify_facet_transverse_exhaustion.py`
checks all twenty coordinate facets and every one of their eighty rational
normal functions. It verifies the same compatibility used in §1 directly
from each relevant central generator and its actual first correction.
Fifteen facets have the following single-monomial pole witnesses:

| Facet | Outside coordinate | Forced normal function |
|---|---|---|
| abcd | f | −10ac/b |
| abde | g | −8de/b |
| acdf | b | −10ac/f |
| acef | d | −10ac/e |
| adeg | b | −8de/g |
| adfg | e | −10ag/f |
| aefh | c | −8ef/h |
| afgh | b | −8fh/a |
| bcdh | a | −8bd/h |
| bcef | g | −8bf/e |
| bcfg | d | −10cg/b |
| bfgh | a | −8fh/b |
| cdfg | b | −10cg/d |
| cdgh | e | −8dh/c |
| degh | c | −8dh/e |

At the denominator's coordinate face, every numerator coordinate is a
unit by the triangle-torus condition. Its coefficient 8 or 10 is nonzero
both in characteristic zero and 101. The pole therefore cannot cancel,
excluding any facet-transverse first-order line on those fifteen facets.

The two additional facets bdeh and befh give three incompatible crossings.
On bdeh the forced normal functions are

```text
Y_a=−d*(8b+9e)/h, Y_c=−d*(9b+8h)/e,
Y_f=0, Y_g=−d*(8e+9h)/b.
```

Projection from the d vertex to P²_(b,e,h) maps a transverse line to a line:
if its image were a point, the original line would pass through that vertex
and would not have four distinct face crossings. The three crossings
would force the projected line to contain

```text
(-9:8:0), (-8:0:9), (0:-9:8).
```

Their 3-by-3 determinant is −217. On befh, projecting from f similarly
forces (0:−8:9), (−8:9:0), (−9:0:8), with determinant 217. Both are nonzero
over Q and units modulo 101. These two facets are excluded. The remaining
three facets are exactly the S3 orbit abce, aegh, bcgh of §4. The rational
elimination in §1 has five simple roots and no omitted denominator cases
in both characteristic zero and 101. Thus there are exactly fifteen
facet-transverse first-order central lines.

For completeness, an arbitrary actual line reducing to such a central
line cannot evade the computation by acquiring outside coordinates of
fractional pi-valuation. Let O' be any finite extension valuation ring in
which the actual line is defined, normalize its two selected support
coordinates to s,t, and call its eight outside line coefficients Z.
They have strictly positive valuation. The central incidence equations
have the form

```text
A(U)*Z + terms at least quadratic in Z + pi*(integral terms) = 0.
```

The linear map A at the residue line is injective on the eight outside
coefficients. For each outside variable, some central generator has just
that outside variable and a nonzero support-coordinate quadratic. Binary
multiplication by this quadratic is injective on its two linear
coefficients, and the four outside variables use disjoint generator
blocks. Thus A has a unit 8-by-8 minor over O'. If delta is the minimum
positive valuation of an outside coefficient and delta<v(pi), invert
this minor in the displayed equations. Their linear terms have minimum
valuation delta, while every other term has valuation at least
min(2delta,v(pi))>delta, a contradiction. Therefore Z is divisible by pi.

It follows that every actual line with facet-transverse reduction falls
within the scaled variables of §2 even after arbitrary finite ramification.
Reducing F(line)/pi gives exactly one of the fifteen first-order points.
At each point the selected Jacobian is a unit, so Hensel uniqueness holds
after any further complete extension. The corresponding actual line must
be the one constructed above. Hence, after the saved certificate checks,
there are **exactly fifteen actual geometric lines whose reduction at the
chosen ramified place is facet-transverse**. Each is reduced, isolated,
and has normal bundle O(−1)⊕O(−1).

Every projective line on the actual fibre extends to a line after passing
to a finite extension DVR, because the Grassmannian is proper. Its central
line is contained in some coordinate facet, since that line is irreducible
and the special scheme is a finite union of the twenty facets. The only
remaining reductions therefore lie in the boundary of the class just
classified: some support coordinate is identically zero, or two support
coordinate forms are proportional so the line meets a lower-dimensional
coordinate stratum. These boundary reductions are **OPEN**. The exhaustion
statement does not prove the total line scheme finite or compute its
geometric length.
