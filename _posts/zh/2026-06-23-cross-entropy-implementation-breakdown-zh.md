---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 交叉熵实现详解
translated: true
type: note
---

**问题：** `F.cross_entropy` 内部是如何实现的？请展示算法。

**答案：**

## `F.cross_entropy` — 从 PyTorch 源码到数学

### 一句话概括

```
F.cross_entropy(logits, targets) = NLL(log_softmax(logits), targets)
```

两步融合：**log_softmax** + **负对数似然**。

---

### 纯 Python 实现（与 PyTorch 所做完全一致）

```python
import torch

def cross_entropy_manual(logits, targets):
    """
    logits:  (B, C) 原始未归一化分数
    targets: (B,)   整数类别索引
    """
    B, C = logits.shape

    # 步骤1: log_softmax（通过 logsumexp 技巧保证数值稳定）
    # 减去最大值以增强稳定性——不改变 softmax 结果
    # 因为 exp(x_i - max) / Σ exp(x_j - max) = exp(x_i) / Σ exp(x_j)
    m = logits.max(dim=1, keepdim=True).values        # (B, 1)
    shifted = logits - m                               # (B, C)
    log_sum_exp = shifted.exp().sum(dim=1, keepdim=True).log()  # (B, 1)
    log_softmax = shifted - log_sum_exp                # (B, C)

    # 步骤2: NLL——选取正确类别的对数概率
    # 对于批次中的每个 i，取 log_softmax[i, targets[i]]
    nll = -log_softmax[torch.arange(B), targets]      # (B,)

    # 步骤3: 均值约减（默认）
    return nll.mean()


# --- 验证 ---
torch.manual_seed(0)
B, C = 4, 10
logits = torch.randn(B, C)
targets = torch.randint(0, C, (B,))

loss_manual = cross_entropy_manual(logits, targets)
loss_pytorch = torch.nn.functional.cross_entropy(logits, targets)

print(f"manual:  {loss_manual.item():.6f}")
print(f"pytorch: {loss_pytorch.item():.6f}")
# manual:  2.453069
# pytorch: 2.453069  ✓
```

---

### logsumexp 技巧——为什么重要

朴素的版本会在 logits 较大时**溢出**：

```python
# 错误——exp(1000) 在 float32 下等于 inf
softmax = logits.exp() / logits.exp().sum()
log_softmax = softmax.log()  # nan

# 正确——通过减去最大值进行平移，数学上等价
# log(exp(x_i) / Σ exp(x_j))
# = log(exp(x_i - m) / Σ exp(x_j - m))   [m 抵消]
# = (x_i - m) - log(Σ exp(x_j - m))
```

在 nanoGPT 的训练循环中，一个 760M 模型产生的 logits 可能很大——这个技巧使得你不会因 softmax 溢出而看到 NaN 的损失值。

---

### One-hot 标签情况（语言模型训练中总是遇到）

对于语言建模，`targets` 是每个位置上的单个整数（下一个 token）。NLL 步骤简化为：

```python
# 无需完整矩阵乘法，直接索引：
loss = -log_softmax[batch_idx, targets[batch_idx]]
```

整个 `(B, C)` 的 log_softmax 矩阵被计算出来，但只使用了其中的 `B` 个值。这就是为什么存在**融合内核**的主要原因——CUDA 可以避免实际分配完整的 softmax。

---

### C++/CUDA 中实际运行的内容

```
F.cross_entropy
  → torch._C._nn.cross_entropy_loss
    → at::nll_loss_nd (用于 targets)
    → at::log_softmax (CUDA 内核: "log_softmax_cuda_kernel")
```

CUDA 内核通过 warp 级别归约，**单次遍历** logit 向量完成 logsumexp——GPU 上不会分配中间 softmax 张量。这就是相比单独执行 `log(softmax(x))` 的真正加速所在。

---

### nanoGPT 中的使用上下文

```python
# 来自 nanoGPT/model.py — GPT.forward()
def forward(self, idx, targets=None):
    logits, _ = self.transformer(idx)          # (B, T, vocab_size)

    if targets is not None:
        # 展平 (B, T, V) → (B*T, V) 和 (B, T) → (B*T,)
        loss = F.cross_entropy(
            logits.view(-1, logits.size(-1)),  # (B*T, vocab_size)
            targets.view(-1),                  # (B*T,)
            ignore_index=-1                    # 掩码填充 token
        )
```

`ignore_index=-1` 意味着填充位置不参与损失计算——PyTorch 内部在求平均前将这些 NLL 值置零。

---

### 思维模型

```
logits (B, C)
    │
    ▼
[每行减去最大值]              ← 防止溢出
    │
    ▼
[exp → sum → log]             ← log(Σ exp(xⱼ - m))
    │
    ▼
log_softmax = x_i - m - log_sum_exp   ← 每个类别的对数概率
    │
    ▼
[按目标类别索引]              ← 选取 log p(y_true)
    │
    ▼
nll = -log_softmax[target]    ← 正确类别的惊讶度
    │
    ▼
loss = mean(nll)              ← 标量
```
