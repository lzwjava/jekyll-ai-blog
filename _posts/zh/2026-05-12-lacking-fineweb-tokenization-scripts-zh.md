---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺少FineWeb分词脚本
translated: true
type: note
---

简短回答：**不——此仓库中没有分词脚本。** 仅包含下载 + parquet→文本提取功能。

当前 `scripts/` 目录中的内容：
- `download/` — 获取 FineWeb parquet 分片（以及 Wikimedia 数据转储）
- `extract/extract_fineweb.py` — 将 parquet 行连接成单个 `.txt` 文件，插入 `<|endoftext|>` 分隔符（`datasets/fineweb-edu/` 中已包含原始 parquet 分片）
- `analysis/` — 日志/评估辅助工具
- 没有 `prepare.py`，没有 `tiktoken`/`uint16` 写入器，没有 `train.bin`/`val.bin` 输出

**在将数据交给 nanoGPT 之前，你需要：**

1. 将 parquet 文件连接成带有 EOT 分隔符的文本文件 — 此步骤已由 `extract_fineweb.py` 完成（但它指向 `fineweb_test_dump/`，而非 `datasets/fineweb-edu/`）。
2. 使用 GPT-2 BPE（`tiktoken.get_encoding("gpt2")`）对该文本进行分词，在文档之间添加 `<|endoftext|>` 的 ID 值。
3. 将 token ID 以 `np.uint16` 格式写入平面的 `train.bin` / `val.bin` 文件（这是 nanoGPT 的 `train.py` 通过 `data/<name>/{train,val}.bin` 进行内存映射的格式）。

权威参考是 nanoGPT 的 `data/openwebtext/prepare.py` — 它流式加载 HuggingFace 数据集，使用 tiktoken 并行分词，并输出 `train.bin`/`val.bin`。我们需要一个 `scripts/extract/prepare_fineweb_edu.py`，执行相同操作，但改为读取 `datasets/fineweb-edu/` 中的本地 parquet 分片，而不是从 HuggingFace 拉取。

需要我编写这个准备脚本（parquet 分片 → 使用 GPT-2 BPE 的 `train.bin` + `val.bin`）吗？