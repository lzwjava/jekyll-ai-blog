---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Python 3.14 的异步 REPL
translated: true
type: note
---

22 通过，1 个预先存在的失败（无关——你的配置中设置了 `search_provider: "bing"`，但测试硬编码了 `"duckduckgo"`）。

以下是我所做的修改：

**iclaw/main.py** — 3 处编辑：
1. 添加了 `import asyncio`
2. 将 `main()` 拆分为同步包装器（`main()` 调用 `asyncio.run(_main())`）和异步函数 `_main()`
3. 将 `session.prompt("> ")` 改为 `await session.prompt_async("> ")`

**tests/test_main.py** — 2 处编辑：
1. 更新了 `_mock_session()`，使其模拟 `prompt_async`（异步函数）而不是仅模拟 `prompt`
2. 修复了 `test_main_token_refresh`——将有限的 `side_effect=[0, 99999, 99999, 99999]` 列表替换为可调用对象，因为 `asyncio.run()` 现在也会在内部调用 `time.monotonic()`（因为 `patch("iclaw.main.time.monotonic")` 全局性地修补了真实的 `time.monotonic`）

**根本原因**：Python 3.14 对 `asyncio.run()` 的执行更加严格——当从正在运行的事件循环中调用时，它会抛出 `RuntimeError`。prompt_toolkit 3.0.52 的 `Application.run()` 会调用 `asyncio.run()`，但浏览器工具的 Playwright 同步 API（或之前 prompt_toolkit 自身的迭代）使得事件循环保持运行。通过使用 `prompt_async()` 将 REPL 变为异步，整个会话只需一个事件循环。