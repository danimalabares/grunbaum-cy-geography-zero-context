# Crystallographic quotients of `CP²`, vertex links, and Stanley–Reisner smoothings

Research run of 2026-09-11 … 2026-09-16 (Claude Fable 5.1, single run; see `README.md` for the one
reproduction command, `SOURCES.md` for citations and the search log, `OPEN_QUESTIONS.md` for what is
missing). Everything marked **verified** below was recomputed exactly in this directory (Python with
exact arithmetic, networkx VF2 isomorphism, Macaulay2 1.20 over `Q`); everything marked **cited** is
taken from the named source; **unresolved** cells are labelled as such. No smoothing and no Calabi–Yau
invariant of a `CP²₁₀` link is asserted.

## 1. Results first

1. **The six rows.** Theorem 1 of Kaneko–Tokunaga–Yoshida (Part II, p. 596) lists exactly the six groups
   `(2,1)₀, (3,1)₀, (4,1)₀, (6,1)₀, (4,2)₁, (3,3)₀`, and these are exactly the six rows of quotient type
   `(1,1,1)` in Table II of Part I (pp. 589–590) (**cited, checked against both tables**). The known
   `CP²₉` construction is the row `(3,3)₀`: Morin–Yoshida's group `Γ = L[h] ⋊ G₆` (Part I, §7, p. 107)
   is affinely conjugate to `(3,3)₀` at `τ = ω` by `D = diag(1,−1)` composed with the similarity
   `(ω²−ω)⁻¹`; the point group `G(3,3,2) = ⟨swap, diag(ω⁻¹,ω)⟩` is dihedral of order 6 with three
   reflections, i.e. `S₃` (**verified**, `scripts/verify_33_identification.py`). Kühnel's complex is
   `K̃/Γ` (Morin–Yoshida, Claim 2, p. 116) and is the unique admissible diagonalisation, up to a quarter
   turn, of the canonical prismatic decomposition of the crystal `T′×T/S₃` (Arnoux–Marin, Prop. 2, p. 179)
   (**cited**). Its vertex link is the Brückner–Grünbaum sphere and is **verified** to be isomorphic to the
   sphere of this repository's sphere problem (explicit relabelling in §4).
2. **The four rows `(m,1)₀`, `m = 2,3,4,6`, share one triangulation: Bagchi–Datta's `CP²₁₀`.** For each
   `m` an explicit `Γ`-invariant rectilinear triangulation `K̃_m` of `C²` was constructed whose quotient is
   a simplicial complex isomorphic to `CP²₁₀` (**verified** on a finite torus cover: invariance under
   generators of `Γ`, regularity of the action, injectivity of face orbits, exact isomorphism with
   relabelling; `scripts/lifts.py`, `output/lifts.json`, `data/lifts/`). The vertex set of `K̃_m` is the
   set of cone-point pairs (`m = 2`) or the cone-point pairs together with one free orbit of barycentres
   (`m = 3,4,6`), and these choices are vertex-minimal for a simplicial quotient (§3). The four lifts
   differ in the crystallographic marking of the ten vertices (`data/cp2_10_crystallographic_markings.tsv`).
   Counted once, the five rows therefore produce **two** triangulations: `CP²₉` and `CP²₁₀`.
3. **Row `(4,2)₁`: no compatible triangulation was located.** Three exact negative results: (a) the
   `CP²₁₀`-lift for `(2,1)₀` at `τ = i` is invariant under the extra diagonal half-period translation but
   not under the extra symmetry `diag(i,i)` of `(4,2)₁`, which induces a transposition of the four
   classes of `S²₄`, and no pure `Z₂`-symmetric subdivision of `S²₄×S²₄` admits a transposition
   (Bagchi–Datta, Theorem 1; automorphism group `A₄×Z₂`); (b) the `(4,1)₀`-lift `K̃₄`, which is invariant
   under a conjugate `H` of `(4,2)₁` of index 4 in `(4,1)₀`, has a quotient by `H` that is a Δ-complex
   with 19 vertices and 192 facets but **not** a simplicial complex (144 edge orbits on 129 distinct
   vertex pairs); (c) the vertex-minimal product cell structure for `H` (vertex set `E[2]×E[2]`, 9 orbits)
   has no admissible diagonalisation at all: a regular `H`-invariant diagonalisation would have exactly
   `6144/128 = 48` facets and 9 vertices, and Dehn–Sommerville with `χ = 3` forces `f₁ = 42 > 36`
   (`scripts/four_two_one_counting.py`); a capped constraint search (1000 invariant compatible
   diagonalisations, 45 h) found none with a simplicial quotient, consistent with the count.
