---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Transformer块：注意力然后多层感知机
translated: true
type: note
---

**问题：** 在 nanoGPT 的 12 层（或 20 层）堆叠中，每个块内部包含什么？FFN 是否包裹了 MLP，注意力机制是否在 MLP 内部？

**回答：**

接近了，但嵌套关系有两处错误。我们来修正这个思维模型：

**1. MLP 和 FFN 是同一回事。** 这是同一个模块的两个名称。"前馈网络"（Feed-Forward Network）是论文中的术语（《Attention Is All You Need》），而"MLP"是 Karpathy 在 nanoGPT 代码中的叫法。它们之间没有包裹关系——它们是同义词。

**2. 注意力机制不在 MLP 内部。** 注意力机制和 MLP 在块内部是*同级*关系，按顺序执行。每个块恰好包含两个子层：

```
Block = LayerNorm → Attention → 残差相加
      → LayerNorm → MLP(FFN) → 残差相加
```

以下是实际的 nanoGPT 代码（[model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)）：

```python
class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = LayerNorm(config.n_embd, bias=config.bias)
        self.attn = CausalSelfAttention(config)   # 子层 1
        self.ln_2 = LayerNorm(config.n_embd, bias=config.bias)
        self.mlp = MLP(config)                    # 子层 2（这就是 FFN）

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))   # 先执行注意力
        x = x + self.mlp(self.ln_2(x))    # 再执行 MLP/FFN
        return x
```

而 MLP 本身——内部没有注意力机制，只是两个线性层中间夹着 GELU 激活函数：

```python
class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd)  # 扩展 4 倍
        self.gelu   = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd)  # 投影回原维度

    def forward(self, x):
        return self.c_proj(self.gelu(self.c_fc(x)))
```

因此，对于 GPT-2 124M（`n_layer=12, n_embd=768`），每个 token 向量的流动路径为：

```
x ∈ R^768
  → ln_1 → 注意力（token 之间相互交流）  → + x
  → ln_2 → 768 → 3072 → GELU → 3072 → 768  → + x
```

× 12 个块，然后经过最终的 LayerNorm → lm_head。

有两个细节值得深入理解：

- **预归一化（Pre-norm）**：nanoGPT（遵循 GPT-2）将 LayerNorm 放在*每个子层之前*，而不是像 2017 年原始 Transformer 那样放在之后。预归一化保持了残差流的清洁，并且在深层时训练更加稳定——这就是为什么你可以堆叠 12、20、48 层而无需预热技巧。
- **分工**：注意力是唯一让 token 之间相互混合的地方（通信）；MLP 则独立处理每个 token 位置（计算）。Karpathy 的框架是："注意力是通信，MLP 是计算。"

关于残差流的一个有用直觉：将 `x` 想象成一个共享的 768 维"总线"，从上到下流动，每个注意力/MLP 子层从中读取数据，计算某些内容，然后将贡献*加回*总线。没有任何东西包裹任何东西——这是在同一个流上执行的 24 次顺序的"读取-计算-相加"操作（12 次注意力 + 12 次 MLP）。

一个 GPT-2 块的参数检查：注意力 ≈ 4 × 768² ≈ 236 万，MLP ≈ 8 × 768² ≈ 472 万——MLP 占据了每个块约 2/3 的参数。在你 7.6 亿参数的运行中，比例相同（直到你使用 MoE，此时 FFN 正是被复制到专家中的部分——这就是 DeepSeek v4 的关联点）。

**参考资料：**

- [nanoGPT model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [《Attention Is All You Need》](https://arxiv.org/abs/1706.03762)
- [GPT-2 论文（《Language Models are Unsupervised Multitask Learners》）](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)