---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Word2vec Implementation Details
translated: false
type: note
---

Here's the full technical breakdown:

---

**Architecture: Skip-gram + CBOW with Negative Sampling**

Faithful port of Mikolov's original C word2vec. Two model architectures (Skip-gram predicts center→context, CBOW averages context→center) trained with Negative Sampling (N noise samples per positive pair, sigmoid cross-entropy loss). No softmax, no hierarchical softmax — just the SGNS variant that became dominant.

**Vocabulary builder**

Read corpus → count word frequencies (lowercased) → filter by `min_count` → sort by frequency descending → assign indices. Stores as parallel `Vec<String>`, `Vec<u64>` counts, `HashMap<String, usize>` for lookup. The sorted order matters for the negative sampling table.

**Negative sampling table**

Pre-computed 100M-entry table where entry `i` maps to word index proportional to `count^0.75`. Built by cumulative distribution: for each word, compute `count^0.75 / sum`, walk through the table filling entries. The `^0.75` smoothing (vs raw frequency) prevents common words from dominating negative samples — same trick as the original. Indexed via `(rng >> 16) % TABLE_SIZE` (upper bits of LCG are more uniformly distributed than lower bits, matching the original C code's bit shift).

**Sigmoid approximation**

Pre-computed lookup table of 1000 entries covering `[-MAX_EXP, MAX_EXP]`. `sigmoid(x) = table[((x + 6.0) / 12.0) * 1000]`. Avoids `exp()` in the hot loop — the original does the same.

**Subsampling of frequent words**

Original formula: `ran = (sqrt(f/t) + 1) * (t/f)` where `f = count/total`, `t = threshold`. If `ran < random_uniform`, discard the word. This down-samples frequent words ("the", "a") while keeping rare words intact. Matches the exact formula from the original C code, not the simplified `1 - sqrt(t/f)` often cited in tutorials.

**Dynamic window reduction**

Each word position: `b = rng % window`, then context ranges from `[pos - window + b, pos + window - b]`. So effective window is `window - b` on each side (uniformly random from 1 to `window`). This gives more diverse context sizes per word — the original does this, not a fixed window.

**LCG PRNG**

`next_random = next_random * 25214903917 + 11` — Park-Miller LCG matching the original C code exactly. Thread-local state (no shared RNG, no locking). The same seed sequence means reproducible results with single-threaded mode.

**Single-threaded training path**

Corpus read into memory as `&[u8]`, split by `\n` and space. Each word lowercased, looked up in HashMap, subsampled, accumulated into sentence buffer (max 1000 words). When buffer full, train on it. Learning rate linearly decays from `lr0` to `lr0 * 0.0001` based on `word_count / total_target`. Exact same loop structure as the original.

**Multi-threaded training: TrainPtrs**

The core Rust challenge. `std::thread::scope::spawn` requires `F: Send`. Raw pointers (`*mut f32`) are `!Send`. Solutions tried:

1. `SendPtr<T>(*mut T)` + `unsafe impl Send` — struct IS Send, but Rust's closure auto-destructuring breaks it: `move || { let x = ptr.0; }` makes the closure capture `*mut f32` (not `SendPtr`), because `Copy` structs get destructured by the compiler when you access fields inside a `move` closure.

2. Extract `.0` before the closure — captures raw pointer directly, same problem.

3. **Working solution:** `TrainPtrs` struct with `unsafe impl Send + Copy`. Don't access `.0` inside the closure. Instead, add a `run()` method and `word_count()` method on `TrainPtrs`. The closure captures `TrainPtrs` (which is `Send`), and calls methods on it. The raw pointer only exists inside the method body (not captured). The compiler sees the captured type as `TrainPtrs`, not `*mut f32`.

**Multi-threaded training: corpus splitting**

Corpus loaded into memory once as `Vec<u8>`. Split into `N` byte ranges (one per thread). Each thread starts at a word boundary (scan forward to next space/newline). Threads process their chunk independently — no sentence boundary coordination needed.

**Multi-threaded training: weight sharing**

All threads share `syn0` (input embeddings) and `syn1` (output embeddings) via raw pointers. This is a deliberate data race — same as the original C code with pthreads. Float writes are atomic at the hardware level on ARM/x86 (32-bit aligned writes). Some gradient updates get lost, but SGD is robust to this noise. No locks, no atomics, no contention.

**Multi-threaded training: epoch loop**

The parallel path was initially missing the epoch loop (single-threaded had it). Added `for epoch in 0..cfg.epochs { ... }` around the `std::thread::scope`. Each epoch re-spawns threads, processes the full corpus again. Per-epoch learning rate decay.

**Multi-threaded training: vocab lookup per thread**

Threads can't access `HashMap` (not `Send` when borrowed from `&mut self`). Solution: pre-build a sorted `Vec<(Vec<u8>, usize)>` (lowercase word bytes → vocab index) before spawning threads. Each thread does `binary_search_by` on this sorted array. For 71k words, this is ~17 comparisons per word — fast enough that it's not the bottleneck.

**Raw pointer training functions**

`train_sg_raw` and `train_cbow_raw` are standalone functions (not methods on `Model`) that accept raw pointers. They replicate the exact gradient update logic:
- For each context word (Skip-gram) or averaged context (CBOW):
  - Positive sample: target=center word, label=1
  - N negative samples: target=neg_table[sample], label=0
  - `f = dot(syn0[input], syn1[target])`
  - `g = (label - sigmoid(f)) * alpha`
  - `neu1e += g * syn1[target]` (accumulate error for input)
  - `syn1[target] += g * syn0[input]` (update output)
  - After all samples: `syn0[input] += neu1e` (update input)

**Vector similarity (post-training)**

`Vectors::load` reads both text and binary formats (auto-detects via null byte presence). L2-normalizes all vectors on load. `most_similar` does brute-force cosine scan. `analogy` computes `vec(a) - vec(b) + vec(c)`, normalizes, finds nearest (excluding a, b, c). Both support interactive REPL mode.

**File format**

Binary (default): `vocab_size dim\n` header, then `word\0<float32_le × dim>` per line. Text: `word f0 f1 ...\n` per line. Both compatible with the original C word2vec output format — can load vectors trained by the C tool and vice versa.

**CLI structure**

Integrated as `ll word2vec <subcommand>` in the existing `ll` project. Subcommands: `train`, `distance`, `analogy`, `accuracy`. Args use `-flag value` style matching the original (not `--flag=value`).
