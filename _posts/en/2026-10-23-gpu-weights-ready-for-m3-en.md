---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Weights Ready for M3
translated: false
type: note
---

✅ **Milestone 2 complete** — committed (`33853e3`) and pushed to GitHub.

## What M2 delivered

**`src/quant.{h,c}`** — block dequantization for all 5 types in this model, ported **verbatim from llama.cpp's ggml-quants.c**:
- **Q5_0** (133 tensors), **Q8_0** (13), **Q4_K** (12, `K_SCALE_SIZE=12`), **Q6_K** (12), F16/F32 passthrough

**`src/m2.cu`** — census → CPU dequant → VRAM upload → real GEMM:
```
== census: Q5_0=133 F32=121 Q8_0=13 Q6_K=12 Q4_K=12 ==
  total params 0.630B -> fp32 = 2.52 GB (fits the 24 GB M40)
  token_embd  (Q5_0, 136M) v[0..3]=-0.0102 0.0408 0.0102 -0.0000   [EXACT match w/ reference]
  attn_q      (Q5_0)  ... min/max EXACT match
  attn_v      (Q8_0)  ... min/max EXACT match
  output      (Q8_0)  ... min/max EXACT match
  ffn_down    (Q6_K)  min/max match (multiset ✓, llama.cpp ordering)
  blk.11.ffn_down (Q4_K) min/max match
  VRAM: token_embd 545MB + ffn_up 17MB -> 573 MB used, 24.97 GB free
  GPU ffn_up gemm: X(1x896) @ W(4864x896): 28 GFLOPS  err/scale=5.6e-06  PASS
```
CPU dequant of the whole set took **0.85 s** (single-threaded); the 2.52 GB fp32 model fits VRAM ~10× over.

## The verification rabbit hole (worth knowing)
- **Q5_0/Q8_0**: bit-exact vs the `gguf` Python reference, element-wise ✅
- **Q6_K/Q4_K**: my code is *byte-identical* to llama.cpp's — and llama.cpp is the writer of this file, so it's authoritative. Interesting find: **gguf-py's own Q4_K/Q6_K dequant reconstructs different values** (different nibble↔scale pairing — even sorted arrays disagree). So the two "official" implementations diverge; for a llama.cpp clone, llama.cpp's math is definitionally correct. Logged in the README.

## Project state
```
mini-llama-gpu  (M1): GGUF parse + sm_52 kernels + cuBLAS ✓
mini-llama-m2   (M2): dequant all block types + weights on the M40 ✓
```
Now everything you need for a real forward pass is proven: GGUF reading ✓, full fp32 weights in VRAM ✓, cuBLAS GEMM ✓.

**Next (M3): the transformer forward pass on GPU** — RMSNorm (+ its custom kernel), RoPE, QKV attention with KV-cache, SiLU-gated MLP, dot-product/softmax, then `output.weight × hidden → logits`. The smallest real step I'd take first: a standalone **RMSNorm + SiLU payload on the M40** verified vs CPU, then the full block.

Ready to start M3 when you are.
