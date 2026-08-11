---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hidden_size in Transformer attention
translated: false
type: note
---

Question: What does `hidden_size` mean in my friend's explanation about Wq/Wk and MLA?

Answer:

`hidden_size` means the **dimension of the hidden state vector `x` inside the Transformer**.

In:

```python
q = x Wq
```

`x` has size:

```
x ∈ R^(hidden_size)
```

So if:

```
hidden_size = 4096
```

then one token is represented as:

```
x =
[
 0.12,
-0.31,
 0.55,
 ...
 0.88
]

length = 4096
```

This 4096-dimensional vector is the model's internal representation of that token.

---

Example with Llama-like model:

Suppose:

```
hidden_size = 4096
num_heads = 32
head_dim = 128
```

Because:

```
32 heads × 128 dimensions/head = 4096
```

The model keeps the same hidden dimension through layers:

```
Token
 |
Embedding
 |
4096-dim hidden state
 |
Transformer block
 |
4096-dim hidden state
 |
Transformer block
 |
4096-dim hidden state
```

The size does not mean "4096 words" or "4096 features humans understand". It is just a learned vector space.

---

Now connect to your friend's sentence:

> Wq、Wk 都是降维运算，你合并后就是将维度升回到 hidden_size，各方面都爆增

He is talking about **head dimension vs hidden_size**.

Normally:

```
hidden_size = 4096
```

Attention splits into heads:

```
Q,K,V

4096
 |
 split
 |
32 heads

each head:
128 dimensions
```

So:

```
head_dim = hidden_size / num_heads

= 4096 / 32

= 128
```

For each head:

```
q_head = x Wq_head

4096 → 128
```

That is the "降维" (dimension reduction).

Matrix:

```
x:

[1 × 4096]


Wq_head:

[4096 × 128]


result:

[1 × 128]
```

---

But if you want to combine all heads:

```
32 heads × 128

= 4096
```

You concatenate:

```
[q1,q2,q3,...q32]

        |
        v

[1 × 4096]
```

Then output projection:

```
Wo:

4096 × 4096
```

This restores hidden_size.

---

MLA (Multi-head Latent Attention) changes this idea.

Normal KV cache:

```
K:

hidden_size

V:

hidden_size
```

For every token you store:

```
4096 + 4096

= 8192 numbers/token
```

For long context:

```
128k tokens × 8192

≈ 1 billion values
```

Memory explosion.

MLA:

Instead of:

```
x
 |
 +--> K 4096
 |
 +--> V 4096
```

it does:

```
x

↓

latent vector

512 dimensions
```

Store:

```
512 numbers/token
```

Later reconstruct K/V.

So your friend's point:

```
先降低维度（latent），然后才考虑合并
```

means:

First compress:

```
4096 → 512
```

then do attention-related operations.

Instead of:

```
4096 → many heads → merge back 4096
```

which creates huge KV cache.

---

A good mental model:

```
hidden_size
=
the width of the model's brain state

For GPT-3:
hidden_size = 12288

For Llama 3 8B:
hidden_size = 4096

For larger models:
hidden_size can be 8192, 16384, etc.
```

Everything inside the Transformer revolves around this dimension:

```
x:

[hidden_size]


Wq/Wk/Wv:

hidden_size → attention dimensions


MLP:

hidden_size → larger intermediate dimension → hidden_size
```

So when your friend says "升回 hidden_size", he means **bringing compressed attention representations back to the model's main internal vector width (for example 4096 dimensions).**