# Status

Last updated: 2026-09-17 (America/Sao_Paulo), second entry of the day. Entries dated 2026-09-04 are unchanged below.

- Provenance freeze: complete. The clean source commit, tree, and decisive files are hash-locked.
- Deformation extraction: complete. The 109-column basis, independently recovered 56-dimensional coordinate orbit, ordered 53-dimensional complement, ten \(S_3\)-orbits, and selected 53-vector are recorded.
- First order: complete. The exact rational map \(y\mapsto T_1y\mapsto(g_1,\ldots,g_{16})\) agrees coefficientwise with the stored generic equivariant six-jet.
- Six-jet: complete. All sixteen generator coefficients through \(q^6\) are exported in JSON, TSV, and executable Macaulay2 form.
- Explicitness audit: complete. The packet gives an explicit six-jet, an abstract all-orders formal extension, and existential algebraization, but no finite algebraic smoothing equations. The quarantined order-four specialization is independently confirmed nonflat (affine dimension 0, degree 567 over \(\mathbb F_{101}\)).
- Geography: exact Hilbert data and local deformation bounds are complete; exact Hodge numbers, Picard group, fundamental group, smoothing-component structure, and rational liaison remain open.
- Literature comparison: primary-source comparison completed and kept separate from packet-internal deductions. Conditional on the packet/package identification of the full embedded Kuranishi equations, the resulting local bound 94 excludes the known general determinantal \((h^{1,1},h^{2,1})=(2,34)\) family, whose smooth embedded Hilbert dimension is 97.
- Reproducibility: all source, deformation, export, Hilbert, Kuranishi, formula, failed-control, and explicitness checks pass.

No source repository was modified by the 2026-09-04 work.

## 2026-09-09 — CP²₉ equivariant-obstruction computation (separate problem)

