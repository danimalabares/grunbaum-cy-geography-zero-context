# Kapustka degree-20: the nine-dimensional tangent space and what it means (2026-09-18)

Follow-up to [`../kapustka-degree20-comparison-2026-09-11/`](../kapustka-degree20-comparison-2026-09-11/)
(left unchanged). One limited question, answered in a short note meant to be read before a
conversation with G. Kapustka:

> Why does the singular contraction `Ybar` in Kapustka's degree-20 construction
> ([arXiv:1010.3895](https://arxiv.org/abs/1010.3895), Table 1 No. 8) fail to embed into `P⁷`,
> and what does that tell us about comparing its smoothings with `SR(M)`?

**Deliverable:** [`DANI_NOTE.pdf`](DANI_NOTE.pdf) (4 pages; source `DANI_NOTE.tex`, compiled with
pdflatex, TeX Live, two passes, logs in `logs/pdflatex_pass*.log`).

Supporting records: [`SOURCES.md`](SOURCES.md) (papers read, verbatim quotations, SHA-256 of the
PDFs, which are not committed), [`CHECKS.md`](CHECKS.md) (the four Macaulay2 scripts, runtimes,
decisive output lines, what is characteristic-zero and what is finite-field),
[`HP_SECTIONS.md`](HP_SECTIONS.md) (heap-project sections that fix the vocabulary assumed, and the
notions introduced), [`CORRECTIONS.md`](CORRECTIONS.md) (seven corrections/clarifications to the
2026-09-11 run, none reversing a conclusion), `HASH_MANIFEST.json` (integrity).

## Summary of the answer

* **Established (characteristic zero).** `Ybar` has one singular point `P`. Its Zariski tangent
  space has dimension `≥ 9`, by the theorem on formal functions applied to the contraction
  `φ: X → Ybar` of `D' ≅ P¹×P¹` with `O_{D'}(−D') = O(2,2)` and `H¹(O(2,2)) = 0`
  (`DANI_NOTE` §2, Step 1). Hence `Ybar` has no closed embedding into `P⁷` or any smooth 7-fold,
  and the ample divisor `T` with `h⁰(T) = 8` is not very ample (§3, Prop. 3.1).
* **Established via a published theorem.** `dim T_P Ybar = 9`, `mult_P Ybar = 8`, and
  `(Ybar, P)` is analytically the anticanonical cone over `P¹×P¹`, i.e. `{xy = zw}/±1`: Gross,
  *Deforming Calabi–Yau threefolds*, Prop. 5.4 (Grauert linearisation), with Reid's theorem that a
  primitive type II contraction is the blow-up of the point. This is the theorem the 2026-09-11 run
  did not name (`CORRECTIONS.md` item 2). The cone/quotient identification is verified over `QQ`
  (`logs/c02`).
* **Established (characteristic zero, general centre).** The image `Y ⊂ P⁷` of the eight sections
  is non-normal at `P` with `δ = 2`, because the seven sections vanishing at `P` see only the
  7-dimensional space of linear forms of `P⁶` inside the 9-dimensional `H⁰(O(2,2))`, while
  `h¹(I_S(k)) = 0` for `k ≥ 2` (`logs/c03`, over `QQ`). So `χ(O_Y(n)) = (10/3)n³ + (14/3)n − 2`
  and `[Y]` is in a different Hilbert scheme from `[SR(M)]`. Kapustka's own Remark 3.3 states the
  non-normality for the analogous degree-15 row.
* **Why it does not persist.** Tangent dimension is upper semicontinuous and equals 3 on smooth
  fibres; the local model `{xy − zw = t}/±1` (Gross §5.5) goes from embedding dimension 9 to 3
  (`logs/c02`). The question that matters for the smooth fibres `Y_t`, whether the eight sections
  of `T_t` embed `Y_t` with projectively normal image (property `(★)` of the earlier run), is
  neither implied nor excluded by the singular model.
* **Relevance to `SR(M)`.** From the monomial ideal: `SR(M)` is arithmetically Gorenstein in
  `P⁷` with h-vector `(1,4,10,4,1)` (`logs/c01`), and every *embedded* deformation of it in `P⁷`
  keeps that (§4, Prop. 4.1, re-proved). The singular models are incomparable; any comparison
  goes through `(★)`. Conditional statements only; the smoothing of `SR(M)` is not assumed, and
  nothing here says Kapustka's `Y_t` is non-aG or deformation-inequivalent to an `SR(M)` smoothing.
* **Next question (for Kapustka).** Is `Sym²H⁰(Y_t, T_t) → H⁰(Y_t, 2T_t)` an isomorphism for
  general `t`; equivalently, does the general member lie on no quadric of `P⁷`?

Not done here, by design: no deformation-equivalence search, no second-order (Kuranishi)
computation, no re-derivation of the earlier run's first-order obstruction.

## Reproduction

Software: Macaulay2 1.20 (`/Applications/Macaulay2-1.20/bin/M2`), pdflatex. From this directory:

```sh
M2 --script scripts/c01_srm_sphere.m2          > logs/c01_srm_sphere.log          2>&1   #  1 s, QQ
M2 --script scripts/c02_anticanonical_cone.m2  > logs/c02_anticanonical_cone.log  2>&1   #  1 s, QQ
M2 --script scripts/c03_projected_surface_QQ.m2 > logs/c03_projected_surface_QQ.log 2>&1 #  4 min, QQ
M2 --script scripts/c04_ybar_charts_F32003.m2  > logs/c04_ybar_charts_F32003.log  2>&1   # 30 s, F_32003; reads ../kapustka-degree20-comparison-2026-09-11/data/
pdflatex DANI_NOTE.tex && pdflatex DANI_NOTE.tex
python3 scripts/hash_run.py                     # rewrites HASH_MANIFEST.json
```

Expected decisive lines are listed in `CHECKS.md`. Input commit of the repository:
`ff3c5040257cca9161dbb76795b7d9a240f31374`.
