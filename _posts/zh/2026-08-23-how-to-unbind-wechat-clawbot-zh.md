---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何解绑微信ClawBot
translated: true
type: note
---

**问题：** 如何解绑/断开微信 ClawBot 与某个程序？

**回答：**

解绑方法取决于你使用的 **ClawBot 集成方式**：

---

### 1. CodeBuddy（腾讯 AI IDE）
如果需要切换账号或断开连接，只需点击 CodeBuddy 微信 ClawBot 配置面板中的 **“解绑”** 按钮，之后即可重新绑定新账号。

---

### 2. Kimi Claw
要断开连接，请打开 **Kimi Claw 设置 → 聊天渠道 → 微信**，先在此处断开微信连接。请注意，每个微信账号只能绑定一个 Kimi Claw——连接新账号将自动覆盖之前的绑定。

---

### 3. OpenClaw / ClawBot 插件（微信端）
ClawBot 通过 **微信 → 我 → 设置 → 功能 → 插件** 启用。要解绑，请前往同一插件页面，在微信中 **禁用或移除** ClawBot 插件。

---

### 4. 自托管 / 自定义机器人（例如 weclaw、wechat-clawbot）
- 停止计算机上正在运行的网关/进程。
- 删除已存储的凭证（通常位于 `~/.weclaw/` 或 `~/.clawbot-gateway/`）。
- 如果机器人账号已单独登录微信，请从微信中退出该账号。

---

**通用提示：** 如果你只想停止机器人响应而不完全解绑，只需 **关闭本地程序**——因为 ClawBot 直接连接到本地计算机上的 OpenClaw，它是一个仅在本地程序运行时才工作的私有代理。

---

**参考：**
- [CodeBuddy 微信 ClawBot 指南](https://www.codebuddy.ai/docs/ide/Platform-integration/weixinbot-guide)
- [Kimi Claw 微信设置](https://www.kimi.com/en-cn/help/kimi-claw/wechat-bot)
- [OpenClaw ClawBot 指南](https://openclawlaunch.com/guides/openclaw-wechat)
- [weclaw GitHub 仓库](https://github.com/fastclaw-ai/weclaw)