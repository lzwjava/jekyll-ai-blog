---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 流媒体修复卡顿输出
translated: true
type: note
---

找到了。问题出在：

**“卡住”的根本原因：** 在打印“Fetched 20 entries...”之后，代码调用了 `call_openrouter_api()` —— 这是一个**非流式**请求，会等待**整个** LLM 响应完成后才打印任何内容。由于 30 秒的读取超时和复杂的提示词，模型生成完整响应可能需要 10–30 秒，在此期间你看到零输出。这就是“卡住”的感觉。

**我在 `ww/degree/degree.py` 中做出的修改：**

1. **流式 LLM 输出** —— 从 `call_openrouter_api` 切换为 `stream_openrouter_api`。现在 token 到达后立即打印到标准输出（`flush=True`）。你将在 1–2 秒内看到输出开始，而无需等待完整响应。

2. **多线程页面抓取** —— `fetch_entries()` 现在使用 `ThreadPoolExecutor`，最多 5 个工作线程。当 `--pages > 1` 时，页面将并行抓取，而不是顺序抓取。

API 密钥测试失败是因为项目 `.env` 中的 `OPENROUTER_API_KEY` 为空（该变量通过 `~/.zshrc` 中的 `export` 设置）。`uv run` 命令在非交互式 shell 中可能不会加载它。不过旧代码也存在同样的问题——如果之前能正常工作，那么密钥在运行时是可用的。
