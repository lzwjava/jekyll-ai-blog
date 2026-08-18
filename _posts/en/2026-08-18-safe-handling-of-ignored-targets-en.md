---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safe Handling of Ignored Targets
translated: false
type: note
---

Question: Explain this PyTorch code path for handling `ignore_index` targets such as `-1`.

Answer:

The key idea is:

> **Some target tokens are invalid/ignored (`y < 0`), so we must not use them to index `token_bytes`.**

Let's go line by line.

### 1. Why is this special case needed?

Suppose:

```python
y = tensor([10, 20, -1, 30])
```

where `-1` means **ignore this target**.

And:

```python
token_bytes = tensor([...])
```

where:

```python
token_bytes[token_id]
```

gives the number of UTF-8 bytes represented by that token.

Normally we'd do:

```python
num_bytes = token_bytes[y]
```

For:

```python
y = [10, 20, 30]
```

that's fine.

But:

```python
y = [10, 20, -1, 30]
```

is dangerous because:

```python
token_bytes[-1]
```

in PyTorch means **the last element**, not "invalid".

So `-1` would accidentally become a real token index.

---

## 2. Why this weird first line?

```python
if (y.int() < 0).any():
```

Break it down:

```python
y.int()
```

casts `y` to `int32`.

Then:

```python
y.int() < 0
```

produces a boolean tensor:

```text
y              = [10, 20, -1, 30]

y.int() < 0    = [F,  F,  T,  F]
```

Then:

```python
.any()
```

asks:

> Does **any** element satisfy `< 0`?

So:

```python
(y.int() < 0).any()
```

is:

```text
True
```

The comment says this is specifically because Apple's **MPS backend** currently doesn't have the required `int64 < 0` kernel, while `int32` works.

---

# 3. Create a validity mask

```python
valid = y >= 0
```

For:

```python
y = [10, 20, -1, 30]
```

we get:

```text
valid = [True, True, False, True]
```

Think of it as:

```text
token 10   → use
token 20   → use
token -1   → IGNORE
token 30   → use
```

---

# 4. Replace invalid indices with 0

This is the important trick:

```python
y_safe = torch.where(
    valid,
    y,
    torch.zeros_like(y)
)
```

`torch.where(condition, a, b)` means:

```text
if condition:
    take a
else:
    take b
```

Therefore:

```text
valid  = [T, T, F, T]
y      = [10,20,-1,30]
```

becomes:

```text
y_safe = [10,20, 0,30]
```

Notice:

```text
-1 → 0
```

Why?

Because now this is safe:

```python
token_bytes[y_safe]
```

We're never doing:

```python
token_bytes[-1]
```

---

# 5. Look up byte lengths

Now:

```python
token_bytes[y_safe]
```

might produce:

```text
token_bytes[y_safe]
    ↓
[3, 4, 1, 2]
```

But remember:

```text
position 2 was originally -1
```

So the `1` we got from:

```python
token_bytes[0]
```

is meaningless.

We need to turn it back into zero.

That's what this does:

```python
num_bytes2d = torch.where(
    valid,
    token_bytes[y_safe],
    torch.zeros_like(y, dtype=token_bytes.dtype)
)
```

Result:

```text
valid                 [T, T, F, T]
token_bytes[y_safe]   [3, 4, 1, 2]
                         ↓
num_bytes2d            [3, 4, 0, 2]
```

So the ignored token contributes **zero bytes**.

---

# 6. Ignore its loss too

Then:

```python
total_nats += (loss2d * (num_bytes2d > 0)).sum()
```

Suppose:

```text
loss2d       = [0.5, 1.2, 9.8, 0.7]
num_bytes2d  = [3,   4,   0,   2]
```

Then:

```python
num_bytes2d > 0
```

gives:

```text
[True, True, False, True]
```

So:

```python
loss2d * (num_bytes2d > 0)
```

becomes:

```text
[0.5, 1.2, 0.0, 0.7]
```

The ignored target's loss is removed.

So:

```text
total_nats = 0.5 + 1.2 + 0.7
```

---

# 7. Count only valid bytes

Finally:

```python
total_bytes += num_bytes2d.sum()
```

For:

```text
num_bytes2d = [3, 4, 0, 2]
```

we get:

```text
total_bytes += 9
```

The ignored token contributes:

```text
0 bytes
```

---

## The whole thing

You can mentally reduce the entire block to:

```python
y = [10, 20, -1, 30]

# -1 means "ignore"
```

### Step 1 — identify valid targets

```text
valid:
[ True, True, False, True ]
```

### Step 2 — make indices safe

```text
y:
[10, 20, -1, 30]

y_safe:
[10, 20,  0, 30]
```

### Step 3 — lookup byte lengths

```text
token_bytes[y_safe]:
[3, 4, 1, 2]
```

### Step 4 — erase the fake lookup for ignored token

```text
num_bytes2d:
[3, 4, 0, 2]
```

### Step 5 — use the same mask for loss

```text
loss2d:
[0.5, 1.2, 9.8, 0.7]

mask:
[1, 1, 0, 1]

effective loss:
[0.5, 1.2, 0, 0.7]
```

So the invariant is:

```text
y < 0
  ↓
invalid target
  ↓
don't index with it
  ↓
replace with safe index 0
  ↓
set its byte count to 0
  ↓
its loss is ignored
```

### Why not simply do this?

You might wonder why they don't write:

```python
num_bytes2d = token_bytes[y]
```

and then mask it.

Because **the indexing happens before the mask**:

```python
token_bytes[-1]
```

has already happened.

The crucial pattern is therefore:

```python
y_safe = torch.where(y >= 0, y, 0)

lookup = token_bytes[y_safe]

result = torch.where(
    y >= 0,
    lookup,
    0
)
```

This is a very common GPU-programming pattern:

> **sanitize indices first → perform gather/indexing → mask invalid results afterward.**

One subtle point: `loss2d * (num_bytes2d > 0)` is effectively an ignore mask here because valid tokens have positive byte lengths. The actual semantic source of truth is `valid`; using `num_bytes2d > 0` works because `num_bytes2d` was constructed to be zero exactly for ignored targets.