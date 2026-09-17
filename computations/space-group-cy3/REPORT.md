# Space groups with orbifold quotient S³ and Kummer Calabi–Yau threefolds — stage 1: the 14 linear cases

Audit run 2026-09-17 (single run, Claude Fable 5.1). Scope of this stage: the 14 symmorphic members of
the 35-group list and their identification with the published Kummer construction. The other 21 groups
are recorded as pending (§8). Every number below is reproduced by `python3 scripts/run_all.py`
(exact arithmetic, about one minute, no dependencies beyond Python 3).

Labels used throughout: **[published]** a statement read in the cited source; **[verified]** recomputed
here from the raw inputs; **[deduction]** an argument written out here from cited theorems whose
hypotheses were checked (the theorem itself is not re-proved; "not re-read" marks theorems cited from
memory of the literature, see `SOURCES.md` §D); **[open]** not established.

## 0. Conclusions

1. **The 35-list is correct as transcribed** [verified against the source]: the labels of Figure 2.8 of
   Johnson–Burnett–Dunbar, recovered from the text layer of the cached PDF, are exactly the 35 numbers
   under audit (`data/jbd_figure_2_8_groups.json`); the counts of §2.9 of that paper (45 = 4+1+4+1+35
   polar groups with non-cyclic point group; 12 cubic groups) are consistent with the list. The
   underlying-space property itself (R³/Γ ≅ S³) is [published] (Dunbar), not re-derived.
2. **The proposed 14 are exactly the symmorphic members of the list** [verified by two independent
   databases]: 16, 21, 22, 89, 97, 149, 150, 155, 177, 195, 196, 207, 209, 211. For each of them every
   coset representative of Γ/Λ has translation part in Λ at the ITA origin (spglib), and CrystCat's
   `IsSymmorphicSpaceGroup` agrees; the other 21 are non-symmorphic in both databases.
3. **Each of the 14 is the published Kummer construction for one of the 16 Z-classes** [verified with
   explicit certificates]: for each group an explicit `P ∈ GL(3,Z)` conjugates the point group, written
   in a primitive basis of Λ, onto Donten-Bury's Table 1 representative and (a second `P`) onto Burek's
   representative (§3, `output/zclass_matching.json`). Together with the two symmorphic groups outside
   the list (I222 = 23, I23 = 197) the 16 symmorphic Sohncke groups with non-cyclic point group biject
   onto the 16 Z-classes; the 16 classes are pairwise non-conjugate by invariants computed here (119
   pairs) or by an exhaustive intertwiner search (the pair F432/I432), independently of the published
   classification.
4. **Hodge numbers** [verified, one shared implementation, §4]: the orbifold Hodge numbers of
   `A_τ/G`, `A_τ = C³/(Λ+τΛ)`, agree with Donten-Bury's Table 2 (via `b₂ = h^{1,1}`, `b₃ = 2+2h^{2,1}`)
   and with Burek's tables in all 14 cases (and in the two control cases), and with
   Andreatta–Wiśniewski for P432. The Euler numbers agree with an independent Dixon–Harvey–Vafa–Witten
   count in all 16 cases.

   | ITA | HM | arithmetic class | (h^{1,1}, h^{2,1}) | e | Donten-Bury | Burek |
   |---|---|---|---|---|---|---|
   | 16 | P222 | 222P | (51, 3) | 96 | D4(1) | G₄.₁ |
   | 21 | C222 | 222C | (21, 9) | 24 | D4(2) | G₄.₂ |
   | 22 | F222 | 222F | (15, 3) | 24 | D4(4) | G₄.₃ |
   | 89 | P422 | 422P | (36, 6) | 60 | D8(1) | G₈.₁ |
   | 97 | I422 | 422I | (15, 3) | 24 | D8(2) | G₈.₂ |
   | 149 | P312 | 312P | (15, 15) | 0 | D6(2) | G₆.₁ |
   | 150 | P321 | 321P | (15, 15) | 0 | D6(1) | G₆.₂ |
   | 155 | R32 | 32R | (7, 7) | 0 | D6(3) | G₆.₃ |
   | 177 | P622 | 622P | (21, 9) | 24 | D12 | G₁₂.₁ |
   | 195 | P23 | 23P | (19, 3) | 32 | A4(1) | G₁₂.₂ |
   | 196 | F23 | 23F | (7, 3) | 8 | A4(2) | G₁₂.₄ |
   | 207 | P432 | 432P | (20, 6) | 28 | S4(1) | G₂₄.₁ |
   | 209 | F432 | 432F | (11, 3) | 16 | S4(2) | G₂₄.₃ |
   | 211 | I432 | 432I | (11, 3) | 16 | S4(3) | G₂₄.₂ |
   | *23* | *I222 (control, not in list)* | 222I | (15, 3) | 24 | D4(3) | G₄.₄ |
   | *197* | *I23 (control, not in list)* | 23I | (7, 3) | 8 | A4(3) | G₁₂.₃ |

