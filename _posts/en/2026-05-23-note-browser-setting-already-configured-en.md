---
audio: false
generated: true
image: false
lang: en
layout: post
title: Note Browser Setting Already Configured
translated: false
type: note
---

The correct `.env` is the one in the `ww` project root:

  /Users/lzwjava/projects/ww/.env

And it's already set there (line 33):

  NOTE_BROWSER_OPEN=false

The `ww/env.py` loads this `.env` via `dotenv`, and `note_workflow.py` reads it with `os.getenv("NOTE_BROWSER_OPEN", "true")`. You're good — no changes needed, it's already `false`.

If you ever need to change it, edit `/Users/lzwjava/projects/ww/.env`. The jekyll-ai-blog `.env` is irrelevant for this setting — it's only used for `BASE_PATH`/`SCREENSHOT_DIR` via the extra env loading path.
