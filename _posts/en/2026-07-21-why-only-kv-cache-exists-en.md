---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Only KV Cache Exists
translated: false
type: note
---

Question: Why is it called **KV cache** instead of **QKV cache**? Does Q not need to be cached?

Answer:

Exactly: **Q does not need to be cached** in autoregressive generation. Only **K and V** need caching.

The reason comes from the attention equation:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d}})V
]

For each newly generated token, we create a new **Q**, but we reuse old **K/V**.

---

## Step-by-step generation

Suppose the prompt is:

```
The capital of France is
```

Tokens:

```
t1 t2 t3 t4 t5
```

At layer L:

First forward pass:

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

We save:

```
KV cache:

(k1,v1)
(k2,v2)
(k3,v3)
(k4,v4)
(k5,v5)
```

We throw away Q.

Why?

Because the next step only needs:

```
new token t6
```

Compute:

```
q6
k6
v6
```

Then attention:

```
q6 attends to:

k1 k2 k3 k4 k5 k6
v1 v2 v3 v4 v5 v6
```

The old queries:

```
q1 q2 q3 q4 q5
```

are never used again.

---

## Why old Q is useless

Imagine decoding token-by-token.

Step 6:

```
Q = q6

K = [k1,k2,k3,k4,k5,k6]

V = [v1,v2,v3,v4,v5,v6]
```

Attention:

```
softmax(q6 · K^T)V
```

Only `q6` participates.

Step 7:

```
Q = q7

K = [k1...k7]

V = [v1...v7]
```

Again:

```
q7 only
```

No operation needs:

```
q6
q5
q4
```

---

## Why K and V are special

Because previous tokens are used as **memory slots**.

Think of attention as:

```
Query:
"What information do I need?"

Keys:
"What information exists?"

Values:
"The actual information"
```

During generation:

Current token asks:

```
Q(new token)
       |
       v
search old memories

K cache
       |
       v
retrieve

V cache
```

The old tokens become a database:

```
        KV cache

token1 -> key1,value1
token2 -> key2,value2
token3 -> key3,value3
...
```

The new query is the search request.

You don't store old search requests.

---

## Training is different

During training, you do:

```
Q:
q1 q2 q3 q4 q5

K:
k1 k2 k3 k4 k5

V:
v1 v2 v3 v4 v5
```

all at once.

The attention matrix:

```
        K

       1 2 3 4 5

Q 1    x
  2    x x
  3    x x x
  4    x x x x
  5    x x x x x
```

Every Q is used once.

No cache needed.

---

## One subtle point: during training with gradient checkpointing

Sometimes people talk about "activation cache" or "attention cache", but that is a different concept.

* KV cache → inference optimization
* activation cache → training memory management
* optimizer state → training state

They are unrelated.

---

## Connection to Flash Attention API

Your code:

```python
flash_attn_with_kvcache(
    q,
    k_cache,
    v_cache,
    k,
    v
)
```

Notice:

```python
q
```

is passed directly:

```
q = current token query
```

while:

```python
k_cache
v_cache
```

are persistent.

The API design itself reflects the math:

```
new Q
 +
old K,V memory
 =
next token attention
```

So **KV cache is the mathematically correct name**. A "QKV cache" would imply storing old queries, but old queries have no future use during autoregressive decoding.
