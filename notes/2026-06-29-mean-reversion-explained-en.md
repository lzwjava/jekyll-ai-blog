---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mean Reversion Explained
translated: false
type: note
---

Question: What does "mean reversion" mean?

Answer:

Mean reversion is the statistical tendency of a series to pull back toward its long-run average after deviating from it. Formally: if `x_t` is far above `μ`, the expected next move `E[x_{t+1} - x_t]` is negative, and vice versa. The strength of the pull scales with the size of the deviation.

The canonical continuous-time model is the **Ornstein–Uhlenbeck process**:

```
dx_t = θ(μ - x_t) dt + σ dW_t
```

- `μ` — long-run mean the process reverts to
- `θ` — reversion speed (larger θ = faster snap-back); half-life of a deviation is `ln(2)/θ`
- `σ` — volatility
- `dW_t` — Brownian noise

Discretized, this is just an AR(1):

```python
import numpy as np

def ou(n=1000, theta=0.1, mu=0.0, sigma=0.2, x0=2.0, dt=1.0):
    x = np.empty(n); x[0] = x0
    for t in range(1, n):
        x[t] = x[t-1] + theta*(mu - x[t-1])*dt + sigma*np.sqrt(dt)*np.random.randn()
    return x
```

Note `x[t] = (1 - θ)·x[t-1] + θ·μ + noise` — the coefficient `(1-θ) < 1` is what guarantees reversion. If that coefficient is ≥ 1 the series is a random walk (no reversion) or explosive.

**Where it shows up:**
- *Quant trading* — pairs/stat-arb: trade the spread of two cointegrated assets, betting it returns to its mean. Test stationarity with ADF; estimate θ via OLS on the AR(1).
- *Volatility / rates models* — Vasicek, CIR for interest rates use OU dynamics.
- *Performance attribution* — "regression to the mean": extreme outliers tend to be followed by less extreme values, a pure sampling artifact, not a force.

The mirror image is **momentum/trending** behavior, where deviations persist or compound rather than decay (coefficient ≥ 1).

Quick mean-reversion test — fit AR(1), check whether the slope is significantly below 1:

```python
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

x = ou()
X = sm.add_constant(x[:-1])
beta = OLS(x[1:], X).fit().params[1]   # < 1 ⇒ mean-reverting
half_life = -np.log(2) / np.log(beta)  # in steps
```
