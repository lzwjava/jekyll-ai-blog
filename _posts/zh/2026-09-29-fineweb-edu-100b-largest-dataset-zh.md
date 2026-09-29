---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb-Edu 100B最大数据集
translated: true
type: note
---

以下是两个项目之间的完整数据集对比：

## `/mnt/data/nanoGPT` 中的数据集（当前目录）

| 数据集 | 位置 | 大小 | 格式 |
| --- | --- | --- | --- |
| **FineWeb-Edu 100B** | `data/fineweb/edu_fineweb100B/` | **263 GB** | 1408 × 191 MB `.npy` 分片 ⬅ 最大 |
| FineWeb 文本 | `data/fineweb/train_fineweb.old.txt` | 16 GB | 原始文本 |
| FineWeb 令牌 | `data/fineweb/train.bin` | 6.9 GB | 已标记化的 uint16 |
| Wikipedia | `data/wikipedia_local/` | 580 MB | 文本 + bin 文件 |
| Shakespeare | `data/shakespeare_char/` | 3.3 MB | 文本 |
| sec-edgar | `data/sec-edgar/` | 0 B | 空（数据位于 `/mnt/data/sec-edgar-gpt*`） |

## `/mnt/data/nanochat` 中的数据集

**本地未存储任何数据集。** 其预训练语料库（ClimbMix-400B，约400B令牌）会按需从 HuggingFace 下载，以 191 MB 的 parquet 分片形式存在（`~/.cache/nanochat/base_data_climbmix/`），目前磁盘上尚不存在。仅有分词器/评估资源（约 30 MB）被缓存。

## `/mnt/data` 中其他相关数据集

| 数据集 | 大小 |
| --- | --- |
| `bilingual-gpt/`（由 `out-bilingual` 使用） | 25 GB — `mixed.txt` 占 11 GB 文本，外加 7.5 GB + 3.3 GB jsonl 分片 |
| `sec-edgar-gpt/` | 985 MB |
| `sec-edgar-gpt-124m/` | 955 MB |
| `cache/` | 77 GB（很可能是 HF/分词器缓存） |
| `bigcode-dataset/` | 20 MB |

## 结论

**最大的数据集是 FineWeb-Edu 100B 令牌分片，大小为 263 GB**，位于 `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B/`。nanochat 没有任何本地训练数据集（它从 HuggingFace 流式加载）。如果只计算原始文本，当前目录下的 16 GB `train_fineweb.old.txt` 仍然是最大的。
