-- Kapustka Table 1 No. 8 : explicit construction, stage 1.
-- Records every random choice explicitly in data/ so the run is replayable.
kk = ZZ/32003; setRandomSeed 20260911;
A = kk[s,t,u,v];
mons = matrix{{s^2*u^2, s^2*u*v, s^2*v^2, s*t*u^2, s*t*u*v, s*t*v^2, t^2*u^2, t^2*u*v, t^2*v^2}};
Mproj = random(kk^7, kk^9);
"data/Mproj.m2" << "Mproj = matrix " << toExternalString entries Mproj << endl << close;
gs = mons * transpose Mproj;
P6 = kk[x_0..x_6];
IS = ker map(A, P6, gs);
"data/IS.m2" << "IS = ideal " << toString first entries gens IS << ";" << endl << close;
G = gens IS;
print("-- I_S generator degrees: " | toString flatten degrees source G);
cq = random(kk^3, kk^2);  "data/coeff_q.m2" << "cq = matrix " << toExternalString entries cq << endl << close;
qq = submatrix(G,{0,1,2}) * cq;
q1 = qq_(0,0); q2 = qq_(0,1);
C3 = super basis(3, module IS);
cF = random(kk^(numColumns C3), kk^1); "data/coeff_F.m2" << "cF = matrix " << toExternalString entries cF << endl << close;
F = (C3*cF)_(0,0);
IX = ideal(q1,q2,F);
"data/IX.m2" << "IX = ideal " << toString first entries gens IX << ";" << endl << close;
print("-- codim X' = " | toString codim IX | " , dim Proj X' = " | toString(dim IX -1) | " , deg X' = " | toString degree IX);
-- nodes: singular points all lie on S; compute the degeneracy scheme on S
BS = P6/IS;
jac = jacobian matrix{{q1,q2,F}};
Zsing = ideal mingens minors(3, sub(jac, BS));
print("-- on S: dim of degeneracy locus (Proj) = " | toString(dim Zsing - 1) | " , degree = " | toString degree Zsing);
print("-- reduced? deg radical = " | toString degree radical Zsing);
