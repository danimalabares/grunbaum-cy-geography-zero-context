#!/usr/bin/env python3
"""Check the packet boundary between finite jets and an actual algebraic family."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    os.environ.get("GS_ZERO_CONTEXT_SOURCE", ROOT.parent / "grunbaum-zero-context-proof")
).expanduser().resolve()
REQUIRED_ABSENT = [
    "certificates/gs_smoothing_family_matrix.txt",
    "certificates/gs_smoothing_relations_matrix.txt",
    "reconstruct/p1_sparse_line_family_exact.txt",
    "reconstruct/p1_sparse_line_relations_exact.txt",
    "reconstruct/p1_sparse_line_certificate.txt",
    "enumerate/exact_p1_hodge_certificate.txt",
]
REQUIRED_PRESENT = [
    "deformation/generic_equivariant_state_F_order6.txt",
    "deformation/generic_equivariant_state_R_order6.txt",
    "deformation/generic_equivariant_sixjet_output.txt",
    "certificates/failed_truncated_order4_family_matrix.txt",
]

for name in REQUIRED_PRESENT:
    assert (SOURCE / name).is_file(), f"missing required finite-jet artifact: {name}"
for name in REQUIRED_ABSENT:
    assert not (SOURCE / name).exists(), f"unexpected exact-family artifact now exists: {name}"
print("EXPLICITNESS_BOUNDARY_CHECK_PASSED")
print("present finite six-jet F/R state: true")
print("present explicit finite algebraic smoothing equations: false")
for name in REQUIRED_ABSENT:
    print(f"absent guard artifact: {name}")
