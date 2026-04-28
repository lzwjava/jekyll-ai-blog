---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multilanguage Quicksort Performance Comparison
translated: false
type: note
---

**Results on 10,000 numbers:**

| Language | Time |
|----------|------|
| Rust | ~0.39 ms |
| Java | ~1.18 ms |
| Python | ~7.89 ms |

---

**Updated post:**

---

**Quicksort in Rust vs Java vs Python: sorting 10,000 numbers**

Same Lomuto partition quicksort, implemented identically in three languages:

**Results:**
- Rust (release): **~0.4 ms**
- Java (JVM): **~1.2 ms**
- Python: **~7.9 ms**

Java sits right in the middle — about 3x slower than Rust, but 6x faster than Python. That's the JVM in a nutshell: you pay JIT warmup overhead on small runs, but the bytecode compilation gets you much closer to native than an interpreter does.

Rust wins because it compiles directly to machine code with no runtime, no GC pauses, no JIT warmup. The Java result would improve significantly with a warmup loop (JIT kicks in after ~10k invocations) — in a long-running server, Java often narrows the gap.

Python's overhead is pure interpreter cost: dynamic dispatch, reference counting, and boxing every integer as a heap object.

All three are O(n log n). The algorithm is the same. The hardware is the same. The difference is entirely in how each language executes it.

---

Want me to commit and push all three files?