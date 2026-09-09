-- OVERNIGHT ONLY. Run after obtaining finite equations AND a separate
-- smoothness/flatness/component certificate for the intended fibre.
-- This script does not create that certificate and never treats a six-jet
-- polynomial truncation as an actual fibre.
--
-- Inputs:
-- GS_FIBRE_INPUT: absolute .m2 file defining a standard 8-variable
-- polynomial ring S over an exact characteristic-zero field and ideal I.
-- GS_FIBRE_CERTIFICATE: existing human-readable certificate file.
-- GS_HODGE_PHASE: normal (default) or square.
-- GS_HODGE_PREFIX: output prefix, whose parent directory already exists.
-- GS_HODGE_MODULAR_BOUND=1: allow a finite-field fibre of a separately
-- certified smooth integral model; report characteristic-zero upper bounds.
--
-- Mathematical output:
-- normal: h0(N)=dim Hom_S(I,S/I)_0, hence h21=h0(N)-63.
-- square: h11=1+Ext^4_S(I²,S(-8))_0,
--         h21=Ext^3_S(I²,S(-8))_0-64.
-- Only degree-zero dual-resolution matrices are ranked; whole Ext modules
-- are not constructed. See PICARD_HODGE_PLAN.md for the proofs.
-- Syntax inspected against installed M2 1.20 Core/ext.m2, matrix1.m2,
-- basis.m2 and res.m2. No CAS was launched by this script's author today.

inputPath = getenv "GS_FIBRE_INPUT";
certPath = getenv "GS_FIBRE_CERTIFICATE";
if inputPath === null then error "Set GS_FIBRE_INPUT to certified finite equations";
if certPath === null then error "Set GS_FIBRE_CERTIFICATE to the separate certificate";
if not fileExists inputPath then error "Missing fibre input";
if not fileExists certPath then error "Missing fibre certificate";
load inputPath;
modularBound = (getenv "GS_HODGE_MODULAR_BOUND" == "1");
assert(char S == 0 or modularBound);
assert(numgens S == 8);
assert(ring I === S);
assert(isHomogeneous I);
phaseString = getenv "GS_HODGE_PHASE";
phase = if phaseString === null then "normal" else phaseString;
prefixString = getenv "GS_HODGE_PREFIX";
prefix = if prefixString === null then "hodge_fibre" else prefixString;
log = openOut(prefix | "_" | phase | ".txt");
record = x -> (log << x << endl << flush; print x;);
record("INPUT " | inputPath);
record("CERTIFICATE " | certPath);
record("PHASE " | phase);
record("CHARACTERISTIC " | toString char S);
assert(codim I == 4);
assert(degree I == 20);
R = S/I;
-- The intended ACM neighbourhood has this Hilbert function. These checks
-- catch many wrong inputs but do not replace flatness or smoothness.
assert(apply(toList(0..5),m->hilbertFunction(m,R)) == {1,8,36,104,232,440});
record("HILBERT_SANITY_OK");

if phase == "normal" then (
    -- A presentation I <- S(-3)^16 <- S(-4)^30 gives, after Hom(-,R),
    -- a map R(3)^16 -> R(4)^30. Its kernel is Hom_S(I,R).
    -- Hom below correctly preserves every grading shift even if this
    -- input has extra minimal syzygies.
    rel := syz gens I;
    record("FIRST_SYZYGY_SIZE " | toString(numRows rel,numColumns rel));
    relR := sub(rel,R);
    normalModule := ker Hom(relR,R^1);
    h0N := numColumns basis(0,normalModule);
    record("H0_NORMAL " | toString h0N);
    record((if char S == 0 then "H21_CONDITIONAL_ON_INPUT_CERTIFICATE " else "CHAR0_H21_UPPER_BOUND_CONDITIONAL_ON_SMOOTH_LIFT ") | toString(h0N-63));
    record((if char S == 0 then "HILBERT_COMPONENT_DIMENSION_CONDITIONAL_ON_INPUT_CERTIFICATE " else "CHAR0_HILBERT_COMPONENT_DIMENSION_UPPER_BOUND ") | toString h0N);
    assert(h0N >= 63);
    -- This upper bound only applies after component membership is certified.
    record("CHECK_INTENDED_COMPONENT_BOUND_H0N_LE_94 " | toString(h0N <= 94));
);

