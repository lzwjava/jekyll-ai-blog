---
audio: false
generated: true
image: false
lang: en
layout: post
title: Together AI Inference Optimization
translated: false
type: note
---

**Question:** What does Tri Dao work on at Together AI to optimize inference?

**Answer:**

Tri Dao is co-founder and chief scientist of Together AI, and also an Assistant Professor at Princeton. His research sits at the intersection of ML and systems, focusing on hardware-aware algorithms and sequence models.

Here's what he's actually doing at Together AI on inference:

---

## 1. FlashAttention Series (Core Work)

The whole FlashAttention line is his main contribution — and it's now the backbone of nearly every serious inference stack.

**The core insight:** Standard attention reads Q, K, V from HBM (slow), computes attention scores, writes back to HBM, reads again for softmax — massive memory bandwidth waste. FA tiles the computation into SRAM-resident blocks, fusing the entire QK^T → softmax → V matmul into a single kernel pass, cutting HBM round-trips from O(N²) to O(N).

**FlashAttention-2:** Rewritten from scratch using NVIDIA's CUTLASS 3.x and CuTe primitives. ~2x faster than FA1, reaching up to 230 TFLOPs/s on A100 (FP16/BF16), with 72% model FLOPs utilization for end-to-end GPT training.

**FlashAttention-3 (H100-specific):** FA2 achieved only 35% utilization of theoretical max FLOPs on H100. FA3 exploits Hopper-specific async instructions — WGMMA (warp group matrix multiply-accumulate) and TMA (Tensor Memory Accelerator) — to overlap operations. Goes from ~350 TFLOPS (FA2 FP16 forward) to ~540-570 TFLOPS. The key technique is **warp specialization**: separate producer warps issue TMA loads while consumer warps run WGMMA, hiding memory latency behind compute.

**FlashAttention-4 (Blackwell):** On Blackwell, MMA accumulators live in TMEM (not registers like Hopper), making it practical to keep multiple MMAs in flight while CUDA cores handle element-wise work (softmax, dS). The key backward pass overlap: while computing softmax for tile j, dK and dQ MMAs for tile j-1 are already issued.

---

## 2. Together Kernel Collection

At the heart of Together AI's infrastructure is the Together Kernel Collection — described as "a breakthrough in AI system optimization developed under the leadership of Chief Scientist Tri Dao." It delivers 2-3x faster inference than hyperscaler solutions. This collection likely packages FA + custom decode kernels + MoE routing kernels under one roof.

---

## 3. Three Inference Regimes (His Framework)

Tri Dao identifies three distinct inference optimization targets:
- **Chatbot workloads** — fast enough to feel responsive but not instantaneous, maintaining natural UX
- **Low-latency ultra-fast inference** — for coding assistants (like Claude Code) or agentic tasks, where users pay a premium to stay in flow
- **Maximum throughput / large batch** — synthetic data generation and RL training rollouts (sampling many trajectories)

Each regime needs different kernel/scheduling strategies — not one-size-fits-all.

---

## 4. Hybrid Mamba-Transformer + Marconi Prefix Caching

Hybrid Mamba-Transformer models now match or exceed leading open models while delivering faster inference and million-token context. The Mamba SSM component reduces the quadratic KV cache cost for long contexts during decode.

From his publications page: **Marconi: Prefix Caching for the Era of Hybrid LLMs** and **Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining** are recent papers from his group — both squarely targeting inference throughput. The expert activation paper is particularly relevant given DeepSeek-style MoE deployment.

---

## TL;DR Stack

| Layer | What he does |
|---|---|
| Attention kernel | FlashAttention 1/2/3/4 — SRAM tiling, IO-awareness, Hopper/Blackwell async |
| Architecture | Mamba/SSM hybrids to kill quadratic KV cache growth |
| MoE | Opportunistic expert activation for faster decode |
| KV cache | Marconi prefix caching for hybrid LLMs |
| System | Together Kernel Collection, targeting 3 inference regimes |

The throughput numbers matter for you concretely: if you're doing RL rollouts or synthetic data gen on your MI300X, FA3/FA4 equivalents (ROCm port of flash-attn exists at `Dao-AILab/flash-attention`) are worth checking — they're the difference between 35% and 75%+ HBM utilization on the attention layer.

**References:**

- [FlashAttention-3 blog](https://tridao.me/blog/2024/flash3/)
- [FlashAttention-4 blog](https://tridao.me/blog/2026/flash4/)
- [Together AI Series B announcement](https://www.prnewswire.com/news-releases/together-ai-raises-305m-series-b-to-scale-ai-acceleration-cloud-for-open-source-and-enterprise-ai-302380967.html)
- [Tri Dao publications](https://tridao.me/publications/)
- [Three inference regimes (X thread)](https://x.com/elliotarledge/status/1970417395476111809)
