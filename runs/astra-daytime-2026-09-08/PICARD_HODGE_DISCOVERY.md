# Discovery freeze before external-source checks

Date: 2026-09-08. Scope: Task B; mathematical-paper-audit targeted verification.
No CAS process was run. These are model derivations, not independent human verification.

1. **PROVED**, for a smooth projective complex CY threefold with the supplied complete embedding in P7: the restricted tangent Euler sequence gives h0(TP7|X)=63 and H1(TP7|X)=0; contraction with a volume form gives h0(TX)=h02=0 and h1(TX)=h21. Thus h0(N)=63+h21.
2. **PROVED**, putting C=I/I²: the cotangent Euler sequence gives h1(ΩP7|X)=1, h2=0, h3=63. The induced first-cohomology map sends the hyperplane class to c1(H), which is nonzero because H³=20. Therefore H1(C)=0, h11=1+h2(C), h3(C)=63+h21.
3. **PROVED**, the ideal sequences at twist zero give h2(C)=h3(I²) and h3(C)=h4(I²)-1. Consequently h11=1+h3(I²), h21=h4(I²)-64. Graded local duality identifies these with degree-zero Ext4(I²,S(-8)) and Ext3(I²,S(-8)), respectively.
4. **PROVED**, conceptually Pic(X_M)=Z·H: the constant-sheaf closed-component Cech resolution has nerve homotopy equivalent to the triangulated S³. In total degree two, compatible P³ degree classes give Z, and the actual O(1) class prevents the only possible d3 differential. H1(O)=H2(O)=0 and GAGA/exponential then identify Pic with integral H2.
5. **CONDITIONAL**, rho of the geometric generic fibre would be one if, after a finite base extension splitting its Neron-Severi classes, the normal total space were Q-factorial: closures of divisors become Cartier after a multiple, while formal existence and H1/H2(O_special)=0 identify total-space Pic with special Pic. Normality, extension and finite-base-change hypotheses must be checked separately.
6. **FAILED** shortcut: total-space regularity fails at all coordinate vertices, and the d-chart has seven minimal special generators in codimension four, precluding an lci/parafactorial shortcut there.
7. **OPEN** six-jet rank method: a determinant with leading coefficient of order <=6 gives a generic rank lower bound for every compatible lift. An upper bound or structural kernel is separately necessary for equality. No six-jet calculation by itself can declare all higher corrections zero.

External-source verification follows this freeze; its results and exact citations belong in PICARD_HODGE_PLAN.md.
