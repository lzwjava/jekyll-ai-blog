---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muda 0.2.0 Released
translated: false
type: note
---

Pushed as **`muda 0.2.0`** (`67ae082`). Here's what got added.

## New API surface

**Runtime / devices**

- `mudaSetDevice`, `mudaGetDevice`, `mudaDeviceGetName`, `mudaDeviceGetAttribute` (23 attributes), `mudaDeviceGetPCIBusId`, `mudaDeviceReset`
- `mudaRuntimeGetVersion`, `mudaDriverGetVersion`, `mudaCtxGetDevice`

**Memory**

- `mudaMallocHost`, `mudaFreeHost`, `mudaHostGetDevicePointer`
- `mudaMemGetInfo`, `mudaPointerGetAttributes` + a full allocation registry that tracks every device/host allocation
- `mudaMemcpy2D` / `mudaMemcpy2DAsync`, `mudaMemsetD8`, `mudaMemsetD32`
- `mudaMemAdvise`, `mudaMemPrefetchAsync` (documented no-ops)

**Modules / launch**

- `mudaFuncGetAttributes` (work-group size, local/private memory)
- `mudaLaunchKernelEx` + full packed `extra[]` argument support (`MUDA_LAUNCH_PARAM_BUFFER_POINTER/SIZE`)
- `mudaOccupancyMaxActiveBlocksPerMultiprocessor`

**Streams / events**

- `mudaStreamCreateWithFlags`, `mudaStreamQuery`, `mudaStreamWaitEvent`
- `mudaEventCreateWithFlags`, `mudaEventQuery`
- Streams are now wrapper objects tracking their last `cl_event`, so non-blocking `Query` actually works

## Driver internals

- Extended the `muda_driver` vtable with ~15 new operations
- Stream wrapper + per-stream event tracking for query/wait
- Packed-argument unpacking with natural alignment
- `MUDA_VERBOSE=1` dumps the OpenCL build log (I used it to find and fix 4 compiler warnings — removed redundant typedefs from the preamble)

## Examples & tests

| example | result on M40 |
| --- | --- |
| `vector_add` (1M floats) | ~0.18 ms, ~70 GB/s |
| `saxpy` (4M floats, streams) | ~0.24 ms, ~210 GB/s |
| `matmul` 256×256 tiled | ~0.09 ms, ~395 GFLOP/s |

Test suite grew from **13 → 35 checks**, all passing, covering 2D copies, packed launches, pointer introspection, device attributes, function attributes/occupancy, and stream/event querying. README updated for 0.2.0.

The repo now tracks `origin/main` cleanly. Want me to tackle the `driver_nouveau` backend next (the true "no NVIDIA userspace" path)?
