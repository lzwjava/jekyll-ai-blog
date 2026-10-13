---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Current Repo Algorithms: Quicksort and Word2Vec"
translated: false
type: note
---

Here's every algorithm/implementation currently in the repo:

## 1. Quicksort — Lomuto partition scheme (3 languages)

Identical algorithm in all three, used for cross-language benchmarking on 10,000 ints:

| File | Notes |
| --- | --- |
| `quicksort.py` | Recursive, pivot = last element, `i`/`j` swap scan; timed with `time.perf_counter()` |
| `Quicksort.java` | Same Lomuto partition; seeded `Random(42)`, timed with `System.nanoTime()` |
| Rust version | Mentioned in README ("via the TUI project's main binary") — but **not actually present in `src/`** anymore; README is stale on this point |

Characteristics: last-element pivot (no randomization → worst case O(n²) on sorted input), in-place, average O(n log n), recursion depth O(n) worst case.

## 2. Word2Vec — `src/word2vec.rs` (~39 KB, the big one)

A faithful Rust port of Mikolov's original `word2vec.c`, zero external deps:

- **Skip-gram with negative sampling** (`train_sg`) — context → center word
- **CBOW with negative sampling** (`train_cbow`) — averaged context → center word
- **Negative sampling table**: unigram distribution raised to power **0.75**, table size 1e8
- **Subsampling of frequent words**: `ran = (sqrt(f/t) + 1) * (t/f)` — Mikolov's frequent-word dropping trick
- **Sigmoid lookup table** approximation (precomputed `exp_table`) instead of `exp()` per step
- **Dynamic window reduction**: `b = next_random % window` (random context window shrinking per sample)
- **Linear learning-rate decay** over total training words
- **LCG PRNG** matching the original C: `next_random * 25214903917 + 11`
- **Vocabulary building** with `min_count` frequency pruning
- **Multi-threaded training** via raw pointers (`UnsafeCell` wrapper) — deliberately replicates the original pthreads "benign data races" design
- Output in text or binary format (`word\0<float32 × dim>`)

## 3. Everything else is I/O, not algorithms

- `gcloud.rs` — reads/parses gcloud config & credentials files, shells out to `gcloud config/auth list`
- `uno.rs` — serial port open/listen/status
- `main.rs` — sysinfo sampling (CPU %, memory, disk) formatted into ratatui tables

**Summary:** the project really has two algorithmic pieces — **quicksort (Lomuto)** as a language benchmark, and a fairly complete **word2vec (Skip-gram/CBOW + negative sampling + subsampling)** training implementation. If you'd like, I can add the missing Rust quicksort bench (e.g. as `cargo run -- bench`) so the three-way comparison actually works.
