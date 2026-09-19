-- c04: sanity checks over F_32003 on the ideals shipped by the 2026-09-11 run (NOT a characteristic-zero argument).
-- Ybar in P(1^8,2^2), chart w = 1 (w has weight 1, so the chart is A^9 with coordinates x_0..x_6, y_1, y_2):
kk = ZZ/32003;
Pw = kk[x_0..x_6, w, y_1, y_2, Degrees => {1,1,1,1,1,1,1,1,2,2}];
load "../../kapustka-degree20-comparison-2026-09-11/data/IYbar.m2";
A9 = kk[x_0..x_6, y_1, y_2];
IBc = sub(sub(IB, {w => 1}), A9);
stderr << "Ybar chart w=1: dim = " << dim IBc << ", ideal generators = " << numgens IBc << endl;
Jac0 = sub(jacobian IBc, apply(gens A9, v -> v => 0));
stderr << "Ybar chart w=1: origin lies on Ybar ? " << (sub(gens IBc, apply(gens A9, v -> v => 0)) == 0) << endl;
stderr << "Ybar chart w=1: rank of Jacobian at the origin = " << rank Jac0 << "  => dim T_P Ybar = " << (9 - rank Jac0) << endl;
-- multiplicity at P: degree of the tangent cone (leading forms)
-- the tangent cone needs a standard basis; use the built-in:
stderr << "Ybar chart w=1: tangent cone computation ..." << endl;
tc = tangentCone IBc;
stderr << "Ybar chart w=1: tangent cone: dim " << dim tc << ", degree (= multiplicity of Ybar at P) = " << degree tc << ", generator degrees " << toString sort flatten degrees source gens tc << endl;
-- Y in P^7, chart w = 1 (A^7):
P7 = kk[x_0..x_6, w];
load "../../kapustka-degree20-comparison-2026-09-11/data/IY.m2";
A7 = kk[x_0..x_6];
IYc = sub(sub(IY, {w => 1}), A7);
Jac7 = sub(jacobian IYc, apply(gens A7, v -> v => 0));
stderr << "Y chart w=1: origin lies on Y ? " << (sub(gens IYc, apply(gens A7, v -> v => 0)) == 0) << ", rank of Jacobian at origin = " << rank Jac7 << " => dim T_P Y = " << (7 - rank Jac7) << endl;
tcY = tangentCone IYc;
stderr << "Y chart w=1: tangent cone: dim " << dim tcY << ", degree (= multiplicity of Y at P) = " << degree tcY << ", generator degrees " << toString sort flatten degrees source gens tcY << endl;
-- Hilbert polynomials (projective) of Y and of SR(M) differ by 2:
RY = P7/IY;
stderr << "Y in P^7: Hilbert polynomial = " << toString hilbertPolynomial(RY, Projective => false) << endl;
