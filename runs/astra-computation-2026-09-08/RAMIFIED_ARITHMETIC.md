# Finite ramified fibre: export and actual arithmetic

## Outcome and exact meaning

**CONDITIONAL on the accepted source/chart computer-certificate boundary.**
The finite algebraic coefficient point is now specified and mathematically
reviewed. Its actual 16 cubic equations are in
`RAMIFIED_FIBRE_EQUATIONS.md`; their finite coefficient system is
`data/ramified_fibre_coefficients.json`. The system has 271 algebraic
variables: pi and 270 dependent generator coefficients. It consists of
pi^7-101 and 270 explicitly indexed bordered determinants of sizes 22,
14, and 33, using shared exact rational linear-form matrices.

All 21 other generator coordinates are the ORIGINAL normalized six-jet
polynomials evaluated at pi. The chosen root satisfies theta_i in pi O,
where O=Z_101[pi]. Its selected 270-square Jacobian has determinant 19
modulo 101, so it is the unique Hensel root with these congruences.

**PROVED field distinction.** The coefficient field is the number field

    L=Q(pi,theta_1,...,theta_270) inside Q_101(pi).

The fact that it embeds in the degree-seven *local* field Q_101(pi) does
not imply L=Q(pi), or that [L:Q]=7. Finite algebraic equations plus the
unique p-adic isolating condition specify L without a primitive element.
The source finite smoothness identities transport to this point; see
`RAMIFIED_POINT_CONSTRUCTION.md` and `RAMIFIED_POINT_REVIEW.md`.

## The actual mixed-characteristic computations

**PROVED ring maps.** For e=2 and e=8 there is a homomorphism

    (Z/101^e Z)[q]/(q^(7e)) -> (Z/101^e Z)[pi]/(pi^7-101)
                              = O/(pi^(7e)),
    q -> pi.

For a coefficient sequence c_0,...,c_(7e-1), substitution is the exact
seven-entry vector

    (sum_(k=0)^(e-1) 101^k c_(i+7k) mod101^e)_(i=0,...,6).

The scripts recompute the ORIGINAL free-path formal solution over the
nonfield Z/101^e Z. They choose Gaussian pivots that are nonzero modulo
101 and invert them modulo 101^e. A nonzero multiple of 101 is not a
permitted pivot. They do not reuse the old F101 coefficient jets.

At every q-order all 6960 original Schur equations are verified. The
averaged-section syzygy graphs are then reconstructed in the 21,13,32
multiplicity blocks, and the coefficients are folded by pi^7=101. Finally
all 490 equations AU-B and all 1160 equations D-CU are checked *directly*
in the seven-entry mixed-characteristic ring. The 21 exact free-coordinate
polynomials are also evaluated and compared there.

**COMPUTER-CERTIFIED pi^14 result.** The recomputation through q^13 over
Z/10201Z passed every coefficient and all 1650 direct block identities.
The root approximation is `data/ramified_hensel_pi14.json`. Concrete
coefficient examples are displayed in `RAMIFIED_HENSEL_ARITHMETIC.md`.

**COMPUTER-CERTIFIED pi^56 result.** The recomputation through q^55 over
Z/101^8 Z likewise passed every coefficient and all 1650 direct block
identities. The actual higher-precision point is
`data/ramified_hensel_pi56.json`. The pi^14 source and artifacts were
preserved; pi^56 used a separate script and records both source hashes.

**PROVED logical separation.** These computations improve arithmetic at
one *already specified algebraic point*. They are not an extension of
the failed F101(q) rational-family search. Conversely, neither a finite
p-adic approximation nor a fitted rational function would independently
prove exact all-orders identities. Here exactness and smoothness rest on
the finite coefficient equations, Hensel uniqueness, the fixed-chart
argument, and the transported source certificates.

## A precisely bounded degree-seven field test

**FAILED bounded-height representation.** At pi^56 precision the script
attempted to reconstruct each of the 270 dependent coefficients in the
basis 1,pi,...,pi^6 as rational numbers with

    |numerator| <= 10^7,    1 <= denominator <= 10^7.

Known free-coordinate polynomials were excluded. This reconstruction is
unique if it exists, because

    2*(10^7)^2 < 101^8 = 10828567056280801.

The first tested entry already failed: the basis-constant coefficient of
theta_1 is congruent to 5101489845552212 modulo 101^8, and has no rational
representative within those bounds. The exact diagnostic is in
`data/ramified_degree7_height_screen.json`. The computation therefore
stopped the field test after one entry; it did not assert that all 1890
entries separately fail.

**PROVED explanation of this negative certificate.** A bounded rational
a/b satisfying a=r*b modulo M gives

    |r/M-k/b|=|a|/(M*b)<1/(2*b^2)

for the corresponding integer k, so k/b must be a continued-fraction
convergent. Euclid's algorithm reaches its first remainder at most 10^7
at remainder 494395, with denominator magnitude 306178586, already
above the permitted bound. Its exact identity is

    494395 = (-306178586)*5101489845552212
             + 144245027*10828567056280801.

Earlier convergents have remainders above the numerator bound and later
convergents have larger denominators. Thus the rejection is a bounded
exact arithmetic statement, not merely a poor numerical fit.

**OPEN.** This does not prove L is different from Q(pi); it does not bound
[L:Q]; and it says nothing against a degree-seven representation with
larger coefficient height. No further precision is authorized by this
attempt. A prospective exact verifier is prepared in
`scripts/verify_degree7_point.py`: had all 1890 entries reconstructed, it
would solve the Schur systems over Q[T]/(T^7-101), verify all full
identities and the root selector, and only then certify L=Q(pi). It was
not run because there was no candidate.

## Commands and measured resources

All commands were run sequentially under the single-process guard with
OMP, OpenBLAS, MKL, and VecLib thread counts equal to one. No CAS ran.

| Job | Guarded elapsed time | Sampled peak RSS | Result |
|---|---:|---:|---|
| Finite coefficient/cubic export | 2.490 s | 23.4 MiB | PASS |
| First pi^14 invocation | 3.763 s | 26.7 MiB | Stopped before lifting; sparse zero-entry assertion |
| Corrected genuine pi^14 lift | 12.187 s | 37.3 MiB | PASS all identities |
| Genuine pi^56 lift and field-height screen | 205.537 s | 63.9 MiB | PASS arithmetic; bounded field-height test FAILED |

The exact commands, run from this directory, were:

```sh
python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag ramified-fibre-export -- python3 -B scripts/export_ramified_fibre.py
python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag ramified-hensel-pi14-cleaned-operator -- python3 -B scripts/ramified_hensel_pi14.py
python3 -B scripts/run_guarded.py --seconds 1800 --memory-mb 2800 --tag ramified-point-pi56-height -- python3 -B scripts/ramified_hensel_pi56.py
```

Logs and order checkpoints have stems

```text
logs/20260908T130325-ramified-fibre-export
logs/20260908T130717-ramified-hensel-pi14
logs/20260908T130846-ramified-hensel-pi14-cleaned-operator
logs/20260908T131634-ramified-point-pi56-height
```

Existing outputs are deliberately not overwritten. Use the saved results
and independent verifiers for a non-mutating replay; reproduce generation
in a fresh copied run directory with the same recorded inputs. Do not
delete successful artifacts merely to rerun a command.

The failed first pi^14 invocation was a sparse-data representation bug:
the reused operator kept dictionary entries with coefficient zero, whereas
the chart omitted them. It stopped before producing any lifted order.
The failed source is preserved in
`data/failed_attempt_sources/ramified_hensel_pi14_before_zero_cleanup.py`.
After removing those zero entries, no mathematical lifting residual failed.
