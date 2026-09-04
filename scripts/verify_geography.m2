-- Exact source-independent computations on the frozen Stanley--Reisner ideal.
S=QQ[a,b,c,d,e,f,g,h];
I=ideal(a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,
        b*d*f,b*d*g,b*e*g,c*d*e,c*e*g,c*e*h,
        c*f*h,d*e*f,d*f*h,e*f*g);
R=S/I;
assert(dim R==4);
assert(degree R==20);
Rmod=coker gens I;
C=res Rmod;
assert(apply(toList(0..4),i->rank C_i)=={1,16,30,16,1});
HS=reduceHilbert hilbertSeries R;
HP=hilbertPolynomial R;
assert(hilbertFunction(0,R)==1);
assert(hilbertFunction(1,R)==8);

needsPackage "VersalDeformations";
F0=gens I;
T1=normalMatrix({0},F0);
T2=CT^2({0},F0);
assert((numRows T1,numColumns T1)==(16,109));
assert((numRows T2,numColumns T2)==(30,27));

Q=QQ[t1,t2,t3,t4,t18,t20,t21,t22,t23,t24,t26,t27,t35,t36,t37,t39,
     t47,t48,t50,t51,t66,t67,t69,t70,t92,t95,t96,t97,t99,t100,t102,
     t104,t105,t106,t108,t109];
JQ=ideal(
 -t96*t102+t99*t105,t18*t99-t1*t102,t20*t99-t4*t102,
 t97*t100-t92*t108,-t69*t92+t26*t100,-t70*t92+t27*t100,
 -t36*t95+t47*t109,-t37*t95+t48*t109,-t95*t104+t106*t109,
 -t2*t36+t23*t47,-t3*t36-t2*t37+t24*t47+t23*t48,
 -t3*t37+t24*t48-t2*t104+t23*t106,t27*t51-t22*t70,
 -t3*t104+t24*t106,-t50*t97+t21*t108,
 -t26*t50+t21*t69-t51*t97+t22*t108,
 -t27*t50-t26*t51+t22*t69+t21*t70,-t4*t39+t20*t67,
 -t35*t96+t66*t105,-t1*t35+t18*t66-t39*t96+t67*t105,
 -t4*t35-t1*t39+t20*t66+t18*t67,-t23*t95+t2*t109,
 -t24*t95+t3*t109,-t50*t92+t21*t100,-t51*t92+t22*t100,
 -t35*t99+t66*t102,-t39*t99+t67*t102);
assert(dim(Q/JQ)==21);

print "CHECK|dimension_projective_scheme|3";
print "CHECK|degree|20";
print "CHECK|resolution|1,16,30,16,1;shifts=0,3,4,5,8";
print concatenate("CHECK|hilbert_series|",toExternalString HS);
print concatenate("CHECK|hilbert_polynomial|",toExternalString HP);
print "CHECK|h0_O|1";
print "CHECK|h0_H|8";
print "CHECK|embedded_tangent_dimension|109";
print "CHECK|complete_obstruction_dimension|27";
print "CHECK|quadratic_cone_in_36_variables_dimension|21";
print "CHECK|quadratic_upper_bound_full_embedded|94";
exit 0;
