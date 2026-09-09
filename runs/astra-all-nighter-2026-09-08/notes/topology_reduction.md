# Bounded topology fallback: one exact local gluing calculation

**PROVED, local scope:** on the complex algebraic fixed-chart curve carrying
the original six-jet, a specific point of triangle {b,e,h} has total-space
analytic local equation

    XY = q² W,                       with one additional smooth coordinate Z.

After every base change q=t^N, the equation is XY=t^(2N)W. The regular locus
of this local analytic germ is simply connected. Consequently every finite
normal cover of this germ that is étale over its regular locus is a disjoint
union of trivial covers. This kills the transverse cyclic local cover group
along nearby generic points of the same triangle, for covers that extend
over this particular degeneration point.

**OPEN:** π1 of a smooth Calabi–Yau fibre, its Picard torsion, and extension
of all finite covers over the complete degeneration. No global conclusion
on these groups follows from the local calculation. This is method
groundwork obtained while equation computations continue, not a replacement
for the equation objective or a claim that a new global theorem is complete.

## Inputs and the already-failed route

Read-only inputs were the original proof at
`ee984e9541e9cb9259728e6dc7b3a1bc0fda8a9b`, the actual two-jet JSON, the
new independent triangle check, and daytime
`PICARD_VERTICAL_CLASS_OBSTRUCTION.md` and `PICARD_HODGE_PLAN.md`, §§10–11.
The latter correctly rules out global Q-factoriality: the twenty vertical
divisors give a rank-19 subgroup of Cl(Y), disjoint from Pic(Y)=ZH. After
every finite base change the same obstruction remains. Thus local class
groups must retain vertical classes; neither local factoriality nor a
purely rational Picard calculation is a valid torsion argument here.

The source does not establish that the eight vertices exhaust the
total-space singular locus. In fact the triangle calculation below shows
additional codimension-two singularities, even before base change.

The exact coefficient branch over the q-line is convergent near q=0 over
C: it is defined by finite polynomial equations with an invertible selected
Jacobian at the central point. The complex analytic implicit function
theorem identifies its analytic solution with the formal selected branch.
The integral omitted-equation theorem makes this a genuine flat algebraic
family locally. The argument below is about this analytic/algebraic germ.
It does not assert that an arbitrary formal series is analytically
convergent, nor require an analytic embedding of the ramified 101-adic ring
into C. Its application to a formal cover needs the relevant algebraization
or comparison step; an algebraic cover can simply be analytified.

## Exact point and parameter-preserving normal form

Use b=1,e=u,h=v and invert uv. Source rows (3,12,9,7), one-based, have
central terms (av,cuv,ug,df). They generate the full central localized
ideal; exact flatness and Nakayama lift this equality to the completed
family. Their three dead-variable derivatives have determinant u²v².
Analytic implicit elimination of a,c,g therefore leaves a hypersurface

    h(q,u,v,d,f)=0,                   h(0,u,v,d,f)=df.

Its critical point in d,f is unique near the origin, by the invertible
normal Hessian. Write its critical value as Δ(q,u,v). The independently
checked two-jet gives exactly

    Δ(q,u,v)=q² G(q,u,v),
    G(0,u,v)=p(u,v)=−8u²−20uv−8v²−20u−20v−8.

Divisibility by q² is exact analytic divisibility, because the constant and
linear Taylor coefficients of Δ vanish identically on the support torus.
The coefficient computation is in `notes/smoothness_audit.md`: the entire
first-order constrained-critical displacement is zero, so Δ₂ is simply
the restriction of source row 7's second-order coefficient.

Take the explicit algebraic point

    u0=1,       v0=(−5+sqrt(7))/2.

Then p(u0,v0)=0, v0≠0, and p_v(u0,v0)=−8sqrt(7)≠0. This is checked in
Q[s]/(s²−7) by `scripts/check_topology_local_point.py`; its output is
`data/topology_local_point.json`. In particular, higher q-terms cannot
invalidate the coordinate change W=−G(q,u,v), Z=u−1: its support Jacobian
is already invertible at this point.

For completeness, the Morse coordinate change can preserve every base
coordinate q,u,v. Translate d,f to their analytic critical point and use
Taylor's integral formula to write h−Δ as a quadratic form in the translated
variables, with a symmetric analytic 2×2 coefficient matrix invertible at
the origin. After a fixed linear change making its first diagonal entry a
unit, analytic LDL decomposition and square roots of the two diagonal
units give an analytic matrix C. The map y=C(d,f,q,u,v)(d,f)^T has invertible
Jacobian in d,f. The analytic inverse function theorem makes y genuine
normal coordinates. A fixed complex linear change converts its nondegenerate
quadratic form to XY. This changes only the normal coordinates. Thus

    h=XY+Δ,                         XY=q²W.

Replacing q by t^N leaves the same support Jacobian invertible and yields
XY=t^(2N)W, with Z free. This proves the exact analytic normal form,
including all higher coefficients and every positive N. It also induces
an isomorphism of completed local rings; no finite-determinacy theorem is
being assumed.

## Elementary local fundamental-group computation

Let m=2N≥2 and

    V_m={xy=z^m w}⊂C^4.

