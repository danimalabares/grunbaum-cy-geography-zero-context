-- Induced action of the automorphism group of a link on T^1_0 and T^2_0 of its Stanley--Reisner ring,
-- and the dimensions of the invariant subspaces.  Method copied from
-- runs/cp2-nine-vertex-equivariant-t2-2026-09-09/scripts/equivariant_t2.m2 (exact arithmetic over QQ).
-- Usage: M2 --script scripts/link_equivariant.m2 <facet file> <group file> <label>
needsPackage "VersalDeformations";
args = commandLine; facetfile = args#(#args-3); groupfile = args#(#args-2); label = args#(#args-1);
ls = select(lines get facetfile, s -> #s > 0 and (first s) != "#");
facets = apply(ls, s -> apply(separate(",", s), value));
verts = sort unique flatten facets; n = #verts;
S = QQ[x_1..x_n];
idx = hashTable apply(n, i -> verts#i => i);
faces = set flatten apply(facets, F -> subsets F);
isface = s -> member(s, faces);
mnf = flatten apply(toList(1..n), k -> select(subsets(verts, k), s -> not isface s and all(subsets(s, k-1), t -> isface t)));
I = ideal apply(mnf, s -> product apply(s, v -> S_(idx#v)));
F0 = gens I; m = numColumns F0; A = S/I;
R = gens ker F0; l = numColumns R;
kos = koszul(2, F0);
M2mod = Hom((image R/image kos), A)/(image substitute(transpose R, A));
T2 = lift(ambient basis(0, M2mod), S);
T1 = normalMatrix({0}, F0);
d2 = numColumns T2; d1 = numColumns T1;
stdio << "CHECK|" << label << "|generators|" << m << "|relations|" << l << "|dimT1_0|" << d1 << "|dimT2_0|" << d2 << endl;
Z = syz R; K = kos // R; assert(R*K == kos);
assert(sub(transpose T2 * Z, A) == 0); assert(sub(transpose T2 * K, A) == 0);
N = image map(A^l, A^m, sub(transpose R, A));
nf = X -> lift((map(A^l, A^(numColumns X), sub(X, A))) % N, S);
T2nf = nf T2;
allMonos = (X) -> unique flatten apply(numRows X, k -> flatten entries (coefficients(X^{k}))_0);
stackRows = (X, monos) -> matrix{{fold((a,b) -> a||b, apply(numRows X, k -> lift((coefficients(X^{k}, Monomials => monos))_1, QQ)))}};
monos2 = allMonos T2nf; Tc2 = stackRows(T2nf, monos2); assert(rank Tc2 == d2);
T1nf = lift((map(A^m, A^d1, sub(T1, A))) % (image map(A^m, A^0, 0)), S);
monos1 = allMonos T1nf; Tc1 = stackRows(T1nf, monos1); assert(rank Tc1 == d1);
perms = apply(select(lines get groupfile, s -> #s > 0 and (first s) != "#"), s -> apply(separate(" ", s), value));
stdio << "group_elements " << #perms << endl;
gensList = flatten entries F0;
permMap = g -> map(S, S, apply(n, i -> S_(g#i - 1)));
genPerm = g -> apply(gensList, mm -> position(gensList, mmm -> mmm == (permMap g) mm));
permMatrix = pi -> matrix apply(m, i -> apply(m, j -> if pi#j == i then 1_S else 0_S));
inverse2 = g -> apply(n, i -> position(g, v -> v == i+1) + 1);
sum2 = 0; sum1 = 0;
mats2 = {}; mats1 = {};
for gi from 0 to #perms-1 do (
    g = perms#gi; h = inverse2 g;
    phig = permMap g; phih = permMap h;
    pig = genPerm g; pih = genPerm h;
    assert(all(pig, v -> v =!= null));
    Pg = permMatrix pig; Ph = permMatrix pih;
    Rh = map(target R, S^(numColumns R), Ph * phih(R));
    Ch = Rh // R; assert(R*Ch - Rh == 0);
    gT2 = map(S^l, S^d2, transpose(phig(Ch)) * phig(T2));
    gT2nf = nf gT2;
    monosAll = unique(monos2 | allMonos gT2nf);
    Ta = stackRows(T2nf, monosAll); Pa = stackRows(gT2nf, monosAll);
    Mg2 = Pa // Ta; assert(Ta*Mg2 - Pa == 0);
    gT1 = map(S^m, S^d1, Pg * phig(T1));
    gT1nf = lift((map(A^m, A^d1, sub(gT1, A))) % (image map(A^m, A^0, 0)), S);
    monosAll1 = unique(monos1 | allMonos gT1nf);
    Ta1 = stackRows(T1nf, monosAll1); Pa1 = stackRows(gT1nf, monosAll1);
    Mg1 = Pa1 // Ta1; assert(Ta1*Mg1 - Pa1 == 0);
    mats2 = append(mats2, Mg2); mats1 = append(mats1, Mg1);
);
-- invariant subspace dimension = rank of the averaging projector
P2 = (1/#perms) * sum mats2; P1 = (1/#perms) * sum mats1;
assert(P2*P2 == P2); assert(P1*P1 == P1);
stdio << "CHECK|" << label << "|group_order|" << #perms << "|invariant_T1_0|" << rank P1 << "|invariant_T2_0|" << rank P2 << endl;
-- coordinate orbit inside T1_0 and its invariant part (gl_n orbital sums)
red = X -> lift((map(A^m, A^(numColumns X), sub(X, A))) % (image map(A^m, A^0, 0)), S);
der = (i,j) -> transpose matrix{apply(gensList, mm -> S_j * diff(S_i, mm))};
allD = matrix{{fold((a,b) -> a|b, flatten apply(n, i -> apply(n, j -> der(i,j))))}};
Dnf = red allD; monosD = unique(monos1 | allMonos Dnf);
TaD = stackRows(T1nf, monosD); PaD = stackRows(Dnf, monosD);
cD = PaD // TaD; assert(TaD*cD - PaD == 0);
-- invariant coordinate directions: image of (gl_n)^G, spanned by orbital sums of x_j d/dx_i
prs = flatten apply(n, i -> apply(n, j -> (i,j)));
orbitOf = p -> unique apply(perms, g -> (g#(p#0) - 1, g#(p#1) - 1));
seen = set {}; orbs = {};
for p in prs do if not member(p, seen) then (o := orbitOf p; orbs = append(orbs, o); seen = seen + set o);
orbD = matrix{{fold((a,b) -> a|b, apply(orbs, O -> sum apply(O, p -> der(p#0, p#1))))}};
orbDnf = red orbD; monosO = unique(monos1 | allMonos orbDnf);
TaO = stackRows(T1nf, monosO); PaO = stackRows(orbDnf, monosO);
cO = PaO // TaO; assert(TaO*cO - PaO == 0);
stdio << "CHECK|" << label << "|coordinate_orbit|" << rank cD << "|invariant_coordinate_directions|" << rank cO << "|genuine_invariant_T1|" << rank P1 - rank cO << endl;
stdio << "DONE " << label << endl;
exit 0;
