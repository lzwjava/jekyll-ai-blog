---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot 方案与代理模式详解
translated: true
type: note
---

**问题：** 在使用 GitHub Copilot 时，我们可以使用 Plan Mode 或 Agent Mode 来帮助修复 Merge Conflicts 吗？请介绍一下 Plan Mode 并解释它与 Agent Mode 的区别。

---

**回答：**

## GitHub Copilot: Plan Mode vs Agent Mode

是的 —— GitHub Copilot 中的 Plan Mode 和 Agent Mode 都可以辅助进行 Merge Conflict 的解决以及复杂的多文件修复。以下是详细的解析。

---

## 概述：双模式系统

GitHub 的双模式方法将“思考”与“执行”分离：一种模式负责起草一个具体的、可审计的计划；另一种模式则可靠地执行更改并对其进行验证。

Plan Mode 允许你在 Agent 开始编写代码之前审查并批准蓝图，而 Agent Mode 则通过分析代码、提议编辑、运行测试以及跨多个文件验证结果来帮助进行大规模的更改。

---

## Plan Mode —— 它是什么

Plan Mode 负责创建、改进并执行循序渐进的实施计划。它会分析你的 Codebase，生成详细的执行计划，并在**开始编写代码之前**验证需求是否已被涵盖。

Plan 代理使你能够在开始实施之前创建详细的实施计划，以确保满足所有需求。通过 Todo Lists，由于代理可以确保它专注于总体目标并有效地跟踪进度。

### 如何在 VS Code 中激活 Plan Mode

打开 Chat 视图（`Ctrl+Alt+I`），然后从代理下拉菜单中选择 **Plan**。或者，输入 `/plan` 后跟你的任务描述，即可切换到 Plan 代理并一步开始规划。

### Planning 的内部工作原理

当开发者要求 Copilot 执行复杂的、多步骤的任务时，它会决定是直接响应还是激活其 Planning Mode。简单的 Prompts 会得到快速回答，而多步骤的 Prompts 则会触发协调一致的计划。调用时，Planning 会创建一个 **Markdown 文件**，定义任务、研究步骤以及每个执行步骤开始时的进度更新。随着 Copilot 的工作，它会修订并完善计划 —— 以适应新的 Context 或结果。

### 用于 Merge Conflicts 的 Plan Mode

当你希望首先**审查解决策略**以处理跨多个文件的冲突时，这是理想的选择 —— Copilot 会提议触及哪些文件、进行哪些更改以及按什么顺序进行，而你**在任何代码更改之前进行批准**。

---

## Agent Mode —— 它是什么

Agent Mode 允许你交给 Copilot 一个高层次的 Prompt，然后观察它自主地规划步骤、选择正确的文件、运行 Tools 或 Terminal 命令，并对代码编辑进行迭代直至任务完成。它可以对整个项目进行推理，采取多步骤操作，并在整个 Session 中保留大量的 Context。

Agent Mode 不仅重写你指定的行，还会分析相关的代码，识别可能需要的额外更改，并在整个项目中应用它们以保持一致性。

Agent Mode **自动**应用编辑，而不是在每一步都等待明确的批准，同时仍会将任何具有潜在风险的命令展示出来供运行前审查。

### 用于 Merge Conflicts 的 Agent Mode

你用自然语言描述冲突解决目标，Copilot 会自主编辑所有受影响的文件，运行测试并进行迭代，直到任务完成 —— 且干扰极小。

---

## 核心区别：Plan Mode vs Agent Mode

| 维度 | Plan Mode | Agent Mode |
|---|---|---|
| **主要目的** | 先制定策略和蓝图 | 自主执行 |
| **人为控制** | 执行前由你批准计划 | 自动应用编辑；标记风险命令 |
| **代码何时更改** | 在你审查并批准计划后 | 立即且持续地 |
| **最适用场景** | 复杂、高风险或多团队任务 | 需求明确、需要快速执行的任务 |
| **输出** | 结构化的 Markdown 计划 + Todo List | 跨文件的实际代码更改 |
| **透明度** | 高 —— 你在每一步执行前都能看到 | 中等 —— 你看到结果，而非预先批准的步骤 |
| **理冲突用例** | 规划跨多个文件的冲突解决策略 | 一旦策略明确，自动修复冲突 |

---

## 它们如何协同工作（Merge Conflicts 推荐工作流）

最佳实践是**按顺序同时使用两者**：

1. **先使用 Plan Mode** —— 描述 Merge Conflict 的情况。Copilot 生成一个分步计划，展示哪些文件存在冲突以及如何解决它们。审查并编辑该计划。
2. **后使用 Agent Mode** —— 计划获批后，切换到 Agent Mode（或让 Copilot 执行该计划），它将在所有冲突文件中自动执行更改。

Plan Mode 在任何代码更改之前提供了一个清晰、可编辑的蓝图。Agent Mode 执行了多文件编辑、运行了测试并开启了 PR，速度比手动编写脚本还要快。两者结合使用，感觉就像一个可靠的 Co-pilot，而不仅仅是另一个工具。

---

## 何时使用哪种模式

当你希望对 Copilot 提议的编辑进行更细粒度的控制时，请使用 Edit/Plan Mode —— 例如，当你想要对定义的一组文件进行快速、特定的更新，或想要完全控制所使用的 LLM 请求数量时。当你心目中有特定任务并希望授权 Copilot 自主编辑代码时，请使用 Agent Mode —— 特别是当你的任务很复杂且涉及多个步骤、迭代和错误处理时。

---

## 可用性

JetBrains、Eclipse、Xcode 和 VS Code Insiders 在企业、组织和用户级别均支持 Plan Mode 遥测。预计 VS Code 稳定版很快将正式发布。

截至 2026 年 3 月，Agent Mode 已在 VS Code 和 JetBrains 上正式发布（General Availability） —— 这是一个重要的里程碑，因为此前它仅限于 VS Code。

---

**参考文献：**

- [GitHub Copilot Features — GitHub Docs](https://docs.github.com/en/copilot/get-started/features)
- [About GitHub Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Planning with Agents in VS Code](https://code.visualstudio.com/docs/copilot/agents/planning)
- [Copilot Ask, Edit, and Agent Modes — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/copilot-ask-edit-and-agent-modes-what-they-do-and-when-to-use-them/)
- [GitHub Copilot in VS Code Upgrade — GitHub Changelog](https://github.blog/changelog/2025-10-28-github-copilot-in-visual-studio-code-gets-upgraded/)
- [Copilot Metrics Now Includes Plan Mode](https://github.blog/changelog/2026-03-02-copilot-metrics-now-includes-plan-mode/)
- [Plan Mode vs Agent Mode — Skywork AI](https://skywork.ai/blog/agent/plan-mode-vs-agent-mode-understanding-githubs-revolutionary-coding-workflows/)
- [Use Agent Mode — Microsoft Learn (Visual Studio)](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-agent-mode?view=visualstudio)
