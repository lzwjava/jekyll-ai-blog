---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm Matrix Multiplication Source Code
translated: false
type: note
---

Now I have a thorough understanding of ROCm's matrix multiplication source code. Here is a comprehensive explanation:

---

## How ROCm Implements Matrix Multiplication in Source Code

ROCm approaches matrix multiplication primarily through three libraries, each offering different levels of abstraction:

### 1. **rocBLAS** — The BLAS Library Entry Point

**File:** [`library/src/blas3/rocblas_gemm.hpp`](https://github.com/ROCm/rocBLAS/blob/develop/library/src/blas3/rocblas_gemm.hpp)

rocBLAS implements the standard BLAS GEMM (General Matrix Multiply) API: **C = α·op(A)·op(B) + β·C**.

The host-side flow begins in `rocblas_gemm_impl()` (in `rocblas_gemm_imp.hpp`). After validating arguments and copying α/β to host, it calls:

```cpp
status = ROCBLAS_API(rocblas_internal_gemm_template)(handle, trans_a, trans_b,
                     m, n, k, alpha, A, 0, lda, 0, B, 0, ldb, 0, beta, C, 0, ldc, 0, 1);
```

This dispatches into the **Tensile** backend.

### 2. **Tensile** — The Kernel Generation Engine (Primary GEMM Backend)

Tensile is a **YAML-driven kernel generator** that creates hand-optimized assembly kernels. The rocBLAS ↔ Tensile interface is in:

**File:** [`library/src/tensile_host.cpp`](https://github.com/ROCm/rocBLAS/blob/develop/library/src/tensile_host.cpp)

#### The dispatch flow

```
rocblas_gemm()
  → rocblas_internal_gemm_template()
    → runContractionProblem()          [tensile_host.cpp]
      → ConstructTensileProblem()       Builds Tensile::ContractionProblem
      → GetTensileInputs()              Sets up A, B, C, D GPU pointers
      → library->findBestSolution()     Best kernel from pre-tuned library
      → adapter.launchKernels()         Launches the GPU kernel
```

**Key code** (from `tensile_host.cpp`):

```cpp
// Find best GPU kernel for this problem size
solution = library->findBestSolution(tensile_prob, *hardware, fitness_query);

// Launch it
hipError_t hip_status = adapter.launchKernels(
    solution->solve(tensile_prob, GetTensileInputs(prob), *hardware),
    handle->get_stream(), ...);
```

Tensile pre-compiles thousands of tuned kernel variations (for different M, N, K sizes, data types, GPU architectures) into `.co` code object files stored at `/opt/rocm/lib/rocblas/library/`.

#### The Tensile Kernel Writer (Assembly)

**File:** [`Tensile/KernelWriterAssembly.py`](https://github.com/ROCm/Tensile/blob/develop/Tensile/KernelWriterAssembly.py)

Tensile generates actual GCN/AMDGPU assembly (`.s` files). The kernel writer emits `v_mfma_f32_16x16x4f32` style MFMA instructions. For example:

```python
# From KernelWriterAssembly.py
class KernelWriterAssembly(KernelWriter):
    def __init__(self, ...):
        self.do["MAC"] = True       # Multiply-Accumulate
        self.do["GlobalReadA"] = True
        self.do["GlobalReadB"] = True
        self.do["LocalWrite"] = True
        self.do["GlobalWrite"] = True
```

It emits assembly like:

```asm
v_mfma_f32_16x16x4f32 v[0:3], v4, v5, v[0:3]  // C += A * B
```

### 3. **Composable Kernel (CK)** — Modern C++ Template Library (Newer Approach)

**Repo:** [`https://github.com/ROCm/composable_kernel`](https://github.com/ROCm/composable_kernel)

CK is the **modern, C++ template-based** approach. It uses a tile-based programming model built on top of AMDGPU intrinsics.

#### Three-level hierarchy

**Level 1 — Grid-level GEMM (kernel entry):**

```
GridGemm
  └─ BlockGemm       (per threadblock)
      └─ WarpGemm    (per wavefront)
          └─ MFMA / WMMA instructions
```

**Level 2 — Block GEMM (from shared memory):**

**File:** `ck/tutorial/ck_tile/gemm/01_naive_gemm/block_gemm_asmem_bsmem_creg.hpp`

```cpp
// C += A * B  (A and B from shared memory, C in registers)
template <typename Problem, typename Policy>
struct BlockGemmASmemBSmemCReg {
    template <typename CBlockTensor, typename ABlockWindow, typename BBlockWindow>
    CK_TILE_DEVICE void operator()(CBlockTensor& c,
                                   const ABlockWindow& a,
                                   const BBlockWindow& b) const {
        // Iterate over K in the inner loop:
        static_for<0, KIterPerWarp, 1>{}([&](auto kIter) {
            static_for<0, MIterPerWarp, 1>{}([&](auto mIter) {
                AWarpTensor a_warp = load_tile(a_warp_windows(mIter)(kIter));
                static_for<0, NIterPerWarp, 1>{}([&](auto nIter) {
                    BWarpTensor b_warp = load_tile(b_warp_windows(nIter)(kIter));
                    WarpGemm{}(c_warp, a_warp, b_warp);  // ← actual MAC
                });
            });
        });
    }
};
```

**Level 3 — Warp GEMM (the actual MFMA instruction):**

**File:** `ck/include/ck_tile/ops/gemm/warp/warp_gemm_attribute_mfma_impl.hpp`

This is where the **actual GPU matrix multiply instruction** is invoked:

```cpp
// F32 GEMM: 16x16x4 tile using MFMA
struct WarpGemmAttributeMfmaImplF32F32F32M16N16K4 {
    // c_vec += a_vec * b_vec
    template <typename... Params>
    CK_TILE_DEVICE void operator()(CVecType& c_vec,
                                   const AVecType& a_vec,
                                   const AVecType& b_vec) const {
#if defined(__gfx9__)
        // Direct builtin intrinsic
        c_vec = __builtin_amdgcn_mfma_f32_16x16x4f32(a_vec[0], b_vec[0], c_vec, 0, 0, 0);
#else
        // Or inline assembly
        asm volatile("v_mfma_f32_16x16x4f32 %0, %1, %2, %3\n"
                     : "+v"(c_vec)
                     : "v"(a_vec), "v"(b_vec), "v"(c_vec));
#endif
    }
};
```

### 4. **hipBLASLt** — The Lightweight Alternate Backend

rocBLAS also supports **hipBLASLt** as a lightweight backend (in `hipblaslt_host.cpp`). This provides an alternative path using hipBLASLt's `hipblasLtMatmul()` API.

### 5. **rocWMMA** — Wavefront Matrix Multiply-Accumulate API

**File:** `rocwmma/internal/mma_impl.hpp`

rocWMMA provides a library-level WMMA API wrapping the hardware MFMA instructions, with support for different data layouts (row/col major).

---

### Summary of the Architecture

```
PyTorch / TensorFlow / User App
         │
    ┌────▼────┐
    │ rocBLAS │  ← C = α·A·B + β·C  (BLAS GEMM API)
    └────┬────┘
         │
    ┌────▼──────────┐
    │   Tensile     │  ← YAML-defined, pre-tuned assembly kernels
    │  (primary)    │     Loads .co code objects for target GPU
    └────┬──────────┘
         │
    ┌────▼──────────────────┐
    │ Composable Kernel (CK)│  ← Modern C++ template library
    │    (newer/optional)   │     Tile-based, uses builtins
    └────┬──────────────────┘
         │
    ┌────▼────────────┐
    │   AMDGPU ISA    │
    │ v_mfma / v_wmma │  ← Hardware matrix instructions
    └─────────────────┘
```

The actual matrix multiplication on AMD GPUs boils down to **MFMA** (Matrix Fused Multiply-Add) instructions — AMD's equivalent of NVIDIA's Tensor Cores — which are invoked either through inline assembly or compiler builtins (like `__builtin_amdgcn_mfma_f32_16x16x4f32`).
