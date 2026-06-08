---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GELU 防止 FFN 中的线性坍塌
translated: true
type: note
---

**问题：** 为什么 nanoGPT 的 FFN 层中需要 GELU？

**回答：**

如果没有 GELU（或任何非线性），你的两个线性变换会组合成一个单一的线性变换：

```python
x_out = W_proj(W_fc(x) + b_fc) + b_proj
      = (W_proj @ W_fc) @ x + ...
```

这仍然只是一个线性函数，所以整个 FFN 层退化为线性代数。你将失去所有模型容量——网络只能学习线性关系。**GELU 打破这种线性，使模型能够学习非线性模式。**

### 为什么用 GELU 而不是 ReLU？

GELU 定义为：

$$\text{GELU}(x) = x \cdot \Phi(x)$$

其中 $\Phi(x)$ 是标准正态分布的累积分布函数。实际中常用近似形式：

$$\text{GELU}(x) \approx 0.5 \cdot x \cdot (1 + \tanh(\sqrt{2/\pi}(x + 0.044715 \cdot x^3)))$$

关键点：**GELU 更平滑且处处可微**，而 ReLU 在零处有硬截止。这之所以重要，是因为：

1. **自适应门控效应**：GELU 根据输入在正态分布下的“典型程度”对输入加权。高幅度输入基本不变地通过；低幅度输入被抑制但不会归零。

2. **梯度流动**：平滑曲线意味着反向传播时梯度传播更好，尤其是在深层堆叠中。

3. **经验性能**：使用 GELU 训练的 Transformer 收敛更快，损失更低。这在 BERT 论文（Devlin 等人，2018）中得到了实验验证。

以下是代码中的比较：

```python
import torch
import torch.nn.functional as F

x = torch.linspace(-3, 3, 100)

relu = F.relu(x)
gelu = F.gelu(x)  # 使用近似
silu = F.silu(x)  # 也是平滑的，LLaMA 中使用

# GELU 在原点处严格更平滑
# ReLU 有尖锐拐角，导致梯度问题
```

### 特别是在 Transformer 的 FFN 中

FFN 的扩展（1600 → 6400 → 1600）创建了一个瓶颈，GELU 在此同时起到以下作用：

- **非线性门控**：决定哪些特征重要
- **自适应正则化**：抑制噪声而不丢失信息

没有它，4 倍扩展就被浪费了——你只是在乘以稠密矩阵，没有学习到的选择性。

**结论**：GELU 是使 FFN 真正学习的关键。它不是装饰性的。
