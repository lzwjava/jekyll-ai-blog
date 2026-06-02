---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超时与错误处理改进
translated: true
type: note
---

已完成。以下是所有 3 个文件的更改摘要：

**1. `/Users/lzwjava/projects/ww/ww/llm/openrouter_client.py`**

- 为 `requests.post()` 添加了 `timeout=(5, 30)` —— 5 秒连接超时，30 秒读取超时（之前：无超时导致永远挂起）
- 对流式端点做了相同修复

**2. `/Users/lzwjava/projects/ww/ww/note/create_note_from_clipboard.py`**

- 将空/短内容时的 `sys.exit(1)` 替换为 `raise ValueError(...)` （之前：会终止整个 Hermes CLI）
- 移除了未使用的 `sys` 导入

**3. `/Users/lzwjava/projects/ww/ww/note/create_note_utils.py`**

- 在 `_call_llm_or_exit()` 中将 `sys.exit(1)` 替换为 `raise RuntimeError(...)` （之前：LLM 失败时会终止 CLI）
- 移除了未使用的 `traceback` 和 `sys` 导入

**4. `/Users/lzwjava/.hermes/plugins/note/__init__.py`**

- 添加了 `import os`
- 当 dotenv 未填充 MODEL 环境变量时，添加了从 `~/projects/ww/.env` 加载的后备方案
- 添加了 `print("Generating title via LLM...")` 以便用户看到反馈
- 添加了内容验证错误的 `ValueError` 捕获（返回清晰消息而非 traceback）

再次尝试运行 `/note` —— 你现在会立即看到 "Generating title via LLM..."，并且如果 API 响应慢，30 秒后会超时，而不是永远挂起。
