# Grünbaum CY geography — zero-context workspace

Reproducible research workspace built on the zero-context proof packet
`grunbaum-zero-context-proof` (immutable source commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`). It contains verified exact
computations, deductions with explicitly stated hypotheses, literature
comparisons, failed computations, and open questions. It is **not** a finished
classification of degree-20 Calabi–Yau threefolds and **not** an independently
refereed proof of the source packet's smoothing theorem.

## Two distinct problems

| | Sphere problem (main line) | CP²₉ fourfold calculation (2026-09-09) |
|---|---|---|
| Object | Stanley–Reisner ring of the Grünbaum–Sreedharan eight-vertex 3-sphere; `X ⊂ P⁷`, claimed smooth degree-20 Calabi–Yau **threefold** | Stanley–Reisner ring `A` of the nine-vertex triangulation of `CP²` (Chapoton–Manivel, arXiv:1109.6490 §5); `Proj A ⊂ P⁸`, a non-Cohen–Macaulay **fourfold** |
| Question | Extract and study the packet's deformation; geography of the smooth fibre | Does the packet's equivariant formal-lifting lemma apply to `A`? |
| Where | `reports/`, `equations/`, `computations/`, `ledger/` | `runs/cp2-nine-vertex-equivariant-t2-2026-09-09/` |

The CP²₉ computation reuses only the *method* (the lemma in the packet's
`deformation/EQUIVARIANT_FORMAL_LIFT.md` §3). It is not part of the sphere's
smoothing argument and proves nothing about the threefold.

## Proof index

**[`PROOFS.md`](PROOFS.md)** lists every result in this repository with its statement, proof
location, certificates, reproduction command and status (established, PROVED within a stated
trust boundary, CONDITIONAL, OPEN, FAILED). Start there.

## Index

### Principal results on the sphere problem

- [`STATUS.md`](STATUS.md) — one-page status of every component.
- [`reports/DEFORMATION_EQUATIONS.md`](reports/DEFORMATION_EQUATIONS.md) — the extracted first-order deformation, the 109-column tangent basis, the 56-dimensional coordinate orbit, the equivariant six-jet.
- [`reports/GEOGRAPHY.md`](reports/GEOGRAPHY.md) — Hilbert data, local deformation bounds, and what requires a smooth fibre.
- [`reports/ABEL_MATHEMATICAL_FACTS.md`](reports/ABEL_MATHEMATICAL_FACTS.md) — verified facts and objectives.
- [`reports/LITERATURE_SOURCES.md`](reports/LITERATURE_SOURCES.md) — primary-source comparison, kept separate from packet-internal deductions.
- [`equations/`](equations/) — exported first-order map and six-jet (JSON, TSV, Macaulay2, TeX).
- [`ledger/CLAIMS.yaml`](ledger/CLAIMS.yaml), [`ledger/DEPENDENCIES.md`](ledger/DEPENDENCIES.md), [`ledger/COVERAGE.md`](ledger/COVERAGE.md) — claim ledger with evidence boundaries.
- [`computations/DEVELOPMENT_FAILURES.md`](computations/DEVELOPMENT_FAILURES.md) — failed and quarantined computations.
- [`PROVENANCE.md`](PROVENANCE.md), [`PUBLICATION.md`](PUBLICATION.md) — source freeze, hash locks, publication audit.

### CP²₉ equivariant-obstruction computation (verified 2026-09-09)

Directory: [`runs/cp2-nine-vertex-equivariant-t2-2026-09-09/`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/)
— [`RESULTS.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/RESULTS.md),
[`REPRODUCE.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/REPRODUCE.md),
[`PUBLICATION_VERIFICATION.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/PUBLICATION_VERIFICATION.md),
[`CHECKPOINT.md`](runs/cp2-nine-vertex-equivariant-t2-2026-09-09/CHECKPOINT.md).

Exact results for `A = QQ[x_1..x_9]/I_Δ` (all verified in Macaulay2 and independently re-verified in exact rational arithmetic in Python):

| quantity | value |
|---|---|
| embedded graded tangent space `Hom_S(I,A)₀` | 93 |
| intrinsic graded cotangent `T¹(A/QQ)₀` (93 minus the 72-dimensional coordinate orbit) | 21 |
| graded obstruction space `(T²_A)₀` | 126 |
| `S₃`-invariant obstructions (`S₃` = stabiliser of vertex 9) | 14 |
| `Aut(Δ)`-invariant obstructions (`|Aut(Δ)| = 54`) | 0 |
| `Aut(Δ)`-invariant embedded tangent directions | 5 |
| … of which coordinate changes | 3 |
| … genuine invariant intrinsic first-order directions | 2 |

