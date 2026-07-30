---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python venv symlink confirmed
translated: false
type: note
---

You're right. The `.venv` is just a symlink to the system one — they're the same thing:

```
.venv/bin/python3.12 -> /usr/bin/python3.12
```

So either way works. And the system's `python3.12` already has everything installed:

- torch 2.11.0 ✅
- flash-attn 2.8.3 ✅
- triton 3.6.0 ✅
- transformers 5.12.1 ✅
- xxhash 3.8.1 ✅

So just:

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py
```

No venv activation needed.