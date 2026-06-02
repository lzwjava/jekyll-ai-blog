---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw Gateway 密码缺失错误
translated: true
type: note
---

**Question:** 如何修复 OpenClaw (AI agent) 中出现的 "unauthorized: gateway password missing (enter the password in Control UI settings)" 错误？

**Answer:**

这个错误意味着 OpenClaw Gateway 被配置为使用 **password-based authentication**，但在 Control UI 浏览器界面中尚未输入密码。以下是详细解释及修复步骤。

---

## 导致此错误的原因是什么？

错误信息 `disconnected (1008): unauthorized: gateway password missing (enter the password in Control UI settings)` 表示 `gateway.auth.mode` 已设置为 `password`，但浏览器未向 gateway 发送凭据。

`unauthorized` 错误意味着 endpoint 可以访问，但提供了错误（或缺失）的 auth 信息。

---

## 修复选项 1：在 Control UI 中输入密码（最快修复）

如果 UI 提示进行 auth，请将 `gateway.auth` 配置中的 token（或密码）粘贴到 Control UI 设置中。连接成功后，UI 会将其存储在 `localStorage` 中。

步骤：
1. 在 **Chrome** 中打开 Control UI（不要使用 Safari — 见下文备注）：`http://127.0.0.1:18789/`
2. 您应该会看到 **Settings** 面板或连接提示。
3. 在密码字段中输入您在 `gateway.auth.password` 中设置的密码。
4. 点击 **Connect**。

> ⚠️ **Safari 备注：** Safari 中的 Control UI 无法渲染密码输入对话框，并会循环尝试重新连接。请改用 Chrome — Chrome 在相同配置下可以正常工作。

---

## 修复选项 2：通过 CLI 设置密码

如果您尚未设置密码，请通过终端进行设置：

```bash
openclaw config set gateway.auth.mode password
openclaw config set gateway.auth.password "YourSecurePasswordHere"
openclaw gateway restart
```

运行这些命令并重启后，UI 会提示您输入密码。

---

## 修复选项 3：切换到 Token Auth

如果您更倾向于使用 token-based auth（对浏览器访问更简洁），请切换模式：

```bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
openclaw gateway restart
```

然后通过附加 token 的 URL 访问仪表盘：

```
http://127.0.0.1:18789/?token=YOUR_TOKEN_HERE
```

Token 的来源是 `gateway.auth.token`（或环境变量 `OPENCLAW_GATEWAY_TOKEN`）；连接后，UI 会在 `localStorage` 中存储一份副本。

---

## 修复选项 4：完全避免 Auth（仅限 Localhost）

如果您仅在本地访问 OpenClaw 且不需要任何 auth，请绑定到 loopback 并移除 auth 块：

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789
  }
}
```

> ⚠️ 仅当您**不**将 gateway 暴露给任何网络时才执行此操作。非 loopback 绑定（lan, tailnet, custom）需要配置 auth。

---

## 常见错误：配置键值错误（v2026.3.7 中的 Breaking Change）

从 OpenClaw 2026.3.7 开始，如果同时配置了 `gateway.auth.token` 和 `gateway.auth.password` 但未设置 `gateway.auth.mode`，Gateway 将拒绝启动。您必须显式声明哪一个处于 active 状态。

正确的配置示例：

**Token 模式：**
```json
{ "gateway": { "auth": { "mode": "token", "token": "${OPENCLAW_GATEWAY_TOKEN}" } } }
```

**Password 模式：**
```json
{ "gateway": { "auth": { "mode": "password", "password": "${OPENCLAW_GATEWAY_PASSWORD}" } } }
```

---

## 诊断命令

运行以下命令调试 auth 问题：

```bash
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.token
openclaw gateway status
openclaw doctor
```

---

**参考资料：**

- [OpenClaw Dashboard Auth Docs](https://openclaw-ai.com/en/docs/web/dashboard)
- [OpenClaw Troubleshooting Guide](https://docs.openclaw.ai/gateway/troubleshooting)
- [Fix OpenClaw 1008 Unauthorized — ucartz.com](https://www.ucartz.com/blog/fix-openclaw-disconnected-from-gateway-1008-unauthorized/)
- [OpenClaw 2026.3.7 Breaking Change — clawcloud.sh](https://www.clawcloud.sh/guides/openclaw-3-7-gateway-auth-mode)
- [GitHub Issue: Safari password prompt bug #4458](https://github.com/openclaw/openclaw/issues/4458)
