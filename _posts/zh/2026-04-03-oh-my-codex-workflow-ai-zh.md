---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Oh My Codex 工作流 AI 介绍
translated: true
type: note
---

我会搜索关于 oh-my-codex 的信息，为您提供全面介绍。问题：什么是 oh-my-codex 的全面介绍，它是一个基于 Codex 的 workflow AI？

答案：

## 概述

Oh My Codex (OMX) 是一个 multi-agent orchestration layer，旨在通过引入结构化团队合作、自动化和高级 workflow 管理来扩展 OpenAI Codex CLI 的功能。它协调多达 30 个角色专属代理和 40+ workflow skills 来自动化 coding 生命周期。可以将其视为一个增强层，将 Codex 从单一 AI coding 助手转变为并行工作的专属代理协调系统。

## 核心目的

OMX 通过叠加一个基于 shell 的系统来解决基础 Codex 环境中的局限性，例如缺乏 hooks、agent coordination 和 persistent execution，从而实现更丰富的交互模式。它保留 Codex 作为 execution engine，并使运行结构化 workflows 变得更容易，让开发者可以将复杂、多步骤任务委托给 AI 团队，而不是手动管理一切。

## 关键组件

### 1. Multi-Agent 系统

OMX 提供了 33 个专属角色提示，按层级组织：

- **Core Development**：architect, planner, executor, debugger, verifier
- **Quality Assurance**：style-reviewer, quality-reviewer, api-reviewer, security-reviewer, performance-reviewer
- **Domain Experts**：dependency-expert, test-engineer, build-fixer, designer, writer
- **Product Strategy**：product-manager, ux-researcher, product-analyst

这些代理可以使用 `/prompts:name` 语法调用，以获得针对性专业知识。

### 2. Workflow Skills

OMX 包含 36 个 workflow skills，可通过 dollar-sign 语法访问，用于 autopilot、team orchestration、planning、recovery 和 QA 周期。主要 workflows 包括：

- **`$autopilot`**：从想法到工作代码的全自主执行
- **`$ralph`**：带验证的自引用完成循环，直至完成
- **`$team`**：N 个 worker 的协调并行执行
- **`$plan`**：带共识审查模式的战略规划
- **`$tdd`**：带 red-green-refactor 周期的 test-driven development
- **`$research`**：用于全面调查的并行 research agents
- **`$security-review`**：专注于漏洞的安全审计

### 3. 带自动 Worktrees 的 Team Mode

从版本 0.10.0 开始，每个 team worker 默认在隔离的 git worktree 中运行，实现无冲突的并行开发，而无需手动分支管理。这意味着：

- 每个 worker 在 `.omx/team/<n>/worktrees/worker-N` 获取专用 worktree
- Worker 写入隔离的 detached branches，而 leader workspace 保持干净
- Leader 通过 merge、cherry-pick 或跨 worker rebase 策略持续集成 worker commits，早期检测并报告冲突
- Auto-commit 确保无工作丢失

系统利用 tmux 等工具同时管理多个 agent 会话，实现 team mode，其中不同代理在共享 workflow 中处理不同职责。

### 4. Persistent State 和 Memory

OMX 提供了五个 MCP (Model Context Protocol) servers，用于 persistent context 和跨会话学习：

- State server
- Memory server
- Code intelligence server
- Trace server
- Session-specific notepads

这允许 workflows 在会话间维护上下文并从先前交互中学习。

### 5. Staged Pipeline 执行

任务通过结构化阶段推进：plan → prd (product requirements document) → exec (execute) → verify → fix 生命周期，用于 evidence-based development workflows。这确保通过内置 quality gates 系统推进开发阶段。

## Workflow Patterns

### 标准 Workflow 路径

主要 workflow 遵循：deep-interview 澄清需求，ralplan 批准实现计划并审查权衡，ralph 执行批准计划直至完成，或 team 用于协调并行执行。

### Launch Modes

OMX 通过 launch profiles 提供对 reasoning effort 的细粒度控制：

- `--yolo`：最小验证的快速执行
- `--high`：增加 reasoning effort
- `--xhigh`：最大 reasoning 深度
- `--madmax`：用于复杂挑战的极端模式

### Mixed Provider 支持

OMX 支持使用 OMX_TEAM_WORKER_CLI_MAP 配置并行运行 Codex、Claude 和 Gemini workers。这允许团队基于各自优势利用不同 AI providers。

## 最近功能 (v0.10.0)

最新版本引入了多项重大增强：

1. **Autonomous Research**：`omx autoresearch` 启动迭代 research 循环，探索主题、细化问题并合成发现
2. **Orchestration Wrapper**：`omx exec` 通过 OMX layer 运行任何命令，带有 hooks、state tracking 和 logging
3. **Intent-First Deep Interviews**：在 Socratic questioning 之前预先进行 intent classification，更快路由到 workflows
4. **Incremental Merge Tracking**：更智能的冲突检测，增量跟踪 worktree 变化

## 集成能力

OMX 通过以下方式与外部服务集成：

- **Discord**：实时通知、webhook 集成和 bot 命令
- **Telegram**：移动通知和命令界面
- **OpenClaw Gateway**：Discord、Slack、Telegram 和自定义 webhook 的统一交付
- **MCP Servers**：用于 persistent state 和外部服务集成

## 安装和使用

```bash
# Install globally
npm install -g oh-my-codex

# Setup and verify
omx setup && omx doctor

# Example usage
omx autoresearch "how does the auth middleware work?"
omx team 3:executor "refactor auth module with full test coverage"
```

## 使用案例

OMX 适用于复杂项目自动化、大规模代码生成、协调代码审查和安全审计、test-driven development 管道，以及可重现的多代理 CI/automation 环境。

## 理念

OMX 不会取代 Codex——它是更好的 task routing + 更好的 workflow + 更好的 runtime，而不是全天手动操作的命令界面。它专为已使用 Codex 的开发者设计，提供增强的 orchestration、persistent state 和 multi-agent coordination 能力叠加其上。

参考资料：

- [https://github.com/Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- [https://sourceforge.net/projects/oh-my-codex-omx.mirror/](https://sourceforge.net/projects/oh-my-codex-omx.mirror/)
- [https://github.com/staticpayload/oh-my-codex](https://github.com/staticpayload/oh-my-codex)
- [https://mcpmarket.com/server/oh-my-codex](https://mcpmarket.com/server/oh-my-codex)
- [https://yeachan-heo.github.io/oh-my-codex-website/](https://yeachan-heo.github.io/oh-my-codex-website/)
- [https://lobehub.com/skills/neversight-learn-skills.dev-oh-my-codex](https://lobehub.com/skills/neversight-learn-skills.dev-oh-my-codex)
- [https://yeachan-heo.github.io/oh-my-codex-website/docs.html](https://yeachan-heo.github.io/oh-my-codex-website/docs.html)
