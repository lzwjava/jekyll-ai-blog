---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Python 3.11 for FineWeb script
translated: false
type: note
---

Use **`python3.11`** — it has `huggingface_hub` (0.28.1) installed and the script runs cleanly with it.

What's on this box:

- `/usr/bin/python3` → `python3.12` (no `huggingface_hub`)
- `/usr/bin/python3.11` ✅ has `huggingface_hub`
- `/home/linuxbrew/.linuxbrew/bin/python3.14` (no `huggingface_hub`)
- No `python3.13` anywhere — that's why your `python` shim failed.

Run it as:

```
python3.11 scripts/download/plan_and_download_fineweb_gpt3.py
```

If you'd rather make `python` work, either symlink it or install deps into 3.12:

```
python3.12 -m pip install -r requirements.txt
```
