# Review of a specified ramified algebraic-number fibre

2026-09-08. Targeted mathematical-paper-audit mode; no CAS was run.
This is model analysis, not qualified-human verification. It does not
repeat the accepted proof audit. The claim under review is that the
finite selected Hilbert chart yields a *particular smooth closed fibre*
by the substitution π^7=101 and a unique101-adic Hensel selector.

## Verdict

**PROVED, conditional on the accepted finite-chart and frozen modular
smoothness certificates:** the construction gives sixteen homogeneous
cubics over a specified finite algebraic number field L and an actual
smooth projective Calabi--Yau threefold over L. It is not merely a formal
generic fibre. No rational reconstruction or primitive-element eliminant
is necessary to specify L: finite polynomial equations together with the
unique ramified-adic root selector specify its generator tuple exactly.

**OPEN:** a small defining polynomial for L, its degree over Q, and a
compact power-basis representation of the sixteen cubics. The construction
does **not** show that L=Q(π), or that a760-variable coefficient system is
a manageable field presentation for subsequent CAS work.

The decisive repair to the previously discussed unramified specialization
is ramification. Taking q=101 did not transfer a characteristic101
six-jet. Taking q=π with π^7=101 transfers it literally as a quotient-ring
identity, and all frozen smoothness witnesses use less than seven powers
of the uniformizer.

**Final export update:** the proof below was written using the intermediate
760-coordinate presentation. The completed export eliminates all490
auxiliary coordinates by the three invertible A-blocks, leaving270
dependent algebraic numbers and pi. Section11 identifies the presentations;
the final equations are in `RAMIFIED_FIBRE_EQUATIONS.md`.

## 1. Inputs and exact scope

