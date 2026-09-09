# Independent targeted review of the fifteen-line construction

**Verdict: PROVED with the audited exact-fibre assumptions and the executed
finite certificates.** The selected ramified fibre has at least fifteen
distinct geometric lines, each an isolated reduced point of its full line
scheme, with normal bundle O(−1)⊕O(−1). The argument closes every omitted
containment equation exactly. It does not determine the complete line
scheme or give a practical arithmetic presentation of the line fields.

This is an adversarial review of `notes/degeneration_lines.md` and
`scripts/certify_degeneration_lines_v2.py`, not qualified-human verification.
The v2 script differs from the first version only by correcting the label
for four face-intersection points with six pairwise determinants. The
executed all-five certificate is
`data/line_certificates_all/line_certificates.json`, SHA256
`e9be734dd691529bbbd2fa56bc0052b0f87a379befb35becf29a71e5e145309e`.
Its script hash is
`7f4c2236b0a7dcb0ea61e06412153097757279dfe97664e39d9ffa92b2540e68`.
The original six-jet and coefficient-export hashes agree with the user
inputs. The guarded all-five job completed with exit 0; I inspected its
code, finite determinants and log without launching another CAS job.

## Atomic claims checked

| ID | Inference | Review state |
|---|---|---|
| L1 | Dividing all 64 line restrictions by π gives integral equations | PROVED from facet support and integral cubic coefficients |
| L2 | The five residue tuples solve these equations, with a unit selected 12×12 Jacobian | COMPUTER-CERTIFIED in F101 and F101² |
| L3 | The 52×52 syzygy minor forces the omitted 52 equations | PROVED using exact FR=0 and the executed unit minors |
| L4 | Hensel solutions define actual lines over finite extensions of L | PROVED; no equality of global and local field degrees claimed |
| L5 | Each line is an isolated reduced point and has N=O(−1)² | PROVED using π⁴ Jacobian scaling and audited smooth CY property |
| L6 | Symmetry gives fifteen distinct geometric lines | PROVED by distinct residue w values and distinct support facets |

Dependencies: exact integral selected fibre and source first jet → L1;
finite residue/Jacobian calculations → L2; exact linear syzygies and their
recorded reduction, together with L1,L2 → L3; L1–L3 → L4; L2,L4 and fibre
smoothness → L5; L4 and exact equivariance → L6. No claim here depends on
an obstruction-vanishing theorem for the line scheme.

## Exact closure and residue-field issues

Let the raw Grassmann coordinates be the four support coefficients U and
the eight outside coefficients D. Substitute D=πY. Every central generator
contains an outside variable, and all cubic coefficients beyond the
central monomials lie in πO. Thus

    E(U,Y)=F(line(U,πY))/π

is a 64-vector of genuine polynomials over L∩O. Its residue is exactly the
first-order incidence system used in the script. If generator normalization
changes the first-order row by a central-generator combination, that
combination restricts to zero on the facet, so this residue system is
unchanged. The code treats all twelve U,Y variables independently when
forming its Jacobian; it does not accidentally differentiate along the
already-solved rational formulas for the residue tuple.

The five residues are w=5,27,9,α,7−α, where
α²−7α+28 is irreducible over F101. The two extension residues are distinct
and are not in F101. An independent 101-element check also gives exactly
5,27 as the quadratic's prime-field roots and 9 as the cubic's prime-field
root. The recorded determinants, in the basis (1,α), are:

| w | 52×52 syzygy determinant | 12×12 selected Jacobian determinant |
|---|---|---|
| 5 | 4 | 11 |
| 27 | 38 | 29 |
| 9 | 39 | 44 |
| α | 82+30α | 59+16α |
| 7−α | 90+71α | 70+85α |

The two final rows are conjugate pairs, consistently with α↦7−α. Their
nonzero norms are respectively 58 and 87 modulo 101. Thus all five
determinants are units in the appropriate complete DVR: O for the first
three tuples and the unramified quadratic extension O2 for the other two.

For every branch the selected indices are the same twelve zero-based
indices

    0,1,2,3,36,37,38,39,42,43,46,47.

The complementary 52 columns are exactly those in the certified syzygy
minor. Hensel lifting solves these selected equations uniquely in each
residue class. To justify the remaining equations, substitute into the
**exact** lifted identity FR=0, divide by π in the torsion-free coefficient
ring, and extract the 150 binary-quartic coefficients. This gives
T(U,Y)E(U,Y)=0. At the Hensel point, the 52 chosen rows reduce to the
certified invertible 52-column block. Since the other twelve E entries
vanish, that block forces every omitted E entry to be zero. This uses
neither a finite residual extrapolation nor a rank statement at an
unrelated point. Having a lower bound 52 for this block suffices; an
unproved generic equality for the full rank of T is not needed.

All coefficients of the selected twelve equations lie in L. Their
Jacobian is invertible at the p-adic solution, so the field generated by
the twelve line parameters has zero relative differentials over L and
is a finite extension in characteristic zero. The degree-2 and degree-3
Q[w] fields in the certificate describe the **central first-order
solutions**. They are not asserted to be the coefficient fields of the
actual lines, and a degree-one or degree-two local completion does not
bound their global degrees.

## Reducedness, normal bundle and distinctness

Write J_E for the selected divided Jacobian. The raw selected containment
Jacobian in U,D is

    J_raw = π J_E diag(I_4, π^(−1) I_8),
    det(J_raw) = π^(12−8) det(J_E) = π⁴ det(J_E) ≠ 0.

Therefore the full line scheme in the 12-dimensional Grassmann chart has
zero Zariski tangent space at each constructed line. Its Noetherian local
ring has maximal ideal m with m/m²=0; Nakayama gives m=0. This proves both
isolation and reducedness in the complete line scheme, not merely in a
subsystem or restricted search. The coordinate choice a=s,b=t is an open
Grassmann chart and therefore loses no infinitesimal directions there.

For a line inside the audited smooth threefold, its normal sheaf is a
rank-two bundle and the line-scheme tangent space is H0(N). Adjunction
with K_X=O gives det(N)=O_P1(−2). After splitting N=O(a)⊕O(b) over an
algebraic closure, H0(N)=0 implies a,b<0; a+b=−2 forces a=b=−1.

Within the original facet the five residue w values distinguish the
Grassmann points. The nonzero determinants u,v,w,z,uz−vw ensure all four
support forms are nonzero and have four distinct face crossings. Applying
the identity and the stated two group elements gives support facets
abce,aegh,bcgh; this also agrees with direct evaluation of all six stored
group permutations. A line with full four-coordinate support cannot lie
in the intersection of two distinct facets. Consequently all fifteen
reductions, and hence all fifteen generic lines, are distinct. The latter
step uses separatedness of the Grassmannian: equal generic lines would
have equal integral reductions after taking a common finite extension.

## Scope and remaining assumptions

No genuine gap was found in the at-least-fifteen theorem. The potential
failure modes examined were scaling the wrong number of parameters,
using only selected equations without closure, conflating residue fields
with global fields, inferring reducedness from isolation, missing
Grassmann directions, and double-counting symmetry images. Each is
addressed above. The only detected defect was the original cosmetic
four-versus-six label, already corrected in the executed v2 script.

The exact coefficient fibre, integral first-jet matching, exact FR=0 with
the exported central syzygies, equivariance, and smooth Calabi–Yau property
remain the previously stated audit assumptions. The theorem does not
assert that the whole line scheme is finite or has length fifteen. The
proposed stronger classification of all facet-transverse reductions has
not been checked in this review and must be reported separately if pursued.
