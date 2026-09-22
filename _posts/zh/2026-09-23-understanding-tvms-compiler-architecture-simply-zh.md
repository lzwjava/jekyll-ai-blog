---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 简单理解TVM的编译器架构
translated: true
type: note
---

问题：**Apache TVM 简介——它是什么，我应该如何看待代码库？**

回答：

Apache TVM 本质上是一个**编译栈，用于将机器学习程序转换为针对特定硬件的快速代码**。

最简单的思维模型是：

```text
PyTorch / 模型
      │
      ▼
   Relax IR          ← "我想要什么计算？"
      │
      │ 图优化 / 算子融合 / 合法化
      ▼
   TensorIR           ← "我具体如何实现这些内核？"
      │
      │ 调度 / 降低 / 代码生成
      ▼
 CUDA / ROCm / LLVM / Metal / Vulkan / ...
      │
      ▼
 原生可执行文件
```

这就是现代 TVM 架构：**Relax + TensorIR**，而不是较旧的"Relay + TE"思维模型。（[GitHub][1]）

---

## 1. TVM 解决什么问题？

假设你用 PyTorch 编写：

```python
y = softmax(x @ W + b)
```

在 Python 层面，这几乎不说明它应该如何执行：

```text
矩阵乘法
  ↓
加法
  ↓
softmax
```

但 A100 想要更接近这样的内容：

```text
for 块 in CUDA 网格:
    从 HBM 加载数据块
    共享内存暂存
    tensor-core MMA
    warp 级归约
    向量化存储
```

AMD GPU 需要不同的实现。

CPU 需要另一种实现。

所以 TVM 的根本任务是：

```text
        高级机器学习程序
                 │
                 │ 编译器变换
                 ▼
       特定于硬件的程序
```

重要的区别在于 TVM 不仅仅是**算子库**。

它是一个**程序变换系统**。

官方项目将其描述为一个开放源码的机器学习编译框架，其当前设计专注于图级 Relax 和张量级 TensorIR 之间的跨层优化。（[GitHub][1]）

---

# 2. 你应该首先理解的两件事

暂时忽略代码库的大部分内容。

学习这两个：

```text
Relax
  ↓
TensorIR
```

### Relax = 图/程序级别

Relax 表示如下内容：

```text
x
│
├── 矩阵乘法
│
├── 加法
│
└── softmax
```

它理解：

* 张量
* 函数
* 数据流
* 控制流
* 形状信息
* 算子组合
* 图变换
* 算子融合

例如：

```python
@R.function
def main(
    x: R.Tensor((M, K), "float32"),
    w: R.Tensor((K, N), "float32"),
):
    y = R.matmul(x, w)
    return R.softmax(y)
```

概念上：

```text
Relax
 ┌──────────────────────────────┐
 │                              │
 │ x ──► matmul ──► softmax     │
 │             │                │
 │             ▼                │
 │             y                │
 │                              │
 └──────────────────────────────┘
```

因此，Relax 在某种程度上类似于**模型/程序整体的 IR**。（[Apache TVM][2]）

---

# 3. TensorIR 是真正有趣的地方

假设 Relax 最终说：

```text
C = A @ B
```

这对于生成高效的 GPU 代码来说仍然过于抽象。

TensorIR 可以表示实际的张量程序：

```python
for i, j, k in T.grid(M, N, K):
    with T.block("matmul"):
        ...
```

现在编译器可以变换实现：

```text
朴素实现
   ↓
分块
   ↓
重排序循环
   ↓
绑定 CUDA 线程
   ↓
向量化
   ↓
共享内存
   ↓
张量核心
```

这是 TVM 的关键思想：

> **算法和实现策略是分开的。**

例如：

```text
C[i,j] = Σk A[i,k] * B[k,j]
```

是算法。

这些是实现决策：

```text
分块大小
线程映射
内存布局
向量化
循环展开
共享内存
张量核心指令
```

TensorIR 为你提供了一个可编程的表示，其中这些决策可以被系统地变换。（[Apache TVM][3]）

---

# 4. 将 TVM 视为"张量程序的 LLVM"

一个有用的类比：

```text
LLVM：

C/C++
  ↓
LLVM IR
  ↓
优化
  ↓
机器码
```

TVM：

```text
机器学习模型
  ↓
Relax
  ↓
TensorIR
  ↓
优化 / 调度
  ↓
CUDA / ROCm / LLVM / ...
```

但有一个重要区别。

LLVM 主要优化**通用程序**。

TVM 专门设计用于优化**张量计算**，其中诸如：

```text
分块
布局
内存层次结构
张量核心
向量化
并行性
```

是一等公民。

---

# 5. 编译器流水线

架构文档大致描述了流程：

```text
                   IRModule
                      │
          ┌───────────┴───────────┐
          │                       │
       Relax                    TensorIR
          │                       │
          │ 变换                  │ 调度
          ▼                       ▼
      优化后的图                 优化后的内核
          │                       │
          └───────────┬───────────┘
                      ▼
                   代码生成
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        CUDA        LLVM        ROCm
          │           │           │
          └───────────┼───────────┘
                      ▼
                 runtime.Module
                      │
                      ▼
                   执行
```

