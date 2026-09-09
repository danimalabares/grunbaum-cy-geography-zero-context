#!/usr/bin/env python3
"""Export a CERTIFIED modular rational model as executable Macaulay2 input.

Requires exact closure output; never accepts a jet checkpoint. The default
is a generic fibre over F_p(q), NOT a characteristic-zero fibre. --value
specializes q but demands separate dimension/smoothness checks afterwards.
"""
import argparse,json,os
from pathlib import Path
from build_fixed_chart import F0,FWORDS,name

RUN=Path(__file__).resolve().parents[1]

def render_m2(model,chart,value=None):
    """Render polynomial monomials with explicit multiplication signs."""
    p=model['prime']
    def poly(seq): return '('+'+'.join(f'{x}*q^{i}' for i,x in enumerate(seq) if x)+')' if any(seq) else '0'
    den=poly(model['denominator'])
    if value is not None:
        assert sum(x*pow(value,i,p) for i,x in enumerate(model['denominator']))%p
    z=[]
    for i in range(291):
        numerator=poly([r[i] for r in model['z_numerator']])
        z.append(f'({numerator}/{den})' if numerator!='0' else '0')
    lookup={(i,tuple(m)):k for k,O in enumerate(chart['coefficient_orbits']) for i,m in O}
    tails=[tuple(m) for m in chart['tail_monomials']]
    text='-- Certified MODULAR rational-family input. Read the separate smoothness/spread certificate.\n'
    if value is None: text+=f'Qq=ZZ/{p}[q]; K=frac Qq; S=K[a,b,c,d,e,f,g,h];\n'
    else: text+=f'K=ZZ/{p}; q=sub({value},K); S=K[a,b,c,d,e,f,g,h];\n'
    generators=[]
    for i in range(16):
        terms=[name(F0[i])]+[f'{z[lookup[i,m]]}*{name(m)}' for m in tails if z[lookup[i,m]]!='0']
        generators.append('+'.join(terms))
    text+='F=matrix{{'+','.join(generators)+'}};\nI=ideal F;\n'
    return text

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('model',type=Path)
    ap.add_argument('--value',type=int)
    a=ap.parse_args(); model=json.loads(a.model.read_text())
    assert model['FR_identity_all_coefficients_zero'] is True
    assert model['matches_selected_normalized_sixjet'] is True, 'synthetic controls are not smoothing inputs'
    p=model['prime']; chart=json.loads((RUN/'data/fixed_chart.json').read_text())
    text=render_m2(model,chart,a.value)
    out=Path(os.environ.get('GS_RUN_OUTPUT',RUN/'data/exported_model')); out.mkdir(parents=True,exist_ok=True)
    dest=out/f'fibre_p{p}_{"generic" if a.value is None else a.value}.m2'
    if dest.exists(): assert dest.read_text()==text
    else: dest.write_text(text)
    print(dest)

if __name__=='__main__': main()
