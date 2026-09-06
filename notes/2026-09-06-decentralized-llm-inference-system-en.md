---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decentralized LLM inference system
translated: false
type: note
---

**BloomBee** is a decentralized system for serving large language model (LLM) inference over a peer-to-peer network.

**Core idea:** Instead of needing one powerful GPU machine to host a huge model (e.g., LLaMA 3.1 405B), BloomBee splits the model's transformer blocks across many peers — each hosting just a few layers — and they collaboratively serve inference requests over the internet. This leverages idle GPU resources for cost-effective LLM access.

**Key challenges it tackles** (inter-node bandwidth + per-node memory):
- **Tensor offloading** — each peer holds more layers, reducing network hops
- **Speculative decoding** — sends multiple draft tokens per round-trip to cut communication frequency
- **Lossless activation compression** — fewer bytes per activation without accuracy loss
- **Micro-batch pipelining** — overlaps communication with computation to hide latency

**Structure:** It's a Python project (`src/`, `tests/`, `benchmarks/`, `examples/`, Docker support), published on PyPI, built on top of the *hivemind* P2P framework, with an associated research paper on arXiv. It looks like a fork/evolution of ideas from Petals-style distributed inference.

Want me to dig into any specific part, like the architecture in `src/` or how the speculative decoding works?
