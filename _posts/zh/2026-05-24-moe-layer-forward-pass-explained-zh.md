---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MoE层前向传播解释
translated: true
type: note
---

**问题：** 在 DeepSeek V3/V4 的 MoE 架构中，简化 MoE 前向传播每一步的 shape 是什么，以及它是如何工作的？

**答案：**

让我精确标注 shape 并解释完整画面。

## 设置/符号

```
B   = 批次大小
T   = 序列长度
d   = 模型隐藏维度（DeepSeek V3：7168）
n   = 总路由专家数（V3/V4 中为 256）
k   = 选择的 top-k 专家数（V3/V4 中为 8）
d_e = 专家中间维度（V3/V4 中为 2048，远小于密集 FFN）
```

---

## 标注了 Shape 的前向传播

```python
# x: [B*T, d]  — 展平的 token，每个是一个 d 维隐藏状态
# router_weight: [n, d]  即 [256, 7168]

router_logits = x @ router_weight.T
# x:             [B*T, d]
# router_weight.T: [d, n]
# result:        [B*T, n]  = [B*T, 256]
# 每行 = 一个 token 对所有 256 个专家的亲和力分数

topk_ids = router_logits.topk(k=8).indices
# shape: [B*T, 8]
# 每个 token 从 256 个专家中选择 8 个专家索引

topk_weights = router_logits.topk(k=8).values.softmax(-1)
# shape: [B*T, 8]  — 归一化的门控权重（每个 token 加起来为 1）

output = sum(expert[i](x) for i in topk_ids)
# 每个 expert[i](x): [B*T, d]  （仅对路由到它的 token 计算）
# 加权求和:         [B*T, d]
```

最终输出 shape：**`[B*T, d]`** — 与输入相同，就像普通的 FFN。

---

## 每个专家实际做什么

每个专家是一个小型 FFN（DeepSeek V3 中的 SwiGLU）：

```python
# 在 expert[i] 内部：
# gate_weight: [d_e, d]  = [2048, 7168]
# up_weight:   [d_e, d]
# down_weight: [d, d_e]  = [7168, 2048]

def expert_forward(x):  # x: [B*T, d]
    gate = x @ gate_weight.T   # [B*T, d_e]
    up   = x @ up_weight.T     # [B*T, d_e]
    act  = F.silu(gate) * up   # [B*T, d_e]  — SwiGLU
    out  = act @ down_weight.T # [B*T, d]
    return out
```

但实际上，只有 **一部分 token** 被发送到每个专家 — 这是分发/收集机制。

---

## 实际的分发（代码中实际发生的）

朴素的循环 `for i in topk_ids` 在实践中是错误的。实际实现：

```python
# [B*T, 8] → 展平以获得 (token_idx, expert_idx) 对
# 对于每个专家 e，只收集分配给它的 token

expert_outputs = torch.zeros(B*T, d)

for e in range(n_experts):  # 256 个专家
    # 哪些 token 路由到专家 e？
    mask = (topk_ids == e).any(dim=-1)         # [B*T] 布尔张量
    tokens_for_e = x[mask]                      # [n_e, d], n_e << B*T

    if tokens_for_e.shape[0] == 0:
        continue

    out_e = expert[e](tokens_for_e)             # [n_e, d]

    # 为每个路由的 token 获取此专家的权重
    weight_e = topk_weights[mask, (topk_ids[mask] == e).nonzero()...]
    expert_outputs[mask] += weight_e.unsqueeze(-1) * out_e

# final: [B*T, d]
```

在真实的 CUDA 内核（和 Triton）中，这是通过 **token 重排** 完成的 — token 按专家分配排序，每批处理一个专家，然后恢复原始顺序。

---

## DeepSeek V3 特有：共享专家 + 路由专家

V3 不仅有 256 个路由专家。它有 **1 个共享专家**（始终激活）+ **256 个路由专家**（选择 top-8）：

```
V3 MoE 层：
  shared_expert(x)           → [B*T, d]   始终激活
+ 前 8 个路由专家的和          → [B*T, d]
= 最终 FFN 输出               → [B*T, d]
```

路由器仅从 256 个 **路由** 专家中选择；共享专家绕过路由。

---

## 关键数字：V3 参数预算

| | 密集等效 | MoE V3 |
|---|---|---|
| FFN 隐藏维度 | ~18K（用于 671B 密集模型） | 每个专家 2048 |
| 每个 token 活跃的专家数 | 全部 | 8 + 1 共享 |
| 总专家参数 | — | 256 × 小型 FFN |
| 每个 token 活跃的参数 | ~671B | ~37B |

路由器矩阵本身很小：`256 × 7168 = 180 万参数` — 可以忽略不计。

---

## 负载均衡（V3 创新：无辅助损失）

V3 使用 **无辅助损失的负载均衡** — 每个专家在路由器 logits 上添加一个偏置项，动态更新以保持专家利用率均匀：

```python
router_logits_biased = router_logits + expert_bias  # [B*T, 256]
topk_ids = router_logits_biased.topk(8).indices     # 路由决策

# 但门控权重使用无偏 logits：
topk_weights = router_logits.gather(-1, topk_ids).softmax(-1)
```

这是 V3 相对于 V2 的关键技巧，V2 使用了显式的辅助损失项。

---

## 总结表格

| 张量 | Shape |
|---|---|
| `x`（输入） | `[B*T, d]` = `[B*T, 7168]` |
| `router_weight` | `[256, 7168]` |
| `router_logits` | `[B*T, 256]` |
| `topk_ids` | `[B*T, 8]` |
| `topk_weights` | `[B*T, 8]` |
| 每个专家输入 | `[n_e, 7168]` 其中 `n_e` ≪ `B*T` |
| 每个专家输出 | `[n_e, 7168]` |
| 最终输出 | `[B*T, 7168]` |

**参考文献：**

- [DeepSeek-V3 技术报告 (arXiv)](https://arxiv.org/abs/2412.19437)
- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3)
- [混合专家模型详解 — Hugging Face](https://huggingface.co/blog/moe)
