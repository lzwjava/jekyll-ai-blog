---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 nanoGPT 架构
translated: true
type: note
---

你问的问题正是理解 nanoGPT 内部工作原理的正确问题。这些组件以特定方式组合在一起，以预测序列中的下一个 token。让我带你了解架构以及它们如何连接。

## 完整图景：从文本到下一个 Token 预测

以下是所有你提到的组件如何组合成完整的 GPT 模型：

```
Input Tokens (IDs)
    ↓
Token Embeddings + Positional Embeddings
    ↓
[Transformer Block × n_layers]
    ├── LayerNorm
    ├── Multi-Head Self-Attention (K, Q, V)
    │   └── Causal Masking (look only at previous tokens)
    ├── Residual Connection (+)
    ├── LayerNorm
    ├── MLP/FeedForward (GELU activation)
    └── Residual Connection (+)
    ↓
Final LayerNorm
    ↓
Linear Layer (lm_head) → Logits for next token
```

## 组件分解

### 1. Embeddings：起点

模型使用 **两个 embedding tables**：
- **Token Embeddings** (`wte`)：将每个 token ID（0 到 vocab_size-1）映射到大小为 `n_embd` 的稠密向量
- **Positional Embeddings** (`wpe`)：将每个位置（0 到 block_size-1）映射到大小为 `n_embd` 的向量

这些向量 **逐元素相加**：`x = token_embeddings + positional_embeddings`。这为每个 token 提供了一个表示，既包含它是什么，也包含它在序列中的位置。

### 2. Self-Attention 中的 K, Q, V 机制

这是魔法发生的地方。在每个 attention head 中，输入 `x` 被投影到三个矩阵：

```python
key = nn.Linear(n_embd, head_size, bias=False)
query = nn.Linear(n_embd, head_size, bias=False)
value = nn.Linear(n_embd, head_size, bias=False)

k = key(x)    # (B, T, head_size)
q = query(x)  # (B, T, head_size)
v = value(x)  # (B, T, head_size)
```

注意力权重计算如下：
```python
wei = q @ k.transpose(-2, -1) / sqrt(head_size)  # Scaled dot-product
```

然后应用 **causal mask**，使用下三角矩阵防止查看未来 token：
```python
tril = torch.tril(torch.ones(T, T))
wei = wei.masked_fill(tril == 0, float('-inf'))
wei = F.softmax(wei, dim=-1)  # Normalize across rows
out = wei @ v  # Weighted aggregation
```

**multi-head** 版本并行运行多个 head，然后连接结果并投影回原维度。

### 3. MLP/FeedForward 层

这是一个简单但关键的两层网络，独立应用于每个 token：
```python
class FeedForward(nn.Module):
    def __init__(self, n_embd, dropout):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),  # Expand 4x
            nn.GELU(),                       # Non-linearity
            nn.Linear(4 * n_embd, n_embd),  # Project back
            nn.Dropout(dropout)
        )
```

隐藏维度通常是 **embedding 维度的 4 倍**（`4 * n_embd`）。

### 4. Transformer Block 结构

每个 block 遵循特定模式，并带有 residual connections：
```python
def forward(self, x):
    # Self-attention with pre-normalization
    x = x + self.attn(self.ln_1(x))
    # Feed-forward with pre-normalization
    x = x + self.mlp(self.ln_2(x))
    return x
```

## “下一个 Token” 预测的工作原理

这是许多人感到困惑的地方。关键洞察是 **模型在训练期间同时预测所有位置**。

### 训练期间：
给定输入序列 `[a, b, c]`，模型：
1. 并行处理所有 token
2. 由于 **causal masking**，位置 1 只看到 token 1，位置 2 看到 token 1-2，位置 3 看到 token 1-3
3. `lm_head`（一个 linear layer）应用于 **每个位置**，以预测该位置的下一个 token
4. 目标 `y` 是原序列右移一位：`[b, c, d]`
5. 损失在所有位置同时计算

这就是训练高效的原因——模型在一次前向传播中从每个位置学习，而不是逐个 token。

### 生成/推理期间：
生成新文本时，模型被反复调用：
```python
for _ in range(max_new_tokens):
    # Crop to last block_size tokens
    x_cond = x[:, -block_size:]
    # Forward pass to get logits
    logits = model(x_cond)
    # Take logits of the last position only
    logits_last = logits[:, -1, :]
    # Convert to probabilities, sample
    probs = F.softmax(logits_last, dim=-1)
    next_token = torch.multinomial(probs, num_samples=1)
    # Append to sequence
    x = torch.cat([x, next_token], dim=1)
```

**重要**：linear layer（`lm_head`）不“知道”上下文。先前 token 的所有上下文信息已在通过所有 transformer block 后编码到最后一个 token 的 embedding 中。

## 层的构建方式

层是分层构建的：

1. **底层**：单个组件（`CausalSelfAttention`、`MLP`、`LayerNorm`）
2. **中间层**：`Block` 结合 attention + MLP 并带 residual
3. **顶层**：`GPT` 类堆叠多个 `Block` 实例

模型配置控制一切：
```python
class GPTConfig:
    block_size = 1024    # Max sequence length
    vocab_size = 50257   # GPT-2 vocabulary size
    n_layer = 12         # Number of transformer blocks
    n_head = 12          # Number of attention heads
    n_embd = 768         # Embedding dimension
```

权重初始化仔细处理，使用 scaled initialization 以适应深层网络，并且 token embeddings 与输出投影（`lm_head`）绑定以提高参数效率。

这种架构虽然组件看似简单，却创造了 GPT 模型强大的自回归行为。
