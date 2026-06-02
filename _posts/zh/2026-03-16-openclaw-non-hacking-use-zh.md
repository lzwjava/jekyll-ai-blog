---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 并非为黑客任务而设计
translated: true
type: note
---

**问题：** OpenClaw 是否非常擅长 hacking，例如在网站中查找 vulnerabilities、scanning ports、breaking passwords，以及执行其他 hacking 任务？OpenClaw 是我让它控制计算机的 AI agent。

**答案：**

否，OpenClaw **不** 擅长 hacking 任务，如查找网站 vulnerabilities、scanning ports、cracking passwords，或任何形式的未经授权 hacking。

OpenClaw 是一个开源的、自托管的 AI agent（前身为 Clawdbot 或 Moltbot），设计为个人助理。它在您的计算机或专用设备上本地运行，并连接到 messaging apps 如 WhatsApp 或 Telegram。它可以执行日常任务，例如管理 emails、日历、发送消息、检查航班，或在您明确允许的情况下控制您自己的机器上的 apps 和 files。

因为它有完全访问您计算机的权限（如果您授予它），它 *技术上* 可以运行您安装并指示它执行的任何 software 或 scripts。例如：
- 您可以安装如 Nmap 之类的 tools 来在您自己的系统上进行 port scanning。
- 您可以编写或运行 scripts 用于 web browsing 或 basic automation。

然而，它 **不** 是为 hacking 构建或优化的：
- 它没有内置的 hacking skills、exploits 或 specialized tools。
- 它的性能完全取决于您连接的 large language model（例如 Claude 或 GPT）以及您给出的确切 commands。
- 它不够“聪明”，无法在没有详细的人类 instructions 和预安装 tools 的情况下自主发现并利用真实世界的 vulnerabilities。
- OpenClaw 本身存在已知 security issues（例如 prompt injection risks 和过去的 remote code execution vulnerabilities），这可能会使您自己的系统安全性降低，如果您运行它。

**重要警告：** 将任何 AI agent（包括 OpenClaw）用于未经授权的 hacking（scanning 他人 ports、breaking into 网站、cracking passwords 等）在大多数国家是**非法**的，并可能导致严重的法律后果。我强烈建议不要这样做。OpenClaw 是用于有帮助的、个人的 automation——而非 offensive security 或 criminal activity。

如果您对在您拥有且有明确权限测试的系统上进行 ethical security testing（white-hat hacking）感兴趣，您仍然需要手动安装 professional tools 并逐步指导 agent。即使如此，dedicated tools 和人类 expertise 也远比依赖 OpenClaw 有效。

有关官方详情，请访问项目网站 https://openclaw.ai 或其 GitHub repository。如果您有关于为合法任务设置 OpenClaw 的其他、非 hacking 问题，请随时提问！
