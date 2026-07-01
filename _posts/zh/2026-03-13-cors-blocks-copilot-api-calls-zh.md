---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CORS 阻止自定义 Copilot API 调用
translated: true
type: note
---

## 是的 — 您会遇到 CORS 问题

如果您尝试从 **自定义 web 门户**（即不同来源的基于浏览器的前端）直接调用 `https://api.githubcopilot.com/chat/completions`，您几乎肯定会遇到 **CORS (Cross-Origin Resource Sharing) 错误**。

---

## 为什么这里会发生 CORS 问题

### 1. CORS 是什么

CORS 是浏览器强制执行的安全机制，它会阻止来自不同来源的请求，除非服务器明确允许。如果请求者的域名与接收者的域名不同，浏览器默认会拒绝该请求 — 即使请求技术上到达了服务器。浏览器会拒绝将响应传递给客户端。

### 2. 为什么 `api.githubcopilot.com` 阻止自定义来源

官方 GitHub Copilot web 聊天托管在 `github.com/copilot/...`。GitHub 的 API 服务器配置为仅允许特定、可信来源（如 `github.com` 本身）在 `Access-Control-Allow-Origin` 响应头中。

当您的自定义 web 门户（例如 `http://localhost:3000` 或 `https://mycustomapp.com`）向 `https://api.githubcopilot.com/chat/completions` 发送 `fetch()` 请求时，浏览器会首先执行 **预检 OPTIONS 请求**。如果 GitHub 的服务器未以匹配您自定义来源的 `Access-Control-Allow-Origin` 响应，浏览器将完全阻止响应。

### 3. 底层 Token 限制

GitHub Copilot 的 API 内部仅向来自 VSCode 的 OAuth token 开放。Copilot token 端点需要与 VSCode 自身 client ID 绑定的 device-flow 认证。这意味着即使绕过 CORS，为自定义 web 门户获取有效的 Copilot API token 本身也是一个重大障碍。

---

## 官方门户与自定义门户比较

| 场景 | CORS 问题？ |
| --- | --- |
| 官方 `github.com/copilot` 门户 | ❌ 否 — 与 GitHub 服务器相同来源 |
| 您自己的其他域名 web 前端 | ✅ 是 — 被浏览器 CORS 策略阻止 |
| 服务器端后端调用 API（Node.js、Python 等） | ❌ 否 — CORS 仅适用于浏览器 |

---

## 如何解决

服务器到服务器的请求（例如通过 Node.js）不会面临 CORS 限制。正确的架构解决方案是：

### ✅ 使用后端代理（推荐）

构建一个 **后端服务器**（Node.js、Python Flask 等），它：

1. 从您的前端接收请求
2. 将其转发到 `api.githubcopilot.com`
3. 将响应返回给您的前端

您的前端调用 **您自己的后端**（相同来源或由您控制的 CORS），您的后端调用 GitHub。由于 CORS 仅由浏览器强制执行，服务器到服务器的调用可以自由工作。

```
Browser (Custom Portal)
    ↓  fetch("https://your-backend.com/api/chat")
Your Backend Server
    ↓  fetch("https://api.githubcopilot.com/chat/completions")
GitHub Copilot API
```

### ✅ 示例：开源代理项目

像 `copilot-api`（一个逆向工程的代理）这样的项目将 GitHub Copilot 暴露为 OpenAI 兼容的 API 服务器，允许工具通过本地代理与 Copilot 通信。但是，请注意，过度自动化使用可能会触发 GitHub 的滥用检测系统。

---

## 总结

- 从自定义域名直接在浏览器中使用 `fetch()` 调用 `api.githubcopilot.com` **会因 CORS 而失败**。
- 这是 **有意设计** — GitHub 仅允许其自身来源。
- 唯一正确的解决方案是路由请求 **通过您控制的后端代理**，然后服务器到服务器调用 GitHub 的 API。

参考资料：

- [CORS Error Explained — FreeCodeCamp](https://www.freecodecamp.org/news/how-to-fix-cross-origin-errors/)
- [copilot-api proxy project (GitHub)](https://github.com/ericc-ch/copilot-api)
- [GitHub Copilot Inside GitHub Actions — den.dev](https://den.dev/blog/github-copilot-inside-github-actions/)
- [I Turned GitHub Copilot into OpenAI API Compatible Provider — DEV](https://dev.to/ericc/i-turned-github-copilot-into-openai-api-compatible-provider-1fb8)
