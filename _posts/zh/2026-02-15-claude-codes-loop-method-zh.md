---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 的不懈循环法
translated: true
type: note
---

**Question:** 在 Claude code 的语境下，“Ralph” 是指什么？

**Answer:**

“Ralph”（全名：**Ralph Wiggum loop** 或 **Ralph technique**）是指一种运行 **Claude Code**（Anthropic 推出的基于 CLI 的 AI coding agent）的流行方法，其核心在于使其处于**自主的、迭代的循环（autonomous, iterative loop）**中。

这个名字源于《辛普森一家》中那个执着但不太聪明的角色 Ralph Wiggum。之所以选择这个名字，是因为这个循环会“顽固”地持续运行，直到任务完成，带有一种幽默色彩。

### 核心理念

与其给 Claude Code 一个 prompt 并获得单次响应，不如将其放入一个重复循环中（通常是一个简单的 Bash `while` 循环），不断地将**相同的核心指令**反馈给 Claude。每一次迭代都会看到代码库的当前状态（包括之前的修改、error、测试失败等），因此 Claude 可以不断地进行完善、修复 bug、添加 feature 并持续改进，直到真正完成目标。

基础版本如下所示：

```bash
while true; do
    cat PROMPT.md | claude-code
done
```

更高级的版本会添加：

- 智能退出条件（例如：检测到 "DONE"、"<promise>COMPLETE</promise>" 或所有测试通过）
- Rate limiting 以避免消耗过多的 API 费用
- 进度追踪
- 防止死循环的安全机制

### 为什么它在 Claude Code 中流行起来

- Claude Code 在 agentic coding 方面能力极强（读写文件、运行命令、逐步思考），但它经常在取得部分进展后停止并等待用户输入。
- Ralph loop 摆脱了人工干预 → 你可以启动一个任务，然后去睡觉，回来时会看到一个完整得多的实现。
- 它有助于应对 **"context rot"**（上下文腐化）——即在极长的单次对话中 Claude 的注意力会逐渐下降。通过在每个循环提供新鲜的 context window，同时在磁盘上持续累积成果，可以有效解决这一问题。

### 命名者 / 推广者

Geoffrey Huntley → 他撰写了病毒式传播的文章 "Ralph Wiggum as a software engineer"，并展示了循环往复的简单坚持往往优于等待一个更聪明的 one-shot model。

### 现代实现（截至 2026 年初）

- 纯 Bash 循环（原始风格）
- **ralph-claude-code** (frankbria 的 GitHub 项目) —— 增加了智能退出检测、rate limiting 等功能。
- Anthropic 官方为 Claude Code 提供的 **Ralph Wiggum plugin**（官方集成）。
- 各种支持进度文件、PRDs（产品需求文档）、commit-after-each-feature 模式等的 fork 和封装工具。

简而言之：**Ralph = 让 Claude Code 在无人值守的循环中不懈地处理你的项目，直到任务真正完成。**

**References:**

- [https://github.com/frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
- [https://ghuntley.com/ralph/](https://ghuntley.com/ralph/)
- [https://ghuntley.com/loop](https://ghuntley.com/loop)
- [https://news.ycombinator.com/item?id=46682325](https://news.ycombinator.com/item?id=46682325)
