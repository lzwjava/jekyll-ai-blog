---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 CPU Inference Works
translated: false
type: note
---

It works! Here's the summary:

- Installed PyTorch (CPU-only) and transformers
- Loaded pretrained GPT-2 (124M params) from HuggingFace
- Generated 3 samples of 100 tokens each on CPU

The model loaded successfully and produced text. Since there's no GPU, it ran on CPU which is slower but functional.

To run again with a custom prompt:

    python3 sample.py --init_from=gpt2 --device=cpu --num_samples=1 --max_new_tokens=200 --start="Once upon a time"

For a larger model you can try gpt2-medium, gpt2-large, or gpt2-xl (but they'll be slower on CPU).