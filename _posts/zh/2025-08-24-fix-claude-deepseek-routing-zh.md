---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Claude代码DeepSeek配置路由
translated: true
type: note
---

明白了。你的配置正在将 **Claude Code 的 Anthropic 风格流量**发送到 **OpenRouter 的 OpenAI 风格端点**以使用 DeepSeek V3.1。当 Claude Code（IDE 代理）尝试执行 tools/plan/stream 操作时，消息模式不匹配 → 导致错误。

以下是一种清晰的连接方式，让 **Anthropic 模型**仍然使用 Anthropic 风格的网关，而 **DeepSeek V3.1**（OpenAI 风格）则保持在 `/chat/completions` 端点上。我将展示你可以直接粘贴的确切修改内容。

---

### 1) 验证 DeepSeek V3.1 的模型标识

OpenRouter 的聊天模型标识是：

```
deepseek/deepseek-chat-v3.1
```

（这是指导/聊天模型——区别于“基础”模型。）([OpenRouter][1])

---

### 2) 为 Claude Code 添加一个 Anthropic 格式的代理

Claude Code 期望 **Anthropic Messages**（`/messages`, `tool_use` 块）。最简单的修复方法是运行一个微小的代理，将 Anthropic 格式转换为 OpenAI（OpenRouter）格式并转换回来。有一个现成的可用：**maxnowack/anthropic-proxy**。像这样启动它（环境变量是你的 OpenRouter 密钥）：

```bash
OPENROUTER_API_KEY=YOUR_KEY npx anthropic-proxy
```

它在本地监听并为你转换模式。([GitHub][2])

现在，添加**第二个提供商**，将 Claude Code 的流量指向该代理。

#### 🔧 用这些有针对性的更改替换你的 JSON

**添加此提供商（保持你当前的 `openrouter` 提供商不变）：**

```json
{
  "name": "anthropic-proxy",
  "api_base_url": "http://127.0.0.1:3000/v1/messages",
  "api_key": "",
  "models": [
    "anthropic/claude-sonnet-4",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3.7-sonnet:thinking",
    "anthropic/claude-opus-4"
  ]
}
```

**保持你现有的 OpenRouter 提供商不变（对于 DeepSeek 和其他 OpenAI 模式模型，使用 `/chat/completions` 是正确的）。** OpenRouter 规范化为 OpenAI 兼容模式，并支持推理令牌、工具等额外功能。([OpenRouter][3])

---

### 3) 将模型路由到正确的提供商

将 Anthropic 模型指向 **anthropic-proxy**；将 DeepSeek/GPT/Gemini/Qwen 指向 **openrouter**。

你可以直接使用的示例路由块：

```json
"Router": {
  "default": "openrouter,openai/gpt-5-mini",

  "background": "openrouter,google/gemini-2.5-flash",
  "think": "openrouter,qwen/qwen3-coder",
  "longContext": "openrouter,moonshotai/kimi-k2",
  "longContextThreshold": 2000,
  "webSearch": "openrouter,mistralai/mistral-medium-3.1",

  "overrides": {
    "anthropic/claude-sonnet-4": "anthropic-proxy,anthropic/claude-sonnet-4",
    "anthropic/claude-3.5-sonnet": "anthropic-proxy,anthropic/claude-3.5-sonnet",
    "anthropic/claude-3.7-sonnet:thinking": "anthropic-proxy,anthropic/claude-3.7-sonnet:thinking",
    "anthropic/claude-opus-4": "anthropic-proxy,anthropic/claude-opus-4",

    "deepseek/deepseek-chat-v3.1": "openrouter,deepseek/deepseek-chat-v3.1"
  }
}
```

> 如果你的路由不支持 `overrides` 映射，等效的方法是：在你的应用程序中创建单独的“配置文件”（例如，“通过 anthropic-proxy 的 Claude Code”与“通过 openrouter 的常规聊天”），并根据每个操作选择配置文件。

---

### 4) 避免在 DeepSeek 上发生推理流冲突（可选但更安全）

DeepSeek V3.1 支持 **“思考”令牌**。许多包装器如果在流中出现这些令牌会出错。在 OpenRouter 上，你可以使用请求标志**排除推理**。如果你的路由允许你设置每个模型的参数，请附加：

```json
"params": {
  "reasoning": { "exclude": true }
}
```

（或者 `include_reasoning: false`，取决于你的路由器的参数命名）。这可以防止 `
