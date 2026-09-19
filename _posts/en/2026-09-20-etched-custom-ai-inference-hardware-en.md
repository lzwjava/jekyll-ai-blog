---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Etched: Custom AI Inference Hardware"
translated: false
type: note
---

Question: **What does Etched do?**

Answer: **Etched is building custom AI inference hardware—basically an alternative to NVIDIA GPUs for serving large AI models.**

The interesting part is that they're attacking the problem at the **ASIC + rack + memory + software** level rather than making another programmable GPU.

### The original idea: hard-code the Transformer

Etched started with **Sohu**, an ASIC specialized for Transformer inference.

Instead of:

```text
GPU
 ├── CUDA
 ├── Tensor cores
 ├── lots of general-purpose machinery
 └── can run many kinds of workloads
```

their philosophy was:

```text
                 Transformer inference
                         │
                         ▼
              ┌───────────────────┐
              │   Etched ASIC      │
              │  specialized HW    │
              └───────────────────┘
                         │
                         ▼
                 tokens / second
```

The bet was essentially:

> Transformers are important enough that we should **throw away programmability** and build silicon specifically for the computation they perform.

That's why the original Sohu was deliberately unable to run CNNs, LSTMs, etc. Etched claimed an 8-chip Sohu server could produce **500K+ tokens/sec on Llama 70B**, with enormous claimed advantages over H100/B200-class GPU servers. Those were company benchmarks, so they shouldn't be treated as independently validated numbers. ([TechCrunch][1])

### But the 2026 Etched is broader

This is the important update if you've only seen the old Sohu story.

Their current website no longer positions the company simply as "a Transformer ASIC company." It calls the product:

> **Frontier Inference Clusters**

They are co-designing:

```text
                ┌──────────────────────────┐
                │      Etched rack         │
                │                          │
model ────────► │  ASICs                   │
                │  SRAM + HBM              │
                │  interconnect             │
                │  compiler/runtime         │
                │  power delivery           │
                │  cooling                  │
                │  packaging                │
                └──────────────────────────┘
                           │
                           ▼
                    inference tokens
```

Etched says its A0 silicon has returned from TSMC N4P and that it's validating its first rack-scale product with customers. ([Etched][2])

Two particularly interesting architectural ideas they're currently advertising are:

**1. Low Voltage Inference (LVI)**

They claim to operate their math units at less than half the voltage of typical AI chips, allowing higher compute density before thermal throttling. ([Etched][2])

**2. Cluster Scale Memory (CSM)**

This is arguably more interesting for inference.

Decode is often **memory/latency bound**, rather than simply FLOP-bound:

```text
decode:

KV cache ──► memory ──► weights ──► matmul ──► token
                 ▲
                 │
          bandwidth / latency
```

Etched is building a shared memory system combining **HBM + SRAM + a custom low-latency interconnect**, trying to get something closer to SRAM-like access latency without giving up HBM-like capacity. ([Etched][2])

### So what's the actual business?

Think of the stack like this:

| NVIDIA     | Etched                         |
| ---------- | ------------------------------ |
| GPU        | Specialized ASIC               |
| CUDA       | Specialized inference software |
| HGX/DGX    | Custom inference rack          |
| HBM        | HBM + SRAM architecture        |
| NVLink     | Custom interconnect            |
| GPU server | Whole inference cluster        |

So they're not really selling "a faster chip."

They're trying to sell **$/token, tokens/sec, latency, and watts/token for frontier-model inference**.

That's a much more interesting framing.

And it's why the company is now talking about **rack-scale systems** rather than just Sohu. Their own site says they are targeting trillion-parameter sparse MoEs, long-context workloads, and agentic workloads. ([Etched][2])

For someone building inference infrastructure, the key question isn't *"Is their ASIC faster than H100?"* It's **whether they can beat GPUs on end-to-end cost/token once you include memory capacity, utilization, batching, KV-cache behavior, networking, model changes, and software/compiler constraints.**

[Etched official site](https://www.etched.com/?utm_source=chatgpt.com)

References:

* [Etched — Frontier Inference Clusters](https://www.etched.com/?utm_source=chatgpt.com) ([Etched][2])
* [TechCrunch — Etched's original Transformer-only ASIC](https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/?utm_source=chatgpt.com)
* [Etched's original Sohu announcement coverage](https://threadreaderapp.com/thread/1805625693113663834.html?utm_source=chatgpt.com)

I can also break down **how Sohu could theoretically get 10–20× the throughput of an H100**, starting from the Transformer forward pass and mapping each operation onto ASIC hardware.

[1]: https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/?utm_source=chatgpt.com "Etched is building an AI chip that only runs one type of model | TechCrunch"
[2]: https://www.etched.com/ "Etched"
