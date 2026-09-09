# Internal discovery frozen before external reference inspection

Date: 2026-09-08. Scope: Task C only. No web source has yet been used in this
derivation. The source proof is commit
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`; audit HEAD is
`9310cd9e3316c69f129d5588d65f0b91f37365b7`; geography HEAD before this run is
`4f75a9ae930a5cb645e06b4b8da79fa7b78a394a`.

- **PROVED** from the displayed matrices: a rank-one 2 by 6 cone has
  dimension 2+6-1=7. Consequently the largest intrinsic quadratic component
  has dimension 17+3*7=38, and adjoining the 56 coordinate directions gives
  the upper bound 94 for local Hilbert dimension, provided these are genuine
  initial Kuranishi equations (the audited computation certifies this input).
- **PROVED** in the source's explicitly indexed intrinsic basis: the entire
  ten-dimensional invariant tangent space lies in P1^3. Each of three
  rank-one matrices has identical rows on this subspace. The proof tangent
  has weights (1,...,10); all its block entries are nonzero, so it belongs
  only to the top quadratic component. A five-equation ratio calculation
  identifies each block on its coordinate torus with the rank-one locus.
- **PROVED** distinction: the sparse tangent has orbit weights
  (1,1,1,1,0,0,1,1,0,1). It differs from the proof tangent. Its nonaveraged
  stored two-jet is not invariant; its later averaged jet and the proof's
  generic invariant six-jet must also be distinguished.
- **OPEN**: a component of the initial quadratic obstruction locus is not
  thereby an actual component of the completed local Hilbert scheme.
- **CONDITIONAL**: a 94-dimensional Hilbert component through X_M with a
  smooth Calabi-Yau member has h21=31, by the smooth CY Hilbert formula
  63+h21. A single smoothing curve supplies no lower bound 94.
- External claims queued for a separate primary-source phase: the degree-20
  determinantal Hodge pair (2,34), and Hartshorne's connectedness theorem
  for the Hilbert scheme with fixed Hilbert polynomial. No literature claim
  has yet been verified by this Task C run.

The atomic claim/dependency ledger will be recorded in
`HILBERT_EXPLANATION.md`; this targeted verification does not re-audit the
smoothing proof. Human verification is not claimed.
