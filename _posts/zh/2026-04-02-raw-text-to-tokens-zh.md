---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 原始文本到令牌化数据的解释
translated: true
type: note
---

根据您的数据准备日志，以下是如何理解“60GB text data”声明与您所见内容的对比：

## 发生了什么

**您的输出**：150 shards × 每个 ~0.19GB ≈ **28GB 总计**

这表明三种可能情况之一：

### 1. **Compression/Tokenization Factor**
“60GB”很可能指的是**raw source text**，而 28GB 是**tokenized/binary format**：
- Raw text → tokens 通常在 binary format 中压缩 2-3 倍
- 60GB raw ÷ 2.1 = 28.5GB（与您的输出匹配）
- 每个 shard 很可能是一个 binary `.bin` 或 `.arrow` 文件，而不是 raw text

### 2. **The Math from Your Log**
```
Speed: 40M tokens/sec
Time: ~20 minutes total = 1,200 seconds
Total tokens processed: 40M × 1,200 = 48B tokens
```

如果每个 token 在 binary format 中平均 ~0.6 bytes（BPE 的典型值）：
- 48B tokens × 0.6 bytes ≈ **28.8GB** — 与您的输出匹配

### 3. **What "60GB" Could Mean**
- **Raw text size**：处理前的 60GB JSON/parquet/text 文件
- **After tokenization**：28GB binary training data
- **Ratio**：~2.1× 压缩（文本 → tokens 的正常情况）

## 为什么这很重要

| 指标       | 值     | 含义                  |
|------------|--------|-----------------------|
| Raw input | ~60GB | Source text files    |
| Binary output | 28GB | Ready for training   |
| Tokens    | ~48B  | Actual training tokens |
| Shards    | 150   | For parallel training |

## 检查方法：
```bash
# Verify raw input size
du -sh /path/to/raw/data/

# Check one shard format
file /path/to/output/shard_0000.bin
```

**要点**：您的处理是正确的 — 60GB raw text → 28GB tokenized output，带有 ~48B tokens，是 LLM 数据准备的健康比例。