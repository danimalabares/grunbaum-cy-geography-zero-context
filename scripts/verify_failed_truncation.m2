-- Preserve the decisive negative control without modifying the source packet.
needsPackage "VersalDeformations";
sourceRoot=getenv "GS_ZERO_CONTEXT_SOURCE";
if sourceRoot === "" then sourceRoot="../grunbaum-zero-context-proof";
U=ZZ/101[q,X1,X2,X3,X4,X5,X6,X7,X8];
familyMatrix=value get concatenate(sourceRoot,"/certificates/failed_truncated_order4_family_matrix.txt");
V=ZZ/101[y1,y2,y3,y4,y5,y6,y7,y8];
sp1=map(V,U,{1,y1,y2,y3,y4,y5,y6,y7,y8});
J1=trim ideal sp1 familyMatrix;
assert(dim(V/J1)==0);
assert(degree J1==567);
print "FAILED_CONTROL|q1_affine_dimension|0";
print "FAILED_CONTROL|q1_degree|567";
print "FAILED_CONTROL|interpretation|nonflat_not_a_smoothing";
exit 0;
