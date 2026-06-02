---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding RMS Voltage Calculation
translated: false
type: note
---

### Explanation

The root mean square (RMS) voltage, \\( V_{RMS} \\), represents the effective value of an alternating voltage that produces the same power dissipation in a resistive load as a direct current (DC) voltage of the same magnitude. For a sinusoidal waveform \\( v(t) = V_{max} \sin(\omega t) \\), where \\( V_{max} \\) is the peak (maximum) voltage, the RMS value is derived as follows:

1. **Mean square value**: The instantaneous voltage squared over one period \\( T \\) is \\( v^2(t) = V_{max}^2 \sin^2(\omega t) \\). The average (mean) of \\( \sin^2(\omega t) \\) over a period is \\( \frac{1}{2} \\), so the mean square voltage is \\( \frac{V_{max}^2}{2} \\).

2. **RMS calculation**: Take the square root of the mean square value:
   \\[
   V_{RMS} = \sqrt{\frac{V_{max}^2}{2}} = \frac{V_{max}}{\sqrt{2}}
   \\]

3. **Numerical approximation**: Since \\( \sqrt{2} \approx 1.414 \\), then \\( \frac{1}{\sqrt{2}} \approx 0.707 \\). Thus, \\( V_{RMS} \approx 0.707 \times V_{max} \\).

This confirms option **B**. The other options are incorrect:
- A overestimates (ignores averaging).
- C inverts the factor (that's \\( V_{max} = \sqrt{2} \times V_{RMS} \\)).
- D underestimates (that's the average value for a full-wave rectified sine, not RMS).
