# Sources

Access date: 2026-09-17. Every statement attributed to a source below was read in the
primary source (arXiv PDF text extracted locally); quotations are verbatim.

## S1 — the comparison family (primary)

- G. Kapustka, *Projections of del Pezzo surfaces and Calabi–Yau threefolds*,
  Adv. Geom. **15** (2015), no. 2, 143–158. Stable source:
  [arXiv:1010.3895](https://arxiv.org/abs/1010.3895), **v5 (4 Mar 2015)**, 22 pp.
- Inspection state: `inspected-primary` (full text).
- Used: Table 1 (p. 2), Proposition 2.1, Corollary 2.2, §3 (Prop. 3.2, Rem. 3.3,
  Thm. 3.4), Lemma 4.1, Theorem 4.4, §5 (Theorem 5.1 and its proof, Prop. 5.3,
  Prop. 5.6, Rem. 5.7), Appendix 1 (the census of `h¹¹ = 1` Calabi–Yau threefolds).
- **Table 1 row 8 (the comparison family), verbatim columns:**
  `No = 8`, `deg D′ = 8`, `X′ = X′_{2,2,3}`, `sing X′ = 44 ODP`, `χ(Y_t) = −60`,
  `H³ = 20`, `h⁰(H) = 8`. Appendix 1 row: `20 | 1 | 31 | −60 | 56 | 8 | | Table 1`.
- **Theorem 5.1** (verbatim): "There exist a Calabi–Yau threefold with Picard group of
  rank 1 of degree 19 (resp. 20) with h1,2 = 23 (resp. h1,2 = 31)."
- **Internal inconsistency recorded, not corrected by us.** The proof of Theorem 5.1
  says: "we find explicitly the centers of projections such that the surfaces ~~D8 ⊂ P6
  and ~D7 ⊂ P6 are embedded into nodal Calabi–Yau threefolds in P6 which are complete
  intersections X1 (resp. X2) of two quadrics and a cubic with 37 (resp. 44) nodes."
  Table 1, Appendix 1, the Betti table printed inside that same proof, the
  Thom–Porteous count and the Macaulay2 computation of this run all give the opposite
  pairing (`~~D₈ ↔ 44 nodes ↔ degree 20 ↔ h¹² = 31`; `~D₇ ↔ 37 ↔ degree 19 ↔ h¹² = 38`).
  The value "23" in the statement belongs to the degree-17 row 6. Proposition 5.6 has
  the same kind of transposition (it reports `(1,31)` and `(1,38)` where Table 1 rows 5
  and 6 give `(1,31)` for `~~D₇` and `(1,23)` for `L_P`). We use Table 1 + Appendix 1,
  which are mutually consistent and are reproduced exactly in
  `scripts/verify_kapustka_table1.py`.
- Applicability: this run compares against **Table 1 No. 8** only.

## S2 — the mechanism that produces `P⁷` models (primary)

- G. Kapustka, *Primitive contractions of Calabi–Yau threefolds II*, J. London Math.
  Soc. (2) **79** (2009) 259–271. Source: [arXiv:0707.2488](https://arxiv.org/abs/0707.2488) v3.
- Used: Theorem 2.1 (nodality), Theorem 2.2 (`ρ = 2`), Theorem 2.3, Lemma 2.1,
  **Lemma 2.2**, Tables 1–6, §2.3.
- **Lemma 2.2** (verbatim): "Let `i : Y ↪ Pⁿ` be a smoothable (normal Gorenstein)
  Calabi–Yau threefold. Then `Y` can be smoothed inside `Pⁿ`." Its proof needs
  `dim sing(Y) = 0`, `Y` normal Gorenstein, and concludes from `H¹(Θ_{Pⁿ}|_Y) = 0`.
  **The hypothesis "`i : Y ↪ Pⁿ`" is an embedding**; it is the step that fails for the
  degree-20 family at `n = 7` (§4 of `REPORT.md`).
- Also used: "For each of the first 13 Calabi–Yau threefolds `Y_t` presented in Table 1,
  the linear system `|H|` is very ample" — the paper asserts very ampleness only where
  the del Pezzo is anticanonically embedded in a linear subspace.
- Theorem 2.3: "if `i = 6` there are two different smoothings … the versal Kuranishi
  space of a cone over a del Pezzo surface of degree 6 has two components".

## S3 — the smoothing theorem

- M. Gross, *Deforming Calabi–Yau threefolds*, Math. Ann. **308** (1997) 187–220.
  Source: [arXiv:alg-geom/9506022](https://arxiv.org/abs/alg-geom/9506022) v2.
- **Theorem 5.8** (verbatim): "Let `π : X̃ → X` be a primitive type II contraction with
  exceptional divisor `E`. Then `X` is smoothable unless (1) `E ≅ P²` or (2) `E ≅ F₁`."
  Here `E = D′ ≅ P¹×P¹`, so the hypothesis is met and `Ybar` is smoothable. (Theorem 4.3
  and the "good singularity" hypothesis are verified inside Gross's §5 for this class.)

## S4 — the lists of arithmetically Gorenstein Calabi–Yau threefolds in `P⁷`

- S. Coughlan, Ł. Gołębiowski, G. Kapustka, M. Kapustka, *Arithmetically Gorenstein
  Calabi–Yau threefolds in `P⁷`*, Electron. Res. Announc. Math. Sci. 23 (2016) 52–68.
  Source: [arXiv:1609.01195](https://arxiv.org/abs/1609.01195) v1.
- Table 1 has eleven entries; the only degree-20 entry is no. 11,
  `h¹¹ = 2`, `h¹² = 34`, "3 × 3 minors of 4 × 4 matrix with linear forms in `P⁷`".
  §4.9 (verbatim): "**Degree 20.** It seems that this case is the most difficult to
  classify. **Only one example is known**, defined by 3 × 3 minors of a 4 × 4 matrix of
  linear forms in `P⁷`. … Recall that the Hodge numbers in this case are `h¹¹(X) = 2`
  and `h¹²(X) = 34`." And: "We have evidence that our Table is complete for degrees
  18, 19 and 20."
- Degree 17 no. 4 (`h¹² = 55`) is recorded as "constructed using unprojection of a del
  Pezzo of degree 5 in a complete intersection 2, 2, 3 in [K1]", and degree 18 nos. 7, 8
  (`h¹² = 46, 45`) as the degree-6 cases of [K1] — i.e. exactly the `d ≤ 6` rows of
  the table in `REPORT.md` §4.3. Degrees 19 and 20 of that table are **absent**.
- Degree 19 of CGKK (a *different* construction, `h¹¹ = 2`) is produced as an
  unprojection of a **linearly normal** `S₆ ⊂ Y₁₃ ⊂ P⁶`, and the passage to `P⁷` is
  justified verbatim by: "The fact that these smoothings can be performed by
  non-degenerate aG Calabi–Yau threefolds in `P⁷` follows from **[K1, Lemma 2.2]**."

- G. Kapustka, M. Kapustka, K. Ranestad, H. Schenck, M. Stillman, B. Yuan,
  *Quaternary quartic forms and Gorenstein rings*, Memoirs AMS **317** (2026).
  Source: [arXiv:2111.05817](https://arxiv.org/abs/2111.05817).
  Artinian reductions of degree-20 arithmetically Gorenstein Calabi–Yau threefolds in
  `P⁷` are exactly the quaternary quartics of type `[000]` (h-vector `(1,4,10,4,1)`).
  §8, type `[000]` (verbatim): "There are several families of Calabi-Yau threefolds of
  degreee 20 whose general Artinian reduction are quartic forms `F` of rank 10. We first
  describe briefly a well known complete family of smooth Calabi-Yau threefolds of
  degree 20, and then construct another family of nodal non-smoothable Calabi-Yau
  threefolds of degree 20." Proposition 8.4 gives the 2-nodal non-smoothable one;
  "Smooth Calabi-Yau threefolds of degree 20 in `P⁷` can be defined by 3 × 3 minors of a
  4 × 4 matrix of linear forms. These are liftings of special quartic forms `F` of type
  `[000]`." **Question 8.5** (verbatim): "Describe the quartics corresponding to AG
  rings of type `[000]` that lift to smooth threefolds."
- Applicability: these are the two published enumerations of arithmetically Gorenstein
  Calabi–Yau threefolds of degree 20 in `P⁷`. Neither contains a family with
  `(h¹¹,h¹²) = (1,31)`; neither asserts that none exists. G. Kapustka is an author of
  both and of S1.

## S5 — consulted, not used as theorem-level evidence

- F. Tonoli, *Construction of Calabi–Yau 3-folds in `P⁶`*, J. Algebraic Geom. 13 (2004)
  209–232 — the degree-14…17 families that Kapustka's rows 2, 4, 5, 6 match numerically.
- Y. Namikawa, *Deformation theory of Calabi–Yau threefolds and certain invariants of
  singularities*, J. Algebraic Geom. 6 (1997) 753–776 — Theorem 10, used by CGKK to
  count the smoothings in their degree-19 case.
- Schenck–Stillman–Yuan, *Calabi–Yau threefolds in `Pⁿ` and Gorenstein rings*
  ([arXiv:2011.10871](https://arxiv.org/abs/2011.10871)).

## S6 — repository inputs (read-only)

- Input commit `09953cefe987f304e1e8549a50df3b937747470c`.
- `scripts/verify_geography.m2` (the frozen `I_M`), `PROOFS.md`, `reports/GEOGRAPHY.md`,
  `runs/astra-daytime-2026-09-08/FIXED_CHART.md`,
  `runs/astra-computation-2026-09-08/GEOGRAPHY_THEOREM.md`,
  `runs/astra-computation-2026-09-08/RAMIFIED_FIBRE_EQUATIONS.md`,
  `runs/astra-all-nighter-2026-09-08/FIBRE_AUDIT.md`,
  `runs/astra-all-nighter-2026-09-08/MODEL.md`.
- The `CP²₉` runs and `computations/crystallographic-links/` are a **different problem**
  and are not used here; the DGLA lineage is not used here.
