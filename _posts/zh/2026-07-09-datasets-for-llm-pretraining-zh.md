---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM预训练数据集
translated: true
type: note
---

**问题：** 除了FineWeb，还有哪些文本数据集可以用于LLM预训练？

**回答：**

以下是按每个数据集在训练混合中的角色分类的实际场景。

## 通用网络文本（FineWeb的替代/同类数据集）

- **DCLM-Baseline**（DataComp-LM，约3.8T token）—— Apple/华盛顿大学基于分类器过滤的Common Crawl。在许多基准测试中，每个token的表现与FineWeb-Edu持平或更优；DCLM论文中的fastText质量分类器本身就值得研究。
- **RefinedWeb** —— 约600B token，经过积极去重的Common Crawl，用于训练Falcon系列模型。
- **Dolma**（AI2，约3T token）—— 完全开放的流水线+数据，驱动OLMo。如果你希望*复现*每一个过滤决策，这是最佳选择。
- **RedPajama v1/v2** —— 在Apache 2.0许可下对LLaMA风格预训练数据的开源复现；v2版附带质量信号列，可自行进行过滤。
- **C4** —— Google为T5模型清理的Common Crawl快照；较旧且噪声较多，但体积小，适合消融实验的标准选择。
- **Nemotron-CC**（NVIDIA，约6.3T token）—— 结合分类器集成与低质量文档的合成重写。有趣的是，它表明用LLM重写数据比直接丢弃更有效。
- **TxT360** —— 跨99个CC快照及14个精选来源进行全局去重。
- **原始Common Crawl** —— 上述所有数据集的基石；每月爬取数百TiB，涉及约20亿页面。经过语言识别、去重和质量过滤后，实际保留2–10%的字节——只有在你构建自己的流水线时才考虑（鉴于你的兴趣，这确实是一个很好的学习项目）。

## 精选/多源数据集

- **The Pile** —— 825 GB，涵盖22个不同来源（书籍、论文、GitHub），约300B token。虽然较旧，但由于每个token的多样性，非常适合nanoGPT规模的运行。
- **SlimPajama** —— RedPajama的去重版本，627B token。
- **Wikipedia + Stack Exchange + Project Gutenberg** —— 体积小、质量高，几乎每个混合数据中都会标准性地过采样这些组件。

## 代码数据

- **The Stack v2** —— 67.5 TB，涵盖600多种语言的宽松许可源代码，驱动StarCoder2。即使对于“文本”模型，在混合数据中加入5–15%的代码也能显著提升推理能力。
- **StarCoderData** —— 如果你不想要原始Stack，这是经过过滤的训练子集。

## 数学数据（每个token对推理能力提升最高）

- **OpenWebMath** —— 约15B token，来自网络，保留LaTeX格式的数学内容。
- **FineMath** —— 54B token，教育类数学内容，过滤方式与FineWeb-Edu类似。
- **Nemotron-CC-Math** —— 133B token的高质量数学预训练集。
- **Proof-Pile-2** —— 数学+形式化证明+arXiv，用于训练Llemma。

## 多语言数据

- **FineWeb-2** —— 覆盖1000多种语言的多语言版FineWeb（包含强大的中文子集）。
- **HPLT 2.0** —— 4.5T token，涵盖75种语言。
- **MADLAD-400** —— 3T token，400种语言，来自Google。

## 适合你规模的实用配方

对于GPT-2 760M / nanoGPT级别的运行（约10–100B token，MI300X），一个强力的混合方案：

```python
# 适用于约1B模型的Chinchilla风格混合，从Hugging Face流式加载
from datasets import load_dataset, interleave_datasets

mix = interleave_datasets([
    load_dataset("HuggingFaceFW/fineweb-edu", "sample-100BT", split="train", streaming=True),
    load_dataset("mlfoundations/dclm-baseline-1.0", split="train", streaming=True),
    load_dataset("bigcode/starcoderdata", data_dir="python", split="train", streaming=True),
    load_dataset("HuggingFaceTB/finemath", "finemath-4plus", split="train", streaming=True),
], probabilities=[0.55, 0.25, 0.10, 0.10], seed=42)
```

比更换数据集更有价值的两个举措：

1. **自行在760M / 10B token规模下对比DCLM与FineWeb-Edu** —— 结果因基准测试而异，运行消融实验能让你学到更多，远胜于任何排行榜。Karpathy的nanochat使用FineWeb-Edu分片，恰恰是因为它是可靠默认值，而非因为它总是最优。
2. **研究过滤分类器，而不仅仅是输出结果**。FineWeb-Edu的分类器是一个轻量级回归模型，在嵌入层上基于Llama-3-70B的教育价值标注进行训练——你可以在周末利用你的4070显卡，针对自定义领域（例如面向智能体/工具使用的语料库）重新训练该流水线。

**参考文献：**

- [FineWeb-Edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
- [The Top 10 LLM Training Datasets for 2026 — iMerit](https://imerit.ai/resources/blog/the-top-10-llm-training-datasets-for-2026/)
- [Best LLM Training Datasets for 2026 — SpyderProxy](https://spyderproxy.com/blog/best-llm-training-datasets)
- [Top 10 LLM Training Datasets — ODSC](https://opendatascience.com/the-top-10-llm-training-datasets-for-2026/)
