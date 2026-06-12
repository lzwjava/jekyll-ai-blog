---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 单一AdamW与MuonAdamW混合
translated: true
type: note
---

**问题：** 在 nanochat/nanoGPT 风格的优化器配置中，“Single AdamW”和“MuonAdamW（Muon 用于矩阵，AdamW 用于嵌入/标量）”是什么意思？

**回答：**

这个表格描述了两种优化器设置，第二种是 Karpathy 在 nanochat 和 modded-nanogpt speedrun 中使用的混合方案。

## AdamW（基线）

带解耦权重衰减的 Adam。通过运行矩估计实现每个参数的自适应学习率：

```python
m = beta1 * m + (1 - beta1) * g          # 一阶矩（动量）
v = beta2 * v + (1 - beta2) * g**2       # 二阶矩（每个参数的方差）
update = lr * m_hat / (v_hat.sqrt() + eps)
p -= update + lr * wd * p                # 解耦权重衰减
```

“Single AdamW” = 对模型中的每个参数使用同一个优化器。简单、稳健，每个参数需要 2 个额外状态张量（m, v）。

## Muon（通过 Newton-Schulz 正交化的动量）

Muon 仅对 **2D 权重矩阵**（注意力投影、MLP 权重）有意义。核心思想：对动量-SGD 更新进行 **正交化** 后再应用。如果动量缓冲区有 SVD `M = U S Vᵀ`，Muon 将其替换为 `U Vᵀ` —— 即所有奇异值都设为 1。

为什么？原始梯度更新通常由少数几个大的奇异方向主导，因此矩阵的大多数“方向”几乎得不到更新。正交化将更新能量均匀分布到所有方向 —— 权重矩阵的每个秩 1 分量都以相同速率移动。经验表明，在中小规模下，这比 AdamW 训练 Transformer 的算力效率高约 1.3–2 倍，Moonshot 也在大规模上验证了它（Kimi K2 使用 MuonClip 训练）。

直接计算 SVD 太慢，因此 Muon 通过在 bfloat16 中执行约 5 次五阶 **Newton–Schulz** 多项式来近似 `UVᵀ`：

```python
import torch

def zeropower_via_newtonschulz5(G, steps=5):
    # 近似计算 G = U S V^T 的 UV^T，即对 G 进行正交化
    a, b, c = (3.4445, -4.7750, 2.0315)
    X = G.bfloat16()
    if G.size(-2) > G.size(-1):
        X = X.mT
    X = X / (X.norm(dim=(-2, -1), keepdim=True) + 1e-7)  # 谱范数 <= 1
    for _ in range(steps):
        A = X @ X.mT
        B = b * A + c * A @ A
        X = a * X + B @ X        # 五阶：将奇异值推向 1
    if G.size(-2) > G.size(-1):
        X = X.mT
    return X

class Muon(torch.optim.Optimizer):
    def __init__(self, params, lr=0.02, momentum=0.95):
        super().__init__(params, dict(lr=lr, momentum=momentum))

    @torch.no_grad()
    def step(self):
        for group in self.param_groups:
            for p in group["params"]:
                g = p.grad
                state = self.state[p]
                if "buf" not in state:
                    state["buf"] = torch.zeros_like(g)
                buf = state["buf"]
                buf.mul_(group["momentum"]).add_(g)
                g = g.add(buf, alpha=group["momentum"])   # nesterov
                O = zeropower_via_newtonschulz5(g)
                # 缩放以使更新 RMS 与形状无关
                scale = max(1, p.size(-2) / p.size(-1)) ** 0.5
                p.add_(O, alpha=-group["lr"] * scale)
```

注意该多项式只需要矩阵乘法 —— 对 GPU 友好，且 FLOP 开销相对于反向传播很小。每个矩阵的状态只需要 1 个动量缓冲区（AdamW 需要 2 个），因此内存也更少。

## 为什么是混合方案（MuonAdamW）

正交化仅对作为线性映射的密集 2D 矩阵有意义。因此 nanochat 将参数分为：

```python
matrix_params = [p for p in model.parameters() if p.ndim == 2 and not is_embedding(p)]
other_params  = [p for p in model.parameters() if p not in matrix_params]
# 嵌入、lm_head、归一化/标量/偏置

opts = [
    Muon(matrix_params, lr=0.02, momentum=0.95),
    torch.optim.AdamW(other_params, lr=3e-4, betas=(0.9, 0.95)),
]
for opt in opts: opt.step()
```

嵌入得到稀疏的、按行更新的梯度（只有批次中的 token 会获得信号），因此对嵌入矩阵进行全局正交化是错误的操作 —— AdamW 的每个参数自适应能力能更好地处理这种情况。lm_head 同理，而 1D 参数（LayerNorm 增益、偏置）根本无法进行正交化。

因此，表格对比的是：平淡但安全的单优化器配置 vs. 经过 speedrun 验证的配置，其中大部分 FLOP（Transformer 的权重矩阵）使用 Muon，其他部分保持 AdamW。

如果你在 MI300X 上运行 nanochat，应使用混合方案 —— 它是默认选项，并且 Newton-Schulz 纯矩阵乘法，ROCm 可以很好地处理。

**参考文献：**

- [Muon: An optimizer for hidden layers in neural networks — Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [modded-nanogpt (Muon 诞生的 speedrun 仓库)](https://github.com/KellerJordan/modded-nanogpt)
- [Muon is Scalable for LLM Training (Moonlight, Moonshot AI)](https://arxiv.org/abs/2502.02982)
- [nanochat](https://github.com/karpathy/nanochat)
