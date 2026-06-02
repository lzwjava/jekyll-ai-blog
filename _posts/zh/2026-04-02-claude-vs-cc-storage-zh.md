---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 代码 vs CC 存储架构
translated: true
type: note
---

问题：CC code 中的对话存储和提示结构是什么，它与 Claude Code 相比如何？

回答：

Claude Code 中的提示/对话结构比大多数“CC-style”代码助手（如简单的基于聊天的代码副驾驶）**更结构化和分层**。它专为**长时间编码会话、repo-aware reasoning 和 tool use**而设计。

以下是典型架构。

---

# Claude Code 提示结构（概念性）

Claude Code 在每次回合内部构建**多层提示**：

### 1. 系统层（固定）

* coding rules
* tool usage instructions
* diff format requirements
* safety + file edit policies

示例（概念性）：

```
You are Claude Code.
You can read/write files.
Return edits as unified diffs.
Prefer minimal changes.
```

---

### 2. 项目上下文层

自动注入：

* repo tree
* relevant files
* open files
* git status
* recent edits

示例：

```
Repository:
src/
  api.ts
  db.ts
tests/
  api.test.ts
```

这**不是聊天历史**——它是**状态快照**。

---

### 3. 对话记忆层

仅最近回合（滑动窗口）

```
User: refactor db layer
Assistant: suggested changes
User: make it async
```

Claude Code **不会保留完整历史**
它会压缩/总结较旧的回合。

这很重要：

* 避免 token 爆炸
* 保持推理专注
* 改善长时间编码会话

---

### 4. 工具结果层

Claude Code 大量使用工具输出：

* file reads
* grep search
* AST search
* test results
* lint output

示例：

```
Tool: read_file src/db.ts
Result: ...
```

这会成为提示的一部分。

这与典型的 CC 助手**非常不同**。

---

### 5. 草稿本/规划层（隐藏）

Claude Code 内部执行：

* plan
* reasoning
* edit strategy
* multi-step actions

然后输出：

* explanation
* diff
* commands

---

# 与典型的“CC”聊天代码助手比较

大多数 CC-style 助手：

### 简单结构

```
system prompt
chat history
user message
```

有时加上：

* selected code
* open file

仅此而已。

没有：

* repo memory
* tool chaining
* diff planning
* execution loop

---

# Claude Code 更接近代理循环

它的工作方式如下：

```
read files
↓
reason
↓
edit
↓
run tests
↓
fix
↓
repeat
```

每个步骤附加到提示中。

因此对话变为：

```
User request
Tool read files
Plan
Apply diff
Run tests
Fix errors
Return result
```

这是**有状态执行**，而非仅聊天。

---

# 关键差异

| Feature        | CC-style chat   | Claude Code          |
| -------------- | --------------- | -------------------- |
| History        | full chat       | sliding + summarized |
| Repo awareness | weak            | strong               |
| Tool use       | limited         | heavy                |
| File edits     | text suggestion | structured diffs     |
| Planning       | minimal         | multi-step           |
| Execution loop | no              | yes                  |
| Memory         | conversation    | project state        |

---

# 为什么 Claude Code 感觉更智能

因为提示包含：

* repo structure
* recent edits
* tool outputs
* plan
* diff format

而非仅：

```
"Here is code, fix bug"
```

它变为：

```
Here is repo
Here is failing test
Here is file
Here is previous attempt
Fix correctly
```

信号强度更高。

---

# 真实心智模型

Claude Code 每次回合的提示：

```
[system rules]
[repo snapshot]
[relevant files]
[conversation summary]
[last tool outputs]
[user request]
```

然后：

```
→ plan
→ modify
→ run tools
→ finalize
```

---

如果您正在与以下进行比较：

* Cursor
* Copilot Chat
* OpenCode
* OpenClaw

我也可以分解它们——它们都以不同方式构建提示。
