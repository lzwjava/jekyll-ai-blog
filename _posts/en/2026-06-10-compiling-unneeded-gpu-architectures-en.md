---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compiling Unneeded GPU Architectures
translated: false
type: note
---

Here's the full picture:

**Parallelism:**

- nvcc `--threads 4` — compiling for 4 architectures simultaneously
- 4 × cicc processes, each at ~100% CPU, ~650MB RAM each
- 32 cores available, load avg 2.90 — plenty of headroom

**Problem — compiling for ALL architectures:**
The build is ignoring `TORCH_CUDA_ARCH_LIST="8.9"`. flash-attn's build system hardcodes 4 targets:

```
-gencode arch=compute_80,code=sm_80   ← H100 (waste for you)
-gencode arch=compute_90,code=sm_90   ← Ada (waste)
-gencode arch=compute_100,code=sm_100 ← Blackwell (waste)
-gencode arch=compute_120,code=sm_120 ← (waste)
```

Your RTX 4070 is sm_89, none of these match exactly. It's compiling ~4x more kernels than needed.

**Current kernel:** `flash_bwd_hdim32_fp16_causal_sm80` — still early in the backward pass.

**Resources:** Fine — 53GB RAM free, disk at 34GB free.

Want me to kill this and restart with `MAX_JOBS=8 FLASH_ATTN_CUDA_ARCHS="8.9"` env var (which flash-attn's setup does respect) to speed it up 4x? Or let it ride?
