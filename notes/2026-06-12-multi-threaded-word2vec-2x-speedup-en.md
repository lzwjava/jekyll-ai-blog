---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-threaded Word2Vec 2x Speedup
translated: false
type: note
---

Done. Pushed to `origin/main`.

**What changed:**

- Multi-threaded training: 8 threads, `std::thread::scope` with `TrainPtrs` Send-safe wrapper
- Epoch loop in parallel path
- `-threads N` flag (default 4)
- Raw pointer training functions (`train_sg_raw`, `train_cbow_raw`)

**Performance on M2 Air (text8, 71k vocab, dim=200):**

| Config | Words/s | Time (5 epochs) |
|--------|---------|-----------------|
| `-threads 1` | 344k | ~240s |
| `-threads 8` | 740k | ~127s |

~2x speedup. Limited by memory bandwidth — all threads read/write the same 71k×200 weight matrices. The bottleneck is shared cache contention, not compute.

Usage:
```
cargo run --release -- word2vec train -input corpus.txt -output vec.bin -threads 8
```
