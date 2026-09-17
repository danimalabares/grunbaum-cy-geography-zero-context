# Unresolved identifications, failed checks and pending work

Status labels as in `REPORT.md`. Nothing in this file is a novelty claim: "not located" means not
located in this run, whose literature scope was the ten cached references.

## Pending by scope (stage 1 stops here)

1. **The 21 non-symmorphic groups** 17, 24, 90, 91, 93, 95, 98, 151, 153, 178, 179, 180, 181, 182, 198,
   199, 208, 210, 212, 213, 214: no fixed-locus computation, no orbifold Hodge numbers, no literature
   search. Their exact generators with translation parts (ITA standard setting and origin, primitive
   basis of Λ) are in `table/space_groups_35.tsv` and `output/crystallographic_data.json`, verified
   against two databases. What stage 2 needs is listed in `REPORT.md` §8.
2. **Six-dimensional toroidal-orbifold classification** (Fischer–Ratz–Torrado–Vaudrevange,
   arXiv:1209.3906): the Z-classes there are six-dimensional lattices; the present lattices
   `L_τ = Λ ⊕ τΛ` with diagonal action `ρ ⊕ ρ` have to be located among them (Z₂×Z₂: 12 Z-classes,
   35 affine classes; S₃: 6/11; D₄: 9/48; D₆: 2/8; A₄: 9/15; S₄: 6/19). Expected but **not verified**:
   P222 is their class 1–1 (Donagi–Wendland 0–1, lattice SU(2)⁶, the standard `T⁶/(Z₂×Z₂)` with
   (51,3)). Their data files were not retrieved.
3. **Other named families.** No attempt was made to identify any of the 14 threefolds with toric
   hypersurfaces, complete intersections, Borcea–Voisin models or string-theory orbifold tables beyond
   the Kummer papers.

## Open mathematical questions met in stage 1

4. **Deformation equivalence / isomorphism** of the threefolds of different Z-classes with equal Hodge
   numbers: P312 vs P321 (15,15), F432 vs I432 (11,3), C222 vs P622 (21,9), F222 vs I422 (15,3) (and,
   with the controls, F222 vs I222, F23 vs I23). Donten-Bury raises the dual-pair case explicitly and
   leaves it open. Not pursued (out of scope). Hence the number of distinct deformation families among
   the 14 is known only to lie between 10 and 14.
5. **Dependence on τ.** All computed invariants are τ-independent; whether `{Y_τ}_τ` is a single
   deformation family (e.g. via the relative `G`-Hilbert scheme of the abelian scheme over the upper
   half plane) was not analysed.
6. **Fundamental group.** `π₁(A_τ/G) = 1` for the 14 groups is a deduction from Armstrong's theorem
   (not re-read); `π₁(Y_τ) = π₁(A_τ/G)` relies on Kollár 1993, Thm 7.8 / Takayama 2003 (not re-read).
   Both statements are standard but were not verified from the sources in this run. For the two
   controls I222, I23 the same deduction gives `π₁(A_τ/G) ≅ (Z/2)²`; this is consistent with, but
   sharper than, Andreatta–Wiśniewski's `H¹(X,Z) = 0`, and has not been compared with any published
   fundamental-group computation.

## Unreconciled observations (no effect on the results)

7. **Donten-Bury, table for D12 (P622), row of the central involution**: the paper lists the images in
   `Y = A³/G` of the 16 fixed curves as "3 × P¹ + 1 × A"; the `G`-orbit decomposition computed here
   is `1 + 3 + 3 + 3 + 6` (four `P¹` and one elliptic curve). Both the paper's total
   `t⁶+21t⁴+20t³+21t²+1` and Burek's (21, 9) agree with the value computed here, so the discrepancy is
   confined to that intermediate row (or to its reading).
8. **Bilbao Crystallographic Server** was not machine-readable (human-verification wall); provenance
   rests on spglib and GAP CrystCat, which agree coset by coset for all 37 groups processed.

## Limits of the certificates

9. The intertwiner search proves non-conjugacy only when every intertwiner module has rank ≤ 1
   (irreducible representations: A₄, S₄). For 222 (rank 3) and 422, 32, 622 (rank 2) the pairwise
   non-conjugacy of the classes is established by invariants (`REPORT.md` §3); the search itself
   supplies only the positive certificates `P`.
10. The S³ property of the 35 real orbifolds is cited from Johnson–Burnett–Dunbar (who cite Dunbar's
    dissertation) and was not re-derived; only the *list* was verified against the source.
