---
audio: false
generated: true
image: false
lang: en
layout: post
title: Block Sparse Attention in LLMs
translated: false
type: note
---

## Question: What is block sparse attention in LLMs?

## Answer

**Block sparse attention** is an optimization of the Transformer attention mechanism where the model **does not compute every token-to-token attention pair**. Instead of a full `N × N` attention matrix, it computes attention only inside selected **blocks** of tokens.

The goal: reduce the quadratic cost of attention.

---

## 1. Standard attention

Normal self-attention:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d}})V
]

For a sequence of length `N`:

* `Q`: `N × d`
* `K^T`: `d × N`

so:

[
QK^T = N \times N
]

Example:

```
Sequence length: 32,768 tokens

Attention matrix:

          token
       0 1 2 3 ... 32767
0      x x x x ... x
1      x x x x ... x
2      x x x x ... x
...
32767  x x x x ... x
```

Number of attention scores:

[
32768^2 \approx 1.07B
]

Huge memory and compute.

---

## 2. Sparse attention idea

Instead of:

```
every token attends to every token

O(N²)
```

do:

```
only selected tokens attend

O(N * k)
```

where `k << N`.

Example:

```
Full attention:

A attends to:
B C D E F G H I


Sparse:

A attends to:
B C
```

---

## 3. Why "block" sparse?

A naive sparse pattern:

```
token 0 attends token 100
token 1 attends token 500
token 2 attends token 999
```

is terrible for GPUs.

GPUs love contiguous memory.

So instead we divide tokens into blocks.

Example:

Sequence:

```
tokens:

[0-63][64-127][128-191][192-255]
```

Blocks:

```
B0       B1       B2       B3
```

Instead of computing:

```
       B0 B1 B2 B3

B0     x  x  x  x
B1     x  x  x  x
B2     x  x  x  x
B3     x  x  x  x
```

compute only:

```
       B0 B1 B2 B3

B0     x  x
B1        x  x
B2           x  x
B3              x
```

The attention matrix becomes a block mask.

---

## 4. Example: Long context LLM

Suppose:

```
Context length = 1M tokens
Block size = 1024
```

Number of blocks:

```
1,000,000 / 1024 ≈ 976 blocks
```

Dense attention:

```
976 × 976 blocks
≈ 952k block operations
```

Sparse:

```
local window + global blocks

maybe only 20k block operations
```

Huge saving.

---

## 5. Common block sparse patterns

### A. Local attention

Most common.

Each token attends nearby tokens:

```
          window

<---------------->

A B C D E F G H I J

        X
        |
        v

A B C D E F G H I J
      ^^^^^
```

Used in:

* Longformer
* BigBird
* many long-context models

---

### B. Sliding window + global tokens

Example:

```
Token attends:

nearby:

[1000]
  |
  v

900 901 902 ...1100


plus:

special tokens:
<system>
<summary>
```

Good for documents.

---

### C. Retrieval/block attention

Only attend retrieved blocks:

```
Question:

"Who is Einstein?"

Retrieve:

block 3000
block 7000
block 9000

attention:

query ---> those blocks only
```

Used in:

* RAG systems
* memory architectures

---

## 6. GPU implementation view

A normal attention kernel:

```
for i in tokens:
    for j in tokens:
        score = Q[i] @ K[j]
```

Complexity:

```
N*N*d
```

Block sparse:

```
for query_block in blocks:
    for key_block in allowed_blocks:
        matmul(query_block,key_block)
```

Example:

```
allowed_blocks = {
 B0: [B0,B1],
 B1: [B0,B1,B2],
 B2: [B1,B2,B3]
}
```

The kernel skips everything else.

---

## 7. Relation to FlashAttention

Important distinction:

### FlashAttention

Does:

```
same full attention

but:
- tile computation
- avoid materializing NxN matrix
- optimize memory bandwidth
```

Complexity:

[
O(N^2)
]

but faster.

---

### Block sparse attention

Does:

```
less attention computation

skip blocks
```

Complexity:

[
O(N \times k)
]

Different idea.

They can be combined:

```
Block sparse pattern
        +
FlashAttention kernel
        =
very long context attention
```

---

## 8. Why modern LLMs don't all use it?

Because dense attention is powerful.

The problem:

Sparse attention introduces an information bottleneck.

Example:

```
Token A needs information from token Z

but sparse pattern blocks connection

A --------X-------- Z
```

The model needs multiple layers to propagate information.

Tradeoff:

| Attention        | Quality | Speed       |
| ---------------- | ------- | ----------- |
| Dense            | best    | expensive   |
| Local sparse     | good    | fast        |
| Block sparse     | good    | much faster |
| Retrieval sparse | depends | very fast   |

---

## 9. Current usage

Examples:

* Google long-context architectures explored sparse attention variants
* Microsoft Longformer introduced sliding-window + global attention
* BigScience used sparse attention ideas in BigBird

Modern frontier LLMs often combine:

```
dense attention
+
FlashAttention
+
KV cache optimization
+
MLA / GQA
+
sometimes sparse attention
```

---

For someone building/training models: **block sparse attention is basically changing the attention mask from a dense NxN matrix into a structured sparse matrix so GPU kernels can skip useless QK matmuls.** The hard part is not the math; it is designing a sparsity pattern that preserves model quality while mapping efficiently to GPU memory access.
