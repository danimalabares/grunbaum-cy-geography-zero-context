# Grünbaum CY geography — zero-context source only

Resumable research workspace for extracting the actual deformation in the
zero-context proof packet and studying the geography of its claimed smooth
degree-20 Calabi–Yau threefold in `P^7`.

This is a reproducible research workspace containing verified exact
computations, deductions with explicitly stated hypotheses, literature
comparisons, failed computations, and open questions. It is not a finished
classification of degree-20 Calabi–Yau threefolds and is not an independently
refereed proof of the source packet's smoothing theorem.

The immutable source is `grunbaum-zero-context-proof` at commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`. By default the scripts expect it
as the sibling directory `../grunbaum-zero-context-proof`; set
`GS_ZERO_CONTEXT_SOURCE=/path/to/grunbaum-zero-context-proof` to use another
clean checkout at the same commit. This workspace neither uses nor imports
results from `fable-dgla-only` or `sr-project/main/rl`.

Run the complete deterministic audit suite with:

```sh
python3 scripts/run_checks.py
```

Then verify the frozen workspace outputs with
`python3 scripts/make_manifest.py --verify`. See `PROVENANCE.md`, `STATUS.md`,
and the reports under `reports/`.

The publication-readiness audit and pre-publication backup record are in
`PUBLICATION.md`.

No license has been added. In the absence of a license, normal copyright
restrictions apply to reuse beyond what applicable law permits.
