---
audio: false
generated: true
image: false
lang: en
layout: post
title: Entropy in Large Language Models
translated: false
type: note
---

Question: What is entropy in the context of large language models (LLMs)?

Answer:

Entropy in LLMs refers to a measure of **uncertainty or randomness** in the model's probability distribution over possible next tokens. It comes from information theory (Shannon entropy) and is defined as:

**H(P) = −∑ P(x) · log P(x)**

Where P(x) is the probability assigned to each token x.

**What it means practically:**

- **High entropy** → the model is uncertain, spreading probability across many tokens (e.g., open-ended creative tasks)
- **Low entropy** → the model is confident, concentrating probability on a few tokens (e.g., factual or deterministic completions)

**Where entropy shows up in LLMs:**

| Context | Role |
| --- | --- |
| **Temperature sampling** | Temperature scales logits before softmax, directly controlling output entropy — higher temp = higher entropy |
| **Perplexity** | Perplexity = exp(H), a standard metric for how "surprised" the model is by a text sequence |
| **Training loss** | Cross-entropy loss measures how far the model's distribution is from the true distribution |
| **Top-p / Top-k sampling** | These methods implicitly trim the distribution to control effective entropy |

**Intuition:** If a model assigns 99% probability to one token, entropy ≈ 0 (very sure). If it spreads probability evenly across 10,000 tokens, entropy is at its maximum (very unsure).

References:

- [Shannon Entropy – Wikipedia](https://en.wikipedia.org/wiki/Entropy_(information_theory))
- [Perplexity of a Language Model – Hugging Face Docs](https://huggingface.co/docs/transformers/perplexity)
- [Temperature and Sampling in LLMs – Lilian Weng's Blog](https://lilianweng.github.io/posts/2021-03-21-lm-bpe/)
