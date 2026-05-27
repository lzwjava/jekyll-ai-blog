---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanoGPT架构逐步详解
translated: true
type: note
---

**问题：** nanoGPT 是如何工作的？请逐步讲解完整架构：GPT Block、因果自注意力、MLP，以及这些层如何堆叠成神经网络。

**回答：**

让我从基本原理开始，逐层构建，然后以可视化方式展示完整架构。我将全程使用 Karpathy 的 nanoGPT 作为参考实现——它是最简洁的 GPT 实现。

---

## 宏观概览

GPT 本质上只是一个 **函数**：输入 token → 输出 logits。其他一切都是为了让这个函数更好地学习而做的工程。

```
输入 ids [B, T]
    → token 嵌入 + 位置嵌入 [B, T, C]
    → N × TransformerBlock [B, T, C]
    → LayerNorm
    → 线性投影 [B, T, vocab_size]
    → logits
```

其中 `B`=批大小，`T`=序列长度，`C`=嵌入维度（n_embd）。

---

## 1. Token + 位置嵌入

```python
self.transformer = nn.ModuleDict(dict(
    wte = nn.Embedding(vocab_size, n_embd),   # token 嵌入
    wpe = nn.Embedding(block_size, n_embd),   # 位置嵌入
    drop = nn.Dropout(dropout),
    h = nn.ModuleList([Block(config) for _ in range(n_layer)]),
    ln_f = nn.LayerNorm(n_embd),
))
```

前向传播：
```python
tok_emb = self.transformer.wte(idx)           # [B, T, C]
pos_emb = self.transformer.wpe(pos)           # [1, T, C]
x = self.transformer.drop(tok_emb + pos_emb) # [B, T, C]
```

这里没有正弦波之类的花哨操作——只是对 token 身份和位置分别使用可学习的查找表。直接将两者相加。

---

## 2. Block（TransformerBlock）

这是核心重复单元。nanoGPT 的 `Block`：

```python
class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))  # 注意力子层 + 残差连接
        x = x + self.mlp(self.ln_2(x))   # FFN 子层 + 残差连接
        return x
```

关键点：**Pre-LN**（LayerNorm 放在子层之前，而不是之后）。原始的 "Attention is All You Need" 使用 Post-LN。Pre-LN 训练更稳定。`x + ...` 是 **残差连接**——梯度可以直接通过它流动，防止梯度在 N 层中消失。

---

## 3. 因果自注意力

这里是魔法发生的地方。

```python
class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        # 将 Q、K、V 投影合并到一个矩阵中以提高效率
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        # 输出投影
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        # 因果掩码
        self.register_buffer("bias", torch.tril(torch.ones(config.block_size, config.block_size))
                             .view(1, 1, config.block_size, config.block_size))

    def forward(self, x):
        B, T, C = x.size()
        head_size = C // self.n_head

        # 投影到 Q、K、V
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)  # 每个 [B, T, C]

        # 重塑为多头： [B, n_head, T, head_size]
        q = q.view(B, T, self.n_head, head_size).transpose(1, 2)
        k = k.view(B, T, self.n_head, head_size).transpose(1, 2)
        v = v.view(B, T, self.n_head, head_size).transpose(1, 2)

        # 注意力分数： (B, nh, T, hs) × (B, nh, hs, T) → (B, nh, T, T)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(head_size))

        # 因果掩码：未来 token → -inf → softmax → 0
        att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)

        # 加权求和 value
        y = att @ v  # [B, nh, T, hs]

        # 重新组合多头
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.resid_dropout(self.c_proj(y))
```

