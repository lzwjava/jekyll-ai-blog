---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Exhaustion in Data Processing
translated: false
type: note
---

Killed by the OOM killer — kernel log confirms:

```
Out of memory: Killed process 1093038 (python3.11)
total-vm:66255412kB, anon-rss:61268720kB ... oom_score_adj:0
```

The process hit ~61 GB resident on a 62 GB machine.

**Why on file ~10**

Each shard is ~2.2 GB compressed parquet → roughly 6–10 GB of Python objects when loaded as a DataFrame (strings have huge per-object overhead). Even though `df` is reassigned each iteration, pyarrow/pandas allocators don't reliably return memory to the OS, so RSS grows roughly monotonically. After ~10 shards you're at ~60 GB and the kernel kills you.

Two design issues amplify it:
- `pd.read_parquet(file)` loads the entire shard at once.
- `df.iterrows()` is slow and allocates a Series per row — millions of temporaries.

**Fixes (cheapest first)**

1. Stream batches with pyarrow instead of loading whole files, and free explicitly:
   ```python
   import pyarrow.parquet as pq, gc
   pf = pq.ParquetFile(parquet_file)
   for batch in pf.iter_batches(batch_size=10_000, columns=["text"]):
       for t in batch.column("text").to_pylist():
           if t and t.strip():
               f.write(t.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")
   del pf; gc.collect()
   ```
2. Drop `iterrows()` even if you keep `read_parquet` — use `df["text"].to_list()`.
3. Bigger picture: writing a single text file across 176 × 2.2 GB shards = ~hundreds of GB on disk that you'll then re-read to tokenize. The standard nanoGPT FineWeb pipeline tokenizes directly from parquet into `.bin` shards — skip the giant intermediate `.txt` entirely.

Want me to rewrite `extract_fineweb_gpt3.py` with the pyarrow streaming version, or go straight to a parquet → tokenized `.bin` script?
