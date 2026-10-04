---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi 的默认模型更新至 MiMo
translated: true
type: note
---

已完成。Pi 的默认模型现在是 `xiaomi/mimo-v2.6-flash`。

**我更改的内容** — `~/.pi/agent/settings.json`：

```json
"defaultProvider": "openrouter",
"defaultModel": "xiaomi/mimo-v2.6-flash",
```

**详情：**
- 该模型位于 Pi 的目录中，属于 **openrouter** 提供商（`Xiaomi: MiMo-V2.6-Flash`），支持 1M 上下文、推理能力和视觉输入——之前的默认模型是 `deepseek/deepseek-v4.1-flash`。
- `OPENROUTER_API_KEY` 已在你的环境中设置，因此身份验证可以正常工作（你的 `auth.json` 为空，但 Pi 会回退到该环境变量）。
- 此更改适用于**新会话**；当前会话保留其模型。如果你想立即切换，请按 `Ctrl+P` 或在当前会话中运行 `/model`。

如果你想恢复，可以在 Pi 中运行 `/model`，选择 DeepSeek 模型，然后按 `Ctrl+S` 将其保存为默认模型。