- `runs/cp2-nine-vertex-equivariant-t2-2026-09-09/`: for the nine-vertex triangulation of CP² (a fourfold in P⁸, not the sphere's threefold), dim Hom_S(I,A)₀ = 93, intrinsic T¹ = 21, dim (T²)₀ = 126; invariant obstructions: 14 for the vertex stabiliser S₃, 0 for the order-54 automorphism group; 5 invariant embedded tangent directions, 3 of them coordinate changes, 2 genuine, each extending to all orders equivariantly. Smoothability undecided. Verifiers re-run before publication with byte-identical outputs (`PUBLICATION_VERIFICATION.md`); four textual corrections to `RESULTS.md` are marked inline.
- Optional quadratic-obstruction cross-check in that run: unfinished, not restarted, not used.
- `scripts/make_manifest.py` now excludes `runs/` (each run has its own manifest); `computations/SHA256SUMS` regenerated accordingly.

## 2026-09-09 — publication of all existing proof material

- `PROOFS.md` added as the proof index (statement, location, certificates, reproduction, status for every result; labels as recorded, none upgraded).
- The three 2026-09-08 runs (`runs/astra-*`) are now committed, minus 1431 large search-checkpoint files (GitHub Release `historical-runs-2026-09-08-large-artifacts`) and six withheld files; see `runs/PUBLICATION_OMISSIONS.json`. `scripts/verify_runs.py` verifies every run manifest allowing exactly those omissions.
- Verified in this pass: all four run manifests (100, 1943, 270, 38 entries; 0 mismatches), the two independent Python checks of the computation run (product minor, ramified export; certificates identical to the shipped ones), the sphere check suite `run_checks.py` (nine mathematical checks pass), the publication audit, and the presence of all six external commits on GitHub. Not re-run: the guarded replay entry points of the 2026-09-08 runs (they refuse by their historical date guards, as designed) and every heavy search.

## 2026-09-11 … 2026-09-16 — crystallographic quotients, vertex links, SR smoothings (separate problem)

- [Crystal: `computations/crystallographic-links/`](https://github.com/danimalabares/crystal/tree/main/computations/crystallographic-links/): the five rows of Kaneko–Tokunaga–Yoshida other than `(3,3)₀`. Rows `(m,1)₀`, `m = 2,3,4,6`: verified `Γ`-invariant rectilinear lifts with simplicial quotient `CP²₁₀` (Bagchi–Datta), two link types (degrees 27 and 22 in `P⁸`), exact degree-0 `T¹`/`T²` and invariant parts; smoothability of the link SR schemes **open** (nothing found in the literature, nothing asserted). Row `(4,2)₁`: no compatible triangulation located; three exact negative results. Row `(3,3)₀`: Morin–Yoshida's group verified conjugate to `(3,3)₀[τ=ω]`; the `CP²₉` link verified equal to the sphere of the sphere problem; `(T²₀)^{S₃} = 0` recomputed. Reproduction: `python3 scripts/run_all.py` in that directory in a Crystal checkout.
- `computations/SHA256SUMS` regenerated to include the new directory.

## 2026-09-17 — Kapustka degree-20 comparison (sphere problem)

- `runs/kapustka-degree20-comparison-2026-09-11/`: does `SR(M)` have a smoothing whose fibres lie in
  G. Kapustka's degree-20 family (arXiv:1010.3895, Table 1 No. 8)? **Unresolved.** Established without
  any trust boundary: rows 1–8 of that Table 1 are reproduced exactly from three closed formulas; row 8 is
  verified computationally (`~~D₈ ⊂ P⁶` with the printed Betti table, a 44-nodal `(2,2,3)` complete
  intersection, `(H³,c₂·H,h⁰(H),h¹¹,h¹²,χ,ρ) = (20,56,8,1,31,−60,1)`, matching the repository's smooth
  fibre); the contracted threefold `Ȳ` of that family has a point of multiplicity 8 and **embedding
  dimension 9** (`(3-fold ODP)/±1`), so `Ȳ ⊄ P⁷` and its `P⁷`-image is non-normal with Hilbert polynomial
  `(10/3)n³+(14/3)n−2`, while the normal model `Ȳ ⊂ P(1⁸,2²)` has the Hilbert function of `k[M]`;
  and **every** smoothing of `SR(M)` is an arithmetically Gorenstein family in `P⁷`, so the question
  reduces to whether Kapustka's general member is arithmetically Gorenstein in `P⁷` — which **fails to
  first order**. The remaining obstacle is a second-order Kuranishi term, stated exactly in that run's
  `OPEN_QUESTIONS.md`.
- No status label of `PROOFS.md` §1–§7 is changed; `PROOFS.md` gains §8 for this run.
- `computations/SHA256SUMS` regenerated (three entries changed: `PROOFS.md`, `README.md`, `STATUS.md`);
  `python3 scripts/make_manifest.py --verify` and `python3 scripts/verify_runs.py` both pass, the latter now
  including the new run's own `HASH_MANIFEST.json` (43 entries).
- Recorded tension, not resolved: if the zero-context smoothing theorem holds, `SR(M)` smooths to a smooth
  arithmetically Gorenstein degree-20 Calabi–Yau threefold in `P⁷` with `(h¹¹,h¹²) = (1,31)`, which is
  absent from the list of Coughlan–Gołębiowski–Kapustka–Kapustka (arXiv:1609.01195) that its authors
  conjecture complete in degree 20, and bears on Question 8.5 of arXiv:2111.05817.

## 2026-09-17 — space groups with quotient S³ and Kummer Calabi–Yau threefolds, stage 1 (separate problem)

- [Crystal: `computations/space-group-cy3/`](https://github.com/danimalabares/crystal/tree/main/computations/space-group-cy3/): the 14 symmorphic members of the JBD 35-list are audited. The list is
  verified against the source (Figure 2.8 text layer); the 14 are exactly the symmorphic members (spglib
  2.7.0 and GAP CrystCat 1.1.10 agree coset by coset for all 37 groups processed); each point group is
  matched by an explicit `GL(3,Z)`-conjugator to one Donten-Bury class and one Burek group (16 ↔ 16 with the
  two controls I222, I23; pairwise non-conjugacy re-established); the orbifold Hodge numbers computed by one
  exact implementation agree with Donten-Bury's Table 2 and Burek's tables in all 16 cases and with
  Andreatta–Wiśniewski for P432; DHVW Euler check passes. Existence of a projective crepant resolution and
  the equality of its Hodge numbers with the orbifold ones are deductions from BKR Thm 1.2 and Yasuda Thm 1.5
  (hypotheses checked). Simple connectedness is a deduction relying on two theorems not re-read.
- Pending (scope of stage 1): the 21 non-symmorphic groups (generators with translation parts recorded,
  no computation), the six-dimensional toroidal-orbifold matching, deformation equivalence between groups
  with equal Hodge numbers. Cached third-party documents are not committed; `sources/MANIFEST.json` records
  URL and SHA-256.
- `computations/SHA256SUMS` regenerated to include the new directory.

## 2026-09-18 — migration to Crystal

The `crystallographic-links` and `space-group-cy3` computations now live in
[danimalabares/crystal](https://github.com/danimalabares/crystal). The original
directories contain navigation READMEs. Their exact pre-migration snapshot remains
in this repository at `dd0f3771ff3f5502a956231a4c69d896e10f4a71`.
Historical mathematical conclusions above have not been re-audited or upgraded.
Reproduction takes place in the corresponding directories of a Crystal checkout.
