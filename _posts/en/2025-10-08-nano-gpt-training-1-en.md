---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Default nanoGPT Training Iterations
translated: false
type: note
---

In the default configuration for nanoGPT (e.g., training on the Shakespeare character dataset), the model runs for a total of **5000 iterations**.

This is set by `max_iters = 5000` in the `config/train_shakespeare_char.py` file. You can override it via the command line with `--max_iters=<value>` when running `train.py`.

[config/train_shakespeare_char.py](https://huggingface.co/nindanaoto/nanoGPT-BitNet158b/blob/main/config/train_shakespeare_char.py)
