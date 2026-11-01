---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深度求索 Flash 默认配置
translated: true
type: note
---

完成。`~/.pi/agent/settings.json` 现在包含：

```json
"defaultProvider": "openrouter",
"defaultModel": "~deepseek/deepseek-flash-latest",
"defaultThinkingLevel": "high"
```

备注：

- 精确的模型 ID 是 `~deepseek/deepseek-flash-latest`（开头的 `~` 是 OpenRouter ID 的一部分），provider 为 `openrouter`。
- 该模型支持 `high` thinking（可选值：`off`、`low`、`high`、`max`），因此保留了现有的 `defaultThinkingLevel`——这与你在 picker 中看到的 `• h` 徽标一致。
- 备份已保存至 `~/.pi/agent/settings.json.bak`。该设置仅影响新会话；当前会话会保持原有模型，除非你使用 `/model` 切换。
