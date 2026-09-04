#!/usr/bin/env python3
"""Elementary exact Hilbert-series and Riemann--Roch checks."""

from fractions import Fraction
from math import comb

h = [1, 4, 10, 4, 1]
one_minus_z_four = [1, -4, 6, -4, 1]
numerator = [0] * 9
for i, x in enumerate(h):
    for j, y in enumerate(one_minus_z_four):
        numerator[i+j] += x*y
assert numerator == [1, 0, 0, -16, 30, -16, 0, 0, 1]

def hilbert(m: int) -> int:
    return sum(h[i] * comb(m+3-i, 3) for i in range(5))

def polynomial(m: int) -> Fraction:
    return Fraction(10, 3)*m**3 + Fraction(14, 3)*m

for m in range(4, 101):
    assert hilbert(m) == polynomial(m)
assert polynomial(0) == 0 and polynomial(1) == 8
assert 6*Fraction(10,3) == 20
assert 12*Fraction(14,3) == 56
assert 94-(8**2-1) == 31
print("FORMULA_CHECKS_PASSED")
print("Hilbert polynomial: (10/3)m^3+(14/3)m")
print("smooth CY consequences: H^3=20, c2.H=56, h0(H)=8")
print("conditional Hilbert bound: h21<=31")
