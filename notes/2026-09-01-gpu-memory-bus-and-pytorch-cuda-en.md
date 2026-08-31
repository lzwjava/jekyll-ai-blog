---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Memory Bus and PyTorch CUDA
translated: false
type: note
---

**Question:** On a GPU like the Quadro 401 (or similar) with 4 VRAM chips, each 64-bit wide, giving a total 256-bit memory bus — how does that hardware fact relate to PyTorch and the CUDA API?

**Answer:**

## 1. What the 256-bit bus actually is

Each GDDR memory chip exposes a 64-bit interface. When you solder 4 of them onto the PCB and wire them in parallel, the GPU's memory controller sees a single, unified 256-bit bus. Memory bandwidth is determined by two factors: memory clock and memory width (bus width). These are multiplied together to produce the theoretical maximum bandwidth.

The formula is:

```
Bandwidth (GB/s) = Memory_Clock_MHz × Bus_Width_bits × DDR_factor / 8 / 1000
```

The theoretical bandwidth is calculated as `f_mem × bus_width × DDR_factor`, where `f_mem` is the memory frequency. So a wider bus directly means more data moved per clock cycle — the whole point of having 4 × 64-bit chips rather than one 64-bit chip.

---

## 2. How this appears to CUDA

The memory bus width is **a hardware throughput ceiling**, not something CUDA programs address directly.

**Bus width does NOT affect alignment rules.** As confirmed by NVIDIA engineers, GPU memory bus width has no effect on alignment or the use of `float4` or any other vector type. The GPU hardware only supports accesses comprising power-of-two bits, up to 128 bits, so data types matching the hardware capability will be more efficient.

What CUDA *does* care about is **cache line granularity**, which is independent of the bus width:

- An L1 cache line is 128 bytes and maps to a 128-byte aligned segment in device memory. Memory accesses cached in both L1 and L2 are serviced with 128-byte memory transactions, whereas accesses cached in L2 only are serviced with 32-byte memory transactions.

**Memory coalescing** is the key mechanism: memory coalescing combines multiple memory requests from the same warp into a smaller number of physical transactions, if the addresses are properly aligned and fall into an L1/L2 cache line.

Empirical benchmarks show that a kernel with coalesced access can execute in 232 microseconds while the same operation with uncoalesced access requires 540 microseconds — a slowdown of more than 2×. In bandwidth-bound kernels, this gap can widen to an order of magnitude.

---

## 3. How this surfaces in PyTorch

PyTorch sits on top of CUDA, so the bus width affects it **indirectly** through bandwidth:

| Layer | What it sees |
|---|---|
| **Hardware** | 4 × 64-bit chips → 256-bit bus → peak GB/s |
| **CUDA kernel** | 128-byte cache line transactions, coalescing rules |
| **PyTorch** | "Is this op memory-bound or compute-bound?" |

- PyTorch's caching allocator holds freed memory in an internal pool rather than returning it to the OS immediately — the gap between `nvidia-smi` and `torch.cuda.memory_allocated()` is this cache, not a leak.

- The data type (dtype) directly impacts memory usage and therefore bandwidth consumption. A `torch.float32` tensor uses 4 bytes per element, `torch.float16` uses 2 bytes, and `torch.int64` uses 8 bytes. On a 256-bit bus, halving dtype size (fp32 → fp16) effectively doubles your usable bandwidth for memory-bound ops.

- Pointwise (elementwise) operations are usually memory-bound. PyTorch JIT automatically fuses adjacent pointwise operations into a single kernel to save multiple memory reads/writes. This matters most when you're near the bandwidth ceiling set by your bus width.

---

## 4. Practical summary

```
4 chips × 64-bit = 256-bit bus
        ↓
Sets the peak GB/s ceiling
        ↓
CUDA coalesces 32 threads (1 warp) into 128-byte transactions
        ↓
PyTorch tensors that are contiguous + float16/bfloat16 use that bus most efficiently
```

For a Quadro 401-class card with only ~100 GB/s of bandwidth, the bus is the bottleneck for any attention or activation operation. Using `torch.float16`, contiguous tensors, and avoiding strided/non-contiguous views are the practical handles you have.

---

**References:**
- [NVIDIA Dev Forum — Bus Width & CUDA Alignment](https://forums.developer.nvidia.com/t/relationship-between-cuda-and-gpu-memory-bus-width/56296)
- [GPU Memory Explained — Thunder Compute](https://www.thundercompute.com/blog/gpu-memory-explained)
- [Memory Coalescing in GPU — Medium](https://medium.com/@himanshu0525125/memory-coalescing-in-gpu-23f222b26ca2)
- [Dissecting GPU Memory Hierarchy — arXiv](https://arxiv.org/pdf/1509.02308)
- [NVIDIA Blog: Global Memory Access in CUDA](https://developer.nvidia.com/blog/how-access-global-memory-efficiently-cuda-c-kernels/)
