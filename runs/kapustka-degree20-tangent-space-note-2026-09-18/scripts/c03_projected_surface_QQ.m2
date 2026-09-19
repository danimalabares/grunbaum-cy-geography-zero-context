-- c03: the doubly projected del Pezzo  S = ~~D_8 in P^6, exactly over QQ.
-- Small random integer projection matrix (seed fixed); the numbers below are those of a general projection.
setRandomSeed 20260918;
A = QQ[s,t,u,v];
mons = matrix{{s^2*u^2, s^2*u*v, s^2*v^2, s*t*u^2, s*t*u*v, s*t*v^2, t^2*u^2, t^2*u*v, t^2*v^2}};
Mproj = matrix apply(7, i -> apply(9, j -> random(-9, 9)));
stderr << "projection matrix (rows = the 7 retained linear combinations of the 9 sections of O(2,2)):" << endl << toString entries Mproj << endl;
stderr << "rank of the projection matrix = " << rank Mproj << endl;
gs = mons * transpose sub(Mproj, A);
P6 = QQ[x_0..x_6];
IS = ker map(A, P6, gs);
stderr << "I_S: codim " << codim IS << ", dim Proj = " << (dim IS - 1) << ", degree " << degree IS << endl;
stderr << "generator degrees of I_S: " << toString sort flatten degrees source gens IS << endl;
stderr << "Betti table:" << endl << betti res IS << endl;
RS = P6/IS;
for k from 0 to 4 do stderr << "k = " << k << ": dim (P6/I_S)_k = " << hilbertFunction(k, RS) << ", h^0(O_D(2k,2k)) = " << (2*k+1)^2 << ", deficiency h^1(I_S(k)) = " << ((2*k+1)^2 - hilbertFunction(k, RS)) << endl;
-- the affine cone over S in A^7: tangent space at the vertex is all of A^7 (no linear forms in I_S), and it is NOT normal:
stderr << "linear forms in I_S: " << #select(flatten entries gens IS, p -> first degree p == 1) << "  => dim T_0 (cone over S) = 7" << endl;
-- (A Jacobian-criterion smoothness check of S was started and abandoned after several minutes of saturation;
--  S is isomorphic to P^1 x P^1 because a general line of P^8 misses the 5-dimensional secant variety of D_8.)
-- The ideal of the affine cone over S is generated in degrees 2 and 3, but the normalisation, the cone over D_8, needs 9 coordinates: delta = 2.
