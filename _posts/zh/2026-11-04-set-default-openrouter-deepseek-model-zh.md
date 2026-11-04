---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设置默认OpenRouter DeepSeek模型
translated: true
type: note
---

在 `~/.pi/agent/settings.json` 中设置为默认值：

```json
"defaultProvider": "openrouter",
"defaultModel": "~deepseek/deepseek-flash-latest",
"defaultThinkingLevel": "high"
```

注释：
- `~` 是 OpenRouter 目录中实际模型 ID 的一部分（`~deepseek/deepseek-flash-latest`，"DeepSeek: DeepSeek Flash Latest"），因此它被原样存储。
- Provider 和 thinking level 已经是 `openrouter` / `high`，所以只有 `defaultModel` 改变了（之前是 `xiaomi/mimo-v2.6-flash`）。
- 新会话将使用它；当前会话保持其模型，直到你运行 `/model` 或重启。