---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch torch.where Explained Simply
translated: false
type: note
---

Question: Explain `torch.where` in PyTorch.

Answer:

`torch.where` is basically **element-wise if/else**.

```python
torch.where(condition, x, y)
```

means:

```python
result[i] = x[i] if condition[i] else y[i]
```

### 1. Simple example

```python
import torch

x = torch.tensor([1, 2, 3, 4])
y = torch.tensor([10, 20, 30, 40])

condition = x > 2

torch.where(condition, x, y)
```

Result:

```text
tensor([10, 20,  3,  4])
```

Because:

```text
x > 2
 ↓
[False, False, True, True]

where:
False → y
True  → x

[10, 20, 3, 4]
```

It's equivalent to:

```python
[
    x[i] if x[i] > 2 else y[i]
    for i in range(len(x))
]
```

but implemented as a tensor operation on the GPU.

---

### 2. Very common LLM usage

You'll often see:

```python
mask = logits < threshold

logits = torch.where(
    mask,
    torch.tensor(float("-inf")),
    logits,
)
```

For example:

```python
logits = torch.tensor([
    1.0, 5.0, 2.0, 8.0
])

mask = logits < 3

result = torch.where(
    mask,
    torch.tensor(float("-inf")),
    logits,
)

print(result)
```

```text
tensor([-inf, 5., -inf, 8.])
```

Conceptually:

```python
if logits[i] < 3:
    result[i] = -inf
else:
    result[i] = logits[i]
```

This is extremely useful for **masking attention/logits**.

---

### 3. Broadcasting

`torch.where` follows PyTorch broadcasting rules.

```python
x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
])

condition = torch.tensor([
    [True, False, True],
    [False, True, False],
])

torch.where(condition, x, 0)
```

Result:

```text
tensor([
    [1, 0, 3],
    [0, 5, 0],
])
```

Here `0` is broadcast to the entire tensor.

So this:

```python
torch.where(condition, x, 0)
```

is basically:

```python
for every element i:
    if condition[i]:
        output[i] = x[i]
    else:
        output[i] = 0
```

---

### 4. `where(condition)` has a different meaning

There is also:

```python
torch.where(condition)
```

with only one argument.

It returns the **indices where condition is true**.

```python
x = torch.tensor([10, 20, 30, 40])

torch.where(x > 20)
```

gives something like:

```text
(tensor([2, 3]),)
```

Meaning:

```text
x[2] = 30
x[3] = 40
```

For a 2D tensor:

```python
x = torch.tensor([
    [1, 5],
    [7, 2],
])

torch.where(x > 3)
```

returns:

```text
(tensor([0, 1]), tensor([1, 0]))
```

which means:

```text
x[0,1] = 5
x[1,0] = 7
```

---

### 5. The mental model

Think:

```python
torch.where(condition, A, B)
```

as a **tensor-level ternary operator**:

```python
condition ? A : B
```

For example:

```python
y = torch.where(x > 0, x, 0)
```

is essentially:

```python
y = max(x, 0)
```

element by element.

And:

```python
y = torch.where(mask, -torch.inf, logits)
```

means:

```text
mask=True  → -inf
mask=False → logits
```

This pattern shows up everywhere in Transformer implementations: **causal masks, padding masks, attention masking, logit filtering, loss masking, etc.**