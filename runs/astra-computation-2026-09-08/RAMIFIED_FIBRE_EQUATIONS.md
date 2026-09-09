# The actual sixteen cubic equations: ramified algebraic-number presentation

**COMPUTER-CERTIFIED finite presentation.** The coefficient data are in
`data/ramified_fibre_coefficients.json`. They specify 271 algebraic
unknowns, not an uncomputed infinite series: pi and theta_1,...,theta_270.
Smoothness uses the reviewed ramified transport of the original six-jet
certificates; see `RAMIFIED_POINT_CONSTRUCTION.md` and the final review.

## Coefficient field and unique root

Take K=Q_101(pi), pi^7=101. Put O=Z_101[pi]. For each of the 270
selected entries below impose the finite bordered determinant equation

    det([[A_r(lambda), B_r(lambda)[:,j]],
         [C_r(lambda)[i,:], D_r(lambda)[i,j]]]) = 0.

Here A_r=I+A_minus_identity. The three shared matrices have A sizes
21, 13, and 32, so each determinant has size at most 33. All rational
linear-form factors and all 270 row/column selections are explicit
in the JSON. This determinant representation is a finite polynomial
equation; no determinant expansion or syzygy unknown is necessary.

Choose the unique solution with theta_i in pi O for all i.
The selected 270-by-270 Jacobian determinant is 19 modulo 101,
so the root exists uniquely by Hensel lifting. All displayed rational
denominators are units at 101. The coefficient field is
L=Q(pi,theta_1,...,theta_270) inside K; its degree is **not** asserted
to be 7. Smoothness descends from K to this number field.

## Exact indexing of the algebraic coefficients

In every polynomial below, lambda_j denotes the following exact
algebraic number. For k=1,...,270 set lambda_(d_k)=theta_k, where
the ordered list (d_1,...,d_270), with one-based indices, is:

```text
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,165,166,167,168,169,170,171,172,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,198,199,200,201,202,203,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,232,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,258,259,260,261,262,264,265,266,268,269,270,271,272,273,274,275,276,278,279,280,281,283,284,285,287,288,289,290,291
```

The other 21 lambda values are these ORIGINAL six-jet polynomials,
not the linear-path experiment:

```text
lambda_38 = (5)*pi + (8)*pi^4 + (135295/9)*pi^5 + (-26469644/81)*pi^6
lambda_39 = (4)*pi + (-340)*pi^4 + (32642/3)*pi^5 + (-2520115/18)*pi^6
lambda_47 = (3)*pi + (-90)*pi^4 + (17808)*pi^5 + (-6675625/54)*pi^6
lambda_65 = (2)*pi + (-1715/3)*pi^4 + (25199/6)*pi^5 + (-273045/2)*pi^6
lambda_90 = (1)*pi + (-300)*pi^4 + (111097/9)*pi^5 + (436345/4)*pi^6
lambda_164 = (8)*pi + (-27/2)*pi^3 + (415/18)*pi^4 + (-8475817/216)*pi^5 + (26290705/72)*pi^6
lambda_173 = (9)*pi + (-150)*pi^3 + (28765/27)*pi^4 + (-9693185/216)*pi^5 + (3667981205/7776)*pi^6
lambda_197 = (60)*pi^3 + (-10790/9)*pi^4 + (-280067/54)*pi^5 + (12604951/36)*pi^6
lambda_204 = (-9/2)*pi^2 + (160/9)*pi^3 + (42601/36)*pi^4 + (-18407/12)*pi^5 + (-566198365/2592)*pi^6
lambda_230 = (6)*pi + (-5820)*pi^5 + (3164510/9)*pi^6
lambda_231 = (7)*pi + (17010)*pi^5 + (-718385)*pi^6
lambda_233 = (-572/3)*pi^3 + (-40429/18)*pi^4 + (366559/9)*pi^5 + (1001600299/1944)*pi^6
lambda_234 = (-4)*pi^2 + (-43/6)*pi^3 + (72247/36)*pi^4 + (14331725/162)*pi^5 + (-992031709/972)*pi^6
lambda_235 = (796/3)*pi^3 + (86095/18)*pi^4 + (2639563/144)*pi^5 + (-308462077/1296)*pi^6
lambda_256 = (-15)*pi^2 + (-175/3)*pi^3 + (-71995/36)*pi^4 + (2787280/81)*pi^5 + (250050475/3888)*pi^6
lambda_257 = (10)*pi^2 + (-180)*pi^3 + (-130495/54)*pi^4 + (7182065/216)*pi^5 + (-356918035/972)*pi^6
lambda_263 = (10)*pi + (125/3)*pi^3 + (-5075/6)*pi^4 + (235465/12)*pi^5 + (47606480/243)*pi^6
lambda_267 = (230/3)*pi^3 + (3125/3)*pi^4 + (3712160/81)*pi^5 + (-205153025/1944)*pi^6
lambda_277 = (-9/2)*pi^2 + (60)*pi^3 + (-5567/12)*pi^4 + (6959075/216)*pi^5 + (-7607521/27)*pi^6
lambda_282 = (-10/3)*pi^2 + (-357/4)*pi^3 + (-47315/27)*pi^4 + (444485/27)*pi^5 + (-57300253/486)*pi^6
lambda_286 = (-5)*pi^2 + (145/3)*pi^3 + (6305/36)*pi^4 + (-3663875/648)*pi^5 + (-198076195/972)*pi^6
```

## All sixteen cubic equations

The fibre is X=V(F_1,...,F_16) in P^7_L with coordinates a,...,h.
Multiplication and exponents in the following code blocks have
their ordinary polynomial meanings. Every summand is displayed.

### F_1

