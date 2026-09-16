#!/usr/bin/env python3
"""Counting obstruction for a vertex-minimal (4,2)_1 model (fast; no search needed).

Let H = G(4,2,2) x| Lambda' (conjugate of (4,2)_1, see four_two_one_search.py) act on E x E with
the product of two '(centre, corner, midpoint)' decompositions (vertex set E[2] x E[2], 8 x 8 = 64
product cells Delta_2 x Delta_2 per period of Z[i]^2).  Any H-invariant diagonalisation of this
cell structure has 6 simplices per cell.  If the H-action is regular (a simplex fixed as a set is
fixed pointwise), then no nontrivial affine map fixes a nondegenerate 4-simplex, so H acts freely
on facets and the quotient complex has exactly (#facets on the cover)/|H_N| facets and
(#vertex H-orbits) vertices.  A simplicial quotient would be a triangulation of C^2/H = CP^2 and
therefore a closed combinatorial 4-manifold with Euler characteristic 3, so Dehn--Sommerville
(2 f_3 = 5 f_4 and 2 f_1 - 3 f_2 + 4 f_3 - 5 f_4 = 0) determine f_1 from f_0 and f_4.
"""
from __future__ import annotations

import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def main():
    # numbers from the finite model (cover Z^2/12Z^2, see four_two_one_search.py): computed here directly
    import four_two_one_setup as st
    n_cells, H_order, n_vertex_orbits = st.n_cells(), st.H_order(), st.n_vertex_orbits()
    f4 = 6 * n_cells // H_order
    f0 = n_vertex_orbits
    f3 = 5 * f4 // 2
    # chi = 3: f0 - f1 + f2 - f3 + f4 = 3  and  2 f1 - 3 f2 + 4 f3 - 5 f4 = 0
    # => f2 = f1 + (f3 - f4 + 3 - f0);  2 f1 - 3 f1 - 3 (f3 - f4 + 3 - f0) + 4 f3 - 5 f4 = 0
    # => f1 = 4 f3 - 5 f4 - 3 (f3 - f4 + 3 - f0) = f3 - 2 f4 - 9 + 3 f0
    f1 = f3 - 2 * f4 - 9 + 3 * f0
    f2 = f1 + (f3 - f4 + 3 - f0)
    out = {
        "product_cells_on_cover": n_cells, "H_order_on_cover": H_order, "facets_on_cover": 6 * n_cells,
        "quotient_facets_if_regular": f4, "quotient_vertices": f0, "forced_f3": f3,
        "forced_f1_from_Dehn_Sommerville_and_chi_3": f1, "forced_f2": f2, "max_possible_f1": comb(f0, 2),
        "contradiction": f1 > comb(f0, 2),
        "conclusion": ("no regular H-invariant diagonalisation of the vertex-minimal product cell structure has a "
                       "simplicial quotient: the quotient would have %d vertices and %d facets, forcing f_1 = %d > C(%d,2) = %d"
                       % (f0, f4, f1, f0, comb(f0, 2))) if f1 > comb(f0, 2) else "no counting obstruction",
        "remark": "For comparison, the (m,1)_0 lifts have 6144/128 = 48 facets and 10 vertices, matching CP^2_10, "
                  "and Kuehnel's CP^2_9 has 9 vertices and 36 facets.",
    }
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(ROOT, "output", "four_two_one_counting.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
