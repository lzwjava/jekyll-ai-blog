---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximum Context for Gemma 4 on 12GB VRAM
translated: false
type: note
---

**Question:** What is the maximum context length I can try for Gemma 4 26B A4B on an RTX 4070 (12GB VRAM) with my current IQ3_S setup?

**Answer:**

Short answer: **neither 160K nor 80K is realistic on your 12GB VRAM with IQ3_S**. Here's the full breakdown of why, and what you *can* actually push to.

---

## Why 80K and 160K Are Out of Reach

Your setup uses `-ngl 25` to stay within VRAM, and you're already at ~10.7GB/12GB at 16K context with Q8_0 KV cache. Context length growth directly inflates the KV cache:

| Context | KV Cache (Q8_0 est.) | Total VRAM est. | Verdict |
|---|---|---|---|
| 16,384 (current) | ~4GB | ~10.7GB | ✅ Stable |
| 32,768 | ~8GB | ~14.7GB | ❌ OOM |
| 65,536 | ~16GB | ~22.7GB | ❌ Way OOM |
| 80K / 160K | — | — | ❌ Not even close |

A 24GB GPU (RTX 3090 or 4090) is what you need to run the full 256K context window with room to spare. Your 12GB card simply doesn't have the headroom.

---

## What's Actually Achievable on Your RTX 4070

For a real-world 12GB VRAM setup, the practical recommendation is a 128K context with fit-based GPU layer placement for text, and 64K context for vision workloads. However, those figures assume a **Q5_K_XL** quantization (larger/higher quality than your IQ3_S), which means the model weights use less VRAM proportionally — but the KV cache math still hurts.

With your **IQ3_S** (10.4GB model on disk), your practical ceiling with Q8_0 KV cache is roughly:

| Config | KV Cache type | Estimated Max Context | Notes |
|---|---|---|---|
| Current (`-ngl 25`) | Q8_0 | ~16K–20K | Stable |
| Drop to `--cache-type-k q4_0` | Q4_0 | ~28K–32K | Some quality loss |
| `-ngl 23` + Q4_0 KV | Q4_0 | ~32K | More GPU headroom |
| Switch to Q4_K_M GGUF + Q4_0 KV | Q4_0 | ~40K–48K | Would need re-download |

---

## Recommended Next Steps to Push Context

**Step 1 — Try Q4_0 KV cache to halve KV memory:**
```bash
./build/bin/llama-server \
  -m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  -ngl 25 \
  -c 32768 \
  --cache-type-k q4_0 \
  --cache-type-v q4_0 \
  -np 1 --host 0.0.0.0 --port 8081
```

**Step 2 — If that OOMs, reduce GPU layers:**
Drop `-ngl` to 22–23 to free another ~1.5GB for the compute buffer.

**Step 3 — For anything beyond 32K**, you'd need to switch to Q4_K_M quantization (~13GB disk) and offload more layers to CPU, accepting slower generation speed.

---

## Summary

- **160K / 80K → Not possible on 12GB VRAM, full stop.**
- **32K → Likely achievable** by switching to Q4_0 KV cache.
- **48K → Possible** only with a better quantization (Q4_K_M) + aggressive layer offloading + Q4_0 KV.
- As a general guideline, start with 32K in practice for good responsiveness, and only increase context if your use case genuinely requires long documents.

References:

- [Running Gemma 4 26B-A4B locally on 12GB VRAM](https://carteakey.dev/blog/running-gemma-4-26b-a4b-locally/)
- [Gemma 4 Hardware Requirements Guide](https://avenchat.com/blog/gemma-4-hardware-requirements)
- [How to Run Gemma 4 with llama.cpp](https://avenchat.com/blog/run-gemma-4-with-llama-cpp)
