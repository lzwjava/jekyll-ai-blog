---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shared Token Embeddings in GPT Models
translated: false
type: note
---

Question: In the GPT series, does every token have a fixed, shared embedding? Is there a common embedding table used across the model?

Answer:

Yes — and no. Let me clarify the nuance carefully, because the answer has two layers.

---

## 1. Yes: Every Token Has One Row in a Shared Lookup Table

In the Transformer architecture, the first layer embeds the token IDs by using a **lookup table** that contains the embedding for each possible token. A token embedding is a vector of a certain length that represents the meaning of the token.

So concretely, for GPT-2 which has a vocabulary of ~50,000 tokens:

The size of the embedding matrix is `(50,000 × 768)` for small models, where there are 50,000 tokens and 768 dimensions.

This means every token ID (e.g., token #1234 = `" cat"`) **maps to exactly one row** in this matrix. It is a simple lookup — no computation, just retrieve the row. This is the "fixed" part you're thinking of: once training is done, each token's row in the table is frozen.

---

## 2. But "Fixed" Only After Training — They Are Learned, Not Predefined

Here is the critical point: these embeddings are **not hand-crafted or pre-set**. They are learned from scratch during training.

These embeddings are **learned during the training** of the entire Transformer model. They are **not predefined or fixed in advance** — they are learned as part of the model's training process. They are initialized with random values and are part of the model's learnable parameters. During training, they are updated through backpropagation.

During model training (like next-word prediction in GPT), the embeddings are updated through backpropagation. Only the rows corresponding to the tokens in the current batch are adjusted. Over many iterations, the model learns to adjust these vectors so that words appearing in similar contexts (like "cat" and "dog") have similar embeddings, while unrelated words move further apart in vector space.

So the lifecycle looks like this:

| Phase | State of Embedding |
| --- | --- |
| Before training | Random noise vectors |
| During training | Continuously updated via backprop |
| After training (inference) | Frozen — each token has one fixed vector |

---

## 3. This Is Different from Word2Vec

Word2Vec trains embeddings **separately** as a standalone step, then you plug them into your model. GPT trains the embedding table **end-to-end together** with all the transformer weights — the embedding is just another weight matrix in the full model.

Embeddings in GPT-style Transformers are **not a standalone feature to be trained separately** — they are trained right alongside the rest of the model. Every time the network backpropagates, it updates the embedding vectors to better capture word relationships needed for accurate predictions. At inference, each token's learned vector is retrieved with a single lookup, ready for the self-attention machinery.

---

## 4. One Important Modern Detail: Input Embedding ≠ Output Embedding

In the era of GPT-2, the input embedding and the output unembedding were the same. Nowadays, embedding and unembedding matrices are **learned separately**.

This means:

- **Input side**: token ID → embedding vector (fed into attention layers)
- **Output side**: the final hidden state → projected back to vocabulary logits (a separate matrix)

They were once tied together (same weights), but modern models separate them for better performance.

---

## Summary

- Yes, there is **one shared embedding table** — one row per token in the vocabulary
- Each token always maps to **the same vector** (after training), so it is "fixed" at inference time
- But those vectors are **not pre-fixed** — they are learned end-to-end during training, just like any other weights
- The embedding table is essentially `nn.Embedding(vocab_size, d_model)` in PyTorch — a learnable matrix initialized randomly

References:

- [Token Embeddings and Positional Embeddings Explained – Cloud-ML](https://cloud-ml.de/llm-token-embeddings/)
- [From One-Hot to Learned Representations: GPT-Style Embeddings](https://medium.com/@nsimaria_83213/from-one-hot-to-learned-representations-understanding-gpt-style-embeddings-ec096f47270d)
- [LLM Basics: Embedding Spaces – LessWrong](https://www.lesswrong.com/posts/pHPmMGEMYefk9jLeh/llm-basics-embedding-spaces-transformer-token-vectors-are)
- [Token Embeddings – Angel Vyas](https://angelvyas.com/posts/llm/token_embeddings/)
