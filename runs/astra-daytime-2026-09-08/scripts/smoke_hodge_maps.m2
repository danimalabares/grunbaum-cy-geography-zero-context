-- Tiny API smoke test only. This is NOT a Hodge calculation for the CY.
S=QQ[x,y];
C=res(module ideal(x^2,y^2),LengthLimit=>5);
complete C.dd;
W=S^{-2};
pieces=apply(toList(0..5),i->Hom(C_i,W));
bases=apply(pieces,M->basis(0,M));
scan(toList(1..5),i->(
    raw:=Hom(C.dd_i,W)*(bases#(i-1));
    coords:=raw//(bases#i);
    assert((bases#i)*coords==raw);
    print (i,numRows coords,numColumns coords,rank sub(coords,QQ));
));
print "HODGE_DEGREE_ZERO_MAP_API_OK";
exit 0;
