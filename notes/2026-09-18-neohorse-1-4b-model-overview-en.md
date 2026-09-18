---
audio: false
generated: true
image: false
lang: en
layout: post
title: NeoHorse-1-4B Model Overview
translated: false
type: note
---

**Question:** What is the NeoHorse-1-4B model on Hugging Face?

**Answer:**

NeoHorse-1-4B is a ~4 billion parameter causal language model developed by **TokenRhythm**, released in September 2026. Here's a summary of what it is:

**Origin & Base Model**
It is post-trained from **Qwen3.5-4B** (by Alibaba Cloud) and fine-tuned by TokenRhythm. This release contains language-model weights only — vision weights are not included. The repackaging changes configuration and tensor key names without altering the fine-tuned tensor values.

**Core Goal: Recursive Self-Improvement (RSI)**
NeoHorse-1-4B is an initial prototype on the path toward **recursive self-improvement (RSI)**. The routing harness assigns tasks to a heterogeneous model pool, records tool interactions and outcomes, estimates capability demand, and uses capability-level feedback to shape the next training mixture. Updated models can return to the harness, closing a prototype evaluation–selection–update loop.

**Capabilities**
It is designed for:
Text-based **agent harnesses**, **tool use**, **coding**, and **instruction following**.

**Key Specs**

| Property | Value |
|---|---|
| Parameters | ~4B |
| Context Length | 262,144 tokens (extensible to ~1M) |
| Format | Safetensors / BF16 |
| License | Apache 2.0 |

**Performance**
It achieves a **64.87 macro average** across ten benchmarks, compared to 58.94 for the base Qwen3.5-4B — a gain of **+5.93 points**. It ranks best overall among the five compared models in the 4B class.

**References:**
- [TokenRhythm/NeoHorse-1-4B on Hugging Face](https://huggingface.co/TokenRhythm/NeoHorse-1-4B)
- [Technical Report (arXiv:2609.08183)](https://arxiv.org/abs/2609.08183)
- [GitHub Repository](https://github.com/TokenRhythm/NeoHorse)
