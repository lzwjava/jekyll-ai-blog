---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: GitHub Copilot 认证流程
translated: true
type: note
---

问得好——GitHub Copilot 的认证流程本质上是标准的 **OAuth2 设备码授权模式**，但在此基础上叠加了 GitHub 专为 Copilot 服务设计的令牌层。让我逐步拆解说明：

---

### 1. **设备流 (`/login/device/code`)**

* 首次登录时，Copilot 客户端（如 VS Code 插件、JetBrains 插件或 CLI）会调用 GitHub 的 OAuth 接口：

  ```
  POST https://github.com/login/device/code
  ```
* 同时传递 Copilot 专属的 **client_id**
* GitHub 返回包含以下字段的响应：
  * `device_code`（用于轮询的内部代码）
  * `user_code`（用户在浏览器中输入的验证码）
  * `verification_uri`（输入验证码的网址）
  * `interval`（客户端轮询频率）

---

### 2. **轮询获取访问令牌**

* Copilot 客户端随后通过轮询获取令牌：

  ```
  POST https://github.com/login/oauth/access_token
  ```
* 请求携带 `device_code` 和 `client_id`
* 当用户在浏览器完成授权后，GitHub 返回：
  * `access_token`（用于 Copilot 的 GitHub OAuth 令牌）
  * `token_type=bearer`
  * `expires_in`（令牌有效期）

此 `access_token` 属于**标准 GitHub OAuth2 令牌**

---

### 3. **兑换 `copilot_internal` 令牌**

* Copilot 客户端不能直接使用 GitHub OAuth 令牌调用 Copilot API
* 需向 Copilot 服务兑换专用令牌：

  ```
  POST https://api.github.com/copilot_internal/v2/token
  Authorization: Bearer <GitHub OAuth access_token>
  ```
* 响应格式为：
  ```json
  {
    "token": "<copilot_internal token>",
    "expires_at": "...",
    "user": { ... }
  }
  ```
* 这个 **`copilot_internal` v2 令牌**才是客户端与 **Copilot 推理服务**（如 `https://copilot-proxy.githubusercontent.com`）通信时使用的凭证

---

### 4. **使用 `copilot_internal` 令牌**

* 所有后续的代码补全或对话请求均通过以下方式认证：

  ```
  Authorization: Bearer <copilot_internal token>
  ```
* 该令牌有效期较短（通常约 1 小时），且与 GitHub 账户及 Copilot 订阅状态绑定
* 客户端通过重新兑换 GitHub OAuth 访问令牌进行定期刷新

---

✅ **核心流程总结：**

* `/login/device/code` → 获取浏览器认证码
* `/login/oauth/access_token` → 获取 GitHub OAuth 令牌
* `/copilot_internal/v2/token` → 兑换短期有效的 Copilot 服务令牌（实际用于代码补全的核心凭证）

---

需要我进一步展示包含请求头与示例 JSON 的**完整请求/响应示例**吗？这样可以更直观地了解实际数据交互细节。
