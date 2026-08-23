---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Unbind WeChat ClawBot
translated: false
type: note
---

**Question:** How do I unbind/disconnect WeChat ClawBot from a program?

**Answer:**

The unbind method depends on **which ClawBot integration** you're using:

---

### 1. CodeBuddy (Tencent's AI IDE)
If you need to switch accounts or disconnect, simply click the **"Unbind"** button in the CodeBuddy WeChat ClawBot configuration panel, then you can rebind with a new account if needed.

---

### 2. Kimi Claw
To disconnect, open the **Kimi Claw settings → Chat Channels → WeChat**, and disconnect WeChat there first. Note that each WeChat account can only bind one Kimi Claw — connecting a new one will automatically overwrite the previous binding.

---

### 3. OpenClaw / ClawBot Plugin (WeChat side)
ClawBot is enabled via **WeChat → Me → Settings → Functions → Plugins**. To unbind, go to that same plugin page and **disable or remove** the ClawBot plugin from WeChat.

---

### 4. Self-hosted / Custom Bot (e.g., weclaw, wechat-clawbot)
- Stop the running gateway/process on your machine.
- Delete the stored credentials (usually in `~/.weclaw/` or `~/.clawbot-gateway/`).
- Log out the bot account from WeChat if it was logged in separately.

---

**General tip:** If you only want to stop the bot from responding without fully unbinding, just **shut down the local program** — since ClawBot connects directly to OpenClaw on your local computer, it's a private agent that only works when your local program is running.

---

**References:**
- [CodeBuddy WeChat ClawBot Guide](https://www.codebuddy.ai/docs/ide/Platform-integration/weixinbot-guide)
- [Kimi Claw WeChat Setup](https://www.kimi.com/en-cn/help/kimi-claw/wechat-bot)
- [OpenClaw ClawBot Guide](https://openclawlaunch.com/guides/openclaw-wechat)
- [weclaw GitHub](https://github.com/fastclaw-ai/weclaw)
