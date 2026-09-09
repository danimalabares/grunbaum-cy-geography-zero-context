# Equivariant obstruction check for the nine-vertex triangulation of CP²

Run: `runs/cp2-nine-vertex-equivariant-t2-2026-09-09`. One worker, exact arithmetic
(Macaulay2 1.20 with VersalDeformations 3.0, pure-Python `fractions` re-verification).
Nothing outside this directory was modified; the reference repository
`../grunbaum-zero-context-proof` (HEAD `ee984e95…`, clean) was read only. No commit or push was
made during the computation itself.

> **Publication pass, 2026-09-09.** The verifiers in this directory were re-run before publication
> (`PUBLICATION_VERIFICATION.md`); every output was reproduced byte for byte. The text below was
> corrected in four places, each marked **[corrected 2026-09-09]**: the 93-dimensional embedded
> tangent space is now distinguished from the 21-dimensional intrinsic `T¹`; a sentence that
> contradicted §6 about `S_3`-equivariant deformations was replaced; the projective caveat was
> fixed (Proj of a flat graded family is a flat projective family); and it is stated explicitly
> that no explicit two-parameter family or smooth generic fibre is claimed. The numerical content
> is unchanged. The unfinished optional quadratic-obstruction cross-check was **not** restarted; no
> result depends on it.

## Headline

**VERIFIED.** For `A = QQ[x_1..x_9]/I_Δ` and `G = ⟨(23)(46)(78), (12)(45)(78)⟩ ≅ S_3`,

| quantity | value |
|---|---|
| dim Hom_S(I,A)₀ — embedded graded tangent space, written `(T¹_A)₀` below | 93 |
| dim T¹(A/QQ)₀ = Hom_S(I,A)₀ / (image of `gl_9`) — intrinsic graded cotangent | 21 |
| dim (T²_A)₀ — graded obstruction space | 126 |
| dim ((T¹_A)₀)^G (embedded; 17 of these are coordinate changes, 6 intrinsic) | 23 |
| dim ((T²_A)₀)^G | **14** |
| dim ((T²_A)₀)^{Aut(Δ)}, `|Aut(Δ)| = 54` | **0** |
| dim ((T¹_A)₀)^{Aut(Δ)} (embedded; 3 are coordinate changes, leaving **2** intrinsic) | 5 |

**Notation [corrected 2026-09-09].** Throughout this file `(T¹_A)₀` denotes the degree-0 part of
`Hom_S(I,A)`, the tangent space of the graded *embedded* deformation functor of the presentation
`S = QQ[x_1..x_9] → A` (93 classes, the `normalMatrix` output). It is **not** the intrinsic first
cotangent cohomology `T¹(A/QQ)₀`, which is the quotient of `Hom_S(I,A)₀` by the 72-dimensional
image of the coordinate changes `gl_9` and has dimension `93 − 72 = 21` (§6, coordinate orbit).
The invariant counts 23 and 5 are for the embedded space; the corresponding intrinsic invariant
counts are 6 and 2. `(T²_A)₀` is the degree-0 second cotangent cohomology of the presentation
(126 classes), which is at the same time the obstruction space of the embedded functor and,
since coordinate changes are unobstructed, of the intrinsic graded functor.

For the requested group `G` (the stabiliser of vertex 9) the invariant obstruction space is
**nonzero**, so the hypothesis `T²^G = 0` of the equivariant formal-lifting lemma
(`EQUIVARIANT_FORMAL_LIFT.md`, §3) **fails**, and, applied to `G` alone, the lemma gives no
all-orders lifting conclusion for the 23-dimensional space of `G`-invariant graded tangent
directions of `A` (its 5-dimensional `Aut(Δ)`-invariant subspace is handled by the full group,
next). For the **full**
automorphism group of order 54 the invariant obstruction space **vanishes**, so the lemma **does
apply** there: all five `Aut(Δ)`-invariant graded tangent directions, two of which are not
coordinate changes, lift to all-orders `Aut(Δ)`-equivariant flat graded deformations of `A`
(§5–§6). Since `G ⊂ Aut(Δ)`, these deformations are in particular `G`-equivariant. Whether any
of them (or any other deformation of `A`) is a smoothing is **undecided**: no generic fibre was
examined. See §4–§7 for exactly what this does and does not mean.

## 1. Input verification (VERIFIED)

Script: `scripts/verify_input.py`, log `logs/verify_input.log`. Facets transcribed from the
arXiv e-print TeX source of Chapoton–Manivel, arXiv:1109.6490v1, §5 (hashes in
`SOURCE_STATE.json`; transcription in `data/facets_chapoton_manivel_1109.6490v1.txt`).

