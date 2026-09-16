#!/usr/bin/env python3
"""Exact combinatorial toolkit for finite simplicial complexes.

Pure Python (plus networkx for exact graph isomorphism).  Everything is exact:
face enumeration, f- and h-vectors, pseudomanifold checks, links, minimal
nonfaces, Hilbert series / polynomial of the Stanley--Reisner ring, rational
Betti numbers, exact isomorphism testing (VF2 on the facet--vertex incidence
graph), automorphism groups, and PL-sphere certificates by bistellar flips.
"""
from __future__ import annotations

import itertools
import random
from fractions import Fraction
from math import comb

import networkx as nx
from networkx.algorithms import isomorphism as nxiso


# ----------------------------------------------------------------------------
# basic face machinery
# ----------------------------------------------------------------------------
def parse_facets(text):
    """Parse facets given as whitespace-separated tokens; tokens are either
    digit strings (each character a vertex 1..9) or comma-separated ints."""
    facets = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        for tok in line.split():
            if "," in tok:
                facets.append(frozenset(int(c) for c in tok.split(",")))
            else:
                facets.append(frozenset(int(c) for c in tok))
    return facets


def vertices(facets):
    return sorted(set().union(*facets))


def all_faces(facets):
    faces = set()
    for F in facets:
        F = sorted(F)
        for k in range(1, len(F) + 1):
            for S in itertools.combinations(F, k):
                faces.add(frozenset(S))
    return faces


def f_vector(facets):
    faces = all_faces(facets)
    d = max(len(F) for F in facets)
    return [sum(1 for f in faces if len(f) == k) for k in range(1, d + 1)]


def h_vector(fvec):
    """h-vector of a (d-1)-dimensional complex with f-vector fvec=(f_0..f_{d-1})."""
    d = len(fvec)
    f = [1] + list(fvec)  # f_{-1}=1
    h = []
    for k in range(d + 1):
        h.append(sum((-1) ** (k - i) * comb(d - i, k - i) * f[i] for i in range(k + 1)))
    return h


def is_pure(facets):
    return len({len(F) for F in facets}) == 1


def ridge_incidences(facets):
    """Map ridge (codim-1 face) -> number of facets containing it."""
    inc = {}
    for F in facets:
        for v in F:
            R = F - {v}
            inc[R] = inc.get(R, 0) + 1
    return inc


def is_pseudomanifold(facets):
    return all(c == 2 for c in ridge_incidences(facets).values())


def is_strongly_connected(facets):
    facets = list(facets)
    idx = {F: i for i, F in enumerate(facets)}
    by_ridge = {}
    for F in facets:
        for v in F:
            by_ridge.setdefault(F - {v}, []).append(idx[F])
    G = nx.Graph()
    G.add_nodes_from(range(len(facets)))
    for lst in by_ridge.values():
        for a, b in itertools.combinations(lst, 2):
            G.add_edge(a, b)
    return nx.is_connected(G)


def link(facets, sigma):
    sigma = frozenset(sigma)
    return [F - sigma for F in facets if sigma <= F]


def star_closed(facets, v):
    return [F for F in facets if v in F]


def minimal_nonfaces(facets, max_size=None):
    """All minimal nonfaces (generators of the Stanley--Reisner ideal).
    Brute force over subsets; fine for <= 16 vertices."""
    V = vertices(facets)
    faces = all_faces(facets)
    dim1 = max(len(F) for F in facets) + 1
    top = min(len(V), dim1) if max_size is None else max_size
    out = []
    for k in range(1, top + 1):
        for S in itertools.combinations(V, k):
            fs = frozenset(S)
            if fs in faces:
                continue
            if all(frozenset(T) in faces for T in itertools.combinations(S, k - 1)):
                out.append(tuple(S))
    return out


def euler_characteristic(fvec):
    return sum((-1) ** i * f for i, f in enumerate(fvec))


