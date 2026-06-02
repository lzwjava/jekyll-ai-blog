---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Slack设置审核：已完成与待处理
translated: true
type: note
---

以下是我们就 Slack 设置已完成及仍需配置步骤的全面回顾：🦞

## ✅ 已完成步骤

1. **Slack 应用已创建** — 您已在工作区中创建 Slack 应用。
2. **机器人令牌已配置** — 已将 `xoxb-...` 机器人令牌添加至 OpenClaw。
3. **应用级令牌已配置** — 已添加 `xapp-...` 应用级令牌用于 Socket 模式。
4. **网关已重启** — 网关已重启，目前 Slack Socket 模式已**连接**。
5. **插件已加载** — Slack 插件已在插件列表中显示为**已加载**。

## 🔧 仍需配置的步骤 (Slack 端配置)

### 1. 事件订阅

在您的 Slack 应用面板 ([api.slack.com/apps](https://api.slack.com/apps)) 中：

- 进入 **事件订阅** 页面
- 将 **启用事件** 开关设为 **开启**
- 在 **订阅机器人事件** 下，添加以下事件：
  - `message.channels` — 用于公共频道消息
  - `message.groups` — 用于私密频道消息
  - `message.im` — 用于直接消息
  - `message.mpim` — 用于群组直接消息
  - `app_mention` — 用于当有人提及机器人时
- 点击 **保存更改**

### 2. OAuth 权限范围 (请确认)

在 **OAuth 与权限** → **机器人令牌权限范围** 中，确保已添加以下权限：

- `chat:write`
- `channels:history`
- `channels:read`
- `groups:history`
- `groups:read`
- `im:history`
- `im:read`
- `im:write`
- `mpim:history`
- `mpim:read`
- `mpim:write`
- `app_mentions:read`

### 3. 邀请机器人至频道

在每个您希望机器人响应的 Slack 频道中：

- 输入 `/invite @您的机器人名称`，将其添加至频道

### 4. Socket 模式 (请确认)

在 Slack 应用面板的 **Socket 模式** 页面：

- 确保 Socket 模式为**已启用**
- 应用级令牌应已处于激活状态

## 🧪 测试

完成以上步骤后：

1. 在已邀请机器人的频道中发送一条消息。
2. 通过命令 `tail -f /tmp/openclaw/openclaw-2026-04-05.log | grep slack` 检查日志，查看是否有事件传入。

您确认这些设置后，需要我再次为您查看日志吗？
