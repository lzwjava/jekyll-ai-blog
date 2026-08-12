---
audio: false
generated: true
image: false
lang: en
layout: post
title: Muon-AdamW Optimizer First Principles
translated: false
type: note
---

Question: **How should I understand this Muon + AdamW optimizer implementation from first principles?**

Answer:

The easiest way is **not to read this as 600 lines of PyTorch**. Reduce it to one conceptual picture:

```text
                    gradient g
                       │
             ┌─────────┴─────────┐
             │                   │
        embedding/scalar     2-D matrix
             │                   │
           AdamW                 Muon
             │                   │
             │          momentum / Nesterov
             │                   │
             │             orthogonalize
             │                   │
             │          variance normalization
             │                   │
             └─────────┬─────────┘
                       │
                 update parameter
```

The key idea is:

> **AdamW treats a parameter tensor mostly element-by-element. Muon treats a 2-D weight matrix as a geometric object and changes the *shape/direction* of its update.**

The source itself says the combined optimizer uses AdamW for embeddings/scalars and Muon for matrix parameters.

---

## 1. Start with ordinary gradient descent

Suppose a neural-network weight matrix is

[
W \in \mathbb{R}^{768\times3072}
]

and backprop gives

[
G=\frac{\partial L}{\partial W}.
]

The simplest optimizer is:

[
W \leftarrow W-\eta G
]

where:

* (W) = current weights
* (G) = gradient
* (\eta) = learning rate

Everything in this file ultimately modifies this basic equation.

---

# 2. AdamW's idea

AdamW keeps two memories:

[
m_t \approx \text{average gradient}
]

and

[
v_t \approx \text{average squared gradient}.
]

The code does:

```python
exp_avg32.lerp_(grad32, 1 - beta1_t)
exp_avg_sq32.lerp_(grad32.square(), 1 - beta2_t)
```

Mathematically approximately:

[
m_t=\beta_1m_{t-1}+(1-\beta_1)G_t
]

[
v_t=\beta_2v_{t-1}+(1-\beta_2)G_t^2.
]

Then:

[
\Delta W
========

-\eta
\frac{m_t}{\sqrt{v_t}+\epsilon}.
]

That's the fundamental Adam idea.

The implementation also applies decoupled weight decay:

[
W\leftarrow (1-\eta\lambda)W.
]

That's exactly what lines 48–59 are doing.

---

# 3. Muon starts differently

Muon is interesting because it says:

> If (G) is a matrix, don't necessarily use the raw matrix (G) as the update.

Suppose

[
G=
\begin{bmatrix}
1 & 0\
0 & 0.01
\end{bmatrix}.
]

Normal SGD says:

[
\Delta W=-\eta
\begin{bmatrix}
1&0\
0&0.01
\end{bmatrix}.
]

So one direction gets an update 100× larger than another.

Muon instead tries to **reshape/orthogonalize the update**.

---

# 4. The most important Muon concept: orthogonalization

This is the heart of the file.

The code says:

```python
X = g

...

X = X / (X.norm(...) * 1.01 + 1e-6)

A = X.mT @ X
B = b * A + c * (A @ A)
X = a * X + X @ B
```

This is an iterative approximation to the **polar decomposition**.

For a matrix

[
G=U\Sigma V^T,
]

Muon wants something approximately like

[
UV^T.
]

Notice what happened:

[
G=U\Sigma V^T
]

contains singular values

[
\Sigma=
\begin{bmatrix}
\sigma_1&&\
&\sigma_2&\
&&\cdots
\end{bmatrix}.
]

The polar factor

[
UV^T
]

essentially **removes the singular-value scaling**.

The source explicitly describes this as replacing the update with the nearest orthogonal matrix.

---

# 5. Why is that interesting?

Think of a matrix gradient as having two kinds of information:

```text
G
│
├── directions / orientation
│
└── singular-value magnitudes
```

SVD:

[
G=U\Sigma V^T
]

Muon roughly transforms:

[
G
\rightarrow
UV^T.
]

So it says:

> "I care about the useful geometric directions of this update, but I don't want its singular values to completely determine the update magnitude."

This is the conceptual difference from AdamW.

---

# 6. A very small example

Suppose

[
G=
\begin{bmatrix}
10&0\
0&1
\end{bmatrix}.
]

SVD gives:

[
U=I,\quad
\Sigma=
\begin{bmatrix}
10&0\
0&1
\end{bmatrix},
\quad
V=I.
]

