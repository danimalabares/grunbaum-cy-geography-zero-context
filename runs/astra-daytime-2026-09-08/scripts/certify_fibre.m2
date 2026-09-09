-- OVERNIGHT, conditional on finite equations with separate family provenance.
-- Positive results from subsets of true 4x4 Jacobian minors certify
-- smoothness. A failure of the selected subsets is expressly inconclusive.
inputPath=getenv "GS_FIBRE_INPUT";
if inputPath===null then error "Set GS_FIBRE_INPUT to finite equations, not a jet";
load inputPath;
assert(numgens S==8 and ring I===S and isHomogeneous I);
assert(codim I==4 and degree I==20);
assert(apply(toList(0..5),m->hilbertFunction(m,S/I))=={1,8,36,104,232,440});
assert(saturate I==I);
print "FINITE_FIBRE_HILBERT_SANITY_OK";
print betti res I;
F=gens I;
assert(numColumns F==16);
Jac=jacobian F;
irrelevant=ideal gens S;
Ksing=I;
passed=false;
scan(0..7,k->if not passed then (
    -- Reproducible linear combinations; their minors belong to the full
    -- Jacobian-minor ideal by Cauchy-Binet. No false positive is possible.
    C:=if k<4 then matrix apply(0..15,i->apply(0..3,j->sub(if i==4*k+j then 1 else 0,S)))
       else matrix apply(0..15,i->apply(0..3,j->sub((i+1)^(j+1)+(k-3)*(i+1)^(4-j),S)));
    Ksing=Ksing+minors(4,Jac*C);
    print ("SMOOTHNESS_SUBSET",k+1,numgens Ksing);
    passed=(saturate(Ksing,irrelevant)==ideal(1_S));
));
if not passed then (
    print "OPEN_SELECTED_MINORS_INCONCLUSIVE_NOT_A_SINGULARITY_CERTIFICATE";
    exit 2;
);
print "COMPUTER_CERTIFIED_PROJECTIVELY_SMOOTH_FINITE_FIBRE";
print "FAMILY_FLATNESS_AND_LINEAGE_REQUIRE_THE_SEPARATE_CERTIFICATE";
exit 0;
