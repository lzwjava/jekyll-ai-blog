---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using CUDA 12.8 for Flash-Attn Build
translated: false
type: note
---

CUDA 12.8 is available at `/usr/local/cuda-12.8/bin/nvcc`. The default `nvcc` is CUDA 13.2 (that's why the build picked 13.2). You need to explicitly use CUDA 12.8.

## Correct install command

```bash
CUDA_HOME=/usr/local/cuda-12.8 \
PATH=/usr/local/cuda-12.8/bin:$PATH \
MAX_JOBS=16 \
TORCH_CUDA_ARCH_LIST="8.9" \
pip install flash-attn==2.8.4 --no-build-isolation
```

This will:
1. ✅ Use **CUDA 12.8** (matching PyTorch 2.10.0+cu128)
2. ✅ Build **only sm_89** kernels (RTX 4070) — ~10x faster compile
3. ✅ Run **16 parallel jobs** (vs 2 before)
4. ✅ No ABI mismatch at runtime

Expected compile time: **~3–8 minutes** instead of 20–60+ minutes.