```text
F_1 = a*b*f
  + lambda_1*(h^3) + lambda_2*(g*h^2) + lambda_3*(g^2*h)
  + lambda_4*(g^3) + lambda_5*(f*h^2) + lambda_6*(f*g*h)
  + lambda_7*(f*g^2) + lambda_8*(f^2*h) + lambda_9*(f^2*g)
  + lambda_10*(f^3) + lambda_11*(e*h^2) + lambda_12*(e*g*h)
  + lambda_13*(e*g^2) + lambda_14*(e*f*h) + lambda_15*(e*f^2)
  + lambda_16*(e^2*h) + lambda_17*(e^2*g) + lambda_18*(e^2*f)
  + lambda_19*(e^3) + lambda_20*(d*h^2) + lambda_21*(d*g*h)
  + lambda_22*(d*g^2) + lambda_23*(d*f*g) + lambda_24*(d*f^2)
  + lambda_25*(d*e*h) + lambda_26*(d*e*g) + lambda_27*(d*e^2)
  + lambda_28*(d^2*h) + lambda_29*(d^2*g) + lambda_30*(d^2*f)
  + lambda_31*(d^2*e) + lambda_32*(d^3) + lambda_33*(c*h^2)
  + lambda_34*(c*g*h) + lambda_35*(c*g^2) + lambda_36*(c*f*g)
  + lambda_37*(c*f^2) + lambda_38*(c*e*f) + lambda_39*(c*e^2)
  + lambda_40*(c*d*h) + lambda_41*(c*d*g) + lambda_42*(c*d*f)
  + lambda_43*(c*d^2) + lambda_44*(c^2*h) + lambda_45*(c^2*g)
  + lambda_46*(c^2*f) + lambda_47*(c^2*e) + lambda_48*(c^2*d)
  + lambda_49*(c^3) + lambda_50*(b*h^2) + lambda_51*(b*g*h)
  + lambda_52*(b*g^2) + lambda_53*(b*f*h) + lambda_54*(b*f*g)
  + lambda_55*(b*f^2) + lambda_56*(b*e*h) + lambda_57*(b*e*f)
  + lambda_58*(b*e^2) + lambda_59*(b*d*h) + lambda_60*(b*d*e)
  + lambda_61*(b*d^2) + lambda_62*(b*c*h) + lambda_63*(b*c*g)
  + lambda_64*(b*c*f) + lambda_65*(b*c*e) + lambda_66*(b*c*d)
  + lambda_67*(b*c^2) + lambda_68*(b^2*h) + lambda_69*(b^2*g)
  + lambda_70*(b^2*f) + lambda_71*(b^2*e) + lambda_72*(b^2*d)
  + lambda_73*(b^2*c) + lambda_74*(b^3) + lambda_75*(a*h^2)
  + lambda_76*(a*g*h) + lambda_77*(a*g^2) + lambda_78*(a*f*h)
  + lambda_79*(a*f*g) + lambda_80*(a*f^2) + lambda_81*(a*e*h)
  + lambda_82*(a*e*g) + lambda_83*(a*e*f) + lambda_84*(a*e^2)
  + lambda_85*(a*d*g) + lambda_86*(a*d*f) + lambda_87*(a*d*e)
  + lambda_88*(a*d^2) + lambda_89*(a*c*f) + lambda_90*(a*c*e)
  + lambda_91*(a*c*d) + lambda_92*(a*c^2) + lambda_93*(a*b*e)
  + lambda_94*(a*b*d) + lambda_95*(a*b*c) + lambda_96*(a*b^2)
  + lambda_97*(a^2*h) + lambda_98*(a^2*g) + lambda_99*(a^2*f)
  + lambda_100*(a^2*e) + lambda_101*(a^2*d) + lambda_102*(a^2*c)
  + lambda_103*(a^2*b) + lambda_104*(a^3)
```

### F_2

```text
F_2 = a*b*g
  + lambda_105*(h^3+e^3) + lambda_106*(g*h^2+a*e^2) + lambda_107*(g^2*h+a^2*e)
  + lambda_108*(g^3+a^3) + lambda_109*(f*h^2+d*e^2) + lambda_110*(f*g*h+a*d*e)
  + lambda_111*(f*g^2+a^2*d) + lambda_112*(f^2*h+d^2*e) + lambda_113*(f^2*g+a*d^2)
  + lambda_114*(f^3+d^3) + lambda_115*(e*h^2+e^2*h) + lambda_116*(e*g*h+a*e*h)
  + lambda_117*(e*g^2+a^2*h) + lambda_118*(e*f*h+d*e*h) + lambda_119*(e*f^2+d^2*h)
  + lambda_120*(e^2*g+a*h^2) + lambda_121*(e^2*f+d*h^2) + lambda_122*(d*g*h+a*e*f)
  + lambda_123*(d*g^2+a^2*f) + lambda_124*(d*f*g+a*d*f) + lambda_125*(d*f^2+d^2*f)
  + lambda_126*(d*e*g+a*f*h) + lambda_127*(d^2*g+a*f^2) + lambda_128*(c*h^2+c*e^2)
  + lambda_129*(c*g*h+a*c*e) + lambda_130*(c*g^2+a^2*c) + lambda_131*(c*f*g+a*c*d)
  + lambda_132*(c*f^2+c*d^2) + lambda_133*(c*e*f+c*d*h) + lambda_134*(c*d*g+a*c*f)
  + lambda_135*(c*d*f) + lambda_136*(c^2*h+c^2*e) + lambda_137*(c^2*g+a*c^2)
  + lambda_138*(c^2*f+c^2*d) + lambda_139*(c^3) + lambda_140*(b*h^2+b*e^2)
  + lambda_141*(b*g*h+a*b*e) + lambda_142*(b*g^2+a^2*b) + lambda_143*(b*f*h+b*d*e)
  + lambda_144*(b*f*g+a*b*d) + lambda_145*(b*f^2+b*d^2) + lambda_146*(b*e*h)
  + lambda_147*(b*e*f+b*d*h) + lambda_148*(b*c*h+b*c*e) + lambda_149*(b*c*g+a*b*c)
  + lambda_150*(b*c*f+b*c*d) + lambda_151*(b*c^2) + lambda_152*(b^2*h+b^2*e)
  + lambda_153*(b^2*g+a*b^2) + lambda_154*(b^2*f+b^2*d) + lambda_155*(b^2*c)
  + lambda_156*(b^3) + lambda_157*(a*g*h+a*e*g) + lambda_158*(a*g^2+a^2*g)
  + lambda_159*(a*f*g+a*d*g)
```

### F_3

```text
F_3 = a*b*h
  + lambda_160*(h^3+b^3) + lambda_161*(g*h^2+b^2*c) + lambda_162*(g^2*h+b*c^2)
  + lambda_163*(g^3+c^3) + lambda_164*(f*h^2+b^2*d) + lambda_165*(f*g*h+b*c*d)
  + lambda_166*(f*g^2+c^2*d) + lambda_167*(f^2*h+b*d^2) + lambda_168*(f^2*g+c*d^2)
  + lambda_169*(f^3+d^3) + lambda_170*(e*h^2+b^2*e) + lambda_171*(e*g*h+b*c*e)
  + lambda_172*(e*g^2+c^2*e) + lambda_173*(e*f*h+b*d*e) + lambda_174*(e*f^2+d^2*e)
  + lambda_175*(e^2*h+b*e^2) + lambda_176*(e^2*g+c*e^2) + lambda_177*(e^2*f+d*e^2)
  + lambda_178*(e^3) + lambda_179*(d*h^2+b^2*f) + lambda_180*(d*g*h+b*c*f)
  + lambda_181*(d*g^2+c^2*f) + lambda_182*(d*f*g+c*d*f) + lambda_183*(d*f^2+d^2*f)
  + lambda_184*(d*e*h+b*e*f) + lambda_185*(d*e*g+c*e*f) + lambda_186*(d^2*h+b*f^2)
  + lambda_187*(d^2*g+c*f^2) + lambda_188*(c*h^2+b^2*g) + lambda_189*(c*g*h+b*c*g)
  + lambda_190*(c*g^2+c^2*g) + lambda_191*(c*f*g+c*d*g) + lambda_192*(c*d*h+b*f*g)
  + lambda_193*(c^2*h+b*g^2) + lambda_194*(b*h^2+b^2*h) + lambda_195*(b*g*h+b*c*h)
  + lambda_196*(b*f*h+b*d*h) + lambda_197*(b*e*h) + lambda_198*(a*h^2+a*b^2)
  + lambda_199*(a*g*h+a*b*c) + lambda_200*(a*g^2+a*c^2) + lambda_201*(a*f*h+a*b*d)
  + lambda_202*(a*f*g+a*c*d) + lambda_203*(a*f^2+a*d^2) + lambda_204*(a*e*h+a*b*e)
  + lambda_205*(a*e*g+a*c*e) + lambda_206*(a*e*f+a*d*e) + lambda_207*(a*e^2)
  + lambda_208*(a*d*g+a*c*f) + lambda_209*(a*d*f) + lambda_210*(a^2*h+a^2*b)
  + lambda_211*(a^2*g+a^2*c) + lambda_212*(a^2*f+a^2*d) + lambda_213*(a^2*e)
  + lambda_214*(a^3)
```

