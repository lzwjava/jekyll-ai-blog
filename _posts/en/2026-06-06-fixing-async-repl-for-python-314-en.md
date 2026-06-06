---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing async REPL for Python 3.14
translated: false
type: note
---

22 pass, 1 pre-existing failure (unrelated — your config has `search_provider: "bing"` but the test hardcodes `"duckduckgo"`).

Here's what I changed:

**iclaw/main.py** — 3 edits:
1. Added `import asyncio`
2. Split `main()` into a sync wrapper (`main()` calls `asyncio.run(_main())`) and an async `_main()` function
3. Changed `session.prompt("> ")` to `await session.prompt_async("> ")`

**tests/test_main.py** — 2 edits:
1. Updated `_mock_session()` to mock `prompt_async` (async function) instead of just `prompt`
2. Fixed `test_main_token_refresh` — replaced finite `side_effect=[0, 99999, 99999, 99999]` list with a callable, since `asyncio.run()` now also calls `time.monotonic()` internally (because `patch("iclaw.main.time.monotonic")` patches the real `time.monotonic` globally)

**Root cause**: Python 3.14 made `asyncio.run()` stricter — it raises `RuntimeError` when called from within a running event loop. prompt_toolkit 3.0.52's `Application.run()` calls `asyncio.run()`, but the browser tool's Playwright sync API (or the previous prompt_toolkit iteration itself) left an event loop running. By making the REPL async with `prompt_async()`, there's a single event loop for the entire session.
