# Targeted review: the eight-parameter singular slice

**PROVED, conditional on the recorded exact fixed-chart map and the passed
v3 support certificate:** every origin-selected flat threefold fibre in
the specified eight-dimensional free-coordinate slice is singular at every
point of P²_(b,e,h). This is an all-orders multivariate statement, not a
deduction from one numerical path or finitely many jets. The original
selected smooth fibre is outside the assertion's scope.

This bounded review inspected the v3 script, its output, the successful
stdout, and the two builders supplying its quadratic map and ten exact
intrinsic tangent vectors. No CAS or new arithmetic job was run. Source
hashing and reading/counting the saved certificate were the only checks
besides mathematical/code inspection. Qualified-human verification is not
claimed.

## The multivariate inference

The state v=(z,U) has 291 cubic coefficients and 490 graph coordinates.
The saved rational map H is homogeneous quadratic and independent of the
chosen path. Its construction solves the selected lower equations as

```text
H_z,dependent = D_dependent^(-1)*(C(z)*U)_selected,
H_z,free = 0,
H_U = B(H_z)−A_minus_identity(z)*U.
```

Thus v=ell+H(v) is the original selected incidence subsystem whenever
ell=(t,B(t)) and D(t)=0; t's free coordinates are the prescribed free
values. Inverting the fixed dependent Jacobian introduces no parameter
dependence or higher-degree terms into H. The builder's elimination and
back substitution implement exactly these formulas.

For j in {1,3,5,6,7,8,9,10}, v3 checks D(t_j)=0 over Q, constructs
ell_j=(t_j,B(t_j)), and checks that their restrictions to the 21 free
coordinates have rank eight. Let a_1,...,a_8 be independent parameters and
ell(a)=sum a_j ell_j. The support algorithm starts with the **union** of
all eight forcing supports, then closes under every nonzero quadratic
monomial of H. Its history is 108→419→539. For every inactive output
coordinate, each monomial contains an inactive input; hence H preserves
the resulting coordinate subspace W identically. This tests mixed terms
between different directions as well as terms within one direction.

Iterating v_0=0, v_(n+1)=ell(a)+H(v_n) stays in W. Since H has degree two,
the iterations stabilize coefficientwise in Q[[a_1,...,a_8]] and give the
unique origin solution of v−ell(a)−H(v)=0 (its derivative in v at zero is
the identity). Therefore every inactive coordinate vanishes exactly in
the multivariate formal solution. Any substitution a_j=a_j(q) with zero
constant terms preserves these identities. The actual free values, not
merely their first derivatives, must remain in this eight-dimensional
span.

The final support has 186 cubic coordinates (178 dependent and eight free)
and 353 U coordinates. These are support bounds: they do not assert every
listed coordinate is nonzero or algebraically independent. The accepted
full-versus-selected fixed-germ theorem supplies exact omitted equations
and flatness on the origin branch; v3 itself does not replay that theorem.

## Singularity follows directly from the monomial support

Set J=(a,c,d,f,g), the ideal of P²_(b,e,h). The script parses each central
cubic as its actual three-letter monomial and checks every active tail
monomial. It proves

```text
F_i in J for every i,
F_i in J² for i outside {3,9,12}.
```

These are exact polynomial support identities. Along the plane all
derivatives in b,e,h vanish, while the normal derivatives of a generator
in J² also vanish. Thus at most rows 3,9,12 of the full Jacobian are
nonzero there, giving rank at most three. On any affine projective chart
the tangent dimension is at least 7−3=4. A flat fibre with the established
threefold Hilbert data has dimension three, so every plane point is
singular. This checks projective points, not the irrelevant cone vertex.

The identities specialize at any convergent origin-selected evaluation.
They also hold on the algebraic closure of the origin branch because
their pullbacks to its faithful formal parametrization vanish. Arbitrary
remote solutions of the selected polynomial subsystem are not certified.

## Scope, repairs, and claim ledger

| Claim | Finding | Remaining assumptions |
|---|---|---|
| Joint support is invariant for arbitrary eight free parameters | supporting-check; supplied proof succeeds | Exact saved rational H and v3 finite support checks |
| Every fibre in the selected flat branch has the plane and Jacobian rank ≤3 | supporting-check; supplied proof succeeds | Origin branch, flat threefold Hilbert data |
| First-order vanishing of orbits 2,4 alone excludes every smoothing | Unsupported broader statement; not claimed | Higher free coefficients can leave the slice |

Version 1's inference from the single-path U support was inadequate for
the enlarged slice. Version 3 repairs it by recomputing closure from the
joint forcing support; the conclusion no longer uses that failed premise.
Version 2's monomial-parser TypeError prevented its certificate and did
not disprove the mathematics. Version 3 explicitly converts the stored
three-letter central monomials into exponent vectors. The failed scripts
and logs remain evidence of those failed attempts, not successful checks.

“Gauge parameters zero” here names the specified linear free-coordinate
slice. It is not an invariant classification of all abstract deformations
whose tangent lies in the eight intrinsic directions. Paths activating
orbits 2 or 4, or leaving that free-coordinate slice at any higher order,
remain outside this exclusion. In particular the original smooth fibre,
whose original direction activates both, is unaffected. The result gives
no model, topology, or novelty statement beyond this bounded exclusion.

Input identities:

```text
eef8fdbbd5ff8eba71f0699d292c52b5f264ae4fac419437e7b5ff7f0d25c839  scripts/certify_singular_eight_parameter_slice_v3.py
c7ee536bebaefd6e0422433b8a8f9f6939fcb014ae824c7e11a54caa53ec5fc9  data/singular_eight_parameter_slice_v3/singular_slice_certificate.json
674b99cda2b41fe70b9a48333fb006c434f233cc7187eb5d1b07ed6238e837d7  logs/20260908T232531034152-singular-joint-slice-monomial-parser.stdout
```

The output is `data/singular_eight_parameter_slice_v3/singular_slice_certificate.json`;
its `input_hashes` identify the exact rational map, tangent vectors, fixed
chart, and block matrices. The successful log is
`logs/20260908T232531034152-singular-joint-slice-monomial-parser.stdout`,
which records the joint closure and completed plane certificate. These
finite outputs are the computational boundary of this paper-only review;
they were inspected, not independently recomputed here.
