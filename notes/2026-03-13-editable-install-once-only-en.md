---
audio: false
generated: true
image: false
lang: en
layout: post
title: Editable Install Once Only
translated: false
type: note
---

`pip install -e .` only needs to be run **once**. After that, code changes are reflected immediately — just run `mini-copilot` again, no reinstall needed (editable installs symlink to your source).

Alternatively, skip install entirely and run directly:

```bash
python -m mini_copilot.main
```

This works from the project directory without any install step.