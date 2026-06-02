---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 数据处理中的内存耗尽
translated: true
type: note
---

被 OOM killer 终止——内核日志确认：

```
Out of memory: Killed process 1093038 (python3.11)
total-vm:66255412kB, anon-rss:61268720kB ... oom_score_adj:0
```

该进程在 62 GB 的机器上占用了约 61 GB 常驻内存。

**为什么在约第 10 个分片时崩溃**

每个分片约为 2.2 GB 压缩 parquet → 加载为 DataFrame 时大约为 6–10 GB 的 Python 对象（字符串有巨大的每对象开销）。尽管每次迭代都会重新赋值 `df`，但 pyarrow/pandas 分配器并不能可靠地将内存返回给操作系统，因此 RSS 大致单调增长。经过约 10 个分片后，内存达到约 60 GB，内核便会杀死进程。

两个设计问题放大了这一情况：
- `pd.read_parquet(file)` 一次性加载整个分片。
- `df.iterrows()` 速度慢，且会为每一行分配一个 Series——产生数百万个临时对象。

**修复方案（按成本从低到高排列）**

1. 使用 pyarrow 流式处理批次，而非加载整个文件，并显式释放内存：
   ```python
   import pyarrow.parquet as pq, gc
   pf = pq.ParquetFile(parquet_file)
   for batch in pf.iter_batches(batch_size=10_000, columns=["text"]):
       for t in batch.column("text").to_pylist():
           if t and t.strip():
               f.write(t.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")
   del pf; gc.collect()
   ```
2. 即使保留 `read_parquet`，也要放弃 `iterrows()`——改用 `df["text"].to_list()`。
3. 更大的视角：将 176 个 × 2.2 GB 分片写入单个文本文件，会在磁盘上产生数百 GB 的数据，之后还需重新读取以进行分词。标准的 nanoGPT FineWeb 流水线直接从 parquet 分词为 `.bin` 分片——完全跳过巨大的中间 `.txt` 文件。

需要我重写 `extract_fineweb_gpt3.py` 为 pyarrow 流式版本，还是直接编写一个 parquet → 分词后 `.bin` 的脚本？
