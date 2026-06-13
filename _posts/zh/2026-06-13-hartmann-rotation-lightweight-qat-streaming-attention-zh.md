---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 哈特曼旋转，轻量级QAT，流式注意力
translated: true
type: note
---

**问题：** 注意力机制中 Q/K 的哈达玛旋转（Hadamard Rotation）、用于精度恢复的轻量级 QAT，以及带有位置衰减和令牌丢弃的流式注意力——它们是什么，又是如何工作的？

**答案：**

这三种技术来自一个中国大语言模型团队（很可能是腾讯的**混元**模型系列，因为提到了“Huyan 模型系列”、128K 上下文以及 GitHub 上的“Slim”项目）。下面我将从基本原理出发逐一解释。

---

## 1. Q 和 K 的哈达玛旋转（即所谓的“Hartmann Rotation”）

这几乎可以肯定是**哈达玛旋转**（原文可能误译或拼写错误）。它用于解决大语言模型量化中的**异常通道问题**。

### 问题：异常通道

在 Transformer 的隐藏状态和 Q/K 投影中，一小部分通道承载着不成比例的大幅度值。根据经验（来自 LLM.int8()、SmoothQuant 等论文），大约 0.1% 的通道的值可能比其他通道大 100 倍。

当你将其量化为 INT8/INT4 时：

```
quantized = round(x / scale)   其中 scale = max(|x|) / 127
```

如果一个通道的值为 200，而其他所有通道的值大约为 1，那么你的 scale = 200/127 ≈ 1.57，所有小的值都会坍缩为 ±1——这会导致巨大的精度损失。

### 解决方法：哈达玛旋转

**哈达玛矩阵** H 是一个正交矩阵，其中每个元素都是 ±1/√n。关键性质：

```
H @ H.T = I   （正交，保持 L2 范数）
```

在量化之前旋转 Q 和 K：

```python
import torch

def hadamard_matrix(n):
    # n 必须是 2 的幂
    if n == 1:
        return torch.tensor([[1.0]])
    H_half = hadamard_matrix(n // 2)
    return torch.cat([
        torch.cat([H_half,  H_half], dim=1),
        torch.cat([H_half, -H_half], dim=1)
    ], dim=0) / (2 ** 0.5)

def rotate_for_quantization(Q, K):
    d = Q.shape[-1]
    H = hadamard_matrix(d).to(Q.device)
    # 旋转：将能量均匀分布到所有通道
    Q_rot = Q @ H.T
    K_rot = K @ H.T
    return Q_rot, K_rot
```

由于 H 是正交的，`Q_rot @ K_rot.T == Q @ K.T` —— **注意力分数保持不变**。但此时能量被均匀分布到所有 d 个通道上，因此没有单个通道占据主导地位，量化尺度能够高效地覆盖所有通道。

这是 **QuaRot**（ETH Zurich, 2024）和 **SpinQuant**（Meta, 2024）的核心思想。

---

## 2. 用于最终精度恢复的轻量级 QAT

### 标准 PTQ 与 QAT 对比

**训练后量化（PTQ）**：在训练完成后，使用少量数据集校准量化尺度。速度快，但在低位宽（W4A8、W4A4）下会有精度损失。

**完整 QAT**：在整个训练过程中模拟量化。精度高，但成本与重新训练相当。

**轻量级 QAT**（他们采用的方法）：在 PTQ 之后进行一个短期的微调过程，在前向传播中模拟量化噪声。

### 直通估计器如何实现这一点

量化是不可微的（取整函数处处梯度为零）。诀窍在于**直通估计器（STE）**：

```python
class FakeQuantize(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, scale, zero_point, bits):
        # 在前向传播中模拟量化
        x_int = torch.round(x / scale) + zero_point
        x_int = torch.clamp(x_int, 0, 2**bits - 1)
        x_dequant = (x_int - zero_point) * scale
        return x_dequant

    @staticmethod
    def backward(ctx, grad_output):
        # STE：直接传递梯度，仿佛没有量化
        return grad_output, None, None, None
```

在轻量级 QAT 过程中：
- 权重在内存中保持全精度
- 前向传播使用伪量化后的权重（模拟 INT4 噪声）
- 反向传播使用 STE 同时更新尺度和权重
- 只运行原始训练步数的约 1-5%

