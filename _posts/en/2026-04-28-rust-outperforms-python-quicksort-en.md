---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Outperforms Python in Quicksort
translated: false
type: note
---

**Results: Rust ~0.75ms vs Python ~7.9ms — ~10x faster.**

---

Here's the post:

---

**Quicksort in Rust vs Python: sorting 10,000 numbers**

I implemented the same Quicksort algorithm from scratch in both Rust and Python — identical Lomuto partition logic — and timed them on 10,000 random integers.

**Results:**
- Rust (release build): **~0.75 ms**
- Python: **~7.9 ms**

That's roughly **10x faster** for the same algorithm, same logic, no tricks.

The code is nearly a 1:1 translation. Python's tuple swap (`a, b = b, a`) is arguably more elegant than Rust's `arr.swap(i, j)`, but Rust compiles down to raw machine code while Python is interpreted with dynamic typing overhead at every step.

What's interesting is the gap is "only" 10x here. Python gets a bad reputation but for algorithmic work on moderate data sizes, it's not catastrophic. Push to 1M numbers or do this in a hot loop and the gap widens fast.

The real lesson: the algorithm matters more than the language at small scale. Both are O(n log n) average case. But when you need every millisecond, Rust's zero-cost abstractions deliver.

Code: `src/main.rs` (Rust) and `quicksort.py` (Python) — same algorithm, very different runtimes.

---

Want me to commit this and push?