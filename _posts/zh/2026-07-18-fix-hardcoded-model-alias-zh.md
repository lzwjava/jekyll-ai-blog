---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复硬编码的模型别名
translated: true
type: note
---

已修复并推送（`b515650`）。

错误原因：`x_bulk_unfollow.py` 中硬编码了 `model="gemini-flash"` —— 这只是一个别名，并非有效的 OpenRouter 模型 ID。OpenRouter 要求使用完整标识符，例如 `google/gemini-2.5-flash`。现已改为 `model=None`，这样 `call_openrouter_api_with_messages` 会回退使用你的 `MODEL` 环境变量（`deepseek/deepseek-v4-flash`）。重新运行 `ww x unfollow` 即可正常执行。