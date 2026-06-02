---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding ROCm Kernel Optimization
translated: false
type: note
---

Now I have a thorough understanding of the codebase. Here's the comprehensive picture:

---

ROCm Kernel Optimization: The Full Landscape

This repository (/Users/lzwjava/projects/ROCm) is a meta-repository — a repo manifest (default.xml) that orchestrates ~30+ sub-projects via Google's `repo` tool. The actual kernel source code lives in separate repositories (llvm-project, composable_kernel, rocm-libraries, etc.) that you'd pull with `repo sync`. Here's how kernel optimization works in the ROCm ecosystem, drawn from the docs:

---

1. KERNEL AUTHORING — Choose Your Weapon

You have three main paths for writing kernels on ROCm:

  HIP (C++): The native approach. Write C++ kernels using HIP's runtime API and
  kernel language. Use hipify-clang to port existing CUDA code. The kernel
  compiles through AMDGPU LLVM backend to GCN/RDNA ISA.

  OpenCL (C): Cross-platform standard. ROCm supports OpenCL 2.0+ for AMD GPUs.

  Triton (Python): Write GPU kernels in Python. Triton compiles through MLIR →
  LLVM IR → AMDGPU ISA. Increasingly popular for AI workloads. The docs have an
  extensive section on Triton optimization (see workload.rst lines 1276-1532).

---

2. THE KERNEL OPTIMIZATION PIPELINE

Step 1: Profile First
────────────────────
Never guess where the bottleneck is. ROCm provides a layered profiling stack:

  PyTorch Profiler          → High-level timeline (export to Perfetto UI)
  ROCm Systems Profiler     → CPU+GPU traces, memory, context switches
  ROCProfiler (rocprof)     → Raw GPU hardware counters (text/CSV output)
  ROCm Compute Profiler     → Guided analysis: roofline, speed-of-light,
                               memory charts, baseline comparison (GUI + CLI)
  ROCr Debug Agent          → Memory fault trapping, wavefront dumps

Quick profiling example:
  rocprof --stats ./my_kernel_app          # collect all counters
  rocprof --hip-trace ./my_kernel_app      # HIP API trace

Step 2: Identify Bottleneck
───────────────────────────
The performance glossary (docs/reference/glossary/performance.rst) defines the
key concepts:

  Compute-bound   → kernel limited by arithmetic throughput (ALU busy)
  Memory-bound    → kernel limited by HBM bandwidth (loads/stores dominate)
  Occupancy       → ratio of active wavefronts to max possible per CU
  Register pressure → too many VGPRs = fewer waves per CU, hiding less latency
  Bank conflicts  → LDS accesses serialized instead of parallel
  Wavefront divergence → threads in same wave take different branches

If GPU is the bottleneck (not CPU/kernel-launch overhead), go to kernel-level profiling.
ROCm Compute Profiler runs your kernel multiple times collecting different
counter sets, then gives you a roofline model showing exactly where you sit.

Step 3: Auto-Tune (Easiest → Most Effort)
─────────────────────────────────────────

Level 1 — Turn on auto-tuning (zero code changes):

# PyTorch TunableOp: tries 1000s of GEMM kernels from rocBLAS/hipBLASLt

  PYTORCH_TUNABLEOP_ENABLED=1 python my_model.py

# Then replay the best config

  PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=0 python my_model.py

# TorchInductor max-autotune: tunes Triton GEMM/conv tile sizes

  TORCHINDUCTOR_MAX_AUTOTUNE=1 python my_model.py

# MIOpen autotune: finds best convolution kernels

  MIOPEN_FIND_ENFORCE=3 MIOPEN_FIND_MODE=1 python my_model.py

Level 2 — Composable Kernel (CK) backend:

# Install CK Python wrapper, add CK to autotune backends

  pip install git+<https://github.com/rocm/composable_kernel@develop>
  TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="TRITON,CK,ATEN"

Level 3 — hipBLASLt manual tuning (TensileLite):

# For max GEMM performance, tune the assembly backend generator

  cd hipBLASLt/tensilelite
  ./Tensile/bin/Tensile config.yaml output_path

# 7-step tuning pipeline: benchmark common params → fork → join → final

Level 4 — Write custom tuned kernels in Triton or HIP:

  Triton auto-tunable parameters (the key knobs):
    BLOCK_M, BLOCK_N, BLOCK_K    → tile sizes (balance compute vs memory)
    num_stages = 2               → pipeline stages (2 for single GEMM)
    num_warps                    → waves per workgroup (affects occupancy)
    waves_per_eu                 → hint compiler to reduce VGPR usage
    matrix_instr_nonkdim = 16    → MFMA instruction size (16x16 > 32x32 on MI300X)

---

3. DEEP KERNEL OPTIMIZATION TECHNIQUES

