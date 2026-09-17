-- Stage 3 (fast): unprojection data by liaison, no saturation.
-- Hom_{O_X'}(I_S,O_X')_d  <->  { g in (I_{X'}+(G)) : I_S  of degree deg(G)+d } / (I_{X'}+ lower)
kk = ZZ/32003; setRandomSeed 20260911;
P6 = kk[x_0..x_6];
load "data/IS.m2"; load "data/IX.m2";
Gm = gens IS;
GG = (submatrix(Gm, toList(3..16)) * random(kk^14, kk^1))_(0,0);
stderr << "G not in I_X' : " << toString(GG % IX != 0) << endl;
A = IX + ideal GG;
stderr << "computing colon ideal ..." << endl;
Q = quotient(A, IS, DegreeLimit => 5);
stderr << "colon gen degrees: " << toString flatten degrees source gens Q << endl;
-- (dimension loop removed: the mingens degrees above already give the answer)
"data/G.m2" << "GG = " << toString GG << ";" << endl << close;
"data/Q.m2" << "Q = ideal " << toString first entries gens Q << ";" << endl << close;
stderr << "saved" << endl;