if phase == "square" then (
    squareIdeal := I^2;
    record("SQUARE_GENERATOR_COUNT " | toString numgens squareIdeal);
    record("START_PARTIAL_RESOLUTION_LENGTH_5");
    -- Ext degrees 3 and 4 need only differentials d3,d4,d5, so resolving
    -- the ideal module through homological degree 5 is sufficient.
    squareModule := module squareIdeal;
    C := res(squareModule,LengthLimit=>5);
    complete C.dd;
    record("PARTIAL_RESOLUTION_COMPLETE");
    record(betti C);
    checkpoint := openOut(prefix | "_square_resolution_data.m2");
    -- Data consists of free-module degrees plus differential entries,
    -- preserving the exact input field's coefficients. With the same S,
    -- reconstruct F_i as S^apply(degrees_i,d->-d), then reconstruct d_i
    -- as map(F_(i-1),F_i,entries_i). Zero-size maps need the stored F_i.
    checkpoint << "squareResolutionDegrees = " << toExternalString(apply(toList(0..5),i->degrees C_i)) << ";" << endl;
    checkpoint << "squareResolutionEntries = " << toExternalString(apply(toList(1..5),i->entries C.dd_i)) << ";" << endl;
    checkpoint << close;
    record("RESOLUTION_CHECKPOINT_WRITTEN");
    W := S^{-8};
    dualPieces := apply(toList(0..5),i->Hom(C_i,W));
    pieceBases := apply(dualPieces,M->basis(0,M));
    pieceDimensions := apply(pieceBases,B->numColumns B);
    record("DEGREE_ZERO_DUAL_DIMENSIONS " | toString pieceDimensions);
    rankList := new MutableList from {0,0,0,0,0};
    scan(toList(3..5),i->(
        D := Hom(C.dd_i,W);
        srcBasis := pieceBases#(i-1);
        tgtBasis := pieceBases#i;
        raw := D*srcBasis;
        coords := raw // tgtBasis;
        assert(tgtBasis*coords == raw);
        scalarMatrix := sub(coords,coefficientRing S);
        rankList#(i-1) = rank scalarMatrix;
        record("DUAL_MAP_RANK_D" | toString i | " " | toString rankList#(i-1));
        matrixFile := openOut(prefix | "_dual_d" | toString i | "_degree0.m2");
        matrixFile << toExternalString entries scalarMatrix << endl << close;
    ));
    ext3 := pieceDimensions#3-rankList#2-rankList#3;
    ext4 := pieceDimensions#4-rankList#3-rankList#4;
    record("EXT3_IDEAL_SQUARE_DEGREE0 " | toString ext3);
    record("EXT4_IDEAL_SQUARE_DEGREE0 " | toString ext4);
    if char S == 0 then (
        record("H11_CONDITIONAL_ON_INPUT_CERTIFICATE " | toString(1+ext4));
        record("H21_CONDITIONAL_ON_INPUT_CERTIFICATE " | toString(ext3-64));
        record("EULER_CONDITIONAL_ON_INPUT_CERTIFICATE " | toString(2*(65+ext4-ext3)));
    ) else (
        record("CHAR0_H11_UPPER_BOUND_CONDITIONAL_ON_SMOOTH_LIFT " | toString(1+ext4));
        record("CHAR0_H21_UPPER_BOUND_CONDITIONAL_ON_SMOOTH_LIFT " | toString(ext3-64));
        if ext4 == 0 then record("CHAR0_PICARD_RANK_ONE_CONDITIONAL_ON_SMOOTH_LIFT");
        record("FINITE_FIELD_OUTPUT_IS_NOT_AN_EXACT_CHAR0_HODGE_PAIR");
    );
    assert(ext3 >= 64 and ext4 >= 0);
);
assert(member(phase,{"normal","square"}));
record("DONE");
log << close;
exit 0;
