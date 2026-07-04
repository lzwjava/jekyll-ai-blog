---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Dimension Split Across Heads
translated: false
type: note
---

Question: Is it correct that in multi-head attention the model dimension is split across attention heads, and it is not the batch size or token length that is split?

Answer:

Yes, your understanding is correct.

In **multi-head attention (MHA)**, the key idea is that the **hidden dimension (model dimension, (d_{model})) is split across multiple heads**, not the batch size or token length.

### 1. What gets split?

Assume:

* Input shape:
  [
  (B, T, d_{model})
  ]
  where:

  * (B) = batch size
  * (T) = token length (sequence length)
  * (d_{model}) = embedding / hidden size

In multi-head attention:

* We split **only the feature dimension**:
  [
  d_{model} \rightarrow h \times d_{head}
  ]
  where:

  * (h) = number of heads
  * (d_{head} = d_{model} / h)

So each head works on a **smaller vector per token**.

---

### 2. What does NOT get split?

* ❌ Batch size (B): stays the same
* ❌ Token length (T): stays the same

Each token still attends over all tokens in the sequence.

---

### 3. What actually happens internally?

For each head:

1. You project input into Q, K, V:
   [
   Q, K, V \in (B, T, d_{head})
   ]
2. Each head computes attention independently:
   [
   Attention(Q, K, V)
   ]
3. Then concatenate all heads:
   [
   (B, T, h \cdot d_{head}) = (B, T, d_{model})
   ]
4. Final linear projection mixes them back.

---

### 4. Intuition

Think of it like:

* Each token is described by a **big vector**
* Multi-head attention splits that vector into **multiple “sub-spaces”**
* Each head learns a different type of relationship:

  * syntax
  * long-range dependency
  * positional patterns
  * semantic similarity, etc.

---

### 5. Key takeaway

* ✔ Split: **feature dimension (embedding space)**
* ✘ Not split: batch size or sequence length
* ✔ Each head sees the full sequence, just in a lower-dimensional representation

---

If you want, I can also draw the exact tensor shape flow (step-by-step like PyTorch `view/reshape/transpose`) so you can see how it is implemented in code.
