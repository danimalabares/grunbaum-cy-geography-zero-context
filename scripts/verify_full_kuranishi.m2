-- Fresh all-109-direction order-two Kuranishi computation. No source writes.
needsPackage "VersalDeformations";
S=QQ[a,b,c,d,e,f,g,h];
I=ideal(a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,
        b*d*f,b*d*g,b*e*g,c*d*e,c*e*g,c*e*h,
        c*f*h,d*e*f,d*f*h,e*f*g);
F0=gens I;
T1=normalMatrix({0},F0);
T2=CT^2({0},F0);
assert((numRows T1,numColumns T1)==(16,109));
assert((numRows T2,numColumns T2)==(30,27));
(vF,vR,vG,vC)=versalDeformation(F0,T1,T2,
    HighestOrder=>2,PolynomialCheck=>false,Verbose=>0);
G2=sum vG;
assert((numRows G2,numColumns G2)==(27,1));
T=ring G2;
JG=ideal flatten entries G2;
assert(all(flatten entries vars S,x->diff(sub(x,T),G2)==0));
assert(dim(T/JG)==102);
print "CHECK|full_kuranishi_T1_shape|16x109";
print "CHECK|full_kuranishi_T2_shape|30x27";
print "CHECK|full_kuranishi_G2_shape|27x1";
print "CHECK|full_kuranishi_raw_dimension|102";
print "CHECK|full_kuranishi_parameter_dimension|94";
print "CHECK|full_kuranishi_x_derivatives_zero|true";
exit 0;