### F_4

```text
F_4 = a*c*g
  + lambda_215*(h^3+e^3+b^3) + lambda_216*(g*h^2+b^2*c+a*e^2) + lambda_217*(g^2*h+b*c^2+a^2*e)
  + lambda_218*(g^3+c^3+a^3) + lambda_219*(f*h^2+e^2*f+d*h^2+d*e^2+b^2*f+b^2*d) + lambda_220*(f*g*h+d*g*h+b*c*f+b*c*d+a*e*f+a*d*e)
  + lambda_221*(f*g^2+d*g^2+c^2*f+c^2*d+a^2*f+a^2*d) + lambda_222*(f^2*h+e*f^2+d^2*h+d^2*e+b*f^2+b*d^2) + lambda_223*(f^2*g+d^2*g+c*f^2+c*d^2+a*f^2+a*d^2)
  + lambda_224*(f^3+d^3) + lambda_225*(e*h^2+e^2*h+b*h^2+b*e^2+b^2*h+b^2*e) + lambda_226*(e*g*h+b*g*h+b*c*h+b*c*e+a*e*h+a*b*e)
  + lambda_227*(e*g^2+c^2*h+c^2*e+b*g^2+a^2*h+a^2*b) + lambda_228*(e*f*h+d*e*h+b*f*h+b*e*f+b*d*h+b*d*e) + lambda_229*(e^2*g+c*h^2+c*e^2+b^2*g+a*h^2+a*b^2)
  + lambda_230*(d*f*g+c*d*f+a*d*f) + lambda_231*(d*f^2+d^2*f) + lambda_232*(d*e*g+c*e*f+c*d*h+b*f*g+a*f*h+a*b*d)
  + lambda_233*(c*g*h+b*c*g+a*g*h+a*e*g+a*c*e+a*b*c) + lambda_234*(c*g^2+c^2*g+a*g^2+a*c^2+a^2*g+a^2*c) + lambda_235*(c*f*g+c*d*g+a*f*g+a*d*g+a*c*f+a*c*d)
  + lambda_236*(b*e*h)
```

### F_5

```text
F_5 = a*c*h
  + lambda_105*(e^3+b^3) + lambda_106*(b^2*c+a*e^2) + lambda_107*(b*c^2+a^2*e)
  + lambda_108*(c^3+a^3) + lambda_109*(e^2*f+b^2*d) + lambda_110*(b*c*d+a*e*f)
  + lambda_111*(c^2*d+a^2*f) + lambda_112*(e*f^2+b*d^2) + lambda_113*(c*d^2+a*f^2)
  + lambda_114*(f^3+d^3) + lambda_115*(b*e^2+b^2*e) + lambda_116*(b*c*e+a*b*e)
  + lambda_117*(c^2*e+a^2*b) + lambda_118*(b*e*f+b*d*e) + lambda_119*(d^2*e+b*f^2)
  + lambda_120*(c*e^2+a*b^2) + lambda_121*(d*e^2+b^2*f) + lambda_122*(b*c*f+a*d*e)
  + lambda_123*(c^2*f+a^2*d) + lambda_124*(c*d*f+a*d*f) + lambda_125*(d*f^2+d^2*f)
  + lambda_126*(c*e*f+a*b*d) + lambda_127*(c*f^2+a*d^2) + lambda_128*(e^2*g+b^2*g)
  + lambda_129*(b*c*g+a*e*g) + lambda_130*(c^2*g+a^2*g) + lambda_131*(c*d*g+a*f*g)
  + lambda_132*(f^2*g+d^2*g) + lambda_133*(d*e*g+b*f*g) + lambda_134*(c*f*g+a*d*g)
  + lambda_135*(d*f*g) + lambda_136*(e*g^2+b*g^2) + lambda_137*(c*g^2+a*g^2)
  + lambda_138*(f*g^2+d*g^2) + lambda_139*(g^3) + lambda_140*(e^2*h+b^2*h)
  + lambda_141*(b*c*h+a*e*h) + lambda_142*(c^2*h+a^2*h) + lambda_143*(e*f*h+b*d*h)
  + lambda_144*(c*d*h+a*f*h) + lambda_145*(f^2*h+d^2*h) + lambda_146*(b*e*h)
  + lambda_147*(d*e*h+b*f*h) + lambda_148*(e*g*h+b*g*h) + lambda_149*(c*g*h+a*g*h)
  + lambda_150*(f*g*h+d*g*h) + lambda_151*(g^2*h) + lambda_152*(e*h^2+b*h^2)
  + lambda_153*(c*h^2+a*h^2) + lambda_154*(f*h^2+d*h^2) + lambda_155*(g*h^2)
  + lambda_156*(h^3) + lambda_157*(a*c*e+a*b*c) + lambda_158*(a*c^2+a^2*c)
  + lambda_159*(a*c*f+a*c*d)
```

### F_6

