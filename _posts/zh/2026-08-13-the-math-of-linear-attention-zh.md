---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 线性注意力的数学
translated: true
type: note
---

问题：LLMs中线性注意力的历史是什么——实际数学演变，而不仅仅是名称？

回答：

**核心技巧（Katharopoulos 等人，ICML 2020，"Transformers are RNNs"）**

标准注意力是 O(N²)，因为你需要显式地生成完整的 `QKᵀ` 矩阵：

```
O_i = Σ_j softmax(q_i · k_j) v_j
```

Katharopoulos 用可分离的核 `φ(q)·φ(k)ᵀ` 替换了 `softmax(q·k)`（他们使用了 `elu(x)+1`）。由于矩阵乘法是可结合的，你可以重新排序：

```python
import torch

def causal_linear_attention(q, k, v, feature_map=lambda x: torch.nn.functional.elu(x) + 1):
    # q, k, v: [B, T, D]
    q, k = feature_map(q), feature_map(k)
    S = torch.zeros(q.shape[0], q.shape[-1], v.shape[-1])  # [B, D, D] 运行状态
    z = torch.zeros(q.shape[0], q.shape[-1])                # [B, D] 归一化器
    outs = []
    for t in range(q.shape[1]):
        S = S + torch.einsum('bd,be->bde', k[:, t], v[:, t])  # 外积写入
        z = z + k[:, t]
        num = torch.einsum('bd,bde->be', q[:, t], S)
        den = torch.einsum('bd,bd->b', q[:, t], z).unsqueeze(-1) + 1e-6
        outs.append(num / den)
    return torch.stack(outs, dim=1)
```

这就是全部思路：注意力变成了一个**具有矩阵值状态** `S ∈ R^{D×D}` 的RNN，通过秩1外积写入 `k_t v_tᵀ` 进行更新。这是 O(N) 时间，每步 O(1) 内存（状态大小与T无关）。2020年以来的所有工作都是关于"`S`的最佳更新规则是什么"。

**时间线**

- **2020 — Katharopoulos, "Transformers are RNNs"**：上述的核技巧重述。
- **2020 — Performer（Choromanski 等人）**：FAVOR+，使用随机傅里叶特征来*无偏地*近似softmax，而非用任意核替换它。
- **2021 — Schlag 等人, "Linear Transformers are Secretly Fast Weight Programmers"**：将状态更新重新解释为快速权重记忆，并引入了**delta规则**写入（`S += k(v - S k)ᵀ`，即误差校正而非纯累积）——这在2024年再次变得重要。
- **2023 — RetNet（Sun 等人，微软亚洲研究院）**：为状态添加固定的指数衰减，`S_t = γS_{t-1} + k_t v_tᵀ`，并给出了**分块并行**形式（块内并行，块间循环），使其在GPU上实际快，而不仅仅是渐进性更好。
- **2023 — RWKV（Peng 等人）**：独立地收敛到相同的衰减状态思想（WKV），以真实LLM规模作为纯RNN训练，推理时无需注意力。
- **2023 — Mamba（Gu & Dao）**：字面上不是核化的注意力，而是一个**选择性状态空间模型**，其中衰减/门控依赖于输入——同样属于O(N)复杂度类别，成为并行分支。
- **2023年12月 — GLA, 门控线性注意力（Yang 等人）**：使衰减*数据依赖*且逐通道（不像RetNet那样是固定标量），并提供了硬件高效的块化Triton核。这催生了 `flash-linear-attention` (fla) 库，几乎所有后续论文都在此基础上构建。
- **2024 — DeltaNet（Yang 等人，NeurIPS）**：重新启用了Schlag的delta规则，并展示了如何通过矩阵乘法在块上并行化它——在联想召回质量上相比纯累积有巨大提升。
- **2024 — Mamba-2（Dao & Gu）**："State Space Duality"论文——正式证明SSM和线性注意力是同一计算的两种不同视角。
- **2024年12月 — Gated DeltaNet（Yang, Kautz, Hatamizadeh, NVIDIA）**：将GLA的门控与DeltaNet的delta规则写入相结合。状态更新：衰减 + 误差校正写入。
- **2025 — RWKV-7 "Goose"**：将delta规则推广为对角加低秩的状态转移矩阵（比标量衰减更具表现力）。
- **2025 — MiniMax-01（闪电注意力）**：第一个大规模生产LLM，以规模交付线性注意力——混合架构，7/8线性注意力层 + 1/8全softmax层，因为纯线性注意力在精确的长距离检索上仍有不足。
- **2025 — DeltaProduct, Titans, Miras**：进一步推进——每个token执行多个delta规则步骤，或将线性状态矩阵替换为MLP（非线性深度记忆）。

**统一视角**：2023年以来的每个模型都是 `S_t = A_t ⊙ S_{t-1} + k_t v_tᵀ`（或写入的delta规则变体），其中*唯一*的区别在于：(1) `A_t` 衰减是标量/对角/低秩且数据依赖的，以及(2) 写入是纯累积还是误差校正（delta规则）。最近的"测试时训练"框架（Sun 等人，2024）明确指出了这一点：状态更新*就是*对`key→value`回归损失的一个在线梯度下降步骤，而不同的论文只是在选择不同的优化器。

参考文献：

- [Transformers are RNNs (Katharopoulos et al., 2020)](http://proceedings.mlr.press/v119/katharopoulos20a.html)
- [Linear Transformers are Secretly Fast Weight Programmers (Schlag et al., 2021)](https://arxiv.org/abs/2102.11174)
- [Retentive Network (Sun et al., 2023)](https://arxiv.org/abs/2307.08621)
- [Gated Linear Attention Transformers (Yang et al., 2023)](https://arxiv.org/abs/2312.06635)
- [Parallelizing Linear Transformers with the Delta Rule (Yang et al., 2024)](https://arxiv.org/abs/2406.06484)
- [Mamba-2 / State Space Duality (Dao & Gu, 2024)](https://arxiv.org/abs/2405.21060)
- [Gated Delta Networks (Yang, Kautz, Hatamizadeh, 2024)](https://arxiv.org/abs/2412.06464)
- [flash-linear-attention (fla) library](https://github.com/fla-org/flash-linear-attention)
- [MiniMax-01 lightning attention](https://arxiv.org/abs/2501.08313)