量化**尺度成为可学习参数**，因此模型会调整其权重分布，使其更有利于量化。结果是：以原始训练成本的极小一部分，实现近乎无损的 W4A8 精度。

---

## 3. 带有位置衰减和令牌丢弃的流式注意力

### 二次复杂度问题

标准注意力的复杂度是 O(n²)，其中 n 是序列长度。在 128K 令牌时：

```
128000² = 164 亿个注意力分数对
```

即使使用 FlashAttention，TTFT（首令牌生成时间）仍然非常严重。因此需要稀疏注意力。

### 标准稀疏注意力的失败模式

简单的令牌丢弃（跳过计算某些 KV 对）会导致**误差累积**：如果位置 i 的令牌被丢弃，那么依赖于 i 的位置 i+1 的令牌会携带一个损坏的状态，并且这种损坏会随着序列不断累积。

### 他们的位置衰减解决方案

关键洞察是：**早期令牌（“汇聚”令牌）总是至关重要的**——这是 StreamingLLM（MIT/Meta, 2023）已经确立的结论，他们发现注意力总是将注意力集中在最初几个令牌上。

他们的设计：

```
序列：[HEAD 令牌：0..K] [TAIL 令牌：K+1..N]

HEAD：完整因果注意力（倒三角掩码——标准方式）
TAIL：位置衰减注意力——每个令牌只能关注
      一个 LOCAL WINDOW + HEAD 令牌
```

可视化形式：

```
令牌位置 →
         0  1  2  ... K  K+1  K+2  ...  N
HEAD:    ▓  ▓  ▓  ... ▓
TAIL:    ▓  ▓  ▓  ... ▓  [w]
TAIL:    ▓  ▓  ▓  ... ▓   ▓   [w]
TAIL:    ▓  ▓  ▓  ... ▓   ▓    ▓   [w]

▓ = 始终关注（汇聚 + HEAD）
[w] = 仅限局部窗口
```

“位置衰减因子”在数学上意味着从位置 i 关注位置 j 的注意力对数会乘上一个衰减项：

```python
def position_decay_mask(seq_len, head_size, window_size):
    mask = torch.full((seq_len, seq_len), float('-inf'))

    # HEAD 令牌：完整因果注意力
    mask[:head_size, :head_size] = 0.0

    # TAIL 令牌：关注 HEAD + 局部窗口
    for i in range(head_size, seq_len):
        mask[i, :head_size] = 0.0              # 始终能看到 HEAD
        mask[i, max(head_size, i-window_size):i+1] = 0.0  # 局部窗口

    return mask
```

这样复杂度变为 **O(n × (K + w))** 而非 O(n²)，其中 K = HEAD 大小，w = 窗口大小。

### 输出感知的令牌丢弃

“输出感知”部分意味着他们还会根据令牌对**输出的贡献**，选择性地丢弃 KV 缓存中的令牌——类似于 H2O（Heavy Hitter Oracle）或 SnapKV。那些在跨头累积注意力权重较低的令牌会被逐出缓存，因为它们在未来的输出中贡献很小。

---

## 总结表格

| 技术 | 解决的问题 | 核心思想 | 复杂度 |
|---|---|---|---|
| 哈达玛旋转 | 异常通道破坏量化 | 正交旋转均匀分布能量 | 通过快速哈达玛变换达到 O(d log d) |
| 轻量级 QAT | PTQ 残留精度损失 | STE + 可学习尺度进行短期微调 | 约为完整训练成本的 1-5% |
| 流式注意力 | 128K 上下文下的 O(n²) | 汇聚令牌 + 局部窗口 + 衰减掩码 | O(n(K+w)) |

这三种都是实用的推理时优化技术，旨在高效部署大型模型——它们并非研究上的新颖点，而是生产级大语言模型服务的工程解决方案。

**参考文献：**

- [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](https://arxiv.org/abs/2404.00456)
- [SpinQuant: LLM quantization with learned rotations](https://arxiv.org/abs/2405.16406)
- [StreamingLLM: Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453)
- [H2O: Heavy-Hitter Oracle for Efficient Generative Inference](https://arxiv.org/abs/2306.14048)
- [SmoothQuant: Accurate and Efficient Post-Training Quantization](https://arxiv.org/abs/2211.10438)