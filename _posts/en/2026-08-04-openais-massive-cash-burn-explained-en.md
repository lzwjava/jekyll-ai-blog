---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenAI's Massive Cash Burn Explained
translated: false
type: note
---

Question: **How does OpenAI burn so much cash, and what are the recent leaked financial news saying?**

Answer:

Yes. Frontier AI companies like OpenAI are extremely capital intensive. The core reason is simple:

> Training and serving frontier models is closer to running a semiconductor company + cloud provider than a normal software startup.

Recent leaked financial reports claimed OpenAI had around **$13B revenue in 2025 but ~$34B total expenses**, with a large operating loss. The reported numbers are controversial because some accounting items (such as valuation changes related to corporate restructuring) inflate headline losses, but the underlying issue is real: OpenAI spends enormous amounts of money on compute and research. ([Quartz][1])

The money goes mainly into several buckets:

---

## 1. GPU compute (the biggest one)

Every ChatGPT request requires inference compute.

Example:

```
User prompt
    |
    v
Tokenizer
    |
    v
GPU cluster
    |
    +-- Attention layers
    +-- MLP layers
    +-- KV cache memory
    |
    v
Generated tokens
```

A GPT-class model:

* hundreds of billions of parameters
* thousands to tens of thousands of GPUs
* huge networking requirements (InfiniBand / NVLink)
* continuous serving 24/7

A rough cost model:

```
Cost per token =
    GPU amortization
  + electricity
  + datacenter
  + networking
  + engineering
```

Even if one query costs only fractions of a cent, billions of queries become millions of dollars.

---

## 2. Training frontier models

Training cost is enormous.

A simplified formula:

```
Training FLOPs ≈ 6 × parameters × tokens
```

Example:

GPT-like:

```
1T parameters
× 20T tokens
× 6

≈ 1.2e26 FLOPs
```

At modern GPU efficiency, this means:

```
10,000 GPUs
× several months
```

The GPU bill alone can be hundreds of millions.

---

## 3. AI researchers are expensive

OpenAI competes with:

* Google DeepMind
* Anthropic
* Meta FAIR
* xAI
* Microsoft AI

Top researchers can cost:

```
salary
+
stock
+
compute budget
+
team
```

Total compensation can reach millions/year for key people.

---

## 4. Building infrastructure

People underestimate this.

OpenAI needs systems like:

```
                    Model
                      |
        +-------------+-------------+
        |                           |
   Training infra             Serving infra
        |                           |
   distributed PyTorch        batching
   checkpointing              KV cache
   fault recovery             quantization
   data pipelines             routing
```

This is similar to building:

* Google Search infrastructure
* AWS cloud infrastructure
* a supercomputer company

---

## 5. Data acquisition and partnerships

Large models require:

* licensed datasets
* publishers
* cloud agreements
* content partnerships

Those costs are growing.

---

## Why burn so much if revenue is already billions?

Because OpenAI is betting on a winner-takes-most market.

The strategy:

```
Spend billions now
        |
        v
Build best models
        |
        v
Get developers/users
        |
        v
Create ecosystem lock-in
        |
        v
Profit later
```

This is similar to:

* Amazon in the 2000s
* Tesla investing before profitability
* semiconductor fabs

---

## The interesting engineering question

The future may not be only "bigger models".

The economics push toward:

### 1. More efficient inference

Examples:

* quantization
* speculative decoding
* MoE models
* custom ASICs

This is why companies like Taalas are interesting.

Instead of:

```
GPU:
general compute
+
large memory
+
high power
```

future AI hardware may become:

```
ASIC:
fixed transformer workload
+
lower power
+
higher throughput
```

---

### 2. Smaller specialized models

Instead of:

```
one giant GPT model serving everything
```

we may get:

```
router
 |
 +-- coding model
 +-- vision model
 +-- reasoning model
 +-- small local model
```

Similar to CPU/GPU specialization.

---

### 3. AI agents increasing utilization

Today:

```
human asks
     |
model answers
     |
done
```

Future:

```
goal
 |
agent
 |
1000 tool calls
 |
software changes
 |
business result
```

The willingness to pay may increase dramatically.

---

My view: the leaked numbers are not surprising from an engineering perspective. Frontier AI is basically a **race to build a new computing platform**. The unusual part is that the "factory" is not a chip fab; it is a giant GPU cluster running neural networks.

The key question is not only "can OpenAI make money?" but:

```
Can intelligence become cheap enough
that every person/company consumes thousands
of AI inference operations per day?
```

If yes, today's burn looks like infrastructure investment. If no, the economics become very difficult.

References:

* ([Quartz][1])
* ([theinformation.com][2])
* ([wsj.com][3])

[1]: https://qz.com/openai-leaked-financials-losses-revenue-ipo-061626?utm_source=chatgpt.com "OpenAI 2025 financials leaked: $38.5B loss ahead of IPO"
[2]: https://www.theinformation.com/articles/openai-burned-3-7-billion-first-three-months-2026?utm_source=chatgpt.com "OpenAI Burned $3.7 Billion in First Three Months of 2026 — The Information"
[3]: https://www.wsj.com/tech/ai/openai-anthropic-ipo-finances-04b3cfb9?utm_source=chatgpt.com "An Inside Look at OpenAI and Anthropic’s Finances Ahead of Their IPOs"