---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download FineWeb Dataset 100GB
translated: false
type: note
---

All good. Here's the command to run from `/workspace/zz`:

```bash
python3 scripts/download/h200/download_fineweb.py
```

That'll download **~100 GB** (25B tokens) to `datasets/fineweb-edu/`. Run it inside tmux so it survives disconnects:

```bash
tmux new -s fineweb
python3 scripts/download/h200/download_fineweb.py
# Ctrl+B D to detach
```

**Summary:**

- Script: `/workspace/zz/scripts/download/h200/download_fineweb.py`
- Output: `datasets/fineweb-edu/` (~100 GB)
- Disk: 178 GB free on `/workspace`
- Python 3.11.10, huggingface_hub 1.22.0
- Starting fresh (no previous progress on this volume)
