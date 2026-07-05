---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sparse Attention in Transformers
translated: false
type: note
---

Question: What is sparse attention?

Answer:

**Sparse attention** is an optimization technique for Transformer models that reduces the amount of attention computation by allowing each token to attend to only a **subset** of other tokens, instead of every token in the sequence.

### Why is sparse attention needed?

In the original Transformer, every token attends to every other token.

If the sequence length is (n), the attention matrix has size:

[
n \times n
]

So the computational complexity is:

* **Time:** (O(n^2))
* **Memory:** (O(n^2))

For example:

| Sequence length | Attention matrix size |
| --------------: | --------------------: |
|           1,024 |    ~1 million entries |
|           8,192 |   ~67 million entries |
|          32,768 |    ~1 billion entries |

This quadratic growth becomes very expensive for long-context LLMs.

---

## Dense attention (standard attention)

Suppose we have 8 tokens:

```
A B C D E F G H
```

Every token attends to every token:

```
      A B C D E F G H
A ->  ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
B ->  ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
C ->  ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓
...
```

This is called **dense attention**.

---

## Sparse attention

Instead, each token attends only to selected tokens.

For example:

```
A -> A B
B -> A B C
C -> B C D
D -> C D E
E -> D E F
...
```

Now each token attends to only a few neighbors.

The complexity becomes roughly

[
O(nk)
]

where (k) is the number of attended tokens per query, often much smaller than (n).

If (k) is fixed (e.g., 64 or 128), the complexity is approximately **linear** in the sequence length.

---

## Common sparse attention patterns

### 1. Sliding window attention

Each token attends only to nearby tokens.

```
Token 5

1 2 3 4 [5] 6 7 8 9

Attend:

3 4 5 6 7
```

This works well because nearby words often carry the most relevant information.

Many long-context models use this approach.

---

### 2. Global attention

Some special tokens attend to all tokens.

Example:

```
[CLS] sentence words ...
```

The `[CLS]` token can see the entire sequence, while ordinary tokens use local attention.

This is useful for tasks like classification.

---

### 3. Strided attention

Each token attends at regular intervals.

Example:

```
Token 20

Attend:

4
8
12
16
20
24
28
```

This helps capture long-range dependencies without attending everywhere.

---

### 4. Block sparse attention

Divide the sequence into blocks.

```
Block1 Block2 Block3 Block4

█ █ . .
█ █ . .
. . █ █
. . █ █
```

Only selected blocks interact.

This is efficient on GPUs because it operates on larger matrix blocks.

---

## Why does sparse attention still work?

Natural language exhibits strong locality.

For example:

> The cat that was sleeping on the sofa woke up.

To predict "woke," the most important tokens are usually nearby:

* cat
* sleeping
* sofa

Far-away tokens often contribute much less.

Sparse attention exploits this observation.

---

## Limitations

Sparse attention can miss important long-range relationships.

For example:

```
The answer is ...

(20,000 tokens later)

... therefore the answer is 42.
```

If the model cannot connect these distant tokens, it may lose important context.

Modern long-context models often combine sparse attention with mechanisms that preserve long-range information.

---

## Relation to modern LLMs

Many recent long-context models use more advanced alternatives or combinations:

* Longformer: sliding-window attention with global tokens.
* BigBird: combines local, random, and global attention, with theoretical guarantees similar to full attention.
* FlashAttention: **not sparse**. It computes the exact dense attention more efficiently by optimizing GPU memory access.
* FlashAttention-2: a faster implementation of dense attention.
* vLLM: primarily optimizes inference through techniques such as PagedAttention for KV-cache management; it does not rely on sparse attention for its core optimization.

### Sparse attention vs. FlashAttention

| Feature                       | Sparse Attention                            | FlashAttention                                             |
| ----------------------------- | ------------------------------------------- | ---------------------------------------------------------- |
| Computes all attention pairs? | No                                          | Yes                                                        |
| Mathematical result           | Approximate (depends on sparsity pattern)   | Exact                                                      |
| Complexity                    | Often (O(n)) or (O(n \log n))               | (O(n^2))                                                   |
| Main goal                     | Reduce the number of attention computations | Make dense attention much faster and more memory-efficient |
| Best for                      | Very long contexts                          | Efficient training and inference with standard attention   |

In short, **sparse attention changes *which* tokens can attend to each other**, while **FlashAttention changes *how* the same dense attention is computed**. These techniques address different bottlenecks and can even be used together in some systems.
