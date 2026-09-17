# Space groups with quotient S³ and Kummer Calabi–Yau threefolds (stage 1: the 14 linear cases)

Audit run 2026-09-17 (Claude Fable 5.1). **Scope of this stage**: of the 35 three-dimensional space
groups whose real orbifold R³/Γ has underlying space S³ (Johnson–Burnett–Dunbar, Fig. 2.8), audit the
14 proposed *linear* (symmorphic) cases: membership in the list, correspondence with the published
integral matrix classes of the Kummer construction (Andreatta–Wiśniewski, Donten-Bury, Burek), and the
Hodge numbers of the crepant resolutions of `A_τ/G`, `A_τ = C³/(Λ + τΛ)`. The remaining 21 groups
are recorded as pending, with their exact affine generators.

* [`REPORT.md`](REPORT.md) — the report (conclusions first; construction, provenance, Z-class
  certificates, Hodge numbers, theorem chain, equivalent inputs, pending work).
* [`SOURCES.md`](SOURCES.md) — sources with the statements read, database provenance, search log.
* [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) — unresolved identifications, failed checks, pending items.
* [`table/space_groups_35.tsv`](table/space_groups_35.tsv), [`.json`](table/space_groups_35.json) —
  the 35-row machine-readable table (number, Hermann–Mauguin and Hall symbols, setting, primitive
  basis, centrings, point group, arithmetic class, symmorphic status, generators with translation parts
  in the primitive basis, stage-1 status, `h^{1,1}`, `h^{2,1}`, Euler number, resolution status,
  literature match, evidence).
* [`data/`](data/) — exact inputs: `spglib_operations.json` and `crystcat_generators.json` (the two
  crystallographic databases, ITA standard settings), `jbd_figure_2_8_groups.json` (the 35-list read
  from the JBD text layer), `literature_zclasses.json` (Donten-Bury Tables 1–2 and duality, Burek's
  16 groups with Hodge numbers, Andreatta–Wiśniewski's S₄ result, all parsed from the LaTeX sources).
* [`scripts/`](scripts/) — `sgcy3.py` (the single shared exact implementation: Smith normal forms,
  lattices, point groups, conjugacy certificates, orbifold Hodge numbers, DHVW Euler numbers),
  `run_all.py` (driver), and the extraction scripts `extract_spglib.py`, `extract_crystcat.g`,
  `extract_jbd_list.py`, `extract_literature.py`, `make_sources_manifest.py`.
* [`output/`](output/) — recorded outputs: `crystallographic_data.json`, `hodge_numbers_linear.json`
  (per-class fixed loci, centraliser orbits, stabilisers), `zclass_matching.json` (explicit
  conjugators, transpose control, pairwise non-conjugacy), `literature_comparison.json`, `run_all.log`.
* [`sources/MANIFEST.json`](sources/MANIFEST.json) — URL, SHA-256 and size of every cached third-party
  document (the documents themselves are not committed, following the repository convention for
  third-party material; `sources/.gitignore`).

## Principal conclusions

1. The 35-list under audit equals the label set of JBD's Figure 2.8 (read from the PDF text layer).
2. Its symmorphic members are exactly the proposed 14 (two independent ITA-derived databases, spglib
   2.7.0 and GAP CrystCat 1.1.10, agree coset by coset for all groups).
3. Each of the 14 point groups, in a primitive basis of its full translation lattice, is conjugate in
   `GL(3,Z)` to exactly one of the 16 Z-classes of Donten-Bury's Table 1 and of Burek's list, with
   explicit conjugators; with the two symmorphic groups outside the list (I222, I23) the 16 groups
   biject onto the 16 classes, whose pairwise non-conjugacy is re-established here.
4. One exact implementation of the orbifold (Chen–Ruan/Batyrev) Hodge numbers reproduces the published
   values in all 14 (+2) cases: (51,3), (21,9), (15,3), (36,6), (15,3), (15,15), (15,15), (7,7),
   (21,9), (19,3), (7,3), (20,6), (11,3), (11,3) for 16, 21, 22, 89, 97, 149, 150, 155, 177, 195, 196,
   207, 209, 211; Euler numbers checked against an independent DHVW count.
5. For all 14, `A_τ/G` has a projective crepant resolution (Bridgeland–King–Reid, Thm 1.2) whose Hodge
   numbers are the orbifold ones (Yasuda, Thm 1.5 / Batyrev, Thms 3.8 and 7.5); `h^{1,0} = h^{2,0} =
   0`; the results are independent of τ, origin, setting and basis. Simple connectedness is a deduction
   relying on two theorems not re-read (Armstrong; Kollár/Takayama).
6. Fourteen labels realise only ten Hodge pairs; deformation equivalence between different groups is
   open; nothing is claimed about 35 distinct families.

## Dependencies and reproduction

The audit itself needs only **Python 3** (tested with 3.11; standard library only):

```sh
python3 scripts/run_all.py
```

(about one minute; writes `output/*.json`, `output/run_all.log`, `table/space_groups_35.*` and ends
with `ALL CHECKS PASSED`). Regenerating the cached inputs additionally needs: `spglib` (Python package)
for `scripts/extract_spglib.py`; Sage 10.7's GAP with the packages Cryst and CrystCat for
`sage -gap -q < scripts/extract_crystcat.g > data/crystcat_generators.json`; `pypdf` and the cached
JBD PDF for `scripts/extract_jbd_list.py`; the cached arXiv e-print sources for
`scripts/extract_literature.py`. `python3 scripts/make_sources_manifest.py --verify` checks the local
cache against `sources/MANIFEST.json`.

Nothing in this directory is used by the sphere problem or by the `CP²` computations of this repository.