Therefore

[
UV^T=I.
]

Muon turns approximately

[
\begin{bmatrix}
10&0\
0&1
\end{bmatrix}
]

into

[
\begin{bmatrix}
1&0\
0&1
\end{bmatrix}.
]

So instead of saying:

```text
direction 1: 10
direction 2: 1
```

it says approximately:

```text
direction 1: 1
direction 2: 1
```

That is the geometric intuition.

---

# 7. But they don't actually calculate SVD

This is important.

You might think the implementation does:

```python
U, S, V = torch.linalg.svd(G)
G = U @ V.T
```

It doesn't.

That would be expensive.

Instead it uses **Newton-Schulz / Polar Express iteration**.

The file has five coefficient tuples:

```python
polar_express_coeffs = [
    (...),
    (...),
    (...),
    (...),
    (...),
]
```

and then performs five iterations.

The source explicitly says:

> "Newton-Schulz iteration to compute the zeroth power / orthogonalization of G."

So conceptually:

```text
G
 ↓
normalize
 ↓
iteration 1
 ↓
iteration 2
 ↓
iteration 3
 ↓
iteration 4
 ↓
iteration 5
 ↓
approximately polar(G)
```

The clever part is that these operations are mostly matrix multiplications, which GPUs are extremely good at.

---

# 8. Why `X.T @ X`?

Suppose

[
X\in\mathbb R^{m\times n}.
]

Then

[
X^TX\in\mathbb R^{n\times n}.
]

If (X) were perfectly orthogonal in the appropriate sense,

[
X^TX\approx I.
]

So the iteration is essentially trying to push the singular values of (X) toward 1.

That is why this is an **orthogonalization process**.

For the other shape, it uses

[
XX^T
]

instead:

```python
if g.size(-2) > g.size(-1):
    A = X.mT @ X
else:
    A = X @ X.mT
```

It chooses the smaller-side Gram matrix to make the computation cheaper.

---

# 9. Then there is momentum

Muon doesn't directly orthogonalize the raw gradient.

First:

```python
momentum_buffer.lerp_(stacked_grads, 1 - momentum)
g = stacked_grads.lerp_(momentum_buffer, momentum)
```

Conceptually:

[
M_t=\beta M_{t-1}+(1-\beta)G_t
]

and then a Nesterov-style combination produces the effective gradient.

So:

```text
raw gradient
     ↓
momentum
     ↓
effective gradient
     ↓
orthogonalization
```

The source describes Muon as internally running standard SGD-momentum and then applying an orthogonalization post-processing step.

---

# 10. Why only 2-D matrices?

Because this geometric idea naturally applies to matrices.

For example Transformer:

```text
Wq : [hidden_size, hidden_size]
Wk : [hidden_size, hidden_size]
Wv : [hidden_size, hidden_size]
Wo : [hidden_size, hidden_size]
```

These are naturally matrices.

Muon says:

```text
2-D matrix
    ↓
treat gradient as matrix
    ↓
orthogonalize matrix update
```

But an embedding table or scalar doesn't necessarily benefit from this treatment.

Hence:

```text
embedding
bias
scalar
final FC
        ↓
      AdamW
```

while:

```text
large 2-D weight matrix
        ↓
      Muon
```

The implementation explicitly warns against using Muon for embeddings, the final fully connected layer, and 0-D/1-D parameters.

---

# 11. The whole Muon update

You can mentally compress the entire 100-line `muon_step_fused()` into:

[
G_t
]

↓

### momentum

[
G'_t=\text{Momentum}(G_t)
]

↓

### orthogonalization

