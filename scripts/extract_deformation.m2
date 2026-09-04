-- Exact, deterministic extraction from the frozen zero-context packet.
-- This script is read-only with respect to the source repository.
needsPackage "VersalDeformations";

sourceRoot = getenv "GS_ZERO_CONTEXT_SOURCE";
if sourceRoot === "" then sourceRoot = "../grunbaum-zero-context-proof";

S = QQ[a,b,c,d,e,f,g,h];
I = ideal(a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,
          b*d*f,b*d*g,b*e*g,c*d*e,c*e*g,c*e*h,
          c*f*h,d*e*f,d*f*h,e*f*g);
F0 = gens I;
Tall = normalMatrix({0},F0);
assert((numRows Tall,numColumns Tall)==(16,109));

intrinsicOneBased = flatten {toList(1..10),toList(18..27),toList(35..39),
                              toList(47..51),toList(66..70),toList(92..109)};
assert(#intrinsicOneBased==53);
T1 = Tall_(apply(intrinsicOneBased,j->j-1));
assert((numRows T1,numColumns T1)==(16,53));

fixedOrbits = {{1,11,19,23,27,34},{2,15,16,25,30,32},
 {3,14,17,21,29,31},{4,13,20,22,26,35},{5,12,18,24,28,33},
 {6,7,10},{8,9},{36,39,43,44,46,53},{37,38,42,45,47,51},
 {40,41,48,49,50,52}};
assert(sort flatten fixedOrbits==toList(1..53));
coeff53 = toList apply(1..53,i->(
  orbitPosition := position(fixedOrbits,O->member(i,O));
  assert(orbitPosition=!=null);
  sub(orbitPosition+1,S)));
lineTangent = T1*transpose matrix{coeff53};

-- Independently rerun y |-> T1*y |-> first-order generator corrections.
T2 = CT^2({0},F0);
assert((numRows T2,numColumns T2)==(30,27));
(tmpF,tmpR,tmpG,tmpC) = versalDeformation(
  F0,lineTangent,T2,HighestOrder=>1,PolynomialCheck=>false,Verbose=>0);
assert((#tmpF,#tmpR)==(2,2));
A = ring first tmpF;
qpar = first gens A;
coeffToS = (M,d)->matrix apply(entries M,row->apply(row,e->
    sub(coefficient(qpar^d,e),S)));
recomputedG = coeffToS(tmpF#1,1);
assert(entries(transpose recomputedG)==entries lineTangent);

-- Load the packet's stored generic equivariant six-jet in the ring A just
-- reconstructed, and compare its q coefficient with the independent rerun.
use A;
storedF = value get concatenate(sourceRoot,"/deformation/generic_equivariant_state_F_order6.txt");
storedR = value get concatenate(sourceRoot,"/deformation/generic_equivariant_state_R_order6.txt");
assert(#storedF==7);
assert(#storedR==7);
assert(all(storedF,M->(numRows M,numColumns M)==(1,16)));
assert(all(storedR,M->(numRows M,numColumns M)==(16,30)));
storedCoefficient = (d)->coeffToS(storedF#d,d);
storedRelationCoefficient = (d)->coeffToS(storedR#d,d);
assert(entries(storedCoefficient 0)==entries F0);
assert(entries(storedCoefficient 1)==entries recomputedG);
assert(all(toList(0..6),n->
  sum apply(toList(0..n),d->storedCoefficient(d)*storedRelationCoefficient(n-d))==0));

print "META|format|gs-deformation-extraction-v1";
print "META|base_field|QQ";
print "META|variables|a,b,c,d,e,f,g,h";
print "META|tangent_rows|16";
print "META|tangent_columns|109";
print "META|coordinate_orbit_dimension|56";
print "META|intrinsic_dimension|53";
print "META|obstruction_dimension|27";

scan(0..15,i->print concatenate("GEN|",toString(i+1),"|",
  toExternalString(F0_(0,i))));

scan(0..108,j->scan(0..15,i->(
  e := Tall_(i,j);
  if e!=0 then print concatenate("BASIS|",toString(j+1),"|",
    toString(i+1),"|",toExternalString(e)))));

print concatenate("INTRINSIC|",replace(" ","",toString intrinsicOneBased));
scan(0..9,k->print concatenate("ORBIT|",toString(k+1),"|",
  replace(" ","",toString fixedOrbits#k)));
print concatenate("VECTOR53|",replace(" ","",toString coeff53));

scan(0..15,i->print concatenate("G1|",toString(i+1),"|",
  toExternalString(recomputedG_(0,i))));
scan(0..6,d->(
  Hd := storedCoefficient d;
  scan(0..15,i->print concatenate("JET|",toString(d),"|",
    toString(i+1),"|",toExternalString(Hd_(0,i))))));

print "CHECK|stored_q_coefficient_equals_recomputed|true";
print "CHECK|stored_generator_relation_jet_valid_through_q6|true";
print "CHECK|dimensions_and_orderings|true";
exit 0;
