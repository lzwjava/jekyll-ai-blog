---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Muda 0.4.0: CUDA Runtime Shim"
translated: false
type: note
---

Milestone 2 is done and pushed as **`muda 0.4.0`** (`cf2e73a`).

## What was added

**`mudart` — CUDA runtime API shim** (`include/mudart.h`, `src/mudart.c`)

Maps the CUDA **runtime** names onto muda:

- Memory: `cudaMalloc/Free`, `cudaMallocHost`, `cudaHostAlloc`, `cudaFreeHost`, `cudaMemcpy/Async/2D`, `cudaMemset`, `cudaMemGetInfo`
- Device: `cudaGetDeviceCount/Get/Set`, `cudaGetDeviceProperties` (real CUDA-shaped `cudaDeviceProp`), `cudaDeviceSynchronize/Reset`
- Streams/events: `cudaStream*`, `cudaEvent*`
- Errors: `cudaGetLastError/PeekAtLastError/GetErrorName/GetErrorString`, with `cudaError*` constants aliased
- Launch bridge: `dim3`, `cudaLaunchKernel((const void*)fn, grid, block, args, shared, stream)`, and the legacy `cudaConfigureCall` / `cudaSetupArgument` / `cudaLaunch` sequence

**Python binding** (`python/muda.py`) — pure `ctypes`, no build step:

- `muda.init()`, `device_info()`, `Module`, `Function`, `DeviceBuffer` (numpy interop), `Stream`, `Event`
- `muda.matmul` / `gemm` / `gemm_buffers` / `gemv` / `saxpy` backed by mudaBLAS
- Demos: `python/demo_kernel.py` (load + launch a kernel), `python/demo_matmul.py` (benchmark)

## Verified on the M40

```
make test
  35 passed, 0 failed     # core runtime
  18 passed, 0 failed     # mudaBLAS
  11 passed, 0 failed     # mudart  (new)

make python PYTHON=.venv/bin/python
  vector_add: OK
  256^3    0.065 ms    518.8 GFLOP/s
  512^3    0.244 ms   1101.1 GFLOP/s
  1024^3   1.831 ms   1173.0 GFLOP/s
  2048^3   13.477 ms  1274.8 GFLOP/s
```

I created a local `.venv` (gitignored) to get numpy for the demos; `uv venv .venv && uv pip install --python .venv/bin/python numpy` works on your machine.

## Suggested next step (Milestone 3)

The remaining gap in "drop-in" is the `<<<...>>>` launch syntax, which needs a front-end. I'd implement a tiny **`mudac` preprocessor** that rewrites:

```c
kernel<<<grid, block, shared, stream>>>(a, b, c, n);
```

into

```c
{ void* _a[] = {&a,&b,&c,&n}; cudaLaunchKernel((void*)kernel, grid, block, _a, shared, stream); }
```

so ordinary `.cu` files compile unchanged with `mudac prog.cu | cc -x c - -lmuda`. Want me to build that, or move on to the native `nouveau` backend?
