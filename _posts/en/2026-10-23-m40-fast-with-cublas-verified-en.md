---
audio: false
generated: true
image: false
lang: en
layout: post
title: M40 Fast with cuBLAS Verified
translated: false
type: note
---

**Verified — the M40 is genuinely fast with cuBLAS:**

```
cublasSgemm 4096³ : 4333.6 GFLOPS   (≈63% of the card's ~6.8 TFLOPS fp32 peak)
1×4096 row GEMM   : 1.42 ms/token   (the exact op llama inference is built on)
```

That last number means: for a 7B-class model (hidden 4096), pure-GEMM time alone would be **~25+ tok/s**; with attention/KV/dequant overhead, realistic **8–15 tok/s on 24 GB VRAM**. That's a legitimately usable inference box — your instinct was right.

## The corrected picture for `192.168.1.137`

| | Works ✅ | Never will ❌ |
|---|---|---|
| **Your own mini-llama.cpp in CUDA** | raw CUDA 12.4 `sm_52` + `cuBLAS` on the M40 — **proven just now** | — |
| PyTorch/vLLM/MiniMax-H3 | — | those need torch's CUDA≥12 op paths → the UVM hang we hit |

The M40 is fine — it's just **fp32-only, CC 5.2**, so your project targets exactly that (not the newest-eye-candy stacks).

## Your mini-llama.cpp → GPU edition on this machine

1. **CPU (plain C, AVX2)**: GGUF header + tensor table parse, llama BPE tokenizer, sampling, KV-cache addr book, layer control flow
2. **GPU (CUDA `sm_52`)**: upload GGUF weights **dequantized q4→fp32 once**; all GEMM via `cublasSgemm` (works: 4.3 TFLOPS); your own tiny kernels for RMSNorm, RoPE, SiLU, softmax, scaled-dot-product attention
3. **VRAM budget** (24 GB): weights (7B q4 ≈ 5 GB, even 13B q4 ≈ 8 GB fit) + fp32 KV cache — plenty of context
4. **Expectation**: 7B q4 ≈ 10-15 tok/s, first token includes a one-time dequant+upload cost

## Ready to pull the trigger?
Next step I'd suggest: download a **Qwen2.5-0.5B-Instruct GGUF (q4_K_M, ≈0.44 GB)** into `/mnt/models` (via hf-mirror) as your milestone-1 test asset, then we implement **Milestone 1: GGUF parser + proof-of-life GPU GEMM** (load a real weight tensor, `cublasSgemm` it, verify against a CPU reference). Say the word and I'll start the download + scaffold that first milestone in the repo.
