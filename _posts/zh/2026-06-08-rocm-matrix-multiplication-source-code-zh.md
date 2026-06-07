---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm 矩阵乘法源代码
translated: true
type: note
---

现在我对ROCm的矩阵乘法源代码有了透彻的理解。以下是全面的解释：

---

## ROCm如何在源代码中实现矩阵乘法

ROCm主要通过三个库来实现矩阵乘法，每个库提供不同层次的抽象：

### 1. **rocBLAS** — BLAS库入口点

**文件：** [`library/src/blas3/rocblas_gemm.hpp`](https://github.com/ROCm/rocBLAS/blob/develop/library/src/blas3/rocblas_gemm.hpp)

rocBLAS实现了标准的BLAS GEMM（通用矩阵乘法）API：**C = α·op(A)·op(B) + β·C**。

主机端流程从`rocblas_gemm_impl()`（位于`rocblas_gemm_imp.hpp`）开始。在验证参数并将α/β复制到主机后，它调用：

```cpp
status = ROCBLAS_API(rocblas_internal_gemm_template)(handle, trans_a, trans_b,
                     m, n, k, alpha, A, 0, lda, 0, B, 0, ldb, 0, beta, C, 0, ldc, 0, 1);
```

这会分发到**Tensile**后端。

### 2. **Tensile** — 内核生成引擎（主要GEMM后端）

Tensile是一个**YAML驱动的内核生成器**，用于创建手工优化的汇编内核。rocBLAS ↔ Tensile的接口位于：

**文件：** [`library/src/tensile_host.cpp`](https://github.com/ROCm/rocBLAS/blob/develop/library/src/tensile_host.cpp)

#### 分发流程

```
rocblas_gemm()
  → rocblas_internal_gemm_template()
    → runContractionProblem()          [tensile_host.cpp]
      → ConstructTensileProblem()       构建Tensile::ContractionProblem
      → GetTensileInputs()              设置A、B、C、D的GPU指针
      → library->findBestSolution()     从预调优库中选择最佳内核
      → adapter.launchKernels()         启动GPU内核
```

**关键代码**（来自`tensile_host.cpp`）：

```cpp
// 针对此问题规模找到最佳GPU内核
solution = library->findBestSolution(tensile_prob, *hardware, fitness_query);

// 启动内核
hipError_t hip_status = adapter.launchKernels(
    solution->solve(tensile_prob, GetTensileInputs(prob), *hardware),
    handle->get_stream(), ...);
```

Tensile预编译了数千个经过调优的内核变体（针对不同的M、N、K大小、数据类型、GPU架构），并将其存储为`.co`代码对象文件，位于`/opt/rocm/lib/rocblas/library/`。

#### Tensile内核编写器（汇编）

**文件：** [`Tensile/KernelWriterAssembly.py`](https://github.com/ROCm/Tensile/blob/develop/Tensile/KernelWriterAssembly.py)

Tensile生成实际的GCN/AMDGPU汇编（`.s`文件）。内核编写器会生成类似`v_mfma_f32_16x16x4f32`的MFMA指令。例如：

```python
# 来自KernelWriterAssembly.py
class KernelWriterAssembly(KernelWriter):
    def __init__(self, ...):
        self.do["MAC"] = True       # 乘加运算
        self.do["GlobalReadA"] = True
        self.do["GlobalReadB"] = True
        self.do["LocalWrite"] = True
        self.do["GlobalWrite"] = True
```

它会生成类似以下的汇编代码：

```asm
v_mfma_f32_16x16x4f32 v[0:3], v4, v5, v[0:3]  // C += A * B
```

### 3. **Composable Kernel (CK)** — 现代C++模板库（较新方法）

**仓库：** [`https://github.com/ROCm/composable_kernel`](https://github.com/ROCm/composable_kernel)

CK是一种**基于现代C++模板**的方法。它采用基于tile的编程模型，构建在AMDGPU内建函数之上。

#### 三层层次结构

**第一层 — 网格级GEMM（内核入口）：**

```
GridGemm
  └─ BlockGemm       （每个线程块）
      └─ WarpGemm    （每个波前）
          └─ MFMA / WMMA指令
```

**第二层 — 块级GEMM（基于共享内存）：**

**文件：** `ck/tutorial/ck_tile/gemm/01_naive_gemm/block_gemm_asmem_bsmem_creg.hpp`

```cpp
// C += A * B  （A和B来自共享内存，C在寄存器中）
template <typename Problem, typename Policy>
struct BlockGemmASmemBSmemCReg {
    template <typename CBlockTensor, typename ABlockWindow, typename BBlockWindow>
    CK_TILE_DEVICE void operator()(CBlockTensor& c,
                                   const ABlockWindow& a,
                                   const BBlockWindow& b) const {
        // 在内层循环中遍历K：
        static_for<0, KIterPerWarp, 1>{}([&](auto kIter) {
            static_for<0, MIterPerWarp, 1>{}([&](auto mIter) {
                AWarpTensor a_warp = load_tile(a_warp_windows(mIter)(kIter));
                static_for<0, NIterPerWarp, 1>{}([&](auto nIter) {
                    BWarpTensor b_warp = load_tile(b_warp_windows(nIter)(kIter));
                    WarpGemm{}(c_warp, a_warp, b_warp);  // ← 实际的乘加运算
                });
            });
        });
    }
};
```

**第三层 — 波前级GEMM（实际的MFMA指令）：**

**文件：** `ck/include/ck_tile/ops/gemm/warp/warp_gemm_attribute_mfma_impl.hpp`

这里是**实际的GPU矩阵乘法指令**被调用的地方：

```cpp
// F32 GEMM：使用MFMA的16x16x4 tile
struct WarpGemmAttributeMfmaImplF32F32F32M16N16K4 {
    // c_vec += a_vec * b_vec
    template <typename... Params>
    CK_TILE_DEVICE void operator()(CVecType& c_vec,
                                   const AVecType& a_vec,
                                   const AVecType& b_vec) const {
#if defined(__gfx9__)
        // 直接使用内建函数
        c_vec = __builtin_amdgcn_mfma_f32_16x16x4f32(a_vec[0], b_vec[0], c_vec, 0, 0, 0);
#else
        // 或使用内联汇编
        asm volatile("v_mfma_f32_16x16x4f32 %0, %1, %2, %3\n"
                     : "+v"(c_vec)
                     : "v"(a_vec), "v"(b_vec), "v"(c_vec));
#endif
    }
};
```

### 4. **hipBLASLt** — 轻量级备用后端

rocBLAS还支持**hipBLASLt**作为轻量级后端（位于`hipblaslt_host.cpp`）。这提供了使用hipBLASLt的`hipblasLtMatmul()` API的替代路径。

### 5. **rocWMMA** — 波前矩阵乘加API

**文件：** `rocwmma/internal/mma_impl.hpp`

rocWMMA提供了一个库级别的WMMA API，封装了硬件MFMA指令，支持不同的数据布局（行主序/列主序）。

---

### 架构总结

```
PyTorch / TensorFlow / 用户应用
         │
    ┌────▼────┐
    │ rocBLAS │  ← C = α·A·B + β·C  (BLAS GEMM API)
    └────┬────┘
         │
    ┌────▼──────────┐
    │   Tensile     │  ← YAML定义、预调优的汇编内核
    │  (主要)       │     加载目标GPU的.co代码对象
    └────┬──────────┘
         │
    ┌────▼──────────────────┐
    │ Composable Kernel (CK)│  ← 现代C++模板库
    │    (较新/可选)        │     基于tile，使用内建函数
    └────┬──────────────────┘
         │
    ┌────▼────────────┐
    │   AMDGPU ISA    │
    │ v_mfma / v_wmma │  ← 硬件矩阵指令
    └─────────────────┘
```

在AMD GPU上，实际的矩阵乘法最终归结为**MFMA**（矩阵融合乘加）指令——这是NVIDIA Tensor Core的AMD等效物——通过内联汇编或编译器内建函数（如`__builtin_amdgcn_mfma_f32_16x16x4f32`）来调用。
