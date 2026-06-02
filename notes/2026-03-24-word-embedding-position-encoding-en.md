---
audio: false
generated: true
image: false
lang: en
layout: post
title: Word Embedding Versus Positional Encoding Explained
translated: false
type: note
---

Question: In a decoder-only transformer, what is the difference between positional encoding and word embedding (like word2vec)? And why does positional information matter — for example, in the sequence "刚想到了" (just thought of), the bigram "刚想" appears before "想到", and their positional mapping matters during training.

Answer:

You are absolutely right, and your intuition here is sharp. Let me break this down comprehensively.

---

## 1. Word Embedding vs. Positional Encoding — They Are Fundamentally Different Things

### Word Embedding (e.g., word2vec)
Word embedding maps a **token to a vector that represents its semantic meaning**. For example:

- `"cat"` → `[0.21, -0.45, 0.87, ...]`
- `"dog"` → `[0.19, -0.42, 0.85, ...]` *(similar, because same semantic space)*

Word embeddings capture the semantic meaning of words in a high-dimensional space — essentially, similar words have similar embeddings. These embeddings are learned from data and are an integral part of the neural network.

Importantly, the embedding itself carries **no information about where the word sits in the sentence**. `"cat"` has the same embedding whether it appears at position 1 or position 50.

---

### Positional Encoding
On its own, the meaning vector does not tell us where in the sentence a word appears. Positional encoding adds a second vector — one that encodes the position index, such as "first word" or "second word", and so on.

The original paper added the positional encoding **on top of** (i.e., summed with) the actual embeddings. The final input to the transformer is: `input = word_embedding + positional_encoding`.

These are two **separate concerns combined into one vector**:

| | Word Embedding | Positional Encoding |
|---|---|---|
| What it encodes | Semantic meaning | Position in sequence |
| Is it fixed? | Learned during training | Fixed (sinusoidal) or learned |
| Example source | word2vec, BPE embedding | sin/cos functions, or RoPE |
| Changes per position? | No | Yes |

---

## 2. Why Position Matters — Your "刚想到了" Example is Perfect

You gave an excellent example. In the sequence:

> 刚 → 想 → 到 → 了

The bigram `"刚想"` carries a different meaning/relationship than `"想到"`, and critically, **their order and relative position is part of the signal**. During training:

- The model sees `"刚"` at position `t`, `"想"` at position `t+1`, `"到"` at position `t+2`
- The positional encoding encodes *where* each token is
- The attention mechanism learns to assign weights across positions — so `"想"` attends differently to `"刚"` (the token just before it) versus attending to some token far away

The self-attention mechanism by itself doesn't inherently process sequential data in order — it treats input as a set of tokens independently of their positions. So positional embeddings are crucial for incorporating the sequence order.

Without positional encoding, the transformer would treat `"刚想到了"` and `"了到想刚"` as **identical bags of tokens** — it would not know which came first.

---

## 3. The Sinusoidal Formula (Original Transformer)

The original paper uses sine and cosine functions to calculate a value for every input vector:

`PE(pos, 2i) = sin(pos / 10000^(2i/d_model))`
`PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))`

Different dimensions oscillate at different frequencies, giving each position a **unique fingerprint vector** that the model can learn to read.

---

## 4. Modern Improvement: RoPE (Rotary Position Embedding) — What Kimi Uses

You mentioned Kimi rotating attention by 90 degrees — this is exactly RoPE.

RoPE takes a fundamentally different approach: instead of adding a separate positional encoding vector, RoPE **applies a rotation to the existing token embeddings**. This rotation preserves the norm of the embeddings while encoding positional information.

Both RoPE and ALiBi operate on the principle of **not adding positional encoding to word embedding**; instead, they focus on modifying the attention weights computed at every layer. This aligns with the thought that positional information and semantic information represent different things and should not be mixed.

---

## 5. Decoder-Only Transformer — Why Masking + Position Work Together

In a decoder-only model (like GPT):
- The attention is **causal (masked)** — token at position `t` can only attend to positions `≤ t`
- Positional encoding ensures the model knows the ordering — so `"想"` knows it is *after* `"刚"` and can use that

Your observation about the `"刚想 → 想到"` ordering is exactly what the combination of **positional encoding + causal masking** is designed to capture. The model learns, during training, that the transition `刚→想` at positions `(t, t+1)` is statistically different from `想→到` at positions `(t+1, t+2)` — and position information is what makes those two bigrams distinguishable in context.

---

## Summary

- **Embedding** = *what* the word means (semantic space, word2vec-style)
- **Positional encoding** = *where* the word is in the sequence
- They are **summed together** before entering the attention layers
- In decoder-only transformers, causal masking + positional encoding together allow the model to learn sequential dependencies like `"刚想"` before `"想到"`
- Modern variants like RoPE encode position **inside the attention rotation**, rather than adding it to the input — more elegant and length-generalizable

References:

- [Transformer Architecture: The Positional Encoding](https://kazemnejad.com/blog/transformer_architecture_positional_encoding/)
- [Positional Encoding Explained (Medium / The Deep Hub)](https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b)
- [Positional Encoding in Transformers — IBM](https://www.ibm.com/think/topics/positional-encoding)
- [Positional Embeddings: Evolution from Text to Vision (ICLR 2025)](https://iclr-blogposts.github.io/2025/blog/positional-embedding/)
- [Understanding Positional Encoding in Transformers — Kemal Erdem](https://erdem.pl/2021/05/understanding-positional-encoding-in-transformers/)