[
G''_t\approx \operatorname{polar}(G'_t)
]

↓

### normalize update scale

↓

### cautious weight decay

↓

[
W_{t+1}
=======

W_t-\eta G''_t-\text{weight decay}.
]

The actual code does these stages in:

```python
# Nesterov momentum
...

# MuonEq
...

# Polar Express
...

# Muon+
...

# Variance reduction
...

# Weight decay + update
...
```

That is the structure you should keep in your head.

---

# 12. What is `MuonEq` doing?

This part:

```python
target = X.float().norm(dim=(-2, -1), keepdim=True) / (X.size(-2) ** 0.5)

row_norm = X.float().norm(dim=-1, keepdim=True)

X = X * (target / row_norm)
```

is basically:

> make different rows have comparable norms before orthogonalization.

Imagine:

```text
row 0  ███████████████
row 1  ██
row 2  █████████
row 3  █
```

MuonEq tries to make the row scales less pathological before running the polar iteration.

The source describes it as **row equilibration** to improve conditioning.

---

# 13. What is `Muon+`?

After orthogonalization:

```python
target_norm = min(m, n) ** 0.5
current_norm = g.norm(...)
g = g * (target_norm / current_norm)
```

An exactly semi-orthogonal matrix has Frobenius norm approximately

[
\sqrt{\min(m,n)}.
]

So they force the update back toward that norm.

In other words:

```text
orthogonalization
       ↓
maybe slightly wrong magnitude
       ↓
renormalize Frobenius norm
```

The source calls this **Muon+ renormalization**.

---

# 14. And then variance reduction

This part is more subtle:

```python
v_mean = g.float().square().mean(...)
second_momentum_buffer.lerp_(...)
step_size = second_momentum_buffer.clamp_min(...).rsqrt()
...
g = g * final_scale
```

The idea is roughly:

> After forcing the update to have a controlled matrix geometry, still adapt its scale using a second-moment estimate.

So Muon isn't simply:

[
G\rightarrow UV^T.
]

It's more like:

[
G
\rightarrow
\text{momentum}
\rightarrow
\text{orthogonalization}
\rightarrow
\text{variance normalization}
\rightarrow
\Delta W.
]

---

# 15. The distributed part is a completely separate problem

Once you understand the above, ignore lines 325+ initially.

That section is basically answering:

> "How do I make the same optimizer work on 8 GPUs without replicating all optimizer state?"

For example with 8 GPUs:

```text
                   gradient
                      │
                reduce_scatter
                      │
          ┌───────┬───┴───┬───────┐
          GPU0   GPU1     ...     GPU7
           │      │                │
         update  update           update
           │      │                │
          └───────┴───┬───────────┘
                   all_gather
                       │
                 updated params
```

For AdamW, large parameters are sliced across GPUs and optimizer states are sharded.

For Muon, parameters are stacked:

```python
stacked_grads = torch.stack([p.grad for p in params])
```

and different GPUs own different matrices.

So there are really **two layers of ideas**:

```text
Algorithmic layer
──────────────────────────
AdamW
Muon
momentum
polar orthogonalization
variance normalization


Systems layer
──────────────────────────
stacking
reduce_scatter
all_gather
async communication
optimizer-state sharding
```

Don't mix these two while learning the code.

---

# 16. The most useful mental model

Given your recent Q/K/V matrix questions, I'd think about Muon this way:

Suppose a Transformer has

[
W_Q\in\mathbb R^{4096\times4096}.
]

Backprop gives

[
G_Q=\frac{\partial L}{\partial W_Q}.
]

AdamW essentially says:

> "For every element of (G_Q), estimate its useful scale using first and second moments."

Muon says:

> "This isn't merely 16 million independent numbers. It is a **4096×4096 linear transformation**. Treat its gradient as a matrix and normalize its geometric structure."

That's the important conceptual jump.

So:

```text
AdamW

G[i,j]
 ↓
element-wise adaptive scaling
 ↓
ΔW[i,j]


Muon

G                    ← matrix
│
├── momentum
│
├── singular directions
│
├── orthogonalize
│
└── controlled matrix norm
        ↓
      ΔW
```

The Muon paper/code is therefore much easier to understand if you already understand **SVD + singular values + orthogonal matrices + matrix multiplication**.

---

## If you want to actually understand the code

I would learn it in exactly this order:

```text
1. SGD
   W ← W - ηG

2. Momentum
   m ← βm + (1-β)G

3. Adam
   m, v → m / sqrt(v)

4. SVD
   G = UΣVᵀ

5. Polar decomposition
   G ≈ UΣVᵀ
   polar(G) = UVᵀ

6. Newton-Schulz
   approximate UVᵀ without SVD

7. Muon
   momentum → polar(G) → scaling → W update

8. Distributed Muon
   reduce_scatter → local Muon → all_gather
```

**The single most important equation to internalize is:**

[
\boxed{
G=U\Sigma V^T
\quad\longrightarrow\quad
UV^T
}
]

That is the conceptual core behind the scary-looking `Polar Express` code. The rest is largely **making that operation fast, numerically stable, scale-controlled, and distributed**.

References:

* [Source: MuonAdamW / DistMuonAdamW implementation]
* [Muon background and orthogonalization]
