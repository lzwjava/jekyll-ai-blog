---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding X.mT in PyTorch
translated: false
type: note
---

Question: What does `X.mT` mean here, and is the overall computation equivalent to what you wrote?

Answer: Yes. In PyTorch, **`.mT` means matrix transpose**.

For a 2-D tensor:

```python
X.mT
```

is equivalent to:

```python
X.transpose(-2, -1)
```

So if

```python
X.shape == (n, d)
```

then:

```python
X.mT.shape == (d, n)
```

Your code can be read as:

```python
X = X / (X.norm(...) * 1.01 + 1e-6)

A = X.mT @ X
B = b * A + c * (A @ A)

X = a * X + X @ B
```

Let's follow the shapes.

Assume:

```text
X: (n, d)
```

where `n` = number of vectors/tokens and `d` = hidden dimension.

### 1. Normalize X

```python
X = X / (X.norm(...) * 1.01 + 1e-6)
```

This scales `X` by some norm-based factor.

Ignoring broadcasting details:

```text
X: (n, d)
```

stays `(n, d)`.

### 2. `X.mT @ X`

```python
A = X.mT @ X
```

means:

```text
(d, n) @ (n, d)
       ↓
     (d, d)
```

So:

```text
A = XᵀX
```

This is essentially a **Gram/correlation matrix of the dimensions/features**.

For example:

```text
X = [
  x₁
  x₂
  x₃
]
```

with each `xᵢ ∈ Rᵈ`.

Then:

```text
XᵀX
```

asks how the **different dimensions of X correlate with each other across the n samples**.

### 3. `A @ A`

```python
A @ A
```

is simply:

```text
A²
```

because `A` is `(d, d)`:

```text
(d, d) @ (d, d)
        ↓
      (d, d)
```

Therefore:

```python
B = b * A + c * (A @ A)
```

is mathematically:

```text
B = bA + cA²
```

So `B` is a **polynomial function of `XᵀX`**:

```text
B = b XᵀX + c (XᵀX)²
```

### 4. `X @ B`

Finally:

```python
X = a * X + X @ B
```

has:

```text
X: (n, d)
B: (d, d)

X @ B: (n, d)
```

so the result can be added back to `X`.

Expanding everything:

```text
X_new
= aX + X[bXᵀX + c(XᵀX)²]
```

or:

```text
X_new
= aX
+ bXXᵀX
+ cX(XᵀX)²
```

This is a nice way to understand the operation: **`X` constructs a feature-space matrix `XᵀX`, turns it into a polynomial transformation `B`, and then applies that learned/data-dependent transformation back to X.**

And importantly, this is **not**:

```text
X = X / X
```

`X.mT` specifically means **transpose the last two dimensions**, not some special multiplication operation.

If `X` is 3-D, e.g. `(batch, seq, hidden)`, `.mT` gives `(batch, hidden, seq)`, which is why PyTorch's `.mT` is particularly convenient for batched matrix multiplication.