---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FP8用于大语言模型训练与推理
translated: true
type: note
---

问题：为什么在LLM训练或推理中使用FP8？

答案：

**FP8（8位浮点数）**主要用于LLM中的**速度、内存节省和能源效率**，而不会显著牺牲模型质量。以下是详细解释：

---

### 1. 内存减少（与FP32相比2–4倍）

| 格式 | 位数 | 相对大小 |
|------|------|----------|
| FP32 | 32   | 4×       |
| BF16 / FP16 | 16 | 2×    |
| **FP8** | **8** | **1×** |

将精度从BF16降至FP8可减少权重、激活和KV-cache约50%的内存，从而在相同硬件上支持更大的模型或更大的批量。

### 2. 硬件吞吐量（FP16的2倍）

NVIDIA H100/H200和Blackwell GPU拥有专用的**FP8 Tensor Cores**，其提供的FLOPS约为FP16的**2倍**。NVIDIA的Transformer Engine会自动利用这一点。

### 3. 两种FP8变体用于不同角色

- **E4M3**（4位指数+3位尾数）——精度更高，用于**权重和激活**（前向传播）
- **E5M2**（5位指数+2位尾数）——动态范围更大，用于**梯度**（反向传播）

### 4. 推理：KV-Cache和延迟

在推理过程中，仅对**KV-cache**进行FP8量化即可节省40-50%的内存，从而实现更长的上下文窗口或更多并发请求。由于Tensor Core操作更快，延迟也会降低。

### 5. 训练稳定性技术

FP8的有限范围需要谨慎处理：

- **每张量/每通道缩放**——每个张量都有自己的缩放因子
- **延迟缩放**——缩放因子定期更新，以避免溢出/下溢
- **主权重保留在BF16/FP32**——优化器状态保持较高精度；仅计算使用FP8

### 为什么不使用INT8？

INT8是定点数，在推理中表现良好，但**不适用于训练**（梯度需要浮点数语义）。FP8兼具两者优点：8位的紧凑性和浮点数的动态范围。

### 总结

| 优势        | 训练   | 推理     |
|-------------|--------|----------|
| 内存节省    | ✅ 激活/梯度 | ✅ 权重/KV-cache |
| 速度提升    | ✅ ~2倍矩阵乘法FLOPS | ✅ 低延迟 |
| 能源节省    | ✅     | ✅       |
| 风险        | 梯度下溢（通过缩放缓解） | 轻微精度损失（通过校准缓解） |

参考文献：

- [NVIDIA Transformer Engine – FP8 训练](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/index.html)
- [FP8 深度学习格式 (Micikevicius 等人, 2022)](https://arxiv.org/abs/2209.05433)
- [NVIDIA H100 Tensor Core GPU 架构白皮书](https://resources.nvidia.com/en-us-tensor-core/gtc22-whitepaper-hopper)