4. **Links.** `CP²₉`: one vertex orbit, link the neighbourly Brückner–Grünbaum sphere
   `f = (8,28,40,20)`, `h = (1,4,10,4,1)`, `|Aut| = 6`. `CP²₁₀`: two vertex orbits under `Aut = A₄`, hence
   two link types, not isomorphic: at the four diagonal vertices `x_ii` a **neighbourly** 9-vertex sphere
   `L10a`, `f = (9,36,54,27)`, `h = (1,5,15,5,1)`, `|Aut| = 6`; at the six vertices `x_ij` a sphere `L10b`,
   `f = (9,31,44,22)`, `h = (1,5,10,5,1)`, `|Aut| = 2`. All links are certified PL 3-spheres by explicit
   bistellar sequences to `∂Δ⁴` (**verified**).
5. **Smoothings of the link SR schemes.** Row `(3,3)₀`: the degree-20 threefold `Proj k[ℳ] ⊂ P⁷` is the
   object of this repository's sphere problem; its smoothing is recorded there as PROVED within an
   explicitly stated trust boundary and not independently refereed (`PROOFS.md`, C05/C06), with
   `(h¹¹,h²¹) = (1,31)`, `c₂·H = 56`, `χ = −60` under that boundary. Rows `(m,1)₀`: **no published
   smoothing theorem, certificate or non-smoothability result exists for either `CP²₁₀` link** (search log
   in `SOURCES.md`); the only published smoothing theorems for SR schemes of 3-spheres concern the five
   7-vertex spheres (Fausk 2012, degrees 11–14). New partial deformation data were computed here
   (**verified**, exact over `Q`): `dim Hom_S(I,A)₀ = 126`, intrinsic `T¹₀ = 54`, `T²₀ = 63` for `L10a`;
   `135`, `63`, `21` for `L10b`; the `Aut`-invariant parts of `T²₀` are `11` and `11` (nonzero), so the
   equivariant unobstructedness argument used for the Grünbaum sphere (where the `S₃`-invariant `T²₀` is
   `0`, recomputed here) does **not** apply to either `CP²₁₀` link. Degrees and Hilbert polynomials are
   derived from the links; Hodge numbers and Euler characteristics for the `CP²₁₀` links are **unresolved**.

## 2. Five-case table

