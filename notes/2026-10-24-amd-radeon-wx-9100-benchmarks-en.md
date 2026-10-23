---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Radeon WX 9100 Benchmarks
translated: false
type: note
---

Everything is consistent now. Here's the full picture.

## Environment

`nvidia-smi` fails — there is **no NVIDIA GPU or driver** on this machine (only stale nvidia userspace packages). The real GPU is:

- **AMD Radeon PRO WX 9100** — Vega 10, `gfx900`, 64 CUs, 1500 MHz, 15.98 GiB HBM2, 2048-bit bus
- Toolchain: **ROCm 7.1 / hipcc (clang 21)** works

## Benchmark program

I created `gpu_bench.hip` (self-contained, no rocBLAS headers needed):

```bash
hipcc -O3 --offload-arch=gfx900 -o gpu_bench gpu_bench.hip
./gpu_bench --size 4096 --iters 20 --burn 20
```

It runs a naive tiled SGEMM, a register-blocked SGEMM, a D2D copy bandwidth test, and a sustained FMA burn loop.

## Results (WX 9100)

| Test | Result | % of peak |
| --- | --- | --- |
| Copy bandwidth (r+w) | **351 GB/s** | ~72% of ~484 GB/s HBM2 |
| FP32 GEMM (naive, 1 elem/thread) | **2.22 TFLOPS** | 18% |
| FP32 GEMM (register-tiled 4×4) | **4.12 TFLOPS** | ~34% of ~12.3 TFLOPS |
| Burn loop (sustained FMA) | **3.77 TFLOPS** | ~31% |

Under the burn load the card held **1500 MHz SCLK / 945 MHz MCLK at ~170 W**, with junction temperature settling around **90–99 °C** (edge ~66 °C, memory ~67 °C). It stayed stable, but junction near 99 °C is warm — worth checking airflow before running long jobs.

## Notes

- The register-tiled kernel roughly **doubled** FP32 throughput over the naive one by reusing operands in registers. A tuned/cached kernel (rocBLAS) or wider vectorized loads + double buffering would get closer to the ~12 TFLOPS FP32 roofline.
- I hit one bug along the way: the burn loop originally queued kernels without synchronizing, creating a huge backlog. Fixed by syncing each launch and correcting the FLOP accounting (only `grid*block` threads are active, not all 64M elements).
- Files left in place: `/home/lzw/projects/nanoGPT/gpu_bench.hip` and the compiled `gpu_bench` binary.

Want me to try a `rocBLAS` version (needs `librocblas-dev`) or an FP16 path to measure closer to peak?