```text
F_6 = a*d*h
  + lambda_1*(b^3) + lambda_2*(b^2*c) + lambda_3*(b*c^2)
  + lambda_4*(c^3) + lambda_5*(b^2*d) + lambda_6*(b*c*d)
  + lambda_7*(c^2*d) + lambda_8*(b*d^2) + lambda_9*(c*d^2)
  + lambda_10*(d^3) + lambda_11*(b^2*e) + lambda_12*(b*c*e)
  + lambda_13*(c^2*e) + lambda_14*(b*d*e) + lambda_15*(d^2*e)
  + lambda_16*(b*e^2) + lambda_17*(c*e^2) + lambda_18*(d*e^2)
  + lambda_19*(e^3) + lambda_20*(b^2*f) + lambda_21*(b*c*f)
  + lambda_22*(c^2*f) + lambda_23*(c*d*f) + lambda_24*(d^2*f)
  + lambda_25*(b*e*f) + lambda_26*(c*e*f) + lambda_27*(e^2*f)
  + lambda_28*(b*f^2) + lambda_29*(c*f^2) + lambda_30*(d*f^2)
  + lambda_31*(e*f^2) + lambda_32*(f^3) + lambda_33*(b^2*g)
  + lambda_34*(b*c*g) + lambda_35*(c^2*g) + lambda_36*(c*d*g)
  + lambda_37*(d^2*g) + lambda_38*(d*e*g) + lambda_39*(e^2*g)
  + lambda_40*(b*f*g) + lambda_41*(c*f*g) + lambda_42*(d*f*g)
  + lambda_43*(f^2*g) + lambda_44*(b*g^2) + lambda_45*(c*g^2)
  + lambda_46*(d*g^2) + lambda_47*(e*g^2) + lambda_48*(f*g^2)
  + lambda_49*(g^3) + lambda_50*(b^2*h) + lambda_51*(b*c*h)
  + lambda_52*(c^2*h) + lambda_53*(b*d*h) + lambda_54*(c*d*h)
  + lambda_55*(d^2*h) + lambda_56*(b*e*h) + lambda_57*(d*e*h)
  + lambda_58*(e^2*h) + lambda_59*(b*f*h) + lambda_60*(e*f*h)
  + lambda_61*(f^2*h) + lambda_62*(b*g*h) + lambda_63*(c*g*h)
  + lambda_64*(d*g*h) + lambda_65*(e*g*h) + lambda_66*(f*g*h)
  + lambda_67*(g^2*h) + lambda_68*(b*h^2) + lambda_69*(c*h^2)
  + lambda_70*(d*h^2) + lambda_71*(e*h^2) + lambda_72*(f*h^2)
  + lambda_73*(g*h^2) + lambda_74*(h^3) + lambda_75*(a*b^2)
  + lambda_76*(a*b*c) + lambda_77*(a*c^2) + lambda_78*(a*b*d)
  + lambda_79*(a*c*d) + lambda_80*(a*d^2) + lambda_81*(a*b*e)
  + lambda_82*(a*c*e) + lambda_83*(a*d*e) + lambda_84*(a*e^2)
  + lambda_85*(a*c*f) + lambda_86*(a*d*f) + lambda_87*(a*e*f)
  + lambda_88*(a*f^2) + lambda_89*(a*d*g) + lambda_90*(a*e*g)
  + lambda_91*(a*f*g) + lambda_92*(a*g^2) + lambda_93*(a*e*h)
  + lambda_94*(a*f*h) + lambda_95*(a*g*h) + lambda_96*(a*h^2)
  + lambda_97*(a^2*b) + lambda_98*(a^2*c) + lambda_99*(a^2*d)
  + lambda_100*(a^2*e) + lambda_101*(a^2*f) + lambda_102*(a^2*g)
  + lambda_103*(a^2*h) + lambda_104*(a^3)
```

### F_7

```text
F_7 = b*d*f
  + lambda_237*(h^3+e^3) + lambda_238*(g*h^2+a*e^2) + lambda_239*(g^2*h+a^2*e)
  + lambda_240*(g^3+a^3) + lambda_241*(f*h^2+d*e^2) + lambda_242*(f*g*h+a*d*e)
  + lambda_243*(f*g^2+a^2*d) + lambda_244*(f^2*h+d^2*e) + lambda_245*(f^2*g+a*d^2)
  + lambda_246*(f^3+d^3) + lambda_247*(e*h^2+e^2*h) + lambda_248*(e*g*h+a*e*h)
  + lambda_249*(e*g^2+a^2*h) + lambda_250*(e*f*h+d*e*h) + lambda_251*(e*f^2+d^2*h)
  + lambda_252*(e^2*g+a*h^2) + lambda_253*(e^2*f+d*h^2) + lambda_254*(d*g*h+a*e*f)
  + lambda_255*(d*g^2+a^2*f) + lambda_256*(d*f*g+a*d*f) + lambda_257*(d*f^2+d^2*f)
  + lambda_258*(d*e*g+a*f*h) + lambda_259*(d^2*g+a*f^2) + lambda_260*(c*h^2+c*e^2)
  + lambda_261*(c*g*h+a*c*e) + lambda_262*(c*g^2+a^2*c) + lambda_263*(c*f*g+a*c*d)
  + lambda_264*(c*f^2+c*d^2) + lambda_265*(c*e*f+c*d*h) + lambda_266*(c*d*g+a*c*f)
  + lambda_267*(c*d*f) + lambda_268*(c^2*h+c^2*e) + lambda_269*(c^2*g+a*c^2)
  + lambda_270*(c^2*f+c^2*d) + lambda_271*(c^3) + lambda_272*(b*h^2+b*e^2)
  + lambda_273*(b*g*h+a*b*e) + lambda_274*(b*g^2+a^2*b) + lambda_275*(b*f*h+b*d*e)
  + lambda_276*(b*f*g+a*b*d) + lambda_277*(b*f^2+b*d^2) + lambda_278*(b*e*h)
  + lambda_279*(b*e*f+b*d*h) + lambda_280*(b*c*h+b*c*e) + lambda_281*(b*c*g+a*b*c)
  + lambda_282*(b*c*f+b*c*d) + lambda_283*(b*c^2) + lambda_284*(b^2*h+b^2*e)
  + lambda_285*(b^2*g+a*b^2) + lambda_286*(b^2*f+b^2*d) + lambda_287*(b^2*c)
  + lambda_288*(b^3) + lambda_289*(a*g*h+a*e*g) + lambda_290*(a*g^2+a^2*g)
  + lambda_291*(a*f*g+a*d*g)
```

### F_8