| row (KTY Thm 1) | point group, lattice | quotient map (KTY Thm 3) | associated triangulation of `CP²` | status of the triangulation | vertex orbits → links | link SR scheme (`Pⁿ⁻¹`, degree, Hilbert polynomial) | SR smoothing to a CY3 | CY3 invariants |
|---|---|---|---|---|---|---|---|---|
| `(2,1)₀` | `G(2,1,2) = C₂ ≀ S₂` (order 8), `L²(τ)`, any `τ` | `(℘(x)+℘(y) : ℘(x)℘(y) : 1)`; `E²/G ≅ Sym²(E/±1) ≅ Sym²P¹`; branch: 4 lines + conic tangent to each | **`CP²₁₀`** (Bagchi–Datta); lift `K̃₂`: grid triangulation of `(½L)²`-cells, vertex set `E[2]²` (16 points = all cone-point pairs), Bagchi–Datta subdivision pulled back | published triangulation + equivariant periodic decomposition **verified** here (descent, purity, isomorphism); vertex-minimal; unique up to the two isomorphic subdivisions of Bagchi–Datta Thm 1 | `Aut(CP²₁₀) = A₄`: `{x_ii}` (4, stabiliser order 8) → `L10a`; `{x_ij}` (6, stabiliser 4) → `L10b` | `L10a`: `P⁸`, degree 27, `(9/2)k³ + (9/2)k`; `L10b`: `P⁸`, degree 22, `(11/3)k³ + (16/3)k` | **not found** (no theorem, no certificate, no nonsmoothability proof); partial data: `T¹₀`, `T²₀` as in §5 | **unresolved**; if a smooth CY3 fibre existed: `L³ = 27`, `c₂·L = 54` (`L10a`); `L³ = 22`, `c₂·L = 64` (`L10b`); `h¹¹, h²¹, χ` unknown |
| `(3,1)₀` | `G(3,1,2) = C₃ ≀ S₂` (18), `L²(ζ)` | `(℘′(x)+℘′(y) : ℘′(x)℘′(y) : 1)`; `Sym²(E/C₃)`; branch: 3 lines + conic | **`CP²₁₀`** (same complex); lift `K̃₃`: fine hexagonal lattice on the three `ω`-fixed points with one `C₃`-orbit of triangles stellarly subdivided; vertex set `(F ∪ B)²`, `F` = 3 cone points, `B` = 3 barycentres | explicit new construction, **verified**; cone points alone give the improper `S²₃` (two triangles on the same three vertices), so a free orbit is forced; barycentric choice unique up to `−1` | same two orbits; markings: `x_ii` ∈ `{(p,p): p ∈ F}` (stab. 18) or `(b,b)` (stab. 2); `x_ij`: stab. 9, 3, 3 | as above | as above | as above |
| `(4,1)₀` | `G(4,1,2) = C₄ ≀ S₂` (32), `L²(i)` | `(℘²(x)+℘²(y) : ℘²(x)℘²(y) : 1)`; `Sym²(E/C₄)` | **`CP²₁₀`** (same complex); lift `K̃₄`: the eight triangles (centre `(1+i)/2`, corner, edge-midpoint) of the unit square with one `C₄`-orbit stellarly subdivided; vertex set `(E[2] ∪ B)²` | explicit new construction, **verified**; `E[2]` alone gives an improper quotient (two triangles on `{0, (1+i)/2, ½}`), the Union-Jack refinement gives a doubled edge; barycentric refinement forced | markings: `x_ii` with stab. 32, 32, 8, 2; `x_ij` with stab. 16, 8, 8, 4, 4, 2 | as above | as above | as above |
| `(6,1)₀` | `G(6,1,2) = C₆ ≀ S₂` (72), `L²(ζ)` | `(℘′²(x)+℘′²(y) : ℘′²(x)℘′²(y) : 1)`; `Sym²(E/C₆)` | **`CP²₁₀`** (same complex); lift `K̃₆`: fine hexagonal lattice on `{0,q,2q}` with the three half-periods inserted as midpoints of the edges not through `0`, one `C₆`-orbit of the twelve triangles stellarly subdivided; vertex set `(F ∪ E[2] ∪ B)²` | explicit new construction, **verified**; forced refinement as for `m = 3,4` | markings: `x_ii` with stab. 72, 18, 8, 2; `x_ij` with stab. 18, 12, 6, 6, 3, 2 | as above | as above | as above |
| `(4,2)₁` | `G(4,2,2)` (16), `L²(i) + Z·((1+i)/2)(1,1)` | `(U²:V²:W²)` composed with the `(2,1)₀` map at `τ = i` (`(2,1)₀ ◁ (4,2)₁`, quotient `(Z/2)²` acting by sign changes); branch: 6 lines (index 2) | **missing**: no compatible triangulation located (§3.4) | three exact negatives: the `CP²₁₀`-lift is not `diag(i,i)`-invariant; `K̃₄/H` (19 vertices, 192 facets) is not simplicial; the vertex-minimal product structure (9 special points) has no admissible diagonalisation (counting) | — | — | — | — |
| `(3,3)₀` (known) | `G(3,3,2) ≅ S₃` (6), `L(τ)(−1,1) + L(τ)(ζ²,ζ)` | lines through pairs of points of the plane cubic (Abel); `E²/S₃ = Sym³₀E ≅ P²`; branch: dual sextic of the cubic, 9 cusps | **`CP²₉`** (Kühnel–Banchoff) `= K̃/Γ` (Morin–Yoshida Claim 2); unique admissible diagonalisation of `T′×T/S₃` up to `C₄` (Arnoux–Marin Prop. 2) | published, **cited**; facet list and `Aut` of order 54 **verified**; conjugation `Γ ∼ (3,3)₀[τ=ω]` **verified** | one orbit (9 vertices, `Aut` order 54, stabiliser `S₃`) → Brückner–Grünbaum sphere `ℳ` | `P⁷`, degree 20, `(10/3)k³ + (14/3)k` | recorded in this repository as PROVED within a stated trust boundary (packet + independent audit), not refereed | `H³ = 20`, `c₂·H = 56`, `(h¹¹,h²¹) = (1,31)`, `ρ = 1`, `χ = −60` — all within that boundary (`PROOFS.md` GEO-003, C05) |

