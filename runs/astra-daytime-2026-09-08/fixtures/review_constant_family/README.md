# Synthetic controls, not smoothing outputs

These immutable fixtures test the rational-closure checker. The positive
fixture is the constant Stanley–Reisner family: it is flat and singular.
The negative fixture deliberately violates a first-order syzygy. Neither
fixture agrees with the selected zero-context six-jet.

Every model under this directory is a software regression artifact. Never
use it as an explicit smooth fibre, overnight mathematical discovery, or
Hodge/Picard input. The current checker records
`matches_selected_normalized_sixjet=false` for the constant control.

Reproduce using `scripts/review_fixed_curve_solvers.py` from this run.
Early regression artifacts are preserved alongside later checks, with
checker hashes distinguishing their versions.
