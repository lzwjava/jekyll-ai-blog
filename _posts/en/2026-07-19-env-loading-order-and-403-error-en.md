---
audio: false
generated: true
image: false
lang: en
layout: post
title: Env Loading Order and 403 Error
translated: false
type: note
---

Here's the env loading order in `ww/env/__init__.py`:

1. **`~/.config/ww/.env`** — base defaults (override=False)
2. **`$CWD/.env`** — current working directory overrides (override=False)
   → you ran from `/Users/lzwjava/projects/jekyll-ai-blog`, so it checks `jekyll-ai-blog/.env`
3. **`/Users/lzwjava/projects/ww/.env`** — project root (override=False)
4. **`BASE_PATH` env var** — if set, loads `$BASE_PATH/.env` (override=True)

All three `.env` files load with `override=False` — meaning if a variable is **already set** from an earlier source, later files won't override it. Only `BASE_PATH` uses `override=True`.

So if your `~/.config/ww/.env` already has `VISION_MODEL=google/gemini-2.5-flash-image`, changing it in `/Users/lzwjava/projects/ww/.env` won't take effect — the earlier load wins.

The 403 error itself is an **OpenRouter ToS rejection** for `google/gemini-2.5-flash-image` — Google models on OpenRouter require explicit opt-in to their terms of service on the provider's side. This isn't a `.env` issue per se, but switching to a non-Google vision model would fix it.

To fix either:
- **Check your `~/.config/ww/.env`** — if `VISION_MODEL` is set there, change it there (it loads first, blocks the project root)
- **Or set a different vision model** like `openai/gpt-4o-mini` or `anthropic/claude-3-5-sonnet-20241022` in whichever `.env` file loads first

Want me to check what's in `~/.config/ww/.env`?
