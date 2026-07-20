---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM描述标志已添加
translated: true
type: note
---

已完成。更改位于 `ww/gen_video/youtube_upload.py`。以下是添加的内容：

**新标志 `--llm-description`** — 设置后，描述将由 OpenRouter 生成，而不是从笔记正文中提取。

**工作原理：**

- 解析 `--llm-description` 作为布尔标志（无值参数）
- 当设置此标志且未提供 `--description` 覆盖时，调用 `call_openrouter_api_with_messages`，使用针对 YouTube 描述定制的提示（纯文本，不超过 4000 字符，关键要点 + 话题标签）
- 如果 LLM 调用失败，则回退到现有的 `_clean_description(body)`
- `--description` 覆盖仍然具有最高优先级 — 仅在未给出显式描述时才执行 LLM 生成

**用法：**

```
ww gen-video upload notes/2026-07-20-tesla-p100-vs-m60-for-ai.md output.mp4 --llm-description
```

省略该标志时，现有行为（从笔记正文提取）保持不变，因此向后兼容。