---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenCode GitHub Copilot集成详情
translated: true
type: note
---

是的——OpenCode 对 GitHub Copilot 提供了一流的支持，支持通过网页登录（设备码 OAuth 流程）。

以下是我从源代码中找到的信息：

**提供者 ID**：`github-copilot`（在 `packages/core/src/provider.ts` 中注册）

**认证流程**：OAuth 设备码流程（RFC 8628），在 `packages/opencode/src/plugin/github-copilot/copilot.ts` 中实现：

1. 在 OpenCode 中选择“使用 GitHub Copilot 登录”
2. 选择部署类型：GitHub.com 或 GitHub Enterprise
3. OpenCode 访问 `https://github.com/login/device/code`，携带 client_id `Ov23li8tweQw6odWQebz`
4. 你会获得一个用户码和验证地址（https://github.com/login/device）
5. 在浏览器中输入该码并授权
6. OpenCode 轮询 `https://github.com/login/oauth/access_token`，直到获取 access token
7. 该 token 将作为所有 Copilot API 调用的 Bearer 认证凭据

**API 端点**：`https://api.githubcopilot.com`（Enterprise 版本为 `https://copilot-api.<your-ghe-domain>`）

**支持的功能**：
- Chat completions API 和 OpenAI Responses API
- 视觉请求（图片）
- Agent 模式（通过 `x-initiator` 标头自动检测）
- 推理/思考（通过 `reasoning_opaque` 字段）
- 通过 Copilot API 动态获取模型列表
- 支持自定义 URL 的 GitHub Enterprise

**使用方法**：
```
# 在 OpenCode TUI 中，进入提供者设置
# 选择 "github-copilot" -> "使用 GitHub Copilot 登录"
# 选择 GitHub.com 或 Enterprise
# 在 github.com/login/device 输入设备码
```

无需 API 密钥——使用你现有的 GitHub Copilot 订阅（个人、企业或组织版）。认证 token 会由 OpenCode 的账户系统保存在本地。