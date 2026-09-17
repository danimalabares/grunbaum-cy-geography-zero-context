# The comparison in the language of linear systems, graded rings and ideals

*Run `runs/kapustka-degree20-comparison-2026-09-11`. Everything is exact: closed formulas
in integer arithmetic (Python), Macaulay2 1.20 over `F₃₂₀₀₃`, and one exact linear-algebra
model in `F₃₂₀₀₃`. Sections marked **[verdict]** summarise `REPORT.md` §8.*

## 1. The two objects

**Ours.** `S = k[a,…,h]`, `I_M` the 16 cubic monomials, `X_M = Proj S/I_M ⊂ P⁷` the union
of the 20 coordinate `P³`'s. Arithmetically Gorenstein, `ω = O`, h-vector `(1,4,10,4,1)`,
Hilbert function `1, 8, 36, 104, 232, 440, …`.

**Kapustka's.** Start from `D = P¹×P¹` with `−K_D = O(2,2)`, so `D ⊂ P⁸` of degree 8.
Project from a *general line* of `P⁸`: `S := ~~D₈ ⊂ P⁶`, still isomorphic to `D` and of
degree 8, but now **not linearly normal** — `h¹(I_S(1)) = 2`, the two linear forms lost in
the projection. Its ideal has 3 quadrics and 14 cubics. Take `X' = V(q₁,q₂,F) ⊂ P⁶`, a
general `(2,2,3)` complete intersection through `S`: a Calabi–Yau threefold of degree 12
with exactly 44 nodes, all on `S`. Blow up `S` (a small resolution), flop, get a smooth
`X` with `Pic X = Z H* ⊕ Z D'`, `D' ≅ D`. Because `K_X = 0`, adjunction gives
`D'|_{D'} = K_{D'}` and `H*|_{D'} = −K_{D'}`, so `G := H* + D'` is trivial on `D'` and
`φ_{|G|}` contracts `D'` to a point `P`. That contraction `Ybar` is smoothed (Gross,
Thm. 5.8); the smooth fibres `Y_t` are the comparison family.

## 2. Why the two look identical numerically

`deg Ybar = deg X' + deg D = 12 + 8 = 20`; `mult_P Ybar = (D'|_{D'})² = K_D² = 8`;
`h⁰(G) = h⁰(H*) + 1 = 8`; Riemann–Roch then gives `c₂·H = 12(8 − 20/6) = 56`;
`χ(Y_t) = χ(X) − 2χ(D) + χ(V) = −56 − 8 + 4 = −60`, hence `h¹² = 31` given `h¹¹ = 1`.
So `⊕_n H⁰(Ybar, nT)` has Hilbert function `1, 8, 36, 104, 232, 440, …` — **the same
graded vector space as `S/I_M`.**

## 3. Where they part company: two extra ring generators

Sections of `T` come from `X'`: `H⁰(G) = s_{D'}·H⁰(H*) ⊕ ⟨w⟩`, so the seven `x_i` vanish
at `P` and `w` does not. In the chart `w = 1` the local ring of `Ybar` at `P` has
associated graded ring `⊕_n H⁰(D, −nK_D)`, the anticanonical cone over `P¹×P¹`, i.e.

```
{ u·uᵀ : q(u) = 0 } ⊂ Sym²U      ( = the ODP {q=0} ⊂ A⁴ modulo ±1 ),
```

of multiplicity 8 and **embedding dimension 9**, while only `7 + 1` coordinates are
available. So `Ybar` needs nine local coordinates and `P⁷` offers seven: `Ybar ⊄ P⁷`.

Algebraically this is the liaison computation of §3(c) of `REPORT.md`: with `G` a general
cubic in `I_S` linking `S` on `X'` to `S'`,

```
Hom_{O_{X'}}(I_S, O_{X'}) = (1/G)·( (I_{X'} + (G)) : I_S ),
   colon-ideal minimal generator degrees  {2,2,3,3,4,5,5}
   ⇒  Hom is generated in degrees 0, 1, 2, 2 :   1,  w,  y₁, y₂.
```

