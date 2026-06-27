---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中断模型上传恢复
translated: true
type: note
---

以下是状态：

**分析（已完成）**

- 模型：GPT-2 124M（12层，768隐藏单元，12头，1024上下文，词汇量50257）
- 文件：config.json、generation_config.json、tokenizer.json、tokenizer_config.json、model.safetensors（622MB float32）
- 缺失：README.md（模型卡片）— 已修复，上传到服务器

**上传进度**

- 仓库已创建：<https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf> ✓
- 服务器上已安装 hf CLI（47.86.12.246） ✓
- HF token 已配置 ✓
- README.md（模型卡片）已创建并复制到服务器 ✓
- 上传已开始 — model.safetensors 上传至 133MB/622MB 时中断（信号15，可能是 SSH 超时）

**剩余任务**

- 恢复上传。小文件（5/6）已传输完成，仅剩 model.safetensors（约489MB）

是否要恢复上传？我会在后台运行，避免超时：

```bash
ssh root@47.86.12.246 "nohup hf upload lzwjava/sec-edgar-gpt-124m-hf ~/sec-edgar-gpt-124m-hf/ > /tmp/hf-upload.log 2>&1 &"
```

或者我现在可以用更长的超时时间开始。您更倾向于哪种？
