---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mini-llama.cpp Milestone 1 Landed
translated: false
type: note
---

Everything is done and pushed to GitHub. Here's the full picture:

## ✅ Milestone 1 landed — `mini-llama.cpp` works on the M40 box

**Repo `lzwjava/mini-llama.cpp` on `.137`** — built, run, verified, committed, **pushed** (`fe030ca` on `origin/main`):

- `src/gguf.{h,c}` — minimal **GGUF v3 reader** (works on the real Qwen2.5 model)
- `src/gpu_mm.cu` — **sm_52 CUDA kernels + cuBLAS** against the M40
- `Makefile` — `make` (CPU stub) + `make mini-llama-gpu`

```
== GGUF ==  arch=qwen2  name=qwen2.5-0.5b-instruct  v3  tensors=291  kv=26
  vocab = 151936  (token_embd Q5_0, hidden=896)
  real tensor blk.0.attn_norm.weight (F32): GPU y=2x+1  max|err|=0  PASS
  cuBLAS GEMM 512²: 921 GFLOPS  rel err 2.4e-7  PASS
```

**The debugging journey (all worth it for your learning):** value-type field is **u32** not u8, GGUF v3 has **no per-tensor KV store**, tensor offsets are **relative to the aligned data section** (not absolute), and cuBLAS is **column-major** (row-major buffers need the transposed reference). Verified byte-for-byte against the reference `gguf` python package.

## Bonus: the M40 story is now unambiguous

- ✅ Raw CUDA `sm_52` + cuBLAS 12.4 runs great: **4.3 TFLOPS GEMM @ 4096²**, ~1.4 ms/token row-GEMM
- The earlier "GPU is dead" conclusion was wrong — it was *PyTorch's* UVM path on the 580 driver. Your own C/CUDA llama.cpp is the right way to use this card.

## Where things stand on `.137`

| Item | Status |
| --- | --- |
| 500 GB TOSHIBA disk | ✅ GPT+ext4, mounted `/mnt/models` (435 GB free), fstab-persistent, 167 MB/s |
| Qwen2.5-0.5B-Instruct q4_K_M GGUF | ✅ `/mnt/models/qwen2.5-0.5b-instruct-q4_k_m.gguf` (491 MB) |
| Git | ✅ identity set, SSH key generated (you added it — push worked!), repo live on GitHub |

## Next (Milestone 2): dequantize on the GPU

The q4_K/Q5_0/Q8_0 block formats → upload fp32 weights to VRAM (24 GB fits the whole 0.5B model ~ 2 GB fp32 — and even a 7B q4 in fp32 ≈ 13 GB). Then Milestone 3 is the real forward pass (RMSNorm → RoPE → attention → SiLU MLP).

Want me to start M2 (block dequant + full weight upload) next?
