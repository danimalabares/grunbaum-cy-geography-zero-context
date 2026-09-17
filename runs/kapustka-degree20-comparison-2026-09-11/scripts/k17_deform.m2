-- Stage 6 (decisive): graded first-order deformations of Ybar inside P(1^8,2^2),
-- and the 2x2 matrix of y-coefficients acquired by the two degree-2 equations.
-- Ybar deforms into P^7 (to first order) iff some deformation makes that matrix invertible.
kk = ZZ/32003;
Pw = kk[x_0..x_6, w, y_1, y_2, Degrees => {1,1,1,1,1,1,1,1,2,2}];
load "data/IYbar.m2";                       -- IB
F0 = mingens IB;
dg = flatten degrees source F0;
stderr << "generator degrees: " << toString dg << endl;
q2i = positions(dg, d -> d == 2);
stderr << "degree-2 generator positions: " << toString q2i << endl;
stderr << "degree-2 generators y-free ? "
       << toString all(q2i, i -> (coefficient(y_1, F0_(0,i)) == 0 and coefficient(y_2, F0_(0,i)) == 0)) << endl;
needsPackage "VersalDeformations";
stderr << "computing normalMatrix ..." << endl;
T1 = normalMatrix({0}, F0);
stderr << "T1 size = " << toString(numRows T1, numColumns T1) << endl;
N = numColumns T1;
lift1 = f -> (try lift(f, Pw) else f);
Cs = apply(N, j -> matrix{
      {coefficient(y_1, lift1 T1_(q2i#0, j)), coefficient(y_2, lift1 T1_(q2i#0, j))},
      {coefficient(y_1, lift1 T1_(q2i#1, j)), coefficient(y_2, lift1 T1_(q2i#1, j))}});
-- span of the 2x2 matrices inside k^4
V = matrix apply(4, r -> apply(N, j -> (Cs#j)_(r//2, r%2)));
V = sub(V, kk);
rk = rank V;
stderr << "dim of the span of the y-coefficient matrices in M_2 = " << toString rk << endl;
if rk > 0 then (
  B = mingens image V;                       -- 4 x rk
  tvars = kk[t_1..t_(numColumns B)];
  Cgen = matrix{{sum(numColumns B, i -> t_(i+1)*sub(B_(0,i),tvars)), sum(numColumns B, i -> t_(i+1)*sub(B_(1,i),tvars))},
                {sum(numColumns B, i -> t_(i+1)*sub(B_(2,i),tvars)), sum(numColumns B, i -> t_(i+1)*sub(B_(3,i),tvars))}};
  dd = det Cgen;
  stderr << "generic determinant on the span = " << toString dd << endl;
  stderr << "an invertible matrix occurs ? " << toString(dd != 0) << endl;
) else stderr << "the y-coefficient map is IDENTICALLY ZERO" << endl;
"data/T1_size.txt" << toString(numRows T1, numColumns T1) << " span=" << toString rk << endl << close;
stderr << "done" << endl;
