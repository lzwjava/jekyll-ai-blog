---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyTorch lerp_ In-Place Interpolation
translated: false
type: note
---

Question: What does `lerp_` mean in PyTorch?

Answer:

`lerp_` means **in-place linear interpolation**.

The name breaks down as:

* `lerp` = **linear interpolation**
* `_` suffix = **modify the tensor in-place**

The core operation is:

[
\text{out} = a + w(b-a)
]

or equivalently:

[
\text{out} = (1-w)a + wb
]

In PyTorch:

```python
a = torch.tensor([0., 10.])
b = torch.tensor([10., 20.])

a.lerp_(b, 0.25)

print(a)
# tensor([ 2.5, 12.5])
```

Because it is `_`, **`a` itself is modified**.

### `lerp` vs `lerp_`

```python
a = torch.tensor([0., 10.])
b = torch.tensor([10., 20.])

c = torch.lerp(a, b, 0.25)

# a is unchanged
# c = [2.5, 12.5]
```

versus:

```python
a.lerp_(b, 0.25)

# a is now [2.5, 12.5]
```

### Why you see `lerp_` in ML code

A very common use is **EMA / exponential moving average**:

```python
ema.lerp_(model, decay)
```

Suppose:

```python
ema = [1, 1]
model = [5, 9]
decay = 0.1
```

Then:

```text
ema ← ema + 0.1 * (model - ema)
```

giving:

```text
[1, 1] + 0.1 * ([5, 9] - [1, 1])
= [1.4, 1.8]
```

This is basically a cheap way to write:

```python
ema = (1 - decay) * ema + decay * model
```

but `lerp_` does it **in-place**, avoiding creation of another tensor.

One important detail: **the third argument is a weight**, not necessarily "decay" semantically. So:

```python
torch.lerp(start, end, weight)
```

means:

```text
start + weight * (end - start)
```

* `weight = 0` → `start`
* `weight = 1` → `end`
* `weight = 0.5` → midpoint
* `weight = 2` → extrapolates beyond `end`

References:

* [PyTorch torch.lerp documentation](https://docs.pytorch.org/docs/stable/generated/torch.lerp.html?utm_source=chatgpt.com)
