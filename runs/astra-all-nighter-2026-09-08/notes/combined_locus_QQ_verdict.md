# Exact contradiction for every quadratic raw-generator path with the fixed tangent

J024 completed in 61.121 internal seconds and used no CAS. Its result is
`data/combined_matrix_QQ/summary.json`: `EXACT_Q_UNIT_FOUND`.

**COMPUTER-CERTIFIED exact-Q contradiction.** Fix the inherited first
normalized coefficient `t`. Let `z2` range over all 21 possible second
coefficients satisfying the order-two incidence equations, and let `G1,G2`
range independently over the full 51-dimensional equivariant generator
endomorphism space. There are 123 scalar parameters. The raw polynomial
generators under consideration are

```
Fraw(q) = F0*(Id+q*G1+q^2*G2) + q*T + q^2*(Z2+T*G1).
```

These include all equivariant raw cubic generator rows of parameter
degree at most two whose normalized first tangent is exactly the original
one. The normalized third coefficient would be `-z2*G1-t*G2`.

The complete necessary order-three incidence equations have no solution
over any characteristic-zero extension of Q. In particular this is
unrestricted by coefficient height, field degree, or 101-adic denominators.
It does not exclude different first tangents, higher parameter degree,
or compact models that are not given by this particular kind of path.

The proof has two algebraic steps. First, constant rational row operations
eliminate the rank-49 `G2` image. Every resulting rational equation is
checked directly as a constant linear combination of the original 1160
equations. The two remaining `G2` parameters are free at this order.
Second, 54 substitutions eliminate a variable from an equation
`a*x+f=0`, where `a` is a nonzero rational constant and `f` does not
involve `x`. Each substitution is valid over every characteristic-zero
field, and its inverse expression is saved. The resulting system
contains the literal unit polynomial `1`; hence an original solution
would give a solution of `1=0`, a contradiction.

This deduction uses exact rational arithmetic throughout. J019's modular
unit ideal is only a discovery aid. The previously problematic inference
from modular incompatibility to arbitrary Q coefficients is unnecessary.

The exact original equations are in `original_system_QQ.json`, the checked
rational row relations in `G2_elimination_QQ.json`, and all 54 inverse
substitutions and final equations in `reduced_locus_QQ.json` and
`QQ_checkpoint.json`, under `data/combined_matrix_QQ/`. The independent J025 replay passed all 54 substitutions and 979 rational
row combinations in 20.125 guarded seconds, using Cartesian monomial
expansion and importing none of the constructors. Its exact result is
`data/combined_QQ_independent_verification/contradiction_verified.json`.
No new Gröbner computation is needed for the conclusion.

J024 also independently checked all original modular equations, all 49
modular `G2` row certificates, all 979 residual certificates, all 20 earlier
modular peels, and the entire actual Singular input used by J019.
`independent_F101_replay.json` records the result. The 583 normalized
constant coefficients equal to one were confirmed to retain their other
monomials; none of the 658 modular inputs was initially the unit polynomial.

This remains a computer-assisted mathematical certificate, not qualified
human verification. The exact scripts and identities, rather than an AI
review label or an unexplained CAS success message, supply its evidence.
