---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parquet Streaming Optimizations for Text Extraction
translated: false
type: note
---

Done. Key changes:

- **Streaming**: `pq.ParquetFile(file).iter_batches(batch_size=10_000, columns=[text_col])` — only loads 10k rows at a time, only the `text` column. RSS stays flat instead of growing each shard.
- **No `iterrows()`**: batch → `to_pylist()` → write. Orders of magnitude faster and far less allocation.
- **Detect text column once per file** from the schema instead of scanning column names every row.
- **`del pf; gc.collect()`** between files so allocator releases pages.
- **Counters separated**: `total_rows_processed` (read) vs `total_rows_written` (non-empty after strip), so progress is accurate.

Memory ceiling now is roughly `BATCH_SIZE × avg_doc_size` ≈ a few hundred MB per shard, not the whole shard. You can run all 176 files without OOM.

One thing worth reconsidering before you launch a multi-hour run: the resulting `.txt` will be hundreds of GB and you'll just re-read it to tokenize. Going parquet → tokenized `.bin` directly skips that. Say the word if you want me to write that variant instead.
