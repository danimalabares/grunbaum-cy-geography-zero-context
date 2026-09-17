-- Stage 5: the normal contracted threefold Ybar inside P(1^8, 2^2).
kk = ZZ/32003;
P6 = kk[x_0..x_6];
load "data/IS.m2"; load "data/IX.m2"; load "data/G.m2"; load "data/Q.m2";
mg = first entries mingens Q;
byd = d -> select(mg, f -> first degree f == d);
g4 = first byd 4;  g5 = byd 5;
Pw = kk[x_0..x_6, w, y_1, y_2, Degrees => {1,1,1,1,1,1,1,1,2,2}];
inc = map(Pw, P6, matrix{{x_0,x_1,x_2,x_3,x_4,x_5,x_6}});
Gw = inc GG;
J0 = inc IX + ideal(w*Gw - inc g4, y_1*Gw - inc(g5#0), y_2*Gw - inc(g5#1));
stderr << "saturating ..." << endl;
IB = saturate(J0, Gw);
stderr << "Ybar: dimProj = " << toString(dim IB - 1) << " , degree = " << toString degree IB << endl;
stderr << "Ybar: gen degrees = " << toString flatten degrees source mingens IB << endl;
RB = Pw/IB;
stderr << "Ybar: Hilbert function 0..5 = " << toString apply(6, n -> hilbertFunction(n, RB)) << endl;
-- (degree-2 part: dim (I)_2 = 38 - 36 = 2, i.e. exactly the two degree-2 generators)
"data/IYbar.m2" << "IB = ideal " << toString first entries mingens IB << ";" << endl << close;
stderr << "saved IYbar" << endl;
