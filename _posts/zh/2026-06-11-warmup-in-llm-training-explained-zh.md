---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM训练预热解析
translated: true
type: note
---

**问题：** 在LLM训练中，"warmup（预热）"是什么意思？

**回答：**

预热是指在训练开始时使用一个极小的学习率，并在前N个步骤中将其逐渐提高到目标学习率，而不是从第0步就直接让优化器使用完整的学习率。

**计划（nanoGPT风格）**

你在 `train.py` 中见过这个：

```python
def get_lr(it, warmup_iters=2000, max_iters=600000,
           max_lr=6e-4, min_lr=6e-5):
    # 1) 线性预热
    if it < warmup_iters:
        return max_lr * (it + 1) / (warmup_iters + 1)
    # 2) 余弦衰减至 min_lr
    if it > max_iters:
        return min_lr
    ratio = (it - warmup_iters) / (max_iters - warmup_iters)
    coeff = 0.5 * (1.0 + math.cos(math.pi * ratio))  # 1 → 0
    return min_lr + coeff * (max_lr - min_lr)
```

因此，对于GPT-2规模的训练：学习率在大约2k步内从0线性增长到6e-4，然后在剩余的训练过程中进行余弦衰减。

**为什么需要它——三个基本原理**

1. **Adam的矩估计在早期不可靠。** Adam通过 `m_t / (sqrt(v_t) + eps)` 来缩放更新，其中 `v_t` 是平方梯度的指数移动平均（EMA），`beta2=0.95–0.999`。在第1步时，`v_t` 仅由大约1个样本估计得出。偏差修正虽然能修正*期望值*，但无法修正*方差*——每个参数的有效学习率都极其嘈杂。早期少数几个不幸的大步骤可能会将权重推入一个永远无法恢复的糟糕区域（甚至直接导致NaN）。预热可以保持步长较小，直到 `v_t` 已经见过足够多的梯度，从而成为一个有意义的估计值。这正是RAdam（Liu等人，2019）提出的动机，该研究展示了预热 ≈ 降低Adam自适应学习率的方差。

2. **初始化时的尖锐曲率。** 在初始化阶段，随机Transformer附近的损失景观条件很差——注意力logits、LayerNorm梯度以及嵌入/反嵌入会产生大量尺度不当的梯度。早期的大步骤会将你推向高曲率区域；一旦注意力熵崩溃（某些头饱和为one-hot状态），就很难挽回了。预热让网络先温和地进入一个更平滑的盆地。

3. **大批量稳定性。** LLM预训练使用巨大的有效批量大小（0.5M–4M tokens）。大批量 → 低梯度噪声 → 你需要大学习率以提高效率——但初始化时的大学习率会导致发散。预热是其中的桥梁（这是Goyal等人2017年原始"一小时ImageNet"论文中的技巧，其中学习率与批大小的线性缩放仅在配合预热时才有效）。

**没有预热的表现**：在前几百步中出现损失尖峰或NaN，或者训练虽然能进行，但最终稳定在一个永久性更差的损失值上（与使用相同超参数但包含预热训练的情况相比）。

**实际数字参考**

- nanoGPT/GPT-2 124M–760M：约700–2000个预热迭代步
- 大型训练（LLaMA, DeepSeek）：通常预热约占总 token 数的0.1–1%（例如，LLaMA-2为2000步）
- 预热时间过长只会浪费算力；过短则有导致不稳定的风险。它是一个相对宽容的超参数——数量级重要，精确值不敏感。

**更深入一层：预热部分是一种补丁。** 多项研究表明，可以通过修复底层不稳定性来减少或消除预热：更好的初始化（例如，GPT-2/nanoGPT已经使用的缩放残差初始化 `0.02/sqrt(2*n_layer)`）、使用Pre-LN代替Post-LN（Xiong等人，2020年证明了Post-LN在初始化时存在梯度爆炸问题，这正是原始Transformer*需要*预热的原因）、z-loss / logit soft-capping、QK-norm或μP风格的参数化。现代相关性：DeepSeek等公司使用**WSD（预热-稳定-衰减）**计划——预热，然后是长时间恒定学习率，最后是短暂急剧衰减——因为它允许你从任何检查点恢复/扩展训练，而无需像余弦衰减那样预先提交总步数。

考虑到你在MI300X上训练GPT-2 760M：将预热保持在约2000步。如果你看到即使有预热，早期仍有损失尖峰，请将 `beta2` 从0.99降至0.95和/或将梯度裁剪收紧到1.0——这些直接作用于预热所解决的同一早期训练方差问题。

**参考文献：**

- [Attention Is All You Need — 原始预热计划，§5.3](https://arxiv.org/abs/1706.03762)
- [自适应学习率的方差及其超越（RAdam）](https://arxiv.org/abs/1908.03265)
- [Transformer架构中的层归一化（Pre-LN vs Post-LN）](https://arxiv.org/abs/2002.04745)
- [准确的大批量SGD（Goyal等人，大批量预热）](https://arxiv.org/abs/1706.02677)
- [nanoGPT train.py — get_lr 实现](https://github.com/karpathy/nanoGPT/blob/master/train.py)
