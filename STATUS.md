# Status

Last updated: 2026-09-09 (America/Sao_Paulo). Entries dated 2026-09-04 are unchanged below.

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
