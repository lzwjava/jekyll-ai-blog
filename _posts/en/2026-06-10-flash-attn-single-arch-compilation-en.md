---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attn Single-Arch Compilation
translated: false
type: note
---

Status update:

- **1 nvcc process** — flash-attn compiles `.cu` files sequentially regardless of MAX_JOBS/ninja
- **2 .o files done**, currently on `flash_bwd_hdim128_bf16_sm80.cu`
- **9 tmpxft temp files** — still early (backward pass, hdim 128)
- **Arch: sm_89 only** — this is the real speedup (~4x faster per file vs 4-arch build)

MAX_JOBS=32 can't help here — flash-attn's build system compiles one `.cu` file at a time. The bottleneck is per-file CUDA compilation. With single-arch, each file should take 1-3 min instead of 5-12 min. Estimate ~30-40 min total remaining.
