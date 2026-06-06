---
audio: false
generated: true
image: false
lang: en
layout: post
title: Async REPL conversion with prompt_async
translated: false
type: note
---

Here's the full breakdown of commit `f148313`:

**Title:** refactor: convert REPL loop to async with prompt_async

**What changed and why:**

The iclaw REPL was using `session.prompt()` (synchronous) from prompt_toolkit. This blocks the thread while waiting for user input, which is fine for simple CLIs but limits future extensibility — e.g., running background tasks, handling async tool callbacks, or integrating with async-native libraries.

**iclaw/main.py (2 changes):**

1. Added `import asyncio` at the top.
2. Split `main()` into two functions:
   - `main()` — thin wrapper that calls `asyncio.run(_main())`
   - `async _main()` — the actual REPL logic, now async
3. Changed `session.prompt("> ")` → `await session.prompt_async("> ")`

The rest of the REPL logic (tool-call loops, token refresh, command handling) remains synchronous inside the async function — `await` is only on the prompt call for now. This is a stepping stone: the async shell is in place, and individual operations can be migrated to `await` incrementally.

**tests/test_main.py (2 changes):**

1. `_mock_session()` — updated to mock `prompt_async` instead of `prompt`. Added an `async def _async_side_effect()` that yields inputs in order (raising exceptions for error inputs). Keeps `.prompt()` as a no-op fallback for safety.

2. `test_token_refresh` — the tricky one. `asyncio.run()` internally calls `time.monotonic()` for its shutdown/generator cleanup, which consumed entries from the `side_effect=[0, 99999, ...]` list unpredictably. Replaced the static side_effect list with a callable `_monotonic()` that tracks call count: returns `0` for the first 2 calls (asyncio internals + startup), then `99999` to trigger the token refresh check. This makes the test deterministic regardless of how many internal monotonic calls asyncio makes.

**Pre-commit:**
- First commit attempt failed — ruff fixed an unused `import asyncio` in the test file (it was added but `asyncio` wasn't directly called in the module scope; the async def uses it implicitly).
- Second attempt passed both ruff and ruff-format.

**Net effect:** +41 lines, -3 lines across 2 files. No behavior change for users — the REPL works exactly the same, just runs under an async event loop now.
