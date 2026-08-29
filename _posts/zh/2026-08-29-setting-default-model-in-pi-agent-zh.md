---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Pi Agent中设置默认模型
translated: true
type: note
---

**问题：** 如何在 Pi agent（pi.dev 编程代理）中设置默认模型？

**回答：**

Pi agent（pi.dev 上的开源编程代理，仓库为 earendil-works/pi）将其默认模型存储在 `settings.json` 中。有以下三种设置方式：

---

**方法 1 — 交互式（推荐初学者使用）**

在 Pi 的交互模式下使用 `/model`，然后在所需模型上按 **Ctrl+S** 将其保存为启动默认模型。类似地，使用 `/thinking` 并按 **Ctrl+S** 可保存默认思考级别。

---

**方法 2 — 直接编辑 `settings.json`**

全局设置文件位于 `~/.pi/agent/settings.json`，适用于所有代理会话。项目级设置文件位于当前工作目录下的 `.pi/settings.json`。

相关字段为 `defaultProvider`（例如 `"anthropic"`、`"openai"`）和 `defaultModel`（模型 ID 字符串）。你还可以设置 `defaultThinkingLevel`，其取值可以是 `"off"`、`"low"`、`"medium"`、`"high"`、`"max"`。

示例：

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-opus-4-8",
  "defaultThinkingLevel": "medium"
}
```

---

**方法 3 — 设置子代理模型默认值（适用于代理团队）**

你可以通过 `subagents.defaultModel` 单独控制子代理的模型，并通过 `subagents.agentOverrides` 按名称固定特定代理。优先级顺序（从高到低）为：每次运行时的覆盖 → 代理 frontmatter 中的模型 → `agentOverrides.<name>.model` → `subagents.defaultModel` → 父会话模型。

示例：

```json
{
  "defaultModel": "claude-opus-4-8",
  "subagents": {
    "defaultModel": "claude-sonnet-4-6",
    "agentOverrides": {
      "reviewer": {
        "model": "claude-opus-4-8",
        "thinking": "high"
      }
    }
  }
}
```

---

**参考资料：**
- [Pi 设置文档（官方）](https://pi.dev/docs/latest/settings)
- [earendil-works/pi — settings.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md)
- [pi-subagents — models.md](https://github.com/nicobailon/pi-subagents/blob/main/docs/models.md)