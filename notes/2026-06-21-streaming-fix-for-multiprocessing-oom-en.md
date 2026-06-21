---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streaming Fix for Multiprocessing OOM
translated: false
type: note
---

Running great. Here's the summary:

```
Progress: 3/38 files | 12 shards | 1.11B tokens | 5.7M tok/s
Memory: 6.5 GB / 62 GB (plenty of headroom)
ETA: ~40 min total
```

The fix:

1. ROOT CAUSE: The old script used `multiprocessing.Pool(16)`. Each worker loaded an entire parquet file into a Python list of token ints. One file = 369M tokens × ~28 bytes per Python int = ~10 GB RAM PER WORKER. 16 workers = 160+ GB. Instant OOM — either killed by the kernel or thrashing so hard sshd couldn't even send its banner.

2. FIX: Removed multiprocessing entirely. Now uses `pq.ParquetFile.iter_batches()` to stream row groups (8192 rows at a time) and writes tokens directly into a pre-allocated numpy uint16 buffer (200 MB for 100M tokens). Single process, ~600 MB peak RAM. No Python list intermediate.

3. Also fixed: EOT token uses `enc.eot_token` (50256) instead of the old `enc._special_tokens["
