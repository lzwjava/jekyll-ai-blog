---
audio: false
generated: true
image: false
lang: en
layout: post
title: Current Token Hidden State
translated: false
type: note
---

Question: What does `x` mean in `q = xWq`?

Answer:

`x` is the **current token's hidden state vector** (the representation produced by previous Transformer layers).

Think of a Transformer layer as:

```
input tokens
      |
      v
embedding
      |
      v
Transformer block 1
      |
      v
Transformer block 2
      |
      v
...
      |
      v
current layer input x
```

At the attention layer, `x` is the data entering the attention module.

---

Example:

Suppose:

```
hidden_size = 4096
```

A token "cat" is represented as:

```
x =
[
 0.12,
-0.31,
 0.55,
 ...
 0.88
]
```

It has 4096 numbers:

```
x ∈ R^4096
```

You can think of it as:

```
cat

↓ embedding + previous layers

[meaning dimensions]
[
  animal-related feature,
  grammar feature,
  context feature,
  position feature,
  ...
]
```

The dimensions are not human-readable, but the network learns useful directions.

---

Then:

```
q = x Wq
```

means:

```
[1 × 4096] × [4096 × 4096]

=

[1 × 4096]
```

Example:

```
x:

1 × 4096


Wq:

4096 × 4096


q:

1 × 4096
```

The matrix `Wq` transforms the generic hidden representation into a **query representation**.

---

A concrete analogy:

Imagine `x` is a person's profile:

```
x:

age
height
income
education
interests
location
...
```

Different companies create different projections:

```
Wq:

"What kind of person am I looking for?"


Wk:

"What kind of person am I?"


Wv:

"What information do I provide?"
```

Same person:

```
x
 |
 +---- Wq ---> query vector
 |
 +---- Wk ---> key vector
 |
 +---- Wv ---> value vector
```

---

For a whole sentence:

```
"The cat sat on the mat"
```

we have many x's:

```
X =

token1 hidden vector
token2 hidden vector
token3 hidden vector
...
token6 hidden vector
```

Matrix form:

```
X:

[6 × 4096]
```

Then:

```
Q = XWq
K = XWk
V = XWv
```

becomes:

```
[6×4096] × [4096×4096]

=

[6×4096]
```

Now every token has its own Q/K/V.

Then attention:

```
Attention = softmax(QKᵀ / sqrt(d))V
```

The important mental model:

```
x = "what this token currently understands"

Wq = learn a way to ask questions

Wk = learn a way to be searched

Wv = learn what information to send
```

The whole Transformer is repeatedly changing `x`.

Layer 1:

```
x0 → x1
```

Layer 2:

```
x1 → x2
```

...

Final layer:

```
xN → next token prediction
```

So `x` is not the word itself. It is the **learned internal state of that token at that point in the network**.