## 3. What "associated triangulation" means, and the choices made

A crystallographic quotient `X = C²/Γ` does not select a triangulation. Following Arnoux–Marin (§14) we
call a triangulation **associated with `Γ`** if it is the quotient `K̃/Γ` of a `Γ`-invariant rectilinear
triangulation `K̃` of `C²` such that (a) the action is *regular* (a simplex mapped to itself is fixed
pointwise), so that `|K̃/Γ| ≅ C²/Γ ≅ CP²` as topological spaces, and (b) `K̃/Γ` is a simplicial complex
(each simplex determined by its vertex set); Arnoux–Marin call such a subdivision of a `Γ`-invariant
cell decomposition an *admissible diagonalisation*. The vertex set is taken as small as possible: the
`Γ`-orbits of the points lying on two reflection lines of `Γ` (for `(3,3)₀` these are the 9 points
`L[f]/L[h]`, Morin–Yoshida p. 107; for `(m,1)₀` they are the pairs of cone points of `E/C_m`; for `(4,2)₁`
they form 9 orbits), enlarged by free orbits only when (b) fails otherwise. The four categories of the
task then read:

* `(3,3)₀`: *published triangulation from a specified equivariant periodic decomposition* (`K̃`,
  Morin–Yoshida §8; prismatic decomposition, Arnoux–Marin §14–15).
* `(2,1)₀`: *published triangulation* (`CP²₁₀`) whose *equivariant periodic lift is verified here*.
  Bagchi–Datta never mention lattices; the lift is new but forced (Theorem 1 of Bagchi–Datta).
* `(3,1)₀, (4,1)₀, (6,1)₀`: *explicit new constructions whose descent and simplicial structure are
  verified*; the abstract quotient is again `CP²₁₀`, the periodic decompositions upstairs differ.
* `(4,2)₁`: *missing construction*; only a homeomorphism `C²/(4,2)₁ ≅ CP²` is available, which does not
  establish geometric compatibility.

### 3.1 Why the `(m,1)₀` rows lead to `CP²₁₀`

For `m = 2,3,4,6`, `G(m,1,2) = (C_m × C_m) ⋊ S₂` acts factorwise on `E×E`, `E = C/L(τ_m)`, and the quotient
factors as `E×E → (E/C_m)×(E/C_m) → Sym²(E/C_m)`, `E/C_m ≅ S²` with cone points of orders `(2,2,2,2)`,
`(3,3,3)`, `(4,4,2)`, `(6,3,2)`. A `Γ`-invariant triangulation of `C²` refining the product of two
`C_m`-invariant, `L`-periodic triangulations of `C` descends to a subdivision of the cell complex
`S²_A × S²_A` (`S²_A` the quotient triangulation of `E`) that is invariant under the swap, and conversely
any such swap-invariant *pure* subdivision pulls back to a `Γ`-invariant rectilinear triangulation of
`C²` (the covering `E → E/C_m` is unbranched off the cone-point vertices, so each closed product cell
`Δ₂×Δ₂` lifts homeomorphically; a triangulation of a product of two Euclidean triangles by its own
vertices is rectilinear). For the quotient to be simplicial one needs `S²_A` itself simplicial:

* `m = 2`: `E[2]` with the grid triangulation of `½L` gives `E/±1 = S²₄` (**verified**);
* `m = 3`: the three fixed points with the fine hexagonal triangulation give the improper `S²₃`; adding the
  barycentres of one `C₃`-orbit of triangles gives `S²₄` (**verified**); by the count `f = (6,18,12)` this
  is the only possibility with one free orbit;
* `m = 4`: `E[2]` alone gives the improper `S²₃`, the Union Jack (`E[2]` + square centres) gives a
  4-vertex Δ-complex with a doubled edge (**checked by hand**, §3.2), the barycentric refinement of one
  `C₄`-orbit of the eight (centre, corner, midpoint) triangles gives `S²₄` (**verified**);
* `m = 6`: fixed points + half-periods give `S²₃`; one barycentric orbit gives `S²₄` (**verified**).

