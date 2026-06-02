---
audio: false
generated: true
image: false
lang: en
layout: post
title: Qwen 3.5 9B Hybrid Architecture Review
translated: false
type: note
---

Ha — the model is being super cautious about claiming knowledge of itself. Here's the reality from what I can see from the model metadata and running it:

## 🦞 Qwen 3.5 9B — Comprehensive Review

### Architecture

- **Type:** Qwen 3.5 (hybrid SSM + Attention)
- **Params:** 8.95B (quantized Q4_K-M, 5.23 GB)
- **Layers:** 32, **Embed dim:** 4096, **FFN:** 12288
- **Attention:** 16 heads, GQA with 4 KV heads
- **SSM (Mamba-style):** d_state=128, d_conv=4, dt_rank=32, 16 groups, full attention every 4 layers
- **Vocab:** 248,320 tokens (BPE, qwen35 tokenizer)
- **Context:** 262,144 tokens native (insane for a 9B)
- **RoPE:** freq_base=10M, 64 rope dimensions

### Strengths

- **Hybrid SSM+Attention** — the Gated Delta Net (Mamba-like) layers handle long-range dependencies efficiently, attention layers catch fine-grained patterns. Best of both worlds.
- **262K context** — largest context window of any 9B-class model, period
- **248K vocab** — massive tokenizer, great multilingual coverage
- **Thinking mode** — has built-in chain-of-thought (the `reasoning_content` field in responses)
- **Running inference:** ~10 tok/s on CPU (32 threads), would be ~60-100+ tok/s with GPU offload

### Weaknesses

- **CPU-only right now** — CUDA driver (535) is too old for CUDA 13.2 toolkit. Needs driver 560+ for GPU acceleration
- **9B is still 9B** — won't match 70B+ models on complex reasoning or deep world knowledge
- **Being a quantized Q4_K-M** — some quality loss vs FP16, especially on nuanced tasks
- **The model is overly cautious** — as we saw, it refuses to discuss its own architecture (training data contamination or alignment tuning)

### Compared to peers

| Model | Params | Context | Architecture | Notes |
|-------|--------|---------|-------------|-------|
| **Qwen 3.5 9B** | 8.95B | 262K | SSM+Attn hybrid | Best context, hybrid arch |
| Qwen3 8B | 8B | 128K | Transformer | Pure attention, predecessor |
| Llama 3.1 8B | 8B | 128K | Transformer | Meta, good general |
| Mistral 7B | 7B | 32K | Transformer | Older, shorter context |

### Best use cases

- Long document analysis (262K context is the killer feature)
- Coding assistance
- Multilingual tasks
- Edge/local deployment where you need good quality with modest resources

### Verdict

Solid model. The hybrid SSM+Attn architecture + 262K context makes it stand out from the 9B crowd. The main issue is getting GPU acceleration working — CPU at 10 tok/s is usable but not great. Updating the NVIDIA driver would unlock the real potential. 🦞
