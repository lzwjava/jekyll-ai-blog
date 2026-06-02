---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 优化 FineWeb 数据流水线
translated: true
type: note
---

## 🔍 Detailed Review: FineWeb Pipeline

---

### 问题回顾（以及原因）

**尝试 1: `datasets` streaming 库 → OOM killed**

`load_dataset(..., streaming=True)` 的承诺具有误导性。即使在 "streaming" 模式下，HF `datasets` 库仍然会：
- 将整个 Arrow schema 加载到内存中
- 在内部队列中缓冲解压后的 parquet 块
- 运行 Python 迭代器，产生显著的每个对象开销

在 1.9GB RAM 上：写入 115MB 后崩溃
在 3.8GB RAM 上：写入 223MB 后崩溃

**根本原因：** 不是数据流本身的问题，而是 HF 库的开销。Arrow table 表示法即使在 "streaming" 时也非常消耗内存。

**尝试 2: `pd.read_parquet()` → OOM killed**

将整个 2.1GB 的 parquet 读取到 pandas DataFrame 中。Pandas + Arrow 转换需要大约文件大小 3-4 倍的 RAM。一个 2GB 的 parquet 需要 ~6-8GB RAM 才能加载。在 3.8GB 内存上瞬间崩溃。

**尝试 3: `pyarrow.ParquetFile.read_row_group()` → OOM killed**

虽然比完整的 pandas 好，但对 row group 执行 `to_pandas()` 仍然会将整个 chunk 转换为 DataFrame。FineWeb 中的 row groups 很大（约 100K+ 行），所以问题依旧。

**尝试 4: `pyarrow.iter_batches(batch_size=4096)` → ✅ 成功运行**

这是正确的方法。它：
- 流式传输小的 RecordBatches（一次 4096 行）
- 每个 batch 在内存中仅占几 MB
- 永远不会将整个 parquet 加载到 RAM
- 内存峰值保持在 500MB 以下

---

### 当前状态评估

| Metric | Value |
|---|---|
| Shards processed | 5 of 21 |
| Text extracted | 13 GB |
| Lines written | 76M |
| Disk used | 18 GB of 77 GB |
| RAM peak | ~500 MB |
| OOM kills | 0 (with iter_batches) |

**剩余的分片 (5-20):** 16 × ~2GB = ~32GB parquet → ~42GB text
**预计总计:** ~55GB raw text
**处理完所有分片后的磁盘:** 77GB - 18GB - 32GB download - 42GB text ≈ **紧张但可行**（提取后会删除分片）

---

### 接下来需要做什么

**1. Tokenization（关键缺失环节）**

你现在有 76M 行原始文本。在训练之前，需要将其转换为 `train.bin` 和 `val.bin`：

```python
# 5 个分片的 token 计数
# ~13GB text ≈ 3-4 billion tokens (GPT-2 BPE)
# 完整的 21 个分片 ≈ 12-15 billion tokens
```

Tokenization 脚本需要：
- 逐行读取文本（内存安全）
- 使用 `tiktoken` GPT-2 encoder 进行 Tokenize
- 写入二进制 `uint16` 数组
- 按 90/10 比例拆分 train/val

**预计 Tokenized 大小：**
- 5 个分片: ~6-8 GB (`train.bin` + `val.bin`)
- 21 个分片: ~24-30 GB

**2. 磁盘空间计算**

| File | 5 shards | 21 shards |
|---|---|---|
| Raw text | 13 GB | 55 GB |
| Tokenized | 7 GB | 28 GB |
| Parquet (temp) | 0 GB (deleted) | 0 GB |
| **Total** | **20 GB** | **83 GB** ⚠️ |

21 个分片将 **超过 77GB 的磁盘限制**。你需要：
- 逐个分片进行 Tokenize（下载 → 提取 → tokenize → 删除文本）
- 升级到更大的磁盘
- 使用更少的分片（`sample-10BT` 使用约 5 个分片）

**3. 下载的并不是 `sample-10BT` 子集**

当前的 parquet 分片来自 `CC-MAIN-2013-20`，这是完整的 FineWeb dataset，而不是经过精选的 `sample-10BT`。对于 GPT-2 124M 训练，`sample-10BT` 更合适：
- 经过精选的质量过滤
- ~10B tokens，正好适合该模型的大小
- 无需下载 21 个分片

**4. 缺少 HF token → 速率限制**

你正在以匿名方式下载。HF 限制未认证的下载速度至约 1GB/小时。每个 2GB 的分片需要 2 小时以上。完整下载需要 40 小时以上。使用 token 后：速度快约 10 倍。

---

### 建议

**立即行动（现在）：**
- 你已经有 5 个分片 / ~13GB / ~3-4B tokens。这足以测试完整的 pipeline。
- 先不要下载更多分片。对现有数据进行 Tokenize，验证训练流程能否跑通。

**在完整下载之前：**
1. 设置 HF token: `huggingface-cli login`
2. 切换到 `sample-10BT` 子集（经过精选且大小合适）
3. 编写逐分片处理的 pipeline（下载 → 提取 → tokenize → 清理）以保持在磁盘限制内
4. 将 tokenized 后的 `train.bin`/`val.bin` 传输到你的 RTX 4070 上进行实际训练

**关于训练：**
- 使用 GPT-2 124M config 处理 5 个分片（~3-4B tokens）可以生成一个不错的模型
- 在有效 batch 为 524K tokens/iter 的情况下，设置 `max_iters=~12000` ≈ 训练量为 6.3B tokens（遍历数据集一次）
- 这与你之前的 `train_log_fineweb3.txt` 配置相匹配

---

### 总结

| Issue | Severity | Fix |
|---|---|---|
| HF `datasets` OOM | ✅ Solved | 使用 `pyarrow.iter_batches` |
| Missing tokenizer | 🔴 Blocker | 编写 `prepare.py` |
| Wrong subset (full vs sample-10BT) | 🟡 Quality | 使用 `sample-10BT` 进行训练 |
| No HF token | 🟡 Speed | `huggingface-cli login` |
| Disk too small for all shards | 🟡 Capacity | 逐个分片 Tokenize 或减少分片数量 |
| Config mismatch | 🟡 Correctness | 根据实际 token 数量设置 `max_iters` |

最困难的部分（内存安全的提取）已经解决。剩下的只是流程衔接。需要我帮你写 tokenizer 并连接整个 pipeline 吗？