5. **Resolution** [deduction from checked hypotheses, §5]: for every one of the 14, `A_τ/G` has a
   projective crepant resolution `Y_τ = G-Hilb(A_τ)` (Bridgeland–King–Reid, Theorem 1.2), a smooth
   projective threefold with `K_Y ≅ O_Y`, `h^{1,0} = h^{2,0} = 0`, `h^{3,0} = 1` and the Hodge numbers
   of the table (Yasuda, Theorem 1.5; equivalently Batyrev, Theorems 3.8 and 7.5). These numbers do not
   depend on τ, on the origin, on the setting or on the primitive basis (§1). `Y_τ` is simply
   connected, hence a strict Calabi–Yau threefold, by a further deduction relying on two theorems not
   re-read here (Armstrong; Kollár/Takayama), §5.3.
6. **Identification with previously studied families** [verified for the Kummer papers, open
   otherwise]: each `Y_τ` is, by construction and by item 3, the Kummer threefold `Kum₃(E_τ, G)` of
   Andreatta–Wiśniewski/Donten-Bury/Burek for the matched Z-class — an identification of the full
   action, not only of Hodge numbers. No identification with any other named family (toric, complete
   intersection, string-theory orbifold tables) was attempted in this stage. None of the 14 is of type A
   or type K in the sense of Hashimoto–Kanazawa (those require infinite `π₁`; deduction of item 5).