With `S²_A = S²₄` in all four cases, Bagchi–Datta's Theorem 1 (exactly two pure `Z₂`-symmetric
subdivisions of `S²₄×S²₄`, isomorphic) leaves `CP²₁₀` as the unique quotient; the two subdivisions are
exchanged by an odd permutation of the four classes, realised by a real-affine (`GL₂(Z)`) or, for
`m ≠ 2`, by an (anti)holomorphic symmetry of the marked data, so the marked models are equivalent up to
such symmetries. Everything in this paragraph was verified computationally in `scripts/lifts.py`: for each
`m` the finite cover `E_N×E_N` (`N = 2`) carries 6144, 13824, 24576, 55296 lifted 4-simplices; the
generators of `Γ_N = G(m,1,2) ⋉ (L/NL)²` (orders 128, 288, 512, 1152) preserve the facet set; every facet
has five pairwise distinct `Γ_N`-orbits of vertices (regularity); the numbers of face orbits and of
distinct orbit-images agree in every dimension (`(10,45,110,120,48)`), so the quotient is a simplicial
complex; VF2 gives an isomorphism with `CP²₁₀`. Sample lifted simplices have non-zero integer
determinants (rectilinear nondegeneracy).

### 3.2 Markings (which vertex of `CP²₁₀` is which special point)

Vertices `x_ii` are the diagonal points `(p,p)`, on the branch conic; vertices `x_ij` are the pairs
`(p,q)`, `p ≠ q`, on two branch lines. The stabiliser orders in `Γ` computed from orbit sizes
(`data/cp2_10_crystallographic_markings.tsv`):

| vertex | `(2,1)₀` | `(3,1)₀` | `(4,1)₀` | `(6,1)₀` |
|---|---|---|---|---|
| `x₁₁, x₂₂, x₃₃, x₄₄` | 8, 8, 8, 8 (`(p,p)`, `p ∈ E[2]`) | 18, 2, 18, 18 (`x₂₂ = (b,b)`, `b` a barycentre) | 32, 8, 2, 32 | 72, 8, 2, 18 |
| `x₁₂, x₁₃, x₁₄, x₂₃, x₂₄, x₃₄` | 4 each | 3, 9, 9, 3, 3, 9 | 8, 4, 16, 2, 8, 4 | 12, 6, 18, 2, 6, 3 |

For `m = 2` the marking is `Aut(CP²₁₀)`-homogeneous on each orbit (the normaliser acts on `E[2]` through
`V₄ ⊂ A₄`); for `m = 3,4,6` the marking breaks the `A₄`-symmetry (only the crystallographic, not the
combinatorial, symmetry distinguishes the vertices). The deck groups `Γ` are infinite crystallographic
groups; `Aut(CP²₁₀) = A₄` (order 12) and `Aut(L10a) ≅ S₃`, `Aut(L10b) ≅ Z/2` are the automorphism groups of
the finite complexes — three different objects.

### 3.3 The known row `(3,3)₀`

Morin–Yoshida define `Γ = L[h] ⋊ G₆`, `G₆ = ⟨diag(ω,ω²), −swap⟩` (p. 107), construct the rectilinear
`Γ″`-invariant triangulation `K̃` of `C²` from the real hyperplane arrangement `Σ = Γ″Π` (§8, with one
`Γ″`-invariant choice in the 3–3 cells, p. 116), and prove `K̃/Γ ≅ K` (Claim 2). Arnoux–Marin (§14–15) show
that the canonical weak prismatic decomposition of `T′×T/S₃` (six flat prisms on the nine `S₃`-fixed
points, the 3-torsion points) has exactly four admissible diagonalisations, all isomorphic to `K`
(Proposition 2), and none for the higher crystals `CPⁿ`, `n ≥ 3` (Proposition 1). Verified here: (i) the
conjugacy `Γ ∼ (3,3)₀[τ = ω]`; (ii) `K` regenerated from the `G₂₇`-orbits of `(12459)` and `(12456)`
equals the Kühnel–Banchoff table and the Chapoton–Manivel transcription; (iii) `f = (9,36,84,90,36)`,
3-neighbourly, `|Aut| = 54`, one vertex orbit, 36 minimal nonfaces (quartics), rational and mod-`p`
Betti numbers `(1,0,1,0,1)`; (iv) the link of every vertex is a PL 3-sphere with `f = (8,28,40,20)`,
all nine links isomorphic, and the link of vertex 9 is isomorphic to the packet's Grünbaum sphere via
`1↦8, 2↦5, 3↦2, 4↦1, 5↦7, 6↦3, 7↦6, 8↦4`.