Consequences, exactly as established: the lemma's hypothesis `T²^H = 0` fails for the vertex
stabiliser `S₃` and holds for the full group `Aut(Δ)`. Each of the two genuine `Aut(Δ)`-invariant
directions therefore extends to an all-orders `Aut(Δ)`-equivariant (hence `S₃`-equivariant) flat
graded deformation of `A`, and `Proj` of it is a flat formal projective family in `P⁸`. Not
established: explicit equations of any such deformation, an explicit two-parameter family,
smoothness of any generic fibre, the identification of the full Hilbert deformation functor at
`Proj A`, and the fate of the other `S₃`-invariant directions. **Smoothability of `Proj A` is
undecided.** An optional cross-check (rank of the second-order Kuranishi quadrics) was left
unfinished and is not used.

### Crystallographic quotients, vertex links and SR smoothings (2026-09-11 … 2026-09-16)

Directory: [`computations/crystallographic-links/`](computations/crystallographic-links/) —
[`REPORT.md`](computations/crystallographic-links/REPORT.md),
[`SOURCES.md`](computations/crystallographic-links/SOURCES.md),
[`OPEN_QUESTIONS.md`](computations/crystallographic-links/OPEN_QUESTIONS.md),
[`README.md`](computations/crystallographic-links/README.md) (one reproduction command:
`python3 scripts/run_all.py` inside the directory).

The five complex crystallographic groups with quotient `CP²` other than the Kühnel row `(3,3)₀`
(Kaneko–Tokunaga–Yoshida, Theorem 1): the four rows `(m,1)₀`, `m = 2,3,4,6`, all descend, through verified
`Γ`-invariant rectilinear triangulations of `C²`, to one and the same triangulation, Bagchi–Datta's ten-vertex
`CP²₁₀`, whose two vertex links are a neighbourly 9-vertex 3-sphere (degree 27 in `P⁸`) and a 22-facet
3-sphere (degree 22 in `P⁸`); no smoothing result for either link exists (degree-0 `T¹`, `T²` and invariant
parts computed exactly; nothing smoothed). For `(4,2)₁` no compatible triangulation was found (three exact
negative results, including a counting obstruction for the vertex-minimal model). The `CP²₉` link is verified
to be the sphere of the sphere problem, and the `S₃`-invariant `T²₀` of its Stanley–Reisner ring is
recomputed as `0`.

### CP²₉ normal-sections dimension audit (historical 2026-09-10)

[`computations/cp29-normal-sections/`](computations/cp29-normal-sections/) packages the completed exact normal-sheaf
section calculation. It obtains \(h^0(N_{X/\mathbf P^8})=93\); against the relevant 84-dimensional smooth embedded
Kummer locus, this gives a compatible bound and **does not** obstruct smoothability. The historical audit is retained in
[`runs/cp2-nine-hilbert-dimension-audit-2026-09-10/`](runs/cp2-nine-hilbert-dimension-audit-2026-09-10/).

### Kapustka degree-20 comparison (2026-09-17)

Directory: [`runs/kapustka-degree20-comparison-2026-09-11/`](runs/kapustka-degree20-comparison-2026-09-11/) —
[`REPORT.md`](runs/kapustka-degree20-comparison-2026-09-11/REPORT.md),
[`SOURCES.md`](runs/kapustka-degree20-comparison-2026-09-11/SOURCES.md),
[`OPEN_QUESTIONS.md`](runs/kapustka-degree20-comparison-2026-09-11/OPEN_QUESTIONS.md),
[`REPRODUCE.md`](runs/kapustka-degree20-comparison-2026-09-11/REPRODUCE.md).

