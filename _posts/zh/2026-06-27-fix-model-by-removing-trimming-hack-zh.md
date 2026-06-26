---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移除修剪黑客以修复模型
translated: true
type: note
---

Here's my analysis:

## 当前状态（在 RunPod 上）

位于 `/workspace/model/hf-model/` 的模型具有 **vocab_size: 50304** —— 即原始 nanoGPT 填充后的词汇量（50257 填充至最近 64 的倍数以提升 CUDA 效率）。`server.py` 中有一个运行时修补措施，在加载时将嵌入从 50304 剪裁至 50257。这正是生成结果异常的根源——权重映射因该剪裁而损坏。

## 新模型（HF: lzwjava/sec-edgar-gpt-124m-hf）

**vocab_size: 50257** —— 已正确转换，为标准 GPT-2 词汇表。架构相同（124M，12 层，隐藏层 768，上下文长度 1024）。无需填充，无需剪裁。这正是它能正常工作的原因。

## `server.py` 中需要修改的内容

1. **删除整个嵌入剪裁块**（第 19-31 行）——不再需要，新模型词汇量正确
2. **保持其他一切不变** —— `MODEL_DIR`、API 端点、采样参数均保留
3. **将新模型下载到 RunPod** —— 替换 `/workspace/model/hf-model/` 下的内容

`server.py` 变得更简单：加载模型，提供服务。不再有修补代码。

需要我继续执行以下操作吗：

1. 更新本地的 `server.py`，移除剪裁修补
2. 通过 SSH 连接 RunPod，从 HF 下载新模型，然后重启服务器？

还是您想逐步操作？