### 3.4 The row `(4,2)₁`

Structure (KTY, proof of Theorem 3, p. 601): `(2,1)₀` with `τ = i` is normal of index 4 in `(4,2)₁`, the
quotient `(Z/2)²` acting on the `(2,1)₀`-plane by `diag(±1,±1,1)`, so `C²/(4,2)₁ = P²/(Z/2)² ≅ P²` via
`(U:V:W) ↦ (U²:V²:W²)`. On `P¹ = E/±1` with branch points `{0, ∞, 1, −1}` (harmonic, `j = 1728`) the two
extra generators act as `u ↦ −u` (from `diag(i,i)`) and `u ↦ −1/u` (from the translation `((1+i)/2,(1+i)/2)`),
i.e. as the permutations `(1 −1)` and `(0 ∞)(1 −1)` of the four cone points; the first is odd. Also
`(4,2)₁ = s·H·s⁻¹` with `s = (1+i)/2` and `H = G(4,2,2) ⋉ (((1−i)Z[i])² + Z(1,1)) ⊂ (4,1)₀`, index 4.
Results (**verified**, `output/lifts.json`, `output/four_two_one_counting.json`, `output/four_two_one_search.json`):

* the lift `K̃₂` (`τ = i`) is invariant under the diagonal half-period translations (they permute the classes
  of `S²₄` inside `V₄ ⊂ A₄`) but **not** under `diag(i,i)` or `diag(i,1)`; the induced class permutation is
  the transposition `(2 3)`; since `Aut((S²×S²)₁₆) = A₄×Z₂` contains no transposition (0 of the 12 odd index
  permutations are automorphisms) and Bagchi–Datta's two subdivisions are the only pure ones, no lift of
  `CP²₁₀` with vertex set `E[2]²` is `(4,2)₁`-invariant;
* `K̃₄` is `H`-invariant, but `K̃₄/H` has 19 vertex orbits and 192 facet orbits with 144 edge orbits on
  only 129 distinct vertex pairs (and 416 triangle orbits on 392 triples): a Δ-complex, not a simplicial
  complex; the same happens for `K̃₄/(2,1)₀` (21 vertices, 150 edge orbits on 130 pairs);
* the vertex-minimal `H`-invariant cell structure (product of two copies of the eight (centre, corner,
  midpoint) triangles, vertex set `E[2]×E[2]`, 9 vertex orbits, 1024 cells on the cover `Z²/12Z²`,
  `|H_N| = 128`) has 12 cell orbits with stabilisers of order 1 or 2; 13 of the 108 triangulations of
  `Δ₂×Δ₂` (all 108 enumerated and verified, `scripts/prism_triangulations.py`) are swap-invariant and
  pure. A regular invariant diagonalisation has `6144/128 = 48` facets on 9 vertices; a closed 9-vertex
  combinatorial 4-manifold with `χ = 3` and 48 facets would have `f₃ = 120`, `f₂ = 108` and `f₁ = 42 > 36`:
  **impossible**. The capped search over the 12 cell orbits found 1000 invariant compatible
  diagonalisations (all with 9 vertex orbits), none with a simplicial quotient — consistent with the count.

Hence any `(4,2)₁`-compatible triangulation must use additional free vertex orbits; the natural candidates
and the required checks are listed in `OPEN_QUESTIONS.md`.

## 4. Links: exact combinatorial data

`data/links/*.txt` contain the facets and minimal nonfaces (SR ideal generators). Isomorphisms were tested
with VF2 on facet–vertex incidence graphs; PL certificates are explicit bistellar sequences
(`output/links.json`, re-verified move by move).