Memory Access Optimization:

- Coalesce global memory accesses (128-byte transactions preferred)
- Maximize use of LDS (on-chip shared memory) — 64KB per CU on MI300X
- Minimize global↔LDS data movement (use tiling/blocking)
- Avoid bank conflicts in LDS (pad shared memory arrays)
- Vectorize: use global_load_dwordx4 (128-bit loads) instead of scalar loads
- For MI300X GEMM: avoid strides that are multiples of 512 bytes (Tagram hotspotting)

Compute Optimization:

- MI300X: prefer mfma_16x16 over mfma_32x32 (better power efficiency)
- bf16 matrix ops are noticeably faster than f16
- Target occupancy: at least 1024 thread blocks (workgroups) in the grid
- MI300X has 304 active CUs (8 XCDs × 38 active CUs each)
- Use WorkGroupMapping multiples of 8 (number of XCDs) for L2 cache efficiency

Occupancy Calculation (lines 1643-1690 of workload.rst):

  1. Find .vgpr_count from ISA: N
  2. Find LDS allocation: grep "triton_gpu.shared" from MLIR dump → L bytes
  3. Find num_warps: grep "triton_gpu.num-warps" from MLIR → nW
  4. occ_vgpr = lookup from VGPR/occupancy table
  5. occ_lds = floor(65536 / L)
  6. occ = min(floor(occ_vgpr × 4 / nW), occ_lds) × nW / 4

ISA Assembly Analysis:

- export AMDGCN_ENABLE_DUMP=1 to dump ISA
- Check for global_load_dwordx4 (vectorized loads)
- Check LDS loads/stores use _b128 suffix (minimize instructions)
- Inspect s_waitcnt(lgkmcnt, vmcnt) for synchronization efficiency
- Overlap instructions to hide latency

MLIR Analysis:

- export MLIR_ENABLE_DUMP=1 to see Triton intermediate representation
- Identify redundant LDS round-trips (like loading, transposing, re-storing)
- Check data layouts: blocked → shared → transpose → blocked → dot_op

---

4. SYSTEM-LEVEL KERNEL OPTIMIZATION

  CU masking (docs/how-to/setting-cus.rst):
    # Pin specific CUs to specific GPUs
    HSA_CU_MASK="0:0-19;1:20-39" ./my_app  # GPU 0 uses CUs 0-19, GPU 1 uses 20-39
    ROC_GLOBAL_CU_MASK="0:0-15,32-47" ./my_app  # HIP-level masking

  Multi-GPU (RCCL):
    - Always use all 8 GPUs for collectives (MI300X fully-connected topology)
    - Disable NUMA auto-balancing: sudo sysctl kernel.numa_balancing=0
    - Use one-process-per-GPU (avoids serialized kernel launches)
    - TORCH_NCCL_HIGH_PRIORITY=1 GPU_MAX_HW_QUEUES=2 for FSDP
    - NCCL_MIN_NCHANNELS=112 for production workloads

  Environment Variables at a Glance:
    PYTORCH_TUNABLEOP_ENABLED=1          auto-select best GEMM kernel
    TORCHINDUCTOR_MAX_AUTOTUNE=1         tune Triton tile configs
    TORCHINDUCTOR_FREEZING=1             inline weights, fold constants (inference)
    MIOPEN_FIND_ENFORCE=3                auto-tune MIOpen conv kernels
    FLASH_ATTENTION_TRITON_AMD_ENABLE=FALSE   use CK backend for Flash Attention
    HSA_DISABLE_FRAGMENT_ALLOCATOR=1     disable memory caching (debugging)
    AMDGCN_ENABLE_DUMP=1                 dump ISA for analysis
    MLIR_ENABLE_DUMP=1                   dump Triton MLIR IR

---

5. KEY KERNEL LIBRARIES (already optimized, use them first)

  rocBLAS/hipBLASLt  → GEMM (with epilogues: ReLU, GELU, bias, etc.)
  Composable Kernel  → template-based kernel generation for GEMM/conv
  MIOpen             → convolution primitives (Winograd, FFT, direct, implicit GEMM)
  RCCL               → multi-GPU collectives (all-reduce, all-gather, etc.)
  rocWMMA            → wave matrix multiply-accumulate (tensor core ops)
  rocFFT             → FFT operations
  rocRAND            → random number generation on GPU
  rocPRIM/rocThrust  → parallel primitives (sort, scan, reduce)

---

In summary: The optimization path is profile → identify bound → auto-tune first
→ if still not enough, manually tune tile sizes/occupancy/instruction selection
→ if absolute max needed, dive into ISA/MLIR analysis and write custom kernels.
Most users will see large gains just from TunableOp + TorchInductor max-autotune

- Flash Attention without writing a single line of kernel code.
