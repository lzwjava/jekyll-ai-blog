---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GELU激活函数概述
translated: true
type: note
---

### 什么是GELU？

高斯误差线性单元（GELU）是一种用于神经网络中的平滑激活函数，尤其广泛应用于基于Transformer的模型（如BERT和GPT系列）。该函数由研究人员Dan Hendrycks和Kevin Gimpel于2016年提出，结合了线性变换的优势与受高斯（正态）分布启发的概率加权特性。与ReLU等简单激活函数（对负输入直接输出零）不同，GELU允许负值存在微小梯度流，通过缓解梯度消失问题并提升收敛性，从而在深度网络中实现更优性能。

#### 数学定义
GELU的核心公式为：

\\[
\text{GELU}(x) = x \cdot \Phi(x)
\\]

其中 \\(\Phi(x)\\) 是标准正态分布的累积分布函数：

\\[
\Phi(x) = \frac{1}{2} \left[ 1 + \erf\left( \frac{x}{\sqrt{2}} \right) \right]
\\]

此处 \\(\erf\\) 为误差函数，用于衡量高斯分布逼近阶跃函数的程度。这种设计使GELU具备概率特性：相较于ReLU，它对负输入的“抑制”更为温和，同时保留正输入的完整性。

为提升计算效率，常使用近似公式，例如基于sigmoid的版本：

\\[
\text{GELU}(x) \approx x \cdot \sigma(1.702x)
\\]

其中 \\(\sigma\\) 为sigmoid函数。

#### 为何使用GELU？
- **平滑性**：全程可微分，有助于优化过程
- **非单调性**：轻微抑制负值但不直接归零，保留信息完整性
- **实证优势**：在自然语言处理等任务中表现优于ReLU和ELU，大型模型中训练速度更快、精度更高
- **局限性**：因需计算erf或sigmoid函数，计算开销略高于ReLU

实际应用中，PyTorch和TensorFlow等框架已内置GELU实现（如`torch.nn.GELU()`）。

#### 参考文献
- [高斯误差线性单元（GELU）论文](https://arxiv.org/abs/1606.08415)
- [GELU激活函数详解](https://www.baeldung.com/cs/gelu-activation-function)
- [GELU激活机制解析](https://medium.com/@shauryagoel/gelu-gaussian-error-linear-unit-4ec59fb2e47c)
