---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinchilla Compute-Optimal Training Principle
translated: false
type: note
---

Question: What does "Chinchilla" mean in the context of "Chinchilla rule of thumb ~20 tokens/parameter for compute-optimal training"?

Answer:

In this context, **"Chinchilla"** refers to a **language model training principle** introduced by researchers at DeepMind in their 2022 paper on compute-optimal training of language models. It is not the animal! 🐿️

The key idea is:

* When training a transformer-based language model, there is a trade-off between **model size (parameters)** and **amount of training data (tokens)** for a fixed compute budget.
* The "Chinchilla rule of thumb" suggests that **for compute-optimal training, you should use roughly 20 tokens of training data per model parameter**. This is much more data than was traditionally used in GPT-3 style training.

Example:

* A model with **1 billion parameters** would need **~20 billion tokens** to train efficiently under this rule.
* Previous GPT-3 style models undertrained data per parameter (using fewer tokens relative to parameters), which meant they were not compute-optimal.

The note you quoted is saying that recent practices (like LLaMA, GPT-3 fine-tuning) often train models with **5–40× more data per parameter than the original Chinchilla guideline** to improve **inference-time quality**, even beyond pure compute efficiency.

References:

* [DeepMind Chinchilla Paper](https://arxiv.org/abs/2203.15556) – *Training Compute-Optimal Large Language Models*
* [Summary of Chinchilla vs GPT-3](https://lilianweng.github.io/posts/2022-03-31-chinchilla/)

If you want, I can also break down **why more tokens per parameter improves inference** in simple terms.
