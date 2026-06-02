---
audio: true
generated: false
image: false
lang: en
layout: post
title: Workflow is BFS, Agent is DFS
type: post
---

According to Anthropic [^1]:

- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents**, on the other hand, are systems where LLMs dynamically control their own processes and tool usage, maintaining flexibility in how tasks are accomplished.

What I understand from this is:

- Using **workflows** to enhance an app or platform is akin to **BFS (Breadth-First Search)**, where tasks are completed in a systematic, level-by-level manner.
- Using **agents** is more like **DFS (Depth-First Search)**, where tasks are tackled in a more exploratory, step-by-step fashion.

Sometimes, **BFS** and **DFS** can be combined. DFS can be nested within another DFS, and the same goes for BFS.

For example, **o1 (chain-of-thought)** is like BFS. Initially, the main tasks are divided into separate steps, and each step is expanded into more detailed explanations. Then, based on all the thinking, the final result is provided.

For very complex tasks, like asking AI to build a YouTube app or create an operating system, it could use BFS, DFS, or a combination of both. It really depends on how we utilize BFS and DFS — sometimes AI needs to dig deep (DFS), and sometimes it needs to expand its approach (BFS).

Another consideration is that for every step, AI should evaluate what to do next to hit its targets.

**Targets** are an interesting aspect. There may be many targets, such as creating a YouTube app, where the AI needs to ensure all code works well, all features are implemented, and all tests pass. The way to reach these targets is fascinating. Should AI tackle one target at a time, or should it make progress on all targets simultaneously and then iterate on each?

---

[^1]: Building effective agents, [Anthropic](https://www.anthropic.com/research/building-effective-agents)
