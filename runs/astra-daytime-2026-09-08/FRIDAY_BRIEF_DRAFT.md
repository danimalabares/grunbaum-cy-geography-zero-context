# Friday discussion draft

**CONDITIONAL on the stated exact-CAS trust boundary:** the zero-context
proof establishes a smoothing of the Grünbaum–Sreedharan Stanley–Reisner
threefold. Its smooth fibres have K=O, H³=20, c2.H=56 and h21≤31,
with H primitive, complete and very ample. The independent audit found
the mathematical chain established, retaining the four specified Singular
membership/standard-basis dependencies. We have not spent this sprint
repeating that audit.

**PROVED with a new small exact certificate:** there is now a finite
algebraic presentation for a smoothing curve, rather than only existential
curve selection. Normalize the sixteen cubic generators, imposeS3, and
lift the thirty linear syzygies. This leaves 291 generator coefficients.
The fixed Hilbert equations have 270 independent derivatives with minor −1,
and the fixed Hilbert germ is formally smooth of dimension 21. Prescribing
the 21 free coordinates through the certified six-jet selects a finite
algebraic curve with smooth generic fibre. The displayed equations are
large; a usable coefficient field and a specified smooth closed fibre
remain **OPEN**. The overnight target is to extract those, not rebuild
the full53-parameter versal system.

**PROVED:** the full Hilbert tangent dimension 109 is 56 coordinate
directions plus 53 intrinsic directions. The largest quadratic obstruction
component has dimension 38=17+3×7, so every Hilbert component through the
special point has dimension at most 94=56+38. Our chosen tangent lies
uniquely in this top quadratic component. It is **OPEN** whether this is
an actual 94-dimensional smoothing component. If it is, h21=94−63=31.
The known generic determinantal family has (2,34) and smooth Hilbert
dimension 97, so it cannot specialize to this point under the audited
local-bound hypothesis. The relevant primary result is Kapustka–Kapustka,
Theorem3.8/Proposition3.10, not Bertin's earlier conflicting Hodge line.

**PROVED computational target:** on a certified smooth fibre,
h21=h0(N)−63 and h11=1+h3(P7,I²). Only the degree-zero portions of
three dual maps in a partial I² resolution are needed. A good-prime
vanishing of the latter cohomology, with a certified smooth lift, can prove rho=1. Exact Hodge numbers,
Euler number, Picard rank, torsion and fundamental group are still **OPEN**.

**PROVED new obstruction:** although Pic(X_M)=ZH, the normal complete-DVR
total space has nineteen independent vertical Weil classes from its
twenty central components, and cannot be Q-factorial. Thus Picard transfer
needs control of class groups modulo vertical components, not a claim
that the total space is factorial.

**COMPUTER-CERTIFIED + PROVED lineage separation:** the older DGLA and
zero-context tangent classes can be transported into one exact basis.
Both lie inP1³ but are not equivalent under projective automorphisms of
the special fibre and invertible reparametrization. Their completed
Hilbert-component relationship remains **OPEN**. Hilbert connectedness
only gives component chains, potentially through singular/nonreduced
schemes; it does not join their smooth loci or identify these arcs.

## Five precise questions for Grzegorz and Sergey

1. Can the S3-fixed291-coefficient cubic/linear-syzygy chart be recognized
   as a known codimension-four Gorenstein construction, or reduced by an
   equivariant format to a tractable number-field fibre? We have its
  270-pivot determinant−1 and the exact selected six-jet.
2. Is there a geometric reason that the complete Kuranishi ideal has a
  38-dimensional branch with this leading P1³ component? What structure
   would force the twelve equations remaining after the15-pivot reduction
   to vanish to all orders, and hence establishh21=31?
3. Can divisor closures on this degeneration be shown to have class group
   generated rationally by H and the twenty vertical components? The
   total space cannot be Q-factorial, so a useful local theorem must
   compute classes modulo those components and glue them globally.
4. For this resolution type inP7, is there an efficient geometric or
   representation-theoretic way to computeH3(I²), or an expected Picard
   lattice that a single good-prime conormal calculation could test?
   Which evidence would distinguishrho1 fromrho≥2?
5. Given two explicitly inequivalent tangents on the same top quadratic
   component, what would establish that the older DGLA and zero-context
   arcs lie on the same completed Hilbert component? Are there reusable
   format, apolar or Hilbert-chart coordinates that make that comparison
   exact without identifying the arcs?

If tonight produces nothing further, all statements above retain their
stated justification. For the Abel proposal, the concrete next objectives
are manageable finite fibre equations, exact Picard/Hodge geography, and
the dimension/component theorem. Linkage remains secondary: the known
degree61 residual has no presently useful descending/rational next link.