中心数据结构是包含函数的**`IRModule`**。Relax 函数描述高级计算，而 TensorIR `PrimFunc` 描述低级张量程序。（[Apache TVM][3]）

---

# 6. 为什么 `IRModule` 很重要

如果你浏览源码，这是我会尽早学习的一个抽象。

想想：

```python
IRModule = {
    relax_function_1,
    relax_function_2,
    tir_primfunc_1,
    tir_primfunc_2,
    ...
}
```

然后编译器遍历反复变换它：

```text
IRModule
   │
   ▼
Pass A
   │
   ▼
IRModule'
   │
   ▼
Pass B
   │
   ▼
IRModule''
   │
   ▼
代码生成
```

这非常符合编译器风格。

而不是：

```text
模型 → 魔法编译器 → 二进制
```

你得到：

```text
程序
  ↓
IR
  ↓
IR 变换
  ↓
IR 变换
  ↓
IR 变换
  ↓
降低后的 IR
  ↓
机器码
```

这使得 TVM 可被轻松修改和扩展。

---

# 7. 一个具体示例

想象一下：

```python
y = x @ W
```

在 Relax 级别：

```text
call_tir(matmul, x, W)
```

然后 TensorIR 可能包含类似的概念：

```python
@T.prim_func
def matmul(
    A: T.Buffer((M, K), "float32"),
    B: T.Buffer((K, N), "float32"),
    C: T.Buffer((M, N), "float32"),
):
    for i, j, k in T.grid(M, N, K):
        with T.block("matmul"):
            C[i, j] += A[i, k] * B[k, j]
```

然后调度变换：

```text
             原始实现
                │
                ▼
       ┌─────────────────┐
       │ i,j,k 循环      │
       └─────────────────┘
                │
             分块
                ▼
       ┌─────────────────┐
       │ io / jo / ko    │
       │ ii / ji / ki    │
       └─────────────────┘
                │
          线程绑定
                ▼
       CUDA 线程/块
                │
          内存布局
                ▼
       共享内存/寄存器
                │
          指令选择
                ▼
       CUDA 内核
```

这就是 TVM 的核心。

---

# 8. 自动调优的作用

这是另一个重要思想。

你并不一定知道最优调度：

```text
tile_M = ?
tile_N = ?
tile_K = ?
num_warps = ?
vector_width = ?
shared_memory_layout = ?
```

TVM 可以搜索。

历史上这演变为 **AutoTVM / Ansor / MetaSchedule**。当前文档将 MetaSchedule 展示为基于搜索的自动调优系统，而 DLight 提供基于规则的调度。（[Apache TVM][4]）

概念上：

```text
                  TensorIR
                     │
          ┌──────────┼──────────┐
          │          │          │
       调度1      调度2      调度3
          │          │          │
        120 μs      80 μs      95 μs
          │          │          │
          └──────────┼──────────┘
                     ▼
                   80 μs
```

这就是 TVM 开始看起来不太像传统编译器，而更像是：

```text
编译器
   +
搜索
   +
性能工程
```

的地方。

---

# 9. 运行时

编译之后，TVM 需要某个地方来执行生成的代码。

所以：

```text
编译器
   │
   ▼
runtime.Module
   │
   ▼
TVM 运行时
   │
   ├── CPU
   ├── CUDA
   ├── ROCm
   ├── Vulkan
   ├── Metal
   └── ...
```

运行时抽象了诸如：

```text
内存分配
设备管理
函数调用
模块加载
RPC
```

等内容。

具体到 Relax，**Relax VM** 执行高级编译程序，并将实际计算分派给编译后的 TIR 内核或外部库。其指令集设计得非常小；VM 主要编排执行，而不是自身进行数值计算。（[Apache TVM][5]）

所以：

```text
Relax VM
   │
   ├── 调用内核 A
   ├── 分配张量
   ├── 调用内核 B
   ├── 分支
   └── 返回
```

而：

```text
CUDA 内核
```

实际执行：

```text
FMA
加载
存储
归约
...
```

---

# 10. 代码库布局

当前代码库非常庞大，所以不要从头到尾阅读。

有趣的部分大致是：

```text
tvm/
├── python/
│   └── tvm/
│       ├── relax/       # 图级编译器
│       ├── tirx/        # TensorIR 表示/降低
│       ├── s_tir/       # 调度 / 调优
│       ├── target/      # 目标抽象
│       ├── runtime/     # 运行时
│       └── ...
│
├── src/
│   ├── relax/
│   ├── tir/
│   ├── runtime/
│   └── ...
│
├── include/tvm/
│
├── tests/
│
└── docs/
```

代码库本身目前将该项目的设计描述为以 Python 优先，并特别强调其围绕 Relax 和 TensorIR 的跨层设计。（[GitHub][1]）

---

# 11. 一个重要的历史提示

如果你搜索 Google/旧博客文章，你会看到：

```text
Relay
TE
TOPI
AutoTVM
AutoScheduler
```

这些在历史上很重要，但**不要围绕它们构建你对当前 TVM 的思维模型**。