7. **Fourteen labels, at most ten Hodge pairs** (§6): the 14 groups realise only 10 distinct pairs
   `(h^{1,1}, h^{2,1})`; two dual pairs of Z-classes lie inside the list (P312/P321 and F432/I432) and
   give equal Hodge numbers although their actions are provably inequivalent. Whether the corresponding
   threefolds are isomorphic or deformation equivalent is **open** (Donten-Bury's question) and was not
   pursued here.

## 1. The construction, made precise

Let Γ be one of the 14 space groups in its ITA standard setting, Λ ⊂ R³ its full translation lattice
(conventional cell plus centring vectors; a primitive Z-basis `B` is recorded for each group in
`output/crystallographic_data.json`), and `G = Γ/Λ` its point group, of order 4, 6, 8, 12 or 24. In the
basis `B`, `G` is a finite subgroup `ρ(G) ⊂ SL(3,Z)` (all 14 groups are Sohncke groups, so
`det = +1`). For `Im τ > 0` put

    L_τ = Λ + τΛ ⊂ C³ = R³ ⊗ C,    A_τ = C³ / L_τ .

**Well-definedness** [verified in the code, trivial]: since `τ ∉ R`, `Λ ⊕ Λ → C³`, `(λ, μ) ↦ λ + τμ`
is injective with discrete image, so `L_τ` is a lattice of rank 6 and `A_τ` is a complex torus; as
`A_τ ≅ E_τ ⊗_Z Λ ≅ E_τ³` (`E_τ = C/(Z + τZ)`), it is an abelian variety. A real matrix `M ∈ ρ(G)`
preserves `Λ`, hence `L_τ` (`M(λ + τμ) = Mλ + τMμ`), so the complex-linear extension of `x ↦ Mx`
descends to `A_τ`; on `H₁(A_τ, Z) = L_τ ≅ Λ ⊕ Λ` it acts by `ρ(M) ⊕ ρ(M)`. An affine element
`x ↦ Mx + b` descends to `A_τ` as well; for the 14 groups all translation parts `b` lie in `Λ` at the
ITA origin [verified], so the induced action of `Γ/Λ` on `A_τ` is the *linear* action of `ρ(G)` and
the quotient is `A_τ/ρ(G)`.

**What depends on the choices.**
* *Origin.* Moving the origin to `o` replaces `b` by `b + (M − 1)o`; the induced actions on `A_τ` are
  conjugate by the translation by `o`, so the quotient does not change. For a non-symmorphic Γ no origin
  makes all `b` lattice vectors, and the translation parts genuinely matter (§8).
* *Setting and primitive basis.* A change of primitive basis conjugates `ρ` in `GL(3,Z)`; the quotient
  `A_τ/G` is unchanged (the identity of `C³` intertwines). Control: the rhombohedral-axes setting of R32
  gives a point group conjugate to the hexagonal-axes one by
  `P = [[1,−2,1],[0,1,−1],[−1,1,−1]]`, with the same Hodge numbers [verified].
* *τ.* Every quantity computed here (fixed loci, centraliser actions, ages, invariant cohomology,
  Hodge and Euler numbers, `π₁(A_τ/G)`) is determined by the integral data `(Λ, ρ)` alone and is
  independent of τ. The isomorphism class of `Y_τ` does depend on τ (the fixed curves are isomorphic to
  quotients of `E_τ`); the question whether all `Y_τ` lie in one deformation family was not analysed.
* *Point group alone.* Not sufficient: the four arithmetic classes 222P, 222C, 222F, 222I have the same
  abstract point group and give four inequivalent actions with Hodge numbers (51,3), (21,9), (15,3),
  (15,3).

Because the 14 groups are symmorphic, "the space group Γ" and "the arithmetic crystal class of Γ"
carry the same information here: a symmorphic Sohncke group is `Λ ⋊ G`, determined up to affine
conjugacy by the `GL(3,Z)`-class of `ρ(G)`.

## 2. Data provenance [verified]

* **Generators.** Two independent implementations of the ITA standard settings were used: the
  Hall-symbol database of spglib 2.7.0 (column convention `x ↦ Rx + t`) and the GAP packages
  Cryst 4.1.27 / CrystCat 1.1.10 (row convention, converted by transposition). For each of the 37
  groups processed (35 + 2 controls) the group of cosets generated by the Cryst generators, reduced to a
  primitive basis of Λ and modulo Λ, equals the spglib coset set (`output/crystallographic_data.json`,
  field `spglib_vs_crystcat_cosets_agree`). The Bilbao server was not machine-readable on the run date
  (`SOURCES.md` B.5).
* **Lattice bases.** Λ is generated by the conventional basis and the centring vectors read from the
  database (R = 1 operations). Primitive bases (columns in conventional coordinates):
  P: identity; C: `(½,½,0), (0,1,0), (0,0,1)`; F: `(½,0,½), (0,½,½), (0,0,1)`;
  I: `(½,½,½), (0,1,0), (0,0,1)`; R (hexagonal axes): `(⅓,⅔,⅔), (0,1,0), (0,0,1)`.
* **Origins.** ITA standard origin (as stored in both databases). Symmorphic status was tested at this
  origin: all translation parts vanish modulo Λ for the 14 (and for 23, 197); for the 21 others at
  least one coset has a non-zero translation part in the database (and CrystCat reports
  non-symmorphic); no origin search was needed for the 14.
* **Point-group matrices** in the primitive basis, with translation parts, for all 35 groups:
  `table/space_groups_35.tsv` (column `generators_primitive_basis`) and
  `output/crystallographic_data.json`.

## 3. Identification with the published matrix classes [verified with certificates]

For each group, `ρ(G)` (primitive basis, column convention) was compared with every Donten-Bury
Table 1 class and every Burek group of the same order: all isomorphisms `φ: ρ(G) → H` were
enumerated, the Z-module of intertwiners `{P : P g = φ(g) P}` computed exactly (Smith normal form),
and a unimodular element searched. The certificates `P` (with `P ρ(G) P⁻¹ = H` as sets, verified by
direct multiplication) are in `output/zclass_matching.json`; those for Donten-Bury's representatives are:

| ITA | class | `P` (rows) | ITA | class | `P` (rows) |
|---|---|---|---|---|---|
| 16 | D4(1) | (0,−1,0; −1,0,0; 0,0,−1) | 177 | D12 | (1,0,0; 1,−1,0; 0,0,−1) |
| 21 | D4(2) | (0,−1,0; −1,−1,0; 0,0,−1) | 195 | A4(1) | (−1,0,0; 0,0,1; 0,−1,0) |
| 22 | D4(4) | (0,1,1; 0,0,−1; −1,−1,−1) | 196 | A4(2) | (0,0,−1; −1,−1,−1; 0,1,1) |
| 89 | D8(1) | (0,1,0; 0,0,−1; −1,0,0) | 207 | S4(1) | (1,0,0; 0,1,0; 0,0,−1) |
| 97 | D8(2) | (0,1,−1; 0,0,1; −1,−1,−1) | 209 | S4(2) | (−1,0,−1; 0,0,1; 0,−1,−1) |
| 149 | D6(2) | (−1,0,0; −1,1,0; 0,0,−1) | 211 | S4(3) | (0,1,0; −1,0,−1; 0,1,−1) |
| 150 | D6(1) | (−1,1,0; 0,−1,0; 0,0,−1) | 23 | D4(3) | (0,−1,1; 0,0,−1; −1,0,−1) |
| 155 | D6(3) | (−1,−1,−1; 1,0,1; 0,−1,1) | 197 | A4(3) | (0,0,−1; −1,−1,−1; 0,−1,0) |

Here `ρ(G)` is the group listed under `generators_primitive_basis` in the table (for instance
F432: `ρ(G) = ⟨(0,−1,0; 1,0,0; 0,1,1), (1,1,2; 0,1,0; −1,−1,−1)⟩`).

Consistency controls:
* *Convention.* The transposed group `ρ(G)ᵀ` is conjugate exactly to the *dual* class of
  Donten-Bury's duality proposition in all 16 cases (e.g. F222ᵀ ↔ D4(3), P312ᵀ ↔ D6(1),
  F432ᵀ ↔ S4(3)); this pins down the column convention used by the two papers and shows that the
  choice of convention matters precisely for the four dual pairs.
