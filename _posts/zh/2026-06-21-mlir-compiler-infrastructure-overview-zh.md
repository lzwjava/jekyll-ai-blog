---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MLIR编译器基础设施概述
translated: true
type: note
---

**问题：** 请介绍 MLIR（mlir.llvm.org）。

**回答：**

## MLIR：多层次中间表示

MLIR 是一个编译器基础设施框架，位于**高级 ML 框架与底层代码生成之间**。它最初由 Google 开发，现在隶属于 LLVM 项目，是 TensorFlow/XLA、JAX、PyTorch（通过 Torch-MLIR）以及大多数严肃 ML 编译器当前工作的核心。

### 它解决的核心问题

在 MLIR 出现之前，每个 ML 框架都构建了自己的 IR、自己的图优化器、自己的降级流水线。TensorFlow 有 XLA HLO，PyTorch 有 TorchScript IR，TOSA 用于边缘设备，CUDA 有 PTX。在这些框架之间复用优化 pass 几乎是不可能的——**N 个框架 × M 个硬件目标 = N×M 个专用编译器**。

MLIR 的解决方案：一个可扩展的 IR，带有一套**方言（dialect）系统**，允许多种抽象层次共存于同一个 IR 中，并逐步降级到彼此之上。

### 关键概念

#### 1. 操作（Ops）

MLIR 中的所有东西都是 `Op`。一个操作包含：

- 名称（`linalg.matmul`、`arith.addi`、`func.call`）
- 操作数（输入的 SSA 值）
- 结果（输出的 SSA 值）
- 属性（编译时常量）
- 区域（嵌套的作用域——循环和函数的表示方式）

```mlir
// 一个简单的 MLIR 片段
func.func @matmul(%A: memref<4x4xf32>, %B: memref<4x4xf32>, %C: memref<4x4xf32>) {
  linalg.matmul ins(%A, %B : memref<4x4xf32>, memref<4x4xf32>)
               outs(%C : memref<4x4xf32>)
  return
}
```

#### 2. 方言（Dialects）

方言是操作、类型和属性的命名空间，用于建模特定的抽象层次。可以将每个方言看作一个“迷你 IR”：

| 方言 | 层次 | 用途 |
| ------ | ------ | ------ |
| `linalg` | 高 | 命名的张量收缩（矩阵乘、卷积） |
| `affine` | 高 | 多面体循环建模 |
| `scf` | 中 | 结构化控制流（for/if/while） |
| `memref` | 中 | 内存引用语义 |
| `arith` | 低 | 标量算术 |
| `llvm` | 极低 | 一对一映射到 LLVM IR |
| `gpu` | 并行 | GPU 内核抽象 |
| `amdgpu` / `nvgpu` | 硬件专用 | ROCm / CUDA 内联函数 |

对于你的 MI300X 相关工作，`amdgpu` 和 `rocdl` 方言直接相关——它们建模了最终降级到 AMDGPU ISA 的 AMD 专用操作。

#### 3. 逐步降级（核心思想）

你不会直接从 `linalg.matmul` 跳到 PTX。你需要经过一个**方言转换流水线**降级：

```
linalg.matmul
    ↓  (平铺 + 向量化)
scf.for + vector.contract
    ↓  (缓冲化)
memref + scf
    ↓  (降级到 GPU)
gpu.launch
    ↓  (转换为 LLVM)
llvm.func  →  LLVM IR  →  PTX / AMDGPU ISA
```

每一步都是一个 **pass**——一种将操作从一种方言重写为另一种方言的转换。多个 pass 可以组合成流水线。

#### 4. 区域与 SSA

MLIR 扩展了 SSA（类似 LLVM），引入了**区域（regions）**——可以嵌套在其他操作内部的块。这使得单个 IR 既能表示高层数据流图，也能表示底层循环，而无需切换表示方式。这就是 `scf.for` 如何持有循环体，或者 `func.func` 如何持有函数体的方式。

### 为什么它对 AI/ML 编译器重要

- **TensorFlow → XLA → StableHLO → MLIR** 流水线
- **PyTorch 2.0 (torch.compile)** 使用 `torch-mlir` 将张量操作降级到 `linalg`
- **IREE**（Google 的推理运行时）几乎完全基于 MLIR
- **Triton**（OpenAI 的 GPU 内核 DSL）在到达 PTX/AMDGPU 之前通过 MLIR pass 进行编译
- **JAX 的 mosaic**（用于 TPU）基于 MLIR

考虑到你在 MI300X 上的训练工作，这一层位于你的 PyTorch 模型与实际 ROCm 内核执行之间。理解它让你能够编写自定义 MLIR pass 来融合操作、为 HBM 带宽进行平铺，或检查编译器实际生成的代码。

### 极简上手入口

Toy 教程是标准入门——它构建了一个小语言，并通过 MLIR 一直降级到 LLVM IR。但对于 AI 工程，我建议从 Python 绑定开始：

```python
# pip install mlir-python-bindings (或从 llvm-project 构建)
from mlir.ir import Context, Module
from mlir.dialects import func, arith

with Context():
    module = Module.parse("""
        func.func @add(%a: i32, %b: i32) -> i32 {
            %c = arith.addi %a, %b : i32
            return %c : i32
        }
    """)
    print(module)
```

对于你的 GPU/训练路径：查看 **IREE** 和 **Triton** 的 MLIR 后端——这些是与你 MI300X 工作直接相关的实际生产用例。

### 心智模型

将 MLIR 视作**IR 界的 Git**——它提供了一个通用基础、版本控制的抽象层和可组合的转换，而不是每个项目都重新发明轮子。方言系统是其杀手锏：你可以在同一个 IR 文件中混用 `linalg` + `gpu` + `affine`，并独立地对它们进行降级。

**参考链接：**

- [MLIR 主页](https://mlir.llvm.org)
- [MLIR 语言参考](https://mlir.llvm.org/docs/LangRef/)
- [Toy 教程（第 1–7 章）](https://mlir.llvm.org/docs/Tutorials/Toy/)
- [MLIR 设计原理](https://mlir.llvm.org/docs/Rationale/Rationale/)
- [AMDGPU 方言](https://mlir.llvm.org/docs/Dialects/AMDGPU/)
