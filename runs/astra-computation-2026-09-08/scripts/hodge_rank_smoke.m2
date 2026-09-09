-- Tiny exact syntax/arithmetic check for the optimized degree-zero
-- dual-resolution calculation. This is not a GS fibre or a Hodge claim.
-- The complete intersection (a²,b²,c²,d²) is nonreduced; its square has
-- the standard regular-sequence square resolution
-- 10S(-4) <- 20S(-6) <- 15S(-8) <- 4S(-10).
-- Consequently Ext3(I²,S(-8))_0 has dimension144-15=129 and Ext4=0.
-- Run only in the root agent's sole CAS slot. Expected seconds, <200MB.
S=QQ[a,b,c,d,e,f,g,h];
J=ideal(a^2,b^2,c^2,d^2);
C=res(module(J^2),LengthLimit=>5);
complete C.dd;
W=S^{-8};
V=apply(toList(0..5),i->Hom(C_i,W));
B=apply(V,M->basis(0,M));
dims=apply(B,Q->numColumns Q);
rs=apply(toList(3..5),i->(
    D:=Hom(C.dd_i,W);
    raw:=D*B#(i-1);
    coords:=raw//B#i;
    assert(B#i*coords==raw);
    rank sub(coords,QQ)));
assert(dims#3-rs#0-rs#1==129);
assert(dims#4-rs#1-rs#2==0);
print("HODGE_DEGREE_ZERO_RANK_SMOKE_OK",dims,rs);
exit 0;
