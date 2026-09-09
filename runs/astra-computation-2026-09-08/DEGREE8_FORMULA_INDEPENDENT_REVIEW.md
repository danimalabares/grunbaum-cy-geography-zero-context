# Independent check of the degree-eight Picard formula

2026-09-08. **PROVED within the stated hypotheses:** the derivation in
`DEGREE8_PICARD_FORMULA.md` gives

    h11 = 1748 + h0(N) - dim(I²)_8.

This reviewer independently reconstructed the signs, ranks, and
hypercohomology arguments below. No computation was run. Qualified human
verification is not claimed; agreement is not an additional mathematical
certificate beyond these explicit checks.

For the signed flip on P tensor P, the antisymmetric summand has

    G1=P1,
    G2=P2 + Sym²P1,
    G3=P3 + P1 tensor P2,
    G4=P4 + P1 tensor P3 + exterior²P2,
    G5=P1 tensor P4 + P2 tensor P3,
    G6=P2 tensor P4 + Sym²P3,
    G7=P3 tensor P4,
    G0=G8=0.

The symmetric terms in degrees2 and6 are essential: the factors have odd
homological degree. Their dimensions give exactly 692,5760,14796,12672
for the dual ambient H7 row. The omitted terms have twists strictly
between -8 and0 and therefore have no ambient cohomology.

**PROVED sign check:** on a local Koszul model a degree-one Tor generator
is e tensor1 - 1 tensor e. The flip negates it, so it acts on exterior^i C
by (-1)^i. Hence G has homology C in degree1 and exterior³C in degree3.
The hypercohomology terms H²C and H³C have no incoming differential and
their only potential outgoing differential is d3 to H5/H6(exterior³C),
both zero by support dimension. Hyper-H3 is zero. Since G_i contributes
ambient total degree7-i, duality reverses the row into the stated scalar
chain. This gives

    rank δ5 = 5760 - 692 - h0(N) = 5068 - h0(N),
    h²C = 14796 - rank δ5 - rank δ6.

**PROVED final-map check:** write u in P3 and w in P4. The antisymmetric
degree-seven representative is u tensor w - w tensor u, and its
differential is

    d3u tensor w - w tensor d3u
      - (u tensor d4w + d4w tensor u).

After dualizing and using the self-dual resolution this is R(8) together
with the polar map u⊙v -> F(u)v+F(v)u, up to signs and invertible basis
changes. Modulo R, the target is I(8), and the polar image is 2I²(8).
Since char(k)!=2, the cokernel is the graded module (I/I²)(8). Therefore

    rank δ6 = 12672 - (4691-r) = 7981+r,
    h²C = 1747 + h0(N) - r.

The conormal/Euler formula h11=1+h²C gives the asserted identity. The
identification occurs before sheafification, so substituting dim(I²)_8
does not assume that I² is saturated or has already been resolved.

**PROVED prerequisite check:** in a flat nearby family from the stated
special resolution, Betti semicontinuity permits no entries outside the
special Betti support. Each relevant shift 0,3,4,5,8 occurs in only one
homological degree. The fixed Hilbert numerator therefore locks the ranks
1,16,30,16,1; there is no adjacent equal-shift cancellation available.
Thus using this self-dual resolution on the smooth generic fibre is
consistent with the flat-family inputs.

**PROVED consequence:** h0(N)<=94 and h11>=1 imply r<=1841. An exact
matrix-rank lower bound r>=1841 therefore forces h0(N)=94, r=1841,
h11=1, h21=31, Euler=-60. This remains conditional on obtaining a valid
rank certificate with correct q-adic precision. It does not settle
Picard torsion, fundamental group, or explicit finite fibre coefficients.
