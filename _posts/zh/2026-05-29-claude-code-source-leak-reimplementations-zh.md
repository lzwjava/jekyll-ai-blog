---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude代码源代码泄露重实现
translated: true
type: note
---

**问题：** 目前最好的 Claude Code 开源项目/重新实现有哪些？

**回答：**

重大消息：**2026年3月31日**，Anthropic 意外将 source map 随 Claude Code npm 包一起发布，暴露了完整的 TypeScript 源代码（约1,884个文件）。Chaofan Shou 发现，已发布 npm 包中嵌入的 source map 文件在 JSON 的 `sourcesContent` 键下包含了原始 TypeScript 源代码。这引发了重新实现的热潮。以下是现状：

---

## 泄露的源代码

**[yasasbanukaofficial/claude-code](https://github.com/yasasbanukaofficial/claude-code)**
原始的泄露 TypeScript 源代码——即实际的 Claude Code CLI 代码库，包含工具调用、agent 工作流和终端 UI。已归档供教育用途。注意：这只是骨架，不是模型/大脑。

**[chauncygu/collection-claude-code-source-code](https://github.com/chauncygu/collection-claude-code-source-code)**
一个收集中心，归档了原始的泄露 TypeScript 源代码，并包含多个从不同角度研究 Claude Code 的子项目——架构分析、研究报告和洁净室重新实现。

---

## 最佳重新实现

### 1. `nano-claude-code`（Python）—— 学习内部机制的最佳选择
一个最小化、完全可运行的 Python 重新实现，已从一个约900行的 v1.0 原型发展到约5,000行的 v3.0，具备多 agent 编排、持久记忆和技能系统。与架构研究不同，它是一个可以立即使用的真实编码助手。支持20多种模型：Anthropic、OpenAI、Gemini、DeepSeek、Ollama、LM Studio。

工具覆盖范围：Read、Write、Edit、Bash、Glob、Grep、WebFetch、WebSearch、MemorySave/Delete/Search、Agent、SendMessage、Skill、SkillList——以及内置的 `/commit`、`/review` 和自定义 markdown 技能，支持参数替换和分支/内联执行。

**如果你想理解 agent 循环架构，这是最好的学习对象。**

### 2. `ruvnet/open-claude-code`（TypeScript）—— 最佳洁净室即插即用替代品
一个洁净室实现（未使用泄露源代码），镜像了实际 Claude Code 架构：异步生成器 agent 循环、25个工具、4种 MCP 传输方式（stdio、SSE、Streamable HTTP、WebSocket）、6种权限模式、钩子、设置链、会话。支持 Anthropic、OpenAI、Gemini、AWS Bedrock、Google Vertex。自动化夜间发布，包含903+ 测试。

```bash
npx @ruvnet/open-claude-code "解释这个代码库"
```

### 3. `openclaw/openclaw` —— 架构比较中被广泛引用
在多篇分析中被提及，作为与原文最接近的对等实现。用于与 Claude Code 和 Hermes-Agent 一起进行跨系统比较，以分析 agent 设计原则。

---

## GitHub 趋势（claude-code 主题，2026年5月）

当前最热门的仓库（按星标数）：
- **"Bash is all you need"** —— 一个类似 nano-claude-code 的 agent 工具集，从头用 Python 构建（约61.9k星标）
- **awesome-claude-skills** —— 精选的技能、MCP 和工作流自动化工具列表（约59.6k星标）
- **omo（oh-my-opencode）** —— TypeScript agent 工具集/TUI，原名 oh-my-opencode（约43.2k星标）

---

## AI 工程师应该学习什么

| 仓库 | 重要性 |
|------|--------|
| `nano-claude-code` | 简洁的 Python agent 循环——从头到尾阅读源码 |
| 泄露的 TypeScript 源代码 | 查看实际的系统提示、工具架构、自修复机制 |
| `ruvnet/open-claude-code` | 生产质量的洁净室实现；MCP 传输实现的良好参考 |
| `VILA-Lab/Dive-into-Claude-Code` | 系统化的分析框架，追溯设计价值观 → 原则 → 实现——适合理解为什么做出某些架构选择，而不仅仅是它们是什么 |

泄露事件最大的启示：在 Claude Code 中，跨领域的集成机制——而非模块化功能——才是工程复杂性的真正所在。工具循环、权限系统和上下文管理相互渗透。值得专门研究这一点。

---

**参考资料：**

- [chauncygu/collection-claude-code-source-code](https://github.com/chauncygu/collection-claude-code-source-code)
- [ruvnet/open-claude-code](https://github.com/ruvnet/open-claude-code)
- [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)
- [GitHub claude-code 主题](https://github.com/topics/claude)