---
audio: false
generated: true
image: false
lang: en
layout: post
title: view -1 automatically infers dimension
translated: false
type: note
---

Question: In `logits.view(-1, logits.size(-1))`, does `-1` mean the last index?

Answer: **No.** In PyTorch `view()`, `-1` means **"infer this dimension automatically"**, not "last index".

For example, suppose:

```python
logits.shape
# [B, T, V]
# [2, 10, 50000]
```

Then:

```python
logits.view(-1, logits.size(-1))
```

becomes:

```python
logits.view(-1, 50000)
```

PyTorch calculates:

```text
2 × 10 × 50000
---------------- = 20
     50000
```

so the result is:

```python
[20, 50000]
```

This is extremely common for language-model loss:

```python
logits = model(x)
# [batch, seq_len, vocab_size]

logits = logits.view(-1, logits.size(-1))
# [batch * seq_len, vocab_size]

targets = targets.view(-1)
# [batch * seq_len]

loss = F.cross_entropy(logits, targets)
```

The idea is:

```text
[B, T, V]
   ↓
[B*T, V]
```

You are **flattening batch × sequence positions**, while keeping the vocabulary dimension intact.

### `-1` vs negative indexing

These are different concepts:

```python
x[-1]       # indexing: last element
x.view(-1)  # reshape: infer dimension
```

So:

```python
logits.size(-1)
```

**does** mean "size of the last dimension" → `V`.

But:

```python
logits.view(-1, ...)
```

means "figure out this dimension automatically."
