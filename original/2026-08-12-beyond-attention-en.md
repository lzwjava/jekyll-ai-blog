---
audio: false
generated: false
image: false
lang: en
layout: post
title: Beyond Atention
translated: false
---

This article is still being working in progress.

---

Q is the query vector, representing the question or the information we are looking for.

K is the representation of the token itself — its meaning or features used for matching with Q.

V is the actual information carried by the token, which will be aggregated based on the attention scores.

For example, if `hidden_size = 4096` and the number of attention heads is `32`, then:

`head_dim = hidden_size / num_heads = 4096 / 32 = 128`

The KV cache size should be approximately:

`sequence_length × num_heads × head_dim × 2`

(the `2` is because we store both K and V).

Q is also split across different heads. Each small q for one head is a vector/matrix with dimension related to `head_dim`.

My understanding of MLA (Multi-head Latent Attention) is that instead of keeping the full K/V information after projection (which requires large `hidden_size × hidden_size` representations), it compresses K/V into a lower-dimensional latent representation first. During attention computation, this latent representation is used and can be projected back when needed.

I am still a bit confused about some details, but anyway, thanks for the discussion!
