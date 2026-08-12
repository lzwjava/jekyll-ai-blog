---
audio: false
generated: false
image: false
lang: en
layout: post
title: Beyond Attention and Transformers
translated: false
---

This article is still a work in progress.

---

When I trained 13 small models using the scripts here (<https://github.com/lzwjava/zz>), what were my thoughts and learnings?

Each time, I learned a bit more. First, I used the fineweb-edu dataset, and then later the financial dataset and code.

Code is more deterministic. When training on code, there is a lot of empty space.

For financial data, we use SEC filings. We use a Hermes agent to help with training. One tip for long-running training or data preparation: we use an agent to generate the commands for us, and then we use tmux to open another terminal to run long-running jobs, so we can observe their progress more closely.

At one point, I used SFT to fine-tune the model. The SFT fine-tuning process also takes hours.

I also bought an AMD MI50 card — actually, it isn't exactly an MI50; it's a Radeon Pro VII. They have some differences. I returned it to the Xianyu seller by mutual agreement. And my original GPU, the RTX 4070, also had some issues with the motherboard, so it went back to the factory for repair with a BIOS reset.

---

Q is the query vector, representing the question or the information we are looking for.

K is the representation of the token itself — its meaning or features — used for matching with Q.

V is the actual information carried by the token, which will be aggregated based on the attention scores.

For example, if `hidden_size = 4096` and the number of attention heads is `32`, then:

`head_dim = hidden_size / num_heads = 4096 / 32 = 128`

The KV cache size should be approximately:

`sequence_length × num_heads × head_dim × 2`

(the `2` is because we store both K and V).

Q is also split across different heads. Each small q for one head is a vector/matrix whose dimension is related to `head_dim`.

My understanding of MLA (Multi-head Latent Attention) is that instead of keeping the full K/V information after projection (which would require large `hidden_size × hidden_size` representations), it compresses K/V into a lower-dimensional latent representation first. During attention computation, this latent representation is used and can be projected back when needed.

I am still a bit confused about some details, but anyway, thanks for the discussion!

---

Q's shape is like hidden_size. If the number of heads is 12 and head_dim is 64, then hidden_size is 768.

Q will be divided into small q's. Wq is the weight matrix for q, which means that...

Every Q is first passed through nn.Linear(n_embd, n_embd), and there is a WQ weight matrix for them. WQ is computed and trained for Q.

K and V are the same; they are all trained out.
