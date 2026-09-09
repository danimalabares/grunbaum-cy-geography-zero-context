# Updated queue after the computational results

**PROVED outcome, within the stated trust boundary:** an actual smooth
number-field fibre is specified; rho1, Hodge(1,31), Euler−60 and Hilbert
dimension94 are settled. The practical open problem is a compact coefficient
field or a simpler geometric model. This changes the purpose of tonight.

**No mandatory heavy computation is currently justified.** The old
order24/32 controller, full I² resolution and normal-space job are not
an unfinished queue. The first has exhausted its prescribed ansatz; the
other two are unnecessary for the now-proved geography. The highest useful
priority is independent verification and Friday-ready mathematical synthesis.

## 1. Recheck the tiny integer product certificate

Question: do the twelve exact first-order product differences give the
displayed integer matrix with determinant−3³8⁹?

In a fresh continuation run prepared as in `OVERNIGHT_PROMPT.md`:

    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag independent-integer-product-certificate -- python3 -B scripts/verify_product_minor.py

Inputs: repository `equations/deformation_data.json`, and the copied
`logs/20260908T122310-picard-product-q1.artifacts/product_first_order_rank.json`.
Measured independent verification was0.657s; expect seconds and under100MiB,
not a new large rank computation. The timestamped JSON/log is the checkpoint.
Success verifies the arithmetic input; the derived conormal argument is
still read and checked mathematically. Failure stops downstream claims
until the discrepancy is explained. Job2 is logically independent.

## 2. Recheck all displayed fibre coefficients and the Hensel Jacobian

Question: do the sixteen displayed cubics match every indexed exact
coefficient, and is the selected Jacobian determinant19 modulo101?

    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag independent-algebraic-coefficient-export -- python3 -B scripts/verify_ramified_export.py

Inputs: `RAMIFIED_FIBRE_EQUATIONS.md`, `data/ramified_fibre_coefficients.json`,
and `data/fixed_chart.json`. Measured1.205s; sampled peak was missed by
the one-second monitor, so do not quote388KB as a real peak. Expect under
100MiB. Save the timestamped independent JSON. Success checks the finite
presentation; it does not replace the written Hensel, full-syzygy flatness
and source-smoothness transport arguments. Failure stops use of that export.

The sequential controller for jobs1 and2 is

    python3 -B scripts/replay_certificates.py --run

## 3. Gated coefficient-field simplification — not a ready heavy job

**OPEN.** A small primitive element or multiplication table for
L=Q(pi,theta1,...,theta270) remains useful. The exact point and pi56
arithmetic are available. Bounded Q(pi) reconstruction failed, and the
specified low-degree coefficient-lattice searches have their exact scopes
in `BOUNDED_FIELD_SEARCH.md` and `EXTRACTION_NEXT.md`.

There is deliberately **no fabricated Gröbner command** here. A new heavy
job requires an actual further reduction of the coefficient equations,
a short algebraic relation with a viable route to representing all
coefficients, or another concrete structural ansatz. State the reduced
unknown/equation count and exact success test before launching it.

Use at most3600s per downstream attempt and2800MiB process-group RSS,
one thread and one substantial process. Checkpoint every eliminated block
or candidate. No timeout extension without measured progress. If no such
reduction emerges, stop computation and polish the established results;
do not grow the jet, repeat LLL, or resolve I² merely to occupy the night.

Exact success means every coefficient is represented over a genuine exact
field, all full Schur/FR identities vanish after clearing denominators,
and the original Hensel selector is verified. That identifies the same
actual fibre and transfers its known geometry. A modular fit alone is not
success. Failure only rejects the explicitly tested ansatz.

## Timing and concurrency

The current copied runner intentionally expires at16:35 on8 September.
Adapt a fresh evening copy to the new overnight window; never remove its
RSS, process ownership, locking or thread checks. Never run a second heavy
job, including a skeletal-polytope computation, simultaneously. The two
mandatory verification checks should take seconds, not an entire night.
