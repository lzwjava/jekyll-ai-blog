---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: GitHub OAuth设备代码流程
translated: true
type: note
---

### 概述

这段 JavaScript 代码实现了 OAuth 2.0 设备授权认证流程（又称设备码授权），用于通过 GitHub 认证并获取访问令牌。该流程通常用于无界面应用程序（如 CLI 工具或嵌入式系统），用户无法直接通过网页浏览器进行认证授权。

在此特定场景中，代码模拟 GitHub Copilot 插件（如 Neovim 或 Vim 版本）的请求，通过伪装 Copilot 客户端的请求头来接入 GitHub 认证系统。其目标是生成可用于 GitHub API 调用的访问令牌（如通过 `scope: "read:user"` 读取用户信息）。

该代码作为 Node.js 脚本运行，使用 `fetch` 发起 HTTP 请求，通过 `process` 读取环境变量。运行需确保 Node.js 支持 `fetch`（新版本或通过 polyfill 实现）。若认证成功，代码将持续轮询 GitHub 服务器直至用户完成授权或超时。

**重要提示：**

- 需设置环境变量 `MY_COPILOT_CLIENT_ID`（应为注册 GitHub Copilot 的 OAuth 应用客户端 ID）
- 错误处理较为简单（如获取失败时仅记录日志并继续执行或退出）
- 访问令牌的存储或记录存在安全风险（其具备 API 访问权限）。本代码直接将完整令牌对象输出至控制台，实际使用中可能引发隐私/安全问题（建议加密存储并定期轮换）
- 流程需用户交互：用户需访问指定 URL 并在 GitHub 网站输入验证码完成授权
- 此非 GitHub 官方文档代码，疑似通过逆向分析 GitHub Copilot 行为实现。请遵循 GitHub 服务条款合规使用 API

### 逐步解析

#### 1. 环境检查

```javascript
const clientId = process.env.MY_COPILOT_CLIENT_ID;

if (!clientId) {
  console.error("MY_COPILOT_CLIENT_ID 未设置");
  process.exit(1);
}
```

- 从环境变量获取 `MY_COPILOT_CLIENT_ID`（可通过 `export MY_COPILOT_CLIENT_ID=your_client_id` 设置）
- 若未设置则记录错误并退出脚本（进程代码 1 表示失败）
- 该客户端 ID 需来自已注册的 GitHub OAuth 应用

#### 2. 通用请求头设置

```javascript
const commonHeaders = new Headers();
commonHeaders.append("accept", "application/json");
commonHeaders.append("editor-version", "Neovim/0.6.1");
commonHeaders.append("editor-plugin-version", "copilot.vim/1.16.0");
commonHeaders.append("content-type", "application/json");
commonHeaders.append("user-agent", "GithubCopilot/1.155.0");
commonHeaders.append("accept-encoding", "gzip,deflate,b");
```

- 创建包含键值对的 `Headers` 对象用于 HTTP 请求
- 这些请求头使请求看似来自 GitHub Copilot Vim 插件（Neovim 0.6.1 的 1.16.0 版本），可能用于伪装用户代理以模拟 Copilot 的 API 调用
- `"accept": "application/json"`：期望 JSON 格式响应
- `"content-type": "application/json"`：请求体使用 JSON 格式
- `"accept-encoding"`：支持 gzip/deflate 压缩以节省带宽

#### 3. `getDeviceCode()` 函数

```javascript
async function getDeviceCode() {
  const raw = JSON.stringify({
    "client_id": clientId,
    "scope": "read:user",
  });

  const requestOptions = {
    method: "POST",
    headers: commonHeaders,
    body: raw,
  };

  const data = await fetch(
    "https://github.com/login/device/code",
    requestOptions,
  )
    .then((response) => response.json())
    .catch((error) => console.error(error));
  return data;
}
```

- **功能**：通过向 GitHub 请求设备码来启动设备码认证流程
- 构建包含以下内容的 JSON 载荷：
  - `client_id`：OAuth 客户端 ID（用于应用认证）
  - `scope`：`"read:user"` — 限制令牌仅可读取基础用户信息（如通过 GitHub API 获取用户名、邮箱）
