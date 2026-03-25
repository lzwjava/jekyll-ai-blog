---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超级力量 AI 代码代理工作流框架
translated: true
type: note
---

问题：GitHub 项目 [https://github.com/obra/superpowers](https://github.com/obra/superpowers) 是什么，它是如何工作的？

回答：

## Overview

**Superpowers** 是一个开源的 **AI coding agent workflow framework**。它本身并不添加新的 model，而是通过模块化的“skills”来**强制 AI coding agents（如 Claude Code, OpenCode, Codex 等）遵循严谨的 software engineering process**。 ([AIToolly][1])

你可以将其理解为：

> 一套**编码为 skills 的开发方法论**，你的 AI agent 必须遵守这套流程。

与其让 Agent 这样做：

```
你：构建登录功能
Agent：立即开始随机编写代码
```

它强制执行以下流程：

```
1. clarify requirements (明确需求)
2. design (设计)
3. plan (规划)
4. implement (TDD 模式实现)
5. review (评审)
6. merge (合并)
```

---

## Core Idea

Superpowers = **skills + workflow + auto-trigger rules**

* Skills = 细分的能力（brainstorm, write plan, TDD, review）
* Workflow = 严格的执行顺序
* Auto-trigger = agent 自动调用这些能力

Agent **不会直接跳入编码环节** —— 它首先提取 spec，创建 plan，然后使用 subagents 执行。 ([GitHub][2])

---

## How It Works (Step-by-Step)

### 1. Brainstorming (编码前)

Agent 会提出问题并澄清你的真实需求。

示例：

```
你：构建一个待办事项应用
Agent：
- web 还是 mobile？
- local storage 还是 backend？
- 需要 auth 吗？
```

这会生成一个 **design document**。

---

### 2. Write Implementation Plan

随后它会创建**细小的任务（每个任务 2-5 分钟）**。

示例：

```
Task 1: 创建项目结构
Task 2: 添加 todo 模型
Task 3: 编写失败的测试
Task 4: 实现最小化代码
```

每个任务包括：

* file paths
* exact code
* verification steps

这是自动生成的。 ([GitHub][2])

---

### 3. Subagent-driven development

现在它会衍生出 **sub agents** 来逐一执行任务：

* agent A 编写代码
* agent B 进行 review
* agent C 运行 tests
* agent D 继续下一步

这允许进行**长时间的自主编码任务 (long autonomous coding sessions)**。 ([GitHub][2])

---

### 4. Enforced TDD

它强制执行：

```
RED → 失败的测试 (failing test)
GREEN → 最小化修复 (minimal fix)
REFACTOR → 清理代码 (cleanup)
```

在编写测试之前，Agent 不被允许编写 feature code。 ([志文工作室][3])

---

### 5. Automatic Code Review

每项任务完成后：

* spec 合规性检查
* code quality 检查
* 如果存在关键问题则阻断流程

---

### 6. Finish Branch

完成后：

* 验证测试
* merge branch
* 创建 PR
* 清理 workspace

---

## Built-in Skills (示例)

### Planning

* brainstorming
* writing-plans
* executing-plans

### Development

* test-driven-development
* using-git-worktrees
* subagent-driven-development

### Debugging

* systematic-debugging
* verification-before-completion

### Collaboration

* requesting-code-review
* finishing-development-branch

所有这些都是可组合的 skills。 ([GitHub][2])

---

## Why This Project Is Popular

它解决了 **AI coding 最核心的问题**：

没有 Superpowers 时：

* agent 编写凌乱的代码
* 没有测试
* 没有计划
* 随机的重构

有了 Superpowers：

* 设计先行
* 小步快跑
* 强制测试
* 必须评审
* 自主执行

它本质上是将 **LLM 转变为一名受过严谨训练的初级工程师 (disciplined junior engineer)**。

---

## Supported Agents

支持以下工具：

* Claude Code
* OpenCode
* Codex
* Cursor (通过手动方式)
* OpenClaw (社区用法)

---

## Example Commands

安装后：

```
/superpowers:brainstorm
/superpowers:write-plan
/superpowers:execute-plan
```

这些指令控制着 workflow。 ([GitHub][2])

---

## 一句话总结

**Superpowers 是一个利用模块化 skills 为 AI coding agents 构建的结构化 software engineering workflow。**

---

## 适用场景

在以下场景中尤其强大：

* 构建大型 app
* 长时间的自主编码
* 多文件重构
* TDD 工作流
* agent-driven development

在以下场景中作用较小：

* 快速脚本
* 微小修改
* 简单的 chat coding

---

如果你需要，我还可以解释：

* 它与 Claude Code 默认模式的区别
* 如何安装
* 它是否优于“跳过权限确认”类型的 agents
* 人们如何将其与 OpenClaw 配合使用

References:

* [https://github.com/obra/superpowers](https://github.com/obra/superpowers)
* [https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents](https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents)
* [https://new2026.medium.com/superpowers-obra-superpowers-claude-code-plugin-for-an-agentic-software-development-workflow-1e7bdffeb065](https://new2026.medium.com/superpowers-obra-superpowers-claude-code-plugin-for-an-agentic-software-development-workflow-1e7bdffeb065)
* [https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/](https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/)

[1]: https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents?utm_source=chatgpt.com "Superpowers: Agent Skill Framework & Software Development Workflow | AIToolly"
[2]: https://github.com/obra/superpowers?utm_source=chatgpt.com "GitHub - obra/superpowers: Claude Code superpowers: core skills library"
[3]: https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/?utm_source=chatgpt.com "什么是 Superpowers: AI 编程智能体的软件开发生命周期工作流 | Superpowers 教程 | OpenCodeDocs"