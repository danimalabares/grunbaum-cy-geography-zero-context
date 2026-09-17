-- Stage 3: the unprojection Y in P^7 and the normal model Ybar in P(1^8,2^2),
-- computed by liaison inside the complete intersection X'.
-- Hom_{O_X'}(I_S, O_X') = (1/G) I_{S'} where S' is linked to S by a cubic G in I_S.
kk = ZZ/32003; setRandomSeed 20260911;
P6 = kk[x_0..x_6];
load "data/IS.m2"; load "data/IX.m2";
Gm = gens IS;
GG = (submatrix(Gm, toList(3..16)) * random(kk^14, kk^1))_(0,0);   -- a general cubic in I_S
print("G_in_IX " | toString(GG % IX == 0));
ISp = saturate((IX + ideal GG) : IS);          -- the linked surface S'
print("degS_prime " | toString degree ISp | "  dimProj " | toString(dim ISp - 1));
-- degree-1, degree-2 unprojection data: elements of (I_{S'})_d modulo I_{X'} + G*(lower)
for d in {3,4,5} do (
  V = super basis(d, module ISp);
  W = super basis(d, module (IX + ideal GG));
  print("d=" | toString d | "  dim (I_S')_d = " | toString numColumns V | "   dim (I_X' + (G))_d = " | toString numColumns W);
);
"data/G.m2" << "GG = " << toString GG << ";" << endl << close;
"data/ISprime.m2" << "ISp = ideal " << toString first entries gens ISp << ";" << endl << close;
