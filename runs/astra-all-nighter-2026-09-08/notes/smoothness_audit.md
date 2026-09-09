# Targeted audit: smoothness of the selected ramified fibre

Scope: the smoothness-transfer step in computation-packet
`RAMIFIED_POINT_REVIEW.md`, §§5–6, against source `PROOF.md`, §4, at
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b` (actual source HEAD agrees).
This is targeted mathematical-paper-audit analysis, not qualified-human
verification. Exact input hashes are in `data/smoothness_transfer_checks.json`.
The original Singular standard-basis identities are accepted within the
user's stated boundary; no attempt was made to repeat their expensive
computations. The selected-point flatness, coefficient indexing, Hensel
uniqueness and integral omitted-equation identity are audited separately.

**PROVED with the following assumptions:** the exact O-family is flat with
pure three-dimensional geometric generic fibre; it is equivariant; its
normalized cubic row agrees with the original certified row, up to an
invertible base-only generator change, modulo π^7; and the original literal
and standard-basis certificates are valid. Under these assumptions, its
specific generic fibre over Q_101(π) is geometrically smooth. No additional
gap in the transfer step was found. This conclusion does not follow merely
from generic smoothness of an unspecified formal family.

## Claim ledger and dependency chain

| ID | Claim checked | Evidence/state |
|---|---|---|
| S1 | Modular identities through π^6 transfer to O | PROVED, quotient-ring derivation |
| S2 | Normalizing generators preserves the relevant singular ideal | PROVED, base-only Jacobian/Cauchy–Binet argument |
| S3 | The stated strata exhaust all possible specializations | COMPUTER-CERTIFIED, exact monomial/orbit check |
| S4 | Triangle critical-value obstruction applies in mixed characteristic | PROVED and COMPUTER-CERTIFIED, independent two-jet extraction below |
| S5 | Global-chart, edge and vertex witnesses apply to singular sections | CONDITIONAL on original Singular identities; source/provenance checked |
| S6 | There are no geometric generic singular points | PROVED assuming S1–S5 and exact flatness/purity |

Dependencies: exact normalized six-jet → S1,S2; central ideal and exact
equivariance → S3; flatness and S1,S2 → S4,S5; properness and purity together
with S3,S4,S5 → S6. The supplied transfer proof succeeds within those
assumptions. Its separate exact-flatness/branch assumptions are not claimed
proved by this note. Classification: supporting checks; no issue established
for the questioned smoothness implication. Confidence is high for this
narrow implication because its finite orders and every stratum are explicit.

## Transfer, basis change and valuation argument

In O=Z_101[π], π^7=101, one has exactly

    O/(π^7) = F_101[q]/(q^7),  π ↔ q.

Thus every polynomial identity modulo q^6 transfers to an identity modulo
π^6. Arbitrary integral lifts of its F_101 coefficients only change an
expression by a multiple of 101=π^7, which is beyond every required order.
Differentiation in projective coordinates does not lower π-order. No
embedding F_101→O or lift of an infinite formal series is asserted here.

Write the original row H and normalized row F with F=HP^(-1) modulo π^7,
P(0)=Id. Lift P to an integral base-only matrix. Its determinant is a unit,
so the exact row FP defines the same ideal as F and agrees with H modulo
π^7. Its affine Jacobian is Jac(F)P (with the appropriate transpose convention).
The ideals of fourth minors of these Jacobians are equal by Cauchy–Binet
and the inverse matrix. Consequently a literal identity involving a chosen
subset of source minors remains an identity in the full singular ideal.
Individual chosen minors need not survive individually.

If a geometric singular point of the generic fibre existed, it would be
defined over a finite extension K'/Q_101(π). Properness extends it over the
integer DVR O'. Normalize homogeneous coordinates to make one a unit. For
π=ετ^r, a transported identity cπ^e ∈ (F,I_4(Jac F))+(π^(e+1)), with c a
unit at its specialization, would evaluate to

    unit * τ^(er) ∈ (τ^((e+1)r)),

which is impossible. Source localization variables are inverses of
coordinates nonzero at the specified support torus, hence are integral
units on this section. This includes arbitrary ramification r.

The cover and actual identity orders are:

| Special point | Certificate order and unit |
|---|---|
| D(a),D(c),D(g),D(d),D(f) | π^5 modulo π^6; global a,d identities and equivariance |
| b,e,h all nonzero | critical value π²p modulo π³; proof below |
| exactly two of b,e,h nonzero | π^4 modulo π^5; edge-25 source identity localized at support coordinate |
| exactly one of b,e,h nonzero | (y2−33)π^5 modulo π^6; multiplier reduces to −33 at the coordinate vertex |

The b-chart identity is **only local at its coordinate vertex**. No argument
uses it on the entire chart. The independent small check verifies the
vertex orbits {a,c,g},{b,e,h},{d,f}, the three-edge orbit in {b,e,h}, and
that setting a=c=d=f=g=0 kills every central generator. The complement of
the five global opens is therefore exactly P²_(b,e,h), with the three
types listed in the table.

## A direct independent triangle argument

On b=1, e=u, h=v, invert uv and order the normal variables as
(a,c,g,d,f). Source generator rows (3,12,9,7), in one-based indexing, have
central terms

    av, cuv, ug, df.

The script verifies equality of the localized central full monomial ideal
with these four generators, and similarly verifies the six edge rows
(9,1,3,10,12,7) after inverting b,e. Given exact flatness, the map
I/πI→I_special is an isomorphism. Thus equality of the special ideals
implies equality of the completed family ideals by Nakayama. This is the
precise extra hypothesis needed to lift the central generator check.

There is a shorter proof of the triangle obstruction than appealing to a
full relative Morse normal form. Let g1,g2,g3 be the first three lifted
rows and h the fourth. Solve the eight constrained-critical equations

    g1=g2=g3=0,
    ∂h/∂x_i − Σ_(j=1)^3 λ_j ∂g_j/∂x_i=0  (i=1,…,5)

for (a,c,g,d,f,λ1,λ2,λ3). At π=0 the Jacobian has exactly one nonzero
determinant term, equal to u^4v^4. It is a support unit, so the formal
implicit function theorem applies over the completed support ring over O,
and after any finite extension O'.

The actual rational two-jet gives no constant support term in the
first-order corrections to g1,g2,g3. The first-order correction to h is
10acd+10cfg, whose normal gradient vanishes on the support torus. Therefore
the first-order constrained-critical displacement is zero. The coefficient
of π² in its exact critical value Δ is simply the restriction of the
second-order correction to source row 7. Independently parsing the supplied
JSON, the small check obtains over Q:

    Δ = π² p(u,v) + O(π³),
    p = −8u²−20uv−8v²−20u−20v−8.

No mixed-characteristic denominators occur except support units and integers
prime to 101. At a singular section the dead rows have independent normal
gradients, and the remaining hypersurface has zero differential. Hence the
section solves the constrained-critical equations and, by implicit
uniqueness, has this same critical value. Differentiating along the support
and using the constraint equations gives Δ=Δ_u=Δ_v=0. Dividing by π² and
reducing modulo τ would give a common zero of p,p_u,p_v over the geometric
residue field.

The following exact identity is rechecked independently:

    1 = 40p + (−43u+22v+22)p_u + (−22u+3v−33)p_v  mod 101.

An even smaller witness is that the two linear gradient equations have
invertible determinant −144=58 modulo 101 and unique solution
u=v=78, where p=48, not zero. This excludes the whole triangle torus.
It also shows why arbitrary perturbations by π^7 cannot spoil this step:
after division by π² they still vanish modulo the valuation maximal ideal.

## Reproduction and limitations

Run `python3 -B scripts/check_smoothness_transfer.py` from this run (or use
its absolute path). It uses only the Python standard library, exact rational
arithmetic and integer reduction modulo 101. It produces/verifies
`data/smoothness_transfer_checks.json`, including input hashes. The original
read-only `enumerate/audit_edge25_q4_certificate_sources.py` was also run
successfully; its new immutable output is
`logs/smoothness-edge-source-audit.stdout`. This source audit confirms the
actual 66-column standard basis and zero normal form of q^4 in the original
locked transcript. It does not rerun that standard basis.

Successful checks took 0.118 and 0.056 seconds with a cumulative child RSS
maximum 15,724,544 bytes. RUSAGE_CHILDREN reports a cumulative high-water
mark across the two short processes, not sampled process-group peaks. An
initial implementation check forgot to remove repeated stabilizer images
when forming vertex orbits; that bookkeeping defect was corrected before
the successful certificate, without changing mathematical inputs. An
attempt to measure using `/usr/bin/time -l` produced a valid child output
but exit 1 because sandbox policy denied `sysctl kern.clockrate`; a permitted
Python resource measurement replaced it. The failed wrapper log is preserved.
No CAS, network source search, background job or external write was used.

Remaining original assumptions: the exact a,d global identities, the local
b multiplier identity, and the edge-25 standard-basis membership; their
provenance boundary remains the frozen Singular computation. The selected
point's full exact flatness and integral agreement with the normalized
six-jet remain separate dependencies. Subject to those, no extra
smoothness hypothesis or unresolved stratum remains.
