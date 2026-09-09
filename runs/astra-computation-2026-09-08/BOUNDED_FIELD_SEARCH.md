# What the coefficient-field searches did and did not prove

**PROVED already, within the accepted geometric trust boundary:** the
271-variable Hensel-selected algebraic-number presentation defines a
particular smooth fibre. This note concerns only shortening that field
presentation. No failed search here changes the Picard/Hodge theorem.

## Exact input

The values in `data/ramified_hensel_pi56.json` belong to

    (Z/(101^8))[pi]/(pi^7-101) = O/(pi^56).

They are true mixed-characteristic approximations of the selected point,
not the earlier F101[q]/q33 series. Their SHA256 is
`693a9a4636d7f8fcf472c61a95202fa3ed783950b9539853d9b218d5a5c6aef2`.

## Completed bounded tests

| Coefficient ansatz | Exact outcome |
|---|---|
| Every theta in Q(pi), seven rational power-basis coefficients each of numerator/denominator height<=10^7 | **FAILED** already on theta1's constant coefficient. The independent integer Euclidean witness is in `certificates/independent_degree7_height_check.json`. |
| A nonzero P(theta1)=0 of relative degree<=2, integral pi-basis coefficient height<=1000 | **COMPUTER-CERTIFIED excluded.** |
| The same quadratic ansatz for theta2 | **COMPUTER-CERTIFIED excluded.** |
| A nonzero P(theta1)=0 of relative degree<=3, integral pi-basis coefficient height<=100 | **COMPUTER-CERTIFIED excluded.** |
| The same cubic ansatz for theta2 | **COMPUTER-CERTIFIED excluded.** |
| A nonzero P(theta1)=0 of relative degree<=3, integral pi-basis coefficient height<=1000 | **COMPUTER-CERTIFIED excluded by exhaustive sphere enumeration:**34 assignments, only the zero leaf. |
| The same cubic ansatz for theta2 | **COMPUTER-CERTIFIED excluded by separately authorized exhaustive sphere enumeration:**34 assignments, only the zero leaf. |

Here

    P(T)=sum_(j=0..d) sum_(r=0..6) c_(j,r)*pi^r*T^j,
    c_(j,r) in Z,    max |c_(j,r)| <= height.

These exclusions do not bound the actual field degree without a
coefficient-height hypothesis. They do not exclude a different primitive
generator or a larger-height presentation over Q(pi).

## Why the negative lattice certificates are rigorous

**PROVED.** All vectors c with P(theta)=0 modulo pi56 form a full integer
lattice in Z^n, where n=7(d+1). Its explicitly constructed index is
`(101^8)^7`. The saved reduction carries an exact unimodular transformation.
The script checks that transformation, the determinant, and modular
membership of every row, then recomputes Gram--Schmidt over Q.

For any full basis b_i with orthogonalized vectors b_i*, a nonzero
integer combination v has length at least min_i ||b_i*||. Indeed, take
the largest index with nonzero integer coefficient and project onto that
orthogonal direction. A coefficient vector of height<=B has squared
length<=n B². Thus

    min_i ||b_i*||² > n B²

excludes every vector in the height box. The strict inequality is recorded
as an exact rational comparison, not a floating-point estimate. A global
algebraic relation would reduce to one of these modular vectors, so the
modular exclusion also excludes a global relation in the same box.

The converse is not asserted: finding a short modular vector only gives
a candidate polynomial. Success still requires representing all291
generator coefficients over the proposed exact field, checking every
full Schur/FR identity, and verifying the original Hensel selector.

## Measured progress before the only continuations

The four initial probes took44.213s and15.59MiB sampled RSS. Both
quadratic reductions finished. Both cubic reductions hit the declared
10000-iteration gate. They were **not** simply restarted.

The checkpoint diagnostic independently recomputed exact Gram--Schmidt
data, unimodular transforms and the integer potential

    Phi = product of all prefix Gram determinants.

At every LLL swap Phi decreases by a factor strictly less than3/4.
The stored checkpoints satisfy the corresponding exact multiplicative
decrease, and a last25-step replay from freshly recomputed data matches
the saved terminal basis. This established measured progress and ruled
out the suspected update cycle before authorizing continuation.

