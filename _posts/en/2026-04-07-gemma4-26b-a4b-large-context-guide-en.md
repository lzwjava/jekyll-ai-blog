---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4 26B A4B Large Context Guide
translated: false
type: note
---

Question: Can we set the context size to 16384 for the Gemma 4 26B A4B running on llama-server with `-ngl 25` and a 12GB VRAM GPU?

Answer:

## Short Answer: Yes — But You Need KV Cache Quantization

Good news: **Gemma 4 26B A4B has a huge architectural advantage** for large context sizes thanks to its Sliding Window Attention (SWA) design. Going from 2048 → 16384 context will cost **much less VRAM than you'd expect** compared to a regular model.

---

## Why Gemma 4 26B A4B Is Good for Large Context

Gemma 4 26B A4B uses a **5:1 local/global attention pattern**:
- **25 local layers** → use SWA with only a **1024-token sliding window** (not the full context!)
- **5 global layers** → full attention over the entire context

The KV cache formula for Gemma 4 26B-A4B works out to approximately **5.20 GiB at max context** in bf16, because the sliding layers only cache 1024 tokens, not the full sequence.

This means scaling from 2048 → 16384 context mostly only grows the KV cost for those **5 global layers**, not all 30 layers.

---

## VRAM Estimate at 16384 Context

Your current state:
- Model weights on GPU (25 layers): ~9.5 GB
- Available headroom: ~2.5 GB

**KV cache at 16384 tokens (FP16, no quantization):**
- 5 global layers × full 16384 tokens = relatively modest
- 25 local layers × only 1024-token window (SWA) = fixed small cost

According to community testing on the 31B model (which has similar architecture), llama.cpp shows about 22.3 GB VRAM usage at 16384 context with FP16 KV cache — but that is the much larger 31B dense model. For the 26B MoE which is far more KV-efficient, the cost is significantly lower.

**The risk is that FP16 KV at 16384 context may still OOM on 12GB.** The safe approach is to quantize the KV cache.

---

## Recommended Config

```bash
./llama-server \
  -m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  -ngl 25 \
  -c 16384 \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  --host 0.0.0.0 \
  --port 8081 \
  --path ./tools/server/public
```

Dropping KV cache from FP16 to Q4 saves about 1.8 GB of VRAM at 16K context with essentially no perceptible quality degradation (BLEU score impact around -0.3%).

If `q8_0` still OOMs, go more aggressive:

```bash
  --cache-type-k q4_0 \
  --cache-type-v q4_0 \
```

---

## Optional: Limit Parallel Sequences

If you are the only user, add `-np 1` to your llama.cpp config — this reserves space for a single SWA KV instead of the default 4, saving significant VRAM.

```bash
./llama-server \
  -m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  -ngl 25 \
  -c 16384 \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  -np 1 \
  --host 0.0.0.0 \
  --port 8081 \
  --path ./tools/server/public
```

---

## What to Watch For

| Signal | Meaning |
|--------|---------|
| OOM on startup | Reduce to `-c 8192` or use `q4_0` KV cache |
| OOM mid-inference | Add `-np 1`, reduce `-ngl` to 23 |
| Slower speed | Expected — larger context = more compute per token |
| Still ~38 t/s | Great sign — SWA keeps speed relatively stable |

---

## TL;DR Strategy

1. **Try first:** `-c 16384 --cache-type-k q8_0 --cache-type-v q8_0 -np 1`
2. **If OOM:** switch to `--cache-type-k q4_0 --cache-type-v q4_0`
3. **If still OOM:** reduce `-ngl` from 25 to 22–23 and retry

The SWA architecture of Gemma 4 26B A4B is specifically designed to make large context affordable — it's one of the best models for this on limited VRAM.

References:

- [Gemma 4 31B and 26B A4B: Architecture and Memory Consumption](https://kaitchup.substack.com/p/gemma-4-31b-and-26b-a4b-architecture)
- [Running Qwen2.5-32B on RTX 4060 8GB — KV cache quantization tricks](https://dev.to/plasmon_imp/running-qwen25-32b-on-rtx-4060-8gb-beating-m4-at-108-ts-with-llamacpp-11je)
- [unsloth/gemma-4-31B-it-GGUF HuggingFace discussion on context VRAM](https://huggingface.co/unsloth/gemma-4-31B-it-GGUF/discussions/2)
- [llama.cpp Advanced Guide: Quantization, GPU Layers, and Context](https://craftrigs.com/guides/llama-cpp-advanced-guide/)
