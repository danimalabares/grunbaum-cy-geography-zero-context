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

### Historical runs (2026-09-08)

Three earlier exploratory runs on the sphere problem live under `runs/`:
`astra-daytime-2026-09-08`, `astra-computation-2026-09-08`, `astra-all-nighter-2026-09-08`
(fixed S₃-Hilbert chart, a specified smooth algebraic-number fibre within the source-certificate
trust boundary, fifteen isolated (−1,−1) lines, exact exclusions of several finite-ansatz
models). They carry their own hash manifests and `REPRODUCE.md`. Their publication and indexing
is being completed in a following commit; until then they are present only in the local
workspace, and nothing in the sphere reports or in the CP²₉ run depends on them.

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
outside `runs/`; each run carries its own manifest). The CP²₉ run is
reproduced by the commands in its `REPRODUCE.md` (about five minutes with
Macaulay2 1.20 and Python 3).

## License

No license has been added. In the absence of a license, normal copyright
restrictions apply to reuse beyond what applicable law permits.
