---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MoE中无直接专家logits
translated: true
type: note
---

问题：**在混合专家（MoE）模型中，计算最终 logits 时，我们使用哪个专家的 logits？**

答案：**不使用任何专家的 logits 直接输出**。专家网络操作的是隐藏状态，其输出会**加权组合后，再由模型最终的 LM head 生成 logits**。

对于一个 token，其前向传播大致如下：

```text
x
│
├── Router(x) → scores
│              ↓
│         top-k 专家
│        /     |      \
│      E1      E3      E7
│       │       │       │
│       └───────┼───────┘
│          加权求和
│              ↓
│        MoE 输出
│              ↓
│       残差 + 归一化
│              ↓
│         隐藏状态 h
│              ↓
│       LM Head / 线性层
│              ↓
│          logits
│              ↓
│       softmax → P(token)
```

### 具体示例

假设路由器选择了 2 个专家：

```python
x = hidden_state

router_logits = router(x)              # [num_experts]
weights, expert_ids = topk(router_logits, k=2)

y1 = expert_3(x)
y2 = expert_7(x)

moe_output = (
    weights[0] * y1 +
    weights[1] * y2
)

h = residual + moe_output

logits = lm_head(norm(h))
```

所以 **Expert 3 不产生词表 logits**，Expert 7 也一样。

它们产生的是类似：

```text
Expert 3:
隐藏维度 = 4096
        ↓
      [4096]

Expert 7:
隐藏维度 = 4096
        ↓
      [4096]
```

加权组合后仍然是一个隐藏向量：

```text
0.7 * Expert3(x) + 0.3 * Expert7(x)
              ↓
           [4096]
```

然后共享的 LM head 将其映射到词表空间：

```text
[4096]
   ↓
Linear(4096 → 128k)
   ↓
[128000]   ← logits
```

### 为什么这很重要

MoE 层本质上可以表示为：

$$
y = \sum_{i \in TopK(x)} g_i(x) E_i(x)
$$

其中：

* \\(E_i(x)\\) = 专家 \\(i\\) 的输出
* \\(g_i(x)\\) = 路由器权重
* \\(TopK(x)\\) = 被选中的专家

随后：

$$
\text{logits} = W_{lm}h
$$

其中 \\(h\\) 是经过 MoE 层及后续 Transformer 层后的**组合后的隐藏状态**。

所以如果你有：

```text
8 个专家
top-k = 2
```

对于某个特定 token：

```text
Expert 1 ──┐
Expert 5 ──┤
            ↓
       加权求和
            ↓
        Transformer
            ↓
         LM head
            ↓
         logits
```

**你不是在选“Expert 1 的 logits”或“Expert 5 的 logits”。**

路由器选择的是**哪些专家贡献给隐藏表示**，而不是哪一个专家生成词表分布。

下一步可以做的有意义的事情是，梳理一下实际的 **DeepSeek/Qwen 风格 MoE PyTorch 代码**，包括确切的张量形状 `[batch, seq, hidden] → router → topk → expert output → logits`。
