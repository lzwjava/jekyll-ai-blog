---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于文本提取的Parquet流式优化
translated: true
type: note
---

完成。关键变更：

- **流式处理**：`pq.ParquetFile(file).iter_batches(batch_size=10_000, columns=[text_col])` —— 每次仅加载1万行，且仅读取`text`列。内存占用保持稳定，不再随分片增长。
- **移除`iterrows()`**：批量处理 → `to_pylist()` → 写入。速度提升数个数量级，且内存分配大幅减少。
- **每个文件仅从schema中检测一次text列**，而非逐行扫描列名。
- **在文件之间执行`del pf; gc.collect()`**，确保内存分配器释放页面。
- **分离计数器**：`total_rows_processed`（读取行数）与`total_rows_written`（去除空白行后的行数），进度显示更准确。

现在内存上限约为 `BATCH_SIZE × avg_doc_size`，每个分片仅需几百MB，而非整个分片。你可以无内存溢出地处理全部176个文件。

在启动耗时长任务前，有一点值得重新考虑：生成的`.txt`文件可能达数百GB，后续仍需重新读取进行分词。直接从parquet转为tokenized `.bin`格式可跳过这一步骤。如需我编写该替代方案，请告知。