```text
F_8 = b*d*g
  + lambda_1*(e^3) + lambda_2*(a*e^2) + lambda_3*(a^2*e)
  + lambda_4*(a^3) + lambda_5*(d*e^2) + lambda_6*(a*d*e)
  + lambda_7*(a^2*d) + lambda_8*(d^2*e) + lambda_9*(a*d^2)
  + lambda_10*(d^3) + lambda_11*(e^2*h) + lambda_12*(a*e*h)
  + lambda_13*(a^2*h) + lambda_14*(d*e*h) + lambda_15*(d^2*h)
  + lambda_16*(e*h^2) + lambda_17*(a*h^2) + lambda_18*(d*h^2)
  + lambda_19*(h^3) + lambda_20*(e^2*f) + lambda_21*(a*e*f)
  + lambda_22*(a^2*f) + lambda_23*(a*d*f) + lambda_24*(d^2*f)
  + lambda_25*(e*f*h) + lambda_26*(a*f*h) + lambda_27*(f*h^2)
  + lambda_28*(e*f^2) + lambda_29*(a*f^2) + lambda_30*(d*f^2)
  + lambda_31*(f^2*h) + lambda_32*(f^3) + lambda_33*(c*e^2)
  + lambda_34*(a*c*e) + lambda_35*(a^2*c) + lambda_36*(a*c*d)
  + lambda_37*(c*d^2) + lambda_38*(c*d*h) + lambda_39*(c*h^2)
  + lambda_40*(c*e*f) + lambda_41*(a*c*f) + lambda_42*(c*d*f)
  + lambda_43*(c*f^2) + lambda_44*(c^2*e) + lambda_45*(a*c^2)
  + lambda_46*(c^2*d) + lambda_47*(c^2*h) + lambda_48*(c^2*f)
  + lambda_49*(c^3) + lambda_50*(b*e^2) + lambda_51*(a*b*e)
  + lambda_52*(a^2*b) + lambda_53*(b*d*e) + lambda_54*(a*b*d)
  + lambda_55*(b*d^2) + lambda_56*(b*e*h) + lambda_57*(b*d*h)
  + lambda_58*(b*h^2) + lambda_59*(b*e*f) + lambda_60*(b*f*h)
  + lambda_61*(b*f^2) + lambda_62*(b*c*e) + lambda_63*(a*b*c)
  + lambda_64*(b*c*d) + lambda_65*(b*c*h) + lambda_66*(b*c*f)
  + lambda_67*(b*c^2) + lambda_68*(b^2*e) + lambda_69*(a*b^2)
  + lambda_70*(b^2*d) + lambda_71*(b^2*h) + lambda_72*(b^2*f)
  + lambda_73*(b^2*c) + lambda_74*(b^3) + lambda_75*(e^2*g)
  + lambda_76*(a*e*g) + lambda_77*(a^2*g) + lambda_78*(d*e*g)
  + lambda_79*(a*d*g) + lambda_80*(d^2*g) + lambda_81*(e*g*h)
  + lambda_82*(a*g*h) + lambda_83*(d*g*h) + lambda_84*(g*h^2)
  + lambda_85*(a*f*g) + lambda_86*(d*f*g) + lambda_87*(f*g*h)
  + lambda_88*(f^2*g) + lambda_89*(c*d*g) + lambda_90*(c*g*h)
  + lambda_91*(c*f*g) + lambda_92*(c^2*g) + lambda_93*(b*g*h)
  + lambda_94*(b*f*g) + lambda_95*(b*c*g) + lambda_96*(b^2*g)
  + lambda_97*(e*g^2) + lambda_98*(a*g^2) + lambda_99*(d*g^2)
  + lambda_100*(g^2*h) + lambda_101*(f*g^2) + lambda_102*(c*g^2)
  + lambda_103*(b*g^2) + lambda_104*(g^3)
```

### F_9

```text
F_9 = b*e*g
  + lambda_160*(e^3+b^3) + lambda_161*(b^2*c+a*e^2) + lambda_162*(b*c^2+a^2*e)
  + lambda_163*(c^3+a^3) + lambda_164*(d*e^2+b^2*f) + lambda_165*(b*c*f+a*d*e)
  + lambda_166*(c^2*f+a^2*d) + lambda_167*(d^2*e+b*f^2) + lambda_168*(c*f^2+a*d^2)
  + lambda_169*(f^3+d^3) + lambda_170*(e^2*h+b^2*h) + lambda_171*(b*c*h+a*e*h)
  + lambda_172*(c^2*h+a^2*h) + lambda_173*(d*e*h+b*f*h) + lambda_174*(f^2*h+d^2*h)
  + lambda_175*(e*h^2+b*h^2) + lambda_176*(c*h^2+a*h^2) + lambda_177*(f*h^2+d*h^2)
  + lambda_178*(h^3) + lambda_179*(e^2*f+b^2*d) + lambda_180*(b*c*d+a*e*f)
  + lambda_181*(c^2*d+a^2*f) + lambda_182*(c*d*f+a*d*f) + lambda_183*(d*f^2+d^2*f)
  + lambda_184*(e*f*h+b*d*h) + lambda_185*(c*d*h+a*f*h) + lambda_186*(e*f^2+b*d^2)
  + lambda_187*(c*d^2+a*f^2) + lambda_188*(c*e^2+a*b^2) + lambda_189*(a*c*e+a*b*c)
  + lambda_190*(a*c^2+a^2*c) + lambda_191*(a*c*f+a*c*d) + lambda_192*(c*e*f+a*b*d)
  + lambda_193*(c^2*e+a^2*b) + lambda_194*(b*e^2+b^2*e) + lambda_195*(b*c*e+a*b*e)
  + lambda_196*(b*e*f+b*d*e) + lambda_197*(b*e*h) + lambda_198*(e^2*g+b^2*g)
  + lambda_199*(b*c*g+a*e*g) + lambda_200*(c^2*g+a^2*g) + lambda_201*(d*e*g+b*f*g)
  + lambda_202*(c*f*g+a*d*g) + lambda_203*(f^2*g+d^2*g) + lambda_204*(e*g*h+b*g*h)
  + lambda_205*(c*g*h+a*g*h) + lambda_206*(f*g*h+d*g*h) + lambda_207*(g*h^2)
  + lambda_208*(c*d*g+a*f*g) + lambda_209*(d*f*g) + lambda_210*(e*g^2+b*g^2)
  + lambda_211*(c*g^2+a*g^2) + lambda_212*(f*g^2+d*g^2) + lambda_213*(g^2*h)
  + lambda_214*(g^3)
```

### F_10

```text
F_10 = c*d*e
  + lambda_1*(h^3) + lambda_2*(g*h^2) + lambda_3*(g^2*h)
  + lambda_4*(g^3) + lambda_5*(d*h^2) + lambda_6*(d*g*h)
  + lambda_7*(d*g^2) + lambda_8*(d^2*h) + lambda_9*(d^2*g)
  + lambda_10*(d^3) + lambda_11*(b*h^2) + lambda_12*(b*g*h)
  + lambda_13*(b*g^2) + lambda_14*(b*d*h) + lambda_15*(b*d^2)
  + lambda_16*(b^2*h) + lambda_17*(b^2*g) + lambda_18*(b^2*d)
  + lambda_19*(b^3) + lambda_20*(f*h^2) + lambda_21*(f*g*h)
  + lambda_22*(f*g^2) + lambda_23*(d*f*g) + lambda_24*(d^2*f)
  + lambda_25*(b*f*h) + lambda_26*(b*f*g) + lambda_27*(b^2*f)
  + lambda_28*(f^2*h) + lambda_29*(f^2*g) + lambda_30*(d*f^2)
  + lambda_31*(b*f^2) + lambda_32*(f^3) + lambda_33*(a*h^2)
  + lambda_34*(a*g*h) + lambda_35*(a*g^2) + lambda_36*(a*d*g)
  + lambda_37*(a*d^2) + lambda_38*(a*b*d) + lambda_39*(a*b^2)
  + lambda_40*(a*f*h) + lambda_41*(a*f*g) + lambda_42*(a*d*f)
  + lambda_43*(a*f^2) + lambda_44*(a^2*h) + lambda_45*(a^2*g)
  + lambda_46*(a^2*d) + lambda_47*(a^2*b) + lambda_48*(a^2*f)
  + lambda_49*(a^3) + lambda_50*(e*h^2) + lambda_51*(e*g*h)
  + lambda_52*(e*g^2) + lambda_53*(d*e*h) + lambda_54*(d*e*g)
  + lambda_55*(d^2*e) + lambda_56*(b*e*h) + lambda_57*(b*d*e)
  + lambda_58*(b^2*e) + lambda_59*(e*f*h) + lambda_60*(b*e*f)
  + lambda_61*(e*f^2) + lambda_62*(a*e*h) + lambda_63*(a*e*g)
  + lambda_64*(a*d*e) + lambda_65*(a*b*e) + lambda_66*(a*e*f)
  + lambda_67*(a^2*e) + lambda_68*(e^2*h) + lambda_69*(e^2*g)
  + lambda_70*(d*e^2) + lambda_71*(b*e^2) + lambda_72*(e^2*f)
  + lambda_73*(a*e^2) + lambda_74*(e^3) + lambda_75*(c*h^2)
  + lambda_76*(c*g*h) + lambda_77*(c*g^2) + lambda_78*(c*d*h)
  + lambda_79*(c*d*g) + lambda_80*(c*d^2) + lambda_81*(b*c*h)
  + lambda_82*(b*c*g) + lambda_83*(b*c*d) + lambda_84*(b^2*c)
  + lambda_85*(c*f*g) + lambda_86*(c*d*f) + lambda_87*(b*c*f)
  + lambda_88*(c*f^2) + lambda_89*(a*c*d) + lambda_90*(a*b*c)
  + lambda_91*(a*c*f) + lambda_92*(a^2*c) + lambda_93*(b*c*e)
  + lambda_94*(c*e*f) + lambda_95*(a*c*e) + lambda_96*(c*e^2)
  + lambda_97*(c^2*h) + lambda_98*(c^2*g) + lambda_99*(c^2*d)
  + lambda_100*(b*c^2) + lambda_101*(c^2*f) + lambda_102*(a*c^2)
  + lambda_103*(c^2*e) + lambda_104*(c^3)
```

