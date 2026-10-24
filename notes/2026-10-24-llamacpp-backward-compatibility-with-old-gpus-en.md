---
audio: false
generated: true
image: false
lang: en
layout: post
title: Llama.cpp Backward Compatibility with Old GPUs
translated: false
type: note
---

Short answer: because llama.cpp's CUDA build deliberately stays backward-compatible with old NVIDIA GPUs like the M40, and it adapts its kernels at runtime to the GPU's compute capability.

The M40 is **Maxwell** (GM200), compute capability **5.2**, 12/24 GB GDDR5. Three things make it work:

**1. The binary ships PTX, not just SASS**
In `ggml/src/ggml-cuda/CMakeLists.txt` the default build includes `50-virtual` (as long as the CUDA toolkit is < 13):

```cmake
if (CUDAToolkit_VERSION VERSION_LESS "13")
    list(APPEND CMAKE_CUDA_ARCHITECTURES 50-virtual 61-virtual 70-virtual)
endif ()
```

`-virtual` means the kernels are compiled to PTX and the **CUDA driver JIT-compiles** them to native code for your exact GPU on first launch. That's why one build works on both an M40 and a modern RTX card.

**2. The CUDA backend switches kernels based on your GPU's compute capability at runtime**
- CUDA graphs are disabled below Volta (`ggml-cuda.cu:4833`).
- Flash attention falls back to a path that doesn't need tensor cores (CC < 70).
- Quantized matmuls select slower but compatible kernels for pre-Volta GPUs (`mmvq.cu:1163`, e.g. `Q2_K`/`Q3_K`/`IQ3_S` use the fallback on Pascal-older).
- FP16 math degrades to FP32 where Maxwell is slow.

**3. Maxwell is the floor of the supported hardware range** - the codebase treats CC 5.0 as the minimum supported NVIDIA arch.

**The caveat:** it *works* but it's not fast. The M40 has no tensor cores, no fast FP16, and no `__dp4a` (sm_61+), so quantized inference is a lot slower than on a modern card. And be aware: **CUDA 13 dropped Maxwell support**, so if your build fails to load on the M40, you need a CUDA 12.x toolkit (or older).

If you meant something more specific (a particular model, a crash, or a performance question about the M40), tell me exactly what you observed and I'll dig into it.
