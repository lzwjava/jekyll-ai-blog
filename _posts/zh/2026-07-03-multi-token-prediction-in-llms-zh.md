---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大型语言模型中的多令牌预测
translated: true
type: note
---

**问题：** 什么是LLM中的MTP（多令牌预测）？

**回答：**

MTP是指训练模型在每个位置预测**多个未来令牌**，而不仅仅是下一个令牌。标准的下一令牌预测（NTP）训练`P(t+1 | ≤t)`。MTP增加了对`t+2`、`t+3`……的目标。你需要了解的两种设计：Meta的并行多头版本（2024年论文）和DeepSeek-V3的顺序模块版本——后者是实际被前沿模型采用并延续到你正在使用的V3.x/R1系列中的方案。

### 为何要这么做

1. **更密集的训练信号。** 每个位置现在贡献D+1个损失项，而非1个。相同数据，更多梯度——样本效率更高，尤其在规模化时（Meta发现收益随模型规模增大而增长；小模型可能反而更差）。
2. **强制远见表征。** 要良好预测t+2，t处的隐藏状态必须编码一个计划，而不仅仅是局部续写。这缓解了纯教师强制的短视问题。
3. **推理时的免费推测解码。** 额外的头/模块起草未来令牌；主模块验证它们。DeepSeek-V3报告第二个令牌的接受率约为85–90%，解码TPS提升约1.8倍。

### Meta的版本（Gloeckle等人，2024）

共享Transformer主干，然后有`n`个独立的输出头，每个头是一个Transformer层，所有头共享解嵌入矩阵。头`k`从相同的主干隐藏状态预测令牌`t+k`。完全并行，预测令牌之间无因果链。损失 = n个交叉熵之和。

### DeepSeek-V3的版本（重要版本）

DeepSeek在每个预测深度保持**完整的因果链**。与并行头不同，MTP深度`k`是一个小型顺序模块：

```
h_k[i] = TransformerBlock_k( W_k · concat( RMSNorm(h_{k-1}[i]), RMSNorm(Emb(t[i+k])) ) )
logits  = SharedUnembed(h_k[i])   # 预测令牌 t[i+k+1]
```

关键点：
- 模块k接收**前一个深度的隐藏状态**以及**实际下一个令牌的嵌入**（训练时为ground truth）。因此预测t+2以知道t+1为条件——因果的，而非边际的。
- 嵌入矩阵和输出头与主模型**共享** → 参数成本低。
- V3使用**D = 1**（一个额外模块，预测一个额外令牌）。
- 损失：`L = L_main + λ · mean(L_mtp_k)`，训练早期λ=0.3，后期0.1。
- 在标准解码时**丢弃MTP模块**，或在推测解码时**保留作为自起草器**。

### 最小实现（~50行，DeepSeek风格）

```python
import torch, torch.nn as nn, torch.nn.functional as F

class MTPModule(nn.Module):
    def __init__(self, d, block_cls):
        super().__init__()
        self.norm_h = nn.RMSNorm(d)
        self.norm_e = nn.RMSNorm(d)
        self.proj = nn.Linear(2 * d, d, bias=False)
        self.block = block_cls(d)          # 一个Transformer块

    def forward(self, h_prev, tok_emb_next):
        # h_prev:       (B, T, d)  前一个深度的隐藏状态
        # tok_emb_next: (B, T, d)  下一个ground truth令牌的嵌入
        x = self.proj(torch.cat([self.norm_h(h_prev), self.norm_e(tok_emb_next)], dim=-1))
        return self.block(x)               # 内部使用因果注意力

class GPTWithMTP(nn.Module):
    def __init__(self, vocab, d, trunk, block_cls, depth=1):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.trunk = trunk                 # 你的主Transformer栈
        self.head = nn.Linear(d, vocab, bias=False)   # 共享解嵌入
        self.mtp = nn.ModuleList(MTPModule(d, block_cls) for _ in range(depth))

    def forward(self, idx, targets, lam=0.3):
        B, T = idx.shape
        e = self.emb(idx)
        h = self.trunk(e)                              # (B, T, d)
        loss = F.cross_entropy(self.head(h).flatten(0, 1), targets.flatten())

        h_k = h
        for k, mod in enumerate(self.mtp, start=1):
            # 对齐：位置i现在预测t[i+k+1]
            h_k = h_k[:, : T - k]
            e_next = self.emb(idx[:, k : T])           # ground-truth t[i+k]
            h_k = mod(h_k, e_next)
            tgt_k = targets[:, k : T]                  # 偏移后的目标
            loss_k = F.cross_entropy(self.head(h_k).flatten(0, 1), tgt_k.flatten())
            loss = loss + lam * loss_k
        return loss
```

要将其接入你的nanoGPT分支：主干不变；添加嵌入偏移的拼接、每个深度一个额外块，以及偏移后的交叉熵损失。在你的MI300X上运行时，预计会有小幅步时增加（D=1时约10%），但换来相同令牌数下更好的损失——这是DeepSeek在671B/14.8T令牌规模下认为值得的权衡。

### 推理：自推测解码

在解码时，运行主模型 → 得到t+1。将h和t+1的嵌入送入MTP模块 → 起草t+2。然后用一次主模型前向传播验证两个令牌；如果主模型的argmax/采样令牌一致则接受。接受率约85–90%意味着每步主模型平均产出约1.8个令牌。这是一种推测解码，其中起草模型几乎零成本，因为它重用了主干的隐藏状态——与EAGLE/Medusa对比，后者事后将类似的起草头附加到冻结模型上。MTP本质上是“Medusa，但从头联合训练，并保持因果链完整”。

### 当前地位

MTP作为训练目标现已成为DeepSeek系列的标准，并被越来越多地方复制；作为推理技巧，它与推测解码文献（Medusa、EAGLE-2/3）趋同。如果你在研究DeepSeek更新的MoE模型，MTP模块是除MLA和无辅助损失MoE路由之外的三个标志性组件之一——建议在阅读V3技术报告第2.2节时，同时打开上面的代码。

**参考文献：**

- [Better & Faster Large Language Models via Multi-Token Prediction (Meta, 2024)](https://arxiv.org/abs/2404.19737)
- [DeepSeek-V3 Technical Report — §2.2 Multi-Token Prediction](https://arxiv.org/abs/2412.19437)
- [Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)
- [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077)