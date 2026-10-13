---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda 0.5.0 预处理器发布
translated: true
type: note
---

Milestone 3 已完成并推送为 **`muda 0.5.0`** (`4ea6be2`)。

## 新增内容

**`mudac` — 一个 `<<<...>>>` 预处理器** (`tools/mudac.c`)

它将普通的 `.cu` 文件转换为无需 `nvcc` 即可针对 muda 编译的内容：

```sh
make build/mudac
build/mudac prog.cu -o prog.cc
c++ -std=gnu++17 -Iinclude prog.cc build/libmuda.a -ldl -lpthread -lm -o prog
./prog
```

它：

1. **提取** 每个 `__global__`/`__device__` 函数为字符串常量，并从宿主代码中移除定义（驱动程序在运行时编译它）。
2. **重写** `kernel<<<grid, block, shared, stream>>>(a, b, n)` 为 `mudartLaunchByName("kernel", ...)`，使用 GNU 语句表达式获取每个参数地址——因此 `2.0f`、`n+1` 等都能正常工作。
3. **替换** `#include <cuda_runtime.h>` 为 `#include "mudart.h"`。

维度可以是 int 或 `dim3`；生成的代码会根据你写的类型选择。

## 为 `mudart` 添加的运行时支持
- `mudartLoadKernelSource` / `mudartLaunchByName`，带 name→函数缓存
- 运行时构造函数，使 `cudaMalloc` 在首次启动之前就能工作
- C++ `dim3` 构造函数 + 重载维度辅助函数（用于 C++ 编译），其中 `MUDAC_AUTO` 在 C++ 中映射到 `auto`，在 C 中映射到 `__auto_type`

## 已验证
```
make test
  35 passed  (core)
  18 passed  (mudaBLAS)
  11 passed  (mudart)
  mudac vector_add: OK                          # stock CUDA program
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK
```

发现并修复了两个真实 bug：C++ 重载不能存在于 `extern "C"` 内部，并且在传递静态归档文件之前，必须用 `-x none` 重置 `-x c++`。

## 项目现状
`muda` 现在覆盖了完整弧线：原始运行时 → 兼容 CUDA 的 API → CUDA 运行时 shim → `<<<>>>` 源码前端 → BLAS + MLP 演示 → Python。README 路线图列出了后续步骤（在 mudac 中实现 `cudaMemcpyToSymbol`/`__constant__`、双缓冲 GEMM、`driver_cpu`，以及原生的 `driver_nouveau`）。

要我继续推进 **原生 `nouveau` 后端 spike**（真正的“无 NVIDIA 用户空间”路径），还是先加固当前栈（更多 mudac 覆盖 + 为无 GPU CI 的 `driver_cpu`）？