---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transformer Dot-Product Attention Scaling
translated: false
type: note
---

Question: How to understand why Transformer uses `1 / sqrt(d_k)` scaling in dot-product attention?

Answer:

The key idea is:

**The dot product value grows with the dimension `d_k`. Large dot products make softmax become too "confident", causing gradients to disappear. Dividing by `sqrt(d_k)` keeps the numbers in a healthy range.** ([NeurIPS Papers][1])

Let's derive it.

## 1. Attention without scaling

Transformer attention:

[
Attention(Q,K,V)=softmax(QK^T)V
]

The score between one query and one key is:

[
score=q\cdot k
]

where:

[
q,k \in R^{d_k}
]

Example:

```
q = [0.2, -0.5, 0.1]
k = [0.8,  0.3, -0.4]

q·k = 0.2*0.8 + (-0.5)*0.3 + 0.1*(-0.4)
    = -0.19
```

It is just a similarity score.

---

## 2. Why does dimension make it explode?

The dot product is:

[
q\cdot k=\sum_{i=1}^{d_k}q_i k_i
]

Assume:

[
q_i,k_i \sim N(0,1)
]

Each multiplication:

[
q_i k_i
]

has:

* mean = 0
* variance = 1

The dot product adds `d_k` independent terms:

[
Var(q\cdot k)=d_k
]

Therefore:

[
std(q\cdot k)=\sqrt{d_k}
]

This is the important part.

The typical magnitude grows as:

[
|q\cdot k|\approx \sqrt{d_k}
]

The paper mentions exactly this variance argument. ([NeurIPS Papers][1])

---

## 3. Example: d_k changes everything

Suppose:

```
d_k = 16

std(score) ≈ sqrt(16)=4
```

Scores might look like:

```
[2.1, 1.8, -3.0, 0.5]
```

Softmax:

```
[0.55, 0.41, 0.02, 0.02]
```

Fine.

---

Now:

```
d_k = 1024

std(score)=sqrt(1024)=32
```

Scores:

```
[25, 18, -30, 5]
```

Softmax:

[
softmax([25,18,-30,5])
]

becomes almost:

```
[0.999, 0.001, 0, 0]
```

The model says:

> "This one key is definitely correct. Ignore everything else."

Too early.

---

## 4. Why is this bad for training?

Softmax:

[
softmax(x_i)=\frac{e^{x_i}}{\sum e^{x_j}}
]

Gradient:

[
\frac{\partial softmax_i}{\partial x_j}
=======================================

p_i(\delta_{ij}-p_j)
]

If:

```
p = [0.999,0.001,0,0]
```

then:

```
p(1-p)
≈ 0.999 * 0.001
≈ 0.001
```

Gradient is almost zero.

Meaning:

```
loss
 |
softmax
 |
attention score
```

cannot send useful learning signal backward.

This is what the paper means by:

> "pushing the softmax function into regions where it has extremely small gradients." ([NeurIPS Papers][1])

---

## 5. Why divide by sqrt(d_k)?

Because:

[
std(q\cdot k)=\sqrt{d_k}
]

So normalize:

[
score=\frac{q\cdot k}{\sqrt{d_k}}
]

Now:

[
Var(\frac{q\cdot k}{\sqrt{d_k}})
================================

\frac{d_k}{d_k}
=1
]

The score distribution becomes stable:

```
before:

d_k=64:
scores std ≈ 8

d_k=1024:
scores std ≈ 32


after:

d_k=64:
scores std ≈ 1

d_k=1024:
scores std ≈ 1
```

Dimension no longer changes the scale.

---

## 6. Intuition analogy

Imagine ranking documents.

Without scaling:

```
small model:

Document A: 5
Document B: 4
Document C: 3


large model:

Document A: 500
Document B: 400
Document C: 300
```

Softmax sees:

```
small:
[0.66,0.24,0.09]


large:
[1.0,0,0]
```

The second one loses all nuance.

Scaling is like converting:

```
500,400,300

into

5,4,3
```

before softmax.

---

## 7. Why additive attention did not have this problem?

Additive attention computes:

[
score=W^T tanh(W_q q + W_k k)
]

The neural network controls the magnitude through learned weights and `tanh`.

Dot product attention is much faster because it is just:

```python
scores = Q @ K.T
```

which maps perfectly to GPU matrix multiplication.

The Transformer paper chose:

```python
scores = Q @ K.T / sqrt(d_k)
attention = softmax(scores) @ V
```

because it gets the speed of dot products while avoiding softmax saturation. ([Harvard NLP][2])

---

A small PyTorch demo:

```python
import torch
import torch.nn.functional as F

for dk in [16, 64, 512, 1024]:
    q = torch.randn(dk)
    k = torch.randn(dk)

    raw = q @ k
    scaled = raw / dk**0.5

    print(
        dk,
        "raw:", round(raw.item(),2),
        "scaled:", round(scaled.item(),2)
    )
```

Typical output:

```
16    raw: -3.5     scaled: -0.9
64    raw: 12.8     scaled: 1.6
512   raw: -35.2    scaled: -1.6
1024  raw: 44.7     scaled: 1.4
```

The scaling keeps attention logits around the same numerical range.

References:

* ([NeurIPS Papers][1])
* ([Harvard NLP][2])

[1]: https://papers.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf?utm_source=chatgpt.com "Attention Is All You Need"
[2]: https://nlp.seas.harvard.edu/2018/04/01/attention.html?utm_source=chatgpt.com "The Annotated Transformer"
