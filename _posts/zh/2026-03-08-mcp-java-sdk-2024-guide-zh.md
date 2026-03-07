---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MCP Java SDK 2024 概述指南
translated: true
type: note
---

## MCP Java SDK — 全面介绍

---

### 1. MCP 是什么？

Model Context Protocol (MCP) 是一种开放协议，它标准化了应用程序向大型语言模型 (LLMs) 提供上下文的方式。它提供了一种标准化的方式，将 AI 模型连接到不同的数据源和工具，使集成无缝且一致，并帮助您在 LLMs 基础上构建代理和复杂工作流。

---

### 2. 起源与历史

Spring AI MCP 于 2024 年 12 月 11 日推出，作为 Model Context Protocol 的强大 Java SDK 实现——这是 Spring AI 生态系统的新增功能，为 Java 平台带来了标准化的 AI 模型集成能力。

最初作为一个实验项目，后来移入官方 MCP Java SDK。该 SDK 是该协议的最新语言绑定，与 Python、TypeScript 和 Kotlin SDK 并列，可在 modelcontextprotocol.io 获取。

该项目已达到 1.0.0 GA 版本，符合 2025-06-18 MCP 规范，并支持多个版本的协议版本协商，包括 2024-11-05、2025-03-26 和 2025-06-18。

---

### 3. 核心架构

MCP 通过两个概念层定义通信：**Data Layer**，它定义了客户端-服务器通信和生命周期管理的协议；**Transport Layer**，它定义了客户端和服务器使用的通信通道和机制。

Java SDK 将这些映射到三个主要架构层：

- **Client/Server Layer** (`McpClient` / `McpServer`)：两者均使用 `McpSession` 进行同步/异步操作，其中 `McpClient` 处理客户端协议操作，`McpServer` 管理服务器端协议操作。
- **Session Layer** (`McpSession`)：使用 `DefaultMcpSession` 管理通信模式和状态。
- **Transport Layer** (`McpTransport`)：通过 HTTP Streamable-HTTP 和 SSE 传输处理 JSON-RPC 消息的序列化/反序列化，并提供 Java HttpClient、Spring WebFlux 和 Spring WebMVC 的专用模块。

整体系统遵循 **host-client-server** 拓扑：**Host** 负责管理一个或多个 MCP 客户端、强制执行安全策略，并协调 LLM 与可用工具之间的交互。**Client** 与单个 MCP 服务器建立并维护专用的、有状态的一对一连接。**Server** 为 MCP 客户端提供上下文和能力。

---

### 4. 关键特性

MCP Java SDK 的关键特性包括：

- 支持同步和异步 MCP 通信
- 启用协议版本兼容性协商，实现平滑互操作性
- 动态发现、注册和执行工具
- 接收工具和资源的实时列表变更通知
- 使用 URI 模板管理资源，实现结构化访问和订阅
- 检索和管理提示，以自定义 AI 模型行为
- 支持采样策略，以微调 AI 交互
- 基于 STDIO 的传输，用于直接进程通信
- 基于 Java HttpClient 的 SSE 客户端传输，用于基于 HTTP 的流式传输
- 基于 Servlet 的 SSE 服务器传输，用于传统服务器环境中的 HTTP 流式传输
- 基于 Spring 的传输，实现与 Spring Boot 的无缝集成

---

### 5. 双 API 模型：Sync 与 Async

SDK 为阻塞式 (`McpSyncClient` / `McpSyncServer`) 和响应式 (`McpAsyncClient` / `McpAsyncServer`) 编程模型提供一流支持。

MCP 基于 JSON-RPC 的异步特性，并定义了双向协议，明确支持异步和流式交互。SDK 使用 **Project Reactor** 作为 Reactive Streams 规范的实现。Reactor 成熟、广泛采用、提供丰富的操作符，并通过上下文传播与可观测性集成良好。

---

### 6. MCP 原语（构建块）

原语是 MCP 的基本构建块。它们定义了上下文信息类型和可执行操作范围。服务器和客户端均提供原语。

#### 服务器原语

服务器原语包括 **Tools**、**Resources** 和 **Prompts**。Tools 是 AI 应用程序可用于执行操作的可执行函数，例如查询数据库或文件操作。Resources 是为客户端提供上下文信息的数据源，例如数据库模式或文件内容。Prompts 是可重用的模板，帮助与语言模型交互。

#### 客户端原语

客户端原语允许 McpServer 作者构建更丰富的交互，包括 **Sampling**、**Elicitation** 和 **Logging**。Sampling 允许服务器在不想在服务器端包含模型 SDK 时，从客户端请求语言模型补全。Elicitation 使服务器能够请求用户额外信息或确认任何操作。

