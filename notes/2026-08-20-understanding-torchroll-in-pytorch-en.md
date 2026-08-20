---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding torch.roll in PyTorch
translated: false
type: note
---

Question: What does `torch.roll` mean?

Answer:

`torch.roll` **circularly shifts tensor elements along a dimension**. Elements that move past one edge wrap around to the other edge.

Think of it like rotating an array.

Syntax:

```python
torch.roll(input, shifts, dims=None)
```

* `input`: tensor
* `shifts`: how many positions to shift
* `dims`: which dimension to shift

### 1D example

```python
import torch

x = torch.tensor([1, 2, 3, 4, 5])

torch.roll(x, shifts=2)
```

Output:

```
tensor([4, 5, 1, 2, 3])
```

Explanation:

```
original:
[1, 2, 3, 4, 5]

shift right by 2:
        <- wrap
[4, 5, 1, 2, 3]
```

The last two elements move to the front.

---

### Negative shift

```python
torch.roll(x, shifts=-2)
```

Output:

```
tensor([3, 4, 5, 1, 2])
```

Shift left by 2:

```
[1, 2, 3, 4, 5]
       ↓
[3, 4, 5, 1, 2]
```

---

### 2D example

Matrix:

```python
x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
```

Shift rows down:

```python
torch.roll(x, shifts=1, dims=0)
```

Output:

```
[
 [7, 8, 9],
 [1, 2, 3],
 [4, 5, 6]
]
```

Shift columns right:

```python
torch.roll(x, shifts=1, dims=1)
```

Output:

```
[
 [3, 1, 2],
 [6, 4, 5],
 [9, 7, 8]
]
```

---

### Why is `torch.roll` used in deep learning?

Common uses:

### 1. Vision models / image shifting

For data augmentation or comparing neighboring pixels:

```python
shifted = torch.roll(image, shifts=(1,1), dims=(1,2))
```

Move image pixels vertically and horizontally.

---

### 2. Self-supervised learning

Example: compare a feature map with a shifted version:

```python
loss = (x - torch.roll(x, 1, dim=1)).abs().mean()
```

Measures local smoothness.

---

### 3. Transformer / LLM research

Used for position manipulation, rotary embeddings experiments, cyclic attention patterns, etc.

Example:

```python
q_shifted = torch.roll(q, shifts=1, dims=1)
```

If:

```
q shape = [batch, seq_len, hidden]
```

then:

```
before:

token0 token1 token2 token3

after roll(1):

token3 token0 token1 token2
```

This creates a shifted token relationship.

---

### Relation to NumPy

It is basically:

```python
numpy.roll()
```

Equivalent:

```python
torch.roll(x, 2)
```

≈

```python
np.roll(x, 2)
```

---

Implementation idea:

```python
def simple_roll(x, shift):
    return torch.cat([
        x[-shift:],
        x[:-shift]
    ])
```

`torch.roll` is just an efficient C++/CUDA implementation of this circular indexing operation.
