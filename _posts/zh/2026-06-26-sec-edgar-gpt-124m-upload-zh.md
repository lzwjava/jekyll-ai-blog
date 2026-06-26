---
audio: false
generated: true
image: false
lang: zh
layout: post
title: sec-edgar-gpt 124M上传
translated: true
type: note
---

已完成步骤：

- 创建仓库：<https://huggingface.co/lzwjava/sec-edgar-gpt（公开）>
- 上传：config.json, tokenizer.json, tokenizer_config.json, generation_config.json, README.md
- 将 nanoGPT 的 ckpt.pt（来自 ~/projects/nanoGPT/out-sec-edgar-124m/）转换为 HF safetensors 格式
- 移除了远程 .gitignore 文件，该文件曾阻止模型上传

剩余步骤：

- model.safetensors（498MB）——正在上传中，只需使用 no-proxy 来加快速度

模型详情：GPT-2 124M，基于 SEC-EDGAR 文件训练（15.5 亿 tokens，47K 次迭代，val_loss 2.28，RTX 4070 上约 8 小时）。

上传完成后，请在此处验证：<https://huggingface.co/lzwjava/sec-edgar-gpt>
