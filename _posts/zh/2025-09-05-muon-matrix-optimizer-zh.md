---
audio: false
generated: true
image: false
lang: zh
layout: post
title: μ子：结构感知矩阵优化器
translated: true
type: note
---

Kimi 中的“Muon”指的是一种先进的优化器——具体来说，是用于训练 Kimi K2 语言模型的**结构感知矩阵正交化优化器**。

---

### 什么是 Muon 优化器？

1.  **矩阵感知优化**
    与 AdamW 或 SGD 不同，Muon 将权重矩阵视为几何实体，而非独立的标量参数。它应用**牛顿-舒尔茨迭代**对动量平均梯度进行正交化，从而产生条件良好、平衡的更新，同时尊重矩阵的行和列结构 ([Medium][1], [kellerjordan.github.io][2])。

2.  **通过牛顿-舒尔茨进行正交化**
    Muon 不执行昂贵的奇异值分解，而是使用一种快速迭代方法（牛顿-舒尔茨）来近似梯度的最近正交矩阵。这使得更新保持在**谱范数约束**下，保留了能量并在所有方向上均匀分散学习 ([Medium][1], [kellerjordan.github.io][2])。

3.  **流程调整**
    标准的更新流程——**梯度 → 动量 → 参数更新**——被替换为：
    **梯度 → 动量 → 牛顿-舒尔茨正交化 → 参数更新**。
    这一修改提高了二维参数矩阵的训练效率和稳定性 ([Medium][3], [kellerjordan.github.io][2])。

4.  **实际应用高效**
    尽管增加了少量计算开销，但 Muon 带来了显著的速度提升：

    *   在 NanoGPT 竞速中创下记录，训练时间缩短了约 35% ([kellerjordan.github.io][2])。
    *   在大语言模型训练中，与权重衰减和逐参数 RMS 调整结合时，扩展性良好 ([arXiv][4])。

5.  **坚实的理论基础**
    近期的研究支持了 Muon 的收敛特性、权重衰减的益处以及最佳批量大小。研究证实了其在各种实际场景下具有更紧的理论界限和效率 ([arXiv][5])。

---

### Muon 在 **Kimi K2** 中的作用

Kimi K2 是 Moonshot AI 的**专家混合模型**，拥有**总计 1 万亿参数**（激活 320 亿），为智能体能力优化。它在知识、推理和代码基准测试中取得了卓越的性能，这部分归功于使用了 Muon（以及一个称为 **MuonClip** 的变体）进行训练 ([Hugging Face][6], [Poe][7])。

*   **MuonClip 优化器** 指的是在超大规模应用 Muon，同时解决此类大模型固有的稳定性挑战 ([Hugging Face][6], [Poe][7])。
*   该优化器是实现**零训练不稳定性**（在约 15.5 万亿 token 的大型数据集上）并交付最先进结果的关键 ([Hugging Face][6])。

---

### 总结（按要求未使用表格）

*   **Muon** = “通过牛顿-舒尔茨正交化的动量”——一种用正交化更新替代原始梯度更新的优化器，改善了矩阵参数的学习动态。
*   它保留了结构，确保了平衡的更新，并通过迭代正交化而非昂贵的分解保持了效率。
*   **Kimi K2** 利用 Muon（和 MuonClip）突破了大规模 MoE 训练的极限，以稳定性和计算效率实现了顶级性能。

---

如果您想深入了解——例如 Muon 与 AdamW 在训练轨迹上的比较、MuonClip 如何为 MoE 调整算法，或者牛顿-舒尔茨方法在代码中如何工作——请告诉我！

[1]: https://medium.com/%40gauritr01/the-truth-about-kimi-k2-pretraining-muon-optimizer-moe-unpacked-43554527d94a?utm_source=chatgpt.com "揭秘 KIMI K2 预训练：Muon 优化器 ..."
[2]: https://kellerjordan.github.io/posts/muon/?utm_source=chatgpt.com "Muon：一种用于神经网络隐藏层的优化器"
[3]: https://medium.com/%40jenwei0312/going-beyond-adamw-a-practical-guide-to-the-muon-optimizer-93d90e91dbd3?utm_source=chatgpt.com "超越 AdamW：Muon 优化器实用指南 ..."
[4]: https://arxiv.org/html/2502.16982v1?utm_source=chatgpt.com "Muon 对于 LLM 训练是可扩展的"
[5]: https://arxiv.org/abs/2507.01598?utm_source=chatgpt.com "Muon 优化器的收敛界限与临界批量大小"
[6]: https://huggingface.co/moonshotai/Kimi-K2-Base?utm_source=chatgpt.com "moonshotai/Kimi-K2-Base"
[7]: https://poe.com/Kimi-K2?utm_source=chatgpt.com "Kimi-K2"