| link | vertices, facets | f-vector | h-vector | `|Aut(link)|`, vertex orbits | stabiliser in `Aut(parent)` | minimal nonfaces (SR ideal) | PL certificate |
|---|---|---|---|---|---|---|---|
| `ℳ` = lk(9, `CP²₉`) | 8, 20 | (8,28,40,20) | (1,4,10,4,1) | 6; orbits `{1,2,3}`, `{4,5,6}`, `{7,8}` (link labels) | 6 (`S₃`) | 16 cubics (all 28 edges present; any two facets meet) | 9 moves |
| `L10a` = lk(`x₁₁`, `CP²₁₀`) | 9, 27 | (9,36,54,27) | (1,5,15,5,1) | 6; orbits of sizes 6, 3 | 3 | 30 cubics (neighbourly) | 14 moves |
| `L10b` = lk(`x₁₂`, `CP²₁₀`) | 9, 22 | (9,31,44,22) | (1,5,10,5,1) | 2; orbits 2,2,2,2,1 | 2 | 5 quadrics `x₃x₆, x₃x₉, x₄x₆, x₄x₇, x₇x₉` + 10 cubics | 9 moves |

`L10a` and `L10b` are not isomorphic (different f-vectors). All 10 links of `CP²₁₀` and all 9 of `CP²₉` were
certified PL spheres, so both complexes are combinatorial 4-manifolds; their rational and `F_p` (`p =
2,3,5,7`) Betti numbers are `(1,0,1,0,1)`, `χ = 3`. The identification with `CP²` is cited (Kühnel–Banchoff,
Morin–Yoshida, Bagchi–Datta 1994 for `CP²₉`; Bagchi–Datta 2010, Lemma 1 and Theorem 1, for `CP²₁₀`); for the
`(m,1)₀` lifts it also follows from regularity of the verified quotient construction.

## 5. Stanley–Reisner schemes of the links: Hilbert data and deformation data

All rings are `A = Q[x₁..x_n]/I_Δ`, Gorenstein of Krull dimension 4; `X = Proj A ⊂ Pⁿ⁻¹` is a degenerate
threefold of degree `f₃`. Hilbert polynomials are derived from the h-vectors,
`P(k) = Σ h_i C(k−i+3,3)` (Macaulay2 agrees).

