---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Triton's cdiv
translated: false
type: note
---

Question: What does `triton.cdiv` mean?

Answer: `triton.cdiv` means **ceiling division** in Triton.

```python
triton.cdiv(x, y)
```

computes:

$$
\left\lceil \frac{x}{y} \right\rceil
$$

Equivalent Python:

```python
(x + y - 1) // y
```

### Example

```python
triton.cdiv(100, 32)
# 4
```

Because:

$$
100 / 32 = 3.125 \rightarrow \lceil3.125\rceil = 4
$$

This is extremely common in GPU kernels when calculating **how many blocks/warps are needed**:

```python
BLOCK_SIZE = 256
num_blocks = triton.cdiv(n, BLOCK_SIZE)
```

If `n = 1000`:

```text
1000 elements
÷ 256 elements/block
= 3.90625 blocks
→ 4 blocks
```

The key difference:

```python
n // BLOCK_SIZE       # floor division → may be too small
triton.cdiv(n, BLOCK_SIZE)  # ceiling division → covers everything
```

For LLM/Triton code, you'll see this constantly for things like **sequence length, tokens, rows, and tiles**.

I can also walk through a real Triton kernel and show exactly why `cdiv` appears in the grid calculation.
