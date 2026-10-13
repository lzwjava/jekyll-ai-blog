---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recommended Next Steps for Muda
translated: false
type: note
---

Good question. Here's how I'd think about it, given where `muda 0.2.0` is now.

## Where we are

`muda` is a working CUDA-compatible runtime, but the bottom of the stack is still NVIDIA's **OpenCL ICD**. So the honest status is: *"CUDA API, no libcuda — but still NVIDIA user space at the bottom."* There are two very different directions from here, and they should not be mixed.

## The fork in the road

**Track A — Purist: own the execution path.**
Replace the OpenCL backend with a native one that talks to the driver/hardware directly. This is the "real" answer to "use the muda driver," but it's research-grade:

- Bind `nouveau` instead of `nvidia`, use `drm_nouveau` GEM + a compute channel, build pushbuffers.
- You'd also need SASS: either hand-write Maxwell instructions or reuse Mesa's `nv50_ir`/an OpenCL binary container.
- **Risk:** unbinding `nvidia` breaks your working ComfyUI/llama.cpp setup until reboot. I'd only do this on a spare machine or with a tested restore script.
- Realistically: weeks, and it may never reach feature parity.

**Track B — Pragmatic: make muda genuinely useful.**
Keep the OpenCL backend, but build the things people actually want on an M40: a BLAS, real workloads, a drop-in CUDA shim, and Python. Fast, low-risk, immediately demonstrable.

## What I'd actually do next (Track B, recommended)

**Milestone 1 — Make it useful (highest value, ~1 session)**

- `mudaBLAS`: tuned `SGEMM`/`SGEMV` (tile + register blocking, `float4` vectorization).
- Benchmark suite vs. naive, track GB/s and GFLOP/s.
- A real demo: train a tiny MLP (or a mini-GPT) end-to-end on the M40 using muda + mudaBLAS.

**Milestone 2 — Make it drop-in (~1 session)**

- CUDA **runtime** API names as a shim (`cudaMalloc`, `cudaMemcpy`, `cudaLaunchKernel`, `cudaDeviceSynchronize`...) implemented on top of muda, so existing single-file `.cu` examples compile **unchanged** against `muda.h`.
- Python bindings via `ctypes` + zero-copy-ish numpy interop.

**Milestone 3 — Native spike (optional, separate branch)**

- Start with a *safe* experiment: a `driver_opencl_exec` hybrid where OpenCL is used only as a **compiler** (`clGetProgramInfo(CL_PROGRAM_BINARIES)` → SASS), and muda owns allocation + submission through `nouveau`. This de-risks Track A by keeping OpenCL for codegen.
- Keep it on a branch, with an `unbind/rebind` helper and a tested recovery path.

## Quick decision guide

| If your goal is… | Do this |
| --- | --- |
| "Show it does real work on the M40" | Milestone 1 |
| "Use it from Python / existing CUDA code" | Milestone 2 |
| "Truly not depend on NVIDIA user space" | Track A / Milestone 3 (research) |
| "Safest incremental polish" | More API tests + `driver_cpu` for CI |

## My recommendation

Start with **Milestone 1** — it turns muda from "a clever API wrapper" into "something I'd actually run." Then Milestone 2 makes it adoptable. Keep Track A as a separate, explicitly-risky research branch.

Want me to start on Milestone 1 (`mudaBLAS` + tuned SGEMM + the tiny-MLP demo and benchmarks)?
