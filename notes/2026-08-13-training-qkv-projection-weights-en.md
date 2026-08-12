---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training QKV Projection Weights
translated: false
type: note
---

Question: How are Q, K, V shapes and weights (`Wq`, `Wk`, `Wv`) trained in Transformer attention?

Answer:

Yes, your understanding is basically correct. Let's walk through the actual forward pass.

Assume GPT-style Transformer:

```
hidden_size = 768
num_heads = 12
head_dim = 64

12 * 64 = 768
```

The input hidden states:

```
X shape = [sequence_length, hidden_size]

X = [T, 768]
```

For example, after token embedding + previous layers, one token has:

```
x = [768]
```

---

### 1. Q projection

The model has a learned matrix:

```
Wq = [768, 768]
```

This is created during initialization and learned during training.

Forward:

```
Q = X @ Wq
```

Shape:

```
[T,768] @ [768,768]

= [T,768]
```

So Q still has hidden_size dimension.

Then split into heads:

```
Q -> [T, 12, 64]
```

or:

```
q1 = [T,64]
q2 = [T,64]
...
q12 = [T,64]
```

Each head has its own slice of Q.

---

### 2. K projection

Same idea:

Learned:

```
Wk = [768,768]
```

Forward:

```
K = X @ Wk
```

Result:

```
K = [T,768]
```

Split:

```
K -> [T,12,64]
```

---

### 3. V projection

Same:

Learned:

```
Wv = [768,768]
```

Forward:

```
V = X @ Wv
```

Result:

```
V = [T,768]
```

Split:

```
V -> [T,12,64]
```

---

### 4. Attention

For one head:

Query:

```
q = [T,64]
```

Key:

```
k = [T,64]
```

Compute similarity:

```
scores = q @ k.T / sqrt(64)
```

Shape:

```
[T,64] @ [64,T]

= [T,T]
```

This gives:

```
token i attends to token j
```

Then:

```
attention = softmax(scores)
```

Finally:

```
output = attention @ v
```

where:

```
attention = [T,T]

v = [T,64]
```

so:

```
[T,T] @ [T,64]

= [T,64]
```

Combine 12 heads:

```
12 * 64 = 768
```

back to:

```
[T,768]
```

---

### Are Wq, Wk, Wv trained?

Yes.

They are ordinary neural network parameters.

During training:

```
loss
 |
backprop
 |
grad(Wq)
grad(Wk)
grad(Wv)
 |
optimizer update
```

For example AdamW:

```
Wq = Wq - learning_rate * Adam(gradient)
```

The model learns:

* `Wq`: what kind of information should become a query
* `Wk`: what features should be searchable/matchable
* `Wv`: what information should be retrieved

---

A useful mental model:

```
hidden state x
      |
      |
      +---- Wq ---> query space
      |
      +---- Wk ---> key space
      |
      +---- Wv ---> value space
```

`Wq`, `Wk`, `Wv` are three different learned projections of the same hidden representation.

They start random, and billions of examples train them into useful transformations.

One subtle point: although Q/K/V come from the same `X`, they are **not the same semantic space** after projection:

```
Q = XWq
K = XWk
V = XWv
```

because:

```
Wq != Wk != Wv
```

The model learns different coordinate systems for:

* asking a question (Q)
* matching a question (K)
* providing information (V)

This is why attention becomes a **data-dependent linear layer**: the matrices `Wq/Wk/Wv` are fixed after training, but the generated attention matrix:

```
softmax(QK^T)
```

changes for every input sequence.
