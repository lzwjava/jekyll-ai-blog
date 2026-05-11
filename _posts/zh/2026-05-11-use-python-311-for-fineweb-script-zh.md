---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Python 3.11运行FineWeb脚本
translated: true
type: note
---

使用 **`python3.11`** — 它已安装 `huggingface_hub` (0.28.1)，脚本可以正常运行。

当前系统上的 Python 环境：
- `/usr/bin/python3` → `python3.12`（没有 `huggingface_hub`）
- `/usr/bin/python3.11` ✅ 包含 `huggingface_hub`
- `/home/linuxbrew/.linuxbrew/bin/python3.14`（没有 `huggingface_hub`）
- 没有任何地方有 `python3.13` — 这就是为什么你的 `python` 软链接失败的原因。

运行方式如下：
```
python3.11 scripts/download/plan_and_download_fineweb_gpt3.py
```

如果你希望让 `python` 正常工作，可以创建符号链接，或者将依赖安装到 3.12 中：
```
python3.12 -m pip install -r requirements.txt
```