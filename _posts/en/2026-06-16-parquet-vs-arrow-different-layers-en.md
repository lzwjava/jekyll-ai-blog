---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Parquet vs Arrow: Different Layers"
translated: false
type: note
---

**Question:** Between Parquet and Arrow, which has better performance?

**Answer:**

They're not really competitors — they solve **different problems** at different layers of the data stack. But let's compare them precisely.

## What They Are

| | Parquet | Arrow |
|---|---|---|
| Type | **Columnar storage format** (on-disk) | **Columnar memory format** (in-memory) |
| Designed for | Long-term storage, compression, query pushdown | Zero-copy IPC, in-process analytics, SIMD |
| Row group / batch | Row groups (MB-scale chunks) | RecordBatches (configurable) |
| Encoding | RLE, dict, delta, bit-packing + Snappy/Zstd/LZ4 | Raw typed buffers (no compression by default) |
| Spec owner | Apache (originated at Twitter/Cloudera) | Apache (originated at Wes McKinney / Cloudera) |

## Performance Breakdown

### Disk I/O → Parquet wins

Parquet's compression + encoding means **5–10x smaller files** than raw Arrow IPC files. For cold reads from S3/NFS, Parquet wins massively due to predicate pushdown and column pruning — you skip reading data at the **file format level**.

```python
# Parquet reads only the columns you ask for — at the C++ reader level
import pyarrow.parquet as pq
table = pq.read_table("data.parquet", columns=["user_id", "event"])
```

### In-memory compute → Arrow wins (not even close)

Arrow buffers are **SIMD-friendly**, cache-aligned, zero-copy between processes/languages. No deserialization needed.

```python
import pyarrow as pa
import pyarrow.compute as pc

# SIMD vectorized, no Python loop overhead
result = pc.sum(table.column("revenue"))
```

Parquet data must be **decoded into Arrow** before compute anyway — that's exactly what DuckDB, Polars, and pandas 2.0 do internally.

### Serialization / IPC → Arrow wins

Arrow IPC (Feather v2) is essentially zero-copy. Writing and reading back a 1GB dataset:

```
Parquet write: ~2–5s (compression cost)
Arrow IPC write: ~0.1–0.3s (memcpy speed)

Parquet read: ~0.5–1s (decompress + decode)
Arrow IPC read: ~0.05s (mmap, near zero)
```

### Query engines use both together

The real pattern is **Parquet on disk → Arrow in memory**:

```
S3/disk         ──[Parquet]──►  DuckDB/Polars  ──[Arrow]──►  result
(compressed,                    (decodes to
 column pruned,                  Arrow buffers,
 predicate pushed)               runs SIMD ops)
```

DuckDB, Polars, DataFusion, Spark, and BigQuery all do this internally.

## Concrete numbers (rough, hardware-dependent)

| Operation | Parquet | Arrow IPC |
|---|---|---|
| Read 1GB from disk | ~0.5–2s | ~0.05–0.1s (mmap) |
| Write 1GB | ~2–5s | ~0.1–0.3s |
| File size (1GB raw) | ~100–300MB | ~900MB–1GB |
| Column scan (in-memory) | N/A (already decoded) | ~1–5 GB/s SIMD |

## When to use which

**Use Parquet when:**

- Storing datasets long-term (S3, HDFS, local)
- Dataset is large and you query subsets of columns
- You need interoperability across systems (Spark, BigQuery, Athena, DuckDB)
- Cold storage / archival

**Use Arrow (IPC/Feather) when:**

- Passing large datasets between processes (e.g., Python → Rust CLI agent)
- Caching intermediate results in a pipeline (avoid re-decoding)
- Building a data service where latency matters
- Shared memory between processes (Arrow's `plasma` store or `mmap`)

## Practical example — your CLI agent workflow

If your `ww`/`zz` agents process large datasets:

```python
import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

# Load from cold storage (Parquet, compressed)
table = pq.read_table("events.parquet", columns=["ts", "event", "user_id"])

# Cache hot working set as Arrow IPC for fast re-reads
with ipc.new_file("events_cache.arrow", table.schema) as writer:
    writer.write_table(table)

# Next run — sub-100ms reload
with ipc.open_file("events_cache.arrow") as reader:
    table = reader.read_all()
```

## TL;DR

- **Parquet** = best for **storage efficiency and disk I/O** (compression, column pruning, ecosystem compatibility)
- **Arrow** = best for **compute throughput and IPC** (SIMD, zero-copy, no deserialization overhead)
- In practice: **Parquet stores it, Arrow processes it** — they're designed to work together, not compete.
