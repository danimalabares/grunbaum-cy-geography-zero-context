# Targeted review of the optimized coefficient and rational-closure scripts

**PROVED (scope).** This checks the matrix recurrence, denominator-clearing
identity, modular solvers, input boundary, and acceptance logic in
`scripts/fixed_curve_lift.py` and `scripts/check_rational_closure.py`.
It does not certify the independent theorem identifying the finite fixed
chart with the equivariant Hilbert germ, nor the existence of a rational
parametrization of its chosen algebraic curve.

## Matrix identities and signs

**PROVED.** Let the quartic multiplication matrix be divided into 98 pivot
columns `P(z)` and 30 extra columns `E(z)`. Write

\[
P(z)=P_0+M(z),\qquad E(z)=P_0U_0+E_1(z),\qquad U=U_0+W,
\]

where `P0` is the inclusion of the 98 pivot-monomial rows and `U0` is the
constant extra-column incidence matrix. Define the linear map
`L(z)=E1(z)-M(z)U0`. Then

\[
E(z)-P(z)U=L(z)-P_0W-M(z)W.
\]

Thus at positive order `n`, the nonlinear contribution is
`sum_{i=1}^{n-1} M(z_i) U_{n-i}`. The bottom 232-by-30 rows give
`L_bottom(z_n)=cross_bottom`; the top rows give
`U_n=L_top(z_n)-cross_top`. These are exactly the signs used in
`fixed_curve_lift.py`. Solving the selected 270 equations determines the
270 dependent coefficients; checking all 6960 bottom equations is still
required and is performed at every computed order.

**PROVED.** If `z=Z/D` and `U=U_num/D`, with `D(0)=1`, put
`W_num=U_num-DU0`. Multiplying the relation by `D^2` gives precisely

\[
D\bigl(L(Z)-P_0W_{num}\bigr)-M(Z)W_{num}=0.
\]

The checker evaluates this polynomial identity. If numerator degree is at
most `m` and denominator degree at most `d<=m`, degree `2m` is an exhaustive
bound. Passing all coefficients therefore certifies an exact identity,
unlike merely fitting the stored jet.

## Bugs found and repaired

**FAILED, then repaired.** The first Padé loop began at denominator degree
one and rejected every consistent rank-deficient system. Exact constants and
polynomials could therefore be falsely rejected. The loop now includes
degree zero and selects zero for free unknowns in a consistent denominator
system. Exact identity verification remains compulsory.

**FAILED, then repaired.** The first version stopped after the first fitting
denominator even when the complete polynomial identity failed. It now saves
the first nonzero residual coefficient and continues to every larger
allowed bound.

**FAILED, then repaired.** The first version accepted a checkpoint without
checking its special generator/syzygy data or provenance. It now verifies
the field prime, array shapes and coefficient residues, origin, canonical
complete special relation basis, free-coordinate conventions, and source
hashes. By default it also verifies agreement with the selected normalized
six-jet. `--allow-other-sixjet` is an explicit control/alternative-curve mode;
the output records whether that six-jet actually matches.

## Exact cheap checks performed

**COMPUTER-CERTIFIED.** `scripts/review_fixed_curve_solvers.py` checks:

- modular LU solves with required row swaps against known answers;
- uniquely soluble and inconsistent overdetermined systems;
- consistent rank-deficient systems, constants, and polynomial sequences;
- the denominators `1-3q` and `1-q-q^2` on exact rational sequences;
- a nontrivial scalar identity `z-W-zW=0` for `z=q`, `W=q/(1+q)`,
  embedded in the checker's matrix shapes;
- detection of an intentionally reversed denominator sign at order three;
- full acceptance of the constant special-fibre family;
- full rejection of a deliberately nonflat linear correction, followed by
  continued testing of denominator bounds 0, 1, and 2;
- rejection of a changed origin and a tampered input hash.

