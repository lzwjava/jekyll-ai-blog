---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen3查询偏移：小损失，稳定准确度
translated: true
type: note
---

问题：为什么将 Qwen3-27B 中的 Query 源上移 0.5 层仅导致约 2.7% 的质量损失？为什么 BF16 和 FP8 的测量结果如此一致？

回答：

**为什么质量损失如此之小（约 2.7% bpb）**

核心见解是，Query 表示在相邻层之间惊人地稳定。在 Transformer 中，残差流变化缓慢——每一层在前一状态的基础上添加一个相对较小的增量。当您将 Q 的源上移 0.5 层（具体而言：使用第 *n* 层的 FFN 前激活作为第 *n* 层 attention 的 Q，而不是使用 FFN 后激活）时，您提供给 attention 的是一个“半层陈旧”的表示。此时残差流已经达到完整层产生的约 97%，因此 attention 仍能计算出有意义的模式。

这也与你朋友提到的**模型解剖 / 模型结构**结论一致：注意力头从 Q 中读取的是粗略的位置/语义路由信息，而非精细变换后的特征。FFN 对 Q 的表达力贡献很小——K 和 V 从完整的 FFN 后表示中获益更多，因为它们编码了被检索的*内容*，而 Q 主要编码的是*要查找什么*。

**为什么仍然存在收益（权衡的动机）**

通过从第 *n* 层的 *FFN 之前*提取 Q，您可以并行执行 attention 和 FFN：
```
第 n 层：  [Attention(Q=x_pre, K/V=x_pre)] ∥ [FFN(x_pre)]
                    ↓                              ↓
          attention 输出            ffn 输出  → 求和 → x_{n+1}
```
这与**并行 Attention + FFN** 架构（例如 PaLM、某些 GPT-J 变体）的思路相同。~2.7% 的质量代价换来的是在 attention 和 FFN 可以重叠的硬件上真正的延迟降低。

**为什么 BF16 和 FP8 测量结果如此一致（+0.0181 vs +0.0191 bpb）**

| 因素 | 效果 |
|---|---|
| 扰动是架构性的，而非数值性的 | Early-Q 偏移引入了结构偏差；FP8 量化噪声基本与之正交 |
| FP8 已经使基线略有下降 | 基线和 Early-Q 都按比例下降，因此*增量*得以保持 |
| SGLang 的 FP8 路径对 Qwen3 校准良好 | Q/K/V 中的激活异常值通过逐张量或逐通道缩放处理，保持相对差异稳定 |
| 24552 个评估位置足够大 | 测量方差低；两种设置仅在数据类型 / 测试框架上有所不同，而非所测量的结构变化 |

近乎完美的复现（+2.66% vs +2.68%）实际上强有力地证明了该效应是一个**清晰的结构性信号**，而非任一评估设置的产物。如果数值精度与扰动相互作用，你会预期 BF16 和 FP8 的增量之间出现更大的差异。

**结论**

微小的损失证实了 Q 是一个低敏感度输入——Transformer 可以容忍陈旧的 Q，且路由误差极小，这使得 Early-Q 成为在无需微调的情况下，用很小的质量代价换取计算并行性的实用手段。

参考文献：
- [PaLM: Scaling Language Modeling with Pathways (parallel attention+FFN)](https://arxiv.org/abs/2204.02311)
- [GPT-J architecture (parallel layers)](https://github.com/kingoflolz/mesh-transformer-jax)
- [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)