# ----------------------------------------------------------------------------
# Hilbert series and polynomial of the Stanley--Reisner ring
# ----------------------------------------------------------------------------
def hilbert_polynomial(hvec):
    """Return coefficients (Fractions) of P(k) in the monomial basis, where
    Hilb(k[Delta], t) = sum h_i t^i / (1-t)^d and P(k) = sum_i h_i C(k-i+d-1, d-1)."""
    d = len(hvec) - 1
    # build polynomial in k via exact evaluation + interpolation
    def P(k):
        return sum(hvec[i] * comb(k - i + d - 1, d - 1) if k - i + d - 1 >= 0 else 0
                   for i in range(d + 1))
    # interpolate degree d-1 polynomial from d+1 points (k large enough)
    pts = [(k, Fraction(P(k))) for k in range(d, 2 * d + 2)]
    # Newton / Lagrange to monomial coefficients
    n = len(pts)
    coeffs = [Fraction(0)] * n
    for i, (xi, yi) in enumerate(pts):
        # Lagrange basis polynomial
        num = [Fraction(1)]
        den = Fraction(1)
        for j, (xj, _) in enumerate(pts):
            if j == i:
                continue
            # multiply num by (x - xj)
            new = [Fraction(0)] * (len(num) + 1)
            for a, c in enumerate(num):
                new[a + 1] += c
                new[a] -= c * xj
            num = new
            den *= (xi - xj)
        for a, c in enumerate(num):
            coeffs[a] += yi * c / den
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs


def poly_str(coeffs, var="k"):
    terms = []
    for a, c in reversed(list(enumerate(coeffs))):
        if c == 0:
            continue
        if a == 0:
            terms.append(f"{c}")
        elif a == 1:
            terms.append(f"({c}){var}" if c.denominator != 1 else f"{c}{var}")
        else:
            terms.append(f"({c}){var}^{a}" if c.denominator != 1 else f"{c}{var}^{a}")
    return " + ".join(terms) if terms else "0"


# ----------------------------------------------------------------------------
# rational homology (exact, Fractions) -- for small complexes
# ----------------------------------------------------------------------------
def _rank_Q(rows, ncols):
    """rank over Q of a sparse integer matrix given as list of dict{col:val}."""
    rows = [dict(r) for r in rows if r]
    rank = 0
    pivots = {}
    for r in rows:
        r = {c: Fraction(v) for c, v in r.items() if v != 0}
        while r:
            c = min(r)
            if c in pivots:
                p = pivots[c]
                f = r[c] / p[c]
                for cc, vv in p.items():
                    nv = r.get(cc, 0) - f * vv
                    if nv == 0:
                        r.pop(cc, None)
                    else:
                        r[cc] = nv
            else:
                pivots[c] = r
                rank += 1
                break
    return rank


def _rank_mod_p(rows, ncols, p):
    rows = [dict(r) for r in rows if r]
    rank = 0
    pivots = {}
    for r in rows:
        r = {c: v % p for c, v in r.items() if v % p}
        while r:
            c = min(r)
            if c in pivots:
                piv = pivots[c]
                f = (r[c] * pow(piv[c], -1, p)) % p
                for cc, vv in piv.items():
                    nv = (r.get(cc, 0) - f * vv) % p
                    if nv == 0:
                        r.pop(cc, None)
                    else:
                        r[cc] = nv
            else:
                pivots[c] = r
                rank += 1
                break
    return rank


def betti_numbers(facets, primes=(2, 3, 5, 7)):
    """Rational Betti numbers b_0..b_d, plus Betti numbers mod small primes
    (equal to the rational ones iff no torsion at those primes)."""
    faces = all_faces(facets)
    d = max(len(F) for F in facets) - 1
    by_dim = {k: sorted(sorted(f) for f in faces if len(f) == k + 1) for k in range(d + 1)}
    index = {k: {frozenset(f): i for i, f in enumerate(by_dim[k])} for k in by_dim}
    boundary_rows = {}
    for k in range(1, d + 1):
        rows = []
        for f in by_dim[k]:
            row = {}
            for i, v in enumerate(f):
                g = frozenset(f[:i] + f[i + 1:])
                row[index[k - 1][g]] = (-1) ** i
            rows.append(row)
        boundary_rows[k] = rows
    def bettis(rank_fn):
        ranks = {k: rank_fn(boundary_rows[k], len(by_dim[k - 1])) for k in range(1, d + 1)}
        b = []
        for k in range(d + 1):
            dimC = len(by_dim[k])
            rk_out = ranks.get(k, 0)      # rank of d_k : C_k -> C_{k-1}
            rk_in = ranks.get(k + 1, 0)   # rank of d_{k+1}
            b.append(dimC - rk_out - rk_in)
        return b
    result = {"Q": bettis(_rank_Q)}
    for p in primes:
        result[f"F{p}"] = bettis(lambda rows, n, p=p: _rank_mod_p(rows, n, p))
    return result


