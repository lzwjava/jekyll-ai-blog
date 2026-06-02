---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Hardware Parallelism Accelerates Array Indexing
translated: false
type: note
---

### Why is Indexing Faster Than Binary Search?

This 2013 blog post by Yin Wang (王寅) dives into the fundamental reason why direct array indexing (e.g., `arr[i]`) is constant time O(1), while binary search on a sorted array takes O(log n) time. He breaks it down at the hardware level using a simple circuit analogy, showing that indexing isn't "magic"—it's just a massively parallel binary search baked into the computer's addressing system.

#### Key Explanation
- **The Core Idea**: Array indexing uses an **addressing circuit** to select a memory location directly from an address (like an index). For a tiny example with 4 memory locations (W, X, Y, Z) and a 2-bit address (bits A and B):
  - Each address bit acts like one step of a binary search, halving the possible selections.
  - Bit A decides between two groups: {W, X} or {Y, Z}.
  - Bit B decides between another split: {W, Y} or {X, Z}.
  - These bits don't run sequentially—they operate **in parallel** using AND gates and wires to combine signals and light up exactly one output (e.g., if A=0, B=1 → select W).

  This mimics 2 steps of binary search (log₂(4) = 2) but completes in a single hardware "tick" because everything happens simultaneously.

- **Scaling Up**: For a full n-bit address (handling 2ⁿ elements), the circuit runs all log₂(n) binary search steps in parallel. That's why it's O(1): the hardware does the "search" instantly, without looping or comparisons in software.

- **Visual Aid**: The post includes a diagram of the circuit with inverters, wires, and AND gates showing signal flow. No code snippets, but it's conceptual—think of it as a decoder turning binary addresses into one-hot selection.

#### Why This Matters
Wang argues this reveals how low-level hardware optimizations make high-level operations feel effortless. Binary search is "slow" only because it simulates this circuit sequentially in software; the CPU's real memory access is the parallel version.

It's a short, insightful read for anyone curious about CS fundamentals beyond big-O notation.

[Why is indexing faster than binary search](https://yinwang0.wordpress.com/2013/04/02/indexing/)
