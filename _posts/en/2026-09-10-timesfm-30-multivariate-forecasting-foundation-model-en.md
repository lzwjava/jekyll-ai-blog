---
audio: false
generated: true
image: false
lang: en
layout: post
title: "TimesFM 3.0: Multivariate Forecasting Foundation Model"
translated: false
type: note
---

Question: **What is Google TimesFM 3.0 (`google/timesfm-3.0-pytorch`)?**

Answer:

**TimesFM 3.0 is essentially a ~330M-parameter foundation model for time-series forecasting — think “LLM-style pretrained model, but the tokens are chunks of numerical time-series data instead of text.”** Google released it on **August 31, 2026**. ([Google Research][1])

![Image](https://images.openai.com/static-rsc-4/Pt_F0BPCex4-gs5xj1xq0s1rFgt5MBr_u0yos-UK8_uAfVy6cX3rY67Y4F02kguTLWTIK2lbFNSgNqewlr_QcIMtc3LISFIl50gEz22N_WdMnk0BCnK6RiBzb2vyY23LoOwzl7pvZw1f9xEfHMAzrCO9dePy4MXIfWnyDpyHi58ZxZ5RIlfqlUrY8vTdAiFf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/HDICMDYMia_I4VeaZx-Q3WLTeLs-yak6nfh01u82cXbSF6FHEiIdPutNyD3naOp9YCYkRNmgbXwpb8zIBvvvnDpqHE4B5KN2SgAqJEKSxZeKgyNxyhXiN2isvJVFS2hWINljwdowdD8g60q7oazirCIrhtLrX6C3A5rgiScZw2pO4lzV4G7OQglQvsYBEBL1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dp4go55OwzOsy3b-I8odzeMsY9rgEkTmngW-F9BT0XJLGZ-9-CCWlAt3EOrcPl-3muxZPHo3jHhFiz9D7CShcgrfETp32XsCM8QLIzeELmw8qZm_xpiBgyn7Puw6Z7-Hx-uzwk0Jmn98RuE9CO2N3BNyymet39KSVuKfZ8iyw6dZoS20HSbPSPNOvZU2qjt1?purpose=fullsize)

### 1. The important jump: multivariate

Older TimesFM models were primarily **univariate**:

```text
sales(t-100 ... t)
        ↓
      TimesFM
        ↓
sales(t+1 ... t+H)
```

TimesFM 3 can jointly model multiple correlated series:

```text
sales ─────────┐
traffic ───────┤
temperature ───┼──→ TimesFM 3 → future sales + traffic + ...
promotion ─────┤
holiday ───────┘
```

This is probably the most important improvement.

It can handle:

* multiple target series
* **past-only covariates**
* **past + future covariates**
* point forecasts
* quantile forecasts

and does this **zero-shot**, without task-specific fine-tuning. ([Google Research][1])

---

### 2. Architecture

The HF model card describes:

```text
Stacked Mixing Transformer
    +
Variate Attention
    +
CPM Iterative RevIN
```

with:

```text
20 Transformer layers
d_model = 1280
heads   = 16

input patch  = 32
output patch = 64
```

The checkpoint is about **0.3B parameters** and is distributed as F32 safetensors. ([Hugging Face][2])

The conceptual forward pass is roughly:

```text
raw time series
      ↓
normalization / RevIN
      ↓
patch into chunks of 32
      ↓
embedding
      ↓
Transformer × 20
      ↓
mix information across variables
      ↓
predict 64-step patches
      ↓
denormalize
      ↓
forecast
```

So it's not simply an MLP/regression model. It is using a Transformer as a **general-purpose sequence model over numerical signals**.

---

### 3. Why “foundation model” matters

The interesting part isn't the 330M parameter count.

It's the **pretraining**.

Google says TimesFM 3 was trained on **more than 1 trillion time points**, combining real-world and synthetic data. ([Google Research][1])

That gives you the same basic idea as an LLM:

```text
pretrain once
    ↓
learn generic temporal patterns
    ↓
give it a new time series
    ↓
forecast without training a new model
```

For example, you could potentially give it:

```python
temperature = [...]
electricity = [...]
traffic = [...]
```

and ask it to forecast the next 24 points.

You don't need to train:

```text
LSTM
XGBoost
Transformer
ARIMA
```

from scratch for every new dataset.

---

### 4. Covariates are especially useful

Suppose you're forecasting retail demand.

```text
target:
    ice_cream_sales

past covariates:
    foot_traffic
    temperature

future-known covariates:
    promotion
    holiday
    weather forecast
```

The distinction is important:

```text
past-only:
    x[0:T]

past + future:
    x[0:T+H]
```

TimesFM 3 can use both. ([Google Research][1])

That makes it much more practical than a model that only sees:

```text
y[t-k:t] → y[t:t+H]
```

---

### 5. Very simple usage

The official repository shows roughly:

```python
import numpy as np

from timesfm3 import TimesFM3Evaluator, ModelConfig

config = ModelConfig(
    checkpoint_path="google/timesfm-3.0-pytorch",
    per_core_batch_size=16,
    device="cuda",
)

model = TimesFM3Evaluator(config)

x = np.random.randn(3, 128).astype(np.float32)

outputs = list(
    model.predict_batch(
        contexts=[x],
        horizon=24,
        return_quantiles=True,
        use_symmetric_averaging=False,
    )
)

forecast = outputs[0].forecast
```

For:

```text
3 variables × 128 historical points
```

you get:

```text
3 variables × 24 future points
```

plus quantile forecasts if requested. ([GitHub][3])

---

### 6. Quantile forecasting

This is another useful feature.

Instead of only:

```text
forecast[t] = 123
```

you can get uncertainty:

```text
10% ── 105
20% ── 112
...
50% ── 123
...
90% ── 145
```

The output has 9 quantiles corresponding to the deciles, with the median at index 4. ([Hugging Face][2])

That's much more useful for:

* inventory
* capacity planning
* cloud/GPU demand
* financial risk
* energy
* traffic
* observability

than a single point estimate.

---

### 7. How big is it?

Interestingly, **330M parameters is tiny by LLM standards**.

| Model       | Approx. params | Domain      |
| ----------- | -------------: | ----------- |
| GPT-2 small |           124M | language    |
| TimesFM 3   |       **330M** | time series |
| TimesFM 2.5 |           200M | time series |
| 7B LLM      |             7B | language    |

The HF checkpoint is listed as ~0.3B parameters. ([Hugging Face][4])

So your **RTX 4070 12GB** should be more than enough for inference; the interesting constraint is likely throughput rather than fitting the model.

---

### 8. What makes TimesFM 3 interesting to you

I'd look at it less as “another forecasting library” and more as:

> **What happens when we apply the foundation-model paradigm to numerical sequences?**

The analogy is surprisingly direct:

```text
LLM

numbers/text
    ↓
tokenization
    ↓
Transformer
    ↓
next-token prediction
```

versus:

```text
TimesFM

time series
    ↓
patching
    ↓
Transformer
    ↓
future-patch prediction
```

The big research question becomes:

```text
Can sufficiently broad pretraining
replace task-specific time-series models?
```

Google reports TimesFM 3 ranked first on **fev-bench, TIME Benchmark, and GIFT-Eval** among the compared foundation models. ([GitHub][3])

One important caveat for your company: **the 3.0 pretrained weights are currently under Google's Non-Commercial License**, explicitly restricting commercial/production use of the default weights. The source code is Apache-2.0, but that does **not** make the 3.0 weights commercially usable. ([GitHub][3])

[TimesFM 3 Hugging Face model](https://huggingface.co/google/timesfm-3.0-pytorch?utm_source=chatgpt.com)
[Google Research — TimesFM 3 announcement](https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com)
[Google Research TimesFM GitHub](https://github.com/google-research/timesfm?utm_source=chatgpt.com)

I can also benchmark **TimesFM 3 vs TimesFM 2.5 vs Chronos-2 vs TabPFN-TS** conceptually and show which one I'd actually run on your 4070.

[1]: https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
[2]: https://huggingface.co/google/timesfm-3.0-pytorch "google/timesfm-3.0-pytorch · Hugging Face"
[3]: https://github.com/google-research/timesfm?utm_source=chatgpt.com "GitHub - google-research/timesfm: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting. · GitHub"
[4]: https://huggingface.co/google/timesfm-3.0-pytorch?utm_source=chatgpt.com "google/timesfm-3.0-pytorch · Hugging Face"
