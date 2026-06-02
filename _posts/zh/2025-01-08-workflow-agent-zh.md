---
audio: true
generated: false
image: false
lang: zh
layout: post
title: Workflow 是 BFS，Agent 是 DFS
translated: true
type: post
---

根据 Anthropic 的定义 [^1]：

- **Workflow** 是通过预定义的代码路径来协调 LLM 和工具的系统。
- **Agent** 则是一个动态控制自己流程和工具使用的系统，具有灵活性来完成任务。

我从中理解到的是：

- 使用 **workflow** 来增强一个应用或平台就像是 **BFS（广度优先搜索）**，任务按系统化、逐层的方式完成。
- 使用 **agent** 更像是 **DFS（深度优先搜索）**，任务以探索性、逐步深入的方式进行。

有时候，**BFS** 和 **DFS** 可以结合使用。DFS 可以嵌套在另一个 DFS 中，BFS 也是如此。

举个例子，**o1（链式思考）** 就像 BFS。一开始，主要任务被划分为不同的步骤，每个步骤扩展为更详细的解释。然后，基于所有的思考，最终的结果被提供出来。

对于非常复杂的任务，比如让 AI 构建一个 YouTube 应用或者创建一个操作系统，AI 可以使用 BFS、DFS 或者两者的结合。具体使用哪一种方法取决于我们如何利用 BFS 和 DFS —— 有时候 AI 需要深入挖掘（DFS），有时候它需要扩展其思路（BFS）。

另外值得考虑的是，对于每一步，AI 应该评估下一步做什么，以达成目标。

**目标** 是一个有趣的方面。可能有很多目标，比如创建一个 YouTube 应用，AI 需要确保所有代码正常工作，所有功能都已实现，所有测试都通过。如何实现这些目标是很有趣的。AI 应该先解决一个目标，然后再解决下一个，还是说 AI 应该对所有目标同时进行一定进展，然后再继续处理每个目标？

---

[^1]: Building effective agents, [Anthropic](https://www.anthropic.com/research/building-effective-agents)
