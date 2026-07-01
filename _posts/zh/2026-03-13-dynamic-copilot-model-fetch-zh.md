---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 动态 Copilot 模型获取指南
translated: true
type: note
---

问题：`GET https://api.githubcopilot.com/models` 端点是什么，它如何工作，我如何使用它来动态获取 `/model` 命令的模型列表，而不是硬编码模型？

回答：

## `GET https://api.githubcopilot.com/models` 端点的概述

这是一个 **非官方但广泛使用** 的 GitHub Copilot 内部 API 端点，它返回您的特定 Copilot 订阅可用的 AI 模型列表。它 **不是官方 `docs.github.com` REST API 文档** 的一部分，而是从 VS Code 和 JetBrains Copilot 客户端与 GitHub 后端的通信方式中逆向工程得出的。

---

## 端点详情

| Property | Value |
| --- | --- |
| **Method** | `GET` |
| **URL** | `https://api.githubcopilot.com/models` |
| **Auth** | Bearer token (Copilot OAuth token, not a GitHub PAT) |
| **Returns** | A list of models your subscription supports |

---

## 所需标头

对于所有 Copilot API 请求，您需要两个必需标头：`Authorization: Bearer YOUR_COPILOT_TOKEN` 用于身份验证，以及 `Copilot-Integration-Id: vscode-chat` 用于标识集成类型。

此外，GitHub Copilot 还可能期望 `Editor-Version`、`Editor-Plugin-Version` 和 `User-Agent` 等标头来标识您的应用程序。

### 完整标头示例

```bash
curl -X GET 'https://api.githubcopilot.com/models' \
  -H 'Authorization: Bearer YOUR_COPILOT_TOKEN' \
  -H 'Copilot-Integration-Id: vscode-chat' \
  -H 'Content-Type: application/json' \
  -H 'Editor-Version: vscode/1.104.1' \
  -H 'Editor-Plugin-Version: copilot-chat/0.26.7' \
  -H 'User-Agent: GitHubCopilotChat/0.26.7'
```

---

## 响应格式

响应返回一个带有 `data` 数组的 JSON 对象，其中每个项目包含 `id`、`object`、`created` 和 `owned_by` 等字段。简化的示例：

```json
{
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1234567890,
      "owned_by": "github-copilot"
    },
    {
      "id": "claude-3.5-sonnet",
      "object": "model",
      "created": 1234567890,
      "owned_by": "github-copilot"
    }
  ]
}
```

列表中的每个 `id` 都是您可以传递给 `/chat/completions` 的模型标识符。

---

## 为什么它是订阅感知的

Copilot 托管了来自 OpenAI、Anthropic、Google 等供应商的众多模型。您可以通过调用此端点列出您的订阅允许的模型，并且每个返回的 ID 都可以直接在您的 API 调用中使用。这意味着：

- **Copilot Individual** 可能返回较少的模型
- **Copilot Business / Enterprise** 可能返回额外的或高级模型
- 随着 GitHub 添加或移除模型支持，该列表会发生变化

---

## 如何获取 Copilot OAuth Token

此处需要的令牌 **不是** 您普通的 GitHub PAT。它是一个短期 Copilot 会话令牌。最简单的途径是从任何 JetBrains IDE（PyCharm、GoLand 等）登录 Copilot — 认证后，会出现一个包含 `oauth_token` 值（即您的 API 调用令牌）的文件。

您也可以通过 Copilot 客户端使用的令牌端点（例如 `https://api.github.com/copilot_internal/v2/token`）以编程方式获取它。

---

## 更新 `/model` 命令以使用此端点

以下是如何在 JavaScript/TypeScript 中实现动态 `/model` 命令：

```typescript
async function fetchAvailableModels(copilotToken: string): Promise<string[]> {
  const response = await fetch("https://api.githubcopilot.com/models", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${copilotToken}`,
      "Copilot-Integration-Id": "vscode-chat",
      "Content-Type": "application/json",
      "Editor-Version": "vscode/1.104.1",
      "Editor-Plugin-Version": "copilot-chat/0.26.7",
      "User-Agent": "GitHubCopilotChat/0.26.7"
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch models: ${response.statusText}`);
  }

  const data = await response.json();
  // Extract just the model IDs
  return data.data.map((model: { id: string }) => model.id);
}

// Example usage in your /model command handler:
async function handleModelCommand(copilotToken: string) {
  const models = await fetchAvailableModels(copilotToken);
  console.log("Available models for your subscription:");
  models.forEach(id => console.log(` - ${id}`));
}
```

---

## 动态获取与硬编码的关键优势

| Hardcoded | Dynamic (`/models` endpoint) |
| --- | --- |
| 当 GitHub 添加/移除模型时会中断 | 始终最新 |
| 可能显示用户无法访问的模型 | 仅显示订阅支持的模型 |
| 更新需要修改代码 | 零维护 |
| 快速（无需网络调用） | 小延迟成本（启动时一个额外请求） |

---

## 重要注意事项

- 这是一个 **逆向工程的、非官方端点** — GitHub 可能随时更改它而不另行通知。
- Copilot API 的过度自动化或脚本化使用可能会触发 GitHub 的滥用检测系统，进一步异常活动可能导致您的 Copilot 访问临时暂停。
- 将模型列表缓存（例如 10–30 分钟），而不是在每次 `/model` 命令调用时重新获取。

参考资料：

- [aider - GitHub Copilot Integration](https://aider.chat/docs/llms/github.html)
- [Alorse/copilot-to-api on GitHub](https://github.com/Alorse/copilot-to-api)
- [ericc-ch/copilot-api on GitHub](https://github.com/ericc-ch/copilot-api)
- [@opeoginni/github-copilot-openai-compatible on npm](https://www.npmjs.com/package/@opeoginni/github-copilot-openai-compatible)
- [GitHub Models API Changelog](https://github.blog/changelog/2025-05-15-github-models-api-now-available/)
