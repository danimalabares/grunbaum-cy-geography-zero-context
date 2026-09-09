# Checkpoint / resumption notes

Status at the end of the session (2026-09-09, ~16:25Z; the 15-minute budget was exceeded by
about ten minutes to finish the order-54 optional item):

**Complete and verified** (nothing to resume): tasks 1, 2, 4; the order-54 invariants; the
independent Python re-verification of both certificates. See `RESULTS.md`.

**Task 3** needs no computation: the `G`-representation was built directly on the full
degree-0 `T²`, so no quadric-span argument is used.

**Optional, UNFINISHED (process stopped after 6 minutes; log ends with the kill note):**
the rank of the coefficient matrix of the 126 order-two Kuranishi quadrics in the 93 tangent
parameters (`scripts/quadric_rank_check.m2`; `versalDeformation(F0,T1,T2,HighestOrder=>2)`).
It only tells whether the dual primary obstruction map `κ₂*` is injective here, i.e. whether a
quadric-based recovery of the representation *would have* sufficed. Rerun with

```sh
/Applications/Macaulay2-1.20/bin/M2 --script scripts/quadric_rank_check.m2 | tee logs/quadric_rank_check.log
```

(single process, >1.2 GB RSS observed after 5 minutes; allow 10–30 minutes).

**Coordinate orbit — complete** (`scripts/coordinate_orbit.m2`, logs `logs/coordinate_orbit_*.log`,
both end in `COORDINATE_ORBIT_DONE`; results in `RESULTS.md` §6). To rerun:

```sh
/Applications/Macaulay2-1.20/bin/M2 --script scripts/coordinate_orbit.m2 data/orbitals_Aut54.txt
/Applications/Macaulay2-1.20/bin/M2 --script scripts/coordinate_orbit.m2 data/orbitals_G_S3.txt
```

**Natural next computation (not started):** the `Aut(Δ)`-equivariant Kuranishi equations restricted
to the 5 invariant tangent parameters (or the `G`-equivariant ones on 23 parameters mapping to the
14 invariant obstructions), to see whether any invariant direction outside the coordinate orbit is
unobstructed to second order.
