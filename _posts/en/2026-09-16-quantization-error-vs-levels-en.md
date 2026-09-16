---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quantization Error vs Levels
translated: false
type: note
---

Question: What is the relationship between quantization error and quantization levels?

Answer:

**Quantization error** (量化误差) and **quantization levels** (量化电平) are inversely and fundamentally related in analog-to-digital conversion:

**Quantization Levels** define the discrete steps used to represent a continuous signal. If a system uses *n* bits, it has **2ⁿ quantization levels**.

**Quantization Error** is the difference between the original analog value and its nearest quantization level. It arises *because* levels are discrete — any value falling between two levels must be rounded.

---

### Their Relationship

| Quantization Levels | Effect on Error |
| --- | --- |
| More levels (more bits) | Smaller step size → smaller max error |
| Fewer levels (fewer bits) | Larger step size → larger max error |

Specifically, if the full signal range is **R** and there are **N = 2ⁿ** levels:

- **Step size (Δ)** = R / N
- **Maximum quantization error** = ±Δ/2 = ±R / (2N)

So quantization error is **inversely proportional** to the number of quantization levels. **Doubling the levels halves the maximum error**, and each additional bit reduces the maximum error by half.

---

### In Summary

> More quantization levels → finer resolution → smaller quantization error → higher signal fidelity.

This trade-off is central to audio encoding, ADC design, and signal processing — e.g., CD audio uses 16-bit depth (65,536 levels) to keep quantization noise below audible thresholds.

References:

- [Quantization (signal processing) – Wikipedia](https://en.wikipedia.org/wiki/Quantization_(signal_processing))
- [Quantization Error – Analog Devices Glossary](https://www.analog.com/en/design-center/glossary/quantization-error.html)
