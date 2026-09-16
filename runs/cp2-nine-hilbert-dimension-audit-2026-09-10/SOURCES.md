# Primary-source inspection

Access date: 2026-09-10. Mathematical discovery was recorded in `DISCOVERY.md`
before the external-source phase. Page numbers below equal PDF page numbers.
Hashes of retrieved PDFs and visually inspected renders are in
`source-manifest.json`; temporary files were kept separate from audit artifacts.

| Source/version | Exact passage inspected | Applicability and inspection state |
|---|---|---|
| [Altmann–Christophersen, arXiv:0901.2502v1](https://arxiv.org/pdf/0901.2502v1), *Deforming Stanley–Reisner schemes*; published Math. Ann. 348 (2010), 513–537 | Theorem 2.1 and section/local-cohomology sequence, p. 3; Theorem 2.2, p. 4; Proposition 5.4(i), p. 13 | `inspected-primary`, including rendered pages. The tangent comparison applies to a simplicial complex and uses no Cohen–Macaulay assumption. The report also gives its concrete presentation proof. |
| [Britze–Nieper, arXiv:math/0101062v1](https://arxiv.org/pdf/math/0101062v1), *Hirzebruch–Riemann–Roch Formulae on Irreducible Symplectic Kähler Manifolds* | §5.2, Theorem 5.1, p. 18; Lemma 5.2 and normalization in the theorem proof, p. 19 | `inspected-primary`, including rendered formulas. The source initially uses λ; its proof states q=(n+1)λ/2. Substitution yields (n+1) binom(q/2+n,n). We use n=2 and deformation invariance. |
| [Dawes, arXiv:1710.01672v4](https://arxiv.org/pdf/1710.01672v4), 5 May 2024, *On the Kodaira dimension of the moduli of deformation generalised Kummer varieties* | §2.2, pp. 3–4 | `inspected-primary`, including rendered pages. Supplies the rank-seven Kummer lattice and polarized period context. Only the general lattice statement is needed; the subsequent split-polarization restriction is not imposed on this audit. |
| [Huybrechts, arXiv:alg-geom/9705025v1](https://arxiv.org/pdf/alg-geom/9705025v1), *Compact Hyperkähler Manifolds: Basic Results* | §1.12, p. 10; §§1.14–1.15, p. 11 | `inspected-primary`, including rendered pages. The local deformation germ is smooth of dimension h11, and a nonzero line-bundle class imposes one independent condition. The polarization contraction map is explicitly surjective. No global projectivity or global Torelli claim from this version is used. |

Standard background used: Kodaira vanishing for an ample line bundle on a smooth
complex projective variety with trivial canonical bundle; the Hilbert tangent
description by the normal sheaf; Euler/normal exact sequences; openness of very
ampleness and nondegeneracy; dimension of PGL and orbit–stabilizer in characteristic
zero. These statements were applied with their hypotheses displayed in the report.

Kapustka's precise argument: `unavailable`, as specified in the task. No inference
about his numbers or proof is made. A brief navigation check of Varesco,
arXiv:2211.11485, found base-point-freeness statements; these are not used to infer
very ampleness or nonemptiness of the required Hilbert locus.

Tool limitations and recoveries: sandbox `ps` was denied; elevated read-only `ps`
succeeded. Some web PDF screenshots failed with cache errors. An attempted Dawes
v5 URL returned 404; the available PDF was v4, whose version was read on its first
page. `pdftotext` was unavailable. Swift/PDFKit rendering failed because of the
installed compiler/SDK mismatch and cache access, and `sips` rendering failed.
That process exited and no algebra job was affected. PyMuPDF 1.28.2 was installed
only under `/private/tmp/cp2-hilbert-audit-pylibs`; it rendered all decisive pages
successfully, which were inspected with `view_image`. These recoveries leave no
formula-transcription obligation open.
