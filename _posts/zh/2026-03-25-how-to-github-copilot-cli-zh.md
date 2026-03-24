---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何使用 GitHub Copilot CLI
translated: true
type: note
---

Question: 如何使用显示的 `% copilot` CLI 界面来执行任务并获取答案？

Answer:

你看到的 `% copilot` CLI 是 **GitHub Copilot CLI** 的交互式界面。以下是它的工作原理以及如何高效使用它：

---

### 1. 启动 CLI

* 你通过输入 `% copilot`（如果已全局安装则输入 `copilot`）来启动它。
* 你将看到如截图所示的欢迎界面。

---

### 2. 基本工作流程

* 该 CLI 的工作方式**类似于基于 prompt 的 AI assistant**。
* 你用自然语言输入**任务（task）或问题（question）**。
* Copilot 将生成建议、code snippets 或答案。

**示例：**

```bash
% copilot
> Create a Python function to reverse a string
```

Copilot 将为你生成一个 code snippet。

---

### 3. 命令与技巧

* `/usage` — 显示当前 session 的使用指标和统计数据。
* `/exit` — 退出 CLI。
* 你也可以尝试使用 `/help` 等命令来查看其他内置选项。

---

### 4. 如何搜索答案

由于这是一个基于文本的界面：

1. 输入一个**清晰、简洁的问题**或任务描述。

   * 示例：`Search how to read a JSON file in Python`
2. Copilot 将生成以下内容之一：

   * 一个 code snippet
   * 操作说明
   * 相关示例

---

### 5. 安全与验证

* Copilot 的建议**可能包含错误**，因此请始终验证生成的代码或指令。
* 它最好被用作**任务的起点**，而不是最终的 production code。

---

### 6. 示例会话

```bash
% copilot
> Create a bash script to backup a folder
# Copilot 会建议一个脚本

> /usage
# 显示 session metrics

> /exit
# 退出 CLI
```

---

如果你需要，我可以制作一份 **Copilot CLI 简易速查表（cheat sheet）**，展示所有命令以及用于 coding、搜索和任务自动化的实用示例。

你需要我这样做吗？