---

### 7. 传输机制

本地服务器使用标准输入和输出 (STDIO) 用于本地进程，这对于同一机器通信足够高效。远程服务器使用 HTTP + Server Sent Events (HTTP+SSE)，它保持有状态连接，或者使用 Streamable HTTP，它允许有状态和无状态连接。

对于 **stateless** 部署：无状态 MCP 服务器实现 Streamable-HTTP 规范的子集，返回 `application/json` 响应。它们不在请求之间维护会话状态，非常适合微服务架构和云原生部署。

---

### 8. JSON 序列化

SDK 使用 **Jackson** 进行 JSON 序列化和反序列化。Jackson 在 Java 生态系统中广泛采用，提供强大的性能和成熟的注解模型。它作为默认实现 (`mcp-json-jackson3`) 提供，但可以通过 SDK 的抽象层插入替代方案。

---

### 9. Maven 依赖设置

核心 `io.modelcontextprotocol.sdk:mcp` 模块提供默认 STDIO、SSE 和 Streamable HTTP 客户端和服务器传输实现，无需外部 Web 框架。

```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp</artifactId>
</dependency>
```

对于 Spring 集成：Spring 特定传输作为可选依赖提供，包括 `mcp-spring-webflux` 用于基于 WebFlux 的响应式传输，以及 `mcp-spring-webmvc` 用于基于 Servlet 的 HTTP 传输。

---

### 10. Spring AI 集成

Spring AI 项目通过为 Spring Boot 应用程序集成添加开发者生产力增强来扩展 MCP Java SDK。使用 Spring Boot starters，开发者可以使用 Spring 的依赖注入和配置管理快速配置 MCP 客户端和服务器，从而更容易将 AI 驱动的工作流集成到应用程序中。

可用的 Spring starters 包括：

- `spring-ai-mcp-client-spring-boot-starter` — 核心客户端 (STDIO + HTTP SSE)
- `spring-ai-mcp-client-webflux-spring-boot-starter` — 响应式 WebFlux 客户端
- `spring-ai-mcp-server-spring-boot-starter` — 核心服务器 (STDIO)
- `spring-ai-mcp-server-webmvc-spring-boot-starter` — 基于 Servlet 的服务器
- `spring-ai-mcp-server-webflux-spring-boot-starter` — 响应式服务器

SDK 还支持 MCP Annotations（基于注解的方法处理，用于 MCP 服务器和客户端）和 MCP Security（基于 OAuth 2.0 和 API 密钥的安全支持）。

---

### 11. 连接生命周期

生命周期阶段包括：**Initialization**（协商和协议版本约定）、**Operation**（通信）和 **Shutdown**（优雅终止连接）。客户端首先发送“initialize”请求，包括支持的协议版本、客户端能力和实现信息。然后服务器发送响应，包括其自身能力和信息。

---

### 12. 错误处理

SDK 通过 `McpError` 类提供全面的错误处理，涵盖协议兼容性、传输通信、JSON-RPC 消息、工具执行、资源管理、提示处理、超时和连接问题。

---

### 总结表格

| 特性 | 详情 |
|---|---|
| **推出时间** | December 2024 (experimental)，GA in 2025 |
| **维护方** | Anthropic + Spring AI 团队 |
| **API 模型** | Sync (`McpSyncClient/Server`) + Async (`McpAsyncClient/Server`) |
| **传输** | STDIO, SSE, Streamable HTTP |
| **响应式引擎** | Project Reactor |
| **JSON 库** | Jackson 2 / Jackson 3 (pluggable) |
| **服务器原语** | Tools, Resources, Prompts |
| **客户端原语** | Sampling, Elicitation, Logging |
| **Spring 支持** | Spring Boot Starters available |
| **许可证** | Apache 2.0 |

References:

- [Spring AI MCP Announcement (Dec 2024)](https://spring.io/blog/2024/12/11/spring-ai-mcp-announcement/)
- [MCP Java SDK Official Release](https://spring.io/blog/2025/02/14/mcp-java-sdk-released-2/)
- [MCP Java SDK GitHub](https://github.com/modelcontextprotocol/java-sdk)
- [MCP Java SDK Official Docs](https://modelcontextprotocol.io/sdk/java/mcp-overview)
- [Introduction to MCP Java SDK – Baeldung](https://www.baeldung.com/java-sdk-model-context-protocol)
- [Spring AI MCP Reference Docs](https://docs.spring.io/spring-ai-mcp/reference/mcp.html)
- [MCP Java SDK Releases](https://github.com/modelcontextprotocol/java-sdk/releases)