Raw control output and exact failure witnesses are saved in versioned JSON
under `certificates/fixed_curve_solver_review-*.json`, and immutable fixtures
under `fixtures/review_constant_family/`. The constant-family model there is
singular and must never be treated as a smoothing discovery or Hodge input.
All checks use standard Python, one thread, and no CAS.

## What success and failure mean

**PROVED (acceptance boundary).** Exact `FR=0`, the correct special generators,
and a lift of the complete special syzygies imply flatness over the local
parameter ring at `q=0`, hence over some open algebraic neighborhood after
shrinking. They do not prove flatness at every value where `D` is nonzero.
The model's status now states this local scope explicitly.

**PROVED (field boundary).** Arithmetic here is in the specified finite
field. A successful rational identity supplies no rational characteristic-zero
coefficients by itself. The output does not claim characteristic-zero
equations or smoothness. A lift/spread and an exact smoothness argument are
separate obligations before using it for the intended geography.

**OPEN (rationality).** A failed bounded run says only that its selected
fits did not close. A consistent underdetermined denominator system may have
other choices besides the chosen free-zero solution. Larger numerator or
denominator bounds may work, and an algebraic curve need not admit a rational
parametrization by this parameter at all. Neither finite lifting nor Padé
failure disproves the independently established algebraic implicit curve.

**CONDITIONAL (continuation identity).** An accepted model matching the six-jet
is a curve agreeing with that normalized six-jet; identifying it with a
particular all-orders formal arc requires an independent uniqueness/gauge
statement. The lifted finite-order files alone remain jets.

## Claim ledger

| ID | Claim | State | Evidence |
|---|---|---|---|
| R1 | The coefficient recurrence has the correct nonlinear signs | **PROVED** | Expansion of `E-PU` above; LU controls |
| R2 | The denominator-cleared identity is exact when all coefficients pass | **PROVED** | Degree bound `2m`; nontrivial rational scalar control |
| R3 | Constants/polynomials and consistent deficient fits are handled | **COMPUTER-CERTIFIED** | Regression fixtures and modular solver checks |
| R4 | A failed fitting candidate does not end larger-bound testing | **COMPUTER-CERTIFIED** | Deliberately nonflat control, three saved failures |
| R5 | A finite-field accepted model already gives the requested characteristic-zero smooth fibre | **FAILED** as an inference | Additional field and smoothness obligations remain |
| R6 | Bounded failure proves nonexistence of a rational or algebraic continuation | **FAILED** as an inference | Unsearched bounds and denominator choices remain |

Dependencies are chart/special-syzygy identification → R1 → R2 → local
flatness. No independent qualification of the complete proof is asserted;
qualified-human verification is not claimed.

## Final export review

**FAILED, then repaired.** Both exporters initially emitted compact cubic
words such as `abf` as if they were executable monomials. Macaulay2 treats
that as a single identifier, so the rational-fibre input would fail.
The exporters now use `a*b*f` and the corresponding explicit products for
all sixteen initial cubics. The rational renderer also omits zero tails.
The public CLI still rejects a model that does not match the selected
normalized six-jet.

**COMPUTER-CERTIFIED.** The standard-Python rendering regression
`scripts/review_export_rendering.py` checks all sixteen cubic products,
the generic finite-field ring, finite parameter rendering, rejection of a
zero denominator, and preservation of the synthetic-control rejection gate.
Its raw result is
`certificates/export_rendering_review-cb0d13ff69bc.json`.

The generated `equations/fixed_curve_QQ.json` was mechanically repaired in
exactly sixteen initial monomial tokens. All other bytes, free paths, and
the `.sing` file were left unchanged. The old JSON SHA-256 was
`797defa019016c5bd7c6b4ba25985c392ecb7c8f8850aa62e4eec3dcc57f61e0`;
the repaired SHA-256 is
`7db0df1eb6f80ce8e877ea3869df2e4d3cfc629126a80f75ef748dcbc83aa8cf`.
