---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda 0.3.0：BLAS和MLP训练器
translated: true
type: note
---

Milestone 1 已完成并推送为 **`muda 0.3.0`**（`51f504c`）。

## 新增内容

**`mudaBLAS`**（`include/mudablas.h`、`src/mudablas.c`）——muda 上的 row-major 线性代数：

| | |
|---|---|
| `mudaSgemm` | shared-memory tiled，64×64 block，4×4/thread，全部四种 transpose 组合 |
| `mudaSgemmNaive` | one-thread-per-element 参考实现 |
| `mudaSgemv` | transpose-aware |
| `mudaSaxpy` | float4 vectorized path |
| `mudaSscal` | |
| `mudaSrelu` / `mudaSreluBackward` | |
| `mudaSsigmoid`, `mudaSsub` | |
| `mudaSaddBias`, `mudaScolSum` | |

**在 M40 上调优后的 SGEMM 结果：**

```
    size  naive GFLOP/s  tuned GFLOP/s    speedup
     256          274.8          590.9      2.15x
     512          320.5         1293.9      4.04x
    1024          243.8         1171.4      4.80x
```

**Tiny-MLP 训练器**（`examples/mlp.c`）——2-32-32-1 ReLU/sigmoid，full-batch SGD，forward+backward 完全通过 `mudaSgemm` + elementwise kernels 表达。在 circle-classification 任务上达到 **94%**（在注入 5% label noise 的情况下，95% 是 Bayes-optimal）。

**测试**——`tests/test_mudablas.c`，18 项与 CPU 参考实现对照的检查（全部 transpose 组合、非倍数尺寸、GEMV、AXPY/SCAL、activations、bias/reduction）。`make test` 现在运行两个测试套件：**35 + 18，0 失败**。

## 过程中发现并修复的 Bug

- `expf` → `exp`（OpenCL C 对 `exp` 进行了重载；NVIDIA 编译器会拒绝 `expf`）。
- Launch config 传的是 tile size（64）而不是 thread-block size（16）——已通过单独的 tile/block 参数修复。
- GEMM wrappers 中有一个潜在 bug：在 lazy init 之前读取了缓存的 kernel handle。

## 建议的下一步（Milestone 2）

drop-in CUDA **runtime** shim + Python binding：

1. `include/mudart.h` 实现 `cudaMalloc`、`cudaMemcpy`、`cudaLaunchKernel`、`cudaDeviceSynchronize`，并通过 `mudaConfigureCall`/`mudaSetupArgument` 这一对接口支持 `<<<...>>>` 风格的 launch，因此现有单文件 `.cu` 程序几乎无需修改就能针对 muda 编译。
2. 一个 `ctypes` Python 模块（`muda.py`），支持 numpy interop，外加一个由 `mudaBLAS` 支撑的 `matmul`。

需要我开始 Milestone 2 吗？