* *Two publications.* The direct identification Donten-Bury → Burek (same method) is
  D4(1)→G₄.₁, D4(2)→G₄.₂, D4(3)→G₄.₄, D4(4)→G₄.₃, D6(1)→G₆.₂, D6(2)→G₆.₁, D6(3)→G₆.₃, D8(1)→G₈.₁,
  D8(2)→G₈.₂, D12→G₁₂.₁, A4(1)→G₁₂.₂, A4(2)→G₁₂.₄, A4(3)→G₁₂.₃, S4(1)→G₂₄.₁, S4(2)→G₂₄.₃,
  S4(3)→G₂₄.₂, and it is compatible with the space-group route in all 16 cases.
* *Completeness and non-conjugacy* [verified independently of the published classification]. The 16
  symmorphic Sohncke groups with non-cyclic point group hit each of the 16 classes exactly once. Their
  pairwise non-conjugacy was certified here: 119 of the 120 pairs are separated by
  `GL(3,Z)`-invariants (per-class orders, class sizes, centraliser orders, invariant factors of `g − 1`
  on `L`, orbit counts; the index `[Λ : Σ_{g≠1} Λ^g]` of the lattice spanned by the rotation axes;
  the index `[Λ : S_Λ]` of §5.3), and the pair F432/I432, whose invariants coincide, by the exhaustive
  intertwiner search (for the irreducible 3-dimensional representations of S₄ every intertwiner module
  has rank ≤ 1, so the search is complete). For 222 the intertwiner modules have rank 3, for
  422/32/622 rank 2; there the box search only produces certificates, never proofs, and the invariants
  carry the non-conjugacy. This recovers Donten-Bury's classification theorem for these 16 classes.

## 4. Hodge numbers [verified]

### 4.1 Formula used

For `g ∈ G` let `A^g ⊂ A_τ` be its fixed locus, `C(g)` its centraliser and `age(g) = Σ αᵢ` where
`e^{2πiαᵢ}`, `αᵢ ∈ [0,1)`, are the eigenvalues of `ρ(g)` on `C³`. The orbifold Hodge numbers of
`[A_τ/G]` are

    h^{p,q}_orb = Σ_{[g]} Σ_{[W]} h^{p−age(g), q−age(g)}( W / C(g,W) ),

