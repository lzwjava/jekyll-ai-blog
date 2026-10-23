---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verify CPU Inference Before GPU Port
translated: false
type: note
---

Here's the state of play and the recommended path forward:

## Current status
- ✅ M1–M3 all committed: GGUF reader → GPU GEMM/dequant (M2) → **CPU Qwen2 inference** (M3, just pushed)
- ⚠️ M3 code is brand-new and **never actually built/run** — it's committed but unverified
- Box facts: **Tesla M40 24GB** (sm_52, cuBLAS verified in M2), GitHub ✅, `hf-mirror.com` ✅, `huggingface.co` ❌ (blocked)

## Recommended next step: **Build & verify M3 end-to-end on a real model**

Everything else (GPU port, optimization) is downstream of knowing the CPU path actually produces sane tokens. Concrete plan:

1. **Wire the build** — add `mini-llama-m3` target to the Makefile (`cc … m3_cpu.c gguf.c quant.c qwen2.c tokenizer.c -lm`). CPU-only, avoids the slow `nvcc` M2 build. Two warnings to clean while at it (`quant.c:105` indentation, unused `buf` param).
2. **Get a small model** — `Qwen/Qwen2.5-0.5B-Instruct-GGUF` **Q8_0** (~530MB) from `hf-mirror.com` (HF direct is blocked; you have 17G free).
3. **Run & verify** — `./mini-llama-m3 model.gguf "The capital of France is" 32`. Check: tokenizer ids look right, finite top-5 logits, sane tok/s, readable output. You already have `~/llama.cpp` on the box → compare against reference llama.cpp logits/tokens as ground truth.
4. **Fix whatever breaks** — likely candidates: tokenizer merge-rank handling, RMSNorm dtype edge, or KV-cache indexing.

## Then M4 (the real milestone after this)
Port the verified CPU forward pass to CUDA on the M40 — the dequant/GEMM work from M2 already proves out the kernels (err 5.6e-6), so M4 is wiring `qwen2_forward_token` to `m2.cu` and adding a GPU KV cache.

**Want me to execute step 1–3 now?** I'll wire the Makefile, pull the Q8_0 model via hf-mirror, build, and run a first inference test.