### F_11

```text
F_11 = c*e*g
  + lambda_105*(h^3+b^3) + lambda_106*(g*h^2+b^2*c) + lambda_107*(g^2*h+b*c^2)
  + lambda_108*(g^3+c^3) + lambda_109*(d*h^2+b^2*f) + lambda_110*(d*g*h+b*c*f)
  + lambda_111*(d*g^2+c^2*f) + lambda_112*(d^2*h+b*f^2) + lambda_113*(d^2*g+c*f^2)
  + lambda_114*(f^3+d^3) + lambda_115*(b*h^2+b^2*h) + lambda_116*(b*g*h+b*c*h)
  + lambda_117*(c^2*h+b*g^2) + lambda_118*(b*f*h+b*d*h) + lambda_119*(f^2*h+b*d^2)
  + lambda_120*(c*h^2+b^2*g) + lambda_121*(f*h^2+b^2*d) + lambda_122*(f*g*h+b*c*d)
  + lambda_123*(f*g^2+c^2*d) + lambda_124*(d*f*g+c*d*f) + lambda_125*(d*f^2+d^2*f)
  + lambda_126*(c*d*h+b*f*g) + lambda_127*(f^2*g+c*d^2) + lambda_128*(a*h^2+a*b^2)
  + lambda_129*(a*g*h+a*b*c) + lambda_130*(a*g^2+a*c^2) + lambda_131*(a*d*g+a*c*f)
  + lambda_132*(a*f^2+a*d^2) + lambda_133*(a*f*h+a*b*d) + lambda_134*(a*f*g+a*c*d)
  + lambda_135*(a*d*f) + lambda_136*(a^2*h+a^2*b) + lambda_137*(a^2*g+a^2*c)
  + lambda_138*(a^2*f+a^2*d) + lambda_139*(a^3) + lambda_140*(e*h^2+b^2*e)
  + lambda_141*(e*g*h+b*c*e) + lambda_142*(e*g^2+c^2*e) + lambda_143*(d*e*h+b*e*f)
  + lambda_144*(d*e*g+c*e*f) + lambda_145*(e*f^2+d^2*e) + lambda_146*(b*e*h)
  + lambda_147*(e*f*h+b*d*e) + lambda_148*(a*e*h+a*b*e) + lambda_149*(a*e*g+a*c*e)
  + lambda_150*(a*e*f+a*d*e) + lambda_151*(a^2*e) + lambda_152*(e^2*h+b*e^2)
  + lambda_153*(e^2*g+c*e^2) + lambda_154*(e^2*f+d*e^2) + lambda_155*(a*e^2)
  + lambda_156*(e^3) + lambda_157*(c*g*h+b*c*g) + lambda_158*(c*g^2+c^2*g)
  + lambda_159*(c*f*g+c*d*g)
```

### F_12

```text
F_12 = c*e*h
  + lambda_160*(h^3+e^3) + lambda_161*(g*h^2+a*e^2) + lambda_162*(g^2*h+a^2*e)
  + lambda_163*(g^3+a^3) + lambda_164*(e^2*f+d*h^2) + lambda_165*(d*g*h+a*e*f)
  + lambda_166*(d*g^2+a^2*f) + lambda_167*(e*f^2+d^2*h) + lambda_168*(d^2*g+a*f^2)
  + lambda_169*(f^3+d^3) + lambda_170*(b*h^2+b*e^2) + lambda_171*(b*g*h+a*b*e)
  + lambda_172*(b*g^2+a^2*b) + lambda_173*(b*e*f+b*d*h) + lambda_174*(b*f^2+b*d^2)
  + lambda_175*(b^2*h+b^2*e) + lambda_176*(b^2*g+a*b^2) + lambda_177*(b^2*f+b^2*d)
  + lambda_178*(b^3) + lambda_179*(f*h^2+d*e^2) + lambda_180*(f*g*h+a*d*e)
  + lambda_181*(f*g^2+a^2*d) + lambda_182*(d*f*g+a*d*f) + lambda_183*(d*f^2+d^2*f)
  + lambda_184*(b*f*h+b*d*e) + lambda_185*(b*f*g+a*b*d) + lambda_186*(f^2*h+d^2*e)
  + lambda_187*(f^2*g+a*d^2) + lambda_188*(e^2*g+a*h^2) + lambda_189*(a*g*h+a*e*g)
  + lambda_190*(a*g^2+a^2*g) + lambda_191*(a*f*g+a*d*g) + lambda_192*(d*e*g+a*f*h)
  + lambda_193*(e*g^2+a^2*h) + lambda_194*(e*h^2+e^2*h) + lambda_195*(e*g*h+a*e*h)
  + lambda_196*(e*f*h+d*e*h) + lambda_197*(b*e*h) + lambda_198*(c*h^2+c*e^2)
  + lambda_199*(c*g*h+a*c*e) + lambda_200*(c*g^2+a^2*c) + lambda_201*(c*e*f+c*d*h)
  + lambda_202*(c*d*g+a*c*f) + lambda_203*(c*f^2+c*d^2) + lambda_204*(b*c*h+b*c*e)
  + lambda_205*(b*c*g+a*b*c) + lambda_206*(b*c*f+b*c*d) + lambda_207*(b^2*c)
  + lambda_208*(c*f*g+a*c*d) + lambda_209*(c*d*f) + lambda_210*(c^2*h+c^2*e)
  + lambda_211*(c^2*g+a*c^2) + lambda_212*(c^2*f+c^2*d) + lambda_213*(b*c^2)
  + lambda_214*(c^3)
```

