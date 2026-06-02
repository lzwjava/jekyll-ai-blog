---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 热辣MoE串类比
translated: true
type: note
---

**问题：** 用烤羊肉串的比喻解释 MoE（混合专家）结构——每根签子是一个专家，每块肉是一个 token/logit。这个简化的前向传播是否正确？

**回答：**

羊肉串的比喻很贴切。让我精确地扩展它，然后修正你的代码。

---

## 🍢 羊肉串 MoE 比喻

```
每根签子 = 一个专家的前馈网络          （例如总共64根签子）
每块肉   = 一个 token                  （序列中的一个位置）
烤串师傅 = 路由器                      （决定每块肉用哪些签子来烤）
TopK 选择 = 只有8根签子得到肉，56根闲置
```

一个 token（一块肉）被**路由到64根签子中的8根**。其他56个专家不激活——这就是 MoE 在推理时计算高效的原因。

---

## 你的代码——几乎正确，有一个 bug

```python
# Simplified MoE forward
router_logits = x @ router_weight.T        # [B*T, n_routed_experts]
topk_ids = router_logits.topk(k=8).indices # select 8 experts
output = sum(expert[i](x) for i in topk_ids)  # ❌ missing routing weights
```

**缺少的部分：路由权重（门控分数）。** 你在平等地求和专家输出——但每个专家应该**按其路由分数成比例地贡献**。第3根签子上的肉可能烤了60%，第7根只有40%——你需要用分数加权。

---

## 正确的前向传播

```python
import torch
import torch.nn.functional as F

# x: [B*T, d_model]  — 每行一个 token（一块肉）
router_logits = x @ router_weight.T          # [B*T, n_experts]  — 给每根签子打分
router_probs  = F.softmax(router_logits, -1) # 归一化分数

topk_vals, topk_ids = router_probs.topk(k=8, dim=-1)
# topk_vals:  [B*T, 8]  — 每个被选中的专家贡献多少
# topk_ids:   [B*T, 8]  — 哪8根签子得到了肉

# 在选中的8个中重新归一化（重要！）
topk_vals = topk_vals / topk_vals.sum(dim=-1, keepdim=True)  # [B*T, 8]

# 对被选中的专家进行加权求和
output = torch.zeros_like(x)
for k in range(8):
    expert_idx   = topk_ids[:, k]          # 每个 token 对应的专家编号
    expert_score = topk_vals[:, k]         # 对应权重   [B*T]

    # 每个 token 被发送到其分配的专家
    # （实际实现中，为效率考虑，会按专家对 token 进行批处理）
    for b in range(x.shape[0]):
        expert_out = experts[expert_idx[b]](x[b])          # 前馈网络前向
        output[b] += expert_score[b] * expert_out          # 加权相加
```

---

## 用签子术语描述的完整流程

```
Token（一块肉）
        │
        ▼
   路由器（师傅）
   给全部64根签子打分
        │
   softmax → 概率
        │
   topk(8) → 选出8根签子
        │
   ┌────┴────────────────────┐
   │  签子3  (w=0.35)        │  FFN_3(x) * 0.35
   │  签子17 (w=0.28)        │  FFN_17(x) * 0.28
   │  签子42 (w=0.15)        │  FFN_42(x) * 0.15
   │  ... 还有5根 ...        │
   └────────────────────────┘
        │
   加权求和 → 输出 token
```

56根签子 = **空闲、冷启动、零计算量**。这就是 MoE 的优势所在。

---

## DeepSeek-V3 / Qwen MoE 真实情况

| 项目 | 数值 |
|---|---|
| 专家总数 | 64–256 |
| 每个 token 激活的专家数 | 8（DeepSeek-V3 在256个中选8个） |
| 每个 token 激活的参数 | 约37B（总参数671B） |
| 路由器类型 | 线性层 + softmax（有时用 sigmoid） |
| 负载均衡损失 | 辅助损失，防止专家崩溃 |

**专家崩溃**是主要的训练风险——如果没有辅助损失，路由器会学会总是把肉发给相同的3根签子，其余61根挨饿。DeepSeek-V3 还在路由专家之上增加了**共享专家**（每块肉都会经过的签子，始终激活）。

---

## DeepSeek-V3 的精确公式

```
output = FFN_shared(x) + Σ_{i ∈ topk} g_i · FFN_i(x)

其中 g_i = softmax(router_logits)[i]  （仅在选中的k个中重新归一化）
```

你的直觉是对的——这是一个加权求和。你只是需要在其中加入 `g_i` 权重。
