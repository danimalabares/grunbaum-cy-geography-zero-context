-- Degree-0 cotangent cohomology of the Stanley--Reisner rings of the three vertex links:
--   L9   = link of a vertex of CP^2_9  (Bruckner--Gruenbaum 8-vertex sphere; baseline, expected Hom_S(I,A)_0 = 109)
--   L10a = link of x_11 in CP^2_10 (neighbourly 9-vertex sphere, 27 facets)
--   L10b = link of x_12 in CP^2_10 (9-vertex sphere, 22 facets)
-- For each: dim Hom_S(I,A)_0 (embedded first-order deformations of Proj A in P^{n-1}),
-- dim of the gl_n coordinate orbit in it, dim (T^2_A)_0 via VersalDeformations' CT^2, Hilbert data.
-- Usage: M2 --script scripts/link_t1_t2.m2 <facet file> <label>
needsPackage "VersalDeformations";
args = commandLine; facetfile = args#(#args-2); label = args#(#args-1);
ls = select(lines get facetfile, s -> #s > 0 and (first s) != "#");
facets = apply(ls, s -> apply(separate(",", s), value));
verts = sort unique flatten facets; n = #verts;
S = QQ[x_1..x_n];
idx = hashTable apply(n, i -> verts#i => i);
faces = set flatten apply(facets, F -> subsets F);
isface = s -> member(s, faces);
mnf = flatten apply(toList(1..n), k -> select(subsets(verts, k), s -> not isface s and all(subsets(s, k-1), t -> isface t)));
I = ideal apply(mnf, s -> product apply(s, v -> S_(idx#v)));
stdio << "LABEL " << label << " vertices " << n << " facets " << #facets << " minimal_nonfaces " << #mnf << " by_size " << toString tally apply(mnf, s -> #s) << endl;
A = S/I;
F0 = gens I;
stdio << "CHECK|" << label << "|dim_A|" << dim A << "|degree|" << degree A << endl;
hp = hilbertPolynomial(A, Projective => false);
stdio << "CHECK|" << label << "|hilbert_polynomial|" << toString hp << endl;
T1 = normalMatrix({0}, F0);
d1 = numColumns T1;
stdio << "CHECK|" << label << "|dim_Hom_S(I,A)_0|" << d1 << endl;
m = numColumns F0;
red = X -> lift((map(A^m, A^(numColumns X), sub(X, A))) % (image map(A^m, A^0, 0)), S);
allMonos = X -> unique flatten apply(numRows X, k -> flatten entries (coefficients(X^{k}))_0);
stackRows = (X, monos) -> matrix{{fold((a,b) -> a||b, apply(numRows X, k -> lift((coefficients(X^{k}, Monomials => monos))_1, QQ)))}};
T1nf = red T1; monos1 = allMonos T1nf;
der = (i,j) -> transpose matrix{apply(flatten entries F0, mm -> S_j * diff(S_i, mm))};
allD = matrix{{fold((a,b) -> a|b, flatten apply(n, i -> apply(n, j -> der(i,j))))}};
Dnf = red allD; monos = unique(monos1 | allMonos Dnf);
Ta = stackRows(T1nf, monos); Pa = stackRows(Dnf, monos);
c = Pa // Ta; assert(Ta*c - Pa == 0);
stdio << "CHECK|" << label << "|coordinate_orbit_dimension|" << rank c << endl;
stdio << "CHECK|" << label << "|intrinsic_T1_0_dimension|" << d1 - rank c << endl;
t0 = currentTime();
T2 = CT^2({0}, F0);
stdio << "CHECK|" << label << "|dim_T2_0|" << numColumns T2 << "|seconds|" << currentTime() - t0 << endl;
stdio << "DONE " << label << endl;
exit 0;