### F_13

```text
F_13 = c*f*h
  + lambda_1*(e^3) + lambda_2*(a*e^2) + lambda_3*(a^2*e)
  + lambda_4*(a^3) + lambda_5*(e^2*f) + lambda_6*(a*e*f)
  + lambda_7*(a^2*f) + lambda_8*(e*f^2) + lambda_9*(a*f^2)
  + lambda_10*(f^3) + lambda_11*(b*e^2) + lambda_12*(a*b*e)
  + lambda_13*(a^2*b) + lambda_14*(b*e*f) + lambda_15*(b*f^2)
  + lambda_16*(b^2*e) + lambda_17*(a*b^2) + lambda_18*(b^2*f)
  + lambda_19*(b^3) + lambda_20*(d*e^2) + lambda_21*(a*d*e)
  + lambda_22*(a^2*d) + lambda_23*(a*d*f) + lambda_24*(d*f^2)
  + lambda_25*(b*d*e) + lambda_26*(a*b*d) + lambda_27*(b^2*d)
  + lambda_28*(d^2*e) + lambda_29*(a*d^2) + lambda_30*(d^2*f)
  + lambda_31*(b*d^2) + lambda_32*(d^3) + lambda_33*(e^2*g)
  + lambda_34*(a*e*g) + lambda_35*(a^2*g) + lambda_36*(a*f*g)
  + lambda_37*(f^2*g) + lambda_38*(b*f*g) + lambda_39*(b^2*g)
  + lambda_40*(d*e*g) + lambda_41*(a*d*g) + lambda_42*(d*f*g)
  + lambda_43*(d^2*g) + lambda_44*(e*g^2) + lambda_45*(a*g^2)
  + lambda_46*(f*g^2) + lambda_47*(b*g^2) + lambda_48*(d*g^2)
  + lambda_49*(g^3) + lambda_50*(e^2*h) + lambda_51*(a*e*h)
  + lambda_52*(a^2*h) + lambda_53*(e*f*h) + lambda_54*(a*f*h)
  + lambda_55*(f^2*h) + lambda_56*(b*e*h) + lambda_57*(b*f*h)
  + lambda_58*(b^2*h) + lambda_59*(d*e*h) + lambda_60*(b*d*h)
  + lambda_61*(d^2*h) + lambda_62*(e*g*h) + lambda_63*(a*g*h)
  + lambda_64*(f*g*h) + lambda_65*(b*g*h) + lambda_66*(d*g*h)
  + lambda_67*(g^2*h) + lambda_68*(e*h^2) + lambda_69*(a*h^2)
  + lambda_70*(f*h^2) + lambda_71*(b*h^2) + lambda_72*(d*h^2)
  + lambda_73*(g*h^2) + lambda_74*(h^3) + lambda_75*(c*e^2)
  + lambda_76*(a*c*e) + lambda_77*(a^2*c) + lambda_78*(c*e*f)
  + lambda_79*(a*c*f) + lambda_80*(c*f^2) + lambda_81*(b*c*e)
  + lambda_82*(a*b*c) + lambda_83*(b*c*f) + lambda_84*(b^2*c)
  + lambda_85*(a*c*d) + lambda_86*(c*d*f) + lambda_87*(b*c*d)
  + lambda_88*(c*d^2) + lambda_89*(c*f*g) + lambda_90*(b*c*g)
  + lambda_91*(c*d*g) + lambda_92*(c*g^2) + lambda_93*(b*c*h)
  + lambda_94*(c*d*h) + lambda_95*(c*g*h) + lambda_96*(c*h^2)
  + lambda_97*(c^2*e) + lambda_98*(a*c^2) + lambda_99*(c^2*f)
  + lambda_100*(b*c^2) + lambda_101*(c^2*d) + lambda_102*(c^2*g)
  + lambda_103*(c^2*h) + lambda_104*(c^3)
```

### F_14

```text
F_14 = d*e*f
  + lambda_237*(h^3+b^3) + lambda_238*(g*h^2+b^2*c) + lambda_239*(g^2*h+b*c^2)
  + lambda_240*(g^3+c^3) + lambda_241*(d*h^2+b^2*f) + lambda_242*(d*g*h+b*c*f)
  + lambda_243*(d*g^2+c^2*f) + lambda_244*(d^2*h+b*f^2) + lambda_245*(d^2*g+c*f^2)
  + lambda_246*(f^3+d^3) + lambda_247*(b*h^2+b^2*h) + lambda_248*(b*g*h+b*c*h)
  + lambda_249*(c^2*h+b*g^2) + lambda_250*(b*f*h+b*d*h) + lambda_251*(f^2*h+b*d^2)
  + lambda_252*(c*h^2+b^2*g) + lambda_253*(f*h^2+b^2*d) + lambda_254*(f*g*h+b*c*d)
  + lambda_255*(f*g^2+c^2*d) + lambda_256*(d*f*g+c*d*f) + lambda_257*(d*f^2+d^2*f)
  + lambda_258*(c*d*h+b*f*g) + lambda_259*(f^2*g+c*d^2) + lambda_260*(a*h^2+a*b^2)
  + lambda_261*(a*g*h+a*b*c) + lambda_262*(a*g^2+a*c^2) + lambda_263*(a*d*g+a*c*f)
  + lambda_264*(a*f^2+a*d^2) + lambda_265*(a*f*h+a*b*d) + lambda_266*(a*f*g+a*c*d)
  + lambda_267*(a*d*f) + lambda_268*(a^2*h+a^2*b) + lambda_269*(a^2*g+a^2*c)
  + lambda_270*(a^2*f+a^2*d) + lambda_271*(a^3) + lambda_272*(e*h^2+b^2*e)
  + lambda_273*(e*g*h+b*c*e) + lambda_274*(e*g^2+c^2*e) + lambda_275*(d*e*h+b*e*f)
  + lambda_276*(d*e*g+c*e*f) + lambda_277*(e*f^2+d^2*e) + lambda_278*(b*e*h)
  + lambda_279*(e*f*h+b*d*e) + lambda_280*(a*e*h+a*b*e) + lambda_281*(a*e*g+a*c*e)
  + lambda_282*(a*e*f+a*d*e) + lambda_283*(a^2*e) + lambda_284*(e^2*h+b*e^2)
  + lambda_285*(e^2*g+c*e^2) + lambda_286*(e^2*f+d*e^2) + lambda_287*(a*e^2)
  + lambda_288*(e^3) + lambda_289*(c*g*h+b*c*g) + lambda_290*(c*g^2+c^2*g)
  + lambda_291*(c*f*g+c*d*g)
```

### F_15

