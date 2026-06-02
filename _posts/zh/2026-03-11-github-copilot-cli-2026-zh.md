---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Copilot CLI 指南 2026
translated: true
type: note
---

## GitHub Copilot CLI — 概述、发布时间线和使用指南

---

### 发布时间线

GitHub Copilot CLI 首次以 **public preview** 形式于 **2025 年 9 月 25 日** 发布。随后于 **2026 年 2 月 25 日** 达到 **general availability (GA)**，对所有 Copilot 订阅者开放。为了纪念 GA 里程碑，版本升级至 **v1.0**。

> **注意：** 较旧的 `gh-copilot` CLI 扩展是一个完全不同的、现已归档的工具。该旧扩展于 2025 年 10 月 30 日归档，用户被鼓励迁移到新的 Copilot CLI。

---

### 什么是 GitHub Copilot CLI？

GitHub Copilot CLI 将 AI 驱动的编码辅助直接带到您的命令行中，让您可以通过自然语言对话来构建、调试和理解代码。它由与 GitHub Copilot 编码代理相同的 agentic harness 驱动，并与您的 GitHub 工作流程深度集成。

---

### 先决条件

您需要有效的 Copilot 订阅。Copilot CLI 是所有 GitHub Copilot 计划的核心功能，包括 Free、Pro、Pro+、Business 和 Enterprise。每次交互都会消耗您计划的 premium request 额度。

如果您使用组织或企业计划，管理员必须在组织设置中启用 Copilot CLI。

---

### 安装

有多种安装 Copilot CLI 的方式。最常见的方法包括：

**通过 npm（所有平台）：**
```bash
npm install -g @github/copilot
```

**通过 shell 安装脚本（macOS/Linux）：**
```bash
curl -fsSL https://github.com/github/copilot-cli/releases/latest/download/install.sh | bash
```

使用 `| sudo bash` 会安装到 `/usr/local/bin`。您可以设置 `PREFIX` 以安装到自定义目录，并设置 `VERSION` 以安装特定版本。

**通过 Homebrew（macOS）：**
```bash
brew install gh-copilot
```

**通过 WinGet（Windows）：**
```powershell
winget install GitHub.CopilotCLI
```

Copilot CLI 还包含在默认的 GitHub Codespaces 镜像中，并作为 Dev Container Feature 可用。

---

### 认证

安装后，使用您的 GitHub 凭据进行认证：
```bash
copilot auth login
```

认证后，CLI 会自动继承您组织的 Copilot 策略和治理设置。

---

### 基本用法

只需运行以下命令即可启动 CLI：
```bash
copilot
```

然后您可以直接输入自然语言提示。一些示例任务：

- "Write a Python function to parse JSON from a file"
- "Debug this error in my code"
- "Create a branch and open a pull request for this change"
- "Explain what this function does"

---

### 主要功能和模式

**1. 默认（交互）模式**
标准对话模式，Copilot 在执行前会提出每个操作。每一步都需要您的批准。

**2. Autopilot 模式**
按 `Shift+Tab` 切换到 autopilot 模式，这会鼓励代理自主继续工作，直到任务完成——执行工具、运行命令并迭代，而无需停止等待批准。

**3. Plan 模式**
先按 `Shift+Tab` 进入 plan 模式来概述工作，使用 `/model` 比较方法，然后在希望 Copilot 推进任务时按 `Shift+Tab` 进入 autopilot。

**4. 后台任务（Fleet）**
在任何提示前添加 `&` 前缀，将工作委托给云端的 Copilot 编码代理，释放您的终端用于其他任务。使用 `/resume` 在本地和远程编码代理会话之间切换。

---

### 有用的 Slash 命令


| 命令 | 描述 |
|---|---|
| `/model` | 切换或比较 AI 模型 |
| `/restart` | 重启 CLI 同时保留会话 |
| `/lsp show` | 显示 Language Server Protocol 状态 |
| `/diff` | 查看文件更改 |
| `/plugin install owner/repo` | 安装社区插件 |
| `/experimental show` | 访问预览功能 |
| `/changelog` | 查看最新 CLI 更新 |
| `/fleet` | 协调并行子代理 |

---

### MCP (Model Context Protocol) 支持

Copilot CLI 内置 GitHub 的 MCP server，并支持自定义 MCP server 以连接任何工具或服务。插件可以捆绑 MCP server、代理、技能和钩子，并直接从 GitHub 仓库安装。

---

### 模型选择

您可以选择最新的模型，包括 Claude Opus 4.6、Claude Sonnet 4.6、GPT-5.3-Codex 和 Gemini 3 Pro。GPT-5 mini 和 GPT-4.1 包含在您的 Copilot 订阅中，无需额外 premium request 费用。

---

### 平台支持

Copilot CLI 支持 macOS、Linux 和 Windows。它在您的终端中独立运行，并可以修改任何编辑器随后显示的文件，无论您选择哪种编辑器都非常有用。

---

参考资料：

- [GitHub Copilot CLI — Official GitHub Page](https://github.com/features/copilot/cli)
- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli)
- [GitHub Copilot CLI — General Availability Announcement](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs — Install Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
- [GitHub Docs — Copilot CLI Quickstart](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started)
