---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OASIS 社交媒体模拟框架
translated: true
type: note
---

我会获取 GitHub 仓库，为您介绍 OASIS。## OASIS 介绍

OASIS 是一个开源的社交媒体模拟器，它使用 large language model agents 来真实模拟像 Twitter 和 Reddit 这样的平台上多达一百万用户的行为。它旨在促进对复杂社会现象的研究，例如 information spread、group polarization 和 herd behavior。

### 主要特性

**Scalability**：OASIS 支持多达一百万 agents 的模拟，使研究社交媒体动态的规模与真实世界平台相当。

**Dynamic Environments**：系统适应社交网络和内容的实时变化，镜像像 Twitter 和 Reddit 这样的平台的流动动态，提供真实的模拟体验。

**Rich Interactions**：Agents 可以执行 23 种动作，例如 following、commenting 和 reposting，从而实现多方面的互动。

**Smart Recommendations**：它具有基于兴趣和 hot-score 的推荐算法，模拟用户如何在社交媒体平台上发现内容并互动。

### 使用场景

该平台支持多种研究和行业应用，包括：

- 研究社会现象的 simulations
- 内容互动分析
- 用户行为预测
- 社交动态实验

### 快速上手

该框架可以通过 PyPI 获取（`pip install camel-oasis`），并使用 OpenAI 的 API 为 agent 提供智能。您定义 agent profiles，指定可用 actions，创建 environment，然后使用手动或 LLM-driven agent actions 运行 simulations。

### 技术细节

- 使用 Python 构建，文档可在 docs.oasis.camel-ai.org/ 获取
- Apache 2.0 许可
- CAMEL-AI 生态系统的一部分
- 包含 simulation data 的 visualization 和 analysis 工具

这对于研究人员特别有价值，他们可以在前所未有的规模上研究 social dynamics，而不受真实平台实验的伦理约束。
