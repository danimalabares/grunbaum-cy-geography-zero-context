# Reproduce the computational results

**PROVED scope.** This packet concerns only the zero-context lineage at
commit `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`. The older DGLA proof
is not identified with this arc or component. The six frozen repository
heads and daytime hashes are recorded in `inputs/SOURCE_MANIFEST.json`
and `EXECUTION_RECORD.md`. Other repositories were read-only.

Work from

    /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-computation-2026-09-08

No package installation is required: the calculations used standard
Python3.13.7. No Macaulay2, Singular, Sage, GAP or Gröbner process was
needed in this computational session.

For the tested sequential verification entry point, follow the fresh-run
copy instructions in `OVERNIGHT_PROMPT.md`, then run

    python3 -B scripts/replay_certificates.py --run

It passed both checks at14:29 on8September. Default mode, without `--run`,
only prints the commands. It never launches field recognition or a CAS.

## First read the mathematics

1. `COMPUTATION_RESULTS.md`: outcomes, exact scope and failed attempts.
2. `GEOGRAPHY_THEOREM.md`, `DEGREE8_PICARD_FORMULA.md`, and
   `PRODUCT_RANK_CERTIFICATE.md`: the Picard/Hodge proof and small integer
   certificate. No ideal-square resolution is a hidden prerequisite.
3. `RAMIFIED_FIBRE_EQUATIONS.md`, `RAMIFIED_POINT_REVIEW.md`, and
   `RAMIFIED_FLATNESS_IDENTITY.md`: the actual coefficient numbers,
   smoothness transfer, and exact denominator-cleared syzygy identity.

The twenty-one free coefficients are the ORIGINAL normalized six-jet
polynomials at pi, not the linear-path or sparse3 experiments.

## Read-only inventory and small independent checks

After finalization, verify the packet without modifying its evidence:

    shasum -a 256 -c ARTIFACT_SHA256SUMS

The corresponding manifest in the sibling daytime run is unchanged.
Inventory measured wrapper runtimes with

    python3 -B scripts/summarize_runs.py

The following are small independent checks, not full proof re-audits:

    python3 -B scripts/verify_product_minor.py
    python3 -B scripts/verify_ramified_export.py

The first independently parses the supplied first-order polynomials and
checks all144 entries and the determinant of the twelve-square integer
minor. The second independently parses all sixteen displayed cubics back
into1680 monomial/coefficient pairs and recomputes the selected Jacobian
determinant by column elimination. Their existing certificate files are
compared, never silently overwritten. A new verifier output after the
packet is frozen should be directed to a fresh run by `GS_RUN_OUTPUT`;
do not update the old manifest to hide differences.

## Resource guard

Every substantial arithmetic job used `scripts/run_guarded.py` with
one thread, one shared run lock, and a monitored process-group RSS ceiling
of2800MiB. It refuses a pre-existing CAS process and fails closed if process
inspection is unavailable. Only its own process group may be terminated.
The four BLAS/OpenMP thread environment variables are forced to1.

The copied runner is deliberately tied to **8 September's authorized
daytime window**: no long launches after16:00, owned jobs stop by16:35,
attempts at most3600s. The primary controller uses1800s per stage.
It is supposed to refuse an evening replay. For tonight, use the fresh-run
instructions in `OVERNIGHT_PROMPT.md`; do not disable monitoring or edit
the frozen daytime runner in place.

## Original controller and checkpoints

The requested command was actually executed:

    python3 scripts/night_primary.py --run

It produced the original F101 order24 and32 checkpoints under
`logs/20260908T121238-night-curve-24.artifacts/` and
`logs/20260908T121301-night-curve-32.artifacts/`.
All6960 equations passed; every tested bounded rational closure failed.
Do not rerun or extend this exhausted rational-function search unchanged.
Its result is a finite jet, not a model over F101(q).

## Actual closed-fibre coefficient files

- `data/ramified_fibre_coefficients.json`: exact shared rational matrix
  factors,270 selected bordered determinants,pi7−101, the unique local
  selector, and all sixteen cubic coefficient maps.
- `data/ramified_hensel_pi14.json`: independently checked true
  mixed-characteristic values in `(Z/10201)[pi]/(pi7−101)`.
- `data/ramified_hensel_pi56.json`: the corresponding true approximation
  over `(Z/101^8)[pi]/(pi7−101)`, with all1650 full identities checked.
  This is point-field arithmetic, not a higher F101(q) Padé search.
- `data/ramified_degree7_height_screen.json`: exact failure of bounded
  rational reconstruction in the seven-dimensional Q(pi) power basis.
  It does not assert L is different from Q(pi).
- `scripts/export_ramified_fibre.py`: exact export and central/Jacobian
  checks. It refuses to overwrite its existing output.
- `scripts/ramified_hensel_pi14.py`: recomputes the genuine Z/101²
  formal coefficients through q13, folds q=pi, and checks all1650 full
  block equations in the ramified ring. It also refuses existing outputs.
- `scripts/ramified_hensel_pi56.py`: the preserved-source, one-time
  higher-precision point-field attempt. Its planned height bound was10^7.
- `scripts/verify_degree7_point.py`: an exact prospective field verifier,
  not run because no complete bounded-height Q(pi) candidate was found.

To rerun a write-once exporter or coefficient job, copy the required
scripts and input data into a fresh sibling run **inside this repository**,
keeping the exact relative repository layout. Do not delete or replace a
certificate just to make its original command run again. The finite
coefficient system, not an approximation, defines the exact point; the
approximations check the arithmetic implementation.

## Bounded coefficient-field exclusions

`BOUNDED_FIELD_SEARCH.md` and `EXTRACTION_NEXT.md` specify every bound,
lattice, checkpoint, and exact verification. At the existing pi56
precision, the completed LLL and exhaustive sphere enumerations prove
that neither theta1 nor theta2 has a nonzero relation of relative
degree<=3 and integral pi-basis coefficient height<=1000. This excludes
only that finite search box, not every small-degree field presentation.
The final enumeration summaries are

    data/theta1_cubic_height1000_enumeration/summary.json
    data/theta2_cubic_height1000_enumeration/summary.json

Both enumerate the entire containing sphere in34 assignments and find
only zero. The exact scripts, fresh Gram--Schmidt data and resumable
stacks are retained. Do not repeat these exhausted searches unchanged.

**COMPUTER-CERTIFIED failures remain evidence.** Logs include the initial
tuple/list chart assertion, a mistyped checkpoint path, and the initial
sparse-zero dictionary assertion in the mixed-characteristic code. These
were implementation failures before the asserted mathematical tests,
repaired without altering the frozen inputs. The failed mixed-characteristic
source is retained under `data/failed_attempt_sources/`.

## Exact trust boundary

The original all-orders equivariant obstruction theorem and audited
modular smoothness witnesses remain accepted inputs. They were not
recomputed with a second CAS in this session. The new Picard rank input
is an integer determinant, independently rechecked; the ramification
passage is an exact quotient-ring and valuation argument. Model agreement
is not an additional certificate, and qualified-human verification is
not claimed.
