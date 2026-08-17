---
audio: false
generated: true
image: false
lang: en
layout: post
title: RoPE Precomputation in NanoChat Code
translated: false
type: note
---

Question: Explain the RoPE implementation in nanochat code.

Answer:

This code is the **precomputation part** of Rotary Position Embedding (RoPE). It creates the `cos` and `sin` tables that will later rotate the Query and Key vectors.

Let's walk from math → tensor shapes → code.

---

## 1. First: what RoPE needs

For every token position `t` and every pair of embedding dimensions, RoPE needs an angle:

[
\theta_{t,i}=t \cdot \frac{1}{base^{2i/d}}
]

where:

* `t` = token position
* `i` = dimension pair index
* `d` = head dimension
* `base` = usually 10000, here 100000

Then:

[
cos(\theta_{t,i})
]

and

[
sin(\theta_{t,i})
]

are used to rotate Q/K.

---

## 2. Calculate head dimension

```python
head_dim = self.config.n_embd // self.config.n_head
```

Example:

GPT:

```
embedding size = 768
heads = 12
```

Then:

```
head_dim = 768 / 12 = 64
```

Attention splits:

```
hidden state

[768]

        split into heads

head0 [64]
head1 [64]
...
head11[64]
```

RoPE works **inside each attention head**, not on the whole embedding.

---

## 3. Precompute rotation table

```python
cos, sin = self._precompute_rotary_embeddings(
    self.rotary_seq_len,
    head_dim
)
```

Suppose:

```
max sequence length = 2048
head_dim = 64
```

Need:

```
position 0
position 1
...
position 2047
```

For each position:

```
64 dimensions
```

But RoPE rotates pairs:

```
(dim0, dim1)

(dim2, dim3)

(dim4, dim5)

...
```

Therefore only half dimensions need frequencies:

```
64 / 2 = 32
```

---

# Inside `_precompute_rotary_embeddings`

## 4. Get device

```python
if device is None:
    device = self.transformer.wte.weight.device
```

Put tensors on the same GPU as embeddings.

Example:

```
cuda:0
```

---

## 5. Create frequency indexes

```python
channel_range = torch.arange(
    0,
    head_dim,
    2,
    dtype=torch.float32,
    device=device
)
```

For:

```
head_dim=8
```

this produces:

```
[0,2,4,6]
```

Because dimensions are paired:

```
dim0 <-> dim1
dim2 <-> dim3
dim4 <-> dim5
dim6 <-> dim7
```

Only first dimension of each pair needs a frequency.

---

## 6. Compute inverse frequencies

```python
inv_freq = 1.0 / (
    base ** (channel_range / head_dim)
)
```

This is the core RoPE formula.

Example:

```
base=100000
head_dim=8
```

For dimension 0:

[
freq_0 =
1 / 100000^{0/8}
]

=1

For dimension 6:

[
freq_6 =
1 / 100000^{6/8}
]

much smaller.

So:

```
low dimensions:
    high frequency rotation

high dimensions:
    slow rotation
```

Like Fourier features.

---

## 7. Create positions

```python
t = torch.arange(seq_len)
```

Example:

```
seq_len=4
```

creates:

```
[0,1,2,3]
```

Token positions.

---

## 8. Outer product

This line is the heart:

```python
freqs = torch.outer(t, inv_freq)
```

Imagine:

```
t:

position
0
1
2
3


inv_freq:

freq0
freq1
freq2
freq3
```

Outer product:

```
             freq0 freq1 freq2 freq3

pos0          0     0     0     0

pos1          f0    f1    f2    f3

pos2          2f0   2f1   2f2   2f3

pos3          3f0   3f1   3f2   3f3
```

Shape:

```
(seq_len, head_dim/2)
```

Example:

```
(2048,32)
```

Each cell is the rotation angle.

---

## 9. Generate lookup tables

```python
cos, sin = freqs.cos(), freqs.sin()
```

Now:

```
cos[position][dimension_pair]

sin[position][dimension_pair]
```

Example:

```
cos:

[
 [1.0,1.0,1.0],
 [0.54,0.99,0.999],
 ...
]


sin:

[
 [0,0,0],
 [0.84,0.01,0.001],
 ...
]
```

---

## 10. Convert precision

```python
cos, sin = cos.to(COMPUTE_DTYPE)
```

Usually:

```
bf16
```

because storing:

```
2048 x 32
```

is small, but for very long context:

```
128k x 64
```

it matters.

---

## 11. Add broadcast dimensions

```python
cos, sin = cos[None,:,None,:]
```

Original:

```
(seq_len, head_dim/2)
```

Example:

```
(2048,32)
```

After:

```
(1,2048,1,32)
```

Why?

Because Q/K usually have shape:

```
(batch, heads, seq_len, head_dim)
```

Example:

```
B=8
H=12
T=2048
D=64


q:

(8,12,2048,64)
```

RoPE operation needs:

```
position dimension
```

to broadcast.

The table:

```
(1,2048,1,32)
```

broadcasts to:

```
(8,12,2048,32)
```

automatically.

---

# The actual rotation later

This code only prepares:

```
cos
sin
```

Later somewhere:

```python
q_rotated = q * cos + rotate_half(q) * sin
```

where:

```
rotate_half([x0,x1,x2,x3])

=

[-x1,x0,-x3,x2]
```

For each pair:

```
[x,y]

rotation:

[x*cos - y*sin,
 x*sin + y*cos]
```

The normal 2D rotation matrix:

[
\begin{bmatrix}
cos\theta & -sin\theta\
sin\theta & cos\theta
\end{bmatrix}
]

---

So the whole pipeline:

```
token
 |
v
embedding
 |
v
Q,K projection
 |
v
split into heads
 |
v
RoPE:

position t
 |
calculate theta
 |
apply:

[x,y] -> rotated [x',y']

 |
v
attention:

Q_rot K_rot^T
 |
v
relative position emerges
```

The nanochat implementation is very close to the original RoPE paper. The clever part is that **this entire positional encoding is just a cached sin/cos table plus elementwise operations — no learned parameters.**
