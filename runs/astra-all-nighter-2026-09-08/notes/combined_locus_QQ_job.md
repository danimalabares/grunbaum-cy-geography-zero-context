# Prepared job: independent replay and exact-Q combined locus

Target: audit the actual F101 input used by J019 and determine whether the
same 123-variable necessary equations admit an exact characteristic-zero
exclusion. This is the combined second-order/generator-matrix ansatz,
not a new direction or a higher-degree search.

Command, to be run only by root under the exclusive guard:

```
python3 -B scripts/equation_reduction_combined_QQ_audit.py \
  --max-seconds 120 --output data/combined_QQ_audit
```

Fields: Q and F101. Variables: 21 second-order tangent parameters and two
51-dimensional equivariant generator matrices. Equations: the complete
1160 third-order incidence conditions. `G2` has constant coefficients;
its elimination leaves at most 72 polynomial variables. All later
substitutions divide only by nonzero rational constants.

Limits: 120 internal seconds, recommended 180-second wrapper, inherited
2800-MiB process-group cap, 100000 total polynomial terms, 2000 terms per
polynomial, degree at most 4. No arithmetic or CAS was run by this agent.
The script never launches CAS. It was syntax checked before handoff.

Expected evidence: exact-Q original equations; a direct independent
check of their F101 reduction; independent verification of all 49 saved
G2 row relations, all 979 residual relations, all 20 polynomial peels,
and the entire J019 Singular input; then an exact-Q reduction certificate
and either a visible unit equation or a small exact-Q Singular input.

Failure/cap handling: once the exact-Q original system is constructed it
is saved before reduction. A capped exact-Q reduction preserves its
current rational echelon, constraints, polynomial equations, and inverse
substitution maps in `QQ_checkpoint.json`. A cap gives no exclusion.
The script has no automatic restart or reset control.

Audit finding already explained by source inspection: constants equal to
one in 583 of the 658 final modular polynomials are expected. The original
normalization divides by the first nonzero coefficient in ascending total
degree, so a nonzero constant becomes one while all remaining monomials
are retained. None of the 658 inputs is the unit polynomial by itself.
The new independent replay checks this explicitly.

Certificate boundary: J019's finite-field unit conclusion does not exclude
arbitrary Q solutions with 101-denominators. A valid exact-Q unit identity
would exclude the whole stated quadratic raw-generator ansatz over every
characteristic-zero extension, since each reduction is a polynomial
isomorphism or a constant linear elimination with its inverse retained.
It would not rule out other first tangents, higher parameter degree, or
the inherited smoothing.

The prior Singular witness-export error remains visible: `ideal*matrix`
does not mean the desired coordinate sum. The generated exact-Q script
uses `matrix T=lift(I,ideal(1))`, loops over `nrows(T)`, and explicitly
sums `I[j]*T[j,1]`. It prints every nonzero witness entry only after checking
that this sum is one. Independent reconstruction of the exported identity
is still required before promoting a printed success to a final certificate.
