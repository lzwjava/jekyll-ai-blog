---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quantization Levels and Error Trade-off
translated: false
type: note
---

**Question:** What is the relationship between quantization levels (量化电平) and quantization error (量化误差) in signal processing?

**Answer:**

In analog-to-digital conversion, **quantization** maps a continuous-amplitude signal to a finite set of discrete values. The relationship between quantization levels and quantization error is fundamentally a trade-off between **precision** and **representational capacity**.

**Quantization levels (量化电平)** are the discrete amplitude steps that an ADC can represent. If a signal spans a range $V$ and the ADC has $N$ bits, the number of levels is $2^N$ and the **step size** (also called the quantization interval) is:

$$\Delta = \frac{V}{2^N}$$

**Quantization error (量化误差)** is the difference between the actual analog sample value and the nearest quantization level. For a uniform quantizer, it is bounded by:

$$-\frac{\Delta}{2} \leq e_q \leq \frac{\Delta}{2}$$

The direct relationship:

- **More quantization levels** (larger $N$) → **smaller step size** $\Delta$ → **smaller maximum quantization error**
- **Fewer quantization levels** (smaller $N$) → **larger step size** → **larger quantization error** (more distortion)

The RMS (root-mean-square) quantization error for a uniform quantizer with a uniformly distributed input is:

$$e_{rms} = \frac{\Delta}{\sqrt{12}}$$

Since $\Delta = V / 2^N$, each additional bit roughly halves the step size, reducing the RMS error by ~6 dB (a factor of 2), which is the origin of the "6 dB per bit" rule in ADC specifications.**In summary**, the relationship is inverse and precisely quantifiable: quantization error is bounded by half the step size ($\Delta/2$), and step size shrinks as the number of levels grows. Every extra bit of resolution doubles the number of levels, halves $\Delta$, and cuts the maximum error in half — which is why high-fidelity audio uses 16–24 bits (65,536–16 million levels) while voice telephony gets by with 8 bits (256 levels).

**References:**
- [Quantization (signal processing) — Wikipedia](https://en.wikipedia.org/wiki/Quantization_(signal_processing))
- [Signal-to-quantization-noise ratio — Wikipedia](https://en.wikipedia.org/wiki/Signal-to-quantization-noise_ratio)
