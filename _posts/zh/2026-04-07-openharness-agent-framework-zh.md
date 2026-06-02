---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开放马具开放智能体框架
translated: true
type: note
---

## OpenHarness — 开放智能体框架（`oh`）

OpenHarness 是由港大数据科学（HKUDS）团队开发的开源 Python 框架，提供覆盖工具使用、技能、记忆与多智能体协调的轻量级核心智能体基础设施。该项目于 **2026 年 4 月 1 日** 首次发布 v0.1.0 版本，并迅速获得广泛关注，在 GitHub 上已收获超过 **5.7k stars** 和 **973 forks**。

---

### 何为“智能体框架”？

**智能体框架** 是围绕大语言模型（LLM）构建、使其成为功能化智能体的完整基础设施。模型提供智能，而框架则提供双手、双眼、记忆与安全边界。

简言之：

- **LLM** = 大脑（决定 *做什么*）
- **框架** = 躯体（处理 *如何做* —— 安全、高效、可观测）

---

### 核心架构

OpenHarness 通过 10 个子系统实现了核心的智能体框架模式：

| 子系统 | 功能 |
|---|---|
| `engine/` | 智能体主循环 —— 流式处理、工具调用、循环控制 |
| `tools/` | 43+ 工具（文件、Shell、搜索、网络、MCP） |
| `skills/` | 通过 `.md` 文件按需加载知识技能 |
| `plugins/` | 扩展系统 —— 命令、钩子、智能体、MCP 服务器 |
| `permissions/` | 安全层 —— 多级模式、路径规则 |
| `hooks/` | 生命周期事件（PreToolUse / PostToolUse） |
| `commands/` | 54 条斜杠命令（`/help`、`/commit`、`/plan` 等） |
| `memory/` | 通过 `MEMORY.md` 实现跨会话持久化记忆 |
| `coordinator/` | 多智能体子智能体生成与团队协调 |
| `ui/` | 基于 React 的终端用户界面（TUI） |

---

### 主要特性

#### 1. 智能体循环引擎

智能体循环支持流式工具调用周期、带指数退避的 API 重试、并行工具执行以及令牌计数与成本追踪。

#### 2. 工具系统（43+）

工具覆盖多类别：文件 I/O（Bash、Read、Write、Edit、Glob、Grep）、搜索（WebFetch、WebSearch、ToolSearch）、用于生成子智能体的 Agent 工具、任务管理以及 MCP（Model Context Protocol）集成。每个工具都具备 Pydantic 输入验证、自描述的 JSON Schema、权限集成和钩子支持。

#### 3. 技能系统

技能是按需知识，仅在模型需要时加载。示例包括 `commit`、`review`、`debug`、`plan`、`test`、`simplify`、`pdf`、`xlsx` 等 40 多种。同时兼容官方的 `anthropics/skills` 仓库 —— 只需将 `.md` 文件复制到 `~/.openharness/skills/` 即可。

#### 4. 权限与安全

支持多级权限模式：**默认模式**（写/执行前询问）、**自动模式**（允许所有操作，适用于沙盒环境）和**计划模式**（阻止所有写操作，用于先审查后执行的工作流）。可在 `settings.json` 中配置路径级规则和禁用命令列表。

#### 5. 多智能体/群体协调

OpenHarness 支持子智能体生成与委派、团队注册与任务管理、后台任务生命周期管理以及 ClawTeam 集成（路线图中）。

#### 6. 插件系统

兼容 claude-code 插件，已测试 12 个官方插件。示例包括用于 git 工作流的 `commit-commands`、在文件编辑时提供安全警告的 `security-guidance`、执行多智能体 PR 审查的 `code-review`，以及创建自定义行为钩子的 `hookify`。

---

### 服务商兼容性

OpenHarness 支持三种 API 格式：**Anthropic**（默认）、**OpenAI 兼容** （`--api-format openai`）和 **GitHub Copilot** （`--api-format copilot`）。

通过 OpenAI 格式支持的服务商包括 DeepSeek、阿里云灵积、OpenAI、GitHub Models、SiliconFlow、Groq 以及本地 Ollama。GitHub Copilot 支持使用 OAuth 设备流程 —— 无需 API 密钥。

---

### 快速开始

```bash
# 一键安装
curl -fsSL https://raw.githubusercontent.com/HKUDS/OpenHarness/main/scripts/install.sh | bash

# 单命令演示
ANTHROPIC_API_KEY=your_key uv run oh -p "检查此仓库并列出前 3 项重构建议"

# 交互模式
oh

# 非交互式 / 脚本模式
oh -p "列出 main.py 中的所有函数" --output-format json
```

---

### 适用人群

OpenHarness 专为研究者、开发者和社区设计，旨在：理解生产级 AI 智能体的底层工作原理，实验前沿的工具、技能与智能体协调模式，通过自定义插件、服务商和领域知识扩展框架，在成熟架构之上构建专门的智能体。

---

### 技术栈

- **后端**：Python ≥ 3.10，由 `uv` 管理
- **前端 TUI**：React + Ink（Node.js ≥ 18）
- **许可证**：MIT

参考链接：

- [https://github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness)
