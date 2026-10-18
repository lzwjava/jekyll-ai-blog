---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型配置已更新
translated: true
type: note
---

已完成。已更新 `/home/lzw/.pi/agent/settings.json`：

```json
{
  "defaultProvider": "openrouter",
  "defaultModel": "deepseek/deepseek-v4.1-flash",
  "defaultThinkingLevel": "high"
}
```

注释：

- `deepseek/deepseek-v4.1-flash` 存在于目录中（OpenRouter提供商，具备推理能力，1M上下文）。
- 提供商保持 `openrouter`，它已经在 `auth.json` 中存储了API密钥。
- 你的思考级别是 `high`，这个模型支持它（`thinkingLevelMap` 有 `high: "high"`），所以没有冲突。
- 新会话现在将以此模型开始。现有会话保持它们记录的模型。
