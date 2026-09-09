-- Induced action of a permutation group on T^1_0 and T^2_0 of A = QQ[x_1..x_9]/I_Delta,
-- Delta = 9-vertex triangulation of CP^2.  Exact arithmetic over QQ.
-- Usage: M2 --script scripts/equivariant_t2.m2 <groupfile.txt> <outprefix>
-- groupfile: one permutation per line as 9 space-separated images g(1) ... g(9).
-- Method (no quadratic obstruction equations are used):
--   * R = gens ker F0 (36 x 90 relation matrix), kos = koszul(2,F0),
--     M2 := Hom(image R/image kos, A)/image(R^T)  (this is Schlessinger's T^2, degree 0 part taken),
--     T2 := representatives of a basis of (M2)_0 in the ambient A^90 (same construction as CT^2).
--   * For g in G with h=g^{-1}: P_h permutes generators, C_h solves R*C_h = P_h*h(R);
--     (g.phi)(r_k) = g(phi(h.r_k)), so g.T2 = (g(C_h))^T * g(T2).
--   * Normal forms modulo image(R^T over A) are compared coefficientwise -> matrix Mg over QQ.
--   * T1 = normalMatrix({0},F0) in A^36; g.T1 = P_g * g(T1); coordinates solved exactly.
needsPackage "VersalDeformations";
args = commandLine;
groupfile = args#(#args-2); outprefix = args#(#args-1);
S=QQ[x_1..x_9];
I=ideal(x_1*x_2*x_3*x_4,x_1*x_2*x_3*x_5,x_1*x_2*x_3*x_6,x_1*x_2*x_4*x_8,x_1*x_2*x_5*x_7,x_1*x_2*x_6*x_9,x_1*x_3*x_4*x_9,x_1*x_3*x_5*x_8,x_1*x_3*x_6*x_7,x_1*x_4*x_5*x_8,x_1*x_4*x_6*x_9,x_1*x_4*x_8*x_9,x_1*x_5*x_6*x_7,x_1*x_5*x_7*x_8,x_1*x_6*x_7*x_9,x_1*x_7*x_8*x_9,x_2*x_3*x_4*x_7,x_2*x_3*x_5*x_9,x_2*x_3*x_6*x_8,x_2*x_4*x_5*x_7,x_2*x_4*x_6*x_8,x_2*x_4*x_7*x_8,x_2*x_5*x_6*x_9,x_2*x_5*x_7*x_9,x_2*x_6*x_8*x_9,x_2*x_7*x_8*x_9,x_3*x_4*x_5*x_9,x_3*x_4*x_6*x_7,x_3*x_4*x_7*x_9,x_3*x_5*x_6*x_8,x_3*x_5*x_8*x_9,x_3*x_6*x_7*x_8,x_3*x_7*x_8*x_9,x_4*x_5*x_6*x_7,x_4*x_5*x_6*x_8,x_4*x_5*x_6*x_9);
F0=gens I; n=numColumns F0; assert(n==36);
A=S/I;
R=gens ker F0; l=numColumns R;
kos=koszul(2,F0);
M2mod = Hom((image R/image kos),A)/(image substitute(transpose R,A));
T2 = lift(ambient basis(0,M2mod),S);
T1 = normalMatrix({0},F0);
d2=numColumns T2; d1=numColumns T1;
stdio<<"relations "<<l<<"  dimT1_0 "<<d1<<"  dimT2_0 "<<d2<<endl;
assert(numRows T2==l); assert(numRows T1==n);
-- sanity: T2 columns are genuine homomorphisms on R/kos (vanish on 2nd syzygies and Koszul relations)
Z=syz R; K=kos//R; assert(R*K==kos);
assert(sub(transpose T2 * Z,A)==0);
assert(sub(transpose T2 * K,A)==0);
stdio<<"T2_columns_are_homomorphisms true"<<endl;
-- normal forms modulo trivial homomorphisms N = image(R^T) in A^l
N = image map(A^l,A^n,sub(transpose R,A));
nf = X -> lift((map(A^l,A^(numColumns X),sub(X,A))) % N, S);
T2nf = nf T2;
-- coefficient extraction: rows = (relation index, monomial); columns = columns of X
allMonos = (X) -> unique flatten apply(numRows X, k-> flatten entries (coefficients(X^{k}))_0);
coefMat = (X,monos) -> (
    matrix apply(numRows X, k -> (
        c := (coefficients(X^{k}, Monomials=>monos))_1;
        entries lift(c,QQ)))
    );
stackRows = (X,monos) -> matrix{{fold((a,b)->a||b, apply(numRows X, k -> lift((coefficients(X^{k},Monomials=>monos))_1,QQ)))}};
monos2 = allMonos T2nf;
Tc2 = stackRows(T2nf,monos2);
assert(rank Tc2 == d2);
stdio<<"T2_normal_forms_independent_rank "<<rank Tc2<<endl;
T1nf = lift((map(A^n,A^d1,sub(T1,A))) % (image map(A^n,A^0,0)),S);
monos1 = allMonos T1nf;
Tc1 = stackRows(T1nf,monos1);
assert(rank Tc1 == d1);
stdio<<"T1_independent_rank "<<rank Tc1<<endl;
-- group elements
perms = apply(select(lines get groupfile, s->#s>0 and (first s)!="#"), s->apply(separate(" ",s),value));
stdio<<"group_elements "<<#perms<<endl;
gensList = flatten entries F0;
permMap = g -> map(S,S,apply(9,i->S_(g#i-1)));    -- x_(i+1) |-> x_(g(i+1)) (S_j is the j-th variable, 0-indexed)
genPerm = g -> apply(gensList, m -> position(gensList, mm -> mm == (permMap g) m));
permMatrix = pi -> matrix apply(n,i->apply(n,j-> if pi#j==i then 1_S else 0_S)); -- (P)_{pi(j),j}=1
inverse2 = g -> apply(9, i -> position(g, v -> v==i+1)+1);
compose2 = (g,h) -> apply(9, i -> g#(h#i-1));   -- (g*h)(i)=g(h(i))
out = new MutableHashTable;
mats2 = {}; mats1 = {};
for gi from 0 to #perms-1 do (
    g = perms#gi; h = inverse2 g;
    phig = permMap g; phih = permMap h;
    pig = genPerm g; pih = genPerm h;
    assert(all(pig, v-> v =!= null));
    Pg = permMatrix pig; Ph = permMatrix pih;
    -- transport of relations
    Rh = map(target R, S^(numColumns R), Ph * phih(R));
    Ch = Rh // R; assert(R*Ch - Rh == 0);
    gT2 = map(S^l, S^d2, transpose(phig(Ch)) * phig(T2));
    gT2nf = nf gT2;
    monosAll = unique(monos2 | allMonos gT2nf);
    Ta = stackRows(T2nf,monosAll); Pa = stackRows(gT2nf,monosAll);
    Mg2 = Pa // Ta; assert(Ta*Mg2 - Pa == 0);
    -- T1 action
    gT1 = map(S^n, S^d1, Pg * phig(T1));
    gT1nf = lift((map(A^n,A^d1,sub(gT1,A))) % (image map(A^n,A^0,0)),S);
    monosAll1 = unique(monos1 | allMonos gT1nf);
    Ta1 = stackRows(T1nf,monosAll1); Pa1 = stackRows(gT1nf,monosAll1);
    Mg1 = Pa1 // Ta1; assert(Ta1*Mg1 - Pa1 == 0);
    mats2 = append(mats2, Mg2); mats1 = append(mats1, Mg1);
    stdio<<"element "<<gi<<" perm "<<toString g<<" traceT2 "<<trace Mg2<<" traceT1 "<<trace Mg1<<" entriesT2 "<<toString sort unique flatten entries Mg2<<endl;
    );
-- representation property (Mgh = Mg*Mh) on all pairs, only when the listed set is closed under composition
idx = g -> position(perms, p -> p==g);
closed = all(#perms, i-> all(#perms, j-> idx compose2(perms#i,perms#j) =!= null));
stdio<<"group_file_closed_under_composition "<<closed<<endl;
repOK2 = "not_checked_generators_only"; repOK1 = "not_checked_generators_only"; inv1 = "see_python_closure"; inv2 = "see_python_closure";
if closed then (
    repOK2 = all(#perms, i-> all(#perms, j-> mats2#(idx compose2(perms#i,perms#j)) == mats2#i * mats2#j));
    repOK1 = all(#perms, i-> all(#perms, j-> mats1#(idx compose2(perms#i,perms#j)) == mats1#i * mats1#j));
    stdio<<"representation_property_T2 "<<repOK2<<"  representation_property_T1 "<<repOK1<<endl;
    Rey2 = (1/#perms) * sum mats2; Rey1 = (1/#perms) * sum mats1;
    assert(Rey2*Rey2 == Rey2); assert(Rey1*Rey1 == Rey1);
    inv2 = rank Rey2; inv1 = rank Rey1;
    stdio<<"CHECK|dimT1_0|"<<d1<<endl;
    stdio<<"CHECK|dimT2_0|"<<d2<<endl;
    stdio<<"CHECK|group_order|"<<#perms<<endl;
    stdio<<"CHECK|dim_T1_0_invariants|"<<inv1<<endl;
    stdio<<"CHECK|dim_T2_0_invariants|"<<inv2<<endl;
    stdio<<"CHECK|trace_Reynolds_T2|"<<trace Rey2<<"  trace_Reynolds_T1 "<<trace Rey1<<endl;
    ) else (
    stdio<<"CHECK|dimT1_0|"<<d1<<endl;
    stdio<<"CHECK|dimT2_0|"<<d2<<endl;
    stdio<<"generators_only: invariants and representation property are established by scripts/verify_certificate.py after closure"<<endl;
    );
-- write certificate
fmt = M -> toString apply(entries M, r -> apply(r, e -> toString e));
f = openOut(outprefix|"_certificate.json");
f << "{\n \"group_file\": \"" << groupfile << "\",\n";
f << " \"dimT1_0\": " << d1 << ", \"dimT2_0\": " << d2 << ", \"relations\": " << l << ",\n";
f << " \"dim_T1_0_invariants\": \"" << toString inv1 << "\", \"dim_T2_0_invariants\": \"" << toString inv2 << "\",\n";
f << " \"representation_property_T2\": \"" << toString repOK2 << "\", \"representation_property_T1\": \"" << toString repOK1 << "\",\n";
f << " \"elements\": [\n";
for gi from 0 to #perms-1 do (
    f << "  {\"perm\": " << replace("\\}","]",replace("\\{","[",toString perms#gi)) << ", \"generator_perm\": " << replace("\\}","]",replace("\\{","[",toString genPerm perms#gi))
      << ", \"traceT2\": \"" << toString trace mats2#gi << "\", \"traceT1\": \"" << toString trace mats1#gi
      << "\",\n   \"M_T2\": " << replace("\\}","]",replace("\\{","[",fmt mats2#gi))
      << ",\n   \"M_T1\": " << replace("\\}","]",replace("\\{","[",fmt mats1#gi)) << "}";
    if gi < #perms-1 then f << ",";
    f << "\n";
    );
f << " ]\n}\n";
close f;
-- also save T2/T1 basis representatives and R for auditing
g2 = openOut(outprefix|"_basis.m2.txt");
g2 << "R = " << toString R << ";\n" << "T2 = " << toString T2 << ";\n" << "T2nf = " << toString T2nf << ";\n" << "T1 = " << toString T1 << ";\n";
close g2;
stdio<<"EQUIVARIANT_T2_DONE"<<endl;
exit 0;
