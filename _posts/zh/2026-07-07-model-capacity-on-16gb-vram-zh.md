---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 16GB显存下的模型容量
translated: true
type: note
---

现在我掌握了全部情况。让我总结一下这个Pod上的内容：

## 硬件：RunPod RTX 2000 Ada — 16 GB 显存

### 使用 SGLang 的模型容量

| 精度 | 最大参数量 | 模型示例 | 显存占用 |
|-----------|-----------|----------------|-----------|
| **FP16/BF16** | **7-8B** | LLaMA-3-8B, Mistral-7B, Qwen2.5-7B | ~16GB（长上下文时紧张） |
| **FP8/INT8** | **13-16B** | Llama-2-13B, DeepSeek-V2-Lite-16B, Qwen2.5-14B | ~8-9GB + KV缓存空间 |
| **INT4（AWQ/GPTQ）** | **30-34B** | Qwen2.5-32B, Yi-34B, CodeQwen-32B | ~8GB → 大量余量 |
| **INT4 72B** | **72B（勉强）** | Qwen2.5-72B-AWQ | ~14GB → 仅剩~2GB用于KV缓存 = 极短上下文 |

### 磁盘上的现有模型

你的 **SEC-EDGAR-GPT（124M）** 已经以 HuggingFace 格式存在于 `/workspace/model/hf-model/` —— 这是一个 628MB 的 safetensors 模型。对于 SGLang 来说非常小（仅占用 <1 GB 显存），因此你有充足的余量。

### 问题

你想部署哪个模型？选项：

1. **你已有的 SEC-EDGAR-GPT 124M** — 很简单，有大量余量
2. **一个新模型** — GPU 可处理高达 7-8B FP16 或 30B-34B INT4。选哪个？