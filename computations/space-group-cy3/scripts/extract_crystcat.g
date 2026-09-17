# Extract the ITA-setting affine generators of the 35 space groups from the GAP
# packages Cryst/CrystCat (SpaceGroupIT).  Output: one JSON object on stdout.
# Convention of Cryst: affine matrices act on ROW vectors from the right,
#   (x, 1) -> (x, 1) * M,  M = [[A, 0], [t, 1]]  (linear part A in the upper-left
#   3x3 block, translation t in the last row).
# Run (from computations/space-group-cy3):
#   sage -gap -q < scripts/extract_crystcat.g > data/crystcat_generators.json
SetPrintFormattingStatus("*stdout*", false);;
LoadPackage("cryst");;
LoadPackage("crystcat");;
# The 35 groups of the audit, followed by the two symmorphic CONTROL groups 23 (I222) and
# 197 (I23), which are not in the 35-list but complete the 16 symmorphic Sohncke groups with
# non-cyclic point group.
nums := [16,17,21,22,24,89,90,91,93,95,97,98,149,150,151,153,155,177,178,179,180,181,182,
         195,196,198,199,207,208,209,210,211,212,213,214, 23, 197];;
Print("{\"gap_version\": \"", GAPInfo.Version, "\", ");;
Print("\"cryst_version\": \"", GAPInfo.PackagesLoaded.cryst[2], "\", ");;
Print("\"crystcat_version\": \"", GAPInfo.PackagesLoaded.crystcat[2], "\", ");;
Print("\"convention\": \"right action on row vectors; 4x4 augmented matrices [[A,0],[t,1]]; entries as strings (rationals)\", ");;
Print("\"groups\": [\n");;
for i in [1..Length(nums)] do
  n := nums[i];
  S := SpaceGroupIT(3, n);
  gens := GeneratorsOfGroup(S);
  P := PointGroup(S);
  Print("{\"number\": ", String(n), ", \"settings\": \"", SpaceGroupSettingsIT(3, n), "\", ");
  Print("\"point_group_order\": ", String(Size(P)), ", ");
  Print("\"is_symmorphic_crystcat\": ", String(IsSymmorphicSpaceGroup(S)), ", ");
  Print("\"generators\": [");
  for j in [1..Length(gens)] do
    M := gens[j];
    Print("[");
    for r in [1..4] do
      Print("[");
      for c in [1..4] do
        Print("\"", String(M[r][c]), "\"");
        if c < 4 then Print(", "); fi;
      od;
      Print("]");
      if r < 4 then Print(", "); fi;
    od;
    Print("]");
    if j < Length(gens) then Print(", "); fi;
  od;
  Print("]}");
  if i < Length(nums) then Print(",\n"); else Print("\n"); fi;
od;;
Print("]}\n");;
QUIT;
