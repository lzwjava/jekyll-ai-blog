---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zero-Shot Forecasting for Any Time Series
translated: false
type: note
---

Question: **What is TimesFM-3 actually useful for? What applications does it enable?**

Answer: **It is useful whenever you have a stream of measurements and need to predict what happens next.** Think of it as an LLM for numerical time sequences.

The killer feature of TimesFM-3 is not merely “forecasting.” It's:

> **Give it a new time-series dataset it has never seen, and get a useful forecast without training a model for that dataset.**

Google reports that TimesFM-3 is designed for multivariate forecasting and can jointly use related series plus historical/future-known covariates. ([Google Research][1])

### Concrete applications

| Application             | Input                                 | Prediction                    |
| ----------------------- | ------------------------------------- | ----------------------------- |
| 🛒 E-commerce           | historical sales, traffic, promotions | next-day/week/month sales     |
| 📦 Inventory            | sales + inventory + lead time         | future demand / stockout risk |
| ⚡ Electricity           | historical load + weather             | future power demand           |
| 💰 Finance              | prices, volume, rates                 | future values / ranges        |
| 🏭 Manufacturing        | machine sensors                       | future sensor trajectories    |
| 🖥️ Cloud/AI infra      | GPU utilization, requests, latency    | future workload               |
| 🌐 Observability        | CPU, memory, QPS, errors              | future system behavior        |
| 🚚 Logistics            | orders, traffic, capacity             | future demand                 |
| 🏥 Healthcare           | patient measurements over time        | future measurements           |
| 🌦️ Weather/environment | temperature, humidity, etc.           | future measurements           |

Google explicitly lists **retail, finance, observability, manufacturing, healthcare and natural sciences** as real-world domains for time-series foundation models. ([Google Research][2])

### The really interesting example

Suppose you operate a GPU cluster:

```text
time ──────────────────────────────>

GPU utilization     ▁▂▃▅▇▆▅▇▇▆▅
request QPS         ▁▂▃▄▆▅▅▇▇▆▅
queue length        ▁▁▂▃▆▅▄▇▆▅▄
power consumption   ▂▂▃▄▆▅▅▇▇▆▅
```

You want:

```text
next 1h / 6h / 24h
```

TimesFM-3 can jointly forecast these signals rather than forecasting each independently.

Then you can build:

```text
TimesFM-3
    ↓
forecast GPU demand
    ↓
forecast probability of saturation
    ↓
start/stop GPU instances
    ↓
schedule training jobs
    ↓
avoid queue explosion
```

That is a **very practical AI-agent + time-series combination**.

---

## The most valuable feature: future-known information

Imagine an online store.

Historical data:

```text
sales
traffic
price
```

But you also know:

```text
Sep 15 → promotion
Sep 20 → holiday
Sep 25 → promotion
```

Then:

```text
sales ────────────────→ ?
traffic ──────────────→ ?
price ────────────────→ ?
promotion ────────────→ known future
holiday ──────────────→ known future
```

TimesFM-3 can use those future covariates.

So instead of:

```text
"Based on the past, sales will probably be 10,000."
```

you can get:

```text
normal day       → 10,000
promotion day    → 12,000
holiday          → 14,000
```

Google's own example demonstrates this with promotion schedules causing forecasted sales lifts. ([Google Research][1])

---

## Another useful application: anomaly detection

TimesFM itself isn't an anomaly detector, but you can turn its probabilistic forecast into one.

Suppose:

```text
forecast:

q10 = 80
q50 = 100
q90 = 120
```

and the actual value suddenly becomes:

```text
actual = 190
```

Then:

```text
190 >> q90
```

→ suspicious.

So you can build:

```text
metrics
   ↓
TimesFM
   ↓
prediction interval
   ↓
actual outside interval?
   ↓
alert
   ↓
LLM agent investigates logs
```

The TimesFM project itself documents this approach. ([GitHub][3])

This is particularly interesting for **DevOps / AI infrastructure observability**.

---

## And this is where I think it gets interesting for you

You could build a tiny **AI infrastructure forecaster**:

```text
Prometheus
    │
    ├── GPU utilization
    ├── VRAM
    ├── CPU
    ├── requests/sec
    ├── queue length
    ├── latency
    └── power
          │
          ▼
      TimesFM-3
          │
          ├── 10m forecast
          ├── 1h forecast
          ├── 6h forecast
          └── uncertainty
                  │
                  ▼
             Agent
          ┌───────┴────────┐
          │                │
      scale GPU        investigate
      capacity          anomaly
```

That's a much more interesting use than simply asking:

> "What will the stock price be tomorrow?"

Because **forecasting + actions** creates an actual agentic system.

One caveat: the released **TimesFM-3 weights are currently non-commercial/non-production licensed**, even though the source code is Apache-2.0. So for your company, I'd use it for research/benchmarking rather than silently putting the pretrained weights into a production service. ([GitHub][4])

**In one sentence:** TimesFM-3 is useful for turning **“a bunch of historical numerical signals” → “what will probably happen next, including uncertainty”**, especially when many signals influence each other.

[1]: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
[2]: https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
[3]: https://github.com/google-research/timesfm/blob/master/timesfm-forecasting/SKILL.md?utm_source=chatgpt.com "timesfm/timesfm-forecasting/SKILL.md at master · google-research/timesfm · GitHub"
[4]: https://github.com/google-research/timesfm?utm_source=chatgpt.com "GitHub - google-research/timesfm: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting. · GitHub"