---
audio: false
generated: true
image: false
lang: en
layout: post
title: Contiguous Memory in PyTorch
translated: false
type: note
---

Question: What does `contiguous` mean in PyTorch?

Answer:

In PyTorch, **contiguous** means that a tensor's elements are stored in a **continuous block of memory following its logical order**.

A tensor has:

1. **shape** — how you view the data
2. **stride** — how PyTorch jumps in memory to access elements
3. **storage** — the actual memory buffer

Example:

```python
import torch

x = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])

print(x.stride())
print(x.is_contiguous())
```

Output:

```
(3, 1)
True
```

Memory layout:

```
memory:
[1][2][3][4][5][6]

row 0: start + 0,1,2
row 1: start + 3,4,5
```

The stride `(3,1)` means:

* move one column → jump 1 element
* move one row → jump 3 elements

This is the normal C-style row-major layout.

---

The important case is when you use `transpose`:

```python
x = torch.tensor([[1,2,3],
                  [4,5,6]])

y = x.T

print(y)
print(y.stride())
print(y.is_contiguous())
```

Output:

```
tensor([[1,4],
        [2,5],
        [3,6]])

stride: (1,3)
contiguous: False
```

Why?

`y` is not copied. PyTorch only changes the **view**:

Original memory:

```
[1][2][3][4][5][6]
```

`x`:

```
1 2 3
4 5 6
```

`y = x.T`:

```
1 4
2 5
3 6
```

To read row-wise from `y`:

```
1 -> jump 3 -> 4
2 -> jump 3 -> 5
3 -> jump 3 -> 6
```

The memory order does not match the tensor order, so it is non-contiguous.

---

Some operations require contiguous memory.

Example:

```python
y = x.T

y.view(-1)
```

may fail:

```
RuntimeError: view size is not compatible with input tensor's size and stride
```

because `view()` only works when the new shape can be represented by the existing memory layout.

Fix:

```python
y = x.T.contiguous()

z = y.view(-1)
```

`contiguous()` makes a real copy:

Before:

```
x storage:
[1][2][3][4][5][6]

y:
1 4
2 5
3 6

(no new memory)
```

After:

```
new storage:
[1][4][2][5][3][6]
```

Now the tensor order and memory order agree.

---

In Transformer code this appears often:

```python
q = q.transpose(1, 2)
q = q.contiguous()
q = q.view(batch, seq, hidden)
```

Typical flow:

```
(B, heads, seq, head_dim)
        |
        transpose
        v
(B, seq, heads, head_dim)
        |
        contiguous
        |
        view
        v
(B, seq, hidden)
```

`transpose()` changes strides without copying; `contiguous()` rearranges memory so later `view()` or CUDA kernels can operate efficiently.

A useful mental model:

```
view()
  = change the interpretation of memory

transpose()
  = change strides (usually no copy)

contiguous()
  = make a new memory layout matching the current view
```

In modern PyTorch, many ops handle non-contiguous tensors automatically, but performance-critical kernels (especially CUDA kernels in attention, matmul, fused ops) often prefer contiguous layouts.
