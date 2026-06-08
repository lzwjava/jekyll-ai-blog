---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2 CPU推理运行
translated: true
type: note
---

成功了！以下是摘要：

- 安装了 PyTorch（仅CPU）和 transformers
- 从 HuggingFace 加载了预训练的 GPT-2（124M参数）
- 在 CPU 上生成了 3 个样本，每个 100 个 token

模型加载成功并生成了文本。由于没有 GPU，它在 CPU 上运行，速度较慢但功能正常。

要使用自定义提示再次运行：

    python3 sample.py --init_from=gpt2 --device=cpu --num_samples=1 --max_new_tokens=200 --start="Once upon a time"

对于更大的模型，你可以尝试 gpt2-medium、gpt2-large 或 gpt2-xl（但在 CPU 上会较慢）。