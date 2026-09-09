# Reproduce the successful finite checks

From the repository root, with the installed Python 3.11 and SymPy 1.14:

```sh
python3 -B runs/astra-all-nighter-2026-09-08/scripts/reproduce_successes_v2.py --output runs/astra-all-nighter-2026-09-08/data/reproduction_02
```

Choose a fresh output directory. This one entry point invokes the preserved resource guard and runs twelve checks sequentially: export rendering/Jacobian, independent rational and mixed-characteristic audit, triangle smoothness calculation, all five line branches, facet-transverse exhaustion, local topology point, exact rational support closure, graph-ray exclusion direct rational degree-three/four/five unit identities, the combined rational contradiction, seven sparse orbit extensions and the singular eight-parameter slice. The final twelve-check invocation passed in 31.795 seconds with sampled peak process-group RSS 111,968 KiB. See `data/reproduction_final/SUCCESS.json`, its `steps.jsonl`, and immutable guarded logs. The earlier nine-check integration run is also preserved in `data/reproduction_01`.

The guard retains the authorized historical calendar: no launches after 2026-09-09 06:00 and no work after 06:30, America/Sao_Paulo. Later reproduction requires a separately authorized guard for the actual session; this entry point deliberately does not silently move those dates. Its process inspection must be permitted, or it fails closed. No original packet is written.

This replay checks finite identities and software paths. The exact closure, flatness, component, line Hensel and topology proofs are mathematical arguments in `FIBRE_AUDIT.md`, `NEW_GEOMETRY.md` and their linked notes. The accepted original invariant-obstruction and Singular smoothness boundary is not re-proved by these finite checks.

The search inputs, resource limits and outcomes are indexed in `JOBS.md` and append-only `RUN_LOG.jsonl`. Every guarded job has immutable stdout/stderr and metadata. Degree-five equations and their successful witness export are in `data/degree5_cas`; the failed original export is preserved too. The direct verifier avoids Singular entirely by summing the exact rational rows. Checkpoint locations and budget constraints are in `RESTART_HANDOFF.md`.

There is no new manageable characteristic-zero CAS model. See `MODEL.md` for the exact partial reduction and its scope.
