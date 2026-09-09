-- Coordinate (locally trivial) directions in T^1_0 = Hom(I,A)_0 and their group-invariant part.
-- gl_9 acts by derivations D_{ij} = x_j d/dx_i; the image of gl_9 in T^1_0 is the tangent space to the
-- GL_9-orbit of the ideal ("coordinate orbit").  For a permutation group H, (image gl_9)^H = image (gl_9)^H,
-- and (gl_9)^H is spanned by the orbital sums sum_{(i,j) in O} D_{ij}.
-- Usage: M2 --script scripts/coordinate_orbit.m2 data/orbitals_<H>.txt
needsPackage "VersalDeformations";
args = commandLine; orbfile = args#(#args-1);
S=QQ[x_1..x_9];
I=ideal(x_1*x_2*x_3*x_4,x_1*x_2*x_3*x_5,x_1*x_2*x_3*x_6,x_1*x_2*x_4*x_8,x_1*x_2*x_5*x_7,x_1*x_2*x_6*x_9,x_1*x_3*x_4*x_9,x_1*x_3*x_5*x_8,x_1*x_3*x_6*x_7,x_1*x_4*x_5*x_8,x_1*x_4*x_6*x_9,x_1*x_4*x_8*x_9,x_1*x_5*x_6*x_7,x_1*x_5*x_7*x_8,x_1*x_6*x_7*x_9,x_1*x_7*x_8*x_9,x_2*x_3*x_4*x_7,x_2*x_3*x_5*x_9,x_2*x_3*x_6*x_8,x_2*x_4*x_5*x_7,x_2*x_4*x_6*x_8,x_2*x_4*x_7*x_8,x_2*x_5*x_6*x_9,x_2*x_5*x_7*x_9,x_2*x_6*x_8*x_9,x_2*x_7*x_8*x_9,x_3*x_4*x_5*x_9,x_3*x_4*x_6*x_7,x_3*x_4*x_7*x_9,x_3*x_5*x_6*x_8,x_3*x_5*x_8*x_9,x_3*x_6*x_7*x_8,x_3*x_7*x_8*x_9,x_4*x_5*x_6*x_7,x_4*x_5*x_6*x_8,x_4*x_5*x_6*x_9);
F0=gens I; n=numColumns F0; A=S/I;
T1=normalMatrix({0},F0); d1=numColumns T1;
red = X -> lift((map(A^n,A^(numColumns X),sub(X,A))) % (image map(A^n,A^0,0)),S);
allMonos = (X) -> unique flatten apply(numRows X, k-> flatten entries (coefficients(X^{k}))_0);
stackRows = (X,monos) -> matrix{{fold((a,b)->a||b, apply(numRows X, k -> lift((coefficients(X^{k},Monomials=>monos))_1,QQ)))}};
T1nf = red T1; monos1 = allMonos T1nf;
der = (i,j) -> transpose matrix{apply(flatten entries F0, m -> S_(j-1) * diff(S_(i-1), m))};  -- x_j d/dx_i applied to generators
coords = X -> ( Xnf := red X; monos := unique(monos1 | allMonos Xnf); Ta := stackRows(T1nf,monos); Pa := stackRows(Xnf,monos); c := Pa // Ta; assert(Ta*c - Pa == 0); c );
-- full coordinate orbit
allD = matrix{{fold((a,b)->a|b, flatten apply(9, i-> apply(9, j-> der(i+1,j+1))))}};
allC = coords allD;
stdio<<"CHECK|coordinate_orbit_dimension_in_T1_0|"<<rank allC<<endl;
stdio<<"CHECK|dimT1_0|"<<d1<<endl;
-- invariant part from orbital sums
orbs = apply(select(lines get orbfile, s->#s>0 and (first s)!="#"), s-> apply(separate(" ",s), t-> apply(separate(",",t), value)));
stdio<<"orbitals "<<#orbs<<endl;
orbD = matrix{{fold((a,b)->a|b, apply(orbs, O -> sum apply(O, p -> der(p#0,p#1))))}};
orbC = coords orbD;
stdio<<"CHECK|invariant_coordinate_directions_in_T1_0|"<<rank orbC<<endl;
f=openOut(replace("\\.txt$","_coordinate_orbit_coords.txt",replace("data/orbitals_","certificates/",orbfile)));
f<<"all81_coords = "<<toString allC<<";\n"<<"orbital_coords = "<<toString orbC<<";\n"; close f;
stdio<<"COORDINATE_ORBIT_DONE"<<endl;
exit 0;
