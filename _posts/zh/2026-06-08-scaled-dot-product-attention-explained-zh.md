---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缩放点积注意力详解
translated: true
type: note
---

**问题：** 缩放点积注意力公式计算什么，为什么它采用这种结构？

**答案：**

这是**缩放点积注意力**的核心——计算每个 token“关注”其他 token 程度的第一步。

## 分解

```python
att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
```

### 第一部分：`q @ k.transpose(-2, -1)`——原始兼容性分数

- `q`：查询向量，形状 `(B, nh, T, d_k)`，其中 `B=batch, nh=num_heads, T=seq_len, d_k=head_dim`
- `k.transpose(-2, -1)`：键向量转置为 `(B, nh, d_k, T)`
- `@`（矩阵乘法）：产生 `(B, nh, T, T)`——一个方阵，其中 `[i, j]` = 查询位置 `i` 与键位置 `j` 的“匹配”程度

这是一个**相似度分数**。如果 `q[i]` 和 `k[j]` 方向一致，它们的点积很大；如果正交，则接近零。

### 第二部分：`* (1.0 / math.sqrt(k.size(-1)))`——缩放

为什么除以 `sqrt(d_k)`？

当 `d_k` 很大（比如 64）时，点积也会变得很大。大值会被推入 softmax 的平坦尾部区域，导致反向传播时梯度消失。

**经验效果：**
```
不缩放时 (d_k=64)：
  点积 ~ 范围 [-500, 500]
  softmax 接近 one-hot
  dL/dq ~ 梯度极小

缩放时 (除以 sqrt(64)=8)：
  点积 ~ 范围 [-7, 7]
  softmax 平滑
  dL/dq ~ 梯度健康
```

缩放因子 `1/sqrt(d_k)` 用于归一化方差。如果 `q` 和 `k` 初始化为均值 0、方差 1，那么它们的点积方差为 `d_k`。除以 `sqrt(d_k)` 使其方差恢复为 1——统计上稳定。

## 完整上下文（前向传播）

```python
def scaled_dot_product_attention(q, k, v, mask=None):
    # q, k, v: (B, nh, T, d_k)

    # 步骤 1：计算注意力分数
    scores = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))  # (B, nh, T, T)

    # 步骤 2：掩码（可选）——在因果注意力中将未来位置置零
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)

    # 步骤 3：Softmax 得到注意力权重
    weights = F.softmax(scores, dim=-1)  # (B, nh, T, T) —— 每行求和为 1

    # 步骤 4：将权重应用于值
    output = weights @ v  # (B, nh, T, d_k)

    return output
```

## 形状流

```
q: (4, 8, 100, 64)           batch=4, heads=8, seq_len=100, head_dim=64
k: (4, 8, 100, 64)
———————————————————
q @ k.T: (4, 8, 100, 100)    —— 每个查询与所有键比较
* scale: (4, 8, 100, 100)    —— 形状相同，仅缩放值
→ softmax: (4, 8, 100, 100)  —— 注意力权重，每行求和为 1
→ @ v: (4, 8, 100, 64)       —— 值的加权平均
```

**关键见解：** 注意力是一种可学习的、可微分的**路由机制**。在位置 `i`，softmax 权重告诉你要关注哪些位置。`1/sqrt(d_k)` 缩放使 softmax 保持在健康区间内。