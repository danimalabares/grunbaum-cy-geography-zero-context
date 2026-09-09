# Actual coefficient arithmetic modulo pi^14

**COMPUTER-CERTIFIED.** The algebraic coefficient point with pi^7=101 has
been evaluated modulo pi^14. Its 291 normalized generator coefficients
and all 490 equivariant syzygy-graph entries are in
`data/ramified_hensel_pi14.json` (about 40 KB). Every coefficient is a
seven-entry vector in the basis 1,pi,...,pi^6 over Z/10201Z.

For example, the first three dependent algebraic numbers satisfy

```text
theta_1 = 4444 + 6363*pi + 2525*pi^2 + 8888*pi^3
          + 6481*pi^4 + 9357*pi^5 + 6618*pi^6  (mod pi^14),
theta_2 = 202 + 9393*pi + 6464*pi^2 + 1818*pi^3
          + 6317*pi^4 + 3019*pi^5 + 8317*pi^6  (mod pi^14),
theta_3 = 909 + 2929*pi + 1111*pi^2 + 1818*pi^3
          + 9101*pi^4 + 5285*pi^5 + 3549*pi^6  (mod pi^14).
```

All constant entries are divisible by 101, as required by
theta_i in pi O. These are approximations to the uniquely specified
algebraic numbers, not replacements for the exact coefficient equations.

## Exact computation and why its characteristic is correct

**PROVED algorithm.** Recompute the original six-jet free-coordinate curve
through q^13 over Z/(101^2), using the same constant 270-square Jacobian.
Select pivots nonzero modulo 101 and invert them modulo 10201; selecting
merely nonzero pivots modulo 10201 would be incorrect in this nonfield.
Every coefficientwise step checks all 6960 original Schur equations.
The first six orders agree with the exact rational normalized source jet
modulo 10201, not just modulo 101.

There is a ring homomorphism

    (Z/10201Z)[q]/(q^14) -> (Z/10201Z)[pi]/(pi^7-101),
    q -> pi.

It is well-defined because pi^14=101^2=0 in the target. Substitution is
explicit: a coefficient at q^(i+7) contributes 101 times that coefficient
to pi^i. Thus a 14-term coefficient sequence c_0,...,c_13 becomes

    (c_i + 101*c_(i+7) mod10201)_(i=0,...,6).

This is genuinely mixed-characteristic arithmetic. An F101 jet cannot
simply be evaluated with pi^7=101 beyond pi^7 precision, because it has
discarded the carries now needed modulo 101^2.

**COMPUTER-CERTIFIED independent identity check within the computation.**
The script reconstructs the equivariant U graphs in blocks 21,13,32 by
the recursion A_0=I. After folding q to pi, it reevaluates all matrix
factors from the 291 coefficient vectors and multiplies directly in the
seven-dimensional ramified ring. All 490 equations AU-B and all 1160
equations D-CU vanish, for a total of 1650 full block equations. It also
checks the 21 exported free-coordinate polynomials directly in that ring.
This is stronger than merely rereading the zero formal-q residuals.

**PROVED interpretation.** The selected Jacobian is a unit at the marked
point; consequently these congruences are the reduction of the unique
exact Hensel root of the finite coefficient equations. The finite
approximation alone would not prove an all-orders identity or smoothness.
Those claims instead follow from the exact finite presentation and the
ramified transport argument reviewed in `RAMIFIED_POINT_REVIEW.md`.

## Resource use, provenance, and preserved failure

The successful guarded run was

    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag ramified-hensel-pi14-cleaned-operator -- python3 -B scripts/ramified_hensel_pi14.py

It completed in 12.187 seconds with 37.3 MiB sampled peak RSS. No CAS or
parallel job ran. Logs and all order-by-order Z/10201 checkpoints are under

    logs/20260908T130846-ramified-hensel-pi14-cleaned-operator.*

The final artifact hashes the actual script, original chart, exact block
data, finite coefficient presentation, source deformation data, and reused
identity/normalization helpers.

**FAILED implementation assertion, corrected transparently.** An earlier
invocation stopped before its first lift because the reused identity
operator retained zero dictionary entries whereas the saved chart omitted
them. Removing those zero entries fixed this representation mismatch. The
failed log is `logs/20260908T130717-ramified-hensel-pi14.stderr`, and its
exact source is retained as
`data/failed_attempt_sources/ramified_hensel_pi14_before_zero_cleanup.py`.
No mathematical residual or failed lifting identity was concealed.
