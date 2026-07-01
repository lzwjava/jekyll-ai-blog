---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过流式传输 Parquet 解决内存溢出问题
translated: true
type: note
---

Question: 这段记录描述了什么，以及它是如何解决处理大型 parquet 文件时的内存溢出 (OOM) 问题的？

Answer:

## Overview

这是一份关于某人在资源受限的服务器（2 vCPU, 3.8GB RAM）上，尝试从 Hugging Face dataset 的大型 parquet 文件中提取文本时，解决 **memory management problem** 的过程记录。

---

## The Core Problem

他们正尝试下载并从以 **parquet format** 存储的海量数据集中提取文本（每个 shard 压缩后约为 2.1GB）。服务器仅有 **3.8GB RAM**，不足以一次性将整个 parquet 文件加载到内存中。

---

## The Progression of Failed Attempts

每种尝试都导致了内存溢出（OOM = Out Of Memory，进程被 Linux OOM killer “杀死”）：

| Attempt | Method | Why It Failed |
| --- | --- | --- |
| 1 | HuggingFace `datasets` streaming | Parquet 解压缩在内存中仍有大量缓冲 (buffering) |
| 2 | `wget` download + `pd.read_parquet()` | `pandas` 一次性将整个 2.1GB 文件加载到 RAM（需要约 6–8GB） |
| 3 | `urllib.request.urlretrieve` + streaming | 仍然存在缓冲；`pd.read_parquet` 占用过大 |
| 4 | PyArrow reader + `.to_pandas()` | `.to_pandas()` 会将整个 row groups 在内存中转换为 DataFrames |

---

## The Working Solution: `iter_batches()`

最终的解决方案是使用 **PyArrow** 的 **`iter_batches()`**，这是一个真正的 streaming reader：

```python
import pyarrow.parquet as pq

parquet_file = pq.ParquetFile("shard.parquet")

for batch in parquet_file.iter_batches(batch_size=1000):
    # Process only 1000 rows at a time
    for text in batch.column("text").to_pylist():
        outfile.write(text + "\n")
```

### Why `iter_batches()` Works

- 它不是加载整个文件，而是 **一次读取一个较小的 batch**（例如 1,000 行）。
- 无论文件大小如何，内存占用都保持 **constant**。
- 文件的其余部分保留在磁盘上，直到需要时才读取。
- 成功地从 **2GB parquet 文件中处理了 100K 行数据而没有发生 OOM**。

---

## Key Concepts

**Parquet Row Groups** — Parquet 文件在内部划分为 "row groups"。早期的 PyArrow 方法一次读取一整个 row group，这仍可能达到数百 MB。`iter_batches()` 则进行了进一步细分。

**OOM Killer** — Linux 会自动杀死超过可用 RAM 的进程。日志显示进程在运行中途被 "killed" —— 这是内核在保护系统稳定性。

**Shard-based datasets** — 大型 HuggingFace datasets 被拆分为多个 parquet "shards" (shard 0, shard 1, shard 2...)。目前的计划是按顺序处理每个 shard，将文本提取到扁平的 `.txt` 文件中，这对于后续任务来说内存效率更高。

---

## Result

- Shard 0 → 在进程结束前提取了 **19M 行 / 3.1GB 文本**（但输出已保存）。
- Shard 1 → 使用 `iter_batches` 测试成功。
- Shards 2+ → 正在使用内存安全的 pipeline 运行。
