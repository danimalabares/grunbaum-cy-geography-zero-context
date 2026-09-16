# Hilbert-dimension audit of the CP²₉ Stanley–Reisner fourfold

**Verdict: the tangent-versus-locus dimension comparison does not exclude a Kummer smoothing.** The actual projective Hilbert tangent has dimension **93**. A smooth, nondegenerate Kummer-type fourfold with the required polarization would lie on an **84-dimensional** Hilbert component. Thus a hypothetical smoothing gives the compatible inequality

\[
84\leq\dim_{[X]}\operatorname{Hilb}^{P}(\mathbf P^8)
\leq h^0(N_{X/\mathbf P^8})=93.
\]

This proves neither existence nor nonexistence of a smoothing. It is our reconstruction, **not an attribution of an argument or numbers to Kapustka**, whose precise argument was unavailable.

Input: separate clone of `https://github.com/danimalabares/grunbaum-cy-geography-zero-context`, commit `30dd90dbdb69e14b1f52b2db70ca451d9281eda9`; historical `runs/cp2-nine-vertex-equivariant-t2-2026-09-09/RESULTS.md`, its published facet data, scripts, and logs. Work is over characteristic zero, with geometric conclusions over ℂ. Input hashes and timing are in `run-manifest.json`. Fable's active-run files were not used; its checkout and processes were not modified. No M2/Sage/Singular job appeared in the initial process inspection, and none was launched here. No additional agents or higher-order deformations were used.

## 1. The actual projective tangent is 93

Set \(S=\mathbf C[x_1,\ldots,x_9]\), \(A=S/I_\Delta\), and \(X=\operatorname{Proj}A\). Here \(N=\mathcal Hom_{\mathcal O_X}(\mathcal I_X/\mathcal I_X^2,\mathcal O_X)\) is the normal **sheaf**; local freeness is not assumed.

