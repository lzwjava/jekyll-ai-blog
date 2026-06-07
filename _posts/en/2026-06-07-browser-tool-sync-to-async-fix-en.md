---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser Tool Sync to Async Fix
translated: false
type: note
---

Works. Here's what I changed:

**Root cause**: `browser_tool.py` used `playwright.sync_api.sync_playwright()` which creates its own asyncio event loop. Since `main()` is now async (running inside `asyncio.run()`), Playwright's sync API detects the existing loop and raises "Sync API inside the asyncio loop."

**Fix — 2 files, 3 changes:**

1. **`iclaw/tools/browser_tool.py`** — full rewrite from sync to async Playwright:
   - `sync_playwright` → `async_playwright`
   - All functions (`_ensure_playwright`, `_get_browser`, `_build_element_map`, `_get_element_snapshot`, `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_press`, `browser_scroll`, `browser_screenshot`, `browser_console`, `browser_back`, `browser_close`, `dispatch_browser_call`) are now `async def`
   - All Playwright calls use `await` (`page.goto()`, `el.click()`, `page.evaluate()`, etc.)

2. **`iclaw/main.py`** — two call sites updated:
   - Line 359: `dispatch_browser_call(...)` → `await dispatch_browser_call(...)`
   - Line 525: `dispatch_browser_call(...)` → `await dispatch_browser_call(...)`

Smoke test passes — navigates to example.com and returns the page snapshot correctly.
