---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inference vs Pretraining Career Path
translated: false
type: note
---

**Question:** Is working on LLM inference/serving infrastructure (vLLM, SGLang, llama.cpp) a better career/learning direction than LLM pretraining?

**Answer:**

Depends what you mean by "better" — but let me give you a sharp take for your specific trajectory.

## The Honest Comparison

| Dimension | Inference/Serving | Pretraining |
| --- | --- | --- |
| Feedback loop | Minutes to hours | Days to weeks |
| Hardware cost | RTX 4070 is enough | Need A100/H100 clusters |
| Job market | **Huge right now** | Narrow (OpenAI, Anthropic, DeepSeek) |
| Depth ceiling | Very high | Highest |
| Transferability | Broad | Narrow |
| Your current setup | ✅ fits | ⚠️ limited |

## Why Inference Is Underrated

Most people think pretraining = more prestigious. That's wrong in practice. The systems problems in inference are **legitimately hard**:

- **vLLM's PagedAttention** — KV cache is the bottleneck; paging it like virtual memory is non-obvious
- **Continuous batching** — request scheduling under dynamic sequence lengths is a real systems problem
- **SGLang's RadixAttention** — prefix caching across requests, KV reuse, this is novel research
- **llama.cpp's quantization** — GGUF, k-quants, understanding how 4-bit GPTQ vs AWQ vs GGUF differ in quality/speed tradeoffs
- **Speculative decoding** — draft model + verification, reduces latency 2-3x, deep transformer internals required

These aren't "glue code" problems. They require knowing attention math, memory bandwidth math, CUDA kernels, and distributed systems simultaneously.

## What You'd Learn in Inference That Compounds

```
Transformer internals
    → KV cache mechanics (shape: [layers, heads, seq_len, head_dim])
    → Attention complexity O(n²) → why sequence length kills you
    → FlashAttention: fused kernel, tiling, avoid HBM round-trips

Systems
    → CUDA memory hierarchy (HBM → L2 → SRAM)
    → Tensor parallelism (split heads across GPUs)
    → Pipeline parallelism (split layers)
    → Prefill vs decode phases (compute-bound vs memory-bound)

Quantization
    → Post-training quantization math
    → Calibration datasets, perplexity impact
    → GPTQ, AWQ, SmoothQuant internals
```

All of this **directly transfers** to understanding pretraining too — because pretraining is just a forward+backward pass, and you already understand the forward pass deeply from inference.

## The Strategic Answer for You

Given your setup (RTX 4070, MI300X access, already training GPT-2 scale):

**Do inference first as your daily driver, pretraining as your weekend project.**

Inference gives you:

- Fast experiments (ship a custom vLLM scheduler in a day)
- Directly applicable at your bank job (serving, latency, cost optimization)
- Skills that transfer to building agents/tools (your `ww`, `zz`, `iclaw` tools)
- A path to contributing to vLLM/SGLang (both are very active OSS, well-funded)

Pretraining gives you:

- Deep understanding of loss landscapes, data pipelines, tokenization
- But requires scale to see interesting results — GPT-2 760M is the floor

## Concrete Ramp for You

```bash
# Week 1-2: vLLM internals
git clone https://github.com/vllm-project/vllm
# Read: vllm/core/scheduler.py — continuous batching logic
# Read: vllm/attention/backends/flash_attn.py — PagedAttention impl

# Week 3-4: SGLang
git clone https://github.com/sgl-project/sglang
# Read: sglang/srt/managers/radix_cache.py — RadixAttention
# Experiment: prefix caching benchmarks on your 4070

# Week 5-6: llama.cpp
git clone https://github.com/ggerganov/llama.cpp
# Read: ggml-cuda.cu — how CUDA kernels are hand-written
# Experiment: quantize a 7B model, measure perplexity vs speed

# Then: contribute a small PR to vLLM or SGLang
```

## Bottom Line

Inference/serving is **not easier** — it's differently hard, with faster feedback. For your situation it's the better primary track because the compounding is faster and you can do real experiments on hardware you already have. Pretraining knowledge comes for free as a byproduct once you deeply understand the forward pass from the inference side.

The Karpathy path: understand every line of the forward pass → that's inference. The pretraining is just `loss.backward()` on top.
