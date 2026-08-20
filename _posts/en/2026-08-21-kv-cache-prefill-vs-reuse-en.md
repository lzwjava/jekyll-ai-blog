---
audio: false
generated: true
image: false
lang: en
layout: post
title: KV Cache Prefill vs Reuse
translated: false
type: note
---

Question: How does KV cache prefill work in LLM inference, and does it mean the KV cache is always the same regardless of input?

Answer:

Not quite — let me clarify the distinction between **prefill** (the phase) and **KV cache reuse** (the optimization).

---

**Prefill Phase (what it always means)**

In LLM inference, every request goes through two phases:

1. **Prefill** — the model processes the entire input prompt in parallel, computing attention keys and values for every token. This produces the initial KV cache.
2. **Decode** — the model generates tokens one at a time, appending to the KV cache as it goes.

So "prefill" just means *processing the prompt upfront*, not that the cache is fixed.

---

**KV Cache Reuse (what you're thinking of)**

You *can* reuse KV cache across requests, but only when **the prefix is identical**. This is called **prefix caching** (or prompt caching):

```
Shared prefix:  [System prompt tokens] → KV computed once, cached ✅
Request A:      [System prompt] + [User query A] → only query A is prefilled
Request B:      [System prompt] + [User query B] → only query B is prefilled
```

The cached KV blocks are **content-dependent** — they're tied to specific token sequences. Different inputs produce different KV values because attention keys/values are computed from the token embeddings.

---

**Why the KV can't be "input-independent"**

The K and V matrices are:

```
K = W_k · x
V = W_v · x
```

Where `x` is the token embedding. Different tokens → different `x` → different K/V values. So the KV cache is **always a function of the specific input tokens**.

---

**What systems like RadixAttention / SGLang do**

They store KV cache in a **prefix tree (radix tree)**, so any request sharing a common prefix reuses those cached blocks. This is the practical realization of your intuition — you *can* skip recomputing the prefill for the shared part.

```
"You are a helpful assistant. Today is..."
        ↑ same across 1000 requests → compute once, reuse KV cache
```

---

References:
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104)
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
