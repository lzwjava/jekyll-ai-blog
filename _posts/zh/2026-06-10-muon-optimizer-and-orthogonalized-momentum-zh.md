---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缪子优化器与正交化动量
translated: true
type: note
---

**问题：** 什么是 Muon 优化器？为什么 nanochat 对权重矩阵使用它（配合 Newton-Schulz 迭代）而不是 AdamW？

**答案：**

## 一句话概括

Muon（**M**oment**U**m **O**rthogonalized by **N**ewton-Schulz，由 Keller Jordan 于 2024 年底提出）对二维权重矩阵执行标准的 SGD 动量更新，然后对其进行**正交化**（将更新矩阵替换为最近似的半正交矩阵），最后应用该更新。仅适用于隐藏层的权重矩阵——嵌入层、`lm_head`、归一化层和偏置仍使用 AdamW，这正是 nanochat 的 `setup_optimizers` 中所做的拆分。

## 为什么要正交化更新？

考虑动量平滑后的梯度 `G ∈ R^{m×n}` 及其 SVD：

```
G = U S Vᵀ
```

实验表明，Transformer 权重的 `G` 具有非常明显的**低秩性**：少数几个大奇异值占主导。因此普通的 SGD/Adam 更新会持续沿着相同的少数方向推动权重，而“稀有”方向几乎不动。正交化将 `G` 替换为

```
O = U Vᵀ        （即所有奇异值设为 1）
```

使得更新中每个方向都具有相同的大小。从几何上看，`UVᵀ` 是以下问题的解：

```
O = argmin ‖O - G‖_F   s.t.  OᵀO = I
```

理论上，这是**在谱范数下的最速下降**，而非 Frobenius/欧几里得范数——对于作为线性映射的矩阵，谱范数是更合适的几何度量，因为它控制了层对激活值的拉伸程度。这与 Shampoo 一脉相承：Muon 的更新正是从 Shampoo 的预条件器 `(GGᵀ)^{-1/4} G (GᵀG)^{-1/4}` 在无累积极限下得到的，恰好等于 `UVᵀ`。

## Newton-Schulz：无需 SVD 的正交化

每一步对每个权重矩阵做 SVD 太慢。Newton-Schulz 是一种迭代多项式方法，仅通过矩阵乘法收敛到 `UVᵀ`，因此可在 GPU 上的 bfloat16 中运行。Muon/nanochat 中使用的五次迭代如下：

```python
def zeropower_via_newtonschulz5(G, steps=5):
    a, b, c = (3.4445, -4.7750, 2.0315)
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT                      # 在宽方向上操作
    X = X / (X.norm(dim=(-2, -1), keepdim=True) + 1e-7)  # 确保 ||X||_2 <= 1
    for _ in range(steps):
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X             # X <- aX + b(XXᵀ)X + c(XXᵀ)²X
    if G.size(-2) > G.size(-1):
        X = X.mT
    return X
```

原理：每次迭代对 `X` 的**奇异值**应用一个奇多项式 `p(x) = a·x + b·x³ + c·x⁵`（`U`、`V` 因子不受 `XXᵀ` 乘以 `X` 的多项式影响）。系数经过调整，使得 `p` 能积极地将 `(0, 1]` 映射到 `≈1`——经过 5 次迭代后，所有奇异值都被压缩到大约 `[0.7, 1.2]` 范围内。它不会精确收敛到 1，但这没关系：我们并不需要完全正交，只需要均衡方向即可。激进的系数以精度换取速度（更少的迭代次数），而 bf16 已经足够，因为该迭代是自校正的。

开销：5 次迭代 × 对 `m×n` 矩阵进行少量矩阵乘法 ≈ **相比 AdamW 的墙钟时间增加 <1%**（在 GPT-2 规模下）。

## 完整的 Muon 步骤

```python
class Muon(torch.optim.Optimizer):
    def __init__(self, params, lr=0.02, momentum=0.95, nesterov=True, ns_steps=5):
        super().__init__(params, dict(lr=lr, momentum=momentum,
                                      nesterov=nesterov, ns_steps=ns_steps))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            for p in group["params"]:
                g = p.grad
                state = self.state[p]
                if "buf" not in state:
                    state["buf"] = torch.zeros_like(g)
                buf = state["buf"]
                buf.lerp_(g, 1 - group["momentum"])          # 动量 EMA
                g = g.lerp_(buf, group["momentum"]) if group["nesterov"] else buf
                g = zeropower_via_newtonschulz5(g, group["ns_steps"])
                # 形状感知缩放，使更新 RMS 在不同矩阵形状下保持一致
                scale = max(1, p.size(-2) / p.size(-1)) ** 0.5
                p.add_(g, alpha=-group["lr"] * scale)
```

关键细节：

1. **先动量，后正交化**——对动量缓冲区进行正交化效果远好于对正交化后的梯度施加动量。
2. **形状感知缩放** `sqrt(max(1, m/n))`——一个半正交的 `m×n` 更新具有 RMS `≈ 1/sqrt(max(m,n))`；该缩放可以归一化不同形状矩阵（注意力 vs MLP）的有效步长，因此同一个学习率即可适用于所有矩阵。这也是为什么 Muon 的学习率（~0.02）看起来比 AdamW 的（~3e-4）大得多——更新是单位谱范数，而不是原始梯度大小。
3. **仅针对二维隐藏层矩阵。** 嵌入层并不是真正的“线性映射”（它们是查找表——谱几何是错误的范数），`lm_head` 对其输出尺度敏感，而一维参数（归一化层/偏置）无法被正交化。因此 nanochat 中采用了 AdamW/Muon 的拆分。如果使用卷积滤波器，则将其展平为二维。

## 为什么收敛更快

- **NanoGPT 极速训练**：与调优后的 AdamW 相比，Muon 在达到相同验证损失时将 GPT-2（124M）的训练墙钟时间减少了约 35%，并且此后一直是所有极速训练记录的基石。
- **样本效率**：在小到中等规模下，计算效率约为 AdamW 的 2 倍；Moonshot 的 Moonlight 工作表明，在 3B/16B-MoE 规模下，通过添加权重衰减并将更新 RMS 与 Adam（约 0.2）匹配以融入现有学习率调度，该效果依然成立。
- **内存**：每个参数只维护一个动量缓冲区，而 Adam 需要两个（无二阶矩），因此对于所覆盖的矩阵，优化器状态减少了一半。

直觉原因：均衡奇异值意味着优化器会在 Adam 会“饿死”的方向上持续取得进展，而谱范数几何限制了单步更新能对层输入-输出映射造成的扭曲程度——因此可以获得更大的稳定步长。

## 具体对应到 nanochat

在 nanochat 中，你会看到完全相同的结构：`Muon` 用于 `transformer.h.*` 的矩阵参数（注意力 QKV/投影、MLP），`AdamW` 用于 `wte`、`lm_head` 以及标量/向量参数，并采用上述 NS5 迭代（通常通过 `torch.compile` 编译，并通过类 ZeRO 的切分 Muon 进行分布式训练，每个 rank 正交化一部分参数然后 all-gather）。

**参考文献：**

- [Muon: An optimizer for hidden layers in neural networks — Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [Muon is Scalable for LLM Training (Moonlight, arXiv:2502.16982)](https://arxiv.org/abs/2502.16982)
- [modded-nanogpt speedrun repo (Muon origin)](https://github.com/KellerJordan/modded-nanogpt)
- [nanochat](https://github.com/karpathy/nanochat)