# ----------------------------------------------------------------------------
# exact isomorphism via VF2 on the facet--vertex incidence graph
# ----------------------------------------------------------------------------
def incidence_graph(facets):
    G = nx.Graph()
    V = vertices(facets)
    for v in V:
        G.add_node(("v", v), kind=0)
    for i, F in enumerate(facets):
        G.add_node(("f", i), kind=1)
        for v in F:
            G.add_edge(("f", i), ("v", v))
    return G


def isomorphism(facets1, facets2):
    """Return a dict vertex1 -> vertex2 realising a simplicial isomorphism, or None.
    Exact: two pure complexes are isomorphic iff their facet--vertex incidence
    graphs are isomorphic by a kind-preserving bijection."""
    if len(facets1) != len(facets2):
        return None
    if sorted(map(len, facets1)) != sorted(map(len, facets2)):
        return None
    if f_vector(facets1) != f_vector(facets2):
        return None
    G1, G2 = incidence_graph(facets1), incidence_graph(facets2)
    GM = nxiso.GraphMatcher(G1, G2, node_match=lambda a, b: a["kind"] == b["kind"])
    if not GM.is_isomorphic():
        return None
    m = GM.mapping
    phi = {n[1]: m[n][1] for n in m if n[0] == "v"}
    # verify
    S2 = set(facets2)
    assert all(frozenset(phi[v] for v in F) in S2 for F in facets1)
    return phi


def automorphism_group(facets, limit=None):
    """All simplicial automorphisms as dicts (exact, via VF2 enumeration)."""
    G = incidence_graph(facets)
    GM = nxiso.GraphMatcher(G, G, node_match=lambda a, b: a["kind"] == b["kind"])
    auts = []
    for m in GM.isomorphisms_iter():
        auts.append({n[1]: m[n][1] for n in m if n[0] == "v"})
        if limit and len(auts) >= limit:
            break
    return auts


def orbits(auts, V):
    seen, out = set(), []
    for v in V:
        if v in seen:
            continue
        orb = sorted({a[v] for a in auts} | {v})
        seen |= set(orb)
        out.append(orb)
    return out


def perm_cycles(perm, V):
    """Cycle notation for a permutation dict on V (fixed points omitted)."""
    seen, cycles = set(), []
    for v in V:
        if v in seen or perm[v] == v:
            seen.add(v)
            continue
        cyc, w = [], v
        while w not in seen:
            seen.add(w)
            cyc.append(w)
            w = perm[w]
        cycles.append(tuple(cyc))
    return cycles


# ----------------------------------------------------------------------------
# bistellar flips: PL-sphere certificates for small spheres
# ----------------------------------------------------------------------------
def bistellar_options(facets, allow_new_vertex=False):
    """Enumerate legal bistellar moves on a pure d-complex (given as facet set).
    A move is given by a face A (in the complex) with link(A) = boundary of a
    simplex B (B not a face); it replaces A*dB by dA*B.  Returns list of (A, B).
    With allow_new_vertex, the moves (A = facet, B = {new label}) that add a vertex are
    included as well."""
    facets = set(facets)
    faces = all_faces(facets)
    out = []
    by_face = {}
    for F in facets:
        F = sorted(F)
        for k in range(1, len(F)):  # proper faces only
            for Sub in itertools.combinations(F, k):
                by_face.setdefault(frozenset(Sub), []).append(frozenset(F))
    for A, star in by_face.items():
        lk = [F - A for F in star]
        Bset = frozenset().union(*lk)
        need = len(lk[0]) + 1
        if len(Bset) != need or len(lk) != need:
            continue
        if set(lk) != {Bset - {b} for b in Bset}:
            continue
        if Bset in faces:
            continue
        out.append((A, Bset))
    if allow_new_vertex:
        new = max(set().union(*facets)) + 1
        for F in facets:
            out.append((frozenset(F), frozenset({new})))
    return out


