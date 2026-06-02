---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 斯坦福 CS25 Transformer 讲座 Vaswani 授课
translated: true
type: note
---

Question: 视频里说了什么？ (https://www.youtube.com/watch?v=1GbDTTK3aR4)

Answer:

这段视频是 Stanford CS25 的讲座，题为“我如何学会停止担忧并爱上 Transformer”，由 Ashish Vaswani 于 2023 年 11 月 7 日演讲。Ashish Vaswani 是 2017 年开创性论文《Attention is All You Need》（该论文引入了 Transformer 架构）的合著者之一。他在讲座中讨论了 Transformer 的设计初衷、演变过程以及未来的潜在研究方向。

### 讲座要点：

- **历史背景**：Vaswani 从 1956 年的 Dartmouth Conference 讲起，当时早期的 AI 研究人员旨在通过精确的规则来模拟人类智能。他指出基于规则的系统如何力不从心，以及现代 AI 如何低估了对大规模计算资源的需求——如今 Transformer 运行在巨大的数据中心上。

- **NLP 的演变**：早期的机翻译系统（Machine Translation）是复杂的流水线（例如：词对齐 word alignments、重评分 rescoring）。神经网络简化了这一过程，并在 2013-2014 年左右催生了用于翻译和问答（QA）等任务的 sequence-to-sequence 模型。

- **Attention 和 Transformer 的兴起**：循环模型（如 LSTM）在顺序处理和并行化方面存在问题。Attention 机制允许更好的摘要提取，而 2017 年的 Transformer 完全用 self-attention 取代了循环结构，实现了并行计算、直接的 token 交互，并通过 dot-product attention 实现了 GPU 优化。

- **Transformer 架构细节**：
  - 用于捕捉复杂关系（如主谓一致）的 Multi-head attention。
  - Positional encodings（最初是正弦函数；后来改进为相对位置编码或 rotary encodings）。
  - Residual connections 和 pre-layer normalization，用于训练更深的模型。

- **2017 年后的改进**：
  - 相对位置编码（如 RoPE）。
  - 用于处理长序列的 Sparse attention。
  - 诸如 Flash Attention 和 grouped-query attention 等效率优化。
  - 转向更大模型和系统级改进。

- **影响力与应用**：Transformer 推动了翻译（如 Google 的无装饰系统）、解析（parsing）和多模态（multimodal）任务的突破。它们通过可扩展的、数据驱动的学习，使 AI 更接近最初的 Dartmouth 愿景。

- **未来方向**：关于 agents、工具使用、推理、效率（如低精度训练）的研究，以及向通用模型的整合。挑战包括专业化和对齐（alignment）。

- **问答环节**：涵盖了诸如 induction heads、非自回归解码（non-autoregressive decoding）的困难（由于排序和众数崩塌 mode collapse）、语言模型中的世界模型（world models，对机器人规划有用）、大型模型的泛化性、多智能体系统（multi-agent systems）、模块化（如 mixture of experts），以及 Vaswani 在其初创公司中利用 Transformer 自动化工作流程的工作。

该讲座强调了 Transformer 如何将许多 AI 方法整合到一个可扩展、高效的架构中，从而推动现代技术的进步。

References:

- [Video Page](https://www.youtube.com/watch?v=1GbDTTK3aR4)
- [Stanford CS25 Course Playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM)
- [Stanford CS25 Course Website](https://web.stanford.edu/class/cs25/)
