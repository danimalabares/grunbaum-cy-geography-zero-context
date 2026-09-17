# Is the Grünbaum–Sreedharan smoothing Kapustka's degree-20 family?

Run date: 2026-09-17 (America/Sao_Paulo). Input commit of this repository:
`09953cefe987f304e1e8549a50df3b937747470c` (2026-09-16). Nothing outside this run
directory was modified; no status label of §1–§7 of `PROOFS.md` is changed.

**Question.** Does `SR(M) = Proj k[M] ⊂ P⁷`, `M` the Grünbaum–Sreedharan eight-vertex
3-sphere, admit a smoothing whose smooth fibres lie in the deformation family of the
degree-20 Calabi–Yau threefold of G. Kapustka, *Projections of del Pezzo surfaces and
Calabi–Yau threefolds*, Adv. Geom. 15 (2015) 143–158 = [arXiv:1010.3895v5](https://arxiv.org/abs/1010.3895),
Table 1 No. 8?

**Verdict: unresolved, reduced to one explicitly stated open property of Kapustka's
family, with a first-order obstruction to that property.** See §8. What *is* established
here is summarised first.

---

## 0. Summary of what is established in this run

| | Statement | Status |
|---|---|---|
| **A** | Kapustka's Table 1 rows 1–8 — node numbers, degrees `H³`, `h⁰(H)`, `c₂·H` and Euler numbers, including the doubling of rows 1/2 and 3/4 — are reproduced exactly from three closed formulas. Row 8 is the family built from `D = P¹×P¹` doubly projected into `P⁶`; it has 44 nodes, `H³ = 20`, `h⁰(H) = 8`, `c₂·H = 56`, `χ = −60`, `(h¹¹,h¹²) = (1,31)`. | **established** (`scripts/verify_kapustka_table1.py`, exact integer arithmetic) |
| **B** | The printed proof of Kapustka's Theorem 5.1 transposes the two cases: it attaches 37 nodes to `~~D₈ ⊂ P⁶` and 44 to `~D₇ ⊂ P⁶`, and the Hodge number 23 to degree 19. Table 1 and Appendix 1 of the same paper, the Betti table printed inside that proof, the Thom–Porteous count and the Macaulay2 computation of this run all give the opposite assignment. | **established** (§2, §3) |
| **C** | The projected surface `S = ~~D₈ ⊂ P⁶` has the Betti table printed in Kapustka's Theorem 5.1 (3 quadrics, 14 cubics, 53, 68, 43, 14, 2), and `h¹(I_S(1)) = 2`, `h¹(I_S(k)) = 0` otherwise. A general `(2,2,3)` complete intersection through it has exactly **44** singular points, a reduced zero-dimensional scheme. | **COMPUTER-CERTIFIED** (Macaulay2 1.20 over `F₃₂₀₀₃`; `logs/k01_surface.log`, `logs/k11_ci.log`) |
| **D** | The *polarised* model of Kapustka's family does **not** live in `P⁷`: the contracted threefold `Ybar` is normal Gorenstein with one singular point `P` which is `(3-fold ODP)/±`, of multiplicity 8 and **embedding dimension 9**. Hence `T` is not very ample on `Ybar`, and G. Kapustka's own Lemma 2.2 ([arXiv:0707.2488]) — the tool that produces arithmetically Gorenstein models in `P⁷` for the degree-17 and -18 members of exactly this family of constructions (and, in CGKK, for a different degree-19 construction) — is not applicable here. | **established** (§4) |
| **E** | The image `Y` of `Ybar` under the morphism defined by `T`, a threefold in `P⁷`, is the Kustin–Miller (type I) unprojection of `S ⊂ X'`; it is non-normal at `P` with δ-invariant `Σ_k h¹(I_S(k)) = 2`, has Hilbert polynomial `(10/3)n³ + (14/3)n − 2`, and lies on exactly two quadrics (cones with vertex `P`). In particular `[Y]` is **not** a point of the Hilbert scheme that contains `[SR(M)]`. | **established** (§4) |
| **F** | **Reduction.** Every smoothing of `SR(M)` — whether or not it is the zero-context one — is automatically an embedded smoothing inside `P⁷` whose smooth fibres are *arithmetically Gorenstein* Calabi–Yau threefolds of degree 20 with h-vector `(1,4,10,4,1)`. Consequently: *`SR(M)` has a smoothing with fibres in Kapustka's family ⟹ Kapustka's family contains an arithmetically Gorenstein member in `P⁷` ⟺ the general member `Y_t` satisfies `h⁰(I_{Y_t}(2)) = 0` and `T_t` very ample*. | **PROVED** (§5; uses only flatness, Hochster's formula and semicontinuity — no trust boundary) |
| **G** | No source in the literature asserts that property. Three papers of G. Kapustka and coauthors that enumerate arithmetically Gorenstein Calabi–Yau threefolds in `P⁷` omit this family: CGKK 2016 §4.9 states that in degree 20 "only one example is known" (the determinantal one, with `h¹¹ = 2`), and KKRSSY (Memoirs AMS 2026) leave the corresponding lifting problem open (their Question 8.5). | **established** (documented quotations in `SOURCES.md`) |
| **H** | Kapustka's smoothing families are indexed by the del Pezzo *threefolds* `V` of the same degree having the contracted del Pezzo surface `D` as a hyperplane section (Pinkham's sweeping out of the cone; Milnor fibre `V ∖ D`). For `deg D = 6` there are two (`P¹×P¹×P¹` and the flag threefold), which reproduces the paired rows 1/2 and 3/4 of Table 1 with their two Euler numbers; for `deg D = 8` there is exactly one (`V₈ = (P³, O(2))`), so **Kapustka's degree-20 family is irreducible** and the criterion in F is unambiguous. | **established** (numerically exact for rows 1–8; §2.4) |
| **I** | **First-order obstruction to (★).** Along any one-parameter deformation of the contracted threefold `Ybar` inside `P(1⁸,2²)`, the `2×2` matrix `C` of `y₁,y₂`-coefficients acquired by the two degree-2 equations has `rank C ≤ 1`; so no first-order deformation moves `Ybar` into a `P⁷`. Structural reason: `dim Λ − dim Λ₀ = 1` for the two spaces of §7.1. In the local model of the smoothing this persists to **all** orders, and the smooth fibre lies on exactly one quadric of `P⁷`. | **PROVED** first order (§7.2); all-orders statement holds in the local model (`scripts/verify_local_model.py`, exact) |

Not established: the property in F beyond first order; therefore neither "yes" nor
"no", although every piece of evidence points to "no". §8.3 states the next specific
obstacle (a second-order Kuranishi term on the explicit ideal shipped in
`data/IYbar.m2`).

---

## 1. Objects and notation

### 1.1 The sphere side

`M` is the eight-vertex triangulation of `S³` with the 16 minimal non-faces frozen in
`scripts/verify_geography.m2` of the repository root:

```
I_M = (abf, abg, abh, acg, ach, adh, bdf, bdg, beg,
       cde, ceg, ceh, cfh, def, dfh, efg)  ⊂  S = k[a,…,h].
```

`scripts/verify_sphere.py` recomputes from these generators: `f(M) = (8,28,40,20)`,
`M` neighbourly, every 2-face in exactly two facets, every vertex link a 2-sphere,
`H_*(M;Z) = H_*(S³;Z)`, h-vector `(1,4,10,4,1)`, Hilbert polynomial
`P(m) = (10/3)m³ + (14/3)m`, Hilbert function `1, 8, 36, 104, 232, …`. Every vertex of
`M` lies in exactly 10 facets. Write `X_M = SR(M) = Proj S/I_M ⊂ P⁷`; it is
arithmetically Gorenstein of degree 20 with `ω = O` (a-invariant 0) and minimal
resolution of Betti numbers `(1,16,30,16,1)` in shifts `(0,3,4,5,8)` (`PROOFS.md`
GEO-001).

The repository's smoothing (`PROOFS.md` C05/C06, within the accepted zero-context
trust boundary) has smooth fibres with
`(h¹¹,h¹²) = (1,31)`, `ρ = 1`, `χ = −60`, `H³ = 20`, `c₂·H = 56`, `h⁰(H) = 8`,
and a 94-dimensional smoothing component of `Hilb(P⁷)`.

