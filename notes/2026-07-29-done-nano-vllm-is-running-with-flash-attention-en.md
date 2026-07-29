---
audio: false
generated: true
image: false
lang: en
layout: post
title: Done! nano-vllm is running with flash-attention
translated: false
type: note
---

✅ **Done!** nano-vllm is running with flash-attention.

Here's the full summary of what was accomplished:

---

## What happened

### 1. Installed `flash-attn==2.8.3` (prebuilt wheel)

- Avoided 20+ min CUDA compilation
- Used the `cu13torch2.10` wheel — CUDA 13.0 matches your PyTorch 2.11.0+cu130
- Import verified ✓

### 2. Changed attention to use flash-attn directly

**File:** `/mnt/data/nano-vllm/nanovllm/layers/attention.py`

| Before | After |
| -------- | ------- |
| `F.scaled_dot_product_attention` | `flash_attn_func` |
| Manual per-seq causal mask loop | `flash_attn_varlen_func` |
| Transpose (batch, heads, seq, dim) | Native (batch, seq, heads, dim) |

### 3. Ran inference ✅

**Model:** Qwen3-0.6B on RTX 4070

| Metric | Value |
| -------- | ------- |
| Prefill | 506 tok/s |
| Decode | ~4–30 tok/s |
| Prompts | 2, 256 tokens each |
| Result | Both completions generated correctly ✓ |