the inner sum over the `C(g)`-orbits of connected components `W` of `A^g`, `C(g,W)` the stabiliser of
`W` (Batyrev's `E_orb`, §7 of arXiv:math/9803071; Yasuda's Theorem 3.15; Chen–Ruan). Facts used, all
verified in the code for each group:
* every `g ≠ 1` is a rotation with eigenvalues `1, e^{iθ}, e^{−iθ}`, so `age(g) = 1`, and its fixed
  line in `Λ` has rank 1;
* `A^g = {x : (g−1)x ∈ L_τ}` is a disjoint union of translates of the one-dimensional subtorus
  `ker(g−1)/(L_τ ∩ ker(g−1))`, each an elliptic curve; the components are indexed by the torsion of
  `L_τ/(g−1)L_τ`, computed by the Smith normal form of `(ρ(g)−1) ⊕ (ρ(g)−1)` on `L_τ ≅ Λ ⊕ Λ`
  (number of components = product of the invariant factors: 16 = 2·2·2·2, 4 = 2·2, 9 = 3·3 or 1);
* `h ∈ C(g)` permutes the components (computed on explicit rational representatives) and acts on a
  component it preserves by an affine map whose linear part is the eigenvalue `χ_g(h) = ±1` of `ρ(h)` on
  the rotation axis of `g`; hence `H^{0,0}(W/C(g,W)) = C` always, and `H^{1,0}(W/C(g,W)) = C` iff
  `χ_g ≡ 1` on `C(g,W)` (the quotient curve is then elliptic; otherwise it is `P¹`);
* untwisted sector: `h^{p,q}(A_τ)^G = dim(Λ^pρ ⊗ Λ^qρ)^G` by characters; for `ρ ⊂ SO(3)` one has
  `Λ²ρ ≅ ρ`, so `h^{1,1}(A)^G = h^{2,1}(A)^G = |G|⁻¹ Σ_g tr ρ(g)²`, and `h^{1,0}(A)^G = h^{2,0}(A)^G =
  |G|⁻¹ Σ_g tr ρ(g) = 0`, `h^{3,0} = 1`.

Therefore `h^{1,1}_orb = h^{1,1}(A)^G + Σ_{[g]≠1} #orbits`, `h^{2,1}_orb = h^{2,1}(A)^G + Σ_{[g]≠1}
#(orbits with elliptic quotient)`, and `h^{1,0}_orb = h^{2,0}_orb = 0`.

### 4.2 Results by conjugacy class

Per non-trivial class: order of g · class size · centraliser order → components → `C(g)`-orbits
(of which elliptic). Full details, including orbit sizes and stabiliser orders, are in
`output/hodge_numbers_linear.json`.

| group | untwisted (h^{1,1},h^{2,1}) | twisted sectors | total |
|---|---|---|---|
| P222 | (3,3) | 2·1·4 → 16 → 16 (0), three times | (51,3) |
| C222 | (3,3) | 2·1·4 → 16 → 10 (6); 2·1·4 → 4 → 4 (0), twice | (21,9) |
| F222 | (3,3) | 2·1·4 → 4 → 4 (0), three times | (15,3) |
| P422 | (2,2) | 4·2·4 → 4 → 4 (4); 2·1·8 → 16 → 10 (0); 2·2·4 → 16 → 16 (0); 2·2·4 → 4 → 4 (0) | (36,6) |
| I422 | (2,2) | 4·2·4 → 1 → 1 (1); 2·1·8 → 4 → 4 (0); 2·2·4 → 4 → 4 (0), twice | (15,3) |
| P312 | (2,2) | 3·2·3 → 9 → 9 (9); 2·3·2 → 4 → 4 (4) | (15,15) |
| P321 | (2,2) | 3·2·3 → 9 → 9 (9); 2·3·2 → 4 → 4 (4) | (15,15) |
| R32 | (2,2) | 3·2·3 → 1 → 1 (1); 2·3·2 → 4 → 4 (4) | (7,7) |
| P622 | (2,2) | 6·2·6 → 1 → 1 (1); 3·2·6 → 9 → 5 (5); 2·1·12 → 16 → 5 (1); 2·3·4 → 4 → 4 (0), twice | (21,9) |
| P23 | (1,1) | 2·3·4 → 16 → 16 (0); 3·4·3 → 1 → 1 (1), twice | (19,3) |
| F23 | (1,1) | 2·3·4 → 4 → 4 (0); 3·4·3 → 1 → 1 (1), twice | (7,3) |
| P432 | (1,1) | 4·6·4 → 4 → 4 (4); 2·3·8 → 16 → 10 (0); 2·6·4 → 4 → 4 (0); 3·8·3 → 1 → 1 (1) | (20,6) |
| F432 | (1,1) | 4·6·4 → 1 → 1 (1); 2·3·8 → 4 → 4 (0); 2·6·4 → 4 → 4 (0); 3·8·3 → 1 → 1 (1) | (11,3) |
| I432 | (1,1) | same data as F432 | (11,3) |

