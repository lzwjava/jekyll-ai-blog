---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Overload Crash Fixed
translated: false
type: note
---

Already finished. Here's the full picture:

---

COMPREHENSIVE SUMMARY

PROBLEM
-------

The tokenize script hung/crashed the workstation (192.168.1.36), making it so overloaded that sshd couldn't even complete the SSH banner exchange — TCP port 22 accepted connections but never responded. Required a physical reboot.

ROOT CAUSE
----------

The original script used `multiprocessing.Pool(16)` with `pool.imap()`. Each of the 16 worker processes:

1. Loaded an ENTIRE parquet file into memory via `pq.read_table()` (~280 MB on disk, larger decompressed)
2. Iterated rows and accumulated tokens into a Python list (`all_tokens.extend()`)
3. One parquet file produces ~369M tokens. A Python list of 369M int objects = ~10 GB RAM (Python int overhead ~28 bytes each)
4. 16 workers running in parallel = 160+ GB RAM needed on a 62 GB machine

Result: kernel OOM killer or catastrophic swap thrashing. The machine froze hard enough that sshd was starved of CPU/memory to send its banner.

Additionally, when workers get OOM-killed, `pool.imap()` hangs silently in the main process — no error, no output, just "Tokenizing with 16 workers..." followed by eternal silence.

THE FIX
-------

Rewrote the script with three key changes:

1. NO MULTIPROCESSING: Single-process. Each parquet file is already huge (~370M tokens), no benefit from parallelism when the bottleneck is memory, not CPU.

2. STREAMING PARQUET READS: Replaced `pq.read_table()` (loads entire file) with `pq.ParquetFile.iter_batches(batch_size=8192)` — processes 8192 rows at a time, never holds a full file in memory.

3. NUMPY BUFFER ACCUMULATION: Replaced Python list (`all_tokens.extend()`) with a pre-allocated numpy uint16 array of 100M tokens (200 MB). Tokens are written directly into this buffer with index tracking. When full, flush to disk as .npy shard. No Python list intermediate at all.

RESULT
------

  Input:  38 parquet files, 10.2 GB
  Output: 141 shards (1 val + 140 train), 27 GB on disk
  Tokens: ~14.07 billion
  Time:   41.1 minutes (~5.7M tok/s)
  Peak RAM: ~600 MB (vs 160+ GB with old script)

Next step: training. The output is in `/mnt/data/zz/datasets/github-code-tok/` in nanoGPT binary format, ready to use.
