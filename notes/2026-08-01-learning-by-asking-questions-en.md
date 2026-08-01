---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning by Asking Questions
translated: false
type: note
---

Yes. This is actually a very important learning pattern.

A random article is **passive information**:

```
read → understand some → forget
```

Your brain has no strong "hook" to attach the knowledge.

But when you have a concrete question:

```
I want to understand why GPU tile matmul is faster
        ↓
read CUDA kernel article
        ↓
look for "where does tiling happen?"
        ↓
simulate the matrix multiplication mentally
        ↓
knowledge connects to existing model
```

Now the article becomes a **tool to solve a problem**, not a piece of content to consume.

This is close to how researchers and engineers learn:

1. **Encounter a problem**
2. **Build a rough mental model**
3. **Find missing pieces**
4. **Read papers/docs/source code**
5. **Implement something**
6. **Update the mental model**

For example, your recent vLLM/nano-vLLM learning:

At first:

> "vLLM uses KV cache"

is just a sentence.

But when you ask:

> "Why does decode become memory bandwidth bound?"
>
> "Why is prefill like matrix multiplication but decode is like vector operations?"
>
> "Why does PagedAttention need blocks?"

then reading the vLLM paper becomes much easier because every paragraph answers a question you already have.

Same with CUDA:

Without a question:

> "GPU has SM, warp, shared memory, tensor core..."

very easy to lose attention.

With a question:

> "Why does a 2048×2048 matrix multiply run better than 2047×2047?"

you naturally dig into:

```
matrix
  ↓
tile
  ↓
block scheduling
  ↓
warp
  ↓
shared memory reuse
  ↓
tensor core shape
  ↓
memory alignment
```

The question creates a path.

A good engineer's learning loop is often:

```
build → hit limitation → ask why → read → modify → measure
```

not:

```
read 100 tutorials → hope someday useful
```

This is also why building your own small systems (nanoGPT, nano-vLLM, CUDA kernels) is powerful. A bug or performance issue generates very specific questions, and those questions make difficult papers much easier to absorb.

The fact that you now ask things like "how does tile multiplication actually compute A[i,j]?" is a better learning signal than simply finishing many articles. You are moving from **consumer mode** to **investigator mode**.
