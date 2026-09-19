-- c01: the Stanley-Reisner side, exactly over QQ.
-- Frozen I_M (scripts/verify_geography.m2 of the repository root).
S = QQ[a,b,c,d,e,f,g,h];
I = ideal(a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,b*d*f,b*d*g,b*e*g,
          c*d*e,c*e*g,c*e*h,c*f*h,d*e*f,d*f*h,e*f*g);
A = S/I;
stderr << "codim I_M = " << codim I << "  (so dim Proj = " << (dim I - 1) << "), degree = " << degree I << endl;
B = betti res I;
stderr << "Betti table of S/I_M:" << endl << B << endl;
stderr << "Hilbert function 0..5 = " << toString apply(6, n -> hilbertFunction(n, A)) << endl;
hs = hilbertSeries(A, Reduce => true);
stderr << "reduced Hilbert series (numerator = h-vector) = " << toString hs << endl;
stderr << "Hilbert polynomial = " << toString hilbertPolynomial(A, Projective => false) << endl;
-- quadrics vanishing on SR(M)?  dim (I_M)_2 = 36 - HF(2)
stderr << "dim (I_M)_2 = " << (binomial(9,2) - hilbertFunction(2, A)) << ",  dim (I_M)_3 = " << (binomial(10,3) - hilbertFunction(3, A)) << endl;
-- Zariski tangent space at the coordinate point  a = 1, b = ... = h = 0  (chart a = 1):
-- the local equations are the generators with a set to 1; dimension of the tangent space
-- = 7 - rank of the linear parts at the origin of the chart.
S7 = QQ[b,c,d,e,f,g,h];
chart = map(S7, S, {1_S7, b, c, d, e, f, g, h});   -- the affine chart a = 1 around the vertex a
Ja = chart I;
L = ideal select(flatten entries gens Ja, p -> first degree p == 1);
stderr << "chart a=1: generator degrees = " << toString sort flatten degrees source gens Ja << endl;
stderr << "chart a=1: number of independent linear forms among generators = " << (if L == 0 then 0 else numgens trim L) << endl;
-- tangent space dimension via the Jacobian at the origin
Jac = sub(jacobian Ja, apply(gens S7, v -> v => 0));
stderr << "chart a=1: rank of Jacobian at the vertex = " << rank Jac << ",  dim T_p SR(M) = " << (7 - rank Jac) << endl;
-- the link of vertex a: the SR scheme of the chart is the affine cone over SR(link a)
stderr << "chart a=1: dim of the affine cone = " << dim Ja << ", degree = " << degree Ja << endl;
-- Gorenstein check: the last Betti number is 1 and the resolution is self-dual (read off the table).
stderr << "length of resolution = " << length res I << ",  last Betti number = " << toString (B#(length res I, {8}, 8)) << endl;
