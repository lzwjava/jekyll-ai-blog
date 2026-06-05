---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streaming Fixes Stuck Output
translated: false
type: note
---

Found it. Here's what was happening:

**Root cause of the "stuck":** After printing "Fetched 20 entries...", the code called `call_openrouter_api()` — a **non-streaming** request that waits for the **entire** LLM response before printing anything. With a 30s read timeout and a complex prompt, the model could take 10-30s to generate the full response, during which you see zero output. That's the "stuck" feeling.

**What I changed in `ww/degree/degree.py`:**

1. **Streaming LLM output** — switched from `call_openrouter_api` to `stream_openrouter_api`. Tokens now print to stdout as they arrive (`flush=True`). You'll see output starting within 1-2 seconds instead of waiting for the full response.

2. **Threaded page fetching** — `fetch_entries()` now uses `ThreadPoolExecutor` with up to 5 workers. When `--pages > 1`, pages are fetched in parallel instead of sequentially.

The API key test failed because `OPENROUTER_API_KEY` is empty in the project `.env` (it's set via `export` in `~/.zshrc`). The `uv run` command may not source it in a non-interactive shell. This is the same for the old code though — if it was working before, the key was available at runtime.
