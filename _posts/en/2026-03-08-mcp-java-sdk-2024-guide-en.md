---
audio: false
generated: true
image: false
lang: en
layout: post
title: MCP Java SDK Overview 2024 Guide
translated: false
type: note
---

Question: What is a comprehensive introduction to the MCP Java SDK that was introduced in December 2024?

Answer:

## MCP Java SDK — Comprehensive Introduction

---

### 1. What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It provides a standardized way to connect AI models to different data sources and tools, making integration seamless and consistent, and helps you build agents and complex workflows on top of LLMs.

---

### 2. Origin and History

Spring AI MCP was introduced on December 11, 2024, as a robust Java SDK implementation of the Model Context Protocol — a new addition to the Spring AI ecosystem bringing standardized AI model integration capabilities to the Java platform.

What began as an experimental project was later moved into the official MCP Java SDK. This SDK is the latest language binding of the protocol, alongside the Python, TypeScript, and Kotlin SDKs, available at modelcontextprotocol.io.

The project has since reached a 1.0.0 GA release, is compliant with the 2025-06-18 MCP specification, and supports protocol version negotiation across multiple versions including 2024-11-05, 2025-03-26, and 2025-06-18.

---

### 3. Core Architecture

MCP defines communication through two conceptual layers: the **Data Layer**, which defines the protocol for client-server communication and lifecycle management, and the **Transport Layer**, which defines the communication channels and mechanisms used by the client and server.

The Java SDK maps these into three main architectural layers:

- **Client/Server Layer** (`McpClient` / `McpServer`): Both use `McpSession` for sync/async operations, with `McpClient` handling client-side protocol operations and `McpServer` managing server-side protocol operations.
- **Session Layer** (`McpSession`): Manages communication patterns and state using `DefaultMcpSession`.
- **Transport Layer** (`McpTransport`): Handles JSON-RPC message serialization/deserialization via HTTP Streamable-HTTP and SSE transports, with dedicated modules for Java HttpClient, Spring WebFlux, and Spring WebMVC.

The overall system follows a **host-client-server** topology: the **Host** is responsible for managing one or more MCP clients, enforcing security policies, and coordinating the interaction between the LLM and the available tools. The **Client** establishes and maintains a dedicated, stateful, one-to-one connection with a single MCP server. The **Server** provides context and capabilities to an MCP client.

---

### 4. Key Features

Key features of the MCP Java SDK include:

- Supports both synchronous and asynchronous MCP communication
- Enables protocol version compatibility negotiation for smooth interoperability
- Discover, register, and execute tools dynamically
- Receive real-time list change notifications for tools and resources
- Manage resources using URI templates for structured access and subscriptions
- Retrieve and manage prompts to customize AI model behavior
- Supports sampling strategies to fine-tune AI interactions
- STDIO-based transport for direct process communication
- Java HttpClient-based SSE client transport for HTTP-based streaming
- Servlet-based SSE server transport for HTTP streaming in traditional server environments
- Spring-based transports for seamless Spring Boot integration

---

### 5. Dual API Models: Sync vs Async

The SDK provides first-class support for both blocking (`McpSyncClient` / `McpSyncServer`) and reactive (`McpAsyncClient` / `McpAsyncServer`) programming models.

MCP builds on JSON-RPC's asynchronous nature and defines a bidirectional protocol, explicitly supporting asynchronous and streaming interactions. The SDK uses **Project Reactor** as its implementation of the Reactive Streams specification. Reactor is mature, widely adopted, provides rich operators, and integrates well with observability through context propagation.

---

### 6. MCP Primitives (Building Blocks)

Primitives are fundamental building blocks of MCP. They define the type of contextual information and range of actions that can be performed. Both the server and the client offer primitives.

#### Server Primitives

Server primitives include **Tools**, **Resources**, and **Prompts**. Tools are executable functions that AI applications can use to perform actions, such as querying a database or file operations. Resources are data sources that provide contextual information to clients, like database schemas or file contents. Prompts are reusable templates that help with interactions with the language models.

#### Client Primitives

Client primitives allow McpServer authors to build richer interactions and include **Sampling**, **Elicitation**, and **Logging**. Sampling allows servers to request language model completions from clients when they don't want to include the model SDK on the server itself. Elicitation gives servers a way to request additional information from the user or confirm any action.

