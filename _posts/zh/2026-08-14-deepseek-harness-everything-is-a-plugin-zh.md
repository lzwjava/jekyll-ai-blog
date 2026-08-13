---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek驾驭框架：万物皆可插件
translated: true
type: note
---

问题：什么是 DeepSeek Harness？`deepseek-ai/deepseek-harness` 介绍

答案：

DeepSeek Harness 是 DeepSeek 推出的一个**智能体运行时 / 智能体框架**。核心思想是：

> **万物皆插件。**

与其将 AI 智能体构建为固定流程：

```
LLM
 |
提示词
 |
工具
 |
记忆
 |
沙箱
 |
UI
```

DeepSeek Harness 将每个组件视为可替换的：

```
                 Agent Runtime

        +----------------------+
        |       Core Loop      |
        +----------------------+

        /        |        \
     Model      Tools    Memory
      |          |          |
   GPT/Qwen   Shell     Vector DB

        \        |        /
          Everything = Plugin
```

代码仓库是 `deepseek-ai/deepseek-harness`。GitHub 上描述为 **"DeepSeek Harness: Everything is a Plugin"**，且主要用 TypeScript 实现。

---

## 为什么需要“harness（运行时框架）”？

这个词来自软件测试/机器人领域：

* test harness = 控制实验的环境
* robot harness = 围绕能力的控制系统
* LLM harness = 控制智能体的运行时

仅凭一个 LLM：

```
input -> transformer -> output
```

并不能成为智能体。

一个智能体需要：

```
观察
  |
推理
  |
选择行动
  |
调用工具
  |
修改环境
  |
再次观察
```

Harness 提供了这个循环。

---

## 与 LangChain / AutoGen / CrewAI 的比较

粗略对比：

| 框架               | 核心理念                         |
| ----------------- | -------------------------------- |
| LangChain         | 可组合的 LLM 应用库               |
| AutoGen           | 多智能体对话框架                  |
| CrewAI            | 基于角色的智能体团队              |
| OpenAI Agents SDK | 简单的生产级智能体运行时          |
| DeepSeek Harness  | 基于插件的可编程智能体操作系统    |

有趣之处在于**架构理念**。

LangChain：

```
Chain = A -> B -> C
```

DeepSeek Harness：

```
Runtime
 |
 +-- Model plugin
 +-- Tool plugin
 +-- Sandbox plugin
 +-- Storage plugin
 +-- UI plugin
 +-- Scheduler plugin
```

更像 Linux 内核模块。

---

## “万物皆插件”思想

示例：

模型：

```ts
plugins.model = [
    "deepseek",
    "openai",
    "qwen",
    "local-llama"
]
```

工具：

```ts
plugins.tools = [
    "shell",
    "browser",
    "git",
    "database"
]
```

记忆：

```ts
plugins.memory = [
    "sqlite",
    "redis",
    "vector-db"
]
```

智能体无需关心实现细节。

---

## 为什么这很重要

当前 AI 智能体工程存在一个问题：

每家公司都在构建：

```
my-agent/
  prompt.py
  tools.py
  memory.py
  workflow.py
```

6 个月后：

* 无法切换模型
* 无法回放失败
* 无法调试
* 无法基准测试

Harness 试图让智能体更像操作系统：

```
Application
    |
Agent API
    |
Agent Runtime
    |
Plugins
    |
Infrastructure
```

---

## 重要概念：轨迹（trajectory）

现代智能体需要可观测性。

一个好的 harness 会记录：

```
Session:

User:
"修复这个 bug"

Agent:
<思考>
需要检查仓库
</思考>

Tool:
git status

Tool:
pytest

Agent:
修改文件

Tool:
git diff

Result:
success
```

然后你可以：

* 回放
* 调试
* 对比模型
* 训练未来的智能体

这对于编码智能体尤为重要。

---

## 与 Claude Code / Codex 的关系

趋势是：

### 2023

提示词工程：

```
system prompt
+
few examples
```

### 2024

工具调用：

```
LLM
 |
tools
```

### 2025-2026

智能体运行时：

```
LLM
 |
Harness
 |
Tools
 |
Memory
 |
Environment
```

Claude Code、Codex 风格的编码智能体、SWE-agent、OpenHands 都朝着这个方向前进。

---

## 对于正在构建智能体的人，值得关注的要点

有价值的资产不是提示词。

提示词：

```
You are a coding agent...
```

很容易复制。

难点在于：

```
agent runtime
+
tool ecosystem
+
evaluation
+
trajectory data
+
plugin architecture
```

这才是护城河。

这类似于操作系统：

Linux 胜出不是因为某个 shell 命令。

它胜出是因为创造了稳定的抽象层：

```
hardware -> kernel -> applications
```

智能体 harness 正试图创建：

```
model -> harness -> agent applications
```

---

## 我的看法

DeepSeek Harness 是一个信号，表明行业正在从：

> “我们如何造出更聪明的模型？”

转向：

> “我们如何围绕模型构建可靠的自主系统？”

下一代 AI 公司可能不会训练基础模型。他们可能构建**智能体操作系统层**。

参考资料：

* [DeepSeek Harness GitHub](https://github.com/deepseek-ai/deepseek-harness?utm_source=chatgpt.com)
* [DeepSeek GitHub organization](https://github.com/deepseek-ai?utm_source=chatgpt.com)
