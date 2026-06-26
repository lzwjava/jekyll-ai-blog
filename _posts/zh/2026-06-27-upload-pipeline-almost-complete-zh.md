---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 上传流水线即将完成
translated: true
type: note
---

## 当前状态

### 模型

- **工作站** (`lzw@192.168.1.36`): 47k步检查点，已转换为HF格式，位于 `/tmp/sec-edgar-gpt-124m-hf/`（652MB）
- **RunPod**: 运行旧的20k步模型 → 输出垃圾内容

### 上传管道（进行中）

```
工作站 → SCP → 中继服务器 (47.86.12.246) → HuggingFace Hub
```

- SCP后台传输中：652MB的model.safetensors从工作站→中继服务器
- 中继服务器有31GB空闲磁盘，可访问HuggingFace
- 小文件（配置、分词器）也待上传

### 上传完成后

1. 在中继服务器上安装 `huggingface-hub`
2. 将所有文件上传至 `lzwjava/sec-edgar-gpt-124m`
3. 在RunPod执行：`huggingface-cli download lzwjava/sec-edgar-gpt-124m --local-dir /workspace/model/hf-model`
4. 重启server.py

### 您将看到的效果

```
之前（20k步）："ivableivableignedignedivable..."
之后（47k步）："The Company has a $2.2 million revolving credit facility..."
```

正在等待SCP完成——传输完成后我会立即继续。