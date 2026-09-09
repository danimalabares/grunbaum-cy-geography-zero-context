# Atomic claims and dependencies

Targeted verification and new construction; not a fresh full-proof audit.
Human verification: not claimed. Inputs and hashes: SOURCE_MANIFEST.json.

| ID | Normalized claim | Status | Proof/claim state and evidence | Consumers |
|---|---|---|---|---|
| D01 | A101-integral equivariant smoothing exists with prescribed six-jet | CONDITIONAL | accepted supplied proof; established within audit's CAS boundary |D04,D05, numerical CY consequences |
| D02 |291 normalized invariant cubic coefficients; rank270; selected minor−1 | COMPUTER-CERTIFIED | new exact standard-Python enumeration/rational determinant; certificate data/fixed_chart.json |D03,D04 |
| D03 | Exact full Schur equations give the fixed Hilbert completion | PROVED | full30 linear syzygies lift; degreewise Tor1 criterion; converse by flatness/postulation |D04 |
| D04 | Selected270/full6960 equations have identical local germ of dimension21 | PROVED | D02+D03+complete invariant unobstructedness; regular-local equal-dimension quotient |D05 |
| D05 | Displayed finite pointed curve has smooth geometric generic fibre | CONDITIONAL | normalized six-jet, minor−1 integral implicit solution, D01 smoothness stability; FIXED_CHART.md |effective equations, modular bounds |
| D06 | A particular finite-q smooth fibre with manageable exact coefficients is known | OPEN | not claimed; finite implicit curve exists but field/point extraction unfinished |exact fibre calculations |
| D07 | h0N=63+h21 andh11=1+h3(I²),h21=h4(I²)−64 | PROVED | complete Euler/conormal/cohomological derivation in PICARD_HODGE_PLAN |Hodge scripts |
| D08 | Pic(X_M)=ZH and Pic(complete DVR total)=ZH | PROVED | closed-component spectral sequence, exponential, line-bundle lifting, formal existence |D09 |
| D09 | Such total space is notQ-factorial; vertical subgroup rank19 | PROVED | principal vertical divisors are only multiples of total fibre; PICARD_VERTICAL_CLASS_OBSTRUCTION |rules out factoriality route |
| D10 | Geometric generic Picard rank=1 | OPEN | modular vanishing or class group modulo vertical divisors needed; no guessed value |full geography |
| D11 | Actual tangent lies uniquely in topP1³ | COMPUTER-CERTIFIED + PROVED |45minor check + torus ratio identities; entire invariant plane included |prioritizes component route |
| D12 | Local Hilbert dimension≤94 andh21≤31 | CONDITIONAL | accepted genuine quadratic initial equations + CY Hilbert smoothness |determinantal exclusion |
| D13 | Actual smoothing component has dimension94 | OPEN | full38-dimensional lower bound missing |h21=31 would follow |
| D14 | Determinantal generic degree20 family has(2,34), Hilbert dimension97 | PROVED | inspected primary KKThm3.8/Prop3.10, plus normal sequence |D12 excludes component |
| D15 | Old/new tangent classes equivalent under projective identification | FAILED | exactsix transport matrices + distinguishing torus invariant; statement false at tangent level |prevents jet transfer |
| D16 | Old/new arcs belong to same completed Hilbert component | OPEN | common quadratic component is insufficient |possible future invariant transfer |
| D17 | A useful low-degree/rational second CI link is supplied | OPEN | cubic second link returns original; first distinctdegree≥47; no rationality mechanism |no heavy linkage queue |

Dependency map:

    accepted T2^G=0 + D02 + D03 -> D04
    D04 + exact normalized six-jet + D01 -> D05
    D05 + effective field/point extraction + finite-fibre certificate -> D06 target
    D06 + D07 -> exact Hodge numbers
    smooth integral reduction + Ext4_0=0 + D07 -> D10
    D08 +20 vertical components -> D09 -> revised Picard strategy
    quadratic obstruction cone -> D12; full38-dimensional family would giveD13
    D12 + D14 -> determinantal component exclusion
    common quadratic component does NOT implyD16

Coverage: TasksA–E were inspected and addressed; primary source/curve
reduction, cohomological plan, Hilbert explanation, exact old-basis transport
and linkage triage completed. Heavy generic field extraction, exact smooth
closed fibre, I² resolution, fullP1 identity, completed local class groups,
fundamental group and torsion were not computed. Code controls retain
repaired defects and false-positive prevention in FIXED_CURVE_SCRIPT_REVIEW.

Confidence: high in the finite combinatorial/linear identities and stated
cohomological deductions; conditional high in the new algebraic smoothing
curve given the accepted source certificate. Low-degree rationality and
resource estimates are HEURISTIC. No agreement among agents substitutes
for the displayed proofs or exact certificate checks.