---

### 7. Transport Mechanisms

Local servers use standard input and output (STDIO) for local processes, which is efficient enough for same-machine communication. Remote servers use either HTTP + Server Sent Events (HTTP+SSE), which keeps a stateful connection, or Streamable HTTP, which allows both stateful and stateless connections.

For **stateless** deployments: stateless MCP servers implement a subset of the Streamable-HTTP specification that returns `application/json` responses. They do not maintain session state between requests and are ideal for microservices architectures and cloud-native deployments.

---

### 8. JSON Serialization

The SDK uses **Jackson** for JSON serialization and deserialization. Jackson is widely adopted across the Java ecosystem, provides strong performance and a mature annotation model. It is shipped as the default implementation (`mcp-json-jackson3`), but alternatives can be plugged in via the SDK's abstraction layer.

---

### 9. Maven Dependency Setup

The core `io.modelcontextprotocol.sdk:mcp` module provides default STDIO, SSE, and Streamable HTTP client and server transport implementations without requiring external web frameworks.

```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp</artifactId>
</dependency>
```

For Spring integration: Spring-specific transports are available as optional dependencies including `mcp-spring-webflux` for WebFlux-based reactive transport and `mcp-spring-webmvc` for servlet-based HTTP transport.

---

### 10. Spring AI Integration

The Spring AI project extends the MCP Java SDK by adding developer productivity enhancements for integration with Spring Boot applications. With Spring Boot starters, developers can quickly configure MCP clients and servers using Spring's dependency injection and configuration management, making it easier to integrate AI-driven workflows into their applications.

Available Spring starters include:

- `spring-ai-mcp-client-spring-boot-starter` — Core client (STDIO + HTTP SSE)
- `spring-ai-mcp-client-webflux-spring-boot-starter` — Reactive WebFlux client
- `spring-ai-mcp-server-spring-boot-starter` — Core server (STDIO)
- `spring-ai-mcp-server-webmvc-spring-boot-starter` — Servlet-based server
- `spring-ai-mcp-server-webflux-spring-boot-starter` — Reactive server

The SDK also supports MCP Annotations (annotation-based method handling for MCP servers and clients) and MCP Security (OAuth 2.0 and API key-based security support).

---

### 11. Connection Lifecycle

The lifecycle phases are: **Initialization** (negotiation and protocol version agreement), **Operation** (communication), and **Shutdown** (gracefully terminate the connection). The client first sends an "initialize" request including the protocol version supported, client capabilities, and implementation info. The server then sends back a response including its own capabilities and information.

---

### 12. Error Handling

The SDK provides comprehensive error handling through the `McpError` class, covering protocol compatibility, transport communication, JSON-RPC messaging, tool execution, resource management, prompt handling, timeouts, and connection issues.

---

### Summary Table

| Feature | Details |
| --- | --- |
| **Introduced** | December 2024 (experimental), GA in 2025 |
| **Maintained by** | Anthropic + Spring AI team |
| **API Models** | Sync (`McpSyncClient/Server`) + Async (`McpAsyncClient/Server`) |
| **Transport** | STDIO, SSE, Streamable HTTP |
| **Reactive Engine** | Project Reactor |
| **JSON Library** | Jackson 2 / Jackson 3 (pluggable) |
| **Server Primitives** | Tools, Resources, Prompts |
| **Client Primitives** | Sampling, Elicitation, Logging |
| **Spring Support** | Spring Boot Starters available |
| **License** | Apache 2.0 |

References:

- [Spring AI MCP Announcement (Dec 2024)](https://spring.io/blog/2024/12/11/spring-ai-mcp-announcement/)
- [MCP Java SDK Official Release](https://spring.io/blog/2025/02/14/mcp-java-sdk-released-2/)
- [MCP Java SDK GitHub](https://github.com/modelcontextprotocol/java-sdk)
- [MCP Java SDK Official Docs](https://modelcontextprotocol.io/sdk/java/mcp-overview)
- [Introduction to MCP Java SDK – Baeldung](https://www.baeldung.com/java-sdk-model-context-protocol)
- [Spring AI MCP Reference Docs](https://docs.spring.io/spring-ai-mcp/reference/mcp.html)
- [MCP Java SDK Releases](https://github.com/modelcontextprotocol/java-sdk/releases)
