---
audio: false
generated: true
image: false
lang: en
layout: post
title: Squeeze Existing Resources First
translated: false
type: note
---

Question: Is it a good strategy to start by fully utilizing existing device resources to learn as much as possible (e.g., mastering computer fundamentals, which already requires significant effort), and then progressively expand into areas like GPU programming?

Answer: Yes, that's actually a very sound and practical approach. Here's why it works well:

**Why "squeeze existing resources first" makes sense:**

- **Depth before breadth** — truly understanding how a CPU, memory, OS, and compiler work together is non-trivial. Most people underestimate how deep this rabbit hole goes (caching, branch prediction, syscalls, threading, etc.).
- **Strong foundation transfers** — everything you learn on a CPU/general system directly informs GPU work. GPU programming (CUDA, ROCm) is essentially "what if we had 10,000 weaker CPU cores and had to think about memory very carefully?" — concepts like memory hierarchy, parallelism, and latency are shared.
- **Cost-efficient** — GPUs (especially cloud GPU time) are expensive. Getting sharp on a laptop/desktop first means you waste less expensive GPU time on beginner mistakes.
- **Avoids premature complexity** — jumping to GPU before understanding memory models or parallelism leads to confusion that's hard to untangle.

**A rough progression that fits your plan:**

| Stage | Focus | Example Tools |
| --- | --- | --- |
| 1 | Programming fundamentals + algorithms | Python, C, any CPU |
| 2 | Computer systems (OS, memory, networking) | Your existing machine |
| 3 | Performance & profiling | `perf`, `valgrind`, flame graphs |
| 4 | Parallelism on CPU | multithreading, SIMD |
| 5 | GPU basics | CUDA/ROCm, Google Colab (free GPU) |
| 6 | Deep learning / HPC | PyTorch, distributed systems |

**Key insight:** The jump from Stage 4 → 5 feels much smaller once you've really wrestled with CPU-level parallelism. Many people skip to GPU too early and find it mystifying.

So yes — your instinct is right. Mastering the machine in front of you is not "settling for less," it's building the mental model that makes everything harder come naturally later.
