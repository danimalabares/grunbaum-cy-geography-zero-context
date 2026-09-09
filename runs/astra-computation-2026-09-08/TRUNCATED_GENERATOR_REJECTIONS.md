# Three generator-only truncations are nonflat

8 September 2026. **COMPUTER-CERTIFIED:** all three bounded candidates below
fail the required degree-four flatness condition. This is stronger than
the previously known failure of a particular truncated generator–syzygy
pair: no choice of higher-degree or rational syzygies can rescue these
fixed polynomial generators as a flat continuation of the prescribed
special fibre.

| Candidate | First-order lineage | Test | Nonzero 99-by-99 minor modulo 101 | Verdict |
|---|---|---|---:|---|
| Raw stored generic six-jet, summed as a degree-six polynomial in q | Selected zero-context S3-invariant direction | q=1 | 19 | **FAILED**, fixed generator candidate nonflat |
| Saved `p1_line_state_F_order4.txt`, summed in its one parameter | Older sparse P1 line, not the selected direction | q=1 | 67 | **FAILED**, fixed generator candidate nonflat |
| Saved universal `p1_universal_order4_vF.txt`, with `t_i=y_i q` for the selected 53-vector y | Selected first-order direction; unaveraged universal higher terms | q=1 | 22 | **FAILED**, fixed generator candidate nonflat |

The tests stopped as soon as rank at least 99 was certified. They do not
claim that the full rank is exactly 99. No q=2 test was needed.

## Mathematical meaning

**PROVED.** For sixteen cubic generators `F_i(q)`, let

\[
L(q):S_1\otimes\mathbf Q[q]^{16}\longrightarrow S_4[q],
\qquad x_j\otimes e_i\longmapsto x_jF_i(q).
\]

This matrix has shape `330 x 128`, since `dim S4=binom(11,7)=330`.
At the Stanley–Reisner central fibre the thirty independent linear
syzygies give rank `128−30=98`, so the quotient degree-four dimension is
`330−98=232=P(4)`. The script also verifies rank exactly 98 directly
from the central monomial columns.

A flat homogeneous continuation must retain that degree-four quotient
dimension. For each candidate a 99-by-99 minor of `L(1)` is nonzero in
F101. Every coefficient denominator in the input expressions was
checked to be invertible modulo 101, and the parser permits only
rational-number denominators, not parameter-dependent denominators.
Therefore the corresponding minor of the rational polynomial matrix
`L(q)` is not identically zero. Its rank over Q(q) is at least 99, giving

\[
\dim_{\mathbf Q(q)}(S/(F_1(q),\ldots,F_{16}(q)))_4\le231<232.
\]

This disproves generic degreewise flatness for those specific polynomial
generators. Equivalently, their space of linear syzygies over Q(q) has
dimension at most 29, so they cannot admit thirty syzygies lifting the
independent central linear relations. Allowing arbitrary rational
coefficients in a syzygy matrix cannot change this dimension bound.

**PROVED boundary:** the negative result is over characteristic zero;
this is not an attempt to lift a positive finite-field smoothness claim.
It does not contradict the existence of a formal smoothing with the
same first-order term or six-jet. Adding further generator corrections
changes the candidate and can restore flatness. In particular, raw
six-jet truncation and truncation after a q-dependent normalization are
different polynomial candidates: only the raw one was tested here.

## Why these checks were not redundant

**PROVED (source inspection).** The existing geography script
`../../scripts/verify_failed_truncation.m2` checks the distinct quarantined
`certificates/failed_truncated_order4_family_matrix.txt`, which already
has affine dimension zero and degree 567 at q=1 over F101. That named
order-four artifact contains powers through q6 after nonlinear
substitution and is not automatically the raw generic six-jet.

In the frozen proof,
`reconstruct/p1_universal_order4_line_test_output.txt` records only
`line_base_zero=true`, `line_FR_zero=false` for the specific sparse
fourth-order generator–relation pair. This alone did not reject a
different syzygy matrix for the same generator polynomials.

The existing `reconstruct/p1_q30_q1_mod1009_output.txt` rejects the
different sparse order-thirty truncation: its q=1 ideal has affine
dimension zero, degree 567, and unit saturation. It does not supply the
present degree-four minor for the saved order-four candidate.

Finally, the daytime normalized six-jet polynomial-pair test found a
nonzero FR coefficient at q7. Its scope was expressly only that pair.
The current raw-generator multiplication test is a separate, stronger
negative statement for its precisely identified generator candidate.

## Inputs, certificates and reproducibility

All proof-source inputs were read-only and belong to frozen zero-context
commit `ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`.

| Input | SHA256 |
|---|---|
| `../../equations/deformation_data.json` | `8e01ffc5cec0ecb5859e6a81aa7d0076b8f9c59ef1c7513578b65f993048a59f` |
| proof `reconstruct/p1_line_state_F_order4.txt` | `5b57371b1d040719c893963daddba9e031cd6fb8c39c84d9397118f3b90a3f3f` |
| proof `reconstruct/p1_universal_order4_vF.txt` | `299c9581a5a90e3ce1da251e0471b66edaffe5c4c05b8314c442112b629c0264` |

The exact script is `scripts/reject_truncated_generators.py`. It parses
the polynomial rows using an AST whitelist, validates the central
generators, checks whether the first-order term agrees with the selected
direction modulo 101, then performs sparse modular column elimination.
An independent dense modular determinant calculation checks the original
selected minor, rather than assuming the sparse pivot count is enough.
All row exponent vectors and generator/variable column labels are saved.

The guarded run used one thread, a 300-second cap and a 2800-MB RSS cap.
**COMPUTER-CERTIFIED execution:** script time 5.728 seconds; guarded time
5.948 seconds; sampled peak RSS 25,736 KB. No CAS ran. Per-candidate
checkpoints were written immediately on completion.

Files relative to this run:

```
logs/20260908T124343-truncated-generator-rank.json
logs/20260908T124343-truncated-generator-rank.stdout
logs/20260908T124343-truncated-generator-rank.stderr
logs/20260908T124343-truncated-generator-rank.artifacts/truncated_generator_degree4_ranks.json
logs/20260908T124343-truncated-generator-rank.artifacts/truncated_raw_generic_six_jet_degree4.json
logs/20260908T124343-truncated-generator-rank.artifacts/truncated_saved_sparse_P1_F4_degree4.json
logs/20260908T124343-truncated-generator-rank.artifacts/truncated_universal_F4_selected_S3_weights_degree4.json
```

Exact replay command, when the single computation slot is available:

```
cd /Users/daniel/github/grunbaum-cy-geography-zero-context/runs/astra-computation-2026-09-08
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_guarded.py \
  --seconds 300 --memory-mb 2800 --tag truncated-generator-rank \
  -- python3 scripts/reject_truncated_generators.py
```

**OPEN:** finite equations for an actual smooth fibre. These negative
checks justify moving on from the three fixed truncations; they do not
reject the finite implicit Hilbert-chart curve or its algebraic branch.
