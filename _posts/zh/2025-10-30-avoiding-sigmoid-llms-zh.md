---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 为何大语言模型避免使用Sigmoid函数
translated: true
type: note
---

### 为什么 GPT/LLM 模型不使用 Sigmoid 函数

像 GPT 这样的大型语言模型（LLM）依赖于 Transformer 架构，其中激活函数在前馈网络（FFN）层中引入非线性特性，并处理注意力输出方面发挥着关键作用。虽然 Sigmoid 函数——定义为 \\(\sigma(x) = \frac{1}{1 + e^{-x}}\\)，将输入压缩到 (0, 1) 区间——在早期神经网络中很流行（例如用于二分类），但在现代 LLM 的内部激活中基本被避免使用。以下是具体原因，按关键问题分解：

#### 1. **梯度消失问题**
   - Sigmoid 在极端值处饱和：对于大的正 \\(x\\)，\\(\sigma(x) \approx 1\\)；对于大的负 \\(x\\)，\\(\sigma(x) \approx 0\\)。
   - 其导数为 \\(\sigma'(x) = \sigma(x)(1 - \sigma(x))\\)，在这些区域趋近于 0。在反向传播过程中，这会导致梯度"消失"（变得极小），从而阻碍深层网络的学习。
   - LLM 中的 Transformer 网络极深（例如 GPT-4 有 100+ 层），因此这会严重影响训练效率。像 ReLU (\\(f(x) = \max(0, x)\\)) 或 GELU（我们之前讨论过）这样的替代方案可以避免在负输入区域完全饱和，从而实现更好的梯度流动。

#### 2. **非零中心化输出**
   - Sigmoid 总是输出正值（0 到 1），这在优化过程中会给权重更新带来偏差。与 tanh 或 GELU 等零中心化函数相比，这会导致梯度下降路径呈"之字形"，减缓收敛速度。
   - 在 Transformer 中，FFN 层处理高维嵌入，零中心化激活有助于在残差连接中保持稳定的信号传播。

#### 3. **经验性性能不足**
   - 大量实验表明，在 NLP 任务中，Sigmoid 的性能落后于现代激活函数。早期的 Transformer（例如原始 GPT）使用 ReLU 以求速度和简洁。后来的模型如 GPT-2/3 转向使用 GELU，因为它具有平滑的、概率化的行为，经验证明可以在避免 Sigmoid 缺点的同时提高准确性和收敛性。
   - 像 SiLU（Sigmoid 线性单元，\\(f(x) = x \cdot \sigma(x)\\)) 这样的变体出现在一些 LLM 中（例如 InstructGPT），但这并非单纯的 Sigmoid——它乘以 \\(x\\) 以修正零中心化问题并减少饱和。

#### 4. **输出层考量**
   - 对于 LLM 中的下一词预测，最终层在 logits 上使用 **softmax**（一种归一化的多 Sigmoid 函数），而不是 Sigmoid。Sigmoid 适用于二元决策，但对于多类别词汇表（例如 5 万+个词元）则会失败，因为其输出之和不为 1，导致概率不稳定。
   - Softmax 确保了有效的概率分布，这对于交叉熵损失函数至关重要。

#### 何时仍会使用 Sigmoid？
- 在 LLM 的隐藏层中很少使用，但偶尔会在特殊位置出现，例如二元门控或较旧的 RNN/LSTM（Transformer 时代之前）。
- 在视觉模型中（例如某些 CNN），有时会用于像素归一化，但在专注于文本的 LLM 中不会使用。

总之，Sigmoid 在 1980 年代所具有的优雅特性无法适应 LLM 的深度和规模。ReLU/GELU/Swish 提供了更快、更可靠的训练，且陷阱更少。如果你正在调整模型，建议从 GELU 开始，以确保与 Transformer 的兼容性。

#### 参考资料
- [Transformer 模型中的线性层和激活函数](https://machinelearningmastery.com/linear-layers-and-activation-functions-in-transformer-models/)
- [深度学习 101：Transformer 激活函数详解](https://www.saltdatalabs.com/blog/deep-learning-101-transformer-activation-functions-explainer-relu-leaky-relu-gelu-elu-selu-softmax-and-more)
- [常用激活函数](https://www.aussieai.com/book/ch21-common-activation-functions)
- [理解 Logits、Sigmoid、Softmax 和交叉熵损失](https://wandb.ai/amanarora/Written-Reports/reports/Understanding-Logits-Sigmoid-Softmax-and-Cross-Entropy-Loss-in-Deep-Learning--Vmlldzo0NDMzNTU3)
