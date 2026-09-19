# Sources consulted (access date 2026-09-18)

The three arXiv PDFs were downloaded to a local scratch directory and their text was extracted with
PyMuPDF; the PDFs are **not** committed (third-party documents). URL and SHA-256 are recorded so
that the exact versions can be re-obtained. Quotations are verbatim from the extracted text.

| id | document | URL | SHA-256 of the PDF |
|---|---|---|---|
| S1 | G. Kapustka, *Projections of del Pezzo surfaces and Calabi–Yau threefolds*, arXiv:1010.3895 **v5** (4 Mar 2015), 22 pp.; Adv. Geom. 15 (2015) 143–158 | https://arxiv.org/pdf/1010.3895v5 | `6e42a7f64ce08d3c0625e6adef1656be0949e265485007f7ce42cbec37e9fbb1` |
| S2 | M. Gross, *Deforming Calabi–Yau threefolds*, arXiv:alg-geom/9506022 **v2**, 47 pp.; Math. Ann. 308 (1997) 187–220 | https://arxiv.org/pdf/alg-geom/9506022v2 | `28c81d3fd09a2e2cc8e8e243257929250cccd527849165b6968ad4503007b01b` |
| S3 | G. Kapustka, *Primitive contractions of Calabi–Yau threefolds II*, arXiv:0707.2488 **v3**, 20 pp.; J. London Math. Soc. (2) 79 (2009) 259–271 | https://arxiv.org/pdf/0707.2488v3 | `058cc2d2d0dbcc6df69ce6309ae849277b0468239ebeb37123e984a22a5822fb` |

Not re-fetched, cited from memory of the standard text: R. Hartshorne, *Algebraic Geometry*,
Theorem III.11.1 (theorem on formal functions); the Artin–Rees lemma used inside its proof.

## S1 — Kapustka, *Projections of del Pezzo surfaces and Calabi–Yau threefolds*

**Table 1, row 8** (p. 2): `No 8 | deg D′ 8 | X′_{2,2,3} | 44 ODP | χ(Y_t) = −60 | H³ = 20 | h⁰(H) = 8`.

**Introduction, p. 3** (on rows 1 and 3, degrees 14 and 15): "Note that No. 1 and No. 3 do not
have smoothing in P6 and the generator of their Picard group is not very ample."

**Proposition 3.2** (degree-15 row, the model for the degree-20 argument): "The image of X under
the morphism ϕ|G| is a threefold Y ⊂ P6 of degree 15 with one singular point P. Moreover, X′ ⊂ P5
is the projection of Y from P." Proof excerpt: "First, G ∈ |H∗ + D′| where H∗ is the pull-back of
H on X. So |G| is very ample outside D′. […] Since G|D′ is trivial we obtain D′ ∩ G = ∅. So |G| is
base-point-free and contracts D′ to a point."

**Remark 3.3**: "The threefold Y is not normal at P. We need to take a multiple of G to obtain a
primitive contraction (cf. [25, Lem. 2.5]). However, it is possible that that in some cases Y can
be smoothed by Calabi–Yau threefolds in P6."

**Theorem 3.4**: "The morphism ϕ|2G| gives a primitive contraction with image being a singular
Calabi–Yau threefold that is a degeneration two family of Calabi–Yau threefolds with h1,2 = 39 and
h1,2 = 40 of degree 15. Moreover, the Picard groups of the threefolds obtained are isomorphic to
Z." Proof excerpts: "If we prove that ϕ|2G| is a primitive contraction, then from [18] the
resulting singular Calabi–Yau threefolds can be smoothed. The problem is to show the normality of
the image." — "Next, the image T of G on Y is an ample divisor (2T is very ample) such that T3 = 15
and h0(O(T)) = 7 (by Proposition 3.2)." — "From [23, Lem. 2.2] we can embed Yt into PN. This
embedding is clearly given by the complete linear system 2Tt".

**Theorem 5.1** (statement, with the transposition already recorded in the 2026-09-11 run):
"There exist a Calabi–Yau threefold with Picard group of rank 1 of degree 19 (resp. 20) with
h1,2 = 23 (resp. h1,2 = 31)." Proof excerpts: "We find explicitly using Singular with a random
choice of the center of projection, two quadrics containing a projected surface intersecting each
other along a smooth threefold Y (it would be interesting to prove that this holds for a generic
choice of the center)." — the printed Betti table of the ideal of `~~D₈`:
```
1  0   0   0   0   0  0
0  3   0   0   0   0  0
0  14  53  68  43  14 2
```
— "We can conclude as in the proof of Theorem 3.4."

