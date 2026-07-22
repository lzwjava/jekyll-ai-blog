---
audio: false
generated: true
image: false
lang: en
layout: post
title: FlashAttention vs Sparse Attention
translated: false
type: note
---

Question: Is your friend's explanation of FlashAttention vs. Sparse Attention correct? Specifically, is FlashAttention's advantage that you don't need to squeeze all attention scores into memory, so computation stays efficient without constantly moving data?

Answer:

Yes. Your friend's explanation is fundamentally correct.

The key point is:

> **FlashAttention is a memory optimization. Sparse Attention is an algorithmic optimization.**

People often confuse them because both make attention faster.

### Standard Attention

Suppose

* Sequence length = (N)
* Head dimension = (d)

Normal attention computes

[
QK^T \rightarrow \text{Softmax} \rightarrow V
]

The expensive part is the **(N \times N)** attention matrix.

The usual implementation is

```
QK^T
 ↓
store N×N matrix to HBM (GPU memory)
 ↓
read it back
 ↓
softmax
 ↓
write again
 ↓
read again
 ↓
multiply V
```

So there is a huge amount of GPU memory traffic.

The bottleneck is often **HBM bandwidth**, not FLOPs.

---

### FlashAttention

FlashAttention computes exactly the same mathematical result.

It **does NOT reduce the amount of attention computation.**

Instead, it changes **how** the computation is scheduled.

It splits Q/K/V into tiles.

```
Q block

        K block
           │
           ▼

compute partial QK
↓
compute local max
↓
compute local exp sum
↓
discard temporary scores
↓
move to next tile
```

Instead of materializing the whole (N \times N) matrix, it only keeps a small tile in fast **SRAM/shared memory**.

So your friend said:

> "不用把所有部分都挤进来也可以算"

That is essentially correct.

You never need the full attention matrix resident in memory.

---

### Why "local max + compensation"?

Softmax needs

[
\frac{e^{x_i}}{\sum_j e^{x_j}}
]

If you process tiles separately, you don't know the global maximum or denominator.

FlashAttention keeps running statistics.

For each tile:

```
running_max
running_sum_exp
running_output
```

When a larger maximum appears,

```
old_sum *= exp(old_max - new_max)

new_sum += exp(tile - new_max)
```

This is the "补量 (compensation)" your friend mentioned.

It guarantees that the final output is **numerically identical** (up to floating-point rounding) to ordinary softmax.

---

### Sparse Attention

Sparse Attention is a different idea.

Instead of

```
every token
    ↓
attends every other token
```

you explicitly remove many attention connections.

Example:

```
████████████

↓

██··········
·██·········
··██········
```

Now complexity becomes

* dense

[
O(N^2)
]

* sparse

[
O(Nk)
]

where (k \ll N).

So Sparse Attention **reduces the number of dot products**.

FlashAttention does **not**.

---

### The comparison

|                           | FlashAttention          | Sparse Attention                     |
| ------------------------- | ----------------------- | ------------------------------------ |
| Same mathematical result? | ✅ Yes                   | ❌ No (changes the attention pattern) |
| Reduce FLOPs?             | ❌ No (roughly the same) | ✅ Yes                                |
| Reduce memory traffic?    | ✅ Huge reduction        | Sometimes                            |
| Complexity                | (O(N^2))                | Usually (O(Nk))                      |
| Main optimization         | IO / memory bandwidth   | Algorithm                            |

### One subtle correction

Your friend said:

> "不过计算量总体区别不做明显优化"

This is mostly true, but more precisely:

* **Arithmetic complexity (FLOPs)** stays about the same.
* **Memory accesses** are reduced dramatically.
* Because modern GPUs are often memory-bandwidth-bound for attention, reducing IO can produce **2–4× real speedups** even without reducing FLOPs.

So the more accurate statement is:

> FlashAttention doesn't significantly reduce the number of attention computations; it drastically reduces memory reads/writes by computing attention tile-by-tile in on-chip SRAM, avoiding materializing the full attention matrix. That's why it achieves large practical speedups.

This is exactly why the FlashAttention paper is subtitled:

> **Fast and Memory-Efficient Exact Attention with IO-Awareness**.
