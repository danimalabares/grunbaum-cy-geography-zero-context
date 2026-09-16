#!/usr/bin/env python3
"""Exact check that the crystallographic group of Morin--Yoshida (1991, Section 7, p. 107),
Gamma = L[h] x| G_6 with G_6 = < sigma = diag(omega, omega^2), tau = -swap >,
L[h] = L(omega) h_0 + L(omega) h_1 + L(omega) h_2, h_0 = (omega^2-omega)(1,1), h_1 = (omega^2-omega)(omega,omega^2),
h_2 = (omega^2-omega)(omega^2,omega),
is conjugate in the complex affine group to the row (3,3)_0 of Kaneko--Tokunaga--Yoshida (1982), Theorem 1:
(3,3)_0 = G(3,3,2) x| { L(tau)(-1,1) + L(tau)(zeta^2, zeta) },  zeta = exp(2 pi i/6), at tau = omega = zeta^2,
where G(3,3,2) = < swap, diag(theta^{-1}, theta) >, theta = exp(2 pi i/3) = omega  (KTY Part II, Section 1).
Conjugating element: D = diag(1,-1) followed by the scalar similarity (omega^2 - omega)^{-1}."""
import sympy as sp
from fractions import Fraction


class Qw:
    """Exact arithmetic in Q(omega), omega^2 + omega + 1 = 0; element a + b*omega."""
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)
    def __add__(self, o): o = o if isinstance(o, Qw) else Qw(o); return Qw(self.a + o.a, self.b + o.b)
    def __sub__(self, o): o = o if isinstance(o, Qw) else Qw(o); return Qw(self.a - o.a, self.b - o.b)
    def __neg__(self): return Qw(-self.a, -self.b)
    def __mul__(self, o):
        o = o if isinstance(o, Qw) else Qw(o)
        # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2, w^2 = -1 - w
        return Qw(self.a * o.a - self.b * o.b, self.a * o.b + self.b * o.a - self.b * o.b)
    __rmul__ = __mul__
    def inv(self):
        # (a + b w)^-1 = conj / norm, conj = a + b w^2 = (a - b) - b w, norm = a^2 - ab + b^2
        n = self.a * self.a - self.a * self.b + self.b * self.b
        return Qw((self.a - self.b) / n, -self.b / n)
    def __truediv__(self, o): o = o if isinstance(o, Qw) else Qw(o); return self * o.inv()
    def __eq__(self, o): o = o if isinstance(o, Qw) else Qw(o); return self.a == o.a and self.b == o.b
    def __hash__(self): return hash((self.a, self.b))
    def is_integral(self): return self.a.denominator == 1 and self.b.denominator == 1
    def __repr__(self): return f"({self.a}+{self.b}w)"


w = Qw(0, 1)
zeta = -w * w        # exp(2 pi i/6) = -omega^2
assert w * w * w == Qw(1) and zeta * zeta == w and zeta * zeta * zeta * zeta * zeta * zeta == Qw(1)


def mat(rows): return tuple(tuple(Qw(x) if not isinstance(x, Qw) else x for x in r) for r in rows)
def mmul(A, B): return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(2)), Qw(0)) for j in range(2)) for i in range(2))
def mvec(A, v): return tuple(sum((A[i][k] * v[k] for k in range(2)), Qw(0)) for i in range(2))
I2 = mat([[1, 0], [0, 1]])
swap = mat([[0, 1], [1, 0]])
sigma = mat([[w, 0], [0, w * w]])
tau = mat([[0, -1], [-1, 0]])
D = mat([[1, 0], [0, -1]]); Dinv = D
g1 = swap
g2 = mat([[w.inv(), 0], [0, w]])
def group(gens):
    G = {I2}; frontier = [I2]
    while frontier:
        new = []
        for A in frontier:
            for g in gens:
                B = mmul(g, A)
                if B not in G:
                    G.add(B); new.append(B)
        frontier = new
    return G
G6 = group([sigma, tau]); G332 = group([g1, g2])
print("order G_6 =", len(G6), " order G(3,3,2) =", len(G332))
conj = {mmul(mmul(D, g), Dinv) for g in G332}
print("D G(3,3,2) D^-1 == G_6 :", conj == G6)
refl = [g for g in G6 if mmul(g, g) == I2 and g != I2 and g[0][0] + g[1][1] == Qw(0)]
print("number of reflections (order 2, trace 0) in G_6:", len(refl), "-> dihedral S_3:", len(G6) == 6 and len(refl) == 3)
v1 = (Qw(-1), Qw(1)); v2 = (zeta * zeta, zeta)
s = w * w - w
h0 = tuple(s * x for x in (Qw(1), Qw(1))); h1 = tuple(s * x for x in (w, w * w)); h2 = tuple(s * x for x in (w * w, w))
def solve2(u1, u2, vec):
    # vec = a u1 + b u2 ; Cramer
    det = u1[0] * u2[1] - u1[1] * u2[0]
    a = (vec[0] * u2[1] - vec[1] * u2[0]) / det
    b = (u1[0] * vec[1] - u1[1] * vec[0]) / det
    return a, b
for name, h in (("h0", h0), ("h1", h1), ("h2", h2)):
    vec = tuple(x / s for x in mvec(Dinv, h))
    a, b = solve2(v1, v2, vec)
    print(f"(D^-1 {name})/(omega^2-omega) = {a} v1 + {b} v2 ; integral over Z[omega]:", a.is_integral() and b.is_integral())
for name, v in (("v1", v1), ("v2", v2)):
    vec = tuple(s * x for x in mvec(D, v))
    a, b = solve2(h0, h1, vec)
    print(f"(omega^2-omega) D {name} = {a} h0 + {b} h1 ; integral:", a.is_integral() and b.is_integral())
for gname, g in (("swap", g1), ("diag(omega^-1,omega)", g2)):
    for vname, v in (("v1", v1), ("v2", v2)):
        a, b = solve2(v1, v2, mvec(g, v))
        print(f"{gname} {vname} = {a} v1 + {b} v2 ; integral:", a.is_integral() and b.is_integral())
print("CONCLUSION: Morin--Yoshida's Gamma is affinely conjugate (by D = diag(1,-1) and the similarity (omega^2-omega)^-1)")
print("to KTY's (3,3)_0 with modulus tau = omega; its point group is G(3,3,2), dihedral of order 6 = S_3.")
