-- Stage 3a: Hom_B(J,B) for J = I_S in B = P6/I_{X'} : the unprojection data.
kk = ZZ/32003;
P6 = kk[x_0..x_6];
load "data/IS.m2"; load "data/IX.m2";
B = P6/IX;
JB = ideal mingens sub(IS, B);
print("J_gen_degrees " | toString flatten degrees source gens JB);
H = Hom(module JB, B^1);
Hp = prune H;
print("Hom_gen_degrees " | toString flatten degrees source gens Hp);
print("Hom_numgens " | toString numgens Hp);
-- also record via syzygies, for the explicit homomorphism
KK = syz gens JB;
print("syz_shape " | toString(numRows KK, numColumns KK));
W = syz transpose KK;
print("W_shape " | toString(numRows W, numColumns W) | "  degrees: " | toString flatten degrees source W);
"data/homdata.m2" << "-- see log" << endl << close;
