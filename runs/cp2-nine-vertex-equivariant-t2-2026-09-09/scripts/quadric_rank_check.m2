-- Optional cross-check for task 3: rank of the primary obstruction map kappa_2^*: T2^* -> Sym^2(T1^*).
-- Computes the order-two Kuranishi equations (126 quadrics in 93 parameters) and the rank of their
-- coefficient matrix.  If the rank is < 126, quadratic obstruction equations alone would NOT detect
-- the whole obstruction space, and a quadric-based recovery of the G-representation would be insufficient.
-- The main computation (equivariant_t2.m2) does not depend on this file.
needsPackage "VersalDeformations";
S=QQ[x_1..x_9];
I=ideal(x_1*x_2*x_3*x_4,x_1*x_2*x_3*x_5,x_1*x_2*x_3*x_6,x_1*x_2*x_4*x_8,x_1*x_2*x_5*x_7,x_1*x_2*x_6*x_9,x_1*x_3*x_4*x_9,x_1*x_3*x_5*x_8,x_1*x_3*x_6*x_7,x_1*x_4*x_5*x_8,x_1*x_4*x_6*x_9,x_1*x_4*x_8*x_9,x_1*x_5*x_6*x_7,x_1*x_5*x_7*x_8,x_1*x_6*x_7*x_9,x_1*x_7*x_8*x_9,x_2*x_3*x_4*x_7,x_2*x_3*x_5*x_9,x_2*x_3*x_6*x_8,x_2*x_4*x_5*x_7,x_2*x_4*x_6*x_8,x_2*x_4*x_7*x_8,x_2*x_5*x_6*x_9,x_2*x_5*x_7*x_9,x_2*x_6*x_8*x_9,x_2*x_7*x_8*x_9,x_3*x_4*x_5*x_9,x_3*x_4*x_6*x_7,x_3*x_4*x_7*x_9,x_3*x_5*x_6*x_8,x_3*x_5*x_8*x_9,x_3*x_6*x_7*x_8,x_3*x_7*x_8*x_9,x_4*x_5*x_6*x_7,x_4*x_5*x_6*x_8,x_4*x_5*x_6*x_9);
F0=gens I;
T1=normalMatrix({0},F0);
T2=CT^2({0},F0);
stdio<<"T1 "<<numColumns T1<<" T2 "<<numColumns T2<<endl;
t0=currentTime();
(vF,vR,vG,vC)=versalDeformation(F0,T1,T2,HighestOrder=>2,PolynomialCheck=>false,Verbose=>0);
G2=sum vG;
stdio<<"G2_shape "<<numRows G2<<" "<<numColumns G2<<" seconds "<<currentTime()-t0<<endl;
T=ring G2;
quads=flatten entries G2;
(mons,cf)=coefficients(matrix{quads});
stdio<<"CHECK|number_of_quadrics|"<<#quads<<endl;
stdio<<"CHECK|number_of_distinct_monomials|"<<numColumns mons<<endl;
stdio<<"CHECK|rank_quadric_coefficient_matrix|"<<rank lift(cf,QQ)<<endl;
stdio<<"CHECK|all_quadrics_homogeneous_degree2|"<<all(quads, q-> q==0 or (degree q)=={2})<<endl;
f=openOut("data/quadratic_obstructions_G2.txt"); f<<toString quads<<endl; close f;
stdio<<"QUADRIC_RANK_DONE"<<endl;
exit 0;