### 4.3 Consistency checks

* **Literature** [published values, transcribed by parsing the sources]: Donten-Bury's Table 2
  (Poincaré polynomials `1 + b₂t² + b₃t³ + b₂t⁴ + t⁶`, read as `h^{1,1} = b₂`, `h^{2,1} = (b₃−2)/2`,
  valid because `h^{1,0} = h^{2,0} = 0`) and Burek's `(h^{1,1}, h^{2,1})` agree with the computed values
  in all 16 cases; Andreatta–Wiśniewski's `t⁶+20t⁴+14t³+20t²+1` for the octahedral S₄ agrees with
  P432. Burek's worked decomposition for G₂₄.₁, `h^{1,1} = 1+4+1+4+10`, `h^{2,1} = 1+0+1+4+0`, is the
  P432 row above up to the order of the classes.
* **Euler number** [verified, independent bookkeeping]: `e = 2(h^{1,1} − h^{2,1})` equals the
  orbifold Euler number `|G|⁻¹ Σ_{gh=hg} e(A^g ∩ A^h)` computed from the counts of common fixed
  points of the commuting pairs generating non-cyclic subgroups (products of invariant factors of the
  stacked matrices `(k−1)_{k∈⟨g,h⟩}`), for all 16 groups.
* **Classical values**: P222 is the standard `T⁶/(Z₂×Z₂)` orbifold with (51,3).
* **Per-class data vs. Burek** (spot checks, P432 and P622): centraliser orders and component counts
  agree. One intermediate row of Donten-Bury's D12 table lists the images in `Y` of the 16 fixed curves
  of the central involution as "3×P¹ + 1×A", whereas the `G`-orbit decomposition computed here is
  `1 + 3 + 3 + 3 + 6` (five curves: four `P¹` and one elliptic; the free orbit of size 6 has stabiliser
  `⟨z⟩` acting trivially on the curve). The totals of both papers agree with ours, so nothing depends on
  this; it is recorded in `OPEN_QUESTIONS.md` as unreconciled.

## 5. From orbifold Hodge numbers to a smooth projective Calabi–Yau threefold [deduction]

### 5.1 Existence of a projective crepant resolution
Bridgeland–King–Reid, Theorem 1.2 (arXiv:math/9908027): for a non-singular quasi-projective complex
variety `M` of dimension `n ≤ 3` and a finite `G ⊂ Aut(M)` such that `ω_M` is locally trivial as a
`G`-sheaf, `G-Hilb(M)` is irreducible and is a crepant resolution of `M/G`. Hypotheses checked: `M =
A_τ` is a projective abelian threefold; `ρ(G)` acts faithfully by group automorphisms; `ω_A` is
trivialised by `dz₁∧dz₂∧dz₃`, on which `g` acts by `det ρ(g) = 1` [verified for every element], so
`ω_A ≅ O_A` as `G`-sheaves. Hence `Y_τ := G-Hilb(A_τ) → X_τ := A_τ/G` is a crepant resolution;
`Y_τ` is projective (closed in the Hilbert scheme of `|G|` points of the projective `A_τ`), and
`K_{Y_τ} = π^*K_{X_τ} = 0` because the `G`-invariant volume form descends to `X_τ`. Crepant
resolutions of `X_τ` are not unique (Andreatta–Wiśniewski exhibit two toric models over the `Z₂×Z₂`
points differing by a flop); all have the same Hodge numbers by 5.2.

