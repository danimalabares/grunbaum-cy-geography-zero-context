# Kapustka degree-20 comparison (2026-09-11 … 2026-09-17)

Does the Grünbaum–Sreedharan Stanley–Reisner scheme `SR(M) ⊂ P⁷` admit a smoothing
whose smooth fibres lie in the deformation family of G. Kapustka's degree-20
Calabi–Yau threefold (Table 1 No. 8 of [arXiv:1010.3895](https://arxiv.org/abs/1010.3895))?

**Read [`REPORT.md`](REPORT.md) first**; the verdict is its §8.
Literature ledger: [`SOURCES.md`](SOURCES.md).
Gaps and failed/omitted searches: [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).
A compact technical walkthrough (ideals, linear systems, the graded ring) is in
[`DANI_EXPLANATION.md`](DANI_EXPLANATION.md).
Reproduction: [`REPRODUCE.md`](REPRODUCE.md). Integrity: `HASH_MANIFEST.json`.

This run concerns the **sphere problem** only. It uses nothing from the `CP²₉`
calculation, from `computations/crystallographic-links/`, or from the DGLA lineage,
and it changes no status label recorded in `PROOFS.md`.

## One-paragraph summary

The comparison family is pinned down and verified independently: it is the smoothing
of the primitive type II contraction of `D′ ≅ P¹×P¹` on a small resolution of a
44-nodal `(2,2,3)` complete intersection in `P⁶` containing the doubly projected
degree-8 del Pezzo surface, and it has exactly the invariants the repository records
for its smooth fibre, `(H³, c₂·H, h⁰(H), h¹¹, h¹², χ, ρ) = (20, 56, 8, 1, 31, −60, 1)`.
But its *polarised* model is not a subvariety of `P⁷`: the contracted threefold `Ybar`
has one singular point, analytically `(3-fold ODP)/±1`, of multiplicity 8 and embedding
dimension **9**, so it needs `P(1⁸,2²)`, and the `P⁷`-image is non-normal with Hilbert
polynomial `(10/3)n³+(14/3)n − 2`. Meanwhile *every* smoothing of `SR(M)` is
automatically an arithmetically Gorenstein family inside `P⁷` (proved here from
flatness alone). The whole question therefore reduces to one property of Kapustka's
family — that its general member be arithmetically Gorenstein in `P⁷` — which is
asserted nowhere in the literature, which is exactly the property that the tool
producing the `P⁷` models of the neighbouring degree-17 and -18 families (Kapustka's
Lemma 2.2) fails to deliver here, and which we show **fails to first order**: no
first-order deformation of the contracted threefold inside `P(1⁸,2²)` reaches a `P⁷`,
and in the local model of the smoothing the smooth fibre always lies on a quadric.
The verdict is therefore **unresolved but with all the evidence pointing to no**; the
one remaining computation is named in `REPORT.md` §8.3.
