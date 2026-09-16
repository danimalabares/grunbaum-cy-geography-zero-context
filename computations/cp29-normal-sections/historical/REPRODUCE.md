# Reproduction

Run from the root of the isolated checkout at historical commit
`30dd90dbdb69e14b1f52b2db70ca451d9281eda9`:

```sh
python3 -B runs/cp2-nine-hilbert-dimension-audit-2026-09-10/check.py
```

Python 3.13.7 was used for the executed exact check. The script requires only the standard library, reads the
historical `data/minimal_nonfaces.json`, and writes only its own audit directory.
Expected results: `Hom_S_I_A_degree0_dimension: 93`, coordinate orbit 72,
Hilbert polynomial coefficients `[3,0,9/2,0,3/2]`. The executed command exited 0
in about four seconds. `exact-check.log` is its captured stdout;
`exact-check.json` includes the multigraded dimensions.

The 84-dimensional Kummer comparison uses external geometric theorems, recorded
in `RESULTS.md` and `SOURCES.md`. Constants concerning Kummer moduli in the script
are **theory inputs**, not independent computer proofs of those theorems.

## Why the tangent computation is exhaustive

A degree-zero homomorphism from the quartic monomial ideal is determined by
coefficients of 459 standard quartic monomials for each of 36 generators.
For each pair `(i,j)` impose

```
(lcm(m_i,m_j)/m_i) * phi(m_i)
  = (lcm(m_i,m_j)/m_j) * phi(m_j) in A.
```

These generate every syzygy: in any fixed monomial multidegree, the generators
dividing that monomial form a basis of the corresponding free-module piece;
the map to the ideal sums their coefficients. Its kernel is spanned by pair
differences. Thus imposing all pairs suffices in every degree.

Surviving output monomials are linearly independent in a monomial quotient.
Multiplication on either side is injective on exponent vectors before reduction.
Consequently every coefficient equation is `v=w` or `v=0`; union-find with a
distinguished zero vertex solves this system exactly in any characteristic.
The result here is used over ℚ and then ℂ. There are 284,130 equations, including
redundancies, and 93 components not joined to zero.

`tangent-basis.json` stores those 93 disjoint supports. A basis vector equals one
on its support and zero elsewhere. Variable `i*459+j` is the coefficient of
standard quartic monomial `j` in the image of generator `i` (all indices zero-based).
Each component has one multidegree. Coordinate derivations are checked to be
unions of complete surviving components; their 72 distinct nonzero multidegrees
prove the orbit rank without floating-point linear algebra.

The polynomial check counts a degree-n monomial with support of size r by
`binomial(n-1,r-1)` and expands with `fractions.Fraction`. It checks equality
coefficient by coefficient with Kummer Riemann–Roch at q=2.

## Integrity and source rendering

`run-manifest.json` records input SHA-256 values. `SHA256SUMS.json` records the
audit artifacts; verify with:

```sh
python3 - <<'PY'
import hashlib, json, pathlib
p = pathlib.Path('runs/cp2-nine-hilbert-dimension-audit-2026-09-10')
for name, expected in json.loads((p/'SHA256SUMS.json').read_text()).items():
    assert hashlib.sha256((p/name).read_bytes()).hexdigest() == expected, name
print('Audit artifact hashes verified')
PY
```

Sources were retrieved to `/private/tmp/cp2-hilbert-audit-sources` and relevant
pages visually checked. PDFs and page images are not copied into this checkout;
the source manifest records their retrieval URLs and hashes. For optional
re-rendering, retrieve the cited PDFs and use PyMuPDF:

```python
import pymupdf
document = pymupdf.open('paper.pdf')
document[page_number - 1].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save('page.png')
```

The numerical/tangent reproduction requires neither these PDFs nor PyMuPDF.
