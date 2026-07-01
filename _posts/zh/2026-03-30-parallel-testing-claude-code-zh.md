---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Claude Code 进行并行测试
translated: true
type: note
---

Question: 当 Claude Code 正在运行一项耗时任务（如 brainstorming、planning 或 executing）时，利用这段时间并行测试软件是一个好主意吗？

Answer:

是的，绝对如此 —— 这是在使用 AI coding assistants 时可以建立的最佳生产力习惯之一。以下是这种方式之所以高效的原因：

## 为什么并行测试（Parallel Testing）是有意义的

**Claude Code 本质上是异步的。** 当它在处理重型任务时 —— 比如生成计划、重构模块或编写 boilerplate —— 你的 CPU 和大脑大多处于空闲状态。如果你只是盯着进度条看，那就是在浪费时间。

## 实际工作流

```
[Window 1] Claude Code — planning / executing
[Window 2] 你的终端 — 运行测试、查看 logs、手动 QA
```

你可以运行：

- 在 Claude 编写新代码的同时，对现有代码运行 `pytest` / `jest` / `go test`
- 对 Claude 刚刚完成的上一个功能进行手动冒烟测试（smoke tests）
- 监控日志（`tail -f`、`docker logs`）以尽早发现 runtime 问题
- 运行耗时较长的 load tests 或 integration tests

## 为什么它特别有效

| Claude Code 阶段 | 你可以并行做的事情 |
| --- | --- |
| Brainstorming / planning | 查看之前的测试结果，编写 test cases |
| Code generation | 运行现有的 test suite |
| Refactoring | 对旧行为运行 regression tests |
| Debugging a problem | 在应用中手动复现 bug |

## 核心洞察

Claude Code 实际上**返还了被同步编程（synchronous coding）偷走的空闲时间**。与其按照“编程 → 停止 → 测试 → 停止 → 编程”的模式，你得到了一个**流水线（pipeline）**：

```
Claude codes → you test → Claude codes → you test
```

这与资深工程师的工作方式非常相似：在思考或编写代码时，后台总是在运行着某些任务。

## 一个实用小技巧

在窗口 2 中保留一个**临时记事本（scratch notepad）**。当你在测试中发现问题时，立即记录下来。当 Claude Code 完成当前任务后，你就拥有了一份准备好的后续 prompts 列表 —— 无需承受 context-switching 的成本。

所以，是的 —— 你只需要一个或两个窗口，利用 Claude 的执行时间进行并行测试是一个非常聪明的工作流。