该架构经历了多次重新设计。当前项目明确将其近期方向描述为：

```text
Relax
   +
TensorIR
   +
Python 优先变换
   +
跨层优化
```

并表示该栈还旨在作为垂直编译器的基础设施，包括面向 LLM 的系统。（[GitHub][1]）

---

# 12. 为什么这对 LLM 推理很有趣

考虑到你正在构建的系统类型，这可能是我会关注的部分。

从编译器的角度来看，LLM 并不是根本特殊的。

在底层它仍然是：

```text
矩阵乘法
注意力
RMSNorm
RoPE
softmax
逐元素操作
归约
KV 缓存操作
```

但现代推理在以下方面存在复杂的交互：

```text
图结构
      +
内核实现
      +
内存布局
      +
量化
      +
GPU 架构
      +
通信
```

跨层编译器可以同时推理这些层中的多层。

例如：

```text
Relax

   注意力
      │
      ├── Q 投影
      ├── K 投影
      ├── V 投影
      ├── 注意力
      └── 输出投影
             │
             ▼
          TensorIR
             │
       ┌─────┴─────┐
       │           │
   内核 A      内核 B
       │           │
       ▼           ▼
      CUDA        CUDA
```

而且 TVM 当前的栈还包括 **Disco**，其分布式运行时，用于多设备执行和集体通信（如 allreduce/allgather）。（[Apache TVM][3]）

---

# 13. 我会学得最快的方式

不要阅读整个 TVM 代码库。

我会这样做：

### 第 1 步 — 编写一个 TensorIR 内核

从以下开始：

```text
向量加法
```

然后：

```text
矩阵乘法
```

然后：

```text
softmax
```

理解：

```text
PrimFunc
Buffer
Block
Loop
Schedule
```

### 第 2 步 — 学习调度

以：

```text
C[i,j] = Σ A[i,k]B[k,j]
```

为例，手动实现：

```text
朴素
→ 分块
→ 并行
→ 向量化
→ GPU
```

这是 TVM 真正价值变得明显的地方。

### 第 3 步 — 学习 Relax

然后：

```text
矩阵乘法 → 加法 → softmax
```

作为一个图。

理解：

```text
Relax Function
IRModule
DataflowBlock
Call
Shape
Tensor
Pass
```

### 第 4 步 — 跟踪降低过程

追踪：

```text
Relax
  ↓
FuseOps
  ↓
LegalizeOps
  ↓
call_tir
  ↓
TensorIR
  ↓
调度
  ↓
CUDA
```

架构文档明确建议在深入各个组件之前，先从整体编译流程开始。（[Apache TVM][3]）

### 第 5 步 — 阅读实现

然后我会跳入：

```bash
git clone https://github.com/apache/tvm
cd tvm

rg "class IRModule" python src
rg "class PrimFunc" python src
rg "class Schedule" python src
rg "FuseOps" python src
rg "MetaSchedule" python src
```

关键是**端到端地跟踪一个内核**，而不是试图全局理解 TVM。

---

## 一句话的思维模型

如果你只记住这个：

```text
TVM = 张量程序的可编程编译器。

Relax    → 机器学习程序计算什么
TensorIR → 计算如何实现
Schedule → 我们如何优化该实现
Target   → 我们在为哪个硬件编译
Runtime  → 结果程序如何执行
```

而整个过程基本上是：

```text
        模型
          │
          ▼
       RELAX
    "计算什么"
          │
          ▼
     TENSORIR
   "如何计算"
          │
          ▼
      调度
   "让它变快"
          │
          ▼
       代码生成
    "针对此 GPU"
          │
          ▼
       运行时
       "执行"
```

这就是我在阅读代码库时心中保留的架构。

### 参考文献

* [Apache TVM 代码库](https://github.com/apache/tvm?utm_source=chatgpt.com) （[GitHub][1]）
* [TVM 设计与架构](https://tvm.apache.org/docs/arch/?utm_source=chatgpt.com) （[Apache TVM][3]）
* [TVM Relax 文档](https://tvm.apache.org/docs/deep_dive/relax/index.html?utm_source=chatgpt.com) （[Apache TVM][2]）
* [Relax VM 架构](https://tvm.apache.org/docs/arch/relax_vm.html?utm_source=chatgpt.com) （[Apache TVM][5]）

接下来我可以逐行走一遍**从 Relax → TensorIR → CUDA 的单个 `matmul`**，这可能是让架构最快速深入理解的方式。

[1]: https://github.com/apache/tvm "GitHub - apache/tvm: 开放机器学习编译器框架 · GitHub"
[2]: https://tvm.apache.org/docs/deep_dive/relax/index.html?utm_source=chatgpt.com "Relax — Apache TVM"
[3]: https://tvm.apache.org/docs/arch/?utm_source=chatgpt.com "设计与架构 — Apache TVM"
[4]: https://tvm.apache.org/docs/?utm_source=chatgpt.com "Apache TVM 文档 — Apache TVM"
[5]: https://tvm.apache.org/docs/arch/relax_vm.html?utm_source=chatgpt.com "Relax 虚拟机 — Apache TVM"