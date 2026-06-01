---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Parameter Memory Requirements Explained
translated: false
type: note
---

Good question. That was all from my own knowledge — no web search.

The key pieces:

1. **Chinchilla scaling law** (Hoffmann et al., 2022) — "optimal tokens ≈ 20× params" is well-established, from my training data. No search needed.

2. **Memory formula** — per-param memory in bf16+Adam is standard systems knowledge: 2 (bf16) + 4 (fp32 master) + 4 (m) + 4 (v) + 2 (grad) = 16 bytes/param. This is basic PyTorch training internals.

3. **GPT-2 architecture** — param count formula is `12 × n_layer × n_embd²` for transformer blocks + `vocab_size × n_embd` for embeddings. For 3B: 12 × 48 × 2560² ≈ 377M per layer × 48 ≈ 3B. Standard knowledge.

4. **LLaMA-1 over-training** — LLaMA-1 7B trained on 1T tokens (vs Chinchilla-optimal ~140B) showed over-training helps. This is from the LLaMA paper (Feb 2023).

**What could be stale:**
- I don't know if there are newer scaling laws post-Chinchilla that change the recommendation
- MI300X specific performance characteristics (flops, memory bandwidth) — I estimated from general HBM3 knowledge
- Newer training techniques (e.g., muP, Sophia optimizer) that might change LR/optimizer choices

**What I'd search for if you want to go deeper:**
- MI300X actual TFLOPS in bf16 to estimate training time
- Whether Karpathy's nanoGPT has been updated with 3B+ configs
- Latest scaling law papers (2024-2025)

Want me to search any of these?