The non-Cohen–Macaulay caveat can be resolved. [Altmann–Christophersen, *Deforming Stanley–Reisner schemes*, Proposition 5.4(i), p. 13](https://arxiv.org/pdf/0901.2502v1) identifies \(H^0(N)\) with \(\operatorname{Hom}_S(I_\Delta,A)_0\) for a simplicial complex. Its positive-twist cohomology input is Theorem 2.2, p. 4: \(H^0(X,\mathcal O_X(d))=A_d\) for \(d\geq1\).

A direct application here makes the hypotheses transparent. The ideal is saturated (an intersection of coordinate primes belonging to the 36 facets). Its 36 generators \(m_i\) are quartics. Their Taylor pair relations give a presentation

\[
\bigoplus_{i<j}S(-d_{ij})\longrightarrow S(-4)^{36}\longrightarrow I_\Delta\longrightarrow0,
\qquad d_{ij}=\deg\operatorname{lcm}(m_i,m_j)\in\{5,6,7,8\}.
\]

Sheafify, apply \(\mathcal Hom(-,\mathcal O_X)\), and take sections. Left exactness expresses \(H^0(N)\) as the kernel of the map from \(H^0(\mathcal O_X(4))^{36}\) to \(\bigoplus H^0(\mathcal O_X(d_{ij}))\). The positive-twist identifications turn this into precisely the graded Hom kernel. No Cohen–Macaulay assumption enters.

The independent `check.py` calculation imposes all 630 Taylor pair relations on 16,524 coefficients (\(36\dim A_4=36\cdot459\)). Each coefficient equation is an equality of two variables or a variable set to zero. Exact component counting leaves **93** free coefficients; `tangent-basis.json` records a full basis. This reproduces the published Macaulay2 number by a different method in about four seconds.

## 2. The required Kummer Hilbert locus

Counting monomials by their supports gives, for \(n\geq1\),

\[
P_X(n)=\sum_{r=1}^{5}f_{r-1}\binom{n-1}{r-1}
=\frac32n^4+\frac92n^2+3,
\quad f=(9,36,84,90,36).
\]

Thus the degree is 36 and \(\chi(\mathcal O_X)=3\). The value \(A_0=1\) differs from \(P_X(0)=3\); a Hilbert polynomial need not equal the Hilbert function in degree zero.

For a fourfold \(Y\) of generalized Kummer deformation type, with the standard integral Beauville–Bogomolov form, [Britze–Nieper, §5.2, Theorem 5.1 and its normalization, pp. 18–19](https://arxiv.org/pdf/math/0101062v1) give

\[
\chi(Y,H^{\otimes n})=3\binom{\tfrac12q(H)n^2+2}{2}
=\frac38q(H)^2n^4+\frac94q(H)n^2+3.
\]

Equality with \(P_X\) forces \(q(H)=2\). Kodaira vanishing gives \(h^0(H)=9\) for ample \(H\). Nondegeneracy is open at \([X]\), so a hypothetical Hilbert smoothing uses the complete nine-section embedding in \(\mathbf P^8\).

The Kummer lattice is \(U^3\oplus\langle-6\rangle\), of rank 7 ([Dawes, §2.2, p. 3](https://arxiv.org/pdf/1710.01672v4)). Consequently \(h^{1,1}=5\). The unpolarized deformation germ is smooth of dimension 5, and retaining a nonzero polarization cuts a smooth hypersurface: the polarized germ has dimension **4** ([Huybrechts, §§1.12–1.14, pp. 10–11](https://arxiv.org/pdf/alg-geom/9705025v1)). This count holds for every polarization divisibility; we impose no split-type assumption.

**Embedding hypothesis:** this establishes the dimension of the relevant very ample locus **if it is nonempty**. Very ampleness is open, so any such embedded \(Y\) supplies all four local polarized parameters. Neither matching the polynomial nor ampleness alone proves very ampleness. Nonemptiness is not established in this audit; a hypothetical smoothing would supply it.

Since \(T_Y\simeq\Omega_Y^1\) and \(h^{1,0}(Y)=0\), \(H^0(T_Y)=0\). The projective stabilizer is therefore finite, and choices of projective frame contribute \(\dim\operatorname{PGL}_9=80\). The local embedded locus has dimension \(4+80=\mathbf{84}\). The Euler and normal sequences independently give

\[
h^0(N_{Y/\mathbf P^8})=80+\dim\ker\bigl(H^1(T_Y)\xrightarrow{c_1(H)}H^2(\mathcal O_Y)\bigr)
=80+(5-1)=84.
\]

The polarized germ and projective frames also show that this is an actual local Hilbert dimension, not just an expected dimension.

## 3. Exact comparison and limits

The exact check reproduces the special orbit dimension 72: all 72 off-diagonal derivations are nonzero with distinct multidegrees; diagonal derivations preserve the ideal. Thus the special stabilizer has dimension 8. Smooth Kummer stabilizers have dimension zero. One must use these consistently:

| Quantity | Special \(X\) | Hypothetical smooth \(Y\) |
|---|---:|---:|
| Projective Hilbert tangent | 93 | 84 |
| Projective orbit | 72 | 80 |
| Projective stabilizer | 8 | 0 |
| Tangent modulo the orbit | 21 | 4 |

On a transverse germ removing the **special** 72-dimensional orbit, a putative 84-dimensional smoothing component would require dimension \(84-72=12\), while the tangent bound is \(93-72=21\). Again there is no contradiction.

- **Proved exclusion:** none from this comparison.
- **Inconclusive bound:** \(\dim_{[X]}\mathrm{Hilb}^{P}\leq93\); smoothing would require at least 84.
- **Missing hypotheses for a stronger conclusion:** a justified local/component dimension bound below 84, or a separate proof that the required very ample Kummer locus is empty. Neither is furnished by the historical tangent/obstruction dimensions. A nonzero obstruction space alone supplies no such bound.

The focused dimension audit is complete. Smoothability remains unresolved. See `ledger.json` for claim states and dependencies, `SOURCES.md` for source inspection, and `REPRODUCE.md` for the exact check. This is recorded mathematical analysis, not a claim of qualified-human verification.
