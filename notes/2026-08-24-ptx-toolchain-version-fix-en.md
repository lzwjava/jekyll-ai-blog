---
audio: false
generated: true
image: false
lang: en
layout: post
title: PTX Toolchain Version Fix
translated: false
type: note
---

Fixed. `GPU 0: OK`, exit 0.

## What was wrong

Two-layer problem, both involving the **PTX toolchain version** vs. your driver:

1. **The bundled `compare.fatbin` was compiled with CUDA 9.2** (PTX ISA 6.0, arch sm_75). Your driver 580.178.04 is CUDA 13.0, and modern drivers refuse to JIT-compile PTX from toolchains that old → "the provided PTX was compiled with an unsupported toolchain".
2. **Rebuilding with the default nvcc (13.2) also failed** — nvcc 13.2 emits PTX ISA 9.2, which is *newer* than what a CUDA 13.0 driver's JIT supports. Same error message.

## The fix

Built the fatbin with the installed **CUDA 12.8** toolkit instead (PTX ISA 8.7 — within the 13.0 driver's supported range), targeted at **sm_89**, the native arch of your RTX 4070:

```bash
cd ~/projects/gpu-burn
/usr/local/cuda-12.8/bin/nvcc -I/usr/local/cuda-12.8/include \
  -arch=compute_89 -fatbin compare.cu -o compare.fatbin
make
```

Verified result: `./gpu_burn 5` → `Tested 1 GPUs: GPU 0: OK`, running at ~20 Tflop/s, 0 errors, temps 37→60 °C.

## Note for future rebuilds

`make clean && make` alone will revert to the broken 13.2 fatbin. To rebuild properly:

```bash
make clean
make CUDAPATH=/usr/local/cuda-12.8 COMPUTE=89
```

(`COMPUTE=89` is optional but produces native SASS/PTX for the 4070 instead of JIT-ing from sm_75.)
