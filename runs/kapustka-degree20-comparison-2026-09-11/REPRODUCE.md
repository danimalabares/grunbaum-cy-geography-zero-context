# Reproduce

Run from **this directory**. Input commit of the repository:
`09953cefe987f304e1e8549a50df3b937747470c`. Nothing outside this directory is read or
written except the frozen `I_M` in `../../scripts/verify_geography.m2`, which is
transcribed into `scripts/verify_sphere.py`.

Software: Python 3 (no packages beyond the standard library) and
Macaulay2 1.20 (`/Applications/Macaulay2-1.20/bin/M2`; any 1.20 build works).
All Macaulay2 work is over `F₃₂₀₀₃` with `setRandomSeed 20260911`; every random
choice is also written out to `data/` so the algebra can be replayed without relying
on the random number generator (see "Determinism" below).

## Pure-Python checks (seconds, exact integer/rational arithmetic, no CAS)

```sh
python3 scripts/verify_sphere.py            # f-vector, links, H_*(M;Z)=H_*(S^3), h-vector, Hilbert polynomial
python3 scripts/verify_kapustka_table1.py   # reproduces rows 1-8 of Kapustka's Table 1 exactly
```

Expected last lines: `ALL CHECKS PASSED` and `ALL ROWS 1-8 REPRODUCED`.

## Macaulay2 chain (about 25 minutes in total on a 2021 laptop)

Each script writes the objects it produces into `data/`, and the next script loads them,
so the steps can be run one at a time.

```sh
M2 --script scripts/k01_surface.m2   >  logs/k01_surface.log   2>&1   #  ~2 min  ~~D8 in P6, Betti table, h^1(I_S(k))
M2 --script scripts/k11_ci.m2        >  logs/k11_ci.log        2>&1   #  ~3 min  X'_{2,2,3}, degree 12, 44 reduced nodes
M2 --script scripts/k14_unproj.m2    >  logs/k14_unproj.log    2>&1   #  ~2 min  ((I_X')+(G)) : I_S  -> generator degrees 2,2,3,3,4,5,5
M2 --script scripts/k15_models.m2    >  logs/k15_models.log    2>&1   #  ~2 min  Y in P^7  (degree 20, Hilbert polynomial P(n)-2)
M2 --script scripts/k16_ybar.m2      >  logs/k16_ybar.log      2>&1   #  ~2 min  Ybar in P(1^8,2^2)  (Hilbert function 1,8,36,104,232,440)
M2 --script scripts/k17_deform.m2    >  logs/k17_deform.log    2>&1   #  longest: graded normal module and the y-coefficient matrix
```

`k01` must be run before `k11`, `k11` before `k14`, `k14` before `k15`/`k16`, `k16`
before `k17`. Messages go to **stderr** (Macaulay2 buffers stdout when redirected), so
keep the `2>&1`.

## Determinism

`k01_surface.m2` chooses a random `7 × 9` projection matrix; it is written to
`data/Mproj.m2` and *not* used again — every later script loads `data/IS.m2` (the
ideal of the projected surface), `data/IX.m2` (the complete intersection),
`data/G.m2`, `data/Q.m2`, `data/IY.m2`, `data/IYbar.m2`. To replay on another machine
or another Macaulay2 build, keep the shipped `data/*.m2` and start at `k11_ci.m2`.
To rebuild from scratch, delete `data/` and run the chain from `k01`; the *numbers*
reported (Betti table, 44 nodes, generator degrees, Hilbert functions) are independent
of the choices, being properties of a general member of the construction. Two
independent sets of random choices were not run in this session — see
`OPEN_QUESTIONS.md`, item (v).

## What each log should say

| log | decisive lines |
|---|---|
| `k01_surface.log` | `total: 1 17 53 68 43 14 2`; deficiency `2` at `k = 1`, `0` elsewhere |
| `k11_ci.log` | `degree_Xprime 12`, `nodes_degree 44`, `nodes_degree_radical 44` |
| `k14_unproj.log` | `colon gen degrees: {2, 2, 3, 3, 4, 5, 5}` |
| `k15_models.log` | `Y: degree = 20`, `Hilbert function 0..4 = {1, 8, 34, 102, 230}`, `Hilbert polynomial = (10/3)*i^3+(14/3)*i-2` |
| `k16_ybar.log` | `Ybar: gen degrees = {2,2, 3×16, 4,4,4}`, `Hilbert function 0..5 = {1, 8, 36, 104, 232, 440}` |
| `k17_deform.log` | `dim of the span of the y-coefficient matrices in M_2 = …` |

## Canonical inputs, and scripts that were abandoned

The files in `data/` **are** the canonical inputs; the Macaulay2 chain from `k11_ci.m2`
onwards reads them and never re-randomises. `k01_surface.m2` and `k10_build.m2` are the
from-scratch builders: `k10_build.m2` produced the shipped `data/IS.m2`,
`data/Mproj.m2`, `data/coeff_q.m2`, and `k01_surface.m2` recomputes the same surface and
writes `data/IS_rebuilt.m2`, `data/Mproj_rebuilt.m2`. On the machine of this run they
came out **byte-identical** to the shipped `data/IS.m2`, `data/Mproj.m2` (checked with
`diff` after stripping whitespace, the two writers using different formatting); across
other Macaulay2 builds the random stream may differ, in which case the *numbers*
reported are unchanged but the ideals are not the same ones. Start from `k11_ci.m2` with the shipped `data/` for an exact replay.

Three scripts were written, started and abandoned during the run; they are kept because
they record what was tried and why it was replaced, and they are **not** part of the
chain:

| script | why abandoned | replaced by |
|---|---|---|
| `k02_ci.m2` | `radical` and `saturate` on the singular locus in `P⁶` did not return within 25 minutes | `k11_ci.m2` (works on `S`, where the degeneracy locus is already 0-dimensional) |
| `k12_hom.m2` | `Hom(module J, B¹)` over the quotient ring did not return within 20 minutes | `k14_unproj.m2` (liaison: the same module as `(1/G)·((I_{X'}+(G)) : I_S)`) |
| `k13_unproj.m2` | `saturate((I_{X'}+(G)) : I_S)` did not return within 25 minutes; the saturation is not needed | `k14_unproj.m2` (`quotient(..., DegreeLimit => 5)`) |

Their logs (`logs/k10_build.log`, `logs/k12_hom.log`, `logs/k13_unproj.log`) are the
partial output at the moment the process was stopped.
