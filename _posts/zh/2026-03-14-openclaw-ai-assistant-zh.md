---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 你的自主 AI 助手
translated: true
type: note
---

**问题：** 什么是 OpenClaw AI agent，它如何为 AI 提供 **full computer access** 以实现更大的 autonomy，类似于一个 super smart human 在 laptop 上操作，几乎能做任何事情？

**回答：**

OpenClaw 是一个免费、开源的 autonomous AI agent（前身为 Clawdbot 和 Moltbot），它在您自己的计算机或设备上本地运行。由开发者 Peter Steinberger 于 2026 年 1 月下旬推出，它在头几周内迅速走红，GitHub 星标超过 160,000。不同于传统的聊天机器人（如 ChatGPT 或 Claude）仅用文本回复，OpenClaw 作为一个真正的数字同事：它 24/7 驻留在您的机器上，直接连接到您日常使用的消息应用（WhatsApp、Telegram、Slack、Discord、Signal、iMessage 等众多应用），并代表您执行真实操作。

您描述的功能——赋予 AI **full computer access**，让它能自主决定做什么，就像一个 super-smart human 坐在您的 laptop 前——正是 OpenClaw 的核心优势。以下是其工作原理：

- **Full system access and control**：一旦安装在 macOS、Windows、Linux（甚至 Raspberry Pi 或专用 Mac Mini）上，OpenClaw 就能直接访问您的文件、shell commands、浏览器、邮件、日历等。它可以读写文件、运行 terminal scripts、控制专用 Chrome 浏览器（使用 Chrome DevTools Protocol 进行点击、填写表单、抓取数据）、管理 Gmail、发送邮件、更新日历、办理航班 check-in、安装软件、谈判交易，甚至控制硬件如空气净化器。用户将其描述为“Claude with hands”或“坐在带键盘和鼠标的桌前拥有眼睛和手的 smart model”。

- **High autonomy and proactive behavior**：OpenClaw 不仅仅是被动响应。它运行后台“heartbeat” scheduler（默认每 30 分钟一次），自动唤醒它检查任务、审阅邮件或执行 workflows，而无需您的提示。它使用 persistent memory 系统（以简单的 Markdown 和 YAML 文件存储在您的磁盘上），从而跨会话记住一切。您可以赋予它高层目标（如“修复我 app 中的 tests”或“谈判更好的车险优惠”），AI 会自行决定步骤、循环执行操作（例如运行 tests、捕获错误、打开 PR），并通过聊天报告结果。它甚至能即时构建自己的新 skills 或 tools。

- **“doing almost anything”的真实示例**：
  - 清空您的收件箱、取消垃圾邮件订阅，并起草回复。
  - 预订旅行、办理航班 check-in，或在您睡觉时订购杂货。
  - 运行 code reviews、构建网站，或从单条 Telegram 消息自动化整个内容 pipeline。
  - 通过抓取网站、填写表单和发邮件给供应商来谈判折扣。
  - 监控您的 biomarkers 并相应调整房间空气质量。

您与之互动就像给一位非常能干的同事发短信：从手机发送消息，它就会在您的计算机上开始工作。一切保持私密，因为它运行在您的硬件上（无云端托管您的数据）。

**Setup 非常简单**：一行安装命令即可设置一切（包括 Node.js）。您选择 AI brain（Claude、GPT、Gemini，或通过 Ollama 的 local models），连接消息应用，并选择授予的访问权限（full system access 或 sandboxed 以确保安全）。Web dashboard 让您监控和控制它。

虽然功能强大，但用户指出由于其广泛权限，需要仔细设置安全（如敏感操作需批准、在 VM 中运行，或限制 API 成本）。许多人将其运行在专用低成本设备上实现 24/7 操作。

简而言之，是的——OpenClaw 正是提供了您描述的 autonomous、computer-controlling 体验。它将任何 LLM 转变为自定向的数字员工，驻留在您的 laptop 内，能处理人类几乎能做的任何数字任务。

**参考资料：**
- [OpenClaw Official Site](https://openclaw.ai/)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [Complete Guide to OpenClaw](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