The proof repository HEAD was read and is the specified frozen commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`.

| Input | SHA-256 |
|---|---|
| frozen `PROOF.md` | `f662287d41f5667cbe9bdc5774834a18e990b235c66f1902530ccf5cbac10c8f` |
| daytime `FIXED_CHART.md` | `07b7758db4d7a59ed3cb5e705d544a7b2bb909d0c6689aa3eb71ea8a03d8e28a` |
| daytime `data/fixed_chart.json` | `74c2059066518c95a5b4f3f46427aa7731ce705062b6d858db12bbc1bd9523fd` |
| computation `data/equivariant_blocks_QQ.json` | `1e815bc09cc42ecdede6e756ab1e12e332bcd456ff1e4523c705b9538c19b4ac` |
| repository `equations/deformation_data.json` | `8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f` |

Source locations inspected: frozen `PROOF.md` lines172--303, especially
the finite q-power criterion and complete stratified cover; daytime
`FIXED_CHART.md` sections1--6; the exact isotypic block builder and its
recorded multiplicities. Accepted dependencies are the full first-syzygy
presentation, formal smoothness of the invariant Hilbert germ, the unit
Jacobian certificate,101-integrality of the normalized six-jet, and the
previously audited literal/normal-form smoothness witnesses. No new
external-source search was needed for the elementary DVR, Newton, and
field-differential arguments below. The external source verification of
the prior audit is not being re-certified here.

## 2. The coefficient ring really has the required truncated characteristic

**PROVED.** Let p=101 and define

    K_p = Q_p[T]/(T^7-p),       π = class(T),
    O = Z_p[π].

The polynomial is Eisenstein. Thus K_p is a field of degree7 over Q_p.
The ring O is a finite complete local domain over Z_p, with maximal ideal
(π), since p=π^7 and O/(π)=F_p. A one-dimensional noetherian local domain
with principal maximal ideal is a DVR. Consequently O is the ring of
integers of K_p and π is its uniformizer.

There is an exact ring isomorphism

    O/(π^7) = O/(p) ≅ F_p[q]/(q^7),          π ↔ q.

Indeed reduction of the presentation Z_p[T]/(T^7-p) modulo p gives
F_p[T]/(T^7). This is not an alleged embedding F_p into O; constants
embed only in the quotient, which is exactly what the jet argument uses.
The map Z_(p) to this quotient reduces rational coefficients modulo p,
since all denominators prime to p remain invertible. For every e<=6 it
induces O/(π^e)≅F_p[q]/(q^e).

## 3. The exact finite point and its unique selector

**PROVED.** Use the *original normalized six-jet free paths* γ_j(q) for
the21 free generator coordinates; do not replace them by their linear
parts. There are two equivalent finite presentations available:

- The original chart has270 dependent generator coordinates and2940
  auxiliary syzygy coordinates, with3210 selected equations and constant
  Jacobian determinant−1.
- The equivariant multiplicity chart has270 dependent generator
  coordinates and490 kernel-graph coordinates, with490 upper equations
  and270 selected lower equations. Its selected generator Jacobian is
  invertible modulo101 by the recorded rank check. In this chart the
  central kernel graph is U=0.

For definiteness use the latter760 equations. Write them as G(q,y)=0,
where y denotes the760 dependent coordinates, and substitute q=π.
Every coefficient lies in A=Z_(101); γ_j(0)=0, G(0,0)=0, and the
Jacobian in y at (0,0) has determinant a unit of A. Therefore

    G(π,0) ∈ π O^760,        det G_y(π,0) ∈ O^×.

Multivariable Newton iteration gives a root y*∈πO^760. It is unique in
that residue class: the difference of the values at any two such roots
is an invertible matrix times their difference, because that matrix
reduces to the same invertible Jacobian modulo π. Completeness supplies
existence; the iteration successively corrects the residue classes
modulo π², π³, and so on, or doubles precision.

Thus the definition is finite and unambiguous:

    π^7=101;   G(π,y*)=0;   y*∈πO^760,

with K_p and π specified by the Eisenstein field presentation above.
No arbitrary root of the global polynomial system is being selected.

## 4. Why the other equations and flatness still hold exactly

**PROVED, using the accepted fixed-germ theorem.** Apply the integral
implicit-function recursion before specializing. The unit Jacobian gives
a unique solution y(w) in A[[w_1,...,w_21]] for the selected equations.
The remaining full Schur equations vanish in Q[[w]], by the established
identification with the smooth21-dimensional fixed Hilbert germ. Their
coefficients already lie in A[[w]], which embeds into Q[[w]], so they
vanish in A[[w]] itself.

Evaluate w_j=γ_j(π). Each value lies in πO, and all coefficients of the
implicit series are101-integral. Every series therefore converges in O.
The resulting tuple is y* by uniqueness. Hence all omitted equations
vanish at y*, not just modulo π^7. In particular the full FR identity is
exact, and every special first syzygy lifts. The appropriate A-blocks
are invertible because they reduce to identity modulo π.

This integrality is essential: an arbitrary Q[[w]] identity cannot be
evaluated101-adically when coefficient denominators are uncontrolled.

For clarity, flatness can be checked directly without an additional
Hilbert-scheme theorem. Put I=(F_1,...,F_16)⊂O[a,...,h]. If a vector v
of polynomial coefficients has Fv divisible by π, then v modulo π is
a special syzygy. Express it in the original thirty linear syzygies,
lift that expression using the exact matrix R, and subtract. The
remaining coefficient vector is divisible by π. Therefore

    I ∩ πO[a,...,h] = πI.

The quotient O[a,...,h]/I is π-torsion-free, hence O-flat. Its graded
pieces are finite free with the required Hilbert function. The same
lifting argument preserves the given pure resolution, or alternatively
the accepted relative Cohen--Macaulay argument applies. Thus the generic
fibre is a pure threefold of codimension4. This dimensional hypothesis
is needed when interpreting fourth Jacobian minors as smoothness tests.

## 5. The six-jet is exactly the one certified in the frozen proof

**PROVED.** Reduce y* modulo π^7 and use the ring isomorphism in section2.
It solves the selected equations over F_101[q]/q^7 with the assigned
free paths and marked central point. Nilpotent implicit-function
uniqueness identifies it with the normalized certified generator jet.
The source normalization is

    H(q) -> H(q)P(q)^(-1),        P(0)=Id_16,

where P is the coefficient matrix on the sixteen fixed pivot monomials.
Its inverse is101-integral modulo q^7. This is a generator-basis change
depending on the base parameter only, not a projective coordinate change.
It preserves the ideal and, modulo the ideal, the rank-four Jacobian
Fitting ideal. Consequently the genuine source Jacobian identities
transport to the normalized equations. No equality of syzygy gauges is
needed for this step.

## 6. Smoothness of this actual fibre, not only generic smoothness in q

**PROVED, conditional on the frozen finite identities.** Suppose the
geometric generic fibre over K_p had a singular point. It is defined
over a finite extension K'/K_p. Let O' be its complete DVR of integers
and τ a uniformizer. Projectivity extends the point to an O'-section.
Write π=uτ^r with u a unit. Its special point lies on the geometric
Stanley--Reisner fibre. Normalize homogeneous coordinates so at least
one is a unit; all affine coordinates on that chart are then integral.

The frozen proof supplies the following complete cover. Each identity
is an identity over F_101[q] modulo the displayed q-power, so section2
transports it to O modulo the identical π-power, and thence to O'.

| Specialization stratum | Frozen certificate | Consequence in O' |
|---|---|---|
| D(a), D(d), and S3 translates D(c),D(g),D(f) | q^5∈(F, selected genuine fourth minors)+(q^6) | A singular section would give π^5∈π^6O', impossible since5r<6r. |
| Interior of triangle {b,e,h} | Relative-Morse leading discriminant q²p(u,v), with `(p,p_u,p_v)=(1)` on the support torus | Support coordinates and the recorded linearization determinants are units. After division by π² and reduction modulo τ, a singular section gives a common critical zero of p, contradicting the exact Bezout identity. |
| Coordinate-edge tori in that plane | Localized q^4 membership modulo q^5 | The inverted support coordinate is a unit on the section. Thus π^4∈π^5O', impossible. |
| Coordinate vertices b,e,h | `(y2−33)q^5` membership modulo q^6 and S3 translates | The multiplier reduces to−33 at the relevant vertex and is a unit. Thus again π^5∈π^6O', impossible. |

The support-localization variables remain integral because their
denominators are units. Flatness and the original central-generator
checks justify the local generating subsets exactly as in the frozen
proof. The relative Morse step uses invertible linearization matrices
and2 invertible, all valid in O'; its residue computation is literally
the same characteristic101 computation. The cover exhausts the special
fibre: the complement of the five global charts is the coordinate plane
P²_{b,e,h}, whose strata are precisely the listed triangle, edges, and
vertices.

Every case contradicts existence of a geometric singular point. Thus
the actual fibre over K_p is smooth. No inference from an open generic
q-locus to a guessed numeric q-value is used: the transported finite
identities are evaluated on the proposed singular section of this
particular mixed-characteristic DVR family.

## 7. Its coefficient field is a finite number field

**PROVED.** Let K_0=Q(π), embedded in K_p, and define

    L=K_0(y*_1,...,y*_760)⊂K_p.

This is a finitely generated field extension of K_0. Differentiate the
760 polynomial identities G(π,y*)=0 over K_0. Since the selected
Jacobian determinant is nonzero, they imply dy*_i=0 for every i.
Therefore Ω_{L/K_0}=0. In characteristic zero, its dimension is the
transcendence degree of this finitely generated field extension. Hence
L/K_0 is algebraic and finite. This also proves directly that the root
is a zero-dimensional algebraic point, despite our having specified it
using a complete local field.

The free coordinates γ_j(π) and all sixteen cubic coefficients lie in
L. Define X_L⊂P^7_L by those sixteen cubics. Its base change to K_p is
the smooth fibre proved above. Smoothness descends under this field
extension. The required Hilbert polynomial, pure resolution, trivial
canonical bundle and O-cohomology follow from the same exact family
and descend as well. After any embedding L into C, this gives a smooth
complex projective Calabi--Yau threefold.

The number field L includes the auxiliary coordinates only for a simple
finite definition; they can be eliminated later. Its completion at the
selected place is K_p, because it already contains K_0, whose completion
is K_p. This local degree7 does **not** determine the global degree[L:Q].

## 8. Hilbert-component identification

**PROVED, using the established component analysis.** The point is the
evaluation of the integral formal parametrization of the origin-selected
fixed Hilbert germ. Every rational polynomial vanishing on the algebraic
component underlying that germ vanishes as a formal series and hence
at this convergent point, after clearing its finitely many denominators.
Thus X_L lies in that same algebraic component; it is not an arbitrary
remote root of a selected equation subsystem.

The fixed germ contains the certified smoothing arc, and its image lies
in the already established94-dimensional Hilbert component. The smooth
point therefore has the certified geography

    h11=ρ=1,       h21=31,       e(X)=−60.

As before, this does not determine Picard torsion or the fundamental
group, and does not prove Pic(X)=ZH without a torsion argument. It also
does not identify this closed point with a specialization of one uniquely
specified all-orders zero-context arc: that arc was never unique. The
construction uses a rigorously identified curve agreeing with its six-jet.

## 9. Atomic claim ledger and failed counterexample attempts

All entries are derivations; existing computational inputs retain the
previously stated trust boundary. Supplied-proof state is `succeeds`
and claim state is `established` **conditional on those inputs** for
R1--R7. Human verification is not claimed.

| ID | Claim | Classification | Direct dependency |
|---|---|---|---|
| R1 | O/(π^7) is precisely F101[q]/q^7 | **PROVED**, supporting-check | Eisenstein presentation and elementary DVR argument |
| R2 | The selected point exists uniquely in πO^760 | **PROVED**, supporting-check | R1, unit Jacobian, integral free paths |
| R3 | All full equations and flatness hold | **PROVED**, supporting-check | R2, integral formal fixed-chart identity, lifted syzygies |
| R4 | The point has the certified six-jet | **PROVED**, supporting-check | R1,R2, normalization and implicit uniqueness |
| R5 | Its actual K_p fibre is geometrically smooth | **CONDITIONAL**, supporting-check | R3,R4, complete frozen finite-identity cover |
| R6 | Coefficient tuple generates a finite number field | **PROVED**, supporting-check | R2, invertible Jacobian, field differentials |
| R7 | The number-field fibre is smooth and lies on the selected component | **CONDITIONAL**, supporting-check | R3,R5,R6, convergent component identities |
| R8 | A small field presentation or field degree is known | **OPEN**, not-checked | Requires subsequent elimination or field extraction |

Dependency map: R1→R2,R4; R2→R3,R4,R6; R3,R4→R5;
R3,R5,R6→R7. R8 is not required by R1--R7.

Attempts to defeat the argument:

- **FAILED counterexample:** the earlier discriminant q(q−101) obstructs
  unramified q=101, but at q=π its terms have valuations2 and8. It
  cannot cancel, so it does not challenge this construction.
- **No issue established:** F101 cannot embed in a characteristic-zero
  field. No such embedding is used; the required embedding is into
  O/(π^7), whose characteristic is101.
- **No issue established:** an algebraic branch could have divergent
  coefficients. Here the unit Jacobian gives uniformly101-integral
  coefficients and all substituted free values lie in πO, ensuring
  convergence.
- **No issue established:** the root might be transcendental over Q.
  The invertible square polynomial Jacobian gives the differential proof
  of algebraicity in section7; mere p-adic existence alone would not.
- **No issue established:** remote roots might lie on different Hilbert
  components. The unique residue-zero Hensel selector and integral
  formal parametrization exclude this ambiguity.
- **Exposition constraint:** do not call the coefficient field Q(π),
  and do not equate a finite implicit number-field presentation with a
  small practical power-basis presentation.

## 10. Verification boundary and reproducibility

**CONDITIONAL trust boundary:** the source modular certificates and exact
chart data are accepted inputs from the previous audit, not rerun here.
Their mathematical applicability to mixed characteristic was checked
explicitly above. The present proof uses only read-only source inspection,
hashing and derivation. A locale warning from `shasum` did not affect its
exit status or hashes; no CAS, package installation, numerical calculation,
or external write occurred.

**High confidence within the recorded analysis:** every initially
identified issue has a direct algebraic resolution, and the decisive
mixed-characteristic passage is an exact quotient-ring isomorphism rather
than a continuity heuristic. Independent qualified-human review remains
appropriate, especially of the accepted finite-chart and modular source
certificates. For the narrow ramification argument itself, no additional
mathematical obligation remains beyond those explicitly stated inputs.

## 11. Final auxiliary-free coefficient presentation

**PROVED equivalence on the selected branch:** in each of the three
isotypic blocks the upper equations give U=A^(-1)B. Since A is the
identity at the central point, its determinant is a unit throughout the
selected residue-zero Hensel branch. Replace each selected lower Schur
entry by its bordered determinant

    det[[A,B_j],[C_i,D_ij]]=det(A)*(D_ij-C_i*A^(-1)*B_j).

The resulting270 equations have the same local zero set after eliminating
the490 auxiliary entries. Their selected Jacobian determinant is19
modulo101, independently recomputed from the exported rational factors.
Thus the implicit existence, uniqueness, integrality and algebraicity
arguments above apply directly to the270 dependent generator coefficients.
Conversely the auxiliary values are uniquely recovered by the displayed
inverse, so omitting them does not change the generated field or the fibre.

The exact final presentation is

    pi^7=101; 270 exported bordered determinants=0;
    (theta1,...,theta270) in(pi O)^270,
    L=Q(pi,theta1,...,theta270) inside Q101(pi).

All21 free coefficients are their original normalized six-jet polynomials
at pi. No alternative tangent or linear free path was substituted. A
separate parser checked every displayed cubic coefficient and the unit
Jacobian; genuine ramified arithmetic checked all1650 full block equations
modulo pi14 and pi56. These finite checks validate the export; the exact
closure proof remains the integral formal-identity argument in section4.
