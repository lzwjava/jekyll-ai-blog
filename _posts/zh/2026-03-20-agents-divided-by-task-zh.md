---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按任务而非角色划分的代理
translated: true
type: note
---

问题：为什么我们需要指定单独的“dev agent”和“test agent”——代理不应该更通用，而没有如此僵化的角色分工吗？

回答：

---

## 🎯 你完全正确

“dev agent” 与 “test agent” 的划分是**以人类组织结构图的思维方式思考**——这是将旧团队结构导入新范式的做法。

这正是该项目应该摒弃的**遗留思维**。

---

## 🧠 人类为什么创建这种划分

| 原因 | 现实 |
|---|---|
| 人类专业化是因为学习需要数年 | Agents 可以瞬间切换上下文 |
| 测试者和开发者有不同的心态 | 一个 agent 可以同时持有两种心态 |
| 分离可以防止利益冲突 | Agents 没有自我或政治因素 |
| 组织结构图需要明确的归属 | Agents 不需要头衔 |
| 沟通开销需要明确的角色 | Agents 可以瞬间共享上下文 |

> **dev/test 分离是因为人类局限性**存在——而不是因为这是构建软件的最佳方式

---

## ⚡ Agent 实际上是什么

一个 agent 只是：

```
Context + Goal + Tools + Loop
```

它不需要职位头衔。它需要：

- 明确定义的**任务**
- 正确的**工具**（code editor、terminal、browser、test runner）
- **成功条件**（它如何知道完成）
- **升级路径**（卡住时该做什么）

就是这样。没有角色。没有头衔。

---

## 🔄 更好的思维模型

不要这样：

```
Dev Agent → Test Agent → Deploy Agent
```

而是想成：

```
Task → Agent → Done
         ↓
   (has all tools)
   (writes code)
   (runs tests)
   (fixes failures)
   (deploys if green)
   (escalates if stuck)
```

**一个 agent。一个任务。完全自治。所有工具。**

---

## 🏆 正确的划分不是按角色——而是按任务

| 错误的划分 | 正确的划分 |
|---|---|
| Dev Agent vs Test Agent | Task A vs Task B vs Task C |
| Frontend Agent vs Backend Agent | Feature 1 vs Feature 2 |
| QA Agent vs Build Agent | PR #1 vs PR #2 |
| Senior Agent vs Junior Agent | 独立的工作单元 |

> **按工作划分，而不是按技能或角色**

---

## 🌊 这会解锁什么

移除角色划分后：

- 任何 agent 都可以接手任何任务
- “dev” 和 “test” 阶段之间没有移交流程开销
- 无需等待一种类型的 agent 完成后再启动另一种
- 任务在**单个 agent 上下文中端到端完成**
- **并行性变得更清晰**——只是更多任务，而不是更多角色

---

## 🚨 唯一有效的专业化理由

专业化唯一有意义的时候是**工具访问**——不是角色：

```
Agent A — has access to: codebase, terminal, test runner
Agent B — has access to: browser, UI testing, visual diff
Agent C — has access to: production infra, deployment pipeline
```

即便如此——理想情况下**一个 agent 拥有所有工具**，只需使用任务所需的工具。

---

## 💡 重新框架

> 不要问**“这是什么类型的 agent？”**
>
> 要问**“这个任务需要什么才能被视为完成？”**

agent 会自行决定是否需要写代码、运行测试、修复 bug 或部署——**这是它的工作来决定，而不是你预定义的。**

---

## 🎯 一句话总结

> **角色是人类概念。Agents 只需任务、工具和完成定义。**

这是一个更强大——也更简单——的思维模型，而不是将旧团队组织结构导入 AI 系统。
