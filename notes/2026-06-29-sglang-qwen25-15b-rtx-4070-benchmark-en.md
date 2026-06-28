---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Qwen2.5-1.5B RTX 4070 Benchmark
translated: false
type: note
---

Here's the full breakdown:

```
SGLang Benchmark — Qwen2.5-1.5B-Instruct on RTX 4070
======================================================

Topic        TTFT(ms)   Total(ms)  Tokens   Tok/s    Quality
────────────────────────────────────────────────────────────────
Math         8453       9175       100      10.9     ok (truncated)
Coding       17         2196       300      136.6    has function
Reasoning    17         497        66       132.8    correct
Creative     17         125        15       119.6    haiku ok
Factual      17         716        96       134.1    covers both
Translation  17         147        18       122.2    correct (FR)
Summarize    17         373        49       131.3    ok
```

**Key findings:**

1. **TTFT (Time to First Token):**
   - First request: **8.5 seconds** — cold start (CUDA graph capture, KV cache allocation). This only happens once.
   - After warmup: **~17ms** — essentially instant. SGLang's radix tree KV cache kicks in.

2. **Throughput:** **~120-137 tok/s** generation speed after warmup. For a 1.5B model on RTX 4070, this is decent — the bottleneck is the small model, not the framework.

3. **Quality assessment (1.5B model):**
   - Math: Correctly breaks down 17×23 but hit 100-token limit before finishing (answer = 391)
   - Coding: Produces a real function with docstring, uses dynamic programming approach
   - Reasoning: Gets the right answer (9 sheep), correct step-by-step
   - Creative: Decent haiku — "Data flows like rivers / Models learn from patterns / Wisdom blooms"
   - Factual: Accurate TCP vs UDP bullets with proper terminology
   - Translation: Perfect French — "Le renard brun rapide saute par-dessus le chien paresseux"
   - Summarize: Solid ELI5 explanation of relativity

4. **The real value of SGLang** isn't single-user latency — it's concurrent throughput. With 1 user it's ~130 tok/s; with 10 concurrent users, SGLang's continuous batching keeps throughput high where naive servers would choke. Also, swap to Qwen2.5-7B for noticeably better quality (uses ~8 GB VRAM, still fits your 12 GB card).

Want me to test with a bigger model, or set it up so your Mac can reach it as an OpenAI-compatible endpoint (e.g., point `ww` LLM commands at it)?