### 1.2 The Kapustka side

Fix the notation of [arXiv:1010.3895v5]:

* `D = D₈ = P¹×P¹` anticanonically embedded by `−K_D = O(2,2)` in `P⁸` (`h⁰(−K_D) = 9`,
  `deg = 8`, `K_D² = 8`, `e(D) = 4`).
* `S = ~~D₈ ⊂ P⁶`: the image of `D` under projection from a general line of `P⁸`.
  The projection is an isomorphism onto its image because `dim Sec(D) = 5` and a general
  line of `P⁸` misses a 5-fold; so `S ≅ P¹×P¹`, `deg S = 8`, `O_S(1) = −K_S`.
* `X' ⊂ P⁶`: a general complete intersection of two quadrics and a cubic from `I_S`
  (Kapustka's `X'_{2,2,3}`). It is a Calabi–Yau threefold of degree 12 with 44 ordinary
  double points, all on `S`.
* `X'' = Bl_S X' → X'` is a small resolution (blowing up the Weil divisor `S`);
  `X` is the flop of its 44 exceptional curves, a smooth Calabi–Yau threefold with
  `ρ(X) = 2`, `Pic X = Z H* ⊕ Z D'`, where `D' ≅ D` is the strict transform of `S`.
* Because `K_X = 0`, adjunction gives `O_{D'}(D') = ω_{D'} = K_D`, while
  `H*|_{D'} = −K_D`; hence `G := H* + D'` restricts trivially to `D'`, and
  `φ = φ_{|G|} : X → Ybar` is the primitive type II contraction of `D'` to a point `P`
  (Kapustka Thm. 3.4/5.1, using Wilson and [RS]).
* `Ybar` is the *normal* contracted Calabi–Yau threefold; `T` denotes the ample class
  with `φ*T = G`. By Gross, *Deforming Calabi–Yau threefolds*, Math. Ann. 308 (1997),
  Theorem 5.8 ("`X` is smoothable unless `E ≅ P²` or `F₁`"), `Ybar` is smoothable;
  `Y_t` is a general smooth fibre and `K` denotes the resulting deformation family.

---

## 2. Independent verification of Table 1, and the identification of row 8

Three closed formulas suffice; all three are verified against every row of Kapustka's
Table 1 (and against Tables 1–5 of [arXiv:0707.2488]) in
`scripts/verify_kapustka_table1.py`.

### 2.1 The number of nodes (Thom–Porteous)

Let `S ⊂ Pⁿ` be a smooth surface whose ideal is generated in degree ≤ `min d_i`, and let
`X'` be a general complete intersection of `k = n−3` hypersurfaces of degrees
`d₁,…,d_k` from `I_S`. The differentials of the `k` defining forms give a map of bundles
on `S`

```
φ : ⊕_i O_S(−d_i) ⟶ N^∨_{S/Pⁿ}      (ranks k and n−2),
```

and `X'` is singular exactly where `φ` drops rank, a locus of expected codimension
`(k−(k−1))·((n−2)−(k−1)) = 2`. Thom–Porteous gives

```
#nodes = c₂(N_{S/Pⁿ} − ⊕_i O(d_i))
       = α(n; d) · deg S + K_S² − e(S),
   α(n; d) = C(n+1,2) − (n+1)e₁ + e₁² − e₂,   e₁ = Σ d_i,  e₂ = Σ_{i<j} d_i d_j.
```

For `n = 6`, `(d) = (2,2,3)`: `α = 21 − 49 + 49 − 16 = 5`, so

```
#nodes = 5·deg S + K_S² − e(S).
```

* `S = ~~D₈` (deg 8, `K² = 8`, `e = 4`):  `40 + 8 − 4 = 44`.
* `S = ~D₇`  (deg 7, `K² = 7`, `e = 5`):  `35 + 7 − 5 = 37`.

Table 1 attaches 44 ODP to the row with `deg D' = 8` and 37 ODP to the row with
`deg D' = 7`; the formula agrees with Table 1 and **disagrees with the "resp." ordering
printed inside the proof of Theorem 5.1**, which attaches 37 to `~~D₈`. The
Macaulay2 computation of §3 settles it independently: 44.

### 2.2 The degree and the multiplicity

`φ_{|G|}` contracts `D'` to `P`, and the linear subsystem of `|G| = |H* + D'|` having
`D'` as a fixed component is `D' + |H*|`, whose image is the projection of `φ(X)` from
`P`; that projection is `X' ⊂ P⁶` (Kapustka Prop. 3.2). Since the projection is
birational,

```
deg Ybar = deg X' + mult_P Ybar,      mult_P Ybar = (D'|_{D'})² = K_D² = deg D,
```

so `deg Ybar = deg X' + deg D`. Also `h⁰(G) = h⁰(H*) + 1 = (n+1) + 1`, because
`H⁰(G)/H⁰(H*) ↪ H⁰(D', G|_{D'}) = H⁰(D', O) = k` and `|G|` does not contain `D'` as a
fixed component. Riemann–Roch on a smooth fibre then fixes `c₂·H`:

```
h⁰(H) = H³/6 + c₂·H/12.
```

Row 8: `deg = 12 + 8 = 20`, `mult_P = 8`, `h⁰(H) = 8`, `c₂·H = 12(8 − 20/6) = 56`.

### 2.3 The Euler number

`χ(X) = χ(X_{d}) + 2k` for the small resolution of a `k`-nodal degeneration of a smooth
complete intersection `X_d` (each node costs 1 in the degeneration and gains 1 more in
the small resolution). Contracting `D'` gives `χ(Ybar) = χ(X) − χ(D) + 1`. Smoothing
replaces the singular point by the Milnor fibre `F`:

```
χ(Y_t) = χ(X) − 2χ(D) + χ(V),
```

using `χ(F) = χ(V) − χ(D)` from §2.4. With `χ(X_{2,2,3}⊂P⁶) = −144` (computed from
Chern classes in the script) and 44 nodes: `χ(X) = −56`, `χ(Ybar) = −59`,
`χ(Y_t) = −56 − 8 + 4 = −60`. With `h¹¹ = 1` (Kapustka Thm. 5.1) this gives
`h¹² = 31`.

### 2.4 Which del Pezzo, how many smoothings, and the local model

The germ `(Ybar, P)` has associated graded ring `⊕_{n≥0} H⁰(D, −nK_D)`, the
anticanonical cone over `D`. For `D = P¹×P¹` this cone is

```
C(D, −K_D) = { u² : u ∈ U, q(u) = 0 } ⊂ Sym²U ,   U ≅ k⁴ with P(U) = P³ ⊃ D = {q = 0},
```

i.e. the image of the affine quadric cone `{q = 0} ⊂ A⁴` — an ordinary double point —
under `u ↦ u²`, which is the quotient by the involution `±1`, free away from the origin.
(`D = P¹×P¹` is the quadric surface in `P(U) = P³` and `−K_D = O(2,2)` is the restriction
of `O_{P³}(2)`, so `v₂` embeds `D` into `P(Sym²U)` spanning the hyperplane `P(H₀)`.) Its `−1`-weight (Pinkham) deformations sweep out the cone:

```
W_t = { u² : q(u) = t }  ≅  { q = t } / ±1,
```

which is smooth for `t ≠ 0`; the Milnor fibre is `(S³)/± = RP³`, so `χ(F) = 0`. In
general the `−1`-weight smoothings of the cone over a del Pezzo surface `(D, −K_D)`
correspond to the *extensions* of `D`, i.e. to del Pezzo threefolds `V` with `D` a
hyperplane section, with `F ≅ V ∖ D` and `χ(F) = χ(V) − χ(D)`:

| `deg D` | `V` with `D` a hyperplane section | `χ(V)` | `χ(F)` | rows of Table 1 |
|---|---|---|---|---|
| 6 | `P¹×P¹×P¹`; flag threefold `W ⊂ P²×P²` | 8; 6 | 2; 0 | 1/2 and 3/4 (two Euler numbers each) |
| 7 | `Bl_pt P³` | 6 | 1 | 5, 7 |
| 8 | `(P³, O(2))` | 4 | 0 | 6, 8 |

That the degree-6 case has exactly two components is also Kapustka's own statement
([arXiv:0707.2488] Thm. 2.3: "the versal Kuranishi space of a cone over a del Pezzo
surface of degree 6 has two components") and the Tom/Jerry dichotomy of KKRSSY.
For `deg D = 8` the del Pezzo threefold of degree 8 is unique (`P³` with `O(2)`), so
**the degree-20 family `K` is irreducible** — consistent with Table 1 listing row 8
once. With these `χ(V)` the formula of §2.3 reproduces all eight Euler numbers of
Table 1 exactly (`logs/verify_kapustka_table1.log`).

### 2.5 The comparison is with a uniquely specified family

Appendix 1 of [arXiv:1010.3895v5] lists every Calabi–Yau threefold with
`h¹¹ = 1` known to the author. The degree-20 rows are

```
H³  h¹¹  h¹²   χ     c₂·H  h⁰(H)   source
20   1    31  −60     56     8     Table 1  (row 8 — the comparison family)
20   1    61 −120     68     9     [23] = arXiv:0707.2488
20   1    61 −120     68     9     X_{1,2,2} ⊂ G(2,5)
```

The determinantal degree-20 family of CGKK has `h¹¹ = 2` and does not appear here.
So the target family is pinned down by `(H³, h¹¹, h¹², χ, c₂·H, h⁰(H)) =
(20, 1, 31, −60, 56, 8)`, and **these are exactly the invariants the repository records
for its smooth fibre** (`runs/astra-computation-2026-09-08/GEOGRAPHY_THEOREM.md`,
`reports/GEOGRAPHY.md`). Matching them is, by itself, not an identification; §§4–6 say
what would be.

---

## 3. The explicit construction (Macaulay2 1.20, `F₃₂₀₀₃`)

Every random choice is written out in `data/` so that the run replays exactly; the seed
is `20260911`. Scripts `k01_surface.m2`, `k11_ci.m2`, `k14_unproj.m2`, `k15_models.m2`.

**(a) The surface.** `P¹×P¹ → P⁸` by the nine monomials of bidegree `(2,2)`, composed
with a random surjection `k⁹ → k⁷` (`data/Mproj.m2`); `I_S` is the kernel of the induced
ring map `k[x₀..x₆] → k[s,t,u,v]`. Output (`logs/k01_surface.log`):

```
codim I_S = 4,  dim Proj = 2,  degree = 8
Betti table of k[x]/I_S :
       0  1  2  3  4  5 6
total: 1 17 53 68 43 14 2
    0: 1  .  .  .  .  . .
    1: .  3  .  .  .  . .
    2: . 14 53 68 43 14 2
```

This is *literally* the Betti table displayed in Kapustka's proof of Theorem 5.1, and
`S` is 3-regular with linear syzygies among the cubics, as that proof requires. The
Hilbert function of `k[x]/I_S` in degrees 0,1,2,3,4 is `1, 7, 25, 49, 81` against
`h⁰(O_D(2k,2k)) = (2k+1)² = 1, 9, 25, 49, 81`, so

```
h¹(I_S(1)) = 2,   h¹(I_S(k)) = 0  for k ≠ 1,        δ := Σ_{k≥0} h¹(I_S(k)) = 2.
```

**(b) The complete intersection.** `q₁,q₂` are two random combinations of the three
quadrics (`data/coeff_q.m2`); `F` is a random element of `(I_S)₃` (`data/coeff_F.m2`).
Output (`logs/k11_ci.log`):

```
codim_Xprime 3        dimProj_Xprime 3      degree_Xprime 12      I_X' ⊂ I_S  true
nodes_dimProj 0       nodes_degree 44       nodes_degree_radical 44
```

The last two lines say: the locus on `S` where the 3×7 Jacobian of `(q₁,q₂,F)` drops
rank is zero-dimensional of degree 44 **and reduced**. By Kapustka's Theorem 2.1 /
Lemma 4.1 these are the singular points of `X'` and they are ordinary double points.
So `X'` is a 44-nodal Calabi–Yau threefold of degree 12: Table 1 row 8, confirmed, and
the "37" of the printed proof of Theorem 5.1 refuted for this case.

**(c) The unprojection data by liaison.** Let `G ∈ (I_S)₃` be a general cubic with
`G ∉ I_{X'}`; then `S` is linked on `X'` by `G` to a surface `S'`, and

```
Hom_{O_{X'}}(I_S, O_{X'})  =  (1/G) · ( (I_{X'} + (G)) : I_S ).
```

A homomorphism of degree `d` is `j ↦ g·j/G` with `deg g = 3 + d`. Output
(`logs/k14_unproj.log`):

```
colon gen degrees: {2, 2, 3, 3, 4, 5, 5}
```

Since `I_{X'} = (q₁,q₂,F) ⊂ Q` and `G ∈ Q`, the minimal generators of degrees `2,2,3,3`
are exactly `q₁,q₂,F` (which give the zero homomorphism, being in `I_{X'}`) and `G`
(which gives the identity, `d = 0`). Hence `Q/I_{X'}` — and so `Hom(I_S,O_{X'})` — has
minimal generators in degrees `3,4,5,5`, i.e.

```
Hom_{O_{X'}}(I_S, O_{X'})  is generated over O_{X'} in degrees 0, 1, 2, 2 :
       1 ,   w  (one generator, degree 1) ,   y₁, y₂  (two generators, degree 2).
```

This is exactly what §4 predicts from `ω_S = O_S(−1)` and `h¹(I_S(1)) = 2`:
`Hom(I_S,O_{X'})/O_{X'} ≅ ω_{k[S]}`, whose degree-`n` piece is `H⁰(O_D(2n−2,2n−2))` of
dimensions `1, 9, 25, …`, while `O_{X'}₁ · w` only reaches the 7-dimensional space of
restrictions of linear forms — leaving `9 − 7 = 2` new generators in degree 2.

---

## 4. The polarised model of Kapustka's family is not in `P⁷`

### 4.1 The singularity

**Proposition 4.1.** Let `φ : X → Ybar` be the primitive type II contraction of
`D' ≅ P¹×P¹` with `O_{D'}(D') = K_{D'}`, and `P = φ(D')`. Then
`gr_{m_P} Ô_{Ybar,P} = ⊕_{n≥0} H⁰(D', −nK_{D'})`, the anticanonical cone over
`P¹×P¹`. Consequently

```
mult_P Ybar = (−K_{D'})² = 8,        dim T_P Ybar = h⁰(−K_{D'}) = 9,
```

and analytically `(Ybar, P) ≅ ({xy − zw = 0} ⊂ A⁴)/±1`.

*Proof.* `Ô_{Ybar,P} = lim← H⁰(O_X/O_X(−nD'))` and `I^n/I^{n+1} = H⁰(O_{D'}(−nD'))
= H⁰(−nK_{D'})`; `H¹(−nK_{D'}) = 0` for `n ≥ 0` on a del Pezzo surface, so the
associated graded ring is the anticanonical cone. Its degree-2 part
`Sym²H⁰(O(2,2)) → H⁰(O(4,4))` is surjective (`O(2,2)` is projectively normal), so
`m/m² = H⁰(O(2,2))` is 9-dimensional and the multiplicity is `deg(D' ⊂ P⁸) = 8`.
Write `U ≅ k⁴` with `P(U) = P³` and `q ∈ Sym²U*` the equation of the quadric surface
`D = {q = 0} ⊂ P(U)`; then `−K_D = O_{P³}(2)|_D`, so
`H⁰(D, −K_D) = Sym²U*/⟨q⟩` and the affine cone over `D ⊂ P(Sym²U)` is
`{u² : u ∈ U, q(u) = 0} ⊂ Sym²U` — the image of the ODP `{q = 0} ⊂ A⁴ = U` under
`u ↦ u²`, a `±1`-quotient, free away from the origin. ∎

### 4.2 Consequences

**Corollary 4.2.**
1. `T` is not very ample on `Ybar`, and `Ybar` admits **no** closed embedding into `P⁷`
   (its embedding dimension at `P` is 9).
2. G. Kapustka's Lemma 2.2 of [arXiv:0707.2488] — *"Let `i : Y ↪ Pⁿ` be a smoothable
   normal Gorenstein Calabi–Yau threefold. Then `Y` can be smoothed inside `Pⁿ`"*,
   proved from `H¹(Θ_{Pⁿ}|_Y) = 0` — is the mechanism that turns the analogous
   constructions of degrees 17, 18 (and, in CGKK, 19) into **arithmetically Gorenstein
   Calabi–Yau threefolds in `P⁷`**. It cannot be applied to `Ybar` with `n = 7`.
3. The image `Y := φ_{|T|}(Ybar) ⊂ P⁷` is the type-I (Kustin–Miller) unprojection of
   `S ⊂ X'`, with unprojection variable the degree-1 generator `w` of §3(c). It is
   non-normal at `P`, with normalisation `Ybar` and
   `δ = dim_k(ν_*O_{Ybar}/O_Y) = Σ_{k≥0} h¹(I_S(k)) = 2`; hence

```
χ(O_Y(n)) = (10/3)n³ + (14/3)n − 2   ≠   P_{SR(M)}(n) = (10/3)n³ + (14/3)n,
dim (I_Y)₂ = 2  (the two quadrics q₁,q₂ of X', which are cones with vertex P).
```
   In particular `[Y]` is **not** a point of `Hilb^{P_{SR(M)}}(P⁷)`.
4. The graded ring `R = ⊕_n H⁰(Ybar, nT)` has Hilbert function
   `1, 8, 36, 104, 232, …` = the Hilbert function of `k[M]`, but needs **two generators
   in degree 2** besides the eight of degree 1: `Ybar ⊂ P(1⁸,2²)`, with
   `(I_{Ybar})₂ = ⟨q₁,q₂⟩` two-dimensional and free of `y`.

*Proof of 3 and 4.* `ν : Ybar → Y` is finite birational and an isomorphism off `P`; the
local ring of `Y` at `P` is the subring of `Ô_{Ybar,P}` generated by the images of the
seven sections of `T` vanishing at `P`, i.e. the coordinate ring of the cone over the
*projected* surface `S = ~~D₈ ⊂ P⁶`. Therefore
`δ = Σ_n (h⁰(O_D(2n,2n)) − dim(k[x]/I_S)_n) = Σ_n h¹(I_S(n)) = 2` by §3(a), and
`χ(O_Y(n)) = χ(O_{Ybar}(nT)) − δ`. Riemann–Roch on `Ybar` (Kawamata–Viehweg vanishing
applies: canonical Gorenstein singularities, `T` ample) gives
`h⁰(nT) = (10/3)n³ + (14/3)n`. Since `dim Sym²H⁰(T) = 36 = h⁰(2T)` and the image has
dimension `h⁰(O_Y(2)) = 36 − 2 = 34`, the map `Sym²H⁰(T) → H⁰(2T)` has a
2-dimensional kernel — the quadrics of `X'` pulled back, which do not involve the
unprojection variable and hence are cones with vertex `P` — and a 2-dimensional
cokernel, which is exactly `ν_*O_{Ybar}/O_Y`. The cokernel is the source of the two
degree-2 ring generators, computed independently in §3(c). ∎

### 4.3 Where the dichotomy sits in Kapustka's constructions

For the same shape of construction (`del Pezzo D of degree d ⊂ nodal X'_{2,2,3} ⊂ P⁶`,
contract, smooth) the contracted threefold `Ybar` is embedded in `P⁷` by `|T|` **iff the
del Pezzo is linearly normal in `P⁶`**, i.e. iff `h⁰(−K_D) = d+1 ≤ 7`, i.e. `d ≤ 6`:

| `d` | model of `D ⊂ P⁶` | `δ` | `deg Y_t` | `Ybar ⊂ P⁷`? | in CGKK Table 1? |
|---|---|---|---|---|---|
| 5 | anticanonical in a `P⁵ ⊂ P⁶` | 0 | 17 | yes | no. 4, `h¹² = 55` |
| 6 | anticanonical in `P⁶` | 0 | 18 | yes | nos. 7, 8, `h¹² = 46, 45` |
| 7 | one projection (`~D₇`) | 1 | 19 | **no** | absent |
| 8 | two projections (`~~D₈`) | 2 | 20 | **no** | absent |

(The degree-19 entry of CGKK Table 1 is a *different* construction: an unprojection of a
linearly normal `S₆` inside a nodal Pfaffian `Y₁₃ ⊂ P⁶`, with `h¹¹ = 2`.) The two rows
where the del Pezzo has to be projected are exactly the two families missing from every
published list of arithmetically Gorenstein Calabi–Yau threefolds in `P⁷`.

**Why degree 20 is the extreme case.** For a linearly normal Calabi–Yau threefold of
degree `d` in `P⁷` with `h⁰(H) = 8`, Riemann–Roch gives `c₂·H = 96 − 2d` and
`h⁰(2H) = d + 16`, so an *arithmetically Gorenstein* one has h-vector `(1,4,d−10,4,1)`
and

```
dim (I)₂ = 36 − h⁰(2H) = 20 − d.
```

Being arithmetically Gorenstein therefore means `μ : Sym²H⁰(H) → H⁰(2H)` is **surjective**
(with a `(20−d)`-dimensional kernel), and only at `d = 20` does it additionally force the
threefold to lie on **no** quadric at all — `μ` is then a map `36 → 36` and surjectivity
is the same as injectivity. (Check: CGKK's degree-17 no. 4 has `3O(−2)` in its minimal
resolution, i.e. three quadrics, `= 20 − 17`.) So degree 20 is the one row of Kapustka's
Table 1 where (★) is the strongest possible demand, and the one where no dimension count
can decide it; that is why §7 is needed.

---

## 5. Every smoothing of `SR(M)` is an arithmetically Gorenstein family in `P⁷`

**Theorem 5.1 (reduction).** Let `π : 𝒳 → (T,0)` be any flat family of projective
schemes with `𝒳₀ ≅ X_M = SR(M)` and `𝒳_t` smooth for `t ≠ 0` near `0`. Then, after
shrinking `T`:

1. the line bundle `O_{X_M}(1)` extends uniquely to a line bundle `ℒ` on `𝒳`;
2. `π_*ℒ` is locally free of rank 8 and `𝒳 ↪ P(π_*ℒ) ≅ P⁷ × T` is a closed embedding
   over `T`;
3. for every `t ≠ 0`, `𝒳_t ⊂ P⁷` is a **smooth arithmetically Gorenstein Calabi–Yau
   threefold of degree 20 with h-vector `(1,4,10,4,1)`**, hence `ω = O`, `h⁰(H) = 8`,
   `(I_{𝒳_t})₂ = 0`, `I_{𝒳_t}` generated by 16 cubics, `H³ = 20`, `c₂·H = 56`.

*Proof.* By Hochster's formula `h^i(O_{X_M}) = dim_k \tilde H^i(M;k)`; `M` is a
`Z`-homology 3-sphere (`scripts/verify_sphere.py`), so `h¹(O) = h²(O) = 0` and
`h³(O) = 1`. Vanishing of `H²(O)` makes `Pic` smooth over the base and vanishing of
`H¹(O)` makes the extension of `O(1)` unique; this gives (1). `k[M]` is Cohen–Macaulay,
so `h^i(O_{X_M}(n)) = 0` for `i = 1,2` and all `n`, and `h³(O_{X_M}(n)) = h⁰(O(−n))^∨`;
hence `χ(ℒ_t) = 8` and, `ℒ_t` being ample with `ω = O` on a smooth fibre, Kodaira
vanishing gives `h⁰(ℒ_t) = 8` for all `t`. So `π_*ℒ` is locally free of rank 8 and the
evaluation map is surjective; the induced `𝒳 → P⁷ × T` is a closed embedding at `t = 0`,
hence on a neighbourhood, giving (2). For (3): flatness fixes the Hilbert polynomial;
`h¹(I_{𝒳_t}(k)) ≤ h¹(I_{X_M}(k)) = 0` by semicontinuity, so `𝒳_t` is arithmetically
Cohen–Macaulay, and `ω_{𝒳_t} = O` (flat limit of `ω`), so arithmetically Gorenstein with
`a`-invariant 0. An arithmetically Gorenstein threefold `Z ⊂ P⁷` with `ω_Z = O_Z` has
last resolution shift `S(−8)`, hence socle degree 4, hence symmetric h-vector
`(1, 4, h₂, 4, 1)` with `1+4+h₂+4+1 = deg Z = 20`, so `h₂ = 10` and
`dim (I_Z)₂ = dim S₂ − H(2) = 36 − 36 = 0`, `dim (I_Z)₃ = 120 − 104 = 16`. ∎

Note the proof uses **only** flatness, Hochster's formula and semicontinuity. It is
independent of the zero-context smoothing theorem and of every trust boundary in
`PROOFS.md`; it applies to *any* hypothetical smoothing of `SR(M)`.

**Corollary 5.2.** Let `K` be Kapustka's degree-20 family (§1.2), an irreducible
31-dimensional family (§2.4). If `SR(M)` admits a smoothing whose smooth fibres lie in
`K`, then the general member `Y_t ∈ K` is arithmetically Gorenstein in `P⁷`;
equivalently

```
(★)      μ_t : Sym² H⁰(Y_t, T_t) ⟶ H⁰(Y_t, 2T_t)      (36 → 36)
```
is an isomorphism for general `t`; equivalently `⊕_n H⁰(nT_t)` is generated in degree 1;
equivalently `T_t` is very ample and `h⁰(I_{Y_t}(2)) = 0`.

*Proof.* Being arithmetically Gorenstein in `P⁷` (i.e. `T_t` very ample and the image
projectively normal) is an open condition in a family of polarised Calabi–Yau threefolds
with `h⁰(T) = 8` constant: very ampleness is open, and `dim ker μ_t` is upper
semicontinuous since `π_*O(𝒯)` and `π_*O(2𝒯)` are locally free of ranks 8 and 36.
`K` is irreducible (§2.4), so if one member has the property the general member does.
(If one prefers not to use the irreducibility of `K`, read the conclusion as: *some*
component of `K` has arithmetically Gorenstein general member — which is what §7 then
obstructs, since §7 works along an arbitrary one-parameter smoothing of `Ybar`.)
By Theorem 5.1, a smoothing of `SR(M)` with fibres in `K` exhibits such a member. The
equivalences: `dim Sym²H⁰(T_t) = dim H⁰(2T_t) = 36`, so `μ_t` is injective iff
surjective; `ker μ_t = (I_{Y'_t})₂` for the image `Y'_t = φ_{|T_t|}(Y_t)` and
`coker μ_t` contains `ν_*O/O` for the normalisation; generation of `⊕H⁰(nT_t)` in
degree 1 is exactly "`φ_{|T_t|}` is a closed embedding with projectively normal image".∎

**At `t = 0` the property fails, and fails for a reason that is intrinsic to the
construction**: by Corollary 4.2, `ker μ₀ = ⟨q₁,q₂⟩` and `coker μ₀ = ν_*O_{Ybar}/O_Y`,
both 2-dimensional, the second being the two units of non-linear-normality
`h¹(I_S(1)) = 2` lost when `D₈ ⊂ P⁸` was projected into `P⁶`.

---

## 6. What remains after (★), and what does **not** identify the two families

Suppose (★) of Corollary 5.2 holds, so that `K` gives an irreducible 31-dimensional
family of arithmetically Gorenstein degree-20 Calabi–Yau threefolds in `P⁷`. Then:

* every `Y_t` is a point of `Hilb^P(P⁷)`, `P(n) = (10/3)n³ + (14/3)n`, with
  `h⁰(N_{Y_t}) = 63 + h¹²= 94` and `h¹(N_{Y_t}) = h¹¹ − 1 = 0`
  (the computation of `runs/astra-computation-2026-09-08/GEOGRAPHY_THEOREM.md` §"Direct
  Hilbert smoothness after Picard rank one" applies verbatim to any smooth
  `ρ = 1`, `H³ = 20`, projectively normal fibre), so `Hilb` is smooth at `[Y_t]` of
  dimension 94 and there is a **unique** component `H_K ∋ [Y_t]`, of dimension 94;
* the repository's smoothing component `H_SR ∋ [SR(M)]` also has dimension 94
  (`PROOFS.md` C05, inside the accepted trust boundary);
* the two families coincide **iff** `H_K = H_SR`.

The following are *not* sufficient to conclude `H_K = H_SR`, and are recorded here so
that they are not mistaken for the argument:

1. **Equality of all numerical invariants.** `(H³, c₂·H, h⁰(H), h¹¹, h¹², χ, ρ)
   = (20, 56, 8, 1, 31, −60, 1)` on both sides — verified in §2 — and the Betti tables
   agree automatically: §5 shows that *every* arithmetically Gorenstein Calabi–Yau
   threefold of degree 20 in `P⁷` has h-vector `(1,4,10,4,1)` and 16 cubic generators.
   The Betti table therefore carries no information at all here.
2. **Equality of component dimensions.** Both are `63 + 31 = 94` for the same reason.
3. **Uniqueness in a census.** `(20,1,31,−60,56,8)` is the unique row of Kapustka's
   Appendix 1 with these invariants, and no other family with them is known. That is
   evidence about the literature, not about the two components.
4. **A shared singular degeneration** would not suffice either without controlling the
   branch: at `[SR(M)]` the quadratic obstruction cone has 27 components of dimensions
   94, 93, 92, 91 (`reports/GEOGRAPHY.md`), with a *unique* 94-dimensional one. So a
   degeneration argument, if one is found, must land on that branch: what would suffice
   is a flat family in `Hilb^P(P⁷)` with general fibre in `K` and special fibre
   `SR(M)`, together with the (conditional) statement `GEO-002` that the local Hilbert
   germ at `[SR(M)]` is cut out by the quadratic equations, which then forces the
   94-dimensional branch to be unique and hence equal to `H_SR`.
5. **A failed search.** None was run here for a weight degeneration; see §7.

Conversely, a *negative* answer needs much less: by Corollary 5.2 it is enough that
(★) fail.

---

## 7. The local model of the smoothing, and a first-order obstruction to (★)

### 7.1 The model

By Proposition 4.1 the germ `(Ybar, P)` is the anticanonical cone over `D = P¹×P¹`,

```
C = { u·uᵀ : u ∈ U, q(u) = 0 }  ⊂  H₀ := ker λ  ⊂  Sym²U ≅ k¹⁰,
λ(A) = a₀₃ − a₁₂ ,  so λ(u·uᵀ) = q(u),   U ≅ k⁴ with P(U) = P³ ⊃ D = {q = 0}.
```

Its `(−1)`-weight (Pinkham) deformation sweeps out the cone over `V₈ = v₂(P³)`:

```
W_s = { u·uᵀ : q(u) = s } ⊂ H_s = {λ = s},    W_s − A₀ ⊂ H₀   (λ(A₀) = s).
```

In the affine chart `w = 1` of `P(1⁸,2²)`, `H₀ ≅ k⁹` has the seven "visible" coordinates
`x₁,…,x₇` (the image of the projection `P⁸ ⇢ P⁶` that produced `S`) and the two
"invisible" ones `y₁,y₂` spanning `K := ker(H₀ → k⁷)`; and the degree-2 piece of the
coordinate ring of `P(1⁸,2²)` restricts to

```
V₀ = ⟨ monomials in x of degree ≤ 2 ⟩ ⊕ ⟨ y₁, y₂ ⟩,    dim V₀ = 1+7+28+2 = 38 = dim (k[P(1⁸,2²)])₂.
```

Because restriction `I_{v₂(P³)}(2) → I_{D₈}(2)` is an isomorphism of 20-dimensional
spaces (the kernel would be `λ·(linear)` with the linear form vanishing on the
nondegenerate `v₂(P³)`), every `Q ∈ I_{D₈}(2)` has a unique extension `Q̃` to `Sym²U`
vanishing on the cone over `v₂(P³)`, and `f_Q := Q̃(A₀ + ·)` lies in `V₀` and vanishes on
`W_s − A₀`. Put

```
Λ   = { Q ∈ I_{D₈}(2) : K ⊆ rad(Q|_{H₀}) }        ( = H⁰(I_S(2)) , the y-free quadrics )
Λ₀  = { Q ∈ Λ         : K ⊆ rad(Q̃) on Sym²U }.
```

For `Q ∈ Λ` the linear form `B_{Q̃}(·,k)` vanishes on `H₀`, hence equals `c_Q(k)·λ`, so the
`y`-coefficient of `f_Q` is `2·λ(A₀)·c_Q = 2s·c_Q`. Therefore

```
rank ( { f ∈ V₀ : f|_{W_s − A₀} = 0 } ⟶ ⟨y₁,y₂⟩ )  =  dim Λ − dim Λ₀     for s ≠ 0.
```

**Computation** (`scripts/verify_local_model.py`, exact over `F₃₂₀₀₃`, four random
choices of `K` and three of the coordinates, plus a direct check of the vanishing
locus): for a general 2-dimensional `K ⊂ H₀`,

```
dim Λ = 3,    dim Λ₀ = 2,    rank = 1,
{ f ∈ V₀ : f|_{W_s−A₀} = 0 } has dimension 3 for every s, with y-image of dimension
      0  for s = 0        and        1  for s ≠ 0.
```

`dim Λ = 3` is the same number as `h⁰(I_S(2)) = 3` found in §3(a) by an entirely
different computation, which is a check on the model.

### 7.2 What this proves

**Proposition 7.1 (first order).** Let `𝒴 → Δ` be a one-parameter deformation of `Ybar`
inside `P(1⁸,2²)` (flat, graded) with `𝒴₀ = Ybar`. Identify `(I_{𝒴_s})₂ ≅ (I_{Ybar})₂ =
⟨q₁,q₂⟩` for small `s` and let `β_s : (I_{𝒴_s})₂ → ⟨y₁,y₂⟩` be the canonical map
(canonical because `Sym²⟨x,w⟩ ⊂ k[P(1⁸,2²)]₂` is). Write `β_s = sC + O(s²)`. Then

```
rank C ≤ 1,        in particular   det C = 0.
```

*Proof.* The germ of `𝒴` at `P` is an embedded deformation of `C ⊂ (k⁹,0)`; up to an
ambient analytic automorphism `Φ_s = id + sΨ + O(s²)` of `(k⁹,0)` it is the model
`W_{c(s)} − A₀` of §7.1. For a quadratic form `Q` that is `y`-free on `H₀`,
`Q∘Φ_s = Q + 2s·B_Q(·, Ψ(·)) + O(s²)`, and the part of `B_Q(·,Ψ(·))` that is linear in
the coordinates is `B_Q(·, Ψ(0))` with `Ψ(0) ∈ H₀`, whose `y`-coefficients
`B_Q(e_{y_a}, Ψ(0))` vanish because `K ⊆ rad(Q|_{H₀})`. So the ambient automorphism does
not change the first-order `y`-coefficients, and these are those of the model, i.e. the
image of `⟨q₁,q₂⟩ ⊆ Λ` under `Q ↦ 2c_Q`, of rank `≤ dim Λ − dim Λ₀ = 1`. ∎

**Remark.** `rank C ≤ 1` already follows from the two dimensions alone:
`(I_{Ybar})₂ = ⟨q₁,q₂⟩` is a 2-dimensional subspace of the 3-dimensional `Λ`, the kernel
of `Q ↦ c_Q` is the 2-dimensional `Λ₀ ⊂ Λ` of codimension 1, so
`dim(⟨q₁,q₂⟩ ∩ Λ₀) ≥ 2 + 2 − 3 = 1` and the image of `⟨q₁,q₂⟩` has dimension `≤ 1`.
No genericity of `q₁,q₂` inside `Λ` is needed.

**Corollary 7.2.** No first-order graded deformation of `Ybar` inside `P(1⁸,2²)`
eliminates both degree-2 ring generators: the first-order term of `det β_s` vanishes for
every such deformation, so `Ybar` has no first-order deformation lying in a `P⁷`. In the
model of §7.1 this persists to all orders in `s`: exactly one of the two degree-2
generators becomes redundant, so `⊕_n H⁰(nT_s)` is generated by `H⁰(T_s)` together with
one element of `H⁰(2T_s)`; the smooth fibre would then satisfy `Y_s ⊂ P(1⁸,2)` and
`h⁰(I_{Y_s}(2)) = h¹(I_{Y_s}(2)) = 1`, so it would be very ample but **not**
arithmetically Gorenstein in `P⁷`, and (★) would fail.

### 7.2b Status of the independent global check

`scripts/k17_deform.m2` computes the same first-order `y`-coefficient map **globally**,
as the composite `Hom_{k[x,w,y]}(I_{Ybar}, R)₀ → M₂(k)`, and reports the dimension of its
image and whether that image contains an invertible matrix; Proposition 7.1 predicts
"image spanned by a single rank-1 matrix, no invertible matrix". The script confirmed the
input data (`generator degrees {2,2,3×16,4,4,4}`, `degree-2 generator positions {0,1}`,
`degree-2 generators y-free? true`) and then entered `normalMatrix({0}, F0)`; **that
computation had not returned after 45 minutes and ~1.2 GB and is recorded as not
completed in this run** (`logs/k17_deform.log`). Proposition 7.1 does not depend on it.

### 7.3 The gap

Proposition 7.1 is a statement about the **first** order only. Beyond first order the
ambient analytic automorphism `Φ_s` does contribute `y`-terms: at order `s²` the term
`Q(sΨ₁(B))` contains `2B_Q(Ψ₁(0), Ψ₁'(B))`, whose `y`-coefficient
`2B_Q(Ψ₁(0), Ψ₁'(e_{y_a}))` need not vanish. Concretely, writing
`β_s = sC + s²C₂ + O(s³)` with `rank C = 1`,

```
det β_s  =  s³ · tr( adj(C)·C₂ )  +  s⁴ det C₂ + O(s⁵),
```

so (★) would already be settled negatively by knowing that `tr(adj(C)C₂) = 0` and
`det C₂ = 0`, and settled positively by either being non-zero. **Deciding (★) therefore
needs the second-order term `C₂` of the actual (global) smoothing of `Ybar` inside
`P(1⁸,2²)`, not just its first-order term.** That is the next specific obstacle; it is a
second-order Kuranishi computation of the same shape as the ones in
`runs/astra-daytime-2026-09-08/FIXED_CHART.md`, but for `I_{Ybar} ⊂ P(1⁸,2²)` (21
generators, 10 variables) rather than for `I_M ⊂ P⁷`.

---

## 8. Verdict

**UNRESOLVED, with the question reduced to a single explicitly stated property and with
first-order evidence against it.** Precisely:

### 8.1 Established unconditionally (no trust boundary)

* **T1.** Kapustka's Table 1 is reproduced exactly, rows 1–8, from three closed formulas
  (§2); the comparison family is row 8, built from `D = P¹×P¹` doubly projected into
  `P⁶` inside a 44-nodal `(2,2,3)` complete intersection, with
  `(H³, c₂·H, h⁰(H), h¹¹, h¹², χ, ρ) = (20, 56, 8, 1, 31, −60, 1)` — the invariants the
  repository records for its smooth fibre. The pairing of the two cases inside the
  printed proof of Kapustka's Theorem 5.1 is transposed (§2.1, `SOURCES.md` S1).
* **T2.** (§4) The contracted threefold `Ybar` of that construction has one singular
  point, analytically `({xy = zw} ⊂ A⁴)/±1`, of multiplicity 8 and **embedding
  dimension 9**. Hence `Ybar` does not embed in `P⁷`; the `P⁷`-image `Y` is the
  Kustin–Miller unprojection of `S ⊂ X'`, is non-normal with `δ = 2`, has Hilbert
  polynomial `(10/3)n³+(14/3)n−2` and lies on two quadrics; and the normal model is
  `Ybar ⊂ P(1⁸,2²)` with Hilbert function `1,8,36,104,232,440` — the Hilbert function of
  `k[M]` — cut out by 2 quadrics, 16 cubics and 3 quartics. (All Macaulay2-certified,
  §3.)
* **T3.** (§5, Theorem 5.1) *Every* smoothing of `SR(M)` is an embedded smoothing inside
  `P⁷` whose smooth fibres are arithmetically Gorenstein Calabi–Yau threefolds of degree
  20 with h-vector `(1,4,10,4,1)`. Therefore

  > `SR(M)` has a smoothing with fibres in Kapustka's family **⟹** the general member of
  > that family is arithmetically Gorenstein in `P⁷`, i.e. **(★)**.

* **T4.** (§7, Proposition 7.1) **(★) fails to first order**: along any one-parameter
  deformation of `Ybar` inside `P(1⁸,2²)`, the `2×2` matrix recording the `y₁,y₂`
  coefficients acquired by the two degree-2 equations has rank `≤ 1` at first order, so
  no first-order deformation moves `Ybar` into a `P⁷`. In the local model of the
  smoothing this persists to all orders: exactly one of the two degree-2 generators
  becomes redundant and the smooth fibre lies on exactly one quadric of `P⁷`.

### 8.2 Established relative to the repository's trust boundary

Nothing new: the repository's `(1,31)`, `ρ = 1`, 94-dimensional component (`PROOFS.md`
C05) are used only to say that the numerical invariants on the two sides agree. T3 does
not use them.

### 8.3 Not established

**(★)** itself, at second and higher order, hence the answer to the question. §7.3 shows
that the first non-trivial invariant is the second-order term `C₂` of the smoothing of
`Ybar` inside `P(1⁸,2²)`:

```
det β_s = s³·tr(adj(C)·C₂) + s⁴·det C₂ + O(s⁵),     rank C = 1.
```

`(★)` holds iff this is not identically zero. The remaining obstacle is that the germ of
the smoothing at the singular point determines the `y`-coefficients only to first order;
at order two an ambient analytic coordinate change can contribute (§7.3). This is a
finite, well-posed computation on the explicit ideal `I_{Ybar} ⊂ k[x₀..x₆,w,y₁,y₂]`
shipped in `data/IYbar.m2`.

### 8.4 What the evidence says

Everything found points the same way — that **(★) fails, and hence that the answer to
the question is no**:

1. the first-order obstruction T4, with a structural explanation (`dim Λ − dim Λ₀ = 1`);
2. the all-orders behaviour of the local model;
3. the systematic pattern of §4.3: in Kapustka's family of constructions the passage to
   an arithmetically Gorenstein model in `P⁷` is made by his Lemma 2.2, whose hypothesis
   ("`Y ↪ Pⁿ` normal Gorenstein") holds exactly when the contracted del Pezzo is
   linearly normal, i.e. in degrees 17 and 18 — and those are exactly the members that
   appear in the published lists;
4. three enumerations by the constructors themselves (CGKK 2016 Table 1 and §4.9,
   KKRSSY Memoirs AMS 2026 §8) omit a degree-20 arithmetically Gorenstein family with
   `h¹¹ = 1`; CGKK say that in degree 20 "only one example is known", the determinantal
   one with `h¹¹ = 2`.

None of 1–4 is a proof. A proof needs §8.3.

### 8.5 A by-product worth recording

If the zero-context smoothing theorem holds, then `SR(M)` smooths to a **smooth
arithmetically Gorenstein Calabi–Yau threefold of degree 20 in `P⁷` with
`(h¹¹,h¹²) = (1,31)`** (T3 plus `PROOFS.md` C05). No such family appears in CGKK's
Table 1 — which those authors conjecture to be complete in degree 20 — nor in KKRSSY,
whose Question 8.5 ("describe the quartics of type `[000]` that lift to smooth
threefolds") is precisely the classification problem it would bear on. So the
zero-context claim is in direct tension with a published conjecture, independently of
anything about Kapustka's degree-20 family. That tension is a sharper test of the
zero-context theorem than the comparison asked for here, and it is stated as such, not
resolved.
