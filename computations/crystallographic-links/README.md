# Crystallographic quotients of `CP²`, vertex links and Stanley–Reisner smoothings

Deliverables of the research run 2026-09-11 … 2026-09-16 (single run, Claude Fable 5.1) on the five
complex crystallographic constructions with quotient `CP²` other than the Kühnel one (Theorem 1 of
Kaneko–Tokunaga–Yoshida, *Complex crystallographic groups II*, rows `(2,1)₀, (3,1)₀, (4,1)₀, (6,1)₀,
(4,2)₁`; the known `CP²₉` is the row `(3,3)₀`).

* [`REPORT.md`](REPORT.md) — result-first report with the five-case table.
* [`SOURCES.md`](SOURCES.md) — exact references with theorem/page citations, provenance, search log.
* [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — precise gaps and concrete next computations.
* [`data/`](data/) — exact facet lists (`CP²₉` from Kühnel–Banchoff 1983; `CP²₁₀` and `(S²×S²)₁₆` from
  Bagchi–Datta arXiv:1004.3157; the packet's Grünbaum sphere), link facets and minimal nonfaces
  (`data/links/`), link automorphism groups, the lifted triangulations on finite torus covers and their
  quotients (`data/lifts/`), the crystallographic markings of `CP²₁₀` (`data/cp2_10_crystallographic_markings.tsv`).
* [`scripts/`](scripts/) — exact Python (`simplicial.py` toolkit, `build_complexes.py`, `links.py`,
  `lifts.py`, `t1_formula.py`, `prism_triangulations.py`, `four_two_one_counting.py`,
  `four_two_one_search.py`, `verify_33_identification.py`) and Macaulay2 (`link_t1_t2.m2`,
  `link_equivariant.m2`, `cp2_10_t1_t2.m2`).
* [`output/`](output/) — recorded outputs: JSON results, logs, Macaulay2 logs (`output/m2/`), the
  45-hour capped `(4,2)₁` search (`output/four_two_one_search.json`).

## Results in one paragraph

The six rows of Theorem 1 were verified against Table II of Part I; Morin–Yoshida's crystallographic
group is exactly conjugate to the row `(3,3)₀` at `τ = ω`, and Kühnel's `CP²₉` is its quotient triangulation
(link: the Brückner–Grünbaum sphere, isomorphic to the sphere of this repository's sphere problem). The four
rows `(m,1)₀`, `m = 2,3,4,6`, all admit `Γ`-invariant rectilinear triangulations of `C²` (constructed and
verified here: descent, regular action, simplicial quotient) whose quotient is one and the same complex,
Bagchi–Datta's `CP²₁₀`, with different crystallographic markings; `m = 2` uses only cone points, `m = 3,4,6`
need one free orbit of barycentres. `CP²₁₀` has two link types: a neighbourly 9-vertex sphere (degree 27 in
`P⁸`, `f = (9,36,54,27)`) at the four diagonal vertices and a 22-facet sphere (degree 22 in `P⁸`,
`f = (9,31,44,22)`) at the six others; no smoothing theorem, certificate or non-smoothability result exists
for either, and none is claimed here; the degree-0 `T¹`, `T²` and their `Aut`-invariant parts were computed
exactly (`T²₀ = 63` and `21`, invariant parts `11` and `11`). For `(4,2)₁` no compatible triangulation was
found: the `CP²₁₀` lift is not invariant under the extra order-four symmetry, the restricted `(4,1)₀` lift
has a non-simplicial quotient, and a counting argument excludes any vertex-minimal admissible
diagonalisation (48 facets on 9 vertices is impossible).

## Reproduction

```sh
python3 scripts/run_all.py
```

runs every exact check (about 3 minutes; Python 3 with `networkx` and `sympy`) and, if `M2` (Macaulay2
1.20) is on the `PATH`, the degree-0 `T¹`/`T²` and equivariant computations (about 1 minute). Logs go to
`output/*.log`, `output/m2/*.log`, a summary to `output/run_all.log`. Add `--no-m2` to skip Macaulay2 and
`--full-search` to rerun the capped `(4,2)₁` diagonalisation search (the recorded run took 45 hours; the
counting obstruction that settles the question is part of the default run).
