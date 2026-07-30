---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python venv 符号链接已确认
translated: true
type: note
---

你说得对。`.venv` 只是指向系统版本的一个符号链接——它们是一样的：

```
.venv/bin/python3.12 -> /usr/bin/python3.12
```

所以两种方式都可行。而且系统的 `python3.12` 已经安装了所有依赖：

- torch 2.11.0 ✅
- flash-attn 2.8.3 ✅
- triton 3.6.0 ✅
- transformers 5.12.1 ✅
- xxhash 3.8.1 ✅

因此只需：

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py
```

无需激活虚拟环境。