Its singular locus is {x=y=z=0}. The regular locus is the union of three
opens Ux={x≠0}, Uy={y≠0}, Uz={z≠0}. Each is C*×C²:

    Ux: coordinates x,z,w,      y=z^m w/x;
    Uy: coordinates y,z,w,      x=z^m w/y;
    Uz: coordinates z,x,y,      w=xy/z^m.

First apply van Kampen to Ux∪Uz. Their intersection has coordinates
(x,z,w) and is (C*)²×C. The x-loop generates π1(Ux) and is null in Uz;
the z-loop generates π1(Uz) and is null in Ux. The resulting amalgam is
therefore trivial. Next add Uy. The intersection Uy∩(Ux∪Uz) is connected:
both Uy∩Ux and Uy∩Uz are connected, and their triple intersection is
nonempty. Moreover Uy∩Uz→Uy surjects on π1 via the y-loop. Van Kampen
therefore gives

    π1(V_m,reg)=1.

Here Ux∩Uy and the triple intersection are (C*)³; they were not
misidentified as (C*)²×C, and no assumption that the full intersection is
simply connected is needed.

This computes the **local** regular-locus group as well. Give x,y weights
m+1 and z,w weights 2, so the equation is positively weighted homogeneous.
Positive real weighted scaling preserves its regular locus. A homogeneous
positive proper radius function identifies that regular locus with
(0,∞)×L_reg; sufficiently small weighted neighborhoods identify with
(0,ε)×L_reg. These neighborhoods form a basis at the origin. Thus the
regular locus of the analytic local germ has the same fundamental group.
Adding the free coordinate Z with positive weight does not change this
argument or the group (globally it is a product with C).

The target is normal: it is a hypersurface, hence S2, and its singular
locus has codimension two, hence it is R1. A finite normal cover étale on
the regular locus is analytically a covering there and must split into
trivial covers. Each resulting component is finite birational over the
normal germ, so its normalization is the germ itself. Therefore the whole
finite normal cover is locally trivial. This conclusion assumes étaleness
over the entire regular locus. For a cover initially known only to be
étale in codimension one, one must first apply purity on the regular
target; that is a distinct step in the global strategy.

## What this kills, and what remains

At a generic triangle point with p≠0 the corresponding local equation,
after q=t^N, is xy=z^(2N) times two smooth support parameters. Its transverse
regular-locus group is μ_(2N): the explicit quotient presentation is

    x=s^(2N), y=r^(2N), z=sr,
    ζ·(s,r)=(ζs,ζ^(-1)r).

The action is free away from the origin and C²\{0} is simply connected.
Thus these cyclic quasi-étale covers really exist locally; ramifying the
base does not remove them. However, for a cover that extends over the
point p=0 above, their loops lie inside the simply connected regular
neighborhood just computed and acquire trivial monodromy. Path transport
along the connected smooth torus stratum p≠0 gives the same conclusion
for its transverse inertia. This is the actual gluing mechanism, stronger
and more precise than ignoring all nonvertex strata.

A global approach to Picard torsion would be:

1. A nontrivial n-torsion line bundle on a smooth fibre produces a cyclic
   finite étale cover by taking Spec of ⊕_(i=0)^(n−1)L^(-i), with the chosen
   trivialization L^n=O. To use the degeneration, spread this cover over a
   suitable finite base extension of the smooth part of the algebraic curve.
2. Normalize the total space in that cover. After a further tame base
   extension killing the finitely many vertical ramification indices, the
   normalization is étale in codimension one. Finiteness of normalization,
   normality of the base-changed target and the tame ramification argument
   must be supplied for the chosen algebraic model. Purity then makes it
   étale over the target's regular locus.
3. Prove local extension across every remaining singular stratum. The
   calculation here removes the triangle-258 cyclic inertia via an actual
   point and actual local equation. It does not treat all other triangle
   boundary phenomena, edge strata, or vertices. The non-lci vertex d
   (central local ideal (ah,bf,bg,ce,ef,fh,acg)) still prevents a blanket
   lci-purity argument.
4. If the cover extends étale over the full proper total space, conclude
   from the special fibre's finite-cover theory. Its P³ components and
   connected linear intersections supply a concrete nerve/gluing
   calculation; the sphere alone cannot justify steps 1–3. Alternatively,
   for torsion only, it suffices to prove that the line bundle extends as
   an n-torsion Cartier class, since Pic(Y)=ZH is torsion-free.

The main remaining geometric objects are therefore the local rings

    C[[t,z_j:j≠v]]/(F_i(t^N,x_v=1,x_j=z_j))

at vertices and the analogous support-localized edge rings, with their
maps from neighboring transverse cyclic groups. These must use the exact
algebraic family or a proved analytic normal form, not raw six-jet
truncations. A computation of abstract groups without those inclusion maps
would not complete the reduction.

No substantial CAS, external source search, or background process was used.
The exact support-point check took 0.071 seconds with child maximum RSS
10,498,048 bytes. Its immutable stdout/stderr and command record are in
`logs/topology-local-point.*` and `RUN_LOG.jsonl`. The topological statements
are derivations above, not conclusions inferred from the script's success
message. All statements remain model analysis, not qualified-human review.
