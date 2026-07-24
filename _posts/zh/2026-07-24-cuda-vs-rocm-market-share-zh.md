---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA与ROCm市场份额
translated: true
type: note
---

**CUDA vs ROCm — 市场份额如何？**

答案：

简短版：

```
AI GPU 计算生态（2025-2026）

NVIDIA CUDA  ████████████████████████████████████  ~80-90%+
AMD ROCm     ██                                    低个位数 / 增长中
其他         █                                     (TPU、Trainium、Ascend 等)
```

具体数字很难精确，因为"市场份额"可以指：

1.  发货的 GPU 硬件
2.  AI 训练集群
3.  开发者使用情况
4.  框架生态
5.  云端可用性

但在所有维度上，CUDA 仍然占据压倒性主导地位。（[OECD][1]）

---

## 1. 硬件市场份额

对于 AI 数据中心 GPU：

*   NVIDIA 占据主导，估计在 AI GPU 份额中超过 80%。（[OECD][1]）
*   AMD Instinct（MI300X/MI325X/MI355X 等）是主要竞争对手，但仍远远落后。（[AMD][2]）

原因不仅仅在于硬件。

一个 GPU 包含：

```
GPU 芯片
+
驱动程序
+
编译器
+
核心库
+
框架集成
+
开发者生态
```

CUDA 几乎拥有整个堆栈。

---

## 2. 开发者生态份额

这是 CUDA 护城河最深的地方。

典型的 AI 堆栈：

```
PyTorch
   |
   |
CUDA
   |
cuDNN
cuBLAS
TensorRT
NCCL
   |
NVIDIA GPU
```

大多数论文、教程、GitHub 仓库、优化技巧：

```
CUDA 优先
```

示例：

一位研究人员编写：

```python
x = torch.randn(1024,1024).cuda()

model.cuda()
```

他们期望使用 NVIDIA。

---

ROCm 堆栈：

```
PyTorch
   |
HIP
   |
rocBLAS
MIOpen
RCCL
   |
AMD GPU
```

技术上相似：

```
CUDA 核函数

__global__ void kernel()

        |
        v

HIP 核函数

__global__ void kernel()
```

HIP 刻意模仿 CUDA 以降低迁移成本。

---

## 3. 为什么 ROCm 在改进

AMD 有一个主要优势：

**开放的软件堆栈。**

ROCm 的源代码比 CUDA 更开放。

这很重要，因为 AI 本身加速了软件迁移：

```
旧世界：

CUDA 代码
     |
     | 工程师数月手动操作
     v
ROCm 移植


AI 世界：

CUDA 代码
     |
     | 大语言模型智能体
     v
HIP/Triton 转换
```

因此切换成本正在降低。

研究项目已经在探索自动化的 CUDA↔HIP 转换。（[arXiv][3]）

---

## 4. 为什么 CUDA 仍然难以取代

真正的护城河不是 CUDA 语法。

而是：

### 库

示例：

训练类 GPT 模型：

```
注意力机制
矩阵乘法
层归一化
softmax
优化器
通信
```

PyTorch 底层：

```
cuBLAS
cuDNN
FlashAttention 核函数
NCCL
TensorRT
```

数千个优化过的核函数。

---

### 分布式训练

大型集群：

```
GPU0
 |
NVLink
 |
GPU1
 |
NVSwitch
 |
GPU2
```

NVIDIA 拥有：

```
NVLink
NCCL
CUDA Graphs
TensorRT-LLM
Megatron 集成
```

这非常成熟。

---

## 5. 当前的实际选择

对于 AI 工程师：

### 研究 / 初创公司 / 本地实验

CUDA：

```
RTX 4070
RTX 4090
RTX 5090
A100
H100
B200
```

开箱即用。

安装：

```bash
pip install torch
```

完成。

---

ROCm：

示例：

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm
```

有时可用。

有时会遇到：

```
缺少算子
内核错误
不支持的 GPU
库不匹配
```

生态正在改善，但不够流畅。（[AIMultiple][4]）

---

## 6. 长期趋势

可能的未来：

```
2020-2025

CUDA 垄断
        |
        |
        v

2026-2030

CUDA 主导
+
ROCm 可信的替代方案
+
TPU
+
Trainium
+
Ascend
```

CUDA 可能不会消失。

更现实的场景是：

```
NVIDIA CUDA: 70-80%

AMD ROCm: 10-20%

其他：剩余部分
```

而不是：

```
CUDA 100%
ROCm 0%
```

AMD 在 AI 基础设施和大客户方面正变得认真，但软件生态仍然是关键战场。（[Reuters][5]）

---

对于构建/训练模型的人：

我的思维模型：

```
CUDA = AI 领域的 Linux x86

ROCm = 挑战者的 Linux ARM
```

硬件可以更快地追赶。

软件生态需要数年时间。

参考资料：

*   OECD — 人工智能基础设施中的竞争（[OECD][1]）
*   Statista / SemiAnalysis — NVIDIA 与 AMD 数据中心 AI GPU 市场份额（[Statista][6]）
*   AMD Instinct 与 NVIDIA 数据中心 GPU 概览（[AMD][2]）
*   CUDA 与 ROCm 生态对比（[AIMultiple][4]）

[1]: https://www.oecd.org/en/publications/competition-in-artificial-intelligence-infrastructure_623d1874-en/full-report/component-5.html?utm_source=chatgpt.com "AI 供应链概览：人工智能基础设施中的竞争 | OECD"
[2]: https://www.amd.com/content/dam/amd/en/documents/partner-hub/instinct/instinct-over-nvidia.pdf?utm_source=chatgpt.com "数据中心解决方案 | AMD INSTINCT™ GPU 对比 NVIDIA® GPU"
[3]: https://arxiv.org/abs/2505.16968?utm_source=chatgpt.com "CASS：利用数据、模型和基准进行 NVIDIA 到 AMD 的转译"
[4]: https://aimultiple.com/cuda-vs-rocm?utm_source=chatgpt.com "AI 的 GPU 软件：2026 年的 CUDA 与 ROCm"
[5]: https://www.reuters.com/business/amd-expected-launch-next-generation-ai-infrastructure-challenge-nvidia-2026-07-23/?utm_source=chatgpt.com "AMD 称其最新 AI 服务器已全面投产，将在数月内发货"
[6]: https://www.statista.com/statistics/1622582/data-center-ai-gpu-market-share/?utm_source=chatgpt.com "NVIDIA 与 AMD 数据中心 AI GPU 市场份额 2025 | Statista"