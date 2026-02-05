---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 谷歌 ADK 最新更新详解
translated: true
type: note
---

我将搜索有关 Google 的 agentic 模式开发 SDK 的最新信息。

# Google Agent Development Kit (ADK): 全面介绍

Google 的 Agent Development Kit (ADK) 是一个用于开发和部署 AI agents 的灵活、模块化、开源框架。它在 Google Cloud NEXT 2025 上发布，旨在让构建复杂的多智能体（multi-agent）系统感觉更像传统的软件开发。

## 什么是 ADK？

虽然针对 Gemini 和 Google 生态系统进行了优化，但 ADK 是 model-agnostic（模型无关）和 deployment-agnostic（部署无关）的，旨在与其他框架兼容。该框架驱动了 Google 产品（如 Agentspace 和 Google Customer Engagement Suite）中的 agents，目前 Google 已将其面向开发者开源。

## 核心特性

**Multi-Language 支持**：ADK 提供 Python、TypeScript、Go 和 Java 版本，允许开发者使用自己擅长的语言进行工作。

**Multi-Agent 编排（Orchestration）**：使用工作流 agents（Sequential、Parallel、Loop）定义可预测的 pipeline，或利用 LLM 驱动的动态路由实现自适应行为。通过在层级结构中组合多个专业 agents，构建模块化、可扩展的应用。

**Model 灵活性**：内置与 LiteLLM 和 Vertex AI Model Garden 的集成，支持除 Gemini 之外的多种模型。

**内置开发工具**：包含开发 UI，用于帮助测试、评估（evaluate）、调试和展示 agents。

**双向流（Bidirectional Streaming）**：支持双向流以实现实时 agent 交互。

**A2A 协议支持**：集成 A2A 协议，用于远程 agent-to-agent 通信。

## 开始使用

不同语言的安装均非常直接：

**Python**: `pip install google-adk`  
**TypeScript**: `npm install @google/adk`  
**Go**: `go get google.golang.org/adk`  
**Java**: 通过 Maven 或 Gradle 添加依赖

这是一个简单的 Python 示例：

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

## Multi-Agent 模式

ADK 支持多种构建多智能体系统的模式：

**Sub-Agents**：创建层级结构，由一个协调器 agent 管理专门的 sub-agents。然而，当 root agent 调用 sub-agent 时，责任会完全转移给该 sub-agent，这可能会限制多步工作流。

**Agent Tools**：这是一种更强大的模式，将专门的 agents 视为 root agent 工具箱中的 tools，允许其对复杂查询进行推理，并使用多个 agents 来完成任务。

## Google Cloud 集成

建议将 ADK agents 部署到 Vertex AI Agent Engine Runtime，这是一个全托管的 Google Cloud 服务，专为部署、管理和扩展 AI agents 而设计。这提供了企业级基础设施，并可访问 100 多个预构建的连接器（connectors），以及与 BigQuery、AlloyDB 和其他 Google Cloud 服务的集成。

## ADK 与其他框架对比

与 Genkit（Google 的另一个框架）相比，ADK 针对具有更高层抽象的复杂 agents 和多智能体系统进行了优化，而 Genkit 则为更广泛的 AI 驱动体验提供基础构建块。

## 资源

- **文档**: https://google.github.io/adk-docs/
- **GitHub**: https://github.com/google/adk-python
- **Google Cloud 文档**: https://cloud.google.com/agent-builder/agent-development-kit/overview

ADK 代表了 Google 让 agentic AI 开发更易触达的愿景，它将开源软件的灵活性与 Google AI 及云生态系统的深度集成相结合。