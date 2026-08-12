---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data-Dependent Linear Layers in Attention
translated: false
type: note
---

Question: How to understand the idea that **Transformer QKV is a data-dependent linear layer**, and why many improvements are about changing static operations into data-dependent ones?

Answer:

The key idea from your friend's comment is:

> Normal neural network layers use **fixed weights**. Attention creates a layer where the effective weights are **generated from the input itself**.

That is the conceptual jump.

---

## 1. Start from a normal linear layer

A normal linear layer:

[
y = Wx
]

Example:

```
x: input vector
W: learned matrix (fixed after training)
y: output vector
```

During inference:

```
same W
+
different x
=
different y
```

But **W never changes**.

This is a **static linear transformation**.

Example:

```
W =
[0.2 0.5
 0.1 0.8]

x1 -> W x1
x2 -> W x2
```

The transformation rule is fixed.

---

## 2. Attention turns this into data-dependent linear

Self-attention:

Input:

[
X \in R^{n \times d}
]

n = sequence length
d = hidden size

For every token:

```
token embedding
      |
      |
      +---- Wq ---> Q
      |
      +---- Wk ---> K
      |
      +---- Wv ---> V
```

Mathematically:

[
Q=XW_Q
]

[
K=XW_K
]

[
V=XW_V
]

At this point:

* Wq/Wk/Wv are still static
* they are ordinary linear layers

The magic happens here:

[
Attention(Q,K,V)
================

softmax(\frac{QK^T}{\sqrt d})V
]

---

## 3. The important matrix: QKᵀ

Look at:

[
A = softmax(QK^T)
]

A shape:

```
sequence x sequence
```

Example:

5 tokens:

```
       token1 token2 token3 token4 token5

token1 0.1    0.7    0.1    0.05   0.05
token2 0.2    0.1    0.6    0.05   0.05
token3 0.1    0.1    0.1    0.6    0.1
...
```

This matrix says:

"for this input, how much should each token look at other tokens?"

Important:

This matrix is different for every sentence.

Example:

Input A:

```
"The cat ate fish"
```

creates:

```
A1
```

Input B:

```
"The dog chased ball"
```

creates:

```
A2
```

because Q and K changed.

So:

[
A=f(X)
]

The attention matrix is **a function of input**.

---

## 4. Why call it data-dependent linear?

The final operation:

[
Y=AV
]

looks like a linear layer.

Because:

```
output = matrix × value
```

But:

```
A is not fixed
```

A comes from:

```
input
 |
Q,K
 |
QK^T
 |
softmax
 |
A
```

So actually:

[
Y=A(X)V
]

or:

[
Y=f(X)XW_V
]

The weights are generated dynamically.

A normal layer:

```
input
 |
fixed W
 |
output
```

Attention:

```
input
 |
generate W(input)
 |
output
```

That is the core idea.

---

## 5. Causal mask

Causal attention adds:

```
token i cannot see future tokens
```

Without mask:

```
       1 2 3 4

1      ✓ ✓ ✓ ✓
2      ✓ ✓ ✓ ✓
3      ✓ ✓ ✓ ✓
4      ✓ ✓ ✓ ✓
```

With causal mask:

```
       1 2 3 4

1      ✓ x x x
2      ✓ ✓ x x
3      ✓ ✓ ✓ x
4      ✓ ✓ ✓ ✓
```

Implementation:

Before softmax:

```python
scores = Q @ K.T

scores = scores.masked_fill(
    future_positions,
    -inf
)

weights = softmax(scores)
```

Why `-inf`?

Because:

[
softmax(-\infty)=0
]

So future tokens get zero attention.

---

## 6. Why your friend mentions ALiBi, RoPE, etc

The broader trend:

> Replace fixed/static behavior with input-dependent behavior.

Examples:

### Traditional positional embedding

Static:

```
position 1 -> vector A
position 2 -> vector B
```

The position information is fixed.

---

### ALiBi

Adds dynamic bias:

[
score=qk^T + m(i-j)
]

The distance changes the attention score.

---

### RoPE

Rotates Q and K depending on position:

[
Q'=R_\theta Q
]

[
K'=R_\theta K
]

The relationship between tokens depends on relative positions.

---

### Mixture of Experts

Normal FFN:

```
x
 |
W
 |
output
```

MoE:

```
x
 |
router(x)
 |
choose experts
 |
output
```

The network chooses different parameters depending on input.

Again:

static → data-dependent.

---

## 7. A very simple mental model

Think of a normal neural network as:

```
A fixed machine:

input ---> [machine] ---> output
```

Transformer attention:

```
input
 |
 |
build a machine for this input
 |
 |
[input-specific machine]
 |
output
```

The transformer does not only compute.

It **constructs a temporary computation graph based on the data**.

That is why attention was such a fundamental change.

---

For understanding QKV, the minimum things to hold:

1. **Q = what this token is looking for**
2. **K = what this token offers for matching**
3. **QKᵀ = dynamically generated routing matrix**
4. **V = information to move**
5. **Attention = input-dependent linear layer**

Once you see `QKᵀ` as a dynamically generated weight matrix, most Transformer variants become much easier to understand.
