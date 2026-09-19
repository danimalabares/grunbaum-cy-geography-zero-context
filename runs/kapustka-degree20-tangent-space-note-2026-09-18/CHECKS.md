# Computational checks (Macaulay2 1.20, `/Applications/Macaulay2-1.20/bin/M2`)

Run from this directory: `M2 --script scripts/<name>.m2 > logs/<name>.log 2>&1`. Messages go to
stderr. Scripts `c01`–`c03` are exact over `QQ`; `c04` is over `F₃₂₀₀₃` and is a sanity check on
the ideals shipped by the historical run, **not** a characteristic-zero argument.

| script | what it verifies | field | runtime | decisive lines in the log |
|---|---|---|---|---|
| `c01_srm_sphere.m2` | the frozen `I_M`: codim 4, degree 20, Betti numbers `1,16,30,16,1` in degrees `0,3,4,5,8`, Hilbert function `1,8,36,104,232,440`, h-vector `(1,4,10,4,1)`, Hilbert polynomial `(10/3)n³+(14/3)n`, no quadrics, 16 cubics; chart `a = 1`: all 16 local generators have degree ≥ 2, so `dim T_p SR(M) = 7` at a vertex; the chart is a cone of dimension 3 and degree 10 | `QQ` | 1 s | `Betti table`, `reduced Hilbert series`, `dim (I_M)_2 = 0`, `dim T_p SR(M) = 7` |
| `c02_anticanonical_cone.m2` | (i) the ideal of `D₈ = v_{2,2}(P¹×P¹) ⊂ P⁸`: 20 quadrics, degree 8, Hilbert function `(2n+1)²`, no linear forms, so the affine cone has `dim T₀ = 9` and multiplicity 8; (ii) the kernel of `QQ[a_ij] → QQ[x,y,z,w]/(xy−zw)`, `a_ij ↦ (i-th coordinate)(j-th coordinate)`: one linear form `a_01 − a_23` and 20 quadrics; the even part of the node has dimensions `1,9,25,49,81`; (ii') the same ideal is obtained from the parametrisation `(x,y,z,w) = (su,tv,sv,tu)` of `{xy = zw}`; (iv) `W₀ = {rank ≤ 1, λ = 0}` equals that ideal; `W₁ = {rank ≤ 1, λ = 1}` has dimension 3, degree 8; `Q₁ = {xy − zw = 1}` is smooth; `dim T = 3` at two points of `W₁`; `dim T = 9` at the vertex of `W₀` and `3` at a non-vertex point | `QQ` | 1 s | `(i) linear forms in the ideal: 0`, `(ii') … equals Iinv ? true`, `(iv) W_0 … equals Iinv ? true`, `dim of Zariski tangent space there = 3`, `W_0 at the vertex: dim T = 9` |
| `c03_projected_surface_QQ.m2` | `S = ~~D₈ ⊂ P⁶` for a random integer `7×9` projection matrix (seed 20260918, entries in `[−9,9]`, printed in the log): codim 4, degree 8, generators 3 quadrics + 14 cubics, Betti table `1; 3; 14 53 68 43 14 2` (Kapustka's), `h¹(I_S(1)) = 2`, `h¹(I_S(k)) = 0` for `k = 0,2,3,4`; no linear forms, so the cone over `S` has `dim T₀ = 7` | `QQ` | 4 min (the `res`) | `Betti table`, `deficiency h^1(I_S(k))` lines |
| `c04_ybar_charts_F32003.m2` | loads `../../kapustka-degree20-comparison-2026-09-11/data/IYbar.m2` and `data/IY.m2`; chart `w = 1`: `Ybar` has `dim T_P = 9`, tangent cone of degree 8 cut out by 20 quadrics (the cone over `D₈`); `Y ⊂ P⁷` has `dim T_P = 7`, tangent cone of degree 8 cut out by 3 quadrics and 14 cubics (the cone over `S`); Hilbert polynomial of `Y` is `(10/3)n³+(14/3)n−2` | `F₃₂₀₀₃` | 30 s | `dim T_P Ybar = 9`, `degree (= multiplicity of Ybar at P) = 8`, `dim T_P Y = 7`, `Hilbert polynomial = (10/3)*i^3+(14/3)*i-2` |

## Abandoned or replaced steps (recorded, not used)

* `c02`: a Jacobian-criterion computation of the singular locus of `W₁` (`minors(7, jacobian W1)`,
  about `10⁷` minors) did not return within 5 minutes and was replaced by the argument that `W₁`
  is the free quotient of the smooth quadric `Q₁` by `±1`, plus tangent-space ranks at two points.
* `c03`: a saturation of the Jacobian ideal of `S` (smoothness of `S`) did not return within
  4 minutes and was dropped; `S ≅ P¹×P¹` because a general line of `P⁸` misses the 5-dimensional
  secant variety of `D₈`.
* `c01`: two earlier versions failed on Macaulay2 substitution syntax; the chart is now built by
  an explicit ring map.

## What is proved in characteristic zero and what is only checked

* `dim T_P Ybar ≥ 9`: proved in `DANI_NOTE.tex` §2 Step 1 (theorem on formal functions and
  `H¹(O_D(2,2)) = 0`); `c02 (i)` is the corresponding computation on the model cone.
* `dim T_P Ybar = 9`, multiplicity 8, analytic model `{xy = zw}/±1`: `DANI_NOTE.tex` §2 Steps 2–3,
  resting on Gross, Prop. 5.4 (with Reid's theorem for "the contraction is the blow-up of `P`");
  `c02 (ii)`, `(ii')` verify the identification of the cone with the quotient of the node over `QQ`.
* `h¹(I_S(k)) = 0` for `k ≥ 2` (needed for `δ = 2`): verified over `QQ` for one random centre
  (`c03`), hence for the general centre by upper semicontinuity; consistent with Kapustka's printed
  Betti table (3-regularity).
* `dim (I_Y)₂ = 2` (Y lies on exactly the two quadric cones): only the finite-field computation of
  the 2026-09-11 run (`k15_models.log`, Hilbert function 34 in degree 2); in characteristic zero
  only `≥ 2` is used in the note.
* Everything about the smooth fibres `Y_t` (very ampleness of `T_t`, projective normality, property
  `(★)`) is **not** decided by any computation here.
