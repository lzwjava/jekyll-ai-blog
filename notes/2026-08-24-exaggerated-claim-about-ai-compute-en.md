---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exaggerated Claim About AI Compute
translated: false
type: note
---

Question: **Is the claim “OpenAI bought all the computing power on Earth” true? How much of this article is accurate?**

Answer:

Short answer: **the headline is exaggerated.** The underlying idea — **OpenAI believes compute is the bottleneck and is aggressively securing future AI infrastructure** — is broadly true. But “买下地球上所有的算力” (“bought all compute on Earth”) is clickbait, not a literal fact.

Let's separate facts from hype.

## 1. “OpenAI wants to buy as much compute as possible” — mostly true

Greg Brockman and OpenAI leadership have repeatedly emphasized that **compute availability is a strategic constraint**.

The logic:

```
AI capability ∝ model size × data × compute × algorithmic improvements
```

For frontier models:

* Training requires enormous GPU clusters.
* Inference demand grows after deployment.
* Agent workloads are much more expensive than chat.

A normal ChatGPT query:

```
user → model → answer → done
```

An agent:

```
goal
 ↓
planning
 ↓
tool calls
 ↓
code execution
 ↓
verification
 ↓
iteration
 ↓
final answer
```

One agent task can consume tens/hundreds/thousands of times more inference tokens.

So the argument:

> "Today's AI usage is tiny compared with future agent usage"

is reasonable.

---

## 2. “Buy all the compute on Earth” — no

There is no evidence that OpenAI literally controls all global compute.

Global AI compute is distributed among:

* NVIDIA customers
* cloud providers:

  * Microsoft
  * Amazon Web Services
  * Google Cloud
* Chinese AI companies
* universities
* government labs
* crypto/mining converted clusters
* private enterprises

OpenAI is one of the biggest buyers, but not the owner of all AI hardware.

A more accurate statement:

> OpenAI is trying to secure a very large fraction of future frontier AI compute.

---

## 3. H100 price increasing after H200/B200/GB200 — plausible

This part is actually interesting.

Normally:

```
new GPU released
      ↓
old GPU price drops
```

Example:

```
RTX 4090 → RTX 5090
```

But AI GPUs behave differently:

```
demand growth > supply growth

H100
 |
 | demand remains huge
 |
price stays high
```

Reasons:

* New GPUs are supply constrained.
* Existing clusters cannot be replaced instantly.
* Software stacks are optimized around CUDA/Hopper.
* Companies need capacity immediately.

So old AI hardware can retain value.

---

## 4. The “Jevons paradox” argument is correct

The article explains an important economic effect.

Example:

Before:

```
GPT-4 level intelligence:
$1 / million tokens
```

Later:

```
same intelligence:
$0.01 / million tokens
```

People think:

> AI becomes cheaper, companies earn less.

But historically:

```
lower cost
    ↓
more users
    ↓
more applications
    ↓
more total consumption
```

Examples:

* CPU became cheaper → billions of computers.
* Internet bandwidth became cheaper → video streaming exploded.
* Storage became cheaper → cloud storage exploded.

AI may follow a similar pattern.

---

## 5. The biggest questionable part: “medical examples become normal”

This is where the article becomes promotional.

AI medical assistance is real:

* literature search
* diagnosis support
* drug discovery
* patient communication

But:

```
AI gives medical suggestion
        ≠
AI replaces doctors
```

Healthcare has:

* regulation
* liability
* incomplete data
* safety requirements

Progress will likely be gradual.

---

## 6. The real strategic picture

The important takeaway is not “OpenAI bought Earth compute”.

The real battle is:

```
               AI race

      Algorithms
          +
        Data
          +
        Compute
          +
      Distribution
          +
      Energy
          +
    Manufacturing
```

Compute is becoming like oil in the industrial era.

The frontier companies are competing for:

```
chips
 ↓
datacenters
 ↓
electricity
 ↓
networking
 ↓
talent
 ↓
customers
```

This is why you see:

* NVIDIA becoming one of the world's most valuable companies.
* Microsoft investing heavily in OpenAI.
* Google building TPU infrastructure.
* Amazon building Trainium.
* Meta buying thousands of GPUs.

---

For someone doing AI infra/LLM engineering, the important implication is:

**The bottleneck is moving from "can you train a model?" to "can you efficiently operate intelligence at massive scale?"**

The valuable engineering areas are likely:

* inference optimization
* distributed training
* GPU utilization
* CUDA/ROCm
* serving systems
* agent infrastructure
* data pipelines

The article exaggerates the headline, but the underlying thesis — **compute is becoming the strategic resource of the AI era** — is largely correct.
