-- Stage 4: explicit models  Y in P^7  and  Ybar in P(1^8,2^2).
kk = ZZ/32003;
P6 = kk[x_0..x_6];
load "data/IS.m2"; load "data/IX.m2"; load "data/G.m2"; load "data/Q.m2";
mg = first entries mingens Q;
byd = d -> select(mg, f -> first degree f == d);
g4  = first byd 4;  g5 = byd 5;
stderr << "generators by degree: " << toString apply(mg, f->first degree f) << endl;
stderr << "#deg4 = " << #(byd 4) << " , #deg5 = " << #g5 << endl;

--------------------------------------------------------------------- Y in P^7
P7 = kk[x_0..x_6, w];
inc = map(P7, P6, matrix{{x_0,x_1,x_2,x_3,x_4,x_5,x_6}});
G7 = inc GG;
IY = saturate(inc IX + ideal(w*G7 - inc g4), G7);
stderr << "Y: dimProj = " << toString(dim IY - 1) << " , degree = " << toString degree IY << endl;
stderr << "Y: gen degrees = " << toString flatten degrees source mingens IY << endl;
RY = P7/IY;
stderr << "Y: Hilbert function 0..4 = " << toString apply(5, n -> hilbertFunction(n, RY)) << endl;
stderr << "Y: Hilbert polynomial = " << toString hilbertPolynomial(RY, Projective => false) << endl;
stderr << "Y: q1,q2 in I_Y ? " << toString(isSubset(ideal(inc (gens IX)_(0,0), inc (gens IX)_(0,1)), IY)) << endl;
"data/IY.m2" << "IY = ideal " << toString first entries mingens IY << ";" << endl << close;
stderr << "saved IY" << endl;
