# Linkage triage: exact starting link, no priority overnight search

## Located certificate and explicit inputs

**COMPUTER-CERTIFIED (existing certificate; not rerun today).** The reported
link is precisely
`grunbaum-cy-geography-fable-dgla/scripts/test_direct_link.m2` at commit
`3f7ef3da88fe963e10001fc66cbff4153d5fcb27`; its result is
`certificates/direct_link_special_QQ.txt`. It is a link of the *special
Stanley–Reisner scheme*. The source script uses the old generator order
identified in `LINEAGE_COMPARISON.md` and defines

\[
C=(m_1+m_5+m_9+m_{13},\ m_2+m_6+m_{10}+m_{14},\
m_3+m_7+m_{11}+m_{15},\ m_4+m_8+m_{12}+m_{16}).
\]

It checks `codim C=4`, computes `J=C:I`, and verifies

\[
C:J=I,\qquad \dim(S/J)=4,\qquad \deg(S/J)=61,
\qquad\operatorname{pd}_S(S/J)=4.
\]

**PROVED.** Four cubics of height four in the polynomial ring form a
regular sequence, so `C` is a complete intersection of degree `3^4=81`.
The double-colon identity certifies the direct link. The residual degree is
`81-20=61`; the depth calculation from Auslander–Buchsbaum gives depth four,
so the residual threefold is arithmetically Cohen–Macaulay. Rationality was
not tested and is not implied.

**COMPUTER-CERTIFIED (new exact transport).** Under
`(x1,...,x8)_old=(b,e,a,d,g,f,c,h)`, the identical link in the current fixed
generator order is

\[
\begin{aligned}
c_1&=f_{13}+f_6+f_{10}+f_3=cfh+adh+cde+abh,\\
c_2&=f_{15}+f_{12}+f_{14}+f_1=dfh+ceh+def+abf,\\
c_3&=f_5+f_{11}+f_7+f_2=ach+ceg+bdf+abg,\\
c_4&=f_4+f_{16}+f_8+f_9=acg+efg+bdg+beg.
\end{aligned}
\]

No change of smoothing lineage is needed to transport a link of the common
special fibre. Transporting this input does not identify their smooth fibres.

## Why the obvious second link provides little information

**COMPUTER-CERTIFIED (existing certificate).** The residual resolution has

\[
\begin{aligned}
\beta_{0,0}&=1,\quad \beta_{1,3}=4,\quad\beta_{1,4}=1,\\
\beta_{2,6}&=6,\quad\beta_{2,7}=16,\quad\beta_{3,8}=30,
\quad\beta_{4,9}=12.
\end{aligned}
\]

**PROVED.** In particular `J_3` has dimension four and is exactly `C_3`.
Any four cubic generators in `J` that form a regular sequence therefore span
the same cubic space, define `C`, and link back to the original degree-20
scheme. A second `(3,3,3,3)` colon computation cannot reveal a new residual.

**PROVED (degree restriction).** Any distinct homogeneous complete
intersection in `J` must use at least one degree-four generator. Since no
equations of degree below three exist, the smallest possible distinct type
is `(3,3,3,4)`. If such a sequence is regular, its residual degree is

\[
3\cdot3\cdot3\cdot4-61=47=20+27.
\]

Thus an immediate second link cannot produce degree below 20. The decrease
from 61 to 47 alone gives no identified rational structure or continuing
descent. This statement does not rule out more elaborate liaison or
Gorenstein linkage.

**OPEN.** No scroll, rational parametrization, lower-degree rational target,
or explicit useful Gorenstein containing scheme was located in the supplied
data. The identical Betti table of another Calabi–Yau family is not a
determinantal presentation and cannot supply such a link.

## What is needed to deform this link

**PROVED (required data and tests).** Once exact finite equations
`F_i(q,x)` for a flat family have been certified, use the four displayed
linear combinations with `f_i` replaced by `F_i`. At the formal/local base,
their special regular-sequence property supplies the candidate relative
complete intersection. For a specified algebraic parameter value, verify
height four again: it need not hold at every distant value.

The exact executable input must include the coefficient field, algebraic
base equations if any, the sixteen cubics, and the selected nonzero fibre.
Compute the actual colon

\[
J_q=(c_1(q),c_2(q),c_3(q),c_4(q)):I_q
\]

and verify inverse colon, saturation/unmixedness, dimension, and degree 61.
For a relative link, separately verify base flatness and compatibility of
colon with the chosen specialization, using a relative free resolution or
the relevant base-change theorem with its hypotheses. A colon of a
nilpotent truncated jet or of its polynomial reinterpretation does not
certify a link of the true smooth fibre.

**HEURISTIC (queue decision).** Linkage should receive no heavy slot tonight
unless explicit-fibre work also exposes a concrete rational target, a useful
low-degree containing Gorenstein ideal, or an explicit descending linkage
chain. A useful proposed next job must specify the containing ideal, actual
colon inputs, expected residual degree, and a structural test beyond merely
reproducing the known degree-61 link. No new heavy linkage script has been
queued: its opportunity cost is currently greater than its expected
geography information.

## Claim ledger and boundary

| ID | Claim | Status | Exact evidence / consequence |
|---|---|---|---|
| E1 | The four displayed old cubic combinations give a degree-61 ACM residual | **COMPUTER-CERTIFIED** (existing) | Source script and certificate; no new CAS replay |
| E2 | The displayed current-coordinate combinations are the same link | **COMPUTER-CERTIFIED** | New monomial permutation, saved in lineage certificate |
| E3 | Any all-cubic second link returns the original ideal | **PROVED** | `dim J_3=4`, `J_3=C_3`, inverse colon |
| E4 | A distinct second homogeneous CI link has residual degree at least 47 | **PROVED** | Four degree-three minimal generators, one degree-four generator |
| E5 | The link reaches a rational or lower-than-20 residual | **OPEN** | No continuing chain or rationality certificate supplied |
| E6 | The special colon certificate certifies a colon on the zero-context smooth fibre | **FAILED** as an inference | Missing finite family and relative specialization checks |

Dependencies are D1 → E2 and E1 → E3/E4. No linkage statement is used to
derive Picard or Hodge data. Qualified-human verification is not claimed.
