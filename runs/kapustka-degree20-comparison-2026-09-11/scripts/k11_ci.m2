-- Stage 2: the nodal (2,2,3) complete intersection X' and its 44 nodes.
kk = ZZ/32003; setRandomSeed 20260911;
P6 = kk[x_0..x_6];
load "data/IS.m2";                      -- IS
G = gens IS;
load "data/coeff_q.m2";                 -- cq (3x2)
qq = submatrix(G,{0,1,2}) * cq;  q1 = qq_(0,0); q2 = qq_(0,1);
-- a general cubic in (I_S)_3 = <linear * quadrics> + <14 cubics>
L = random(P6^1, P6^{3:-1});            -- 3 linear forms
cc = random(kk^16, kk^1);
F = (L * transpose submatrix(G,{0,1,2}))_(0,0) + (submatrix(G, toList(3..18)) * cc)_(0,0);
"data/coeff_F.m2" << "L = matrix " << toExternalString entries L << "; cc = matrix " << toExternalString entries cc << endl << close;
IX = ideal(q1,q2,F);
"data/IX.m2" << "IX = ideal " << toString first entries gens IX << ";" << endl << close;
print("codim_Xprime " | toString codim IX);
print("dimProj_Xprime " | toString(dim IX - 1));
print("degree_Xprime " | toString degree IX);
print("IS_subset_IX " | toString isSubset(IX, IS));
BS = P6/IS;
jac = jacobian matrix{{q1,q2,F}};
Z = minors(3, sub(jac, BS));
print("nodes_dimProj " | toString(dim Z - 1));
print("nodes_degree " | toString degree Z);
print("nodes_degree_radical " | toString degree radical Z);
