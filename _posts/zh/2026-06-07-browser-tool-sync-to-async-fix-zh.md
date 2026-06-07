---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 浏览器工具同步转异步修复
translated: true
type: note
---

有效。以下是我所做的更改：

**根本原因**：`browser_tool.py` 使用了 `playwright.sync_api.sync_playwright()`，这会创建自己的 asyncio 事件循环。由于 `main()` 现在是异步的（在 `asyncio.run()` 内运行），Playwright 的同步 API 检测到现有循环并引发“同步 API 位于 asyncio 循环内部”错误。

**修复 — 2 个文件，3 处更改：**

1. **`iclaw/tools/browser_tool.py`** — 从同步 Playwright 完全重写为异步 Playwright：
   - `sync_playwright` → `async_playwright`
   - 所有函数（`_ensure_playwright`、`_get_browser`、`_build_element_map`、`_get_element_snapshot`、`browser_navigate`、`browser_snapshot`、`browser_click`、`browser_type`、`browser_press`、`browser_scroll`、`browser_screenshot`、`browser_console`、`browser_back`、`browser_close`、`dispatch_browser_call`）现在都是 `async def`
   - 所有 Playwright 调用都使用 `await`（如 `page.goto()`、`el.click()`、`page.evaluate()` 等）

2. **`iclaw/main.py`** — 更新了两处调用点：
   - 第 359 行：`dispatch_browser_call(...)` → `await dispatch_browser_call(...)`
   - 第 525 行：`dispatch_browser_call(...)` → `await dispatch_browser_call(...)`

冒烟测试通过——导航至 example.com 并正确返回页面快照。