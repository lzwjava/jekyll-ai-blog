---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Common Emitter Amplifier Analysis
translated: false
type: note
---

### Collector Current \\( I_C \\)

The input resistance \\( R_{in} \\) for a common-emitter BJT amplifier with an grounded emitter is approximately the small-signal base resistance \\( r_\pi = \frac{\beta V_T}{I_C} \\), where \\( V_T = 0.026 \\) V (thermal voltage at room temperature) and \\( \beta = 100 \\).

Given \\( R_{in} = 1 \\) k\\( \Omega = 1000 \\) \\( \Omega \\),

\\[
r_\pi = \frac{100 \times 0.026}{I_C} = 1000
\\]

\\[
\frac{2.6}{I_C} = 1000
\\]

\\[
I_C = \frac{2.6}{1000} = 0.0026 \text{ A} = 2.6 \text{ mA}
\\]

This bias point yields a collector-emitter voltage \\( V_{CE} = V_{CC} - I_C R_C = 12 - (0.0026 \times 2200) \approx 12 - 5.72 = 6.28 \\) V, which is near the midpoint of the supply for reasonable linearity.

### Voltage Gain \\( A_V \\)

The small-signal voltage gain for a common-emitter amplifier (with no emitter resistor) is \\( A_V = -g_m R_C \\), where the transconductance \\( g_m = \frac{I_C}{V_T} \\).

\\[
g_m = \frac{0.0026}{0.026} = 0.1 \text{ A/V (or S)}
\\]

\\[
A_V = - (0.1 \times 2200) = -220
\\]

The negative sign indicates phase inversion.