### 5.2 Hodge numbers of the resolution
Yasuda, Theorem 1.5 (= Corollary 3.16, arXiv:math/0110228): if `X, X′` are complete varieties with
Gorenstein quotient singularities and `Z → X`, `Z → X′` are proper birational with `K_{Z/X} =
K_{Z/X′}`, the orbifold cohomologies of `X` and `X′` have the same Hodge structures. Hypotheses
checked: `X_τ = A_τ/G` is complete; at a point with stabiliser `G_x` it is locally `C³/G_x` with
`G_x ⊂ SL(3,C)` (tangent action through `ρ`), so its singularities are Gorenstein quotient
singularities; `X′ = Z = Y_τ` is smooth with `K_{Y/X} = 0 = K_{Y/Y}`. Hence `H^*(Y_τ)` has the Hodge
numbers of §4 (for a smooth `X′` its orbifold cohomology is its cohomology). The same conclusion
follows from Batyrev's Theorem 7.5 (`E_st(X, Δ_X) = E_orb(A_τ, G)`, with `Δ_X = 0` since no element of
`ρ(G)` fixes a divisor — no non-trivial element of `SL(3,C)` of finite order is a pseudo-reflection)
together with his Theorem 3.8 (`E_st(X) = E(Y)` for a crepant resolution). Consequences:
`h^{1,0}(Y_τ) = h^{2,0}(Y_τ) = 0`, `h^{3,0} = 1`, so `H¹(Y_τ, O) = H²(Y_τ, O) = 0` and `Y_τ` is a
Calabi–Yau threefold in the sense of Hashimoto–Kanazawa's definition; since `h^{2,0} = 0`, the Picard
number of `Y_τ` equals `h^{1,1}` for every τ.

### 5.3 Fundamental group [deduction; two cited theorems not re-read]
By Armstrong's theorem `π₁(A_τ/G) ≅ Γ_τ/N`, where `Γ_τ = L_τ ⋊ G` acts on `C³` and `N` is the normal
subgroup generated by the elements with fixed points. An element `(g, ℓ)`, `g ≠ 1`, has a fixed point
iff `ℓ ∈ S_g := L_τ ∩ (g−1)R⁶` (the saturation of `(g−1)L_τ`); products `(g,s)(g,s′)⁻¹ = (1, s−s′)`
show `N ⊇ S := Σ_{g≠1} S_g`, and modulo `S` the group `G = {(g,0)}` is normal in `(L_τ/S) ⋊ G`
(conjugation by a translation changes `(g,0)` by `(g−1)ℓ ∈ S`), so `π₁(A_τ/G) ≅ L_τ/S ≅ (Λ/S_Λ)²`.
Computed [verified]: `S_Λ = Λ` for all 14 groups, i.e. `A_τ/G` is simply connected; for the two
controls `[Λ : S_Λ] = 2`, i.e. `π₁(A_τ/G) ≅ (Z/2)²` for I222 and I23. A resolution of a normal variety
with quotient singularities has the same fundamental group as the variety (Kollár 1993, Thm 7.8;
Takayama 2003 for log-terminal singularities), so the 14 threefolds `Y_τ` are simply connected — strict
Calabi–Yau threefolds — and in particular neither of type A nor of type K (Hashimoto–Kanazawa require an
infinite fundamental group). This paragraph is the only place where results not re-read in this run are
used; the rest of the report does not depend on it.

## 6. Equivalent inputs and the count of families

* Inputs that give the same construction: any two symmorphic Sohncke groups in the same arithmetic
  class (there is exactly one per class), any origin, any setting or primitive basis (§1).
* Inputs that provably differ but give equal Hodge numbers: the dual pairs P312/P321 (149/150,
  classes D6(2)/D6(1)) and F432/I432 (209/211, classes S4(2)/S4(3)) inside the list, and the dual
  partners F222/I222, F23/I23 with one member outside the list; also the non-dual coincidences
  C222 (21,9) = P622 (21,9) and F222 (15,3) = I422 (15,3). Donten-Bury proves that the *quotients*
  `A³/G` of non-conjugate classes have different singular-locus structure (e.g. D4(3) versus D4(4)) but
  leaves the isomorphism/deformation question for the resolutions open; it is open here as well.