def apply_bistellar(facets, A, B):
    facets = set(facets)
    star = {F for F in facets if A <= F}
    new = {(A - {a}) | B for a in A}
    return (facets - star) | new


def bistellar_reduce_to_simplex_boundary(facets, seed=0, max_steps=3000):
    """Reduce a PL d-sphere to the boundary of the (d+1)-simplex by bistellar flips
    (Bjorner--Lutz strategy): always take a random move among those removing the most
    (a move (A,B) with |B| > |A| lowers the f-vector; |B| = d+1 removes a vertex); when no
    lowering move exists, perform random raising moves (2->3 type, occasionally adding a new
    vertex) to escape.  Returns (success, move_list, final_facets)."""
    rng = random.Random(seed)
    cur = set(frozenset(F) for F in facets)
    d = len(next(iter(cur))) - 1
    target = d + 2
    moves = []
    for _step in range(max_steps):
        if len(vertices(cur)) == target and len(cur) == target:
            return True, moves, cur
        opts = bistellar_options(cur, allow_new_vertex=True)
        lowering = [o for o in opts if len(o[1]) > len(o[0])]
        if lowering:
            best = max(len(B) for A, B in lowering)
            cands = [o for o in lowering if len(o[1]) == best]
        else:
            neutral = [o for o in opts if len(o[1]) == len(o[0])]
            raising = [o for o in opts if 2 <= len(o[1]) < len(o[0])]
            adding = [o for o in opts if len(o[1]) == 1]
            r = rng.random()
            if neutral and r < 0.5:
                cands = neutral
            elif raising and r < 0.9:
                cands = raising
            else:
                cands = adding or raising or neutral
        A, B = rng.choice(cands)
        cur = apply_bistellar(cur, A, B)
        moves.append((tuple(sorted(A)), tuple(sorted(B))))
    return False, moves, cur


def verify_bistellar_certificate(facets, moves):
    """Re-apply recorded moves from the start complex, checking legality of each; return
    the final facet set."""
    cur = set(frozenset(F) for F in facets)
    for A, B in moves:
        A, B = frozenset(A), frozenset(B)
        legal = {(a, b) for a, b in bistellar_options(cur, allow_new_vertex=True)}
        if (A, B) not in legal:
            raise ValueError(f"illegal move {sorted(A)} -> {sorted(B)}")
        cur = apply_bistellar(cur, A, B)
    return cur


def is_simplex_boundary(facets):
    facets = set(facets)
    V = set().union(*facets)
    d = len(next(iter(facets)))
    return len(V) == d + 1 and facets == {frozenset(V - {v}) for v in V}


def certify_pl_sphere(facets, seeds=range(30)):
    """Return (ok, moves) where ok means an explicit bistellar sequence to the boundary
    of a simplex was found and re-verified."""
    for s in seeds:
        ok, moves, final = bistellar_reduce_to_simplex_boundary(facets, seed=s)
        if ok:
            fin = verify_bistellar_certificate(facets, moves)
            assert is_simplex_boundary(fin)
            return True, moves
    return False, None


def is_combinatorial_manifold_3(facets):
    """For a pure 3-complex: every vertex link is a 2-sphere (connected, closed
    surface with Euler characteristic 2) and every edge link is a circle."""
    faces = all_faces(facets)
    V = vertices(facets)
    for v in V:
        lk = link(facets, {v})
        fv = f_vector(lk)
        if len(fv) != 3 or euler_characteristic(fv) != 2 or not is_pseudomanifold(lk) or not is_strongly_connected(lk):
            return False
    for e in [f for f in faces if len(f) == 2]:
        lk = link(facets, e)
        fv = f_vector(lk)
        if len(fv) != 2 or fv[0] != fv[1] or not is_pseudomanifold(lk) or not is_strongly_connected(lk):
            return False
    return True


def relabel(facets, phi):
    return [frozenset(phi[v] for v in F) for F in facets]


def facets_to_str(facets, sep=" "):
    return sep.join("".join(str(v) for v in sorted(F)) if max(F) <= 9 else ",".join(str(v) for v in sorted(F))
                    for F in sorted(sorted(F) for F in facets))
