---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent 概述与功能
translated: true
type: note
---

以下是 Hermes Agent README 的概要：

**什么是 Hermes Agent？**
Hermes 是 Nous Research 开源的 AI 智能体框架。其核心特性是自我改进的学习循环——它可以从经验中创建技能，随时间不断优化，跨会话保持持久记忆，并能检索过往对话。它不仅仅是一个聊天封装器，而是一个能够自主调度任务、委派子智能体、并通过多个平台与您交流的自主智能体。

**关键能力：**

1. **多平台网关** — 一个进程同时服务于 CLI、Telegram、Discord、Slack、WhatsApp、Signal 和 Email。您可以从任何地方与它对话。

2. **闭环学习** — 技能在完成复杂任务后自动创建，使用过程中自我改进，并跨会话持久保留。基于 FTS5 的会话搜索功能使其能回忆过往对话。

3. **Cron 调度** — 自然语言驱动的定时任务，可在无人值守时运行，并将结果推送到任何已连接的平台。

4. **子智能体委派** — 可生成并行的独立智能体以进行并发工作，或通过 RPC 运行 Python 脚本，从而将多步骤工具流水线压缩为单一操作。

5. **7 种终端后端** — 本地、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox。无服务器选项（Modal、Daytona）在空闲时自动休眠。

6. **模型无关** — Nous Portal、OpenRouter（200+ 模型）、NovitaAI、NVIDIA NIM、Xiaomi MiMo、z.ai/GLM、Kimi/Moonshot、MiniMax、Hugging Face、OpenAI 或任何自定义端点。通过 `hermes model` 切换。

**安装：** Linux/macOS/WSL2 上一行命令 `curl | bash`。Windows 上使用 PowerShell 一行命令（早期测试版）。

**迁移：** 提供 `hermes claw migrate` 命令，可从 OpenClaw 导入所有内容（记忆、技能、API 密钥、角色设定）。

**文档：** 完整文档位于 hermes-agent.nousresearch.com/docs，涵盖快速入门、CLI 用法、配置、消息网关、安全、工具、技能、记忆、MCP、Cron 及架构。

**许可证：** MIT。

您希望深入了解哪个具体部分吗？