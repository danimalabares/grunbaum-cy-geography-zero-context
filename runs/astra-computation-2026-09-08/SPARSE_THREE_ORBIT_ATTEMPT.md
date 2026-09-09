# One controlled three-orbit explicitness attempt

8 September 2026. **FAILED bounded rational ansatz; OPEN algebraic
continuation and smoothness.** The sole attempted alternate direction has
S3-orbit weights

```
(0,0,1,0,0,0,0,1,0,1).
```

It was selected mathematically after the two-orbit grading obstruction,
not by a parameter sweep. No other sparse weights were lifted.

## Exact precheck

**COMPUTER-CERTIFIED over Q:** `scripts/check_sparse_direction_weights.py`
derives the direction by summing the source53-basis columns in orbits
3,8,10. It verifies equivariance in the actual291-coordinate chart and
all6960 linear tangent equations. The full nine-variable weight system
(a,...,h,q) has rank8, with kernel only ordinary projective scaling and
q weight zero. Thus there is no nontrivial diagonal grading fixing q.

The same twelve degree-eight product rows and columns have integer
determinant−1. The input, chart, original minor and script hashes, full
first-order polynomial coefficients, grading equations, kernel, chart
tangent and12-by-12 minor are retained in

```
data/sparse3_direction_exact.json
logs/20260908T125416-sparse3-weight-check.json
logs/20260908T125416-sparse3-weight-check.stdout
```

**PROVED scope:** this is a different first-order direction from the
selected zero-context smoothing. It lies in the same smooth S3-fixed
Hilbert germ, so any independently certified smooth characteristic-zero
fibre on the resulting branch would have Hodge pair(1,31). It does not
inherit the original six-jet smoothness certificate. The grading test
only removes diagonal-action obstructions; it does not rule out
reducibility or other causes of singularity.

## One linear-free-coordinate curve, through order32

**COMPUTER-CERTIFIED finite jets over F101:** the separate script
`scripts/fixed_curve_lift_sparse3.py` prescribes exactly

```
z_free(q)=q * sparse3_tangent_free.
```

At each order it solves the original constant270-by-270 linear system
and checks all6960 Schur coefficients, using the same canonical central
syzygy basis. All coefficients through order32 pass. Every order is
written to an immutable checkpoint with hashes of the actual variant,
its helpers, the source data, the direction certificate and chart.

The lift does not terminate polynomially at low order: the numbers of
nonzero invariant generator coefficients at orders1,6,12,24,32 are
6,20,53,69,68 respectively. First-order sparsity does not persist.

## Both bounded rational tests fail

**FAILED exact finite-field linear fitting problems:** the separate
`scripts/check_rational_closure_sparse3.py` tests both all generator plus
canonical-syzygy coefficients together and the generator coefficients
alone. At order32, every common-denominator bound `0<=d<=10` fails for
each numerator bound `d+1` and `d+6`. There are44 final fits in total,
all inconsistent. No fit reached the exact FR-verification stage, and
no rational family or rational-generator candidate was produced.

The order24 run used the smaller admissible fitting window. The single
extension to32 completed the larger numerator/denominator window; the
experiment then stopped. Failure means only failure of these rational
ansatz bounds for this finite-field curve. It is not nonexistence of an
algebraic curve, of higher-bound rational models, or of a smoothing.
No additional prime, weight choice, parameter sweep, or higher order
was tested.

## Commands and artifacts

All computation stages were sequential, single-threaded, under the
2800-MB memory guard. Timings include guard overhead:

| Stage | Time | Sampled peak RSS |
|---|---:|---:|
| Exact direction/weight/minor check | 1.384s | Too short for useful peak sampling |
| Lift through24 | 5.272s | 24,676KB |
| Closure screens at24 | 1.191s | Too short for useful peak sampling |
| Resume24 to32 | 3.560s | 25,608KB |
| Closure screens at32 | 1.187s | Too short for useful peak sampling |

Checkpoint and final summary:

```
logs/20260908T125640-sparse3-curve-24.artifacts/sparse3_curve_p101_order24.json
logs/20260908T125753-sparse3-curve-32.artifacts/sparse3_curve_p101_order32.json
logs/20260908T125707-sparse3-closure-24.artifacts/sparse3_closure_summary.json
logs/20260908T125814-sparse3-closure-32.artifacts/sparse3_closure_summary.json
```

Each stem also has a guard JSON, stdout and stderr alongside its
`.artifacts` directory. All individual fitting attempts are checkpointed.
The same-run direction certificate is immutable; reproducing it requires
a new output filename, or reading and comparing the existing certificate.

The exact successful lift command was

```
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_guarded.py \
  --seconds 1800 --memory-mb 2800 --tag sparse3-curve-24 \
  -- python3 scripts/fixed_curve_lift_sparse3.py --order 24 --prime 101
```

The resume command adds `--order 32 --resume` with the order24 checkpoint
path above. The final screening command was

```
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_guarded.py \
  --seconds 1800 --memory-mb 2800 --tag sparse3-closure-32 \
  -- python3 scripts/check_rational_closure_sparse3.py \
  logs/20260908T125753-sparse3-curve-32.artifacts/sparse3_curve_p101_order32.json \
  --max-denominator 10
```

No further jobs are queued for this direction. The ramified algebraic
point construction uses the original six-jet path, not this experiment.
