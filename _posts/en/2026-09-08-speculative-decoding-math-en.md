---
audio: false
generated: true
image: false
lang: en
layout: post
title: Speculative Decoding Math
translated: false
type: note
---

Question: **What is the math behind speculative decoding?**

Answer:

Let:

* \\(p(x)\\) = probability distribution of the **large target model**
* \\(q(x)\\) = probability distribution of the **small draft model**

The problem is that we want samples from \\(p\\), but evaluating \\(p\\) is expensive.

### 1. Draft model proposes tokens

Suppose the draft model generates \\(K=5\\) tokens:

```text
context
   ↓
draft q
   ↓
t1 → t2 → t3 → t4 → t5
```

For example:

```text
"The capital of France is"
        ↓
"Paris is one of the"
```

The draft model has generated these autoregressively, so it computes:

$$
q(t_1|x)
$$

then

$$
q(t_2|x,t_1)
$$

etc.

### 2. Target model evaluates all of them in parallel

Now the important trick.

Instead of asking the big model:

```text
x → t1
x,t1 → t2
x,t1,t2 → t3
x,t1,t2,t3 → t4
x,t1,t2,t3,t4 → t5
```

we construct one sequence:

```text
x t1 t2 t3 t4 t5
```

and run **one transformer forward pass**.

Because Transformer training/inference over a known sequence is naturally parallelizable across positions, the target model can calculate:

$$
p(t_1|x)
$$

$$
p(t_2|x,t_1)
$$

$$
p(t_3|x,t_1,t_2)
$$

$$
...
$$

in the same forward pass.

This is the core performance trick.

---

## 3. But can we simply accept the draft tokens?

No.

Suppose for one token:

```text
draft q:
A = 0.8
B = 0.2

target p:
A = 0.4
B = 0.6
```

The draft strongly prefers A, but the target prefers B.

If we blindly accepted the draft, we'd change the distribution of the target model.

Instead, speculative decoding uses a clever **accept/reject sampling rule**.

For a proposed token \\(x\\):

$$
a(x)=\min\left(1,\frac{p(x)}{q(x)}\right)
$$

So the draft token is accepted with probability:

$$
\boxed{\min(1,p(x)/q(x))}
$$

### Example

Draft:

$$
q(A)=0.8
$$

Target:

$$
p(A)=0.4
$$

Then:

$$
a(A)=\frac{0.4}{0.8}=0.5
$$

So A has a **50% chance of being accepted**.

---

### Another example

Draft:

$$
q(B)=0.2
$$

Target:

$$
p(B)=0.6
$$

Then:

$$
a(B)=\min(1,0.6/0.2)=1
$$

So B is **always accepted**.

This makes intuitive sense:

> If the target likes the token at least as much as the draft does, there is no reason to reject it.

---

# 4. What happens when a token is rejected?

This is the really elegant part.

Suppose the draft proposes:

```text
t1 t2 t3 t4 t5
```

and:

```text
t1 ✓
t2 ✓
t3 ✓
t4 ✗
```

We keep:

```text
t1 t2 t3
```

Then instead of throwing everything away, we sample the replacement token from a **residual distribution**:

$$
r(x)
=
\frac{\max(0,p(x)-q(x))}
{\sum_y\max(0,p(y)-q(y))}
$$

So:

$$
\boxed{
r(x)=
\frac{[p(x)-q(x)]_+}
{\sum_y[p(y)-q(y)]_+}
}
$$

where

$$
[z]_+=\max(0,z)
$$

This correction distribution contains probability mass that the target model has **more of than the draft model**.

---

# 5. Why does this preserve the target distribution?

This is the beautiful mathematical property.

For a token \\(x\\), there are two ways it can become the output:

### Accepted draft

The draft chooses \\(x\\) with probability \\(q(x)\\), and we accept it with:

$$
\min(1,p(x)/q(x))
$$

Therefore:

$$
q(x)\min(1,p(x)/q(x))
=
\min(q(x),p(x))
$$

So the accepted probability mass is:

$$
\min(p(x),q(x))
$$

### Rejection correction

The remaining probability mass is:

$$
p(x)-\min(p(x),q(x))
$$

which is exactly:

$$
[p(x)-q(x)]_+
$$

After normalization, the residual distribution gives exactly this missing mass.

Therefore:

$$
\underbrace{\min(p(x),q(x))}_{accepted}
+
\underbrace{[p(x)-q(x)]_+}_{correction}
=
p(x)
$$

Boom.

So the final sample is distributed according to **exactly \\(p\\)**.

That's why speculative decoding isn't merely an approximation.

---

# 6. The practical picture

Think of the target model as:

```text
        Large Model
       ┌─────────────┐
       │  70B / 400B │
       └──────┬──────┘
              │
        expensive pass
              │
              ▼
         1+ tokens
```

Speculative decoding adds:

```text
             Small model
             1B / 7B
                 │
          cheaply generate
                 │
          t1 t2 t3 t4 t5
                 │
                 ▼
        ┌─────────────────┐
        │   Large model   │
        │   verify all    │
        │   in one pass   │
        └─────────────────┘
                 │
          ✓ ✓ ✓ ✓ ✗
                 │
                 ▼
           emit 4 tokens
```

If the draft model is very good, you might get something like:

```text
Draft:    t1 t2 t3 t4 t5 t6
Target:   ✓  ✓  ✓  ✓  ✓  ✗
                         ↑
                    correction
```

Instead of **6 separate expensive target-model iterations**, you did approximately **one target-model verification iteration**.

---

# 7. Why this works particularly well for LLM inference

A decoder-only Transformer has two very different computational patterns.

**Autoregressive generation:**

```text
token 1 → forward
token 2 → forward
token 3 → forward
token 4 → forward
```

The dependency is sequential.

But when the tokens are already proposed:

```text
token 1
token 2
token 3
token 4
   ↓
one Transformer forward
```

the Transformer can process those positions simultaneously.

So speculative decoding converts some of the **sequential decoding problem into parallel verification**.

The GPU is much happier doing:

$$
\text{large matrix operations on several positions}
$$

than repeatedly launching the expensive target forward pass for one new token.

---

## 8. Connection to KV cache

This also connects directly to the KV-cache question you asked earlier.

During normal generation:

```text
KV cache: [old tokens]
              +
new token
              ↓
         target forward
              ↓
         new K,V added
```

With speculative decoding:

```text
KV cache: [old tokens]

draft model:
    generates t1 t2 t3 t4 t5

target:
    KV cache + [t1 t2 t3 t4 t5]
                    ↓
             one verification
                    ↓
              ✓ ✓ ✓ ✓ ✗
```

The target model can compute the K/V for the proposed sequence and evaluate all those next-token distributions in one pass.

That's why speculative decoding and KV caching are closely related in high-performance inference engines.

---

### The one-line mental model

> **Draft cheaply, verify in parallel, reject/correct statistically so the final distribution remains exactly the target model's distribution.**

The interesting engineering question after this is **how vLLM / TensorRT-LLM actually implements speculative decoding on CUDA**, including the attention mask, KV-cache handling, and why acceptance rate determines the real tokens/sec speedup. I can walk through that next with a minimal PyTorch implementation.