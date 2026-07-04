---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型预训练数据集
translated: true
type: note
---

**问题：** 除了 FineWeb，还有哪些文本数据集可用于 LLM 预训练？

**答案：**

以下是按各数据集在训练混合中扮演的角色组织的实际概览。

## 通用网页文本（FineWeb 替代品/同类）

- **DCLM-Baseline**（DataComp-LM，约 3.8T token）—— Apple/华盛顿大学基于分类器过滤的 Common Crawl。在许多基准测试中，它在每个 token 上的表现与 FineWeb-Edu 相当或更好；DCLM 论文中的 fastText 质量分类器本身就值得研究。
- **RefinedWeb** —— 约 600B token 的激进去重 Common Crawl，用于训练 Falcon 系列模型。
- **Dolma**（AI2，约 3T token）—— 完全开放的流水线 + 数据，为 OLMo 提供支持。如果你想*复现*每一个过滤决策，这是最佳选择。
- **RedPajama v1/v2** —— LLaMA 风格预训练数据的开放复现，采用 Apache 2.0 许可；v2 版本以列的形式附带了质量信号，因此你可以自行进行过滤。
- **C4** —— 谷歌为 T5 清理的 Common Crawl 快照；年代较久且噪声更大，但体积小且是消融实验的标准选择。
- **Nemotron-CC**（NVIDIA，约 6.3T token）—— 结合了分类器集成 + 低质量文档的合成改写。有趣之处在于它展示了用 LLM 改写数据比直接丢弃数据效果更好。
- **TxT360** —— 在 99 个 CC 快照 + 14 个精选来源上进行全局去重。
- **原始 Common Crawl** —— 上述所有数据集的基石；每月抓取的数据量达数百 TiB，涵盖约 20 亿个页面。经过语言识别、去重和质量过滤后，实际保留的字节数通常只有 2–10% —— 只有在你自己构建流水线时才需要用到它（考虑到你的兴趣，这确实是一个很好的学习项目）。

## 精选 / 多来源

- **The Pile** —— 825 GB，涵盖 22 个不同来源（书籍、论文、GitHub），约 300B token。虽然年代较久，但由于每个 token 的多样性，它非常适合 nanoGPT 规模的数据运行。
- **SlimPajama** —— RedPajama 经去重后的 627B token 版本。
- **Wikipedia + Stack Exchange + Project Gutenberg** —— 体积小、质量高，几乎是每个混合中的标准上采样组件。

## 代码

- **The Stack v2** —— 67.5 TB，涵盖 600 多种语言的宽松许可源代码，为 StarCoder2 提供支持。即使对于“文本”模型，在混合中加入 5–15% 的代码也能显著提升推理能力。
- **StarCoderData** —— 如果你不想使用原始 Stack，这是过滤后的训练子集。

## 数学（每个 token 对推理的提升最大）

- **OpenWebMath** —— 约 15B token，来自网页的保留 LaTeX 格式的数学内容。
- **FineMath** —— 54B token，类似 FineWeb-Edu 的过滤方式，专注于教育类数学内容。
- **Nemotron-CC-Math** —— 133B token 的高质量数学预训练集。
- **Proof-Pile-2** —— 数学 + 形式化证明 + arXiv，用于训练 Llemma。

## 多语言

- **FineWeb-2** —— 多语言版 FineWeb，覆盖 1000 多种语言（包含强大的中文子集）。
- **HPLT 2.0** —— 4.5T token，涵盖 75 种语言。
- **MADLAD-400** —— 3T token，400 种语言，来自谷歌。

## 适合你规模的实用配方

对于 GPT-2 760M / nanoGPT 级别的运行（约 10–100B token，MI300X），一个强有力的混合方案：

```python
# 约 1B 模型的类 Chinchilla 混合，从 HF 流式加载
from datasets import load_dataset, interleave_datasets

mix = interleave_datasets([
    load_dataset("HuggingFaceFW/fineweb-edu", "sample-100BT", split="train", streaming=True),
    load_dataset("mlfoundations/dclm-baseline-1.0", split="train", streaming=True),
    load_dataset("bigcode/starcoderdata", data_dir="python", split="train", streaming=True),
    load_dataset("HuggingFaceTB/finemath", "finemath-4plus", split="train", streaming=True),
], probabilities=[0.55, 0.25, 0.10, 0.10], seed=42)
```

比替换数据集更有价值的两个做法：

1. **自行在 760M / 10B token 规模上对 DCLM 与 FineWeb-Edu 进行消融实验** —— 不同基准测试的结果不同，运行消融实验比任何排行榜都更能让你学到东西。Karpathy 的 nanochat 使用 FineWeb-Edu 分片，恰恰因为它是一个可靠的默认选择，而不是因为它总是最优。
2. **研究过滤分类器，而不仅仅是输出结果**。FineWeb-Edu 的分类器是一个轻量级回归器，基于 Llama-3-70B 对嵌入进行的教育价值标注训练而成 —— 你可以在一周内，用你的 4070 显卡，重新训练该流水线以适应自定义领域（例如，专注于 agent/工具使用的语料库）。

**参考资料：**

- [FineWeb-Edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- [The Top 10 LLM Training Datasets for 2026 — iMerit](https://imerit.ai/resources/blog/the-top-10-llm-training-datasets-for-2026/)
- [Best LLM Training Datasets for 2026 — SpyderProxy](https://spyderproxy.com/blog/best-llm-training-datasets)
- [Top 10 LLM Training Datasets — ODSC](https://opendatascience.com/the-top-10-llm-training-datasets-for-2026/)