---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Transformer MLP 中的稀疏 MoE
translated: true
type: note
---

以下是 `train.py` 中 MoE 代码的导览。核心思想：**一个 Mixtral/Switch 风格的稀疏 MoE，可替换每个 Transformer 块中的 MLP。**

## 1. 接入位置

在 `Block.__init__` 中（约第 354 行）：

```python
if config.use_moe:
    self.moe = MoE(config)
else:
    self.mlp = MLP(config)
```

因此注意力部分保持不变；每个块的前馈部分被替换为“N 个专家 + 一个路由”。`--moe` 参数开启此功能。相关参数（第 227–232 行，第 524–527 行）：

| 参数 | 含义 |
|---|---|
| `n_experts` | 每个块中专家 FFN 的数量 |
| `n_experts_active` | 每个 token 分配给 top-k 个专家 |
| `moe_expert_dim` | 专家隐藏层大小 = `moe_expert_dim * n_embd`（4 表示与密集 MLP 相同） |
| `moe_aux_loss_coef` | 负载均衡损失的权重 |

## 2. 一个专家 = 一个小型 MLP

`Expert`（第 290 行）本质上就是密集的 `MLP`，但具有可配置的隐藏层大小：

```python
x -> Linear(C -> dim*C) -> GELU -> Linear(dim*C -> C)
```

## 3. 路由与分发（`MoE.forward`，第 323 行）

假设形状为 `N = B*T` 个 token，`C = n_embd`，`E = n_experts`，`k = n_experts_active`：

```python
flat = x.view(-1, C)                          # (N, C) 展平 batch+time
router_logits = self.gate(flat)              # (N, E) 普通的 Linear，无偏置
topk_logits, topk_idx = torch.topk(router_logits, k, dim=-1)   # (N, k)
weights = F.softmax(topk_logits, dim=-1)     # (N, k) 仅在选中的 k 个上重新归一化
```

注意它**仅对 top-k 的 logits 进行 softmax**（Mixtral 行为），而不是对整个 E 路 softmax 后再 gather（GShard）。这就是为什么梯度只流向所选专家的路由权重。

然后分发循环（第 331–341 行）避免了密集的 `N x E` 矩阵乘法，而是按专家收集 token：

```python
flat_idx  = topk_idx.reshape(-1)                                  # (N*k,) 每个槽位想要哪个专家
flat_w    = weights.reshape(-1, 1)                                # (N*k, 1) 每个槽位的门控权重
token_idx = arange(N).repeat_interleave(k)                        # (N*k,) 每个槽位属于哪个 token
for e, expert in enumerate(self.experts):
    mask  = flat_idx == e                                         # 路由到专家 e 的槽位
    slot  = mask.nonzero(...)
    out   = expert(flat[token_idx[slot]])                         # 只对这些 token 运行专家
    y = y.index_add(0, token_idx[slot], out * flat_w[slot])       # 加权散射回原位
```

`token_idx` 是关键的映射：槽位 `s = token*k + j` 属于 token `token_idx[s]`，并且使用了该 token top-k 选择中的第 `j` 个。`index_add` 将 k 个贡献累加到每个 token 的输出行中。每个 token 都被处理——这里 **没有容量限制 / 丢弃 token**，这与完整的 Switch Transformer 不同。

## 4. 辅助负载均衡损失（第 343–349 行）

如果没有惩罚，路由会崩溃到少数几个专家上。Switch-Transformer 的损失为 `L_aux = E * Σᵢ fᵢ · Pᵢ`：

```python
router_probs = F.softmax(router_logits, dim=-1)                        # 完整的 (N, E) softmax
gathered   = torch.gather(router_probs, 1, topk_idx)                   # (N, k) 选中专家的概率
one_hot    = F.one_hot(flat_idx, E)                                    # (N*k, E)
density    = one_hot.mean(0)                                           # f_i: 指向专家 i 的槽位比例
mean_prob  = (one_hot * gathered.reshape(-1,1)).sum(0) / N             # P_i: 专家 i 的平均路由概率
self.aux_loss = E * (density * mean_prob).sum()
```

- `f_i`（density）= 分配到专家 i 的 `N*k` 个槽位的比例。
- `P_i`（mean_prob）= 专家 i 接收的平均路由概率质量。
- 当两者都均匀时（`f_i = 1/E`，得到 `E * Σ (1/E)(1/E) = 1/E`）和最小，当一个专家承担所有时最大。这促使路由均衡。它通过 `router_probs`/`gathered` 可微分，从而训练门控网络。

## 5. 重新连接回模型

`GPT.forward`（第 445–459 行）累加各块的辅助损失，并将其加到 LM 损失中：

```python
aux_loss = x.new_zeros(())
for block in ...:
    x = block(x)
    if block has moe: aux_loss += block.moe.aux_loss
...
loss = F.cross_entropy(logits, targets) + config.moe_aux_loss_coef * aux_loss
```

`get_aux_loss()`（第 422 行）只是分离并求和每个块的值用于日志记录——你会在第 845 行的日志中看到 `aux X.XXXX`。

## 6. 参数统计

`get_num_params_active()`（第 408 行）报告“激活”参数数量，用于 MFU/flops 估算：

```python
expert_params = sum(params of all experts)
frac_active = k / E
n -= expert_params * (1 - frac_active)
```

即总参数量仍然很大，但每个 token 只触及 `k/E` 的专家权重加上所有共享权重。模型构建时会打印这两个总量。

## 如何整体理解

1. `Expert` = 可替换的 MLP。
2. `gate` = 线性路由，为每个 token 生成 E 个 logits。
3. top-k + softmax 为每个 token 选择并加权 k 个专家（Mixtral 路由）。
4. 按专家 gather → 专家 → 加权的 `index_add` scatter（稀疏计算，密集输出）。
5. 辅助损失防止路由崩溃。
6. `Block`/`GPT` 将辅助损失合并到总损失中，并暴露激活参数统计。

实验时需注意：
- 没有容量因子/丢弃，因此内存/吞吐量随路由偏斜程度变化（极不平衡的路由器仍然处理所有 token，只是每个专家不均匀）。
- `self.aux_loss = torch.zeros(())` 在 `__init__` 中位于 CPU/float32，但总是被 `forward` 覆盖，因此没问题；只有在任何前向之前调用 `get_aux_loss()` 才有影响。
- 辅助损失中的 `density` 基于槽位 (`N*k`) 计算，因此当 `k>1` 时，每个 token 每个选中的专家计数一次——这与此处基于槽位的 `P_i` 归一化一致，但在规模上与原始的 top-1 公式不同。
- `moe_expert_dim` 控制专家大小；当 `n_experts=k`（全部激活）时，MoE 退化为更宽的密集 MLP。

需要我添加一个可运行的小示例或形状追踪打印输出，以便你实时查看路由过程吗？