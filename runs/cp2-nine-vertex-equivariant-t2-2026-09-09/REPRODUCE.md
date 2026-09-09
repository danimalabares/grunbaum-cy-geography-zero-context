# Reproduce

From this run directory, in order (about 4 minutes total for the S_3 part on a 4-core laptop):

```sh
python3 -B scripts/verify_input.py                       # f-vector, minimal nonfaces, G ≅ S_3, |Aut| = 54; writes data/*.json
python3 - <<'EOF2'
import json; d=json.load(open("data/minimal_nonfaces.json"))
open("data/generators.m2.txt","w").write("I=ideal("+",".join("x_%d*x_%d*x_%d*x_%d"%tuple(m) for m in d["minimal_nonfaces"])+");\n")
EOF2
# regenerate data/group_G_S3.txt and data/group_Aut54.txt from data/groups.json (see logs) or reuse the shipped files
/Applications/Macaulay2-1.20/bin/M2 --script scripts/t2_dims.m2                 # dims: T1_0 = 93, T2_0 = 126 (via CT^2)
/Applications/Macaulay2-1.20/bin/M2 --script scripts/equivariant_t2.m2 data/group_G_S3.txt certificates/G_S3
python3 -B scripts/verify_certificate.py G_S3 6           # independent Fraction-arithmetic re-verification
```

Optional (order-54 automorphism group, generators only; the Python step closes the group):

```sh
/Applications/Macaulay2-1.20/bin/M2 --script scripts/equivariant_t2.m2 data/group_Aut54_generators.txt certificates/Aut54_generators
python3 -B scripts/verify_certificate.py Aut54_generators 54
```

Optional cross-check of the primary obstruction map rank (not used by the main result):

```sh
/Applications/Macaulay2-1.20/bin/M2 --script scripts/quadric_rank_check.m2
```

The scripts `t2_dims.m2`, `equivariant_t2.m2`, `quadric_rank_check.m2` embed the generator
list from `data/generators.m2.txt` at build time; if you regenerate that file, re-splice it
(the shipped scripts already contain it). Expected final lines are recorded in `logs/`.
Hashes of every file in this run are in `HASH_MANIFEST.json` (`python3 scripts/hash_run.py`).

Note on provenance of the shipped files: `certificates/G_S3_certificate.json` was produced by an
earlier revision of `equivariant_t2.m2` that emitted Macaulay2 list braces for the `perm` fields
(repaired in place by a regex to valid JSON, no numeric content touched); the script was then patched
to emit JSON brackets and to skip the closure-dependent checks when the group file is not closed
under composition. `certificates/Aut54_generators_certificate.json` was produced by the shipped
revision. Rerunning the shipped script for `G_S3` regenerates the same matrices.
