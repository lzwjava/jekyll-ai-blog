---
audio: false
generated: true
image: false
lang: en
layout: post
title: Outer Product for RoPE
translated: false
type: note
---

**Question:**
What does `freqs = torch.einsum("i,j -> ij", t, inv_freq)` mean?

**Answer:**

This line computes an **outer product** between two 1D tensors:

```python
freqs = torch.einsum("i,j -> ij", t, inv_freq)
```

Equivalent PyTorch:

```python
freqs = t[:, None] * inv_freq[None, :]
```

or:

```python
freqs = torch.outer(t, inv_freq)
```

### Step-by-step

Assume:

```python
t = torch.tensor([0, 1, 2, 3])      # shape: [4]

inv_freq = torch.tensor([1.0, 0.1, 0.01])  # shape: [3]
```

The einsum notation:

```
"i,j -> ij"
```

means:

* input 1 has dimension `i`
* input 2 has dimension `j`
* output keeps both dimensions: `ij`

Mathematically:

[
freqs_{ij}=t_i \times inv_freq_j
]

So:

```
          inv_freq
          1.0    0.1    0.01
t=0       0      0      0
t=1       1      0.1    0.01
t=2       2      0.2    0.02
t=3       3      0.3    0.03
```

Output:

```python
freqs.shape
# torch.Size([4, 3])
```

---

### Why used in Transformers?

This is usually from **RoPE (Rotary Position Embedding)**.

Typical code:

```python
t = torch.arange(seq_len)
inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2) / dim))

freqs = torch.einsum("i,j->ij", t, inv_freq)
```

Here:

* `t` = token positions

Example:

```
t = [0,1,2,3,...,2047]
```

* `inv_freq` = frequencies for each pair of embedding dimensions

Example:

```
inv_freq =
[
 1.0000,
 0.1000,
 0.0100,
 0.0010,
 ...
]
```

The output:

```
freqs[position, dimension]
```

contains the rotation angle:

[
\theta_{pos,k}=pos \times \frac{1}{10000^{2k/d}}
]

Then:

```python
cos = torch.cos(freqs)
sin = torch.sin(freqs)
```

are used to rotate Q/K vectors:

[
q' = q \cos(\theta) + rotate(q)\sin(\theta)
]

---

### Forward-pass view

For a sequence length 4096 and hidden dimension 4096:

```python
t.shape
# [4096]

inv_freq.shape
# [2048]
```

After einsum:

```python
freqs.shape
# [4096,2048]
```

Meaning:

```
             dimension frequency
position 0   θ0 θ1 θ2 ... θ2047
position 1   θ0 θ1 θ2 ... θ2047
position 2   θ0 θ1 θ2 ... θ2047
...
position4095
```

Each token position gets a different phase for every rotary dimension pair.

So this single line is basically:

> "Generate the complete position × frequency matrix used to rotate every token embedding dimension in RoPE."
