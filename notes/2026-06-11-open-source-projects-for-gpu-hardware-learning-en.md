---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Source Projects for GPU Hardware Learning
translated: false
type: note
---

**Question:** What are great open-source projects for learning how HBM memory, GPU chips, and related hardware actually work?

**Answer:**

The trick is to attack this at three layers: **RTL (the actual chip logic)**, **cycle-accurate simulators (where HBM timing lives)**, and **the software/driver stack (where you already have hardware — your MI300X and RTX 4070)**. Here's the ladder, ordered by learning ROI.

## Layer 1: GPU RTL — read real Verilog

**[tiny-gpu](https://github.com/adam-maj/tiny-gpu)** — start here, finish in a weekend. A minimal GPU implementation in Verilog optimized for learning how GPUs work from the ground up, built precisely because full projects like MIAOW and VeriGPU are too complex to learn from. ~15 Verilog files: a dispatcher, compute cores with fetcher/decoder/scheduler/ALU/LSU, and a memory controller. You'll see SIMD execution and memory-latency hiding in their rawest form.

```bash
git clone https://github.com/adam-maj/tiny-gpu && cd tiny-gpu
pip install cocotb  # testbenches are Python, very vibe-codable
make test_matadd    # watch a matrix-add kernel run cycle by cycle
```

**[Vortex](https://github.com/vortexgpgpu/vortex)** — the serious one. An open-source hardware and software RISC-V GPGPU that supports OpenCL/CUDA, runs on FPGA, and ships a complete open-source compiler, driver, and runtime stack. This just got much more interesting: Vortex 3.0 (released this week) adds a fixed-function 3D graphics pipeline with rasterizer and texture units, tensor core structured sparsity, warp-group-level matrix multiplication, a hardware kernel scheduler, plus a Mesa Vulkan backend and HIP support via chipStar. It also added ASIC synthesis flows targeting ASAP7 (7nm) and SAED14 predictive nodes — so you can take the same RTL from FPGA to a synthesis flow without licensing anything.

The killer learning feature: developers prototype designs in `simx` (a cycle-level C++ simulator) before doing the RTL implementation — so you can read the *same microarchitecture twice*, once in readable C++ and once in SystemVerilog. Study the cache subsystem (`hw/rtl/cache/`) and memory interconnect to see how a GPU actually feeds bandwidth-hungry cores.

Honorable mentions: **Ventus** (RISC-V vector-based GPGPU from Tsinghua — relevant given your location/network), **MIAOW** (AMD Southern Islands ISA clone), **Nyuzi**.

## Layer 2: HBM — simulators are where the learning is

There's no open-source HBM PHY/RTL (the PHY + interposer IP is the crown jewel of Synopsys/Rambus). What *is* open is the timing model and memory controller logic, which is 90% of what you need to reason about MI300X performance.

**[Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2)** (CMU SAFARI / Onur Mutlu's group) — the best codebase to learn DRAM/HBM internals. A modular, extensible, cycle-accurate DRAM simulator under MIT license with models for DDR3/4/5, LPDDR5, GDDR6, and HBM/HBM2/HBM3. The HBM3 model is a single readable file encoding the full JEDEC state machine — banks, bank groups, pseudo-channels, tRCD/tRP/tFAW timing constraints:

```bash
git clone https://github.com/CMU-SAFARI/ramulator2 && cd ramulator2
mkdir build && cd build && cmake .. && make -j
# then read: src/dram/impl/HBM3.cpp  ← the entire HBM3 spec as code
./ramulator2 -f ../example_config.yaml  # swap DRAM type to HBM3, replay traces
```

Run the same memory trace against DDR5 vs HBM3 configs and watch why HBM wins on bandwidth (32 pseudo-channels) but not latency. That single experiment teaches more than any datasheet.

**[DRAMsim3](https://github.com/umd-memsys/DRAMsim3)** — cycle-accurate with thermal modeling alongside performance modeling, specifically built to model 3D-stacked DRAM — relevant because HBM's thermal behavior (stacked dies on interposer) is a real MI300X constraint.

**[gem5](https://gem5.org)** — when you want full-system: CPU + GPU (it has a GCN3/Vega GPU model) + HBM, all simulated together. Ramulator 2.0 integrates with gem5. Heavier, learn it third.

**[LiteDRAM](https://github.com/enjoy-digital/litedram)** — a DRAM *controller* written in Migen (Python-generated HDL). Not HBM, but it's the most readable open memory controller in existence, and it's Python — perfect for your workflow.

## Layer 3: Software stack — you own an MI300X-hour, use it

**[ROCm](https://github.com/ROCm/ROCm)** + the `amdkfd` kernel driver — AMD's whole stack is open. Trace how `hipMalloc` becomes HBM pages: HIP runtime → ROCr → KFD ioctls → GPU page tables. Then measure your actual HBM3:

```cpp
// hbm_bw.cpp — STREAM triad on MI300X, measures real HBM3 bandwidth
#include <hip/hip_runtime.h>
#include <cstdio>
__global__ void triad(float* a, const float* b, const float* c, float s, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) a[i] = b[i] + s * c[i];
}
int main() {
    size_t n = 1ULL << 30;  // 4 GB per array, 12 GB total — trivial on 192GB
    float *a, *b, *c;
    hipMalloc(&a, n*4); hipMalloc(&b, n*4); hipMalloc(&c, n*4);
    hipEvent_t t0, t1; hipEventCreate(&t0); hipEventCreate(&t1);
    hipEventRecord(t0);
    for (int i = 0; i < 10; i++)
        triad<<<(n+255)/256, 256>>>(a, b, c, 2.0f, n);
    hipEventRecord(t1); hipEventSynchronize(t1);
    float ms; hipEventElapsedTime(&ms, t0, t1);
    printf("HBM BW: %.1f GB/s (theoretical MI300X: 5300)\n",
           10.0 * 3 * n * 4 / (ms * 1e6));
}
// hipcc hbm_bw.cpp -o hbm_bw && ./hbm_bw
```

You should see ~3.5–4 TB/s achieved vs 5.3 TB/s theoretical — then the question "where did the rest go?" sends you back to Ramulator's bank-conflict and refresh modeling. That loop (measure on real silicon → explain in simulator) is the fastest way to build genuine intuition.

**[tinygrad](https://github.com/tinygrad/tinygrad)** — has its own AMD driver that talks to the GPU at the PM4 packet / ioctl level, bypassing ROCm. Reading `tinygrad/runtime/ops_amd.py` is the shortest path to understanding what a GPU driver actually *is*. Also **NVIDIA's [open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)** for your 4070.

## Layer 4 (optional): RTL → silicon

**[OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD)** / **[OpenLane](https://github.com/efabless/openlane2)** for synthesis/place-and-route, **[Verilator](https://github.com/verilator/verilator)** for fast RTL simulation, **[Tiny Tapeout](https://tinytapeout.com)** if you ever want actual silicon back for ~$300.

## Suggested path for you

1. **Week 1:** tiny-gpu end-to-end on the MacBook Air (cocotb sims are light).
2. **Weeks 2–4:** Ramulator2 — read `HBM3.cpp`, run DDR5-vs-HBM3 trace experiments. This is the nanoGPT of memory systems: small, complete, modifiable.
3. **Parallel:** the HIP bandwidth benchmark + `rocprof` on your AMD droplet whenever it's up — connect simulator numbers to silicon.
4. **Month 2+:** Vortex `simx` → RTL, focusing on the cache/memory hierarchy. This directly feeds your inference-optimization goals: once you've seen how a GPU LSU coalesces accesses in RTL, KV-cache layout and memory-bound kernel optimization stop being folklore.

**References:**

- [tiny-gpu](https://github.com/adam-maj/tiny-gpu)
- [Vortex GPGPU](https://github.com/vortexgpgpu/vortex)
- [Vortex 3.0 release coverage — Phoronix](https://www.phoronix.com/news/Vortex-3.0-RISC-V-GPGPU)
- [Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2) / [paper](https://people.inf.ethz.ch/omutlu/pub/Ramulator2_arxiv23.pdf)
- [DRAMsim3](https://github.com/umd-memsys/DRAMsim3)
- [LiteDRAM](https://github.com/enjoy-digital/litedram)
- [tinygrad](https://github.com/tinygrad/tinygrad)
- [NVIDIA open GPU kernel modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
