---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 OpenClaw 进行直接服务器管理
translated: true
type: note
---

问题：让 OpenClaw 通过 SSH 登录另一台机器并安装 CUDA drivers、Ollama 等是否更自然？因为它就像一个 digital employee，而使用 Claude Code 或 Codex 则更间接且需要跳过权限，而在 OpenClaw 中我们可以直接授予其 sudo 权限。

回答：

是的，在 AI agent 工作流和“digital employee”风格工具的语境下，你的推理非常有道理。

**为什么 OpenClaw（或类似的 agentic tools）在处理此类任务时更自然：**

- **模拟直接服务器访问**：像 OpenClaw 这样支持 SSH 执行的工具可以像远程运维（sysadmin）或 digital employee 一样工作。你可以直接指令它：
  - 通过 SSH 登录目标机器
  - 运行 `sudo apt update && sudo apt install ...`（或对应发行版的命令）
  - 安装 NVIDIA CUDA drivers
  - 安装 Ollama
  - 配置 environment variables、pull models 等

- **Sudo 权限**：为 agent 提供具有 sudo 权限的用户（或配置了 sudoers 的 SSH key），可以让它干净利落地执行特权操作，而无需不断绕过权限限制。

- **有状态且持久化的工作流**：agent 可以在多个 SSH 会话中保持 context，检查安装状态，处理错误，在驱动安装需要时重启机器，验证 `nvidia-smi`，然后继续安装和运行 Ollama。这完全模仿了人类 DevOps 工程师的工作方式。

**与 Claude Code / Cursor / Codex 风格工具的对比：**

- 这些主要是 IDE 或浏览器内的 **code generation 和 editing assistants**。它们擅长编写 scripts、Dockerfiles 或 bash 命令，但通常无法直接在远程服务器上执行它们。
- 你需要：
  - 要求模型生成安装命令或完整的 script
  - 自己复制粘贴 script（或使用某种 terminal 集成）
  - 手动处理 sudo/password 提示
  - 通过将错误信息反馈给模型来迭代调试失败的情况
- 这产生了一个更间接的、human-in-the-loop 的过程。它非常适合规划和编写整洁的代码，但在实际的远程服务器管理方面不够无缝。

**最佳实践建议：**

1. 使用 **OpenClaw（或具有 SSH 能力的类似 agent）** 执行重任务，例如：
   - 在远程 GPU 服务器上安装 CUDA、drivers、Ollama 和 dependencies
   - 运行冗长的 setup 序列
   - 进行实时的监控和 troubleshooting

2. 使用 **Claude / Cursor / GPT-4o 等** 用于：
   - 规划安装步骤
   - 编写健壮的、idempotent 的 bash scripts
   - 生成 Docker Compose 文件或优化的 Ollama 配置
   - 当 agent 卡住时调试复杂的错误

3. 混合方案（推荐）：
   - 让 Claude 帮助你编写一份注释详尽的安装 script
   - 然后将其交给具有 sudo 权限和 SSH 访问权限的 OpenClaw 进行运行和验证

**安全提示**：
给予任何 AI agent 通过 SSH 访问 sudo 的权限虽强大但也存在风险。最佳实践包括：
- 使用专门的低权限 service account，并限制 sudo 权限（如果可能，仅限特定命令）
- 将 SSH key 访问限制在特定 IP 地址
- 监控 agent 执行的任务日志和命令
- 考虑对危险操作使用具有 sandboxing 或确认提示的工具

你需要一份可以交给 agent 的 CUDA + Ollama 安装 bash script 模板，还是关于如何为此类 digital employee 设置安全配置 SSH/sudo 的建议？

References:  
- None