**Remark 5.2**: "From the proof below we deduce that the general projection ˜˜D8 ⊂ P6 needs 14
cubics an 3 quadrics generators."

References of S1 used to resolve citations: [18] = Gross, Deforming Calabi–Yau threefolds (= S2);
[23] = Kapustka, Primitive contractions II (= S3); [25] = G. Kapustka, M. Kapustka, Primitive
contractions of Calabi–Yau threefolds I, Comm. Algebra 37 (2009) 482–502 (not fetched).

## S2 — Gross, *Deforming Calabi–Yau threefolds*

**§5, classification** (after Wilson [54]): "Type I: π contracts a union of curves. Type II: π
contracts a divisor to a point. Type III: π contracts a divisor to a curve." A primitive
contraction is one that "cannot be factored in the algebraic category".

**Theorem 5.2, proof, first sentence**: "By [41, Thm. 2.11], π is the blowing-up of X at P, the
singular point of X. The exceptional surface E is a generalized del Pezzo surface (ωE is ample) of
degree k, where k is Reid's invariant (see §3)."

**Proposition 5.4** (verbatim): "Suppose (X, 0) is an isolated rational Gorenstein threefold point
with k = mult0X ≥ 5, such that if X̃ → X is the blowing-up of X at 0, then X̃ is non-singular and
the exceptional divisor E is non-singular. Then (X, 0) is analytically isomorphic to a cone over E."
Proof excerpt: "If H1(ΘE ⊗ (IE/I2E)n) = H1((IE/I2E)n) = 0 for all n ≥ 1, then [9, Cor. to Satz 7],
tells us that (X̃, E) is analytically isomorphic to an open neighborhood of E embedded in the normal
bundle of E in X̃ as the zero section. This will then give the theorem. E is a del Pezzo surface of
degree between 5 and 9, and IE/I2E = ω−1E."

**§5.5, k = 8** (verbatim): "There are two cases. If E ≅ P1 × P1, then (X, 0) can be smoothed by
taking a hyperplane section of a cone over P3 embedded via the 2-uple embedding. If E ≅ F1, there
is no smoothing. In both cases, dimk T1 = 1."

**Theorem 5.8** (verbatim): "Let π : X̃ → X be a primitive type II contraction with exceptional
divisor E. Then X is smoothable unless (1) E ≅ P2 or (2) E ≅ F1."

References of S2 used: [9] Grauert, *Über Modifikationen und exzeptionelle analytische Mengen*,
Math. Ann. 146 (1962) 331–368; [41] Reid, *Canonical 3-folds*, Géométrie Algébrique Angers (1980)
273–310; [54] Wilson, *The Kähler cone on Calabi–Yau threefolds*, Invent. Math. 107 (1992) 561–583.

## S3 — Kapustka, *Primitive contractions of Calabi–Yau threefolds II*

**Lemma 2.2** (verbatim): "Let i: Y ↪ Pn be a smoothable (normal Gorenstein) Calabi–Yau threefold.
Then Y can be smoothed inside Pn." Proof excerpt: "The latter follows from Theorem 1.7 (ii) in
[Weh] if we show that H1(ΘY|Pn) = 0. Indeed, since dim(sing(Y)) = 0 and Y is normal Gorenstein it
follows from [AJ, Prop. 1.1] that H1(OY(1)) = 0."
The hypothesis is a closed embedding `Y ↪ Pⁿ`; for Kapustka's degree-20 contraction and `n = 7` it
fails (DANI_NOTE, Proposition 3.1), which is why the lemma cannot be used to put the smooth fibres
into `P⁷`. It is used by Kapustka with `N` and `|2T_t|` in the proof of S1, Theorem 3.4.

## Repository inputs (read only)

`runs/kapustka-degree20-comparison-2026-09-11/` — `REPORT.md` (§0–§8), `DANI_EXPLANATION.md`,
`OPEN_QUESTIONS.md`, `SOURCES.md`, `REPRODUCE.md`, `scripts/k01_surface.m2`, `k15_models.m2`,
`k16_ybar.m2`, `logs/*.log`, and the shipped ideals `data/IY.m2`, `data/IYbar.m2` (loaded by
`scripts/c04_ybar_charts_F32003.m2` here, over `F₃₂₀₀₃`). The frozen `I_M` is transcribed from
`scripts/verify_geography.m2` at the repository root. Nothing in the historical run was modified.
