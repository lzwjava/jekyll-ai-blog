---
audio: false
generated: true
image: false
lang: en
layout: post
title: YouTube Upload Fixes and Updates
translated: false
type: note
---

Committed and pushed to `main` (ca2be2d).

**Summary of all fixes:**

1. **OAuth redirect_uri error** — removed the manual `flow.authorization_url()` call that was firing before the local server started. Now `run_local_server(port=8080)` handles the full flow, including the redirect_uri.

2. **YouTube invalidDescription error** — root cause was the `<` character in `(<$80)`. YouTube's API rejects `<` as potential HTML. Fixed by replacing `<` with `less than` in the `_clean_description()` function, plus stripping reference links, tables, code blocks, and other markdown artifacts.

3. **Pyright exclusion** — added `ww/gen_video/youtube_upload.py` to pyright's exclude list since the google packages aren't in its type-checking environment.

**Files changed:**

- `ww/gen_video/youtube_upload.py` — new (YouTube upload module)
- `ww/main.py` — subcommand routing + help text
- `pyproject.toml` — pyright exclusion + google-api-python-client dep
