---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb-Edu Download Setup
translated: false
type: note
---

Done. Here's what's set up:

**Script:** `~/zz/scripts/download/h200/download_fineweb.py`

- Downloads FineWeb-Edu for GPT-3 ablation on AMD MI300X
- Default: ~25B tokens (~100 GB)
- Resumable via `datasets/fineweb-edu/progress.json`
- Run from `~/zz` with: `python3 scripts/download/h200/download_fineweb.py`

**tmux:** installed (3.2a)

**Smoke check:** passed — connected to HuggingFace, listed shards, downloaded at ~68 MB/s. When you're ready for the real download, run it in a tmux session so it keeps going after you disconnect:

```bash
cd ~/zz
tmux new -s fineweb
python3 scripts/download/h200/download_fineweb.py
# Ctrl+B D to detach, tmux attach -t fineweb to reattach
```

Available flags: `--tokens <N>` for custom amount, `--refresh-plan` to re-list shards, `--output-dir <path>` to change destination.
