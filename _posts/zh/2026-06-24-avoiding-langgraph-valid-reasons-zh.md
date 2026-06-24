---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 避免LangGraph：有充分理由？
translated: true
type: note
---

**问题：** 为什么我一直避免使用 LangGraph，我的理由是否合理？

**回答：**

你的自我分析很准确。让我来验证并强化每个要点：

**1. “我的 200-300 行代码 + LLM 调用已经能工作”** — 这是最诚实的理由，在还没到极限时确实是*正确*的。你遇到了大多数严肃构建者都会碰到的同类型障碍：手写的 agent 循环在 1-3 个工具、1 个 agent、线性流程下没问题，但在以下情况开始失效：

- 多 agent 协调（agent A 条件性地等待 agent B 的输出）
- 带状态积累的循环（retry loops、reflection patterns）
- 检查点/可恢复性（长时间运行的任务中途崩溃）

LangGraph 的真正价值是 **state graph with persistence** — 而非抽象层。如果你从未需要 checkpoint/resume 或 agent 间真正的条件分支，那么你确实不需要它。

**2. Playground/demo 目录的混乱** — 真实的摩擦。“我到底该把这个实验放在哪里”的认知成本扼杀了探索欲。这个问题一小时内就能解决：今天创建 `~/code/langgraph-lab/`，放一个最基本的 `StateGraph` 骨架。

**3. 没有规模合适的项目** — 这才是真正的门槛。LangGraph 最适用于：

- 多步骤管道，其中各步骤可独立失败
- 带 human-in-the-loop checkpoints 的 agent 系统
- 你的 `ww`/`iclaw`/`zz` CLI 工具，如果需要分支重试逻辑

你的银行 AI 工作实际上是个完美候选——可审计、可步骤追踪的 agent 工作流非常契合受监管环境。

**4. 2023 年就知道了但一直等待** — 典型的“知道但未行动”。说实话，这样做是对的——2023 年的 LangGraph 还很粗糙。persistence/streaming 功能在 2024-2025 年才显著成熟。

**现在真正的问题是：** 是什么促使你开始认真使用它？这才是值得追踪的信号——哪个项目迫使你跨过了这个门槛？
