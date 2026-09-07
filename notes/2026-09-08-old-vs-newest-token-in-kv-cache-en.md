---
audio: false
generated: true
image: false
lang: en
layout: post
title: Old vs Newest Token in KV Cache
translated: false
type: note
---

Question: What do “old tokens” and “newest token” mean in KV cache?

Answer: **“Old” and “newest” simply mean the tokens that have already been processed vs. the token currently being generated.**

Take:

```text
The cat sat
```

Suppose the LLM has already processed these 3 tokens:

```text
Token 1: The
Token 2: cat
Token 3: sat
```

Now it wants to generate **token 4**.

### 1. The "old tokens"

The tokens already in the context are the **old tokens**:

```text
The   cat   sat
 ↑     ↑     ↑
old   old   old
```

The transformer has already computed their:

```text
K1, V1
K2, V2
K3, V3
```

and stores them in the KV cache:

```text
KV Cache:

K1 V1   ← "The"
K2 V2   ← "cat"
K3 V3   ← "sat"
```

These don't need to be recomputed.

---

### 2. The "newest token"

Now the model generates the next token, say:

```text
"The cat sat on"
              ↑
          newest token
```

`on` is the **newest token** because it was just generated.

For this token, the model computes:

```text
Q4
K4
V4
```

Then:

```text
KV Cache:

K1 V1   ← The
K2 V2   ← cat
K3 V3   ← sat
K4 V4   ← on       ← newly added
```

Then when generating token 5:

```text
The cat sat on the
                  ↑
              newest token
```

Now:

```text
The cat sat on
 ↑   ↑   ↑   ↑
old old old old

the
 ↑
newest
```

The cache already contains:

```text
K1 V1
K2 V2
K3 V3
K4 V4
```

so we only calculate:

```text
Q5 K5 V5
```

and append `K5,V5`.

---

### The important distinction

At every decoding step, there is **one newly processed token**:

```text
┌──────────────────── already processed ────────────────────┐
│                                                           │
The   cat   sat   on   the   mat
 ↑     ↑     ↑    ↑    ↑
 old   old   old  old  old
                         │
                         └── newest at this step
```

After generating `mat`, the situation changes:

```text
The   cat   sat   on   the   mat
 ↑     ↑     ↑    ↑    ↑     ↑
 old   old   old  old  old  newest
```

On the **next** step, the next generated token becomes newest, and `mat` becomes old.

So **"old" isn't a permanent property of a token**. It's relative to the current generation step.

---

### One subtle but important point

When generating token 6, the model still needs to **attend to all previous tokens**:

```text
Q6  ×  [K1 K2 K3 K4 K5]
       ↓  ↓  ↓  ↓  ↓
      all previous tokens
```

But it doesn't need to **recompute** `K1...K5` and `V1...V5`.

That's the entire point of KV cache:

```text
                OLD TOKENS
                   │
             K/V already cached
                   │
                   ▼
new token → Q ──→ attention → next-token probability
       └────→ K,V → append to cache
```

This is also why **KV cache grows by one token every decoding step**.
