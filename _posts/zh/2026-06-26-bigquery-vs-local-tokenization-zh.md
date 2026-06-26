---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BigQuery 与本地令牌化
translated: true
type: note
---

问题：当LLM对大Parquet文件进行分词时，CPU在某些情况下可能挂起或停滞。BigQuery是否已经为您处理了这种大规模处理？

回答：

让我区分一下您混为一谈的两件不同事情，因为答案对每个都不一样。

## 1. CPU 在大 Parquet 上“挂起”——实际发生了什么

当您本地对一个大的 Parquet 进行分词，CPU 出现停滞时，几乎从来不是因为分词器本身慢。通常是以下原因之一：

- **将整个 Parquet 加载到内存中** —— `pd.read_parquet()` 或 `pq.read_table()` 会物化所有数据。一个 50GB 的 Parquet 文件在 16GB 的机器（您的 M2 Air）上会交换到磁盘，进程看起来就像挂起。解决办法是流式处理，而不是增加 CPU。
- **单线程分词** —— HuggingFace 的 `tokenizers`（基于 Rust）很快且释放了 GIL，但如果您在 Python 循环中逐行调用它，所有工作都会序列化到一个核心上。
- **行组物化** —— Parquet 是列式的；逐行读取以进行分词与这种格式相悖。

本地解决办法是流式处理行组并进行批量分词：

```python
import pyarrow.parquet as pq
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
pf = pq.ParquetFile("big.parquet")

for batch in pf.iter_batches(batch_size=10_000, columns=["text"]):
    texts = batch.column("text").to_pylist()
    enc = tok(texts, truncation=True, max_length=1024)  # 批量处理，Rust，多核
    # 将编码结果写入分片（np.memmap / .bin）——不要保留在内存中
```

这是 nanoGPT/nanochat 的 `prepare.py` 模式：流式读取 → 批量分词 → 写入连续的 `uint16` `.bin` 分片。CPU 永远不会挂起，因为通过批次限制了内存，并且 Rust 分词器在批次内并行化。

## 2. “BigQuery 能处理吗？”——能，但它解决的是**不同的问题**

BigQuery 是一个**列式、分布式 OLAP 数据仓库**（底层是 Dremel）。它绝对解决了“大 Parquet 放不下 / 单 CPU 停滞”的问题——但针对的是 **SQL 风格的转换**，而不是运行分词器。

BigQuery 免费为您提供：

- **没有机器内存上限** —— 它是无服务器的；Google 会将扫描分散到数千个节点上。50GB 或 5TB 的 Parquet 与本地内存无关。
- **列式修剪** —— 如果您只需要 `text` 列，它只读取该列的存储，不会读取其余部分。
- **大规模并行** —— 扫描/过滤/聚合会自动分片。

因此，如果您的“分词”是 BigQuery SQL 能表达的操作，那么答案是肯定的，它可以处理。而且现在越来越**可以**了：

- `ML.GENERATE_TEXT` / `ML.GENERATE_EMBEDDING` —— BigQuery ML 可以直接在 SQL 中对表调用 Vertex AI / Gemini 模型，为您批量和并行化处理。
- **远程函数 / `ML.PREDICT`** —— 您可以注册一个模型并逐列应用。

但有一个明显的边界：**BigQuery 不会运行您的 HuggingFace 分词器**。没有原生的“将这段文本分词为 GPT-2 BPE ID”的 SQL 函数。如果您想要**您特定的**分词器（与您正在训练的模型匹配的那个），您有以下选择：

- **远程 UDF** —— 将您的分词器包装成 Cloud Function / Cloud Run 端点，注册为 BigQuery 远程函数，然后逐行调用。BigQuery 会并行化这些调用。可行，但对于数十亿行来说，网络往返会使其变慢且昂贵。
- **JS UDF** —— 纯 JS 的 BPE 实现；对于实际的分词器来说不实用。
- **导出再处理** —— 务实的选择：使用 BigQuery 在数据仓库规模上对语料进行**过滤/去重/采样**，将清洗后的 `text` 列导出为 GCS 上的 Parquet/JSONL，然后在 GPU/CPU 机器（您的 MI300X 云实例或工作站）上运行上述流式分词器。

## 对于您的训练管道的实际答案

对于 nanoGPT 规模到 DeepSeek-v4 规模的数据准备，AI 原生的分工如下：

1. **BigQuery 负责繁重的数据工程** —— 去重、语言过滤、质量评分、采样、连接。这是“我的机器放不下”的终结。让 Dremel 吞噬 TB 级数据。
2. **自己流式分词清理后的输出** —— 因为分词器必须与您的模型完全匹配，并且您需要连续的 `.bin` 分片以实现快速的训练数据加载。在拥有 CPU 核心的地方（工作站）或在 GPU 旁边的机器上运行它。

BigQuery 解决了**规模**问题。它没有解决**分词器保真度**问题。不要试图将 BPE 分词强行塞入 SQL——这是您保留在本地/自行掌控的那一部分，并且上述流式批处理模式意味着无论语料多大，它都不会挂起。

如果您告诉我您的实际语料大小以及您正在准备哪个分词器/模型，我将为您提供精确的 `prepare.py`，其中包含针对您的 MI300X 加载器调整的分片大小。
