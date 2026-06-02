---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: QK-Norm 技术的全面介绍
translated: true
type: note
---

**Question:** 请提供关于 QK-Norm 的全面介绍。

**Answer:**

### 什么是 QK-Norm？

QK-Norm (Query-Key Normalization) 是一种应用于 Transformer 模型（特别是 LLMs）Attention 机制中 Query (Q) 和 Key (K) 向量的 Normalization 技术。引入该技术是为了通过防止 Q 和 K 向量的 Norm 过度增长来提高训练稳定性。如果 Q 和 K 的 Norm 过大，会导致极大的 Attention Logits，从而使 Softmax 输出饱和（产生接近 One-hot 的 Attention 分布），并引发后续的训练不稳定或不收敛（Divergence）。

与应用于整个输入的标准 LayerNorm 或 RMSNorm 不同，QK-Norm 特别是在计算点积**之前**对 Q 和 K 进行 Normalization。这使得 Attention Scores 更接近 Cosine Similarities，从而限制了 Logits 的范围并降低了对数值波动的敏感性。

### 背景与动机

在标准的 Scaled Dot-product Attention 中：

\\[
\text{Attention}(Q, K, V) = \softmax\left(\frac{Q K^T}{\sqrt{d_k}}\right) V
\\]

其中 \\(d_k\\) 是 Head Dimension。如果没有适当的控制，Q 和 K 的 Norm 在训练过程中可能会呈指数级增长，特别是在 Multimodal 模型（例如混合文本和图像）或使用高 Learning Rate 时。这会导致 Attention Logits \\(Q K^T\\) 的数值变得非常大，从而导致：

- Softmax 饱和（输出接近 0 或 1）。
- 不稳定的 Gradients 和 Loss Spikes。
- 训练不收敛（Divergence）。

QK-Norm 通过沿 Head Dimension 对 Q 和 K 向量进行 Normalization（通常使用 RMSNorm 或 L2 Normalization）来解决这个问题，通常后面还会接一个可学习的 Scaling Parameter 以保持模型的表达能力。

### QK-Norm 的工作原理

修改后的 Attention 计算步骤如下：

1. 照常计算 Q 和 K。
2. 对两者分别应用 Normalization：
   - \\( Q' = \rms_norm(Q) \\)（或 L2 Norm：\\( Q' = Q / \|Q\|_2 \\)）
   - \\( K' = \rms_norm(K) \\)
3. （可选）乘以一个可学习的 Scalar \\(\alpha\\)（或每个 Head 独立的 Scalars）以恢复 Scaling 的灵活性。
4. 计算点积：\\( Q' (K')^T \\)（由于 Norm 已被限制，\\(\sqrt{d_k}\\) 的缩放可能会被调整或移除）。

这确保了点积是有界的（例如，对于单位向量，范围在 [-1, 1] 之间），在防止 Logit 任意爆炸的同时，通过 Scaling Parameter 维持了模型产生尖锐或平滑 Attention 分布的能力。

常见的变体包括：

- **Per-head QK-Norm**：每个 Attention Head 进行独立的 Normalization。
- **Per-layer QK-Norm**：在所有 Head 间共享，但每层独立。
- 与其他 Norm 结合（例如 QKV-Norm 同时对 Q、K 和 V 进行 Normalization）。

### 优势

- **提高训练稳定性**：允许使用更高的 Learning Rate（在某些情况下最高可达 3 倍）而不会出现不收敛。
- **更好的低精度数值稳定性**：对于在边缘设备上进行 FP16/BF16 Inference 至关重要，降低了 Overflow 风险。
- **提升性能**：通常能带来更低的 Perplexity 和更好的下游任务结果。
- **在 Multimodal LLMs 中非常有用**：防止来自不同 Token Embeddings（如文本 vs 图像 Token）引起的不稳定性。
- **无显著额外开销**：增加的计算量极小（Normalization 计算成本很低）。

### 历史与应用

- **起源**：在 2020 年的论文 "Query-Key Normalization for Transformers" 中针对低资源机器翻译提出，提升了 BLEU 分数。
- **普及**：在 Vision Transformers（如 Scaling Vision Transformers, 2023）和 Multimodal 模型（如 Chameleon, 2024）中获得关注。
- **现代 LLMs**：为了稳定性，被近期的模型广泛采用：
  - Qwen3 系列（使用 QK-Norm 取代 QKV Biases）。
  - DeepSeek, Gemma 2, OLMo 2, MiniMax-M2, StableLM 等变体。
  - 通常与 RMSNorm 和 Post-norm 布局结合使用。

随着模型规模的增长以及对多样化模态或长上下文的整合，它已成为训练大规模 Transformers 的标准工具。

### 局限性与替代方案

- 可能需要微调 Scaling Parameter。
- 由于 Q/K 的部分实例化，与某些高效 Attention 变体（如 Multi-Latent Attention）不兼容。
- 替代方案：Softmax Capping、QK Clipping 或用于 Logit 控制的权重重参数化（Weight Reparameterization）。

总的来说，QK-Norm 是一个简单但强大的改进，为现代 LLMs 的可靠缩放（Scaling）做出了显著贡献。

**参考文献：**

- [Query-Key Normalization for Transformers (arXiv:2010.04245)](https://arxiv.org/abs/2010.04245)
- [Scaling Vision Transformers (Dehghani et al., 2023)](https://arxiv.org/abs/2206.07682) (在视觉/多模态语境下普及)
- [Methods of improving LLM training stability (arXiv:2410.16682)](https://arxiv.org/abs/2410.16682)
- [QK Norm and the Curious Case of Logit Drift (Ross Taylor's blog)](https://rossjtaylor.com/blog/qk-norm-and-the-curious-case-of-logit-drift/)
- [Qwen3 Technical Report (提到为稳定性而采用 QK-Norm)](https://qwenlm.github.io/blog/qwen3/)
