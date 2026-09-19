# heap-project (HP) sections consulted, and what the note assumes

HP checkout: `/Users/daniel/github/heap-project`, HEAD `04548da9d` (Vertex algebras, modular forms,
Peter-Weyl). HP fixes the vocabulary that `DANI_NOTE.tex` uses without introduction; everything
else is introduced at first use in the note.

## Assumed (present in HP)

| notion | HP file and section (label) |
|---|---|
| Zariski tangent and cotangent space, Jacobian criterion | `algebraic-geometry.tex`, §Zariski tangent space (`section-zariski-tangent-space`, `definition-zariski-tangent`, `proposition-jacobian-tangent`) |
| Hilbert function, Hilbert polynomial | `algebraic-geometry.tex`, §Hilbert polynomial |
| Hilbert scheme | `algebraic-geometry.tex`, §Hilbert scheme; `deformations.tex` ("Zariski tangent space of the Hilbert scheme") |
| node / ordinary double point (for curves; the threefold node `xy = zw` is written out explicitly) | `algebraic-geometry.tex`, "A node is an ordinary double point" |
| blow-up | `algebraic-geometry.tex`, §Blow-up |
| normalization | `algebraic-geometry.tex`, §Normalization; `commutative-algebra.tex` (`commutative-algebra-section-normalization`) |
| ample and very ample line bundles | `algebraic-geometry.tex`, §Ample line bundles |
| affine cone over a projective variety | `algebraic-geometry.tex` ("be the affine cone over Y") |
| Stanley–Reisner ideal, ring, scheme; the Grünbaum–Sreedharan complex | `stanley-reisner.tex`, §Stanley-Reisner schemes (`section-sr`), §Stanley-Reisner scheme of Grünbaum sphere and a determinantal CY3 (`section-grunbaum-sphere`) |
| the Gulliksen–Negård ("GN") degree-20 determinantal threefold, CGKK's table | `stanley-reisner.tex`, §GN variety (`section-gn`) |
| first-order deformations, `T¹`, flat families | `deformations.tex`, §Deformations of Stanley-Reisner schemes (`theorem-deformations-threefolds`, `remark-dani1`), §Deformations of schemes |
| flat family / degeneration language | `deformations.tex`; `stanley-reisner.tex` §Dual complex of a degeneration |

## Introduced in the note (absent from HP or only mentioned in passing)

del Pezzo surface and its degree; anticanonical embedding; linearly normal; embedding dimension;
Gorenstein versus arithmetically Gorenstein (HP mentions "Gorenstein" only in the linkage notes of
`16th-alga-meeting-2026.tex` and in the CGKK citation of `stanley-reisner.tex`); Cohen–Macaulay via
the length of the minimal free resolution; primitive contraction and Wilson's types I–III; flop
(one clause); section ring; theorem on formal functions; Kawamata–Viehweg vanishing (used as a
black box, named); Hochster's formula (named only, in the paragraph on abstract smoothings).

## Conventions borrowed from HP's `AGENTS.md`

No `align*`; `\mathbb` for number fields; no text inside displayed equations; definitions
italicise the defined term. (The 45-character source line width and the "no subsections" rule of
HP were not applied: the note is not an HP file.)