* Hence the 14 labels give 10 distinct Hodge pairs and between 10 and 14 deformation families; the
  35 labels certainly do not correspond to 35 distinct families.

## 7. Failed or unresolved checks in this stage

* Bilbao GENPOS could not be read programmatically; two other ITA-derived databases were used and
  agree (no mathematical consequence).
* The intermediate D12 table row of Donten-Bury (4 versus 5 quotient curves) is unreconciled; totals
  agree.
* Non-conjugacy of Z-classes with intertwiner modules of rank 2 or 3 is established by invariants, not
  by the intertwiner search (which is complete only for rank ≤ 1).
* `π₁` statements (5.3) rely on Armstrong and Kollár/Takayama, not re-read in this run.
* No literature identification beyond the three Kummer papers; the six-dimensional toroidal-orbifold
  classification (Fischer–Ratz–Torrado–Vaudrevange) has not been matched (their Z-classes are
  six-dimensional; the lattice `Λ ⊕ Λ` with diagonal action must be located among them).
* Deformation equivalence between different groups with equal Hodge numbers: open.

## 8. The 21 pending groups — what stage 2 needs

Groups 17, 24, 90, 91, 93, 95, 98, 151, 153, 178–182, 198, 199, 208, 210, 212, 213, 214 (all
non-symmorphic in both databases; their generators with translation parts are in the table). Their
individual literature searches and affine-action computations were deferred. Required:

*Code (extension of `sgcy3.py`, all exact).* (i) Fixed loci of affine maps `x ↦ Mx + b` on `A_τ`: the
equation `(M−1)x ≡ −b (mod L_τ)` has solutions iff `b ∈ L_τ + (M−1)R⁶` (a finite test via the Smith
normal form used already); if it has none the element acts freely and contributes no twisted sector;
otherwise the components form a torsor under the same finite group as in the linear case and explicit
rational representatives are obtained from one particular solution. (ii) The centraliser must be taken
in the finite group `Γ/L_τ` (pairs `(M,b)` modulo `L_τ`), its permutation of components computed with
the affine maps, and the stabiliser character `χ` read off the linear parts as before (translations act
trivially on the cohomology of a curve). (iii) The untwisted sector is unchanged (translations act
trivially on `H^*(A_τ)`); ages are unchanged (they depend on `M` only). (iv) The DHVW Euler check must
sum over commuting pairs of `Γ/L_τ`. (v) `π₁` via Armstrong now sees elements without fixed points; the
quotient may have infinite fundamental group, and if every non-trivial element acts freely `A_τ/G` is
already smooth (a hyperelliptic threefold, Calabi–Yau with infinite `π₁` — the type A situation).
Example showing that translations matter even for a fixed point group: for I2₁2₁2₁ (24) the screw
`x ↦ Mx + b` with `b = ½a` along the axis has fixed points on `A_τ` because `(½,½,½) ∈ Λ` supplies a
lattice vector with axis component `½`, while for P2₁2₁2₁ (19, not in the list) the same screw acts
freely.

*Mathematics.* (i) The theorem chain of §5 applies verbatim (BKR needs only `ω_A` `G`-equivariantly
trivial, which holds as the linear parts have determinant 1; Yasuda/Batyrev need only Gorenstein
quotient singularities), so a crepant projective resolution exists and its Hodge numbers are the
orbifold Hodge numbers; the strict Calabi–Yau property (`h^{1,0} = h^{2,0} = 0`) again follows from the
linear parts. (ii) For groups with freely acting elements the resolution may have infinite `π₁`; the
type A/K classification (Oguiso–Sakurai; Hashimoto–Kanazawa) and the classification of hyperelliptic
threefolds (Catanese–Demleitner) become the relevant literature. (iii) Matching against the
six-dimensional affine classes of Fischer–Ratz–Torrado–Vaudrevange (roto-translations) requires their
data files; the Z₂×Z₂ cases also appear in Donagi–Wendland and Förste et al. (iv) The topological
condition defining the 35-list (R³/Γ ≅ S³) plays no role in the complex construction; whether it has
any consequence for `Y_τ` is not known to us and no such claim is made.
