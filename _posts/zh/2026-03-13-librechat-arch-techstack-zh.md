---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LibreChat 架构与技术栈
translated: true
type: note
---

我会搜索有关 LibreChat 架构的信息，以给您一个全面的回答。让我搜索更多关于前端技术使用的具体信息。现在我已经获得了 LibreChat 架构的全面信息。让我将其编译成一个结构良好的回答。

---

**问题：** LibreChat 的架构全面介绍是什么？它是如何构建的，使用什么技术（TypeScript、React 或其他）？

**回答：**

## LibreChat 架构概述

LibreChat 是一个开源的、可自托管的 AI 聊天平台，它将多个 AI 模型（OpenAI、Claude、Gemini、Azure、AWS Bedrock、Ollama）统一到一个单一界面中。它采用现代 monorepo 架构，前端、后端和共享包之间有清晰的分离。

### 技术栈

#### **前端**
- 使用 React 构建 UI 组件，并结合 Recoil 进行状态管理
- TypeScript 用于类型安全的代码
- React Query（@tanstack/react-query）用于 API 交互和服务器状态管理
- React Hook Form 用于表单验证和提交
- CSS 自定义属性（CSS 变量）用于支持浅色、深色和自定义主题的主题感知样式，并使用 Tailwind CSS 进行基于实用程序的样式设计

#### **后端**
- /packages/api 中的所有新后端代码均使用 TypeScript
- Express.js 用于运行在 3080 端口的 API 服务器
- Passport.js 用于认证策略配置

#### **数据库与存储**
- MongoDB 作为主要数据存储，用于用户数据、对话、消息、事务和应用状态
- Redis 用于缓存、会话存储以及使用 Redis Streams 和 Pub/Sub 的 Resumable Streams 功能
- MeiliSearch 用于搜索索引更新
- 多种文件存储后端：本地文件系统、Firebase、S3 和 Azure Blob

### Monorepo 结构

LibreChat 使用 monorepo 工作区结构，具有包边界，其中所有新后端代码必须在 /packages/api 中使用 TypeScript，数据库特定的共享逻辑属于 /packages/data-schemas，前端/后端共享的 API 逻辑（端点、类型、data-service）属于 /packages/data-provider。

组织结构包括：
- **packages/data-provider**：使用 TypeScript + Axios + React Query 构建，导出所有 API 操作的 React hooks
- **packages/data-schemas**：使用 TypeScript 和 Mongoose 构建的数据库模式和类型
- **packages/api**：使用 TypeScript 和 MCP SDK 构建的 MCP 服务和核心 API
- **client**：可重用的 React UI 组件

### 消息流架构

消息流遵循以下序列：用户在 TextInput 组件中输入 → 组件更新 Recoil 提交状态 → React Query mutation hook 被触发 → Axios POST 到 /api/messages → Express 路由处理程序接收请求 → Passport.js 验证 JWT token → 请求被验证和清理 → 根据端点选择 AI 客户端。

### 配置系统

LibreChat 使用分层配置系统，具有三个层级，其中更高层覆盖较低层，通过 CONFIG_PATH 环境变量在启动时加载 librechat.yaml 配置。多层配置系统使用 Zod 验证，关键模式包括用于自定义端点定义的 endpointSchema、用于 Azure OpenAI 配置的 azureEndpointSchema，以及用于代理能力的 agentsEndpointSchema。

### 高级功能架构

#### **Agents 系统**
Agents 系统支持带有工具使用的代理工作流，包括可切换的功能，如 execute_code、file_search、actions、tools、artifacts、context、ocr、chain 和 web_search，并带有 recursionLimit 参数（默认：25）以防止无限循环。

#### **AI 提供商集成**
LibreChat 使用抽象客户端模式，通过统一界面支持多个 AI 提供商。每条消息通过统一 API 界面路由到选定的模型提供商（OpenAI、Azure、Anthropic），路由逻辑在 api 目录中定义，端点基于用户设置和环境变量配置。

#### **Streaming 与弹性**
LibreChat 具有弹性流式传输架构，通过自动使用带哈希标签的键确保多键操作保持在同一集群槽位，从而确保网络中断时内容不会丢失，当连接恢复时响应会自动恢复。

#### **文件存储**
LibreChat 实现了灵活的、类型感知的存储路由系统，支持多个提供商后端和回退机制，支持 uploads/ 目录的本地文件系统存储、Firebase、S3 和 Azure Blob。

### 代码标准

开发遵循干净代码原则，使用接口定义 TypeScript 类型，通过 React Hook Form 进行表单验证，通过 useLocalize() hook 进行本地化，并使用 Jest 进行单元测试、Supertest 进行 API 端点测试，以及 Playwright 进行端到端测试。

### 基础设施组件

初始化序列加载 .env 配置、连接 MongoDB 并进行索引同步和数据库种子数据加载、加载 librechat.yaml 应用配置、初始化文件存储（S3/Firebase/Local）、设置 Express 中间件栈、初始化 Passport.js 认证策略、初始化 MCP 服务器、挂载 API 路由，并在 3080 端口启动服务器。

---

**参考资料：**

- [LibreChat Project Architecture Documentation](https://www.librechat.ai/docs/development/architecture)
- [LibreChat Architecture - GitHub Gist](https://gist.github.com/ChakshuGautam/fca45e48a362b6057b5e67145b82a994)
- [Code Standards and Conventions](https://www.librechat.ai/docs/development/conventions)
- [DeepWiki - Architecture Overview](https://deepwiki.com/LibreChat-AI/librechat.ai/1.1-architecture-overview)
- [DeepWiki - Infrastructure Documentation](https://deepwiki.com/LibreChat-AI/librechat.ai/7-infrastructure)
- [DeepWiki - Frontend Components](https://deepwiki.com/danny-avila/LibreChat/6-frontend-components)
- [LibreChat Resumable Streams Documentation](https://www.librechat.ai/docs/features/resumable_streams)
- [DeepWiki - File Storage Strategies](https://deepwiki.com/LibreChat-AI/librechat.ai/7.1-file-storage-strategies-documentation)
- [Deep Dive into Open-Source AI Chat Architecture - Medium](https://medium.com/@sonaldhiman2605/gpt-in-librechat-a-deep-dive-into-open-source-ai-chat-architecture-d7e9e8d8fdbb)
- [DeepWiki - Main LibreChat Documentation](https://deepwiki.com/danny-avila/LibreChat)
