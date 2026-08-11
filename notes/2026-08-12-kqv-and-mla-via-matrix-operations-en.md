---
audio: false
generated: true
image: false
lang: en
layout: post
title: K/Q/V and MLA via Matrix Operations
translated: false
type: note
---

Question: How to understand K/Q/V and MLA in LLMs using matrix operations?

Answer:

The easiest way to understand attention is: **every token is a vector, and K/Q/V are just different linear projections of that vector.**

Start from the Transformer hidden state:

```
x ∈ R^d_model
```

For example:

```
d_model = 4096
```

A token after embedding + previous layers becomes:

```
x = [0.12, -0.31, ..., 0.88]   # 4096 dimensions
```

Then attention creates three views:

```
Q = x Wq
K = x Wk
V = x Wv
```

where:

```
Wq ∈ R^(4096 × 4096)
Wk ∈ R^(4096 × 4096)
Wv ∈ R^(4096 × 4096)
```

The matrix multiplication is just a learned coordinate transformation:

genui{"linear_algebra_optimization":{"type_id":"MATRIX_MULTIPLICATION_ROW_COLUMN_RULE"}}

---

## 1. What does Q mean?

Query = "what am I looking for?"

Example:

Sentence:

```
The cat sat on the mat because it was tired.
```

When processing "it":

The query vector might encode:

```
I need to find:
- an animal/person
- previous subject
- something compatible with "tired"
```

Mathematically:

```
q = x Wq
```

The Wq matrix learns:

```
hidden space
     |
     |
     v

query space
```

It extracts features useful for searching.

---

## 2. What does K mean?

Key = "what information do I contain?"

Each previous token also creates:

```
k_i = x_i Wk
```

For example:

```
cat:

k_cat = [0.2, 0.7, ...]


mat:

k_mat = [-0.1,0.3,...]
```

The query compares with keys:

```
score = q · k
```

Usually:

```
Attention score:

QK^T / sqrt(d)
```

Matrix form:

```
Q: [sequence, d]

K: [sequence, d]


QK^T:

[sequence,d] × [d,sequence]

=

[sequence,sequence]
```

Example:

10 tokens:

```
        token1 token2 token3 ...

token1    0.1    0.2    0.9
token2    0.3    0.1    0.4
token3    0.8    0.2    0.1
```

This is the attention map.

---

## 3. What is V?

Value = actual information to retrieve.

```
v_i = x_i Wv
```

After attention:

```
output = softmax(QK^T)V
```

Meaning:

1. QK^T decides:

"look at which tokens?"

2. V provides:

"what information to copy?"

Example:

```
Query: "it"

Attention:

cat    0.8
mat    0.1
was    0.1


output:

0.8 * V(cat)
+
0.1 * V(mat)
+
0.1 * V(was)
```

It is a weighted sum.

---

# Why does MLA (Multi-head Latent Attention) exist?

Your friend's point:

> Wq, Wk are dimensionality reduction operations, but merging later explodes dimension.

Let's look at normal multi-head attention.

Suppose:

```
hidden_size = 4096

heads = 32

head_dim = 128
```

Normally:

```
Q:

4096 → 4096


K:

4096 → 4096


V:

4096 → 4096
```

because:

```
32 heads × 128 dim = 4096
```

During inference, every previous token needs KV cache:

```
KV cache:

sequence_length × heads × head_dim × 2
```

Example:

```
context = 128k tokens

KV:

128000 × 32 × 128 × 2

≈ 1 billion floats
```

Huge memory.

---

# MLA idea (DeepSeek)

MLA says:

Instead of storing:

```
K:

4096 dimensions

V:

4096 dimensions
```

compress first.

Example:

```
hidden

4096

 |
 |  W_down

 v

latent

512
```

Store:

```
latent KV cache:

512 dimensions
```

Then reconstruct when needed:

```
latent

512

 |
 | W_up

 v

K,V
```

So:

Old:

```
token
 |
 +--> K 4096
 |
 +--> V 4096


cache = 8192
```

MLA:

```
token

 |
 v

latent 512


cache = 512
```

Huge reduction.

---

# Matrix view of the whole attention block

Normal attention:

```
X

↓

Q = XWq
K = XWk
V = XWv


Attention:

softmax(QK^T)V


↓

output
```

MLA:

```
X

↓

latent = XC


cache latent


when decoding:


latent

↓

K,V reconstruction


Attention
```

The key insight:

**Transformer is mostly matrix multiplication.**

The intelligence comes from learning the matrices:

```
Wq
Wk
Wv
Wo
```

They learn different coordinate systems.

A useful mental model:

```
hidden space
      |
      |
      +---- Wq ---> "what do I want?"
      |
      +---- Wk ---> "what do I have?"
      |
      +---- Wv ---> "what information do I carry?"
```

MLA is basically asking:

> "Can we find a smaller latent space that preserves the useful information for attention, instead of storing huge K/V matrices?"

That is why it saves inference memory, especially for long-context models.