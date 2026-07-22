---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 苹果派轻量级子代理扩展
translated: true
type: note
---

问题：`https://github.com/dodo-reach/apple-pi` 是什么？

回答：

`apple-pi` 是一个 **Pi 编码代理的扩展**，用于添加**轻量级进程内子代理**。它并非让单个 LLM 完成所有任务（规划、搜索、编辑、推理），而是允许父代理将任务的一部分委托给并行运行的专业化代理。([Pi][1])

概念上：

```
           父代理
              │
     委托(任务列表)
              │
     ┌──────────┼──────────┐
     │          │          │
  scout      scout      worker
 (Haiku)    (Haiku)    (Sonnet)
 只读        grep等    编辑/bash
     │          │          │
     └──────────┼──────────┘
              │
       合并结果返回
```

设计目标：

* 每个子代理使用**更小的上下文窗口**。
* **并行执行**（`Promise.allSettled`）。
* **不同任务使用不同模型**，例如：

  * Claude Haiku → 仓库搜索
  * Claude Sonnet → 代码编辑
  * GPT-5 → 规划
* **无子进程**——每个子代理只是同一进程中的另一个 `Agent` 对象，因此生成它们的成本远低于启动多个 CLI 实例。([Pi][1])

示例工作流：

```
用户：
    重构认证模块。

父代理：
    委托：
        - 查找认证代码
        - 检查测试
        - 实施变更

Scout #1：
    grep 认证相关文件

Scout #2：
    检查测试

Worker：
    修改代码

父代理：
    总结并生成最终响应
```

每个代理定义为一个带有 YAML 前置元数据的 Markdown 文件，例如：

```yaml
---
name: scout
description: 快速仓库侦察
model: anthropic/claude-haiku-4-5
thinking: off
tools:
  - read
  - grep
  - find
  - ls
---
你只搜索代码库。
永远不要编辑文件。
```

该扩展从以下位置发现这些代理定义：

1. `.pi/agents/`（项目）
2. `~/.pi/agent/agents/`（用户）
3. 内置默认值

允许项目定义自定义专业代理。([Pi][1])

### 为什么这很有趣

这与现代代理系统所使用的架构非常相似：

* Claude Code 的任务委托
* Codex 的工作代理
* OpenAI 的多代理编排
* Gemini 的规划/执行分离

关键思路是：

> 一个大的上下文通常不如多个聚焦的上下文高效。

与其给一个模型 100k 个 token，不如给三个小代理各 10k 个 token，让它们独立工作，然后综合输出。

既然你最近一直在讨论 Pi 和 CLI 原生代理，这个仓库本质上就是在 Pi 内部演示这一理念：**廉价、可组合、并行的代理执行，而非单一的助手。**

参考资料：

* Pi 包页面（README 和架构）：[https://pi.dev/packages/apple-pi](https://pi.dev/packages/apple-pi) ([Pi][1])
* Pi 项目概览：[https://github.com/earendil-works/pi](https://github.com/earendil-works/pi) ([GitHub][2])

[1]: https://pi.dev/packages/apple-pi?page=58&utm_source=chatgpt.com "apple-pi · Packages · Pi"
[2]: https://github.com/earendil-works/pi/blob/main/README.md?utm_source=chatgpt.com "pi/README.md at main · earendil-works/pi · GitHub"