---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sparse Attention in LLMs Explained
translated: false
type: note
---

**Question:** What is Sparse Attention in LLMs, and how does it work?

**Answer:**

In standard transformers, every token attends to every other token — this is called *full* (or *dense*) attention. For a sequence of length N, that means N² attention pairs, which becomes computationally brutal at long contexts. Sparse attention is the idea of only computing a *subset* of those pairs — letting each token attend to a carefully chosen few, not all.

Here's a diagram illustrating the contrast:The key insight is that most tokens don't need to look at all other tokens to do their job — nearby words and a few globally important positions are usually enough. Sparse attention exploits this by restricting the attention pattern.

**Main patterns used in practice:**

**Local / sliding window** — each token attends only to a fixed window of neighbors (e.g., ±128 tokens). This captures local syntax and context at O(N·w) cost. Used in Longformer.

**Strided / dilated** — tokens attend to neighbors *and* every k-th token further away. This is like having a coarse "global scan" layered on top of local attention.

**Global tokens** — a small set of special tokens (like `[CLS]` or task-relevant words) attend to *everything* and everything attends back to them. This gives the model a way to aggregate long-range information without every pair needing to connect. Also used in Longformer and BigBird.

**Random** — each token attends to a random subset of others. Theoretically sufficient for global mixing when combined with the above patterns.

**Learned / dynamic** — the model learns *which* positions to attend to, rather than using a fixed pattern. Used in Reformer (locality-sensitive hashing) and Routing Transformers.

**Why it matters:**

Full attention has O(N²) memory and compute. For a 100k-token context, that's 10 billion pairs — impossible on current hardware. Sparse attention reduces this to roughly O(N·k) where k ≪ N, enabling long-context models. This is fundamental to systems like Claude's extended context window, though modern approaches often combine sparse patterns with other tricks (FlashAttention, ring attention, etc.).

**The trade-off:** You can miss long-range dependencies that don't fall on the attended positions — which is why hybrid patterns (local + global tokens + random) tend to outperform any single pattern alone.

---

**References:**

- [Longformer: The Long-Document Transformer (Beltagy et al., 2020)](https://arxiv.org/abs/2004.05150)
- [BigBird: Transformers for Longer Sequences (Zaheer et al., 2020)](https://arxiv.org/abs/2007.14062)
- [Generating Long Sequences with Sparse Transformers (Child et al., 2019)](https://arxiv.org/abs/1904.10509)
- [Reformer: The Efficient Transformer (Kitaev et al., 2020)](https://arxiv.org/abs/2001.04451)
