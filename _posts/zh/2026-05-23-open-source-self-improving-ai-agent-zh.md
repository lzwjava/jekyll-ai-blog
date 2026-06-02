---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源自我改进AI智能体
translated: true
type: note
---

以下是 Hermes Agent 的简介：

Hermes Agent 是由 Nous Research 构建的开源、自我改进型 AI 代理。关键要点：

1. 自我改进循环 —— 它能从对话中学习：从经验中创建技能，在使用中改进技能，跨会话持久化记忆，并随时间建立用户模型。这是它与普通聊天机器人封装的核心区别。

2. 模型无关 —— 兼容 OpenRouter（200+ 模型）、OpenAI、Anthropic、Nous Portal、小米 MiMo、HuggingFace 及自定义端点。通过 `hermes model` 切换模型，无锁定。

3. 多平台 —— 单个网关进程服务于 Telegram、Discord、Slack、WhatsApp、Signal、Email 以及 CLI 本身。当它在云端 VM 上运行时，你可以通过手机上的 Telegram 与其交流。

4. 两种界面：
   - CLI（`hermes`）—— 终端界面，支持多行编辑、斜杠命令、自动补全、流式工具输出
   - 网关（`hermes gateway start`）—— 消息平台桥接

5. 40+ 内置工具 —— 终端、文件操作、网络搜索、浏览器、图像生成、TTS、Cron 调度、子代理委派等。工具按工具集组织，可启用/禁用。

6. 技能系统 —— 以 SKILL.md 文件存储的程序性记忆。代理在完成复杂任务后创建技能，随后重用。兼容 agentskills.io 开放标准。

7. 随处运行 —— 终端后端：本地、Docker、SSH、Modal（无服务器）、Daytona、Singularity、Vercel Sandbox。可在 5 美元的 VPS 或 GPU 集群上运行。

8. 面向研究 —— 支持批量轨迹生成与压缩，用于训练未来的工具调用模型。

9. 内置 Cron —— 用自然语言调度任务，将结果投递至任意已连接平台。

10. OpenClaw 迁移 —— 若你使用过 OpenClaw（前代产品），`hermes claw migrate` 可导入设置、记忆、技能和 API 密钥。

项目结构以 `run_agent.py`（包含核心对话循环的 AIAgent 类）和 `cli.py`（交互式 CLI）为中心。工具通过 `tools/registry.py` 自动发现。网关位于 `gateway/` 目录，内含各平台适配器。

许可协议：MIT。由 Nous Research 构建。