- 向 `https://github.com/login/device/code`（GitHub OAuth 设备码端点）发起 POST 请求
- 解析 JSON 响应（预期包含字段：`device_code`、`user_code`、`verification_uri`、`expires_in`）
- 发生错误时（如网络问题）记录日志但继续执行（可能返回 `undefined`）
- 返回 GitHub 的解析后 JSON 数据对象

#### 4. `getAccessToken(deviceCode: string)` 函数

```javascript
async function getAccessToken(deviceCode: string) {
  const raw = JSON.stringify({
    "client_id": clientId,
    "device_code": deviceCode,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
  });

  const requestOptions = {
    method: "POST",
    headers: commonHeaders,
    body: raw,
  };

  return await fetch(
    "https://github.com/login/oauth/access_token",
    requestOptions,
  )
    .then((response) => response.json())
    .catch((error) => console.error(error));
}
```

- **功能**：在用户授权后，通过轮询 GitHub 将设备码兑换为访问令牌
- 接收上一步获取的 `device_code`
- 构建包含以下内容的 JSON：
  - `client_id`：同上
  - `device_code`：标识此设备/认证尝试的唯一代码
  - `grant_type`：指定此为设备码授权类型（标准 OAuth2 URN）
- 向 `https://github.com/login/oauth/access_token` 发起 POST 请求
- 返回解析后的 JSON 响应，可能为：
  - 成功：`{ access_token: "...", token_type: "bearer", scope: "read:user" }`
  - 处理中/错误：`{ error: "...", error_description: "..." }`（如 "authorization_pending" 或 "slow_down"）
- 错误（如 fetch 失败）会被记录但未显式处理，调用方需检查返回值

#### 5. 主执行逻辑（立即调用异步函数）

```javascript
(async function () {
  const { device_code, user_code, verification_uri, expires_in } =
    await getDeviceCode();
  console.info(`请输入用户代码：\n${user_code}\n${verification_uri}`);
  console.info(`有效期：${expires_in} 秒`);
  while (true) {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    const accessToken = await getAccessToken(device_code);
    if (accessToken.error) {
      console.info(`${accessToken.error}: ${accessToken.error_description}`);
    }
    if (accessToken.access_token) {
      console.info(`访问令牌：\n${JSON.stringify(accessToken, null, 1)}`);
      break;
    }
  }
})();
```

- **整体流程**：协调完整的 OAuth 2.0 设备码授权流程
- 调用 `getDeviceCode()` 并解构响应变量（假设执行成功且包含相应属性）
- 输出用户指引：
  - `user_code`：短字母数字代码（如 "ABCD-EFGH"）
  - `verification_uri`：通常为 `https://github.com/login/device`，用户需在此完成认证
  - `expires_in`：代码有效期（秒），通常为 900 秒（15 分钟）
- 用户需访问该 URL，登录 GitHub 并输入用户代码以授权应用
- 进入无限循环进行令牌轮询：
  - 每次尝试间隔 5 秒（GitHub 建议对频繁请求使用 slow_down 控制）
  - 调用 `getAccessToken(device_code)`
  - 若响应含 `error`：记录日志（如持续等待时显示 "authorization_pending"）
  - 若含 `access_token`：输出完整令牌对象（带缩进格式）并退出循环
- **边界情况/问题**：
  - 若 `getDeviceCode()` 失败，解构可能出错（代码未作检查）
  - 未设置循环超时 — 除非获取访问令牌或脚本崩溃，否则持续轮询
  - 访问令牌输出至控制台存在暴露风险，生产环境应安全存储（如保存至文件或数据库）

### 端到端运行原理

1. **步骤 1：请求设备码** → 脚本从 GitHub 获取临时代码
2. **步骤 2：用户授权** → 用户访问 GitHub 并输入代码授予权限
3. **步骤 3：轮询令牌** → 脚本持续向 GitHub 查询直至获得令牌
4. **结果**：获取指定作用域的访问令牌（如通过 GitHub API 读取用户数据）

此代码模拟了 GitHub CLI 等工具的工作机制，并适配于 Copilot 场景。关于 GitHub OAuth 的官方文档请参阅 <https://docs.github.com/zh/developers/apps/building-oauth-apps/authorizing-oauth-apps#device-flow。如需构建类似功能，请确保符合> OAuth 标准及 GitHub 政策。若对修改或运行此代码有疑问，欢迎咨询！
