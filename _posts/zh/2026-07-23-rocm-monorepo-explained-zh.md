---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm Monorepo 解析
translated: true
type: note
---

## 问题：什么是 ROCm 单体仓库（monorepo），我们应该如何理解它？

## 回答：

AMD ROCm（Radeon Open Compute 平台）是 AMD 的 **开放 GPU 软件栈**，类似于 NVIDIA CUDA。

要点：**ROCm 不是一个库，而是一个生态系统。**

GitHub 仓库 `ROCm/ROCm` 是一个 **元仓库**。它并不包含 ROCm 的完整实现，而是充当一个 **地图/索引/构建清单**，连接着数百个 ROCm 组件。

一个心智模型：

```
                AI 框架
                     |
        +------------+-------------+
        |                          |
     PyTorch                  TensorFlow
        |
        |
       HIP
 (类似 CUDA 的编程层)
        |
        |
    ROCr / ROCclr
 (GPU 运行时层)
        |
        |
    HSA 运行时
 (硬件抽象层)
        |
        |
     AMD GPU
 MI300X / MI250 / MI210 / Radeon
```

---

## 1. HIP —— AMD 的 CUDA 替代方案

ROCm 最重要的组件是 **HIP**。

CUDA：

```cpp
__global__ void add(float *a, float *b) {
    int i = threadIdx.x;
    a[i] += b[i];
}
```

HIP：

```cpp
__global__ void add(float *a, float *b) {
    int i = hipThreadIdx_x;
    a[i] += b[i];
}
```

HIP 致力于让 CUDA 代码可移植。

示例：

```
CUDA 代码
    |
    | hipify 工具
    v
HIP 代码
    |
    v
AMD GPU
```

PyTorch 对 AMD 的许多支持，都是因为 PyTorch 的 CUDA 核函数可以转换为 HIP。

---

## 2. 数学库

CUDA 拥有：

```
cuBLAS
cuFFT
cuRAND
cuSPARSE
```

ROCm 的对应库：

| NVIDIA   | AMD ROCm  |
| -------- | --------- |
| cuBLAS   | rocBLAS   |
| cuFFT    | rocFFT    |
| cuRAND   | rocRAND   |
| cuSPARSE | rocSPARSE |
| cuSOLVER | rocSOLVER |

示例：

矩阵乘法：

```
C = A × B
```

AI 训练中大量时间花费在此。

PyTorch：

```python
torch.matmul(a,b)
```

最终变为：

```
PyTorch
  |
ATen
  |
rocBLAS
  |
HIP
  |
GPU 矩阵核心
```

---

## 3. 编译器栈

ROCm 拥有自己的编译器基础设施：

```
C++ / HIP 源码
        |
        v
      clang
        |
        v
    LLVM 后端
        |
        v
    AMD GCN / CDNA 指令集
        |
        v
      GPU
```

重要组成部分：

### ROCm 编译器支持

提供：

* clang HIP 编译器
* LLVM 补丁
* 设备库

示例：

```bash
hipcc hello.cpp
```

是 AMD 对以下命令的等效：

```bash
nvcc hello.cu
```

---

## 4. GPU 运行时

运行时管理：

* GPU 内存
* 核函数启动
* 同步
* 队列

NVIDIA：

```
CUDA 运行时
      |
CUDA 驱动
      |
GPU
```

AMD：

```
HIP 运行时
      |
ROCr 运行时
      |
HSA
      |
GPU
```

HSA = 异构系统架构（Heterogeneous System Architecture）。

AMD 围绕 CPU + GPU 集成设计了这一架构。

---

## 5. 通信库：RCCL

对于 AI 集群，这一点至关重要。

NVIDIA：

```
NCCL
```

AMD：

```
RCCL
```

示例：

训练 GPT：

```
GPU0              GPU1

层梯度

     |
     v

 all-reduce（全归约）

     |
     v

 同步后的权重
```

PyTorch 分布式：

```python
torch.distributed.all_reduce()
```

在 NVIDIA 上：

```
NCCL
```

在 AMD 上：

```
RCCL
```

对于 MI300X 集群，RCCL 是核心组件。

---

## 6. 性能分析与调试

类似 NVIDIA Nsight：

AMD 拥有：

### rocprofiler

性能计数器：

```
GPU 利用率
内存带宽
核函数时间
缓存行为
```

示例：

```bash
rocprof ./train.py
```

### roctracer

跟踪：

```
PyTorch
 |
HIP 核函数
 |
GPU 执行时间线
```

有助于发现：

* 慢速核函数
* CPU 瓶颈
* 同步问题

---

## 7. 深度学习栈

现代 AI：

```
用户
 |
PyTorch
 |
torch-mlir / ATen
 |
HIP
 |
MIOpen
 |
rocBLAS
 |
ROCm
 |
MI300X
```

对应的 NVIDIA 栈：

```
PyTorch
 |
CUDA
 |
cuDNN
 |
cuBLAS
 |
CUDA 驱动
 |
H100
```

---

## 8. 为什么 ROCm 对 AI 很重要

历史上：

```
NVIDIA:
CUDA 生态系统优势
---------------------------------
GPU
CUDA
cuDNN
TensorRT
NCCL
PyTorch 支持
开发者工具
```

AMD 拥有：

```
GPU
+
硬件优势
-
软件生态系统差距
```

ROCm 是 AMD 缩小这一差距的尝试。

例如：

### MI300X

硬件：

```
192GB HBM3
5.3 TB/s 带宽
```

软件：

```
ROCm
 |
PyTorch
 |
DeepSpeed
 |
Megatron
 |
vLLM
```

没有 ROCm，MI300X 无法与 H100/H200 竞争。

---

## 9. 作为工程师如何理解 ROCm 仓库

该仓库类似于 Linux 内核的伞式仓库。

通常你不会直接修改它。

你与之交互的方式：

AI 开发者：

```
pip install torch
```

然后：

```
torch.version.hip
```

核函数开发者：

```
HIP C++ 核函数
```

编译器开发者：

```
LLVM / clang
```

性能工程师：

```
rocprof
```

集群工程师：

```
RCCL + Kubernetes
```

---

## 10. 与你的 MI300X / PyTorch 工作的关系

对于你的用例（训练 GPT 风格模型）：

```
nanoGPT
 |
PyTorch
 |
ROCm PyTorch 构建
 |
HIP
 |
rocBLAS
 |
MIOpen
 |
RCCL（多 GPU）
 |
MI300X
```

你的大部分代码保持不变：

```python
device="cuda"
```

即使在 AMD 上也是如此。

PyTorch 暴露：

```python
torch.cuda.is_available()
```

因为 HIP 有意模仿 CUDA API。

示例：

```python
import torch

print(torch.cuda.is_available())
print(torch.version.hip)
```

在 AMD 上的输出：

```
True
6.2.x
```

---

## 总结

ROCm 本质上是：

```
AMD GPU 对 CUDA 的等效实现

          ROCm
           |
 +---------+----------+
 |         |          |
 HIP    Libraries   Tools
 |         |          |
CUDA    BLAS       Profiler
API     FFT        Debugger

           |
        PyTorch

           |
        MI300X
```

对于 AI 基础设施，需要理解的两个最大组件是：

1. **HIP** → CUDA 兼容层
2. **RCCL** → 多 GPU 训练通信

ROCm 单体仓库是连接所有这些组件的“目录”。