-- Independent exact verification of the 109 = 56 + 53 split.
needsPackage "VersalDeformations";
S=QQ[a,b,c,d,e,f,g,h];
I=ideal(a*b*f,a*b*g,a*b*h,a*c*g,a*c*h,a*d*h,
        b*d*f,b*d*g,b*e*g,c*d*e,c*e*g,c*e*h,
        c*f*h,d*e*f,d*f*h,e*f*g);
F0=gens I;
Tall=normalMatrix({0},F0);
assert((numRows Tall,numColumns Tall)==(16,109));
J=jacobian I;
variableList=flatten entries vars S;
coordinateColumns=flatten apply(0..7,i->apply(variableList,x->x*transpose J^{i}));
Coord=fold(coordinateColumns,(u,v)->u|v);
R=S/I;
X=sub(Coord,R) // sub(Tall,R);
coordinateIndices=select(toList(0..108),i->any(toList(0..63),j->X_(i,j)!=0));
intrinsicIndices=select(toList(0..108),i->not member(i,coordinateIndices));
expected=flatten {toList(1..10),toList(18..27),toList(35..39),
                  toList(47..51),toList(66..70),toList(92..109)};
assert(#coordinateIndices==56);
assert(#intrinsicIndices==53);
assert(apply(intrinsicIndices,i->i+1)==expected);
print "CHECK|intrinsic_split_recomputed|true";
print concatenate("SPLIT|coordinate_columns|",
       replace(" ","",toString apply(coordinateIndices,i->i+1)));
print concatenate("SPLIT|intrinsic_columns|",
       replace(" ","",toString expected));
exit 0;
