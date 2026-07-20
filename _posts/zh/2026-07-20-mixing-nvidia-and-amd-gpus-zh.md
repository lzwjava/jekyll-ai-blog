---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 混合使用NVIDIA和AMD显卡
translated: true
type: note
---

问题：能否在同一台AI工作站中混用不同的NVIDIA GPU（RTX 4070 + RTX 3090），以及能否混用NVIDIA和AMD的GPU？

答案：

## 1. RTX 4070 + RTX 3090：可以，完全没问题

这是AI爱好者和研究人员非常常见的配置。

示例：

```
机器

CPU
 |
 +-- RTX 3090 24GB  (cuda:0)
 |
 +-- RTX 4070 12GB  (cuda:1)
```

PyTorch识别情况：

```python
import torch

print(torch.cuda.device_count())

# 2

for i in range(2):
    print(torch.cuda.get_device_name(i))
```

输出：

```
0 NVIDIA GeForce RTX 3090
1 NVIDIA GeForce RTX 4070
```

CUDA不要求GPU型号完全一致。

---

## 但存在权衡

### 使用DDP进行训练

示例：

```
batch
 |
 +----------+
 |          |
3090       4070

24GB       12GB
```

问题：

较小显存的GPU会限制批次大小。

如果您的模型需要：

```
GPU0: 20GB
GPU1: 20GB
```

那么：

```
3090: 正常
4070: 显存不足
```

解决方案：

使用：

* 非均匀批次分配
* 模型并行
* ZeRO
* FSDP

或简单方案：

```
3090 -> 训练
4070 -> 推理 / 实验
```

这通常是最实用的设置。

---

## 对于大语言模型工作，RTX3090 + RTX4070 实际上优于 2×4070

因为：

RTX3090：

```
24GB 显存
384-bit 显存位宽
936 GB/s 带宽
```

RTX4070：

```
12GB 显存
192-bit 显存位宽
504 GB/s 带宽
```

对于大语言模型：

显存容量是关键。

示例：

一个13B模型：

```
FP16：
13B × 2字节 ≈ 26GB
```

3090：

```
24GB
通过量化基本可容纳
```

4070：

```
12GB
需要更多压缩
```

---

# 2. NVIDIA + AMD GPU 混用？

示例：

```
RTX3090
+
AMD MI50 / Radeon Pro VII
```

物理层面：

可以。

软件层面：

困难得多。

---

## CUDA生态

大多数AI框架：

```
PyTorch
 |
CUDA
 |
NVIDIA GPU
```

NVIDIA路径：

```
PyTorch
 |
CUDA
 |
RTX3090
```

运行完美。

---

AMD路径：

```
PyTorch
 |
ROCm
 |
AMD GPU
```

是一个独立的生态。

通常无法做到：

```
单个PyTorch进程

cuda:0 RTX3090
+
rocm:0 AMD MI50
```

它们是不同的后端。

---

## 可以分别运行两者

示例：

```
机器：

RTX3090
 |
CUDA
 |
vLLM 服务


AMD MI50
 |
ROCm
 |
PyTorch 实验
```

Linux可以处理这种情况。

只需要分别运行不同进程即可。

---

## 为什么NVIDIA + AMD混用不常见

问题不在硬件。

问题在于软件栈。

NVIDIA：

```
CUDA
cuDNN
TensorRT
FlashAttention
xFormers
vLLM
DeepSpeed
```

AMD：

```
ROCm
MIOpen
HIP
```

许多前沿AI库都优先优化NVIDIA。

---

## 例外：如果您喜欢底层实验

对于像您这样喜欢以下内容的人：

* 从头训练GPT-2
* nanoGPT
* GPU基础设施
* ROCm探索

AMD显卡颇具趣味。

示例：

```
RTX3090：
主要大语言模型工作


AMD MI50：
学习ROCm
内核实验
低成本算力
```

这实际上是个有趣的实验室。

---

## 我对AI工作站的推荐排名

### 最佳实用方案

```
RTX3090 24GB
+
RTX4070 12GB
```

⭐⭐⭐⭐⭐

---

### 同样优秀

```
2 × RTX3090
```

⭐⭐⭐⭐⭐

（但功耗/散热问题）

---

### 可行方案

```
2 × RTX4070
```

⭐⭐⭐⭐

（算力不错，显存受限）

---

### 实验方案

```
RTX3090
+
AMD MI50
```

⭐⭐⭐

（学习价值高，便利性较低）

---

### 建议避免

```
RTX4070
+
AMD消费级GPU
```

除非您专门研究ROCm。

对于家中的小型"AI工厂"，我会先围绕**单一的NVIDIA生态**搭建。混用NVIDIA和AMD更像是运行一个小型研究实验室。
