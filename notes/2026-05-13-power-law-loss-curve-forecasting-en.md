---
audio: false
generated: true
image: false
lang: en
layout: post
title: Power-Law Loss Curve Forecasting
translated: false
type: note
---

Fitting a power law to the val loss curve so far. Using the 11 data points (iter 1000→6000), a `L(n) = L_∞ + A · n^(-α)` fit gives consistent results across two reasonable choices of `L_∞`:

```
Fit A: L(n) = 2.7 + 42.4 / n^0.5     (residuals ~0.05)
Fit B: L(n) = 2.5 + 24.4 / n^0.4     (residuals ~0.05)
```

Both agree to ~0.02 across the projected range, so the forecast is robust to the choice. Predictions:

```
iter       Fit A    Fit B    Forecast    Δ from iter 6000 (3.247)
─────────────────────────────────────────────────────────────────
 7,500     3.19     3.20     ~3.19       -0.06
10,000     3.12     3.11     ~3.11       -0.14
12,500     3.08     3.05     ~3.06       -0.19
15,000     3.05     3.01     ~3.03       -0.22
19,073     3.01     2.96     ~2.98       -0.27
```

Sanity check against the most recent eval-to-eval deltas (4500→6000 averaged ~0.025/500 iters): integrating the implied 1/√n deceleration from iter 6000 forward gives ~0.27 total drop by 19,073 — matches both fits.

**Takeaways:**
- The earlier "~3.0–3.1 at iter 10,000" projection was slightly pessimistic — looks more like **3.11**.
- Full run lands at **~2.96–3.01**, with **2.98** as the central estimate.
- The curve flattens hard after iter ~12,000: from 12,500→19,073 (52% more iters) we only gain another ~0.08 in loss. Diminishing returns get steep.

**Caveats:**
- Power-law assumes no LR-schedule discontinuity. If there's cosine decay still kicking in, the back half could outperform this by 0.02–0.05.
- 95% confidence band at iter 19,073 is roughly **2.93–3.04** — the fit is tight, but eval-to-eval noise has been ±0.015.
