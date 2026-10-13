---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Muda: CUDA runtime using OpenCL"
translated: false
type: note
---

Done. I built **`muda`** in `/home/lzw/projects/muda` and it runs real kernels on your Tesla M40.

## Result

```
$ make && ./build/test_muda
driver: opencl
== device ==
  device 0: Tesla M40 sm_52, 11436 MiB, 24 SMs
== memory ==
== vector_add ==
== saxpy ==
== shared_memory_+_syncthreads ==
== 2d_grid ==
== streams_and_events ==
13 passed, 0 failed

$ ./build/vector_add
vector_add of 1048576 elements: OK (0.206 ms, 61.2 GB/s)
```

## What it is

A CUDA-compatible runtime + its own driver layer that **never links or loads `libcuda`**:

- `include/muda.h` — CUDA-like API (`mudaMalloc`, `mudaMemcpy`, `mudaModuleLoadData`, `mudaLaunchKernel`, streams, events).
- `src/muda_internal.h` — a real `muda_driver` vtable, so backends are pluggable.
- `src/driver_opencl.c` — default "muda driver": loads `libOpenCL.so.1` via `dlopen` and dispatches through the OpenCL ICD.
- `src/muda_translate.c` — rewrites CUDA C → OpenCL C (I verified the output). Handles `__global__`, `__shared__`, `threadIdx/blockIdx/blockDim/gridDim`, `__syncthreads()`, and auto-inserts the `__global` address-space qualifier on pointer params, so normal CUDA signatures work unchanged.
- No CUDA toolkit, `nvcc`, or OpenCL dev headers needed to build.

## The one honest caveat

Your phrase was "don't use the CUDA driver, use the muda driver." I avoided `libcuda` entirely, but the lowest layer is still NVIDIA's **OpenCL** userspace ICD, because a from-scratch Maxwell driver would require reimplementing PMU/FECS firmware bring-up. I documented this and gave the vtable a clear path to a true `nouveau`/MMIO backend.

## Next steps I can take

- Add a `driver_nouveau` backend that talks to the open `nouveau` kernel driver directly (unbind `nvidia`, use `/dev/dri` pushbuffers) — the genuine "no NVIDIA userspace" path.
- Add a `driver_cpu` reference so tests run GPU-less.
- Push the commit to `git@github.com:lzwjava/muda.git`.

Committed locally as `62c8806`. Want me to push it?
