---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 创建 Slack 机器人令牌
translated: true
type: note
---

我将指导你创建 Slack 机器人令牌。 🦞

1. **访问** [https://api.slack.com/apps](https://api.slack.com/apps) 并点击 **创建应用**。
2. 选择 **从头开始**，为其命名（例如“OpenClaw Bot”），并选择你的工作空间。
3. 在左侧边栏中，进入 **OAuth 与权限**。
4. 在 **权限范围** 下，添加以下机器人令牌权限范围：
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
5. 向上滚动并点击 **安装到工作空间**。
6. 安装完成后，复制 **机器人用户 OAuth 令牌**（以 `xoxb-` 开头）。

获取该令牌后，请将其粘贴在此处，我将配置 OpenClaw 使用它。
