---
audio: false
generated: true
image: false
lang: en
layout: post
title: "KV Cache: Speed via Memory"
translated: false
type: note
---

**KV cache (Key-Value cache)** is a technique used during inference in large language models (LLMs) to avoid recomputing work for tokens the model has already processed. It significantly speeds up text generation.

### The intuition

Imagine you're writing a sentence one word at a time:

> "The cat sat on the..."

To predict the next word, the model needs to consider all previous words:

* The
* cat
* sat
* on
* the

Without a KV cache, every time a new word is generated, the model would reprocess the entire sequence from scratch.

With a KV cache, the model remembers the important intermediate computations for the previous tokens and only computes them for the newly generated token.

---

## Why "Key" and "Value"?

LLMs use **self-attention**. For every token, the model computes three vectors:

* **Query (Q)** – what the current token is looking for
* **Key (K)** – what each previous token represents
* **Value (V)** – the information each token contains

The attention formula is roughly:

$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
$$

During generation:

* Keys and values for old tokens never change.
* Only the newest token needs new K and V vectors.

So instead of recomputing K and V for every previous token, we **cache** them.

---

## Without KV cache

Suppose the prompt has 1000 tokens.

Generating token 1001:

* Compute K/V for tokens 1–1000
* Compute Q for token 1001
* Perform attention

Generating token 1002:

* Compute K/V again for tokens 1–1001
* Compute Q for token 1002
* Perform attention

This repeats over and over.

---

## With KV cache

After processing the prompt once:

```
KV Cache

Token 1  -> K1, V1
Token 2  -> K2, V2
...
Token1000 -> K1000, V1000
```

When generating token 1001:

* Compute only:

  * Q1001
  * K1001
  * V1001
* Use cached K1...K1000 and V1...V1000.

Then append:

```
Token1001 -> K1001, V1001
```

Repeat for the next token.

---

## Visualization

Without cache:

```
Prompt
  ↓
Transformer
  ↓
Generate token 1

Prompt + token1
      ↓
Transformer
      ↓
Generate token2

Prompt + token1 + token2
           ↓
Transformer
```

Everything is recomputed.

With cache:

```
Prompt
   ↓
Compute K,V once
Store in cache

Generate token1
Compute only K,V for token1
Append to cache

Generate token2
Compute only K,V for token2
Append to cache
```

Only incremental work is done.

---

## Performance benefits

KV caching:

* 🚀 Reduces computation dramatically during autoregressive decoding.
* ⚡ Lowers latency per generated token.
* 📈 Increases tokens generated per second.

This is why nearly all production LLM serving systems (e.g., vLLM, TensorRT-LLM, and Hugging Face Text Generation Inference) use KV caching.

---

## Memory cost

The trade-off is memory.

Each generated token stores K and V tensors for **every transformer layer**.

The cache size grows roughly as:

$$
\text{Cache size} \propto
\text{sequence length}
\times
\text{number of layers}
\times
\text{hidden size}
$$

For long contexts (e.g., 128K or 1M tokens), the KV cache can consume tens or even hundreds of gigabytes of GPU memory, which is why techniques like **KV cache quantization**, **paged KV cache**, and **cache eviction** are used in modern inference systems.

---

## During training vs. inference

* **Training:** KV caching is generally **not used**, because all tokens are processed in parallel and gradients must flow through the full computation graph.
* **Inference:** KV caching is essential because tokens are generated sequentially, one at a time.

---

## A simple analogy

Imagine reading a book and taking notes after each chapter.

* **Without KV cache:** Every time someone asks about the next chapter, you reread the entire book from page 1.
* **With KV cache:** You keep your notes from earlier chapters and only read the new chapter before updating your notes.

The notes are analogous to the cached **keys** and **values**, allowing the model to avoid repeating work while still attending to the full history.
