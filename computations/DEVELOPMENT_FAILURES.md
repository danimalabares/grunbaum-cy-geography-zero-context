# Preserved failed computations

## Quarantined source candidate: mathematical negative control

The source packet contains `certificates/failed_truncated_order4_family_matrix.txt`.
The independent script `scripts/verify_failed_truncation.m2` specializes that
candidate at \(q=1\) over \(\mathbb F_{101}\) and obtains affine dimension 0
and degree 567. This proves that this truncation is nonflat and cannot be used
as a smoothing family. Its input is hash-locked; its successful reproduction
is preserved in `failed_truncation.stdout.txt`.

## Extractor development failures: implementation diagnostics only

Two early local development runs failed before producing mathematical output:

- Combining the coordinate-split computation and the versal deformation in
  one Macaulay2 process caused incompatible-ring coercions. The computations
  were separated into independent exact processes; both now pass.
- An early generated Macaulay2 export reused `f` as a list variable, shadowing
  the polynomial-ring variable `f`. The generator was renamed and both final
  exports now parse in clean Macaulay2 processes.

These failures establish no mathematical claim. They are recorded to explain
the present process isolation and export-parse checks. The final successful
stdout/stderr files supersede the transient diagnostic output.
