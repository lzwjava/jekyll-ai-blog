---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Key Compute Units in NVIDIA GPUs
translated: false
type: note
---

Question: Provide a comprehensive introduction to compute units in NVIDIA GPUs: Tensor Cores, CUDA cores, load/store units, and warp schedulers.

Answer:

NVIDIA GPUs are designed for massive parallel processing, particularly in graphics, scientific computing, and AI workloads. The core building block is the **Streaming Multiprocessor (SM)**, which contains various compute units responsible for executing instructions. These units work together under the SIMT (Single Instruction, Multiple Thread) model, where threads are grouped into **warps** of 32 threads that execute the same instruction simultaneously.

### CUDA Cores

CUDA cores (also called Streaming Processors or SPs) are the general-purpose arithmetic units in the SM. They handle scalar operations, including:

- Floating-point arithmetic (FP32, FP16, etc.)
- Integer operations (INT32)
- Basic logic and control instructions

Each CUDA core executes one operation per thread per clock cycle (or in some cases, shared across cycles). Modern SMs (e.g., in Ampere or later architectures) typically have 64–128 CUDA cores per SM, divided into FP32 and INT32 paths. They are versatile and used for most non-specialized computations, such as general math in games, simulations, or non-matrix AI operations.

CUDA cores follow the SIMT model: all 32 threads in a warp execute the same instruction, but on different data. If threads diverge (e.g., via branches), inactive threads are masked off, reducing efficiency.

### Tensor Cores

Introduced in the Volta architecture (2017) and improved in subsequent generations (Turing, Ampere, Hopper, Blackwell), Tensor Cores are specialized accelerators for matrix multiply-accumulate (MMA) operations, which are fundamental to deep learning (e.g., neural network training and inference).

Key features:

- They perform dense matrix operations much faster than CUDA cores by processing small matrix fragments (e.g., 4x4 or larger tiles) in a single cycle.
- Support mixed precision: e.g., FP16 or BF16 inputs with FP32 accumulation for higher accuracy.
- In later architectures, they handle additional formats like INT8, TF32, or FP8 for even higher throughput.

A single Tensor Core can deliver hundreds to thousands of operations per cycle, far exceeding CUDA cores for matrix workloads. They are programmed via warp-level primitives (e.g., WMMA or MMA instructions in CUDA). Tensor Cores dominate AI performance but are limited to specific operations; general tasks fall back to CUDA cores.

### Load/Store Units (LD/ST)

Load/Store units handle memory operations: loading data from memory into registers and storing results back. They are essential for accessing global memory, shared memory, constant memory, etc.

Characteristics:

- Typically 16–32 LD/ST units per SM (varying by architecture).
- Each unit processes memory requests for one or more threads (often half-warp or per-thread in coalesced accesses).
- They compute addresses, handle coalescing (merging requests from threads in a warp to reduce memory transactions), and manage cache interactions (L1 and L2).

Efficient use requires coalesced accesses (threads accessing contiguous memory) to maximize bandwidth and avoid serialization. LD/ST units are a common bottleneck in memory-bound kernels.

### Warp Schedulers

Warp schedulers manage the execution of warps within an SM. They are critical for hiding latency and maximizing throughput.

Role and operation:

- Each SM has multiple warp schedulers (typically 4 in modern architectures like Turing, Ampere, Hopper).
- Each scheduler selects eligible warps (those with ready instructions, not stalled on memory or dependencies) and issues one instruction per cycle to the appropriate execution units (CUDA cores, Tensor Cores, LD/ST, etc.).
- When a warp stalls (e.g., waiting for memory), the scheduler switches to another ready warp—this "latency hiding" keeps the SM busy.

Scheduling policies (e.g., round-robin or priority-based) ensure fairness and utilization. High warp occupancy (many resident warps per SM) improves performance by providing more options for scheduling.

### How They Interact in an SM

A typical modern SM (e.g., Ampere) is partitioned into 4 processing blocks, each with:

- A portion of CUDA cores
- Tensor Cores
- LD/ST units
- A warp scheduler and dispatch unit

Instructions from selected warps are dispatched to the relevant units. This design allows concurrent execution of different instruction types and efficient resource use.

In summary, CUDA cores provide general compute, Tensor Cores accelerate AI-specific matrix ops, LD/ST units manage memory traffic, and warp schedulers orchestrate everything to hide latencies and achieve high parallelism. Understanding these units helps optimize CUDA kernels for specific workloads.

References:

- [NVIDIA Volta Architecture Whitepaper](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)
- [NVIDIA Turing Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-turing-architecture-in-depth/)
- [Inside NVIDIA GPUs: Anatomy of high performance matmul kernels](https://www.aleksagordic.com/blog/matmul)
- [A Beginner's Guide to NVIDIA GPUs in 2025](https://www.cudocompute.com/blog/a-beginners-guide-to-nvidia-gpus)
- [CUDA Cores vs Tensor Cores](https://acecloud.ai/blog/cuda-cores-vs-tensor-cores/)