Does `SR(M)` have a smoothing whose smooth fibres lie in the deformation family of
G. Kapustka's degree-20 Calabi–Yau threefold (Table 1 No. 8 of
[arXiv:1010.3895](https://arxiv.org/abs/1010.3895))? **Verdict: unresolved**, with the
question reduced to one property of Kapustka's family and a first-order obstruction to
that property. Established in the run, independently of every trust boundary: Kapustka's
Table 1 is reproduced exactly (rows 1–8) and its row 8 verified computationally
(44 reduced nodes, `(H³,c₂·H,h⁰(H),h¹¹,h¹²,χ,ρ) = (20,56,8,1,31,−60,1)` — the same
invariants as the repository's smooth fibre); the *polarised* model of that family is
**not** in `P⁷` (the contracted threefold has a point of embedding dimension 9, namely
`(3-fold ODP)/±1`, and lives in `P(1⁸,2²)`, its `P⁷`-image being non-normal with Hilbert
polynomial `(10/3)n³+(14/3)n−2`); and *every* smoothing of `SR(M)` is an arithmetically
Gorenstein family in `P⁷`, so the question reduces to whether Kapustka's general member
is arithmetically Gorenstein in `P⁷` — which fails to first order. Nothing in §1–§7 of
`PROOFS.md` changes.

### Space groups with quotient S³ and Kummer Calabi–Yau threefolds — stage 1 (2026-09-17)

Directory: [`computations/space-group-cy3/`](computations/space-group-cy3/) —
[`REPORT.md`](computations/space-group-cy3/REPORT.md),
[`SOURCES.md`](computations/space-group-cy3/SOURCES.md),
[`OPEN_QUESTIONS.md`](computations/space-group-cy3/OPEN_QUESTIONS.md),
[`README.md`](computations/space-group-cy3/README.md) (one reproduction command:
`python3 scripts/run_all.py` inside the directory; Python 3 only, about one minute).

Audit of the claim that the 14 symmorphic members (16, 21, 22, 89, 97, 149, 150, 155, 177, 195, 196,
207, 209, 211) of Johnson–Burnett–Dunbar's list of 35 space groups with real orbifold quotient `S³` are
covered by the published linear Kummer construction (Andreatta–Wiśniewski, Donten-Bury, Burek).
Verified: the 35-list equals the label set of JBD's Figure 2.8; the 14 are exactly the symmorphic members
(two independent ITA databases agree coset by coset); each point group is conjugate in `GL(3,Z)`, by an
explicit certificate, to exactly one of the 16 published Z-classes (with I222 and I23 outside the list
completing a bijection, pairwise non-conjugacy re-established); one exact implementation of the orbifold
Hodge numbers of `A_τ/G`, `A_τ = C³/(Λ+τΛ)`, reproduces the published values in all cases —
`(h¹¹,h²¹) = (51,3), (21,9), (15,3), (36,6), (15,3), (15,15), (15,15), (7,7), (21,9), (19,3), (7,3),
(20,6), (11,3), (11,3)` — with Euler numbers checked by an independent DHVW count. A projective crepant
resolution exists (Bridgeland–King–Reid) with these Hodge numbers (Yasuda / Batyrev); results are
independent of `τ`, origin, setting and basis. Fourteen labels give ten Hodge pairs; deformation
equivalence between different groups is open. The 21 non-symmorphic groups are recorded as pending with
their exact affine generators. This computation is independent of the sphere problem.

### Historical runs on the sphere problem (2026-09-08)

Three exploratory runs, published in full with their own manifests and `REPRODUCE.md` files
(status labels unchanged; see [`PROOFS.md`](PROOFS.md) §2–§4):

- [`runs/astra-daytime-2026-09-08/`](runs/astra-daytime-2026-09-08/) — finite `S₃`-fixed Hilbert chart (270 × 270 minor of determinant −1, 21 free directions), Picard/Hodge reductions, exact inequivalence of the DGLA and zero-context tangent classes; claims D01–D17 in its `CLAIM_LEDGER.md`.
- [`runs/astra-computation-2026-09-08/`](runs/astra-computation-2026-09-08/) — the geography theorem `(h¹¹,h²¹) = (1,31)`, `ρ = 1`, component dimension 94, and a specified smooth number-field fibre with all sixteen cubics displayed, both **within the accepted zero-context smoothing trust boundary**; several exact negative results.
- [`runs/astra-all-nighter-2026-09-08/`](runs/astra-all-nighter-2026-09-08/) — audit of that fibre, fifteen isolated `(−1,−1)` lines, exact exclusion of several finite-ansatz models; no new manageable exact model.

1431 large search-checkpoint files of the computation run (about 116 MB) are in the GitHub Release
`historical-runs-2026-09-08-large-artifacts` rather than in Git, and six files are withheld; both
sets are listed with their manifest hashes in [`runs/PUBLICATION_OMISSIONS.json`](runs/PUBLICATION_OMISSIONS.json).
Nothing in the sphere reports or in the CP²₉ run depends on them.

## Reproduction

The immutable source is `grunbaum-zero-context-proof` at commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`. By default the scripts expect it
as the sibling directory `../grunbaum-zero-context-proof`; set
`GS_ZERO_CONTEXT_SOURCE=/path/to/grunbaum-zero-context-proof` to use another
clean checkout at the same commit. This workspace neither uses nor imports
results from `fable-dgla-only` or `sr-project/main/rl`.

Run the complete deterministic audit suite for the sphere problem with:

```sh
python3 scripts/run_checks.py
```

Then verify the frozen core-workspace outputs with
`python3 scripts/make_manifest.py --verify` (this manifest covers everything
outside `runs/`) and every run's own manifest with
`python3 scripts/verify_runs.py`. Each run directory has a `REPRODUCE.md`;
the CP²₉ run reproduces in about five minutes with Macaulay2 1.20 and
Python 3. The 2026-09-08 runs' guarded entry points are deliberately tied
to their original session windows and refuse to launch afterwards; their
small independent Python checks run directly (see `PROOFS.md` §3).

## License

No license has been added. In the absence of a license, normal copyright
restrictions apply to reuse beyond what applicable law permits.
