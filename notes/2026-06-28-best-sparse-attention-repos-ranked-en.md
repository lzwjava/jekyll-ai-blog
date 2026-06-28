---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Sparse Attention Repos Ranked
translated: false
type: note
---

Here are the repos worth your time, ranked by signal-to-noise for actually understanding the mechanics:

## Original / canonical

**[openai/sparse_attention](https://github.com/openai/sparse_attention)** — Child et al.'s own reference implementation. Small, readable. The `attention.py` has the strided/fixed patterns directly. This is the primary source — read it first. Note it's TF1-era so you won't run it, but the pattern logic is what matters.

## For the kernels (the part that makes it real)

**[openai/triton](https://github.com/openai/triton)** — the `python/tutorials/06-fused-attention.py` tutorial is the canonical block-sparse/fused attention walkthrough in Triton. This is where "fused block-sparse GPU kernels" stops being a phrase and becomes code you can modify. Directly relevant to your CUDA/inference-optimization interest.

**[Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)** — not sparse per se, but FlashAttention is the IO-aware tiling idea that superseded the "recompute to save memory" trick from the Sparse Transformer paper. Read `flash_attn/flash_attn_triton.py` to see the modern version of what Child et al. were reaching for. Essential lineage.

## For the lineage forward

**[lucidrains repos]** — Phil Wang reimplements basically every attention variant in clean minimal PyTorch:
- [sparse-attention](https://github.com/lucidrains/sinkhorn-transformer) and the routing/reformer ones
- [routing-transformer](https://github.com/lucidrains/routing-transformer) — content-based clustering branch
- [reformer-pytorch](https://github.com/lucidrains/reformer-pytorch) — LSH bucketing branch

These are the best way to see the *content-agnostic vs content-based* fork in actual code, side by side. ~200 lines each, no infra.

**[allenai/longformer](https://github.com/allenai/longformer)** and **[google-research/bigbird](https://github.com/google-research/bigbird)** — the direct generalizations of fixed-pattern attention (local + global + random). BigBird's `bigbird/core/attention.py` shows how the fixed patterns got combined.

## My recommendation for your workflow

Given you learn by building: skip straight to the **Triton fused-attention tutorial** and **lucidrains' minimal reimplementations**. Clone both, run on your 4070, then port the `strided_mask` sketch above into a working block-sparse attention layer. That's a tight afternoon project that teaches you more than reading all six papers.

Want a minimal nanoGPT-style training script that swaps in block-sparse attention so you can benchmark it against dense on your hardware?