- 36 distinct 5-element facets on vertices 1..9; every 4-face lies in exactly two facets.
- f-vector `(9, 36, 84, 90, 36)`; every 3-subset is a face, so all minimal nonfaces are the
  `126 − 90 = 36` missing 4-subsets: `I_Δ` has exactly 36 minimal generators, all quartic
  monomials (`data/minimal_nonfaces.json`, `data/generators.m2.txt`).
- `G` has order 6, is nonabelian (hence `≅ S_3`), fixes vertex 9, and maps the facet set to
  itself, hence preserves `I_Δ`. Brute force over `S_9` gives `|Aut(Δ)| = 54`, and `G` is
  exactly the stabiliser of vertex 9 in `Aut(Δ)`. The paper's generators
  `(147)(258)(369)`, `(123)(456)(789)`, `(12)(46)(89)` lie in `Aut(Δ)`.
- Link of vertex 9: 8 vertices, 20 facets (a 3-sphere). Its own obstruction theory is **not**
  used anywhere below.
- Ring data (`logs/t2_dims.log`): `dim A = 5` (affine), `degree 36`, Hilbert-series numerator
  `1 + 4t + 10t² + 20t³ − t⁴ + 2t⁵` (negative entry: `A` is not Cohen–Macaulay, as expected for
  a triangulated CP²). First syzygies of the 36 quartics: 90, all linear.

## 2. Cotangent cohomology and the induced G-action (VERIFIED)

Script: `scripts/equivariant_t2.m2`, log `logs/equivariant_t2_G_S3.log`, certificate
`certificates/G_S3_certificate.json`, basis representatives `certificates/G_S3_basis.m2.txt`.
Independent re-verification: `scripts/verify_certificate.py`, log
`logs/verify_certificate_G_S3.log`, summary `certificates/G_S3_python_reverification.json`.

Construction (no quadratic obstruction equations are involved):

- `F0` = the 36 generators, `R = gens ker F0` (36×90), `kos = koszul(2,F0)`.
  `T² := Hom(im R / im kos, A) / im(Rᵀ)` is Schlessinger's second cotangent cohomology of the
  presentation; its degree-0 basis (126 classes) is taken as representatives in `A^90`. This is
  the same module `CT^2` uses; `CT^2({0},F0)` independently returns a `90×126` matrix.
- Each representative is checked to be a genuine homomorphism (it kills the second syzygies
  `syz R` and the Koszul relations), and the 126 normal forms modulo the trivial homomorphisms
  `im(Rᵀ)` are linearly independent over `QQ` (rank 126).
- For `g ∈ G` with `h = g⁻¹`: `g` permutes the 36 monomial generators (permutation matrix
  `P_g`, no signs at this level); the transported relation matrix `P_h·h(R)` lies in `im R`, and
  `C_h` with `R·C_h = P_h·h(R)` is computed exactly. Then `(g·φ)(r_k) = g(φ(h·r_k))`, i.e.
  `g·T2 = g(C_h)ᵀ · g(T2)`, is well defined because `φ` kills `syz R`. Normal forms modulo
  `im(Rᵀ)` are compared coefficientwise to obtain a `126×126` matrix `M_g` over `QQ`, with
  the identity `T2nf · M_g = (g·T2)nf` asserted exactly. Signs do occur: every `M_g` has
  entries in `{−1, 0, 1}` and `−1` appears for all `g ≠ e`.
- `(T¹)₀ = Hom(I, A)₀` (93 classes from `normalMatrix`), with `g·T1 = P_g · g(T1)` and
  coordinates solved exactly.
- The six matrices satisfy `M_{gh} = M_g M_h` on all 36 pairs, for both `T²` and `T¹`
  (checked in Macaulay2 and again in Python). Reynolds projectors `(1/6)Σ M_g` are idempotent;
  their ranks equal their traces.

Characters (element order : trace on `T²`, trace on `T¹`; multiplicity in `G`):

| class | count | χ_{T²} | χ_{T¹} |
|---|---|---|---|
| identity | 1 | 126 | 93 |
| transpositions | 3 | −12 | 9 |
| 3-cycles | 2 | −3 | 9 |

Hence, as `S_3`-representations (triv, sgn, std of dimensions 1,1,2):

- `(T²)₀ ≅ 14·triv ⊕ 26·sgn ⊕ 43·std`, so `dim (T²)₀^G = 14`.
- `(T¹)₀ ≅ 23·triv ⊕ 14·sgn ⊕ 28·std`, so `dim (T¹)₀^G = 23`.

The dimension of invariants is the same for a representation and its dual (finite group,
characteristic 0), so no left/right or dual convention affects the number 14.

## 3. Quadratic obstruction equations were not used (VERIFIED by construction)

The representation was constructed directly on the full degree-0 `T²` (§2), so no injectivity
of the dual primary obstruction map `κ₂*: T²* → Sym²(T¹*)` is needed and none is claimed.
An optional cross-check of that injectivity (rank of the 126 order-two Kuranishi quadrics in
93 variables, `scripts/quadric_rank_check.m2`) is reported in §6 if it finished; it does not
feed into the headline result.

