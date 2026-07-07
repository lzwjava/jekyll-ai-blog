---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SM120表示计算能力12.0
translated: true
type: note
---

问题：在NVIDIA GPU术语中，SM120 是什么意思？SM 是流式多处理器（Streaming Multiprocessor）吗？工程师会把 H200/RTX4070 称为 "SM120" 吗？

回答：

你的理解接近，但有两个相关含义：

## 1. SM = 流式多处理器（Streaming Multiprocessor）

是的，**SM 代表流式多处理器**。它是 NVIDIA GPU 内部的基本执行单元。

一个 GPU 大致结构如下：

```
GPU
 ├── SM 0
 │    ├── CUDA 核心
 │    ├── Tensor 核心
 │    ├── 寄存器
 │    ├── 共享内存
 │    └── 线程束调度器
 │
 ├── SM 1
 │    └── ...
 │
 └── SM N
```

CUDA 在 SM 级别调度工作。一个 CUDA 内核会启动线程块，而这些线程块会被分配到 SM 上。

（[NVIDIA 文档][1]）

---

## 2. 但 "SM120" 通常指的是计算能力 12.0

当 NVIDIA 工程师说：

```
sm_120
SM120
```

他们通常指的是 **CUDA 计算能力 12.0**，而不是 "该 GPU 有 120 个流式多处理器"。

命名方式：

```
sm_<主版本号><次版本号>

sm_80  = 计算能力 8.0
sm_86  = 计算能力 8.6
sm_89  = 计算能力 8.9
sm_90  = 计算能力 9.0
sm_120 = 计算能力 12.0
```

CUDA 编译器的目标名称就是这样命名的。（[NVIDIA 开发者][2]）

例如：

```bash
nvcc kernel.cu -arch=sm_120
```

意思是：

"编译这个 CUDA 内核，优化目标为 Blackwell 计算能力 12.0。"

---

## 3. 你举的例子并不准确

### RTX 4070

Ada Lovelace 架构：

```
架构：Ada
计算能力：8.9
CUDA 目标：sm_89
```

因此：

```
RTX 4070 -> SM89
```

而不是 SM120。

---

### H200

Hopper 架构：

```
架构：Hopper
计算能力：9.0
CUDA 目标：sm_90
```

因此：

```
H200 -> SM90
```

而不是 SM120。

---

### RTX 5090 / RTX PRO Blackwell

Blackwell 消费级/工作站架构：

```
架构：Blackwell
计算能力：12.0
CUDA 目标：sm_120
```

因此：

```
RTX 5090 -> SM120
```

（[NVIDIA 开发者][2]）

---

工程师的简称大致如下：

| GPU       | 架构                | CUDA 目标 |
| --------- | ------------------- | --------- |
| RTX 4090  | Ada                 | sm_89     |
| RTX 4070  | Ada                 | sm_89     |
| H100/H200 | Hopper              | sm_90     |
| B200      | Blackwell 数据中心  | sm_100    |
| RTX 5090  | Blackwell 消费级    | sm_120    |

（[NVIDIA 开发者][2]）

---

对于 AI 内核开发来说，这一点很重要，因为像 **PyTorch、FlashAttention、Triton、CUTLASS、vLLM** 等库会针对这些目标编译专门的内核。

例如：

```bash
TORCH_CUDA_ARCH_LIST="8.9;9.0;12.0"
```

意思是：

"为 Ada、Hopper 和 Blackwell 构建内核。"

仅为 `sm_89` 编译的内核可能通过 PTX JIT 在更新的 GPU 上运行，但不一定能使用新硬件特性，比如 Blackwell 的 FP4/Tensor Core 指令。（[NVIDIA 开发者][3]）

所以，当 NVIDIA 工程师说 "SM120" 时，他们是在谈论 CUDA 编译器/硬件能力语言，而不是字面上的 SM 数量。

[1]: https://docs.nvidia.com/cuda/archive/12.8.0/pdf/Blackwell_Tuning_Guide.pdf?utm_source=chatgpt.com "Blackwell 调优指南"
[2]: https://developer.nvidia.com/cuda/gpus?utm_source=chatgpt.com "CUDA GPU 计算能力 | NVIDIA 开发者"
[3]: https://developer.nvidia.com/blog/nvidia-blackwell-and-nvidia-cuda-12-9-introduce-family-specific-architecture-features/?utm_source=chatgpt.com "NVIDIA Blackwell 与 NVIDIA CUDA 12.9 引入系列特定架构特性 | NVIDIA 技术博客"
