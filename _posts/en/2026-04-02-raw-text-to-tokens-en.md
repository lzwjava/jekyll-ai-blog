---
audio: false
generated: true
image: false
lang: en
layout: post
title: Explaining Raw Text to Tokenized Data
translated: false
type: note
---

Based on your data preparation log, here's how to understand the "60GB text data" claim versus what you're seeing:

## What's Happening

**Your output**: 150 shards × ~0.19GB each ≈ **28GB total**

This suggests one of three scenarios:

### 1. **Compression/Tokenization Factor**

The "60GB" likely refers to **raw source text**, while the 28GB is **tokenized/binary format**:

- Raw text → tokens typically compresses 2-3× in binary format
- 60GB raw ÷ 2.1 = 28.5GB (matches your output)
- Each shard is likely a binary `.bin` or `.arrow` file, not raw text

### 2. **The Math from Your Log**

```
Speed: 40M tokens/sec
Time: ~20 minutes total = 1,200 seconds
Total tokens processed: 40M × 1,200 = 48B tokens
```

If each token averages ~0.6 bytes in binary format (typical for BPE):

- 48B tokens × 0.6 bytes ≈ **28.8GB** — matches your output

### 3. **What "60GB" Could Mean**

- **Raw text size**: 60GB of JSON/parquet/text files before processing
- **After tokenization**: 28GB of binary training data
- **Ratio**: ~2.1× compression (normal for text → tokens)

## Why This Matters

| Metric | Value | Meaning |
|--------|-------|---------|
| Raw input | ~60GB | Source text files |
| Binary output | 28GB | Ready for training |
| Tokens | ~48B | Actual training tokens |
| Shards | 150 | For parallel training |

## Check with

```bash
# Verify raw input size
du -sh /path/to/raw/data/

# Check one shard format
file /path/to/output/shard_0000.bin
```

**Bottom line**: Your processing is correct — 60GB raw text → 28GB tokenized output with ~48B tokens is a healthy ratio for LLM data preparation.
