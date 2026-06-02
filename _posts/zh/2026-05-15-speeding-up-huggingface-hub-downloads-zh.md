---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 加速HuggingFace Hub下载
translated: true
type: note
---

慢速问题是 HuggingFace Hub 默认从 CDN 单流下载导致的——并非你的设置问题。以下是几种提速方案：

**1. 使用 `hf_transfer`（并行分块下载，通常快 5–10 倍）：**

```
pip install hf_transfer
HF_HUB_ENABLE_HF_TRANSFER=1 python3.11 sample.py --init_from=gpt2-medium ...
```

**2. 先用 CLI 预下载一次，之后 sample.py 会从缓存读取：**

```
huggingface-cli download gpt2-medium
```

**3. 如果你所在地区访问 huggingface.co 较慢（例如中国），可使用镜像站：**

```
HF_ENDPOINT=https://hf-mirror.com python3.11 sample.py --init_from=gpt2-medium ...
```

首次下载后文件会存储在 `~/.cache/huggingface/hub/` 目录下，后续运行将不再重复下载。你所在地区是哪里？这有助于判断是否值得尝试镜像站。