## 4. Does the equivariant formal-lifting lemma apply? (assessment)

**No, not as stated.** The lemma requires `T²^G = 0`; here `dim ((T²_A)₀)^G = 14`. The
argument that lifted every invariant tangent of the eight-vertex sphere ring to all orders
therefore does not transfer to `A`, even though the sphere is the link of the fixed vertex 9.
Every number differs: the sphere note has `dim T¹ = 109`, `dim T² = 27`, `T²^G = 0`; here
`93`, `126`, and a 14-dimensional invariant obstruction space.

What this does **not** say:

- It does **not** show that any invariant tangent direction is obstructed. The equivariant
  Kuranishi map `(T¹)₀^G → (T²)₀^G` (23 → 14) may still vanish on some or all directions; its
  zero locus was not computed. Nonvanishing invariants make the lemma inconclusive, nothing more.
- It says nothing about smoothability: vanishing invariant obstructions would not prove a
  smoothing exists, and nonvanishing ones do not prove non-smoothability.
- All statements concern the **graded embedded deformation functor** of the presentation
  `S → A` (homogeneous ideal with its 36 generators). **[corrected 2026-09-09]** Every flat graded
  deformation of `A` over an Artinian base `QQ[q]/(q^n)` has a `Proj`, which is a flat projective
  family in `P⁸` over that base with special fibre `X = Proj A`; so each all-orders graded
  deformation produced in §6 does give a formal arc in the Hilbert scheme `Hilb(P⁸)` through
  `[X]`. What is **not** established is the converse identification of the whole Hilbert
  deformation functor at `[X]` with the graded embedded functor of `A` (equivalently, that
  `Hom_S(I,A)₀ → H⁰(N_X)` and the obstruction spaces match). That comparison needs
  vanishing hypotheses on local cohomology that were not checked (`A` is not Cohen–Macaulay),
  so `(T¹_A)₀` and `(T²_A)₀` are not asserted to be the tangent and obstruction spaces of
  `Hilb(P⁸)` at `[X]`, and nothing is said about deformations of `X` that do not come from
  graded deformations of `A`.
- The same considerations apply to any subgroup `H ⊆ G`: since `(T²)^G ⊆ (T²)^H`, every
  subgroup also has nonzero invariant obstruction space (`dim ≥ 14`), so the lemma fails for all
  of them. For the larger group `Aut(Δ)` of order 54 the invariant space is a subspace of the
  14-dimensional one; see §5.

## 5. Full automorphism group of order 54 (status below)

Generators `(147)(258)(369)`, `(123)(456)(789)`, `(12)(46)(89)` together with the two
`G`-generators were fed to the same script (`data/group_Aut54_generators.txt`); the Python
verifier closes the group by composition/matrix multiplication and checks well-definedness
on all pairs before computing the Reynolds projector. See §6 for the outcome.

## 6. Status of optional items

**Order-54 group `Aut(Δ)` — VERIFIED.** Matrices for the five generators
`(147)(258)(369)`, `(123)(456)(789)`, `(12)(46)(89)`, `(23)(46)(78)`, `(12)(45)(78)` were computed
in Macaulay2 (`logs/equivariant_t2_Aut54_generators.log`, `certificates/Aut54_generators_certificate.json`);
`scripts/verify_certificate.py` closed the group exactly (54 distinct permutations, every product
assigned a unique matrix, representation property checked on all 54² pairs of both `T²` and
`T¹` matrices; log `logs/verify_certificate_Aut54.log`):

| quantity | value |
|---|---|
| dim ((T²_A)₀)^{Aut(Δ)} | **0** |
| dim ((T¹_A)₀)^{Aut(Δ)} | 5 |

Character data (element order : χ_{T²}, χ_{T¹}; count): identity (126, 93) ×1; order 2 (−12, 9) ×9;
order 3 (−3, 9) ×6, (0, 0) ×6, (0, 3) ×14; order 6 (0, 0) ×18. Reynolds projector on `T²` is the
zero matrix, on `T¹` it is an idempotent of rank 5 = trace.

Consequence: for the **full** automorphism group the hypothesis `T²^{Aut} = 0` of the equivariant
formal-lifting lemma **holds**. Applying the lemma exactly as in `EQUIVARIANT_FORMAL_LIFT.md` §3 (finite
group of order 54, invertible in `QQ`; graded embedded deformation functor of the presentation
`S → A` with tangent `(T¹_A)₀` and complete obstruction space `(T²_A)₀`), every `Aut(Δ)`-invariant
graded tangent direction (a 5-dimensional space) is the tangent of a compatible all-orders
`Aut(Δ)`-equivariant formal graded embedded deformation of `A` over `QQ[[q]]`. Caveats:

- This is an all-orders **flat graded** deformation statement for `A`, not a smoothing statement.
  **[corrected 2026-09-09]** Taking `Proj` order by order turns each such deformation into a flat
  formal projective family in `P⁸` with special fibre `X = Proj A ⊂ P⁸`, i.e. a formal arc in
  `Hilb(P⁸)` through `[X]`. Identifying the *entire* Hilbert deformation functor at `[X]` with
  the graded embedded functor of `A` is a separate question that was not addressed (see §4).
- Some or all of the five invariant directions may be coordinate changes (image of the
  `Aut(Δ)`-invariant part of `gl_9` in `Hom(I,A)₀`); the lemma is only interesting for directions
  outside that image. See the coordinate-orbit item below.
- The lemma is applied for the whole group; it fails for the vertex stabiliser `G ≅ S_3` (§2), and
  hence for every subgroup of `G`.

**Coordinate orbit — VERIFIED** (`scripts/coordinate_orbit.m2`, logs `logs/coordinate_orbit_*.log`,
coordinates in `certificates/*_coordinate_orbit_coords.txt`). The 81 derivations `x_j ∂/∂x_i`
(the `gl_9`-action, i.e. projective coordinate changes) span a **72**-dimensional subspace `C` of
`(T¹_A)₀ = Hom(I,A)₀`; the quotient `(T¹)₀/C ≅ T¹(A/QQ)₀` of abstract graded first-order
deformations of `A` has dimension **21**. Since `(im gl_9)^H = im (gl_9)^H` and `(gl_9)^H` is spanned
by the orbital sums of `H` on ordered pairs (the diagonal orbital is the Euler derivation, which
maps to 0):

| group `H` | orbitals | dim `C^H` | dim `(T¹)₀^H` | dim `(T¹/C)^H` (invariant abstract directions) |
|---|---|---|---|---|
| `Aut(Δ)` (54) | 4 | 3 | 5 | **2** |
| `G ≅ S_3` | 21 | 17 | 23 | **6** |

So the lemma, applied to `Aut(Δ)`, yields a 2-dimensional space of `Aut(Δ)`-invariant abstract
graded first-order deformations of `A` each of which extends to an all-orders equivariant flat
graded deformation. Nothing is asserted about the generic fibre of any of these deformations.

**[corrected 2026-09-09] What is and is not claimed here.** The extension statement is an
existence statement obtained from the lemma (obstruction classes lie in `(T²)^{Aut(Δ)} = 0`), one
tangent direction at a time, over `QQ[[q]]`. No explicit equations of any of these deformations
were computed, not even to second order; no explicit two-parameter family is exhibited; and no
statement about the singularities or smoothness of any generic fibre is made. Whether `X = Proj A`
(a triangulated `CP²`, a non-Cohen–Macaulay Stanley–Reisner fourfold in `P⁸`) is smoothable at all
remains **undecided** by this run.

**Primary-obstruction rank cross-check — NOT FINISHED (optional, not needed).** The order-two
Kuranishi computation (`scripts/quadric_rank_check.m2`, 126 quadrics in 93 parameters) was stopped
after 6 minutes of wall time (1.3 GB RSS) to respect the session budget; `logs/quadric_rank_check.log`
records only the dimensions. Its purpose was to test whether the dual primary obstruction map
`κ₂*: T²* → Sym²(T¹*)` is injective, i.e. whether a quadric-based recovery of the representation
would have detected the whole 126-dimensional obstruction space. **No claim about that rank is
made.** The representation results above do not depend on it. Resume instructions: `CHECKPOINT.md`.

## 7. Conjectures / not verified

- **[corrected 2026-09-09]** An earlier version of this bullet said that nothing in this run
  establishes existence of a `G`-equivariant all-orders graded deformation of `A`. That contradicted
  §6: the `Aut(Δ)`-equivariant all-orders deformations obtained there are `G`-equivariant because
  `G ⊂ Aut(Δ)`. So `G`-equivariant all-orders graded deformations **do** exist, with tangents in the
  5-dimensional (2-dimensional intrinsic) `Aut(Δ)`-invariant subspace. What remains open is whether
  any of the *other* `G`-invariant tangent directions — the `23 − 5 = 18` embedded, or `6 − 2 = 4`
  intrinsic, directions not fixed by all of `Aut(Δ)` — extend to all orders; the lemma is silent
  there because `(T²)^G ≠ 0`, and deciding it needs the `G`-equivariant Kuranishi equations
  restricted to the 23 invariant parameters (a follow-up computation; `versalDeformation` with the
  invariant sub-basis of `T¹` would give the primary quadratic part).
- The isotypic decompositions above are exact consequences of the verified characters; any
  geometric interpretation of the 14 invariant obstruction classes is not attempted.
