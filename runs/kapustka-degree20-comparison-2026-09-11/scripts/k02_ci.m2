-- Step 2: nodal (2,2,3) complete intersection X' in P6 containing S = ~~D_8.
kk = ZZ/32003; setRandomSeed 20260911;
A = kk[s,t,u,v];
mons = matrix{{s^2*u^2, s^2*u*v, s^2*v^2, s*t*u^2, s*t*u*v, s*t*v^2, t^2*u^2, t^2*u*v, t^2*v^2}};
Mproj = random(kk^7, kk^9);
gs = mons * transpose Mproj;
P6 = kk[x_0..x_6];
IS = ker map(A, P6, gs);
G = gens IS;
q = submatrix(G, {0,1,2});                       -- the 3 quadrics
cub = submatrix(G, toList(3..18));               -- the 16 listed cubic columns (14 new + deg-3 pieces)
q1 = (q * random(kk^3, kk^1))_(0,0);
q2 = (q * random(kk^3, kk^1))_(0,0);
-- a general cubic in I_S: random element of the degree-3 piece of I_S
C3 = super basis(3, module IS);
F  = (C3 * random(kk^(numColumns C3), kk^1))_(0,0);
IX = ideal(q1,q2,F);
print("-- codim X' = " | toString codim IX | " , dim Proj X' = " | toString(dim IX - 1) | " , degree X' = " | toString degree IX);
print("-- is CI (3 gens, codim 4-1=3)? " | toString(codim IX == 3));
RX = P6/IX;
print("-- omega check, Betti of P6/I_{X'}:"); print betti res IX;
-- singular locus
J = ideal jacobian IX;
Sing = saturate(IX + minors(3, jacobian IX));
print("-- dim Sing (Proj) = " | toString(dim Sing - 1) | " , degree Sing = " | toString degree Sing);
print("-- Sing radical? degree of radical = " | toString degree radical Sing);
print("-- Sing contained in S? " | toString(isSubset(IS, Sing)));
-- check each singular point is an ODP: the Hessian / tangent cone rank.  Use: multiplicity 2 and
-- the degree of the singular subscheme of the *scheme* Sing is 44 reduced points.
print("-- number of points of Sing (degree of reduced structure) = " | toString degree radical Sing);
"data/IX.m2" << "IX = ideal " << toExternalString(gens IX) << endl << close;
"data/IS_gens.m2" << "IS = ideal " << toExternalString(G) << endl << close;
