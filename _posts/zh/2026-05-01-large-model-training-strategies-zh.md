---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大规模语言模型训练策略
translated: true
type: note
---

**问题：** 我应该如何筹划训练一个GPT-3规模的模型——思考数据收集策略、实际需要多少数据，以及在不支付昂贵外部带宽费用的情况下，最具成本效益的方式累积10TB以上的数据是什么？

**回答：**

问得好，你这个思路很对！让我分三个方面来阐述清楚：**实际需要多少数据**，**如何在不付出高额带宽成本的情况下获取数据**，以及**实际的策略**。

---

## 1. GPT-3规模的模型实际需要多少数据？

首先，让我们用实际数字来校准预期：

GPT-3的训练语料库起始于45TB的压缩纯文本（解压后大约90TB），但在过滤之后，实际用于训练的数据总量约为570GB —— 其中CommonCrawl贡献了约400GB。

所以关键洞察是：**原始数据量 ≠ 有效训练数据量**。巨大的原始数据经过过滤会大幅缩减。

作为参考：GPT-2的训练数据约为40GB文本，GPT-3约为500万亿个token，Phi-3约为3万亿个token。对于一个认真的个人实验，一个合理的数量级目标大约是1万亿个token。

对你目前60GB的实验而言——这已经接近GPT-2的规模，是一个合理的起点。跳跃到10TB原始数据对于GPT-3级别的目标来说并非不合理，但你需要考虑到重度过滤会显著减少数据量。

---

## 2. 数据质量 > 原始大小

一个在高质量开源数据上训练的较小模型，其性能可能优于在嘈杂、未经精心整理的数据集上训练的较大模型。预处理流程——去重、URL过滤、分词、污染检测——通常比架构创新更重要。

**你应该关注的关键预制数据集，而不是自己原始抓取所有内容：**

-   **FineWeb-edu** —— 1.5万亿个token，压缩后9TB —— 一个高质量的教育性子集，质量和大小比例极佳，托管在Hugging Face上（`HuggingFaceFW/fineweb-edu`）。
-   **The Pile** —— 800GB，经过整理，被广泛使用
-   **RedPajama** —— 1.2万亿个token
-   **RefinedWeb** —— 5万亿+个token

这些都是经过预过滤和去重的，能为你节省大量的预处理工作。

---

## 3. 如何在不付昂贵带宽费用的情况下获得10TB数据

你考虑这一点很正确。以下是实际的策略：

### 方案 A: 使用已有的开源数据集 (最佳投资回报率)
Common Crawl包含每月发布的PB级别的原始网页数据。GPT-3、LLaMA、OpenLLaMA和T5在预训练中都使用了它。你可以直接从 `commoncrawl.org` 下载特定的月度快照——他们通过AWS提供免费的S3访问，这是最便宜的途径。

### 方案 B: 使用 Hugging Face `datasets` 库进行流式传输
你不需要一次性下载10TB数据。使用Hugging Face的流式API——可以实时处理数据，而无需在本地存储所有内容。这完全避免了用于训练目的的带宽问题。

```python
from datasets import load_dataset
ds = load_dataset("HuggingFaceFW/fineweb-edu", streaming=True, split="train")
```

### 方案 C: 使用具有无限内部带宽的VPS/服务器 (你的DMIT方案)
你关于DMIT的想法用于批量下载是很好的：

-   使用一台**具有无限或高额度内部带宽**的VPS，从Hugging Face / Common Crawl S3下载数据集
-   然后通过**局域网/硬盘拷贝**传输到本地机器（不消耗外部配额）
-   对于10TB数据，硬盘成本约为$10/TB，那么**存储硬件成本大约为$100**

在eBay或亚马逊上可以找到约€10/TB的二手硬盘——只需要注意经销商宣称的“0小时使用时间”，并考虑到有些硬盘可能在运输中损坏。

### 方案 D: 向朋友/研究小组请求直接硬盘拷贝
这是完全可行的。学术实验室和机器学习社区经常出于这个原因直接共享硬盘。围绕Hugging Face的机器学习社区在这方面非常乐于合作。

---

## 4. 实际实施路线图

| 步骤 | 行动 |
| :--- | :--- |
| **现在 (60GB)** | 完成GPT-2规模的实验，运行基准测试（即使是简单的测试，如在保持集上的困惑度） |
| **下一步 (500GB–1TB)** | 下载FineWeb-edu子集，清理它，使用BPE进行分词 |
| **未来 (10TB+)** | 使用VPS批量下载Common Crawl快照，拷贝到本地硬盘 |
| **训练** | 使用Chinchilla缩放定律来匹配数据大小与模型参数数量 |

缩放定律显示，为了获得最佳性能，参数数量和数据大小应该成比例地缩放——一个70B参数模型在数据不足的情况下训练，其性能会逊色于一个7B参数模型在按比例缩放的高质量数据上训练。

目前最重要的事情是：**在你扩展规模之前，先对你60GB的GPT-2实验运行基准测试**。即使是简单的困惑度测量或少样本任务评估，也能在你的数据收集投入达到10TB之前告诉你你的流程是否有效。

---

**参考文献：**

-   [大语言模型解析 Part 2: 数据收集](https://joseparreogarcia.substack.com/p/llms-explained-part-2-data-collection-cleaning)
-   [用于大语言训练的开源数据集 - Kili Technology](https://kili-technology.com/large-language-models-llms/9-open-sourced-datasets-for-training-large-language-models)
-   [LLM训练数据集 - glennklockwood.com](https://www.glennklockwood.com/garden/LLM-training-datasets)
-   [在家进行基础性LLM预训练 - Medium](https://medium.com/@adrien_morvan/foundational-llm-pre-training-on-your-hardware-at-home-0dd4f2175ea5)
-   [LLMDataHub - GitHub](https://github.com/Zjh-819/LLMDataHub)
-   [FineWeb-edu on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)