```text
F_15 = d*f*h
  + lambda_237*(e^3+b^3) + lambda_238*(b^2*c+a*e^2) + lambda_239*(b*c^2+a^2*e)
  + lambda_240*(c^3+a^3) + lambda_241*(e^2*f+b^2*d) + lambda_242*(b*c*d+a*e*f)
  + lambda_243*(c^2*d+a^2*f) + lambda_244*(e*f^2+b*d^2) + lambda_245*(c*d^2+a*f^2)
  + lambda_246*(f^3+d^3) + lambda_247*(b*e^2+b^2*e) + lambda_248*(b*c*e+a*b*e)
  + lambda_249*(c^2*e+a^2*b) + lambda_250*(b*e*f+b*d*e) + lambda_251*(d^2*e+b*f^2)
  + lambda_252*(c*e^2+a*b^2) + lambda_253*(d*e^2+b^2*f) + lambda_254*(b*c*f+a*d*e)
  + lambda_255*(c^2*f+a^2*d) + lambda_256*(c*d*f+a*d*f) + lambda_257*(d*f^2+d^2*f)
  + lambda_258*(c*e*f+a*b*d) + lambda_259*(c*f^2+a*d^2) + lambda_260*(e^2*g+b^2*g)
  + lambda_261*(b*c*g+a*e*g) + lambda_262*(c^2*g+a^2*g) + lambda_263*(c*d*g+a*f*g)
  + lambda_264*(f^2*g+d^2*g) + lambda_265*(d*e*g+b*f*g) + lambda_266*(c*f*g+a*d*g)
  + lambda_267*(d*f*g) + lambda_268*(e*g^2+b*g^2) + lambda_269*(c*g^2+a*g^2)
  + lambda_270*(f*g^2+d*g^2) + lambda_271*(g^3) + lambda_272*(e^2*h+b^2*h)
  + lambda_273*(b*c*h+a*e*h) + lambda_274*(c^2*h+a^2*h) + lambda_275*(e*f*h+b*d*h)
  + lambda_276*(c*d*h+a*f*h) + lambda_277*(f^2*h+d^2*h) + lambda_278*(b*e*h)
  + lambda_279*(d*e*h+b*f*h) + lambda_280*(e*g*h+b*g*h) + lambda_281*(c*g*h+a*g*h)
  + lambda_282*(f*g*h+d*g*h) + lambda_283*(g^2*h) + lambda_284*(e*h^2+b*h^2)
  + lambda_285*(c*h^2+a*h^2) + lambda_286*(f*h^2+d*h^2) + lambda_287*(g*h^2)
  + lambda_288*(h^3) + lambda_289*(a*c*e+a*b*c) + lambda_290*(a*c^2+a^2*c)
  + lambda_291*(a*c*f+a*c*d)
```

### F_16

```text
F_16 = e*f*g
  + lambda_1*(b^3) + lambda_2*(b^2*c) + lambda_3*(b*c^2)
  + lambda_4*(c^3) + lambda_5*(b^2*f) + lambda_6*(b*c*f)
  + lambda_7*(c^2*f) + lambda_8*(b*f^2) + lambda_9*(c*f^2)
  + lambda_10*(f^3) + lambda_11*(b^2*h) + lambda_12*(b*c*h)
  + lambda_13*(c^2*h) + lambda_14*(b*f*h) + lambda_15*(f^2*h)
  + lambda_16*(b*h^2) + lambda_17*(c*h^2) + lambda_18*(f*h^2)
  + lambda_19*(h^3) + lambda_20*(b^2*d) + lambda_21*(b*c*d)
  + lambda_22*(c^2*d) + lambda_23*(c*d*f) + lambda_24*(d*f^2)
  + lambda_25*(b*d*h) + lambda_26*(c*d*h) + lambda_27*(d*h^2)
  + lambda_28*(b*d^2) + lambda_29*(c*d^2) + lambda_30*(d^2*f)
  + lambda_31*(d^2*h) + lambda_32*(d^3) + lambda_33*(a*b^2)
  + lambda_34*(a*b*c) + lambda_35*(a*c^2) + lambda_36*(a*c*f)
  + lambda_37*(a*f^2) + lambda_38*(a*f*h) + lambda_39*(a*h^2)
  + lambda_40*(a*b*d) + lambda_41*(a*c*d) + lambda_42*(a*d*f)
  + lambda_43*(a*d^2) + lambda_44*(a^2*b) + lambda_45*(a^2*c)
  + lambda_46*(a^2*f) + lambda_47*(a^2*h) + lambda_48*(a^2*d)
  + lambda_49*(a^3) + lambda_50*(b^2*e) + lambda_51*(b*c*e)
  + lambda_52*(c^2*e) + lambda_53*(b*e*f) + lambda_54*(c*e*f)
  + lambda_55*(e*f^2) + lambda_56*(b*e*h) + lambda_57*(e*f*h)
  + lambda_58*(e*h^2) + lambda_59*(b*d*e) + lambda_60*(d*e*h)
  + lambda_61*(d^2*e) + lambda_62*(a*b*e) + lambda_63*(a*c*e)
  + lambda_64*(a*e*f) + lambda_65*(a*e*h) + lambda_66*(a*d*e)
  + lambda_67*(a^2*e) + lambda_68*(b*e^2) + lambda_69*(c*e^2)
  + lambda_70*(e^2*f) + lambda_71*(e^2*h) + lambda_72*(d*e^2)
  + lambda_73*(a*e^2) + lambda_74*(e^3) + lambda_75*(b^2*g)
  + lambda_76*(b*c*g) + lambda_77*(c^2*g) + lambda_78*(b*f*g)
  + lambda_79*(c*f*g) + lambda_80*(f^2*g) + lambda_81*(b*g*h)
  + lambda_82*(c*g*h) + lambda_83*(f*g*h) + lambda_84*(g*h^2)
  + lambda_85*(c*d*g) + lambda_86*(d*f*g) + lambda_87*(d*g*h)
  + lambda_88*(d^2*g) + lambda_89*(a*f*g) + lambda_90*(a*g*h)
  + lambda_91*(a*d*g) + lambda_92*(a^2*g) + lambda_93*(e*g*h)
  + lambda_94*(d*e*g) + lambda_95*(a*e*g) + lambda_96*(e^2*g)
  + lambda_97*(b*g^2) + lambda_98*(c*g^2) + lambda_99*(f*g^2)
  + lambda_100*(g^2*h) + lambda_101*(d*g^2) + lambda_102*(a*g^2)
  + lambda_103*(e*g^2) + lambda_104*(g^3)
```

## Reproducibility and remaining representation work

**COMPUTER-CERTIFIED.** The exporter checks the original sixteen
central cubics, the thirty canonical degree-four syzygies, central
block values, all denominator units, and the selected Jacobian.
The original resolution certifies that these linear relations
generate the entire first-syzygy module; this retains the stated
computer-algebra trust boundary of the source proof.

**OPEN convenience reduction.** A primitive element or a small
multiplication table for L has not been extracted. Neither is
needed to specify the finite algebraic numbers by the unique
p-adic root above. The global coefficient zero locus can have
other components; those are excluded by the isolating condition.

Reproduce under the sequential resource guard:

    python3 -B scripts/run_guarded.py --seconds 300 --memory-mb 2800 --tag ramified-fibre-export -- python3 -B scripts/export_ramified_fibre.py
