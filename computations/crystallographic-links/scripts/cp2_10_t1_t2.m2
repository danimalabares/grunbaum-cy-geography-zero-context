-- Degree-0 T^1 and T^2 of the Stanley--Reisner ring of CP^2_10 itself (a fourfold in P^9),
-- for comparison with the CP^2_9 numbers (93, 21, 126) of runs/cp2-nine-vertex-equivariant-t2-2026-09-09.
needsPackage "VersalDeformations";
args = commandLine; facetfile = args#(#args-1);
ls = select(lines get facetfile, s -> #s > 0 and (first s) != "#");
facets = apply(ls, s -> apply(separate(",", s), value));
verts = sort unique flatten facets; n = #verts;
S = QQ[x_1..x_n];
idx = hashTable apply(n, i -> verts#i => i);
faces = set flatten apply(facets, F -> subsets F);
isface = s -> member(s, faces);
mnf = flatten apply(toList(1..n), k -> select(subsets(verts, k), s -> not isface s and all(subsets(s, k-1), t -> isface t)));
I = ideal apply(mnf, s -> product apply(s, v -> S_(idx#v)));
stdio << "CP2_10: vertices " << n << " facets " << #facets << " minimal_nonfaces " << #mnf << " by_size " << toString tally apply(mnf, s -> #s) << endl;
A = S/I; F0 = gens I;
stdio << "CHECK|CP2_10|dim_A|" << dim A << "|degree|" << degree A << endl;
T1 = normalMatrix({0}, F0); d1 = numColumns T1;
stdio << "CHECK|CP2_10|dim_Hom_S(I,A)_0|" << d1 << endl;
t0 = currentTime();
T2 = CT^2({0}, F0);
stdio << "CHECK|CP2_10|dim_T2_0|" << numColumns T2 << "|seconds|" << currentTime() - t0 << endl;
stdio << "DONE CP2_10" << endl;
exit 0;
