# Provenance freeze

## Immutable source

- Original audit layout: sibling directory `../grunbaum-zero-context-proof`
- Configurable source locator: environment variable `GS_ZERO_CONTEXT_SOURCE`
- Requested commit and observed HEAD: `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`
- Observed branch: `main`
- Observed Git tree: `451a038cdd9fece1d35bb32f1268756fb55cebcd`
- Observed status: clean (`git status --porcelain` empty)
- Commit subject: `Package ultra-01 zero-context smoothing candidate`
- Author/committer date: `2026-09-03T14:04:33-03:00`
- Commit parent: none (the packaged repository commit is a root commit)

The packet's own provenance records model/run `gpt-5.6-sol`, `ultra-01`,
and archive SHA-256
`f7bdb43c36df6529b0affb39d1870151a6f8982e8a65af3369622b57be661cd5`.

## Frozen relevant files

The deterministic verifier `scripts/verify_source.py` locks the commit,
tree, clean status, and these SHA-256 values:

| Source-relative file | SHA-256 |
|---|---|
| `README.md` | `18aebfaf69483659d58130f130a0b3bb4687167041be249f0a6dc4643ea82555` |
| `PROVENANCE.md` | `0ab9958b6a0c354af0ea77113a92da9a7e05540d1597f321f1c1f53b93481f52` |
| `FINAL.md` | `a2fb4e12b44989522f6fb106dff07b69bebaca9a509dd6d326c623d244e5fbf8` |
| `PROOF.md` | `f662287d41f5667cbe9bdc5774834a18e990b235c66f1902530ccf5cbac10c8f` |
| `FORMAL_SMOOTHING_THEOREM.md` | `ab6a7946a6f72a154a3e1cab93eeab06beba2518fca6b8adefd6b8c2ef44c42b` |
| `deformation/EQUIVARIANT_FORMAL_LIFT.md` | `93cdd165b8ba6ae3d4753213bcf489ebc0f3848ab9bb5031cbc2e88a81d0fa08` |
| `deformation/INTEGRAL_EQUIVARIANT_LIFT.md` | `e9c6fc29c2ebdd83ac3ccb2cadfd89dadbd36fa8dee67dfd9206fe0fe2263a95` |
| `enumerate/FORMAL_ALGEBRAIZATION.md` | `c4743605429306c76e9827822a35bb708ffaf373756f3e9b2ad6400524e8c2c2` |
| `deformation/build_equivariant_sixjet.m2` | `708d5dbb0d5ee43d2869af2ae47e165c9c91810b698fc38198afa8decdc02fb5` |
| `deformation/generic_equivariant_state_F_order6.txt` | `8c5040d19de950bd4e852ce6b11fc08c1bb605d2f97b5bacdaebce3b10056351` |
| `deformation/generic_equivariant_state_R_order6.txt` | `39e841e2e5b5196a160c3fd3ac8457727976ecd2d9ecc933abf25728fa985874` |
| `deformation/generic_equivariant_sixjet_output.txt` | `0bc0af569146605f379142310b71921d4b746ac8c8b089e392eaeb82ac3697c8` |
| `certificates/hom_basis.json` | `3bf7b7fdd8d2b2a9ce81a2fe9b392e1262f418f8ca8b5b3a03bd84c2efd00dcc` |
| `scripts/sr_hom.py` | `82a89a138152104d00dfaa9e61e09381f104f4253759fc8b4d0d8996dcb46fef` |
| `reconstruct/coordinate_split_rank.m2` | `e2f9823ef7f1e1ac31381869152a46155730bcac019a707d7643914740112d61` |
| `deformation/check_sparse_direction_symmetry.m2` | `4a3d64d2506061c63b674e33785f8ec292cccb728cfbc8ea13530d744266ac32` |
| `reconstruct/audit_section5_numerics.m2` | `1e60779a5c5d1235ef987656d9cc7fc7ce6eafadf6511392a558ea45e8ba8b5f` |
| `reconstruct/audit_section5_full_kuranishi.m2` | `2298e285eee91ecc66d73de174b737e5824227c508601b4e681089adebd2a218` |
| `certificates/failed_truncated_order4_family_matrix.txt` | `0f08625a7358bec8248ee256f025975ccd9cf9338cd1f0392abefbdc38d22eb4` |
| `failed_verify_truncated_order4.m2` | `8b6b65e49ce61ca624c8d3e67f7c56548cf5ecc1b71f0b9331c91a220b80bc1d` |

Source files are read in place; none are copied over as authorities or
modified. `computations/SHA256SUMS` freezes the research-workspace outputs.

## Reproduction environment

- macOS/Darwin host
- Macaulay2 1.20
- Python 3.13.7
- Git 2.37.1
- exact coefficient fields: \(\mathbb Q\), and \(\mathbb F_{101}\) only for the frozen negative control

## Scope isolation

Discovery and extraction were confined to this zero-context repository.
No result from `fable-dgla-only`, the cross-model audit workspace, or
`sr-project/main/rl` was used. External literature research was recorded
separately and began only after source-only extraction was complete.