数学公式：
```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

- `QKᵀ / √d_k` → [T, T] 分数矩阵：位置 i 对位置 j 的关注程度？
- `masked_fill(..., -inf)` → 强制上三角在 softmax 后变为 0 = **因果**（不能窥视未来）
- `softmax` → 将分数转换为概率（每行和为 1）
- `@ V` → value 向量的加权求和

每个头在 `C/n_head` 维度上独立操作，学习不同的注意力模式。多头 = 并行运行 N 次，然后拼接。

---

## 4. MLP（FFN）

```python
class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)
        self.gelu   = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        x = self.c_fc(x)    # [B, T, 4C]
        x = self.gelu(x)    # 非线性变换
        x = self.c_proj(x)  # [B, T, C]
        x = self.dropout(x)
        return x
```

先扩展 4 倍，应用 GELU，再投影回去。这是模型在注意力跨位置混合信息后，进行 **每个 token 独立计算** 的地方。注意力 = 通信。MLP = 计算。这就是思维模型。

GELU 与 ReLU：GELU 在 0 处平滑，有助于梯度流动。定义为 `x · Φ(x)`，其中 Φ 是高斯累积分布函数。

---

## 5. 输出头

```python
self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
```

关键地，**权重共享**：
```python
self.transformer.wte.weight = self.lm_head.weight
```

嵌入矩阵和最终投影共享权重。这在 GPT-2 中节省约 5000 万参数，并且在语义上合理：相同的向量空间用于编码输入 token 和解码输出 logits。

---

## 完整前向传播

```python
def forward(self, idx, targets=None):
    B, T = idx.size()
    pos = torch.arange(0, T, dtype=torch.long, device=idx.device)

    # 嵌入
    tok_emb = self.transformer.wte(idx)
    pos_emb = self.transformer.wpe(pos)
    x = self.transformer.drop(tok_emb + pos_emb)

    # N 个 transformer block
    for block in self.transformer.h:
        x = block(x)

    # 最终 LayerNorm
    x = self.transformer.ln_f(x)

    # 投影到词汇表
    if targets is not None:
        logits = self.lm_head(x)  # [B, T, vocab_size]
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
    else:
        logits = self.lm_head(x[:, [-1], :])  # 推理时：仅最后一个 token
        loss = None

    return logits, loss
```

推理时，你只需要对最后一个 token 的隐藏状态运行 `lm_head`——这就是下一个 token 的预测。

---

现在让我可视化整个堆栈：点击任意组件可深入了解。

---

## 参数数量（GPT-2 small：124M）

| 组件 | 参数 |
|---|---|
| `wte`（token 嵌入） | `vocab_size × C = 50257 × 768 ≈ 38.6M` |
| `wpe`（位置嵌入） | `1024 × 768 ≈ 0.8M` |
| 每个 Block：attn `c_attn` | `C × 3C = 768 × 2304 ≈ 1.77M` |
| 每个 Block：attn `c_proj` | `C × C ≈ 0.59M` |
| 每个 Block：MLP `c_fc` | `C × 4C ≈ 2.36M` |
| 每个 Block：MLP `c_proj` | `4C × C ≈ 2.36M` |
| 12 个 block 总共 | `≈ 85M` |
| `lm_head` | 与 `wte` 共享，+0 |

权重共享节省约 38.6M 参数。

---

## 残差流思维模型

将 `x` 想象成一条 **残差流**，流经整个网络。每个 block 从中读取信息，并写回增量更新：

```
x₀ = embed(tokens)
x₁ = x₀ + attn₁(ln(x₀))
x₂ = x₁ + mlp₁(ln(x₁))
x₃ = x₂ + attn₂(ln(x₂))
...
xₙ = logits
```

没有任何信息被破坏——信息在不断累积。这就是残差网络训练效果远好于普通深层网络的原因：梯度可以直接从损失流回嵌入层，无需经过乘法链。

---

## 一句话总结

Karpathy 对 transformer 最精辟的洞察：**“注意力是通信，MLP 是计算。”** 注意力让 token 从序列中的其他位置收集信息。MLP 则逐个 token 独立处理收集到的信息。将这些重复堆叠 N 次，就能得到一个模型，它能随着层数增加，逐步构建越来越抽象的表示。

参考文献：
- [nanoGPT 源码 — Karpathy](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)