| link | ambient | degree | Hilbert polynomial | `dim Hom_S(I,A)₀` | `gl_n`-orbit | intrinsic `T¹₀` | AC Thm 4.6/5.7 | `dim T²₀` | `Aut`-inv. `Hom₀` | `Aut`-inv. `T²₀` | genuine invariant intrinsic `T¹` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ℳ` (`P⁷`) | `P⁷` | 20 | `(10/3)k³ + (14/3)k` | 109 | 56 | 53 | 53 | 27 | 21 | **0** | 10 |
| `L10a` | `P⁸` | 27 | `(9/2)k³ + (9/2)k` | 126 | 72 | 54 | 54 | 63 | 21 | 11 | 9 |
| `L10b` | `P⁸` | 22 | `(11/3)k³ + (16/3)k` | 135 | 72 | 63 | 63 | 21 | 68 | 11 | 32 |

Notes. (i) The `ℳ` row reproduces the sphere-problem inputs of this repository independently: 109 and 56
(`PROOFS.md` DEF-001/002), 53 intrinsic directions in ten `S₃`-orbits (DEF-003: "ten `S₃`-orbits", here
10 genuine invariant intrinsic directions), 27 degree-two obstruction coordinates (PROOF.md §2), and the
hypothesis `(T²₀)^{S₃} = 0` of the packet's equivariant lifting lemma (accepted in D04) — recomputed here
as `0`. (ii) For the `CP²₁₀` links the invariant obstruction spaces are nonzero, so no equivariant
unobstructedness statement is available; `T²₀ ≠ 0` does not prove obstructedness. (iii) For the fourfold
`Proj k[CP²₁₀] ⊂ P⁹` (non-Cohen–Macaulay, not a link): `dim Hom_S(I,A)₀ = 131`, `dim T²₀ = 180` (for
`CP²₉`: 93 and 126, `runs/cp2-nine-vertex-equivariant-t2-2026-09-09`). (iv) Corollary 5.8 of
Altmann–Christophersen (rigidity when all edge valencies are ≥ 5) does not apply: every link has edges of
valency 3 and 4 (`ℳ`: 7 and 9; `L10a`: 6 and 12; `L10b`: 6 and 13).

**Riemann–Roch reading.** If a smooth Calabi–Yau threefold `Y` with `L = O_Y(1)` lay in the same Hilbert
scheme as `X`, then `χ(O_Y(kL)) = P(k) = (L³/6)k³ + (c₂·L/12)k`, giving `c₂·L = 56, 54, 64` for
`ℳ, L10a, L10b`. For `ℳ` this is the recorded `c₂·H = 56` (GEO-003). For the `CP²₁₀` links no smooth fibre is
known, so these two numbers are conditional readings, not invariants of an established threefold; `h¹¹`,
`h²¹` and `χ` are **unresolved** and are not inferred from the degree or the f-vector.

**Smoothing status by category** (task §Computations).

| link | published smoothing theorem | independently verified certificate | partial deformation computations | proven nonsmoothability |
|---|---|---|---|---|
| `ℳ` | none in the literature; the smoothing is a claim of the zero-context packet, PROVED within its trust boundary (this repository) | certificates re-run in this repository (`PROOFS.md` §1–§3), not refereed | complete first-order data, six-jet, all-orders equivariant lift (packet), fixed chart, ramified fibre (runs) | none |
| `L10a` | **not found** | none | `T¹₀ = 54`, `T²₀ = 63`, `(T²₀)^{S₃} = 11`, `Hom₀ = 126` (this run) | none |
| `L10b` | **not found** | none | `T¹₀ = 63`, `T²₀ = 21`, `(T²₀)^{Z₂} = 11`, `Hom₀ = 135` (this run) | none |

The only published smoothings of SR schemes of 3-spheres are Fausk's for the five 7-vertex spheres
(`P⁶`, degrees 12, 13, 14 smoothable to `(2,2,3)` complete intersections and Pfaffian CY3s with
`h²¹ = 73, 61, 50`; degree 11 not smoothable). A small resolution of a nodal fibre (Fausk's degree-11 case)
is not a smoothing; nothing of either kind is known for `L10a`, `L10b`.

## 6. Distinctions kept

* the `CP²` triangulation (`CP²₉`, `CP²₁₀`; 4-dimensional complexes) and its non-Cohen–Macaulay fourfold SR
  scheme in `P⁸`, `P⁹`;
* its 3-sphere links (`ℳ`, `L10a`, `L10b`) and their Gorenstein threefold SR schemes in `P⁷`, `P⁸`;
* the Kummer/K3^[2]-type fourfolds `Hilb²(E×E/C_m)^∼ → Sym²P¹` and `K₂(A) → P²` of Sawon over the same bases
  (context only; no statement about SR schemes);
* the crystallographic deck groups `Γ` (infinite) versus `Aut(CP²₉)` (54), `Aut(CP²₁₀)` (12), `Aut(ℳ)` (6),
  `Aut(L10a)` (6), `Aut(L10b)` (2).

## 7. Verification summary (what was checked, how)

* Six rows: read from KTY Part II Theorem 1 and Part I Table II; matched by type `(1,1,1)`.
* `(3,3)₀` identification: exact arithmetic in `Q(ω)` (`scripts/verify_33_identification.py`).
* `CP²₉`: two independent facet provenances (Kühnel–Banchoff table; Morin–Yoshida orbit description) agree
  with the stored Chapoton–Manivel transcription; all combinatorial invariants recomputed.
* `CP²₁₀`, `(S²×S²)₁₆`: regenerated from Bagchi–Datta's data; f-vectors, automorphism groups, the product-cell
  structure, geometric validity of each cell's 6 simplices (exact determinants, opposite-side and
  supporting-hyperplane tests), purity, quotient.
* Lifts `K̃_m`: finite-cover model with integer coordinates; invariance, regularity, face-orbit injectivity,
  isomorphism with `CP²₁₀`, stabiliser orders.
* Links: VF2 isomorphism classes, bistellar PL certificates (re-verified), Betti numbers over `Q` and `F_p`.
* Deformation data: Macaulay2 1.20 (`normalMatrix`, `CT^2`, Schlessinger's `T²` construction and the
  transport of relations copied from the repository's earlier run) and, independently, the combinatorial
  formulas of Altmann–Christophersen implemented from their Definition 4.4 (agreement 53/54/63).
* `(4,2)₁`: exact invariance tests, quotient analysis of `K̃₄/H`, enumeration of the 108 triangulations of
  `Δ₂×Δ₂`, counting obstruction, capped search.

Not done: independent refereeing of the sphere problem's smoothing; any smoothing attempt for `L10a`, `L10b`;
polytopality of `L10a`, `L10b`; a `(4,2)₁`-compatible triangulation with extra vertices (see
`OPEN_QUESTIONS.md`).
