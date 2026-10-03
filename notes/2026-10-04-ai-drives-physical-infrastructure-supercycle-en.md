---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Drives Physical Infrastructure Supercycle
translated: false
type: note
---

Question: **What does a16z’s most recent “State of Markets” report say about the market?**

Answer: The newest one is **“State of Markets II,” published September 30, 2026**. It is much more interesting than the January report because a16z is basically arguing that **the market has entered a broader technology/infrastructure supercycle, with AI pulling capital from software into physical infrastructure.** ([Andreessen Horowitz][1])

### The core thesis

**1. Tech is no longer just a sector — it is becoming “the everything cycle.”**

a16z says tech contributed about **76% of S&P 500 earnings growth in 2026 as of late August**.

Their argument is that the old economic cycle was driven by physical goods—houses, cars, appliances—while the previous decade was dominated by software. Now technology is embedded throughout the economy. ([Andreessen Horowitz][1])

---

**2. The big rotation is “bits → atoms.”**

This is probably the most important part for you.

The previous cycle:

```text
software
  ↓
cloud
  ↓
SaaS
  ↓
developer tools
```

The current cycle:

```text
AI models
   ↓
GPU / ASIC compute
   ↓
memory
   ↓
networking
   ↓
power
   ↓
datacenters
   ↓
robots / manufacturing / physical AI
```

a16z argues that hardware and infrastructure are coming back after years in which software captured most of the attention.

They specifically mention:

* semiconductors
* GPUs / compute
* memory
* networking
* electricity / grids
* robotics
* manufacturing
* defense
* autonomous vehicles

as areas receiving unusually strong capital investment. ([Andreessen Horowitz][1])

This is directly relevant to your **used-GPU / GPU repair / small GPU lab** thinking.

---

### 3. “GPU obsolescence” hasn't happened the way people expected

This is probably the most interesting finding for your hardware experiments.

The conventional argument was:

```text
A100 → H100 → H200 → B200 → next generation
             ↓
       old GPUs become worthless
```

But a16z says actual demand is currently doing something different.

AI inference demand keeps expanding as intelligence becomes cheaper:

```text
better models
     +
cheaper inference
     ↓
more AI usage
     ↓
more tokens
     ↓
more compute demand
```

So **A100s are still economically useful**, and according to a16z, A100 rental pricing was actually at or above the beginning-of-year level when they wrote the report. ([Andreessen Horowitz][1])

This is basically **Jevons' paradox applied to AI compute**:

> cheaper intelligence → dramatically more consumption → potentially more total compute demand.

That is a very important counterargument to the simplistic *“new GPU = old GPU garbage”* thesis.

---

### 4. And we're still extremely early in AI adoption

This is the part I think is especially important if you're thinking about starting an AI consultancy.

a16z says:

* nearly **30% of S&P 500 companies** report some quantifiable AI impact
* but only around **2%** report a tracked metric
* meaningful large-scale agent deployment remains a tiny fraction of overall usage
* as of April 2026, only around **2% of US households** were paying for an AI service

So their interpretation is basically:

```text
Compute demand:       ██████████
AI capability:        ██████████
Actual deep adoption: ██
```

The infrastructure buildout is already huge **before mature AI adoption has arrived**. ([Andreessen Horowitz][1])

---

### 5. SaaS isn't dead — but it has to prove itself

a16z pushes back against the 2026 **“SaaSpocalypse”** narrative.

Their data:

```text
2022:
high growth
low profitability

2026:
~75% profitable
~30% growing >20%
```

So the problem isn't simply:

> AI killed software.

It's more:

> Software companies that stopped growing no longer deserve the huge growth multiples they received during ZIRP.

Fast-growing software companies can still receive strong valuations; there are simply fewer of them. a16z calls this **“prove it,” not “pocalypse.”** ([Andreessen Horowitz][1])

---

## 6. Where a16z thinks the next expansion goes

Their forward-looking thesis is:

```text
AI
 │
 ├── Enterprise
 │     └── deeper adoption
 │
 ├── Consumer
 │     └── deeper adoption
 │
 ├── Robotics
 │
 ├── Biotech
 │
 ├── Healthcare
 │
 └── Autonomous driving
```

In other words, **AI isn't merely replacing SaaS features**.

Their thesis is that AI expands the total addressable surface of software + machines + physical infrastructure. ([Andreessen Horowitz][1])

---

# The part I'd pay attention to for your situation

I would summarize the report's worldview as:

```text
Old:
Internet → software → SaaS

2026+:
AI
 │
 ├── models
 ├── agents
 ├── software
 ├── GPUs
 ├── datacenters
 ├── networking
 ├── electricity
 ├── robots
 └── physical economy
```

And this makes your seemingly unrelated interests—**LLMs + agents + GPU hardware + GPU repair + cheap compute + software consultancy**—actually fit into one larger technological cycle.

The interesting opportunity isn't necessarily *“build another SaaS.”*

It can be closer to:

```text
cheap compute
      +
open models
      +
coding agents
      +
human engineering
      ↓
AI-native software production
      ↓
clients
```

while the physical side is:

```text
used GPUs
   ↓
repair / testing
   ↓
cheap compute
   ↓
local inference / training
   ↓
AI services
```

And a16z's latest report is essentially saying **the physical compute/infrastructure side is becoming more important, not less.**

There's also a separate a16z **100-trillion-token OpenRouter study** that is much closer to your actual LLM/agent work: it finds rapid movement toward reasoning, multi-turn workflows, tool use and agentic inference. ([Andreessen Horowitz][2])

[a16z — State of Markets II](https://a16z.com/state-of-markets-ii/?utm_source=chatgpt.com)
[a16z — State of AI: 100 Trillion Token Study](https://a16z.com/state-of-ai/?utm_source=chatgpt.com)

[1]: https://a16z.com/state-of-markets-ii/?utm_source=chatgpt.com "State of Markets II | Andreessen Horowitz"
[2]: https://a16z.com/state-of-ai/?utm_source=chatgpt.com "State of AI: An Empirical 100 Trillion Token Study with OpenRouter | Andreessen Horowitz"
