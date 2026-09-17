-- Step 1: the doubly projected degree-8 del Pezzo  ~~D_8 = P1 x P1  in P6.
-- D_8 = P1 x P1 anticanonically embedded by O(2,2) in P8 (9 sections).
-- Project from a general line: keep 7 general linear combinations of the 9 sections.
-- Outputs: Betti table of I_S, number of quadric/cubic generators, h^1(I_S(k)).
kk = ZZ/32003;
setRandomSeed 20260911;
A = kk[s,t,u,v];
mons = matrix{{s^2*u^2, s^2*u*v, s^2*v^2, s*t*u^2, s*t*u*v, s*t*v^2, t^2*u^2, t^2*u*v, t^2*v^2}};
Mproj = random(kk^7, kk^9);          -- general projection P8 --> P6
gs = mons * transpose Mproj;         -- 1 x 7 matrix of bidegree-(2,2) forms
P6 = kk[x_0..x_6];
phi = map(A, P6, gs);
IS = ker phi;
print("-- generators degrees of I_S: " | toString(flatten degrees source gens IS));
print("-- codim I_S = " | toString codim IS | ", dim Proj = " | toString(dim IS - 1) | ", degree = " | toString degree IS);
bS = betti res IS;
print "-- Betti table of I_S (res of the module S/I_S):";
print bS;
print("-- minimal generators in degree 2 (from the Betti table) = " | toString(#select(flatten degrees source gens IS, d -> d == 2)));
print("-- minimal generators in degree 3 (from the Betti table) = " | toString(#select(flatten degrees source gens IS, d -> d == 3)));
-- h^1(I_S(k)) : compare Hilbert function of P6/I_S with h^0(O_D(2k,2k)) = (2k+1)^2
RS = P6/IS;
for k from 0 to 4 do (
  hf = hilbertFunction(k, RS);
  print("-- k = " | toString k | " : dim (P6/I_S)_k = " | toString hf | " , h^0(O_D(2k,2k)) = " | toString((2*k+1)^2) | " , deficiency = " | toString((2*k+1)^2 - hf));
);
print("-- delta = sum over k >= 0 of h^1(I_S(k)) = " | toString(sum for k from 0 to 8 list ((2*k+1)^2 - hilbertFunction(k, RS))));
-- the shipped data/IS.m2 and data/Mproj.m2 were produced by scripts/k10_build.m2 with the
-- same seed; this script writes them in the same, loadable, format (see REPRODUCE.md).
"data/IS_rebuilt.m2"    << "IS = ideal " << toString first entries gens IS << ";" << endl << close;
"data/Mproj_rebuilt.m2" << "Mproj = matrix " << toExternalString entries Mproj << endl << close;
