#!/usr/bin/env python3
"""Finite first-order and Hensel nonsingularity certificates for five lines.

Root must run this under the shared resource guard. This script does not
solve/approximate the 270 coefficient numbers. It certifies the line Hensel
systems over that exact, audited fibre using first-order data and exact FR=0.
All writes are confined to the explicitly supplied fresh output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
import sympy as sp

V = 'abcdefgh'
SUPPORT = (0, 1, 2, 4)
OUTSIDE = (3, 5, 6, 7)
NVAR = 12
PARAMETERS = ['u', 'v', 'w', 'z', 'd_s', 'd_t', 'f_s', 'f_t',
              'g_s', 'g_t', 'h_s', 'h_t']


class FF:
    """F101[alpha]/(alpha^2-7alpha+28), also representing its prime field."""
    __slots__ = ('a', 'b')
    def __init__(self, a=0, b=0):
        if isinstance(a, FF): self.a, self.b = a.a, a.b
        else: self.a, self.b = int(a) % 101, int(b) % 101
    def __add__(self, other):
        other = FF(other); return FF(self.a + other.a, self.b + other.b)
    __radd__ = __add__
    def __neg__(self): return FF(-self.a, -self.b)
    def __sub__(self, other): return self + (-FF(other))
    def __rsub__(self, other): return FF(other) - self
    def __mul__(self, other):
        other = FF(other)
        return FF(self.a*other.a - 28*self.b*other.b,
                  self.a*other.b + self.b*other.a + 7*self.b*other.b)
    __rmul__ = __mul__
    def inverse(self):
        norm = (self.a*self.a + 7*self.a*self.b + 28*self.b*self.b) % 101
        assert norm, 'division by zero in residue field'
        n = pow(norm, -1, 101)
        return FF((self.a + 7*self.b)*n, -self.b*n)
    def __truediv__(self, other): return self * FF(other).inverse()
    def __rtruediv__(self, other): return FF(other) / self
    def __pow__(self, n):
        if n < 0: return self.inverse()**(-n)
        out, base = FF(1), self
        while n:
            if n & 1: out = out*base
            base = base*base; n //= 2
        return out
    def __bool__(self): return bool(self.a or self.b)
    def __eq__(self, other):
        other = FF(other); return self.a == other.a and self.b == other.b
    def encode(self): return [self.a, self.b]
    def __repr__(self): return f'FF({self.a},{self.b})'


class Jet:
    """Value and its twelve exact first derivatives over the residue field."""
    __slots__ = ('value', 'd')
    def __init__(self, value=0, d=None):
        if isinstance(value, Jet): self.value, self.d = value.value, value.d
        else:
            self.value = FF(value)
            self.d = list(d) if d is not None else [FF(0) for _ in range(NVAR)]
    def __add__(self, other):
        other = Jet(other)
        return Jet(self.value+other.value, [a+b for a,b in zip(self.d,other.d)])
    __radd__ = __add__
    def __neg__(self): return Jet(-self.value, [-a for a in self.d])
    def __sub__(self, other): return self + (-Jet(other))
    def __rsub__(self, other): return Jet(other) - self
    def __mul__(self, other):
        other = Jet(other)
        return Jet(self.value*other.value,
                   [a*other.value+self.value*b for a,b in zip(self.d,other.d)])
    __rmul__ = __mul__


def parse(s):
    out = {}
    for term in s.replace('-', '+-').split('+'):
        if not term: continue
        c, e = 1, [0]*8
        for factor in term.split('*'):
            if factor.startswith('-'): c = -c; factor = factor[1:]
            if factor and factor[0] in V:
                name, _, degree = factor.partition('^')
                assert len(name) == 1
                e[V.index(name)] += int(degree or 1)
            else: c *= int(factor)
        e = tuple(e); out[e] = out.get(e, 0) + c
    return {e:c for e,c in out.items() if c}


def binary_mul(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j] = out[i+j] + x*y
    return out


def binary_monomial(e, coords):
    out = [1]
    for n,x in zip(e,coords):
        for _ in range(n): out = binary_mul(out,x)
    return out


def binary_poly(poly, coords):
    out = [0]*4
    for e,c in poly.items():
        term = binary_monomial(e,coords)
        assert len(term) == 4
        out = [a+c*b for a,b in zip(out,term)]
    return out


def normal_values(w):
    u = -(4*w*w+w+10)/(3*w)
    v = -2*(4*w*w+w+10)/(5*(w-2))
    z = (6*w*w-w+20)/(5*(w-2))
    d_s = -10*u/w
    f_s = -(10*v+u*z+v*w+2*u*w+3*u*u*z+6*u*v*w+8*u*w*z+4*v*w*w)
    f_t = -(v*z+2*u*z+2*v*w+6*u*v*z+3*v*v*w+4*u*z*z+8*v*w*z)
    return [u,v,w,z,d_s,0,f_s,f_t,0,0,0,0]


def central_residuals(values, monomials, first):
    u,v,w,z = values[:4]
    coords = [[1,0],[0,1],[u,v],[0,0],[w,z],[0,0],[0,0],[0,0]]
    normal = {outside: values[4+2*k:6+2*k] for k,outside in enumerate(OUTSIDE)}
    result = []
    for e,g in zip(monomials,first):
        row = binary_poly(g,coords)
        outsiders = [j for j in OUTSIDE if e[j]]
        assert outsiders
        if len(outsiders) == 1:
            j = outsiders[0]
            ee = list(e); ee[j] -= 1
            term = binary_mul(binary_monomial(ee,coords),normal[j])
            row = [a+b for a,b in zip(row,term)]
        result.extend(row)
    assert len(result) == 64
    return result, coords


def pivot_rows_columns(matrix):
    a = [[FF(x) for x in row] for row in matrix]
    original_rows = list(range(len(a)))
    r, row_indices, columns = 0, [], []
    for col in range(len(a[0])):
        hit = next((i for i in range(r,len(a)) if a[i][col]),None)
        if hit is None: continue
        a[r],a[hit] = a[hit],a[r]
        original_rows[r],original_rows[hit] = original_rows[hit],original_rows[r]
        row_indices.append(original_rows[r]); columns.append(col)
        pivot = a[r][col]; inv = pivot.inverse()
        for j in range(col,len(a[0])): a[r][j] = a[r][j]*inv
        for i in range(r+1,len(a)):
            c = a[i][col]
            if c:
                for j in range(col,len(a[0])): a[i][j] = a[i][j]-c*a[r][j]
        r += 1
        if r == len(a): break
    return row_indices, columns


def determinant(matrix):
    a = [[FF(x) for x in row] for row in matrix]
    n = len(a); answer = FF(1)
    for k in range(n):
        hit = next((i for i in range(k,n) if a[i][k]),None)
        if hit is None: return FF(0)
        if hit != k: a[k],a[hit] = a[hit],a[k]; answer = -answer
        pivot = a[k][k]; answer = answer*pivot; inv = pivot.inverse()
        for i in range(k+1,n):
            c = a[i][k]*inv
            if c:
                for j in range(k+1,n): a[i][j] = a[i][j]-c*a[k][j]
    return answer


def syzygy_constraints(coords, syzygies):
    matrix = [[FF(0) for _ in range(64)] for _ in range(150)]
    for k,syzygy in enumerate(syzygies):
        for sign,entry in [(1,syzygy['positive']),(-1,syzygy['negative'])]:
            i,j = entry
            for n in range(4):
                matrix[5*k+n][4*i+n] += sign*coords[j][0]
                matrix[5*k+n+1][4*i+n] += sign*coords[j][1]
    return matrix


def exact_candidate_checks(monomials, first):
    w = sp.Symbol('w')
    polynomials = [19*w*w-2*w+40,w**3-16*w*w-10*w-50]
    values = normal_values(w)
    residuals,_ = central_residuals(values,monomials,first)
    result = []
    for polynomial in polynomials:
        p = sp.Poly(polynomial,w,domain=sp.QQ)
        assert p.is_irreducible
        encoded = []
        for value in values:
            numerator, denominator = sp.fraction(sp.cancel(value))
            assert sp.gcd(denominator,p.as_expr()) == 1
            rep = sp.rem(numerator*sp.invert(denominator,p.as_expr(),w),p.as_expr(),w)
            encoded.append(str(rep))
        for value in residuals:
            numerator,denominator = sp.fraction(sp.cancel(value))
            assert sp.rem(numerator,p.as_expr(),w) == 0
            assert sp.gcd(denominator,p.as_expr()) == 1
        boundary = [values[0],values[1],values[2],values[3],
                    values[0]*values[3]-values[1]*values[2]]
        for value in boundary:
            numerator,denominator = sp.fraction(sp.cancel(value))
            assert sp.gcd(numerator,p.as_expr()) == 1
            assert sp.gcd(denominator,p.as_expr()) == 1
        result.append({'minimal_polynomial':str(polynomial),'degree':p.degree(),
                       'irreducible_over_Q':True,'parameter_values_reduced_mod_polynomial':encoded,
                       'all_64_central_residuals_zero_over_Qw':True,
                       'all_four_coordinate_face_intersections_pairwise_distinct':True})
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--only-rational-residues',action='store_true')
    args = ap.parse_args(); start = time.monotonic()
    run = Path(__file__).resolve().parents[1]; repo = run.parents[1]
    output = args.output.resolve()
    assert output.is_relative_to(run) and not output.exists(), 'require fresh run-owned output'
    source = repo/'equations/deformation_data.json'
    exported = repo/'runs/astra-computation-2026-09-08/data/ramified_fibre_coefficients.json'
    data = json.loads(source.read_text()); fibre = json.loads(exported.read_text())
    monomials = [next(iter(parse(s))) for s in data['generator_order']]
    first = [parse(s) for s in data['six_jet_coefficients'][1]]
    named_first = [parse(s) for s in data['first_order_corrections']]
    assert first == named_first, 'source q sign differs; adjust Y formulas explicitly'
    syzygies = fibre['central_linear_syzygies']; assert len(syzygies) == 30
    exact = exact_candidate_checks(monomials,first)
    print('PASS_EXACT_QW_FIRST_ORDER_AND_BOUNDARY_CHECKS',flush=True)
    assert not any((x*x-7*x+28)%101 == 0 for x in range(101))
    roots = [('quadratic-w5',FF(5)),('quadratic-w27',FF(27)),('cubic-w9',FF(9))]
    if not args.only_rational_residues:
        roots += [('cubic-walpha',FF(0,1)),('cubic-w7minusalpha',FF(7,-1))]
    certificates = []
    for name,w in roots:
        assert (19*w*w-2*w+40)*(w**3-16*w*w-10*w-50) == 0
        vals = [FF(x) for x in normal_values(w)]
        u,v,_,z = vals[:4]
        assert all([u,v,w,z,u*z-v*w])
        jets = [Jet(x,[FF(int(i==j)) for j in range(NVAR)]) for i,x in enumerate(vals)]
        residuals,_ = central_residuals(jets,monomials,first)
        residuals = [Jet(x) for x in residuals]
        assert all(not x.value for x in residuals)
        jac = [x.d for x in residuals]
        _,coords = central_residuals(vals,monomials,first)
        constraints = syzygy_constraints(coords,syzygies)
        rows,columns = pivot_rows_columns(constraints)
        assert len(rows) == len(columns) == 52
        selected = [i for i in range(64) if i not in columns]
        assert len(selected) == 12
        td = determinant([[constraints[i][j] for j in columns] for i in rows])
        jd = determinant([jac[i] for i in selected])
        assert td and jd, (name,td,jd)
        # Differentiate exact E*R=0 at E=0: T*J must vanish. This catches
        # matrix ordering/sign mistakes independently of the two ranks.
        for row in constraints:
            for j in range(NVAR):
                assert sum((row[i]*jac[i][j] for i in range(64)),FF(0)) == 0
        cert = {'name':name,'w_residue':w.encode(),
                'parameter_residues':[x.encode() for x in vals],
                'residue_field_degree':1 if not w.b else 2,
                'syzygy_matrix_shape':[150,64],'syzygy_rank':52,
                'syzygy_minor_rows_zero_based':rows,'syzygy_minor_columns_zero_based':columns,
                'syzygy_minor_determinant':td.encode(),
                'selected_residual_indices_zero_based':selected,
                'selected_residual_generator_binary_power_pairs':[[i//4,i%4] for i in selected],
                'selected_jacobian_determinant':jd.encode(),
                'all64_first_order_residuals_zero':True,'syzygy_times_jacobian_zero':True,
                'boundary_units':[x.encode() for x in [u,v,w,z,u*z-v*w]],
                'elapsed_seconds':round(time.monotonic()-start,3)}
        certificates.append(cert)
        print('PASS_LINE',name,'SYZYGY_DET',td,'JACOBIAN_DET',jd,
              'seconds',round(time.monotonic()-start,3),flush=True)
    result = {'status':'COMPUTER-CERTIFIED first-order lines, full-equation closure minors, Hensel Jacobians',
              'prime':101,'quadratic_residue_extension_polynomial':'alpha^2-7*alpha+28',
              'facet':'abce','grassmann_chart':'a=s,b=t,c=u*s+v*t,e=w*s+z*t; (d,f,g,h)=pi*(Y_s*s+Y_t*t)',
              'parameter_order':PARAMETERS,'binary_coefficient_order':'s^3,s^2*t,s*t^2,t^3',
              'exact_candidate_fields':exact,'branches':certificates,
              'first_order_sign_relative_to_actual_sixjet':1,
              'proof_dependencies':['audited exact selected-fibre cubics and FR=0',
                 'original R central syzygies in the stated ordering',
                 'Hensel lemma for selected12 residuals divided by pi',
                 'unit52 syzygy minor forces all64 residuals',
                 'smooth CY fibre for N_line=O(-1)+O(-1) conclusion'],
              'input_hashes':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [source,exported,Path(__file__)]},
              'elapsed_seconds':round(time.monotonic()-start,3)}
    output.mkdir(parents=True)
    (output/'line_certificates.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS_ALL_LINE_CERTIFICATES',output,flush=True)


if __name__ == '__main__': main()