`w` is the Kustin–Miller unprojection variable (degree 1), giving `Y ⊂ P⁷`; but that `Y`
is **non-normal** at `P`, with `δ = Σ_k h¹(I_S(k)) = 2` and Hilbert polynomial
`(10/3)n³ + (14/3)n − 2` — a *different* Hilbert scheme from `X_M`'s. The normal model
needs `y₁,y₂` as well:

```
Ybar ⊂ P(1,1,1,1,1,1,1,1,2,2),   Hilbert function 1, 8, 36, 104, 232, 440,
I_Ybar cut out by 2 quadrics, 16 cubics, 3 quartics,  (I_Ybar)₂ = ⟨q₁,q₂⟩ free of y.
```

## 4. What the question becomes

`SR(M)` has `h¹(O) = h²(O) = 0` (Hochster, `M` a homology `S³`), so `O(1)` deforms
uniquely and **every** smoothing of `SR(M)` is an embedded smoothing inside `P⁷` with
arithmetically Gorenstein fibres — `h-vector (1,4,10,4,1)`, no quadrics, 16 cubics. So a
Kapustka-family smoothing exists only if the general `Y_t` is arithmetically Gorenstein in
`P⁷`, i.e. iff `μ_t : Sym²H⁰(T_t) → H⁰(2T_t)` (a `36 → 36` map) is an isomorphism, i.e.
iff the two degree-2 generators `y₁,y₂` become redundant. In the flat family inside
`P(1⁸,2²)` that says: the 2-dimensional `(I_{𝒴_s})₂` must contain `y₁ − Q₁(x)` and
`y₂ − Q₂(x)`, i.e. the `2×2` matrix of `y`-coefficients must be invertible.

## 5. The obstruction **[verdict]**

Under the smoothing, `{u·uᵀ : q(u) = 0}` becomes `{u·uᵀ : q(u) = s}`, translated into the
fixed `k⁹` by any `A₀` with `λ(A₀) = s`. The quadrics `Q` in `(I_Ybar)₂` are the ones that
do not involve `y`, i.e. whose radical contains the 2-plane `K` of "lost" directions; each
has a unique extension `Q̃` to `Sym²U` vanishing on the cone over `v₂(P³)`, and
`B_{Q̃}(·,k) = c_Q(k)·λ`, so the acquired `y`-coefficient is `2s·c_Q`. Exactly (checked in
`F₃₂₀₀₃`, several random `K`):

```
Λ  = { Q : K ⊆ rad(Q|_{H₀}) } has dimension 3   ( = h⁰(I_S(2)), independently confirmed )
Λ₀ = { Q : K ⊆ rad(Q̃) }       has dimension 2
⇒ the map Q ↦ c_Q has rank 1, and (I_Ybar)₂ is a 2-plane inside the 3-dimensional Λ,
  so dim( (I_Ybar)₂ ∩ Λ₀ ) ≥ 2 + 2 − 3 = 1  and the y-matrix has rank ≤ 1.
```

A first-order ambient coordinate change cannot repair this (its only contribution to the
linear part is `B_Q(·, Ψ(0))` with `Ψ(0) ∈ H₀`, which `K ⊆ rad(Q|_{H₀})` kills). So **no
first-order deformation of `Ybar` lands in a `P⁷`**, and in the local model the rank stays
1 at all orders: the smooth fibre would lie on exactly one quadric of `P⁷` and be very
ample but not arithmetically Gorenstein.

**Verdict: unresolved, everything pointing to "no".** The one missing item is the
second-order term: writing the `y`-matrix as `sC + s²C₂ + …` with `rank C = 1`,
`det = s³·tr(adj(C)C₂) + s⁴·det C₂`, and `C₂` for the *global* smoothing is not computed
here — past first order an ambient analytic coordinate change at `P` can contribute.
