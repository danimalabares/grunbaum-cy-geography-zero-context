# CP²₉ normal-sheaf global sections

This package preserves and makes reproducible the completed 2026-09-10
Hilbert-dimension audit.  It computes global sections of the normal sheaf for
the nine-vertex Stanley--Reisner fourfold (X\subset\mathbf P^8).

For (A=S/I), it assigns quartic corrections to the 36 generators of (I)
and imposes their syzygies.  This computes
\(\operatorname{Hom}_S(I,A)_0\), whose exact dimension is **93**.
Altmann--Christophersen, [*Deforming Stanley--Reisner schemes*, Proposition
5.4(i)](https://arxiv.org/pdf/0901.2502), identifies this group with
\(H^0(X,N_{X/\mathbf P^8})\).

Thus \(\dim_{[X]}\operatorname{Hilb}\leq93\).  Since the relevant smooth
embedded Kummer locus has dimension 84, the compatible comparison
\(84\leq\dim_{[X]}\operatorname{Hilb}\leq93\) determines neither local
dimension nor smoothability.  In particular, this proposed Hilbert-dimension
obstruction proves nothing.

## Reproduce

Dependencies: Python 3 and its standard library only.

From the repository root, run:

```sh
python3 -B computations/cp29-normal-sections/check.py
```

Fresh output is written to `fresh/exact-check.json` and
`fresh/tangent-basis.json`; it is deliberately separate from the recorded
historical output in `historical/`.  The checker is the completed audit's
`check.py`, adapted only to read the packaged exact input at
`input/minimal_nonfaces.json` and write to `fresh/`.  The untouched historical
audit, including its recorded stdout and integrity metadata, is in
`historical/`.  `historical/REPRODUCE.md` documents the original invocation.

The full audit discussion and source notes are in `historical/RESULTS.md` and
`historical/SOURCES.md`.