Theta1 then finished after1084 additional iterations in4.792s guarded
time. Theta2's separately audited continuation used5.306s guarded time.
Both recalculated all Gram--Schmidt data every100 steps; no arithmetic
drift occurred. No coordinate, degree, height or uniformizer precision
was enlarged during those continuations.

The authoritative completed cubic certificates are

- `data/lll_theta1_cubic_audited_resume/audited_resume_result.json`
- `data/lll_theta2_cubic_audited_resume/audited_resume_result.json`

The earlier capped states remain in `data/padic_relative_degree_pi56/`;
their old summary is intentionally not rewritten to conceal the cap.

## Exhaustive sphere enumeration settled the remaining declared boxes

**COMPUTER-CERTIFIED:** the exact Fincke--Pohst searches in both completed
28-dimensional cubic lattices exhausted the sphere of squared radius
28000000. Each visited34 integer assignments and reached exactly one
leaf, the zero vector. Consequently there is no nonzero lattice vector
in the sphere and no polynomial coefficient vector in the height1000
box. This is an exhaustive bounded negative result, not absence of a
short LLL basis vector.

The theta1 search used0.003950 seconds, its Python process0.186176
seconds, and its guard1.216 seconds. Theta2's separately authorized
search used0.002029 seconds, its process0.173800 seconds, and its
guard1.197 seconds. Its limits were100000 assignments,120 internal
seconds, and an outer300-second/2800MiB guard. No cap was approached.

The complete exact bases, rational GSO data, search status and empty
terminal DFS stacks are preserved in

- `data/theta1_cubic_height1000_enumeration/summary.json`
- `data/theta2_cubic_height1000_enumeration/summary.json`

The generic enumeration source was not edited for theta2. The separate
`scripts/enumerate_theta2_height_box.py` wrapper rechecked the original
source hash, actual point hash, selected coordinate, complete kernel
lattice, unimodular transform, determinant and modular membership, then
called the same exact DFS routine. Its smoke tests again matched tiny
exhaustive integer-lattice enumerations, including interrupted-stack
resumption. The first sandboxed guard attempt failed closed because
`ps` was unavailable; no search process started. The identically bounded
command then ran after approval for the read-only process/RSS guard.

## A short human-checkable certificate behind the34-node searches

**COMPUTER-CERTIFIED rational inequalities; PROVED deductions.** Use
zero-based indices, write B_i=||b_i*||², and R=28000000. The exact
saved GSO coefficients all satisfy |mu_(i,j)|<=1/2. The following
coarse bounds were checked by rational comparison, not floating point.

For theta1, every B_i except B_24 exceeds R, and B_24>24000000.
In a nonzero sphere vector v=sum a_i b_i, its highest nonzero coefficient
must therefore be a_24=+/-1. Only less than4000000 of the squared-norm
budget remains. If j<24 is the highest lower nonzero coefficient, its
orthogonal component has absolute coefficient at least1/2, contributing
more than R/4=7000000. This is impossible. Thus v=+/-b_24, but

    ||b_24||² = 421425243 > R.

This excludes the sphere without expanding a large polynomial relation.

For theta2, every B_i except B_25 and B_27 exceeds R. We have
B_25>19000000, B_27>26000000, B_24>31000000, and B_j>43000000
for j<24. Also |mu_(25,24)|<3/8.

- If the highest nonzero index is27, its coefficient is+/-1 and less
  than2000000 remains. Every lower B_j exceeds19000000, so any highest
  lower nonzero coefficient contributes more than19000000/4. Hence all
  lower coefficients vanish, but ||b_27||²=514215978>R.
- If the highest nonzero index is25, its coefficient is+/-1 and less
  than9000000 remains. A highest lower nonzero index j<24 contributes
  more than43000000/4>9000000. At j=24 the sharper bound gives a
  contribution greater than31000000·(5/8)²=12109375>9000000.
  Therefore again all lower coefficients vanish, but
  ||b_25||²=373614447>R.

These are the only possible highest indices. Thus both exact lattices
contain no nonzero vector of squared norm at most R. The compact
inequalities independently explain the exhaustive search outputs.

**Stop:** all declared height1000 quadratic/cubic ansätze for theta1
and theta2 are now excluded. Do not reinterpret this as a lower bound
on the actual number-field degree without coefficient-height hypotheses.
No additional precision, coordinate, degree, height box or further
computation is authorized by these negative results.
