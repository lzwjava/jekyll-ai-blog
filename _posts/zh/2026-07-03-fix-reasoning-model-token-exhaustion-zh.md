---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复推理模型令牌耗尽
translated: true
type: note
---

应用了两个更改。以下是总结：

**根本原因**：`deepseek/deepseek-v4-flash` 是一个推理模型。它会在生成实际 `content` 之前，先在 `reasoning` 字段输出思维链。当 `content` 为 `null` 且 `finish_reason` 为 `"length"` 时，模型在推理过程中耗尽了 token 预算，因此未能输出回答。

**修复**（两个文件均在 `/home/xiaoxin/projects/ww/` 中）：

1. **`ww/llm/openrouter_client.py`** — 当 `content` 为 `null` 时，改为回退到 `reasoning` 字段，而不是直接崩溃。此时会打印一条警告，以便您知晓发生了该情况，但笔记仍然会被创建。

2. **`ww/note/create_note_utils.py`** — 将标题生成中的 `max_tokens` 从 1024 增加到 4096，为推理模型提供足够的空间，使其既能进行推理（`reasoning`），又能生成 6 个词的标题（`content`），而不会耗尽预算。

如果监控器/处理器已在运行，您需要重启它才能使更改生效（按 `Ctrl+C` 停止监控器，然后再次运行 `ww note watch`）。
