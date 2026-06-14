---
audio: false
generated: true
image: false
lang: en
layout: post
title: Liquid Tag Build Fix
translated: false
type: note
---

Build is GREEN! 🎉

```
status: completed
conclusion: success
```

Here's the summary of what happened:

Root cause: Posts about the fine-tuning pipeline contained bare `{% %}` in text (describing Liquid tag syntax). Liquid tried to parse it as an unterminated tag and crashed the build.

Three commits, two distinct fixes:

1. `_posts/en|zh/2026-06-12-fine-tuning-pipeline-*` and `notes/2026-06-12-*` — these files have NO raw wrapper, so the bare `{% %}` needed inline escaping: `{% raw %}{% %}{% endraw %}`

2. `_posts/en|zh/2026-06-14-fine-tuning-qwen3-*` and `notes/2026-06-14-*` — these files already have a file-level `{% raw %}` wrapper (line 14 to end). My initial fix of adding inline `{% raw %}{% %}{% endraw %}` actually BROKE them by prematurely closing the outer raw block. Reverted to original `{% %}` which is safe inside the existing wrapper.
