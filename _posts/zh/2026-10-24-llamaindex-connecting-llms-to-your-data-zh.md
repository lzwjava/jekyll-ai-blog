---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LlamaIndex：将LLM连接到您的数据
translated: true
type: note
---

**问题：** 什么是 LlamaIndex？

**答案：**

LlamaIndex 是一个开源的、基于 MIT 许可证的 Python 框架，用于在您自己的数据之上构建 LLM 应用。它最初名为 GPT Index，专门专注于将 LLM 与您的数据连接起来。

### 核心能力

它提供 ingestion pipelines、vector stores、query engines、structured extraction，以及一个在数据层之上进行推理的 agent layer。更具体地说，它帮助您从多种来源摄取和解析数据、构建索引、检索相关上下文并合成答案——并且它与许多托管的 LLM API 以及本地模型（例如通过 Ollama）集成。

### 最适合的场景

它最适合那些 agent 价值来自自身数据而不仅仅是模型的团队。关键用例包括：对大量内部文档语料库进行生产级 RAG、从杂乱的 PDF 和电子邮件中进行结构化提取、将查询数据层作为工具的 agents，以及混合关键字 + 向量检索 pipelines。

### 当前状态（2026）

2026 年的 LlamaIndex 不再“仅仅是一个 RAG 索引库”——它是一个事件驱动的 workflow 框架，具备生产级 runtime，并内置了 observability 和 evaluation 能力。

agent 类（`FunctionAgent`、`ReActAgent`）和 workflow primitive 将 LlamaIndex 从纯粹的 RAG 框架转变为具有强大检索基础的通用 agentic 框架。截至 2026 年年中，该框架版本为 0.14.x，拥有约 49,000 个 GitHub stars。

> **关于 TypeScript 的说明：** LlamaIndex.TS（TypeScript 移植版）已归档，自 2026 年起不再积极维护。Python 是当前积极维护的实现。

### 与 LangChain 对比

2026 年的关键结构性差异：LangChain 将 RAG 视为众多 runnable 之一；而 LlamaIndex 将 RAG 视为整个系统。

---

**参考文献：**

- [LlamaIndex Overview – EnterpriseDNA](https://enterprisedna.co/directories/open-source/llamaindex)
- [What is LlamaIndex in 2026 – FutureAGI](https://futureagi.com/blog/what-is-llamaindex-2026/)
- [LlamaIndex in 2026: Workflows & Production – FutureAGI](https://futureagi.com/blogs/exploring-llamaindex-a-powerful-tool-for-llms)
- [LlamaIndex – Real Python](https://realpython.com/ref/ai-coding-tools/llamaindex/)
- [LangChain vs LlamaIndex 2026 – Groovy Web](https://www.groovyweb.co/blog/langchain-vs-llamaindex-comparison)
