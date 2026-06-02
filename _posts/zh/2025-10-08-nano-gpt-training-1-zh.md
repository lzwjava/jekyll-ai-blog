---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 默认nanoGPT训练迭代次数
translated: true
type: note
---

在nanoGPT的默认配置中（例如使用莎士比亚字符数据集进行训练），模型总共运行**5000次迭代**。

这由`config/train_shakespeare_char.py`文件中的`max_iters = 5000`参数设定。您可以在运行`train.py`时通过命令行参数`--max_iters=<数值>`来覆盖该设置。

[config/train_shakespeare_char.py](https://huggingface.co/nindanaoto/nanoGPT-BitNet158b/blob/main/config/train_shakespeare_char.py)
