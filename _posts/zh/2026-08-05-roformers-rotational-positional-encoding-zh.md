---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RoFormer的旋转位置编码
translated: true
type: note
---

## 核心思想

标准位置编码是加性的：`x_i + p_i`。RoPE 是乘性的：将 query/key 向量旋转一个与位置成比例的角度。旋转天然地免费带来了相对位置信息，因为两个旋转后向量的点积只取决于它们旋转角度的*差*。

## 二维情形（这就是全部技巧）

取一对维度，将其视为复数。对于位置 `m`，旋转 `mθ`：

```
f(x, m) = x * e^(imθ)   # 复数乘法 = 二维旋转
```

那么对于位置 `m` 的 query、位置 `n` 的 key：

```
<f(q,m), f(k,n)> = Re[q * conj(k) * e^(i(m-n)θ)]
```

结果只依赖于 `m - n`，即**相对位置从绝对旋转中涌现**。这就是第 3.4.1 节的完整推导——只是一个代数练习，没有更深的东西。

## 推广到 d 维

将 `d` 拆成 `d/2` 对，每对有自己的频率：

```
θ_i = 10000^(-2(i-1)/d),  i = 1..d/2
```

与正弦位置编码（Vaswani）使用相同的频率调度，但你不是将 `sin/cos` 向量加到 `x` 上，而是对 `x` 做块对角旋转：

```
R_Θ,m = blockdiag(R(mθ_1), R(mθ_2), ..., R(mθ_{d/2}))
q_m = R_Θ,m @ (W_q x_m)
k_n = R_Θ,n @ (W_k x_n)
```

注意力分数 `q_m^T k_n = x_m^T W_q^T R_Θ,(n-m) W_k x_n` —— 纯粹是 `n-m` 的函数。

## 最小实现（这就是每个现代 LLM 中实际使用的：LLaMA、GPT-NeoX、Qwen 等）

```python
import torch

def rope_freqs(dim, seq_len, base=10000.0, device="cpu"):
    theta = 1.0 / (base ** (torch.arange(0, dim, 2, device=device).float() / dim))
    pos = torch.arange(seq_len, device=device).float()
    freqs = torch.outer(pos, theta)  # [seq_len, dim/2]
    return torch.cos(freqs), torch.sin(freqs)

def apply_rope(x, cos, sin):
    # x: [batch, heads, seq, dim]
    x1, x2 = x[..., ::2], x[..., 1::2]
    cos = cos[None, None, :, :]
    sin = sin[None, None, :, :]
    rotated = torch.stack([x1 * cos - x2 * sin,
                            x1 * sin + x2 * cos], dim=-1)
    return rotated.flatten(-2)

# 用法
dim, seq_len = 64, 128
cos, sin = rope_freqs(dim, seq_len)
q = torch.randn(1, 8, seq_len, dim)
k = torch.randn(1, 8, seq_len, dim)
q_rot = apply_rope(q, cos, sin)
k_rot = apply_rope(k, cos, sin)
scores = q_rot @ k_rot.transpose(-2, -1)  # 相对位置感知的注意力
```

这就是论文中的公式 34（稀疏/高效实现）——无需物化完整的块对角旋转矩阵，只需在维度对上进行逐元素乘加交换。

## 为什么它能立足（特性，第 3.3 节）

- **长期衰减**：`θ_i = 10000^(-2i/d)` 使得高频维度对的点积贡献随 `|m-n|` 增大而衰减——与相距较远的 token 应减少关注的直觉一致（论文图 2，经验验证而非严格证明）。
- **序列长度灵活**：没有可学习的位置表，因为是 `m` 的纯函数，可在任意长度下工作。这才是它胜出的真正原因——外推/插值（后续工作：NTK-aware scaling、YaRN、线性缩放）都建立在此之上，因为 RoPE 有一个可重新缩放的闭式角度。
- **可与线性注意力组合**：由于旋转保持范数不变，你可以直接旋转 `ϕ(q)`/`φ(k)` 的输出（公式 19）——这就是 Performer+RoPE 有效的原因。
- 无额外参数，除旋转外无额外计算开销。

## 它的不足（论文自述的局限部分）

对于*为什么*它在长文本上收敛更快或泛化更好，没有理论解释——只有经验结果（BLEU +0.2、BERT MLM 收敛更快、长文本 CAIL2019-SCM 的提升）。数学只证明了*机制*（旋转 → 相对位置），而非*训练动力学*上的收益。

## 后续发展（你可能会比原论文更需要这些）

- **NTK-aware / YaRN scaling** —— 通过重新缩放 `θ_i` 来扩展上下文长度，而非重新训练。
- **ALiBi** —— 竞争方案，用加性偏置代替旋转，更简单但现已较少使用。
- 每个现代开源模型（LLaMA、Qwen、DeepSeek、Mistral）都默认使用 RoPE——值得检查它们的 `θ` base 值选择（LLaMA 使用 10000，一些长上下文模型将 base 推到 500k–1M 以实现外推）。

参考文献：

- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/pdf/2104.09864)
- [EleutherAI RoPE 博客（很好的可视化讲解）](https://blog.eleuther.ai/rotary-embeddings/)
