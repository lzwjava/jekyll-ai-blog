---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streaming Parquet to Solve OOM Issues
translated: false
type: note
---

Question: What is this transcript describing, and how does it solve the out-of-memory (OOM) problem when processing large parquet files?

Answer:

## Overview

This is a transcript of someone working through a **memory management problem** while trying to extract text from large Hugging Face dataset parquet files on a resource-constrained server (2 vCPU, 3.8GB RAM).

---

## The Core Problem

They're trying to download and extract text from a massive dataset stored in **parquet format** (each shard ~2.1GB compressed). The server only has **3.8GB RAM**, which is not enough to load a full parquet file into memory at once.

---

## The Progression of Failed Attempts

Each approach ran out of memory (OOM = Out Of Memory, process gets "killed" by the Linux OOM killer):

| Attempt | Method | Why It Failed |
| --- | --- | --- |
| 1 | HuggingFace `datasets` streaming | Parquet decompression still buffers heavily in memory |
| 2 | `wget` download + `pd.read_parquet()` | `pandas` loads the entire 2.1GB file into RAM at once (~6–8GB needed) |
| 3 | `urllib.request.urlretrieve` + streaming | Still buffered; `pd.read_parquet` too large |
| 4 | PyArrow reader + `.to_pandas()` | `.to_pandas()` converts whole row groups into DataFrames in memory |

---

## The Working Solution: `iter_batches()`

The final fix was using **PyArrow's `iter_batches()`**, which is a true streaming reader:

```python
import pyarrow.parquet as pq

parquet_file = pq.ParquetFile("shard.parquet")

for batch in parquet_file.iter_batches(batch_size=1000):
    # Process only 1000 rows at a time
    for text in batch.column("text").to_pylist():
        outfile.write(text + "\n")
```

### Why `iter_batches()` Works

- Instead of loading the whole file, it reads **one small batch at a time** (e.g., 1,000 rows)
- Memory usage stays **constant** regardless of file size
- The rest of the file stays on disk until needed
- Successfully processed **100K rows from a 2GB parquet file without OOM**

---

## Key Concepts

**Parquet Row Groups** — Parquet files are divided into "row groups" internally. Earlier PyArrow methods read one entire row group at a time, which can still be hundreds of MB. `iter_batches()` subdivides even further.

**OOM Killer** — Linux automatically kills processes that exceed available RAM. The log shows the process getting "killed" mid-run — this is the kernel protecting system stability.

**Shard-based datasets** — Large HuggingFace datasets are split into multiple parquet "shards" (shard 0, shard 1, shard 2...). The plan is to process each shard sequentially, extracting text to a flat `.txt` file, which is far more memory-efficient for downstream tasks.

---

## Result

- Shard 0 → extracted **19M lines / 3.1GB of text** before the process died (but the output was saved)
- Shard 1 → tested successfully with `iter_batches`
- Shards 2+ → now running with the memory-safe pipeline
