---
audio: false
generated: true
image: false
lang: en
layout: post
title: LibreChat Architecture and Tech Stack
translated: false
type: note
---

I'll search for information about LibreChat's architecture to give you a comprehensive answer.Let me search for more specific information about the frontend technologies used.Now I have comprehensive information about LibreChat's architecture. Let me compile this into a well-structured answer.

---

**Question:** What is a comprehensive introduction to LibreChat's architecture? How is it made, what technologies does it use (TypeScript, React, or others)?

**Answer:**

## LibreChat Architecture Overview

LibreChat is an open-source, self-hostable AI chat platform that unifies multiple AI models (OpenAI, Claude, Gemini, Azure, AWS Bedrock, Ollama) into a single interface. It follows a modern monorepo architecture with clear separation between frontend, backend, and shared packages.

### Technology Stack

#### **Frontend**

- React for UI components combined with Recoil for state management
- TypeScript for type-safe code
- React Query (@tanstack/react-query) for API interactions and server state management
- React Hook Form for form validation and submission
- CSS custom properties (CSS variables) for theme-aware styling across light, dark, and custom themes, with Tailwind CSS for utility-based styling

#### **Backend**

- TypeScript for all new backend code in /packages/api
- Express.js for the API server running on port 3080
- Passport.js for authentication strategy configuration

#### **Database & Storage**

- MongoDB as the primary data store for user data, conversations, messages, transactions, and application state
- Redis for caching, session storage, and Resumable Streams functionality using Redis Streams and Pub/Sub
- MeiliSearch for search index updates
- Multiple file storage backends: Local filesystem, Firebase, S3, and Azure Blob

### Monorepo Structure

LibreChat uses a monorepo workspace structure with package boundaries where all new backend code must be TypeScript in /packages/api, database-specific shared logic belongs in /packages/data-schemas, and frontend/backend shared API logic (endpoints, types, data-service) belongs in /packages/data-provider.

The organized structure includes:

- **packages/data-provider**: Built with TypeScript + Axios + React Query, exports React hooks for all API operations
- **packages/data-schemas**: Database schemas and types built with TypeScript and Mongoose
- **packages/api**: MCP services and core APIs built with TypeScript and MCP SDK
- **client**: Reusable React UI components

### Message Flow Architecture

The message flow follows this sequence: User types in TextInput component → Component updates Recoil submission state → React Query mutation hook triggered → Axios POST to /api/messages → Express route handler receives request → Passport.js validates JWT token → Request validated and sanitized → AI client selected based on endpoint.

### Configuration System

LibreChat uses a hierarchical configuration system with three layers where higher layers override lower ones, with librechat.yaml configuration loaded at startup via CONFIG_PATH environment variable. The multi-layer configuration system uses Zod validation with key schemas including endpointSchema for custom endpoint definitions, azureEndpointSchema for Azure OpenAI configurations, and agentsEndpointSchema for agent capabilities.

### Advanced Features Architecture

#### **Agents System**

The Agents system enables agentic workflows with tool use, including toggleable capabilities like execute_code, file_search, actions, tools, artifacts, context, ocr, chain, and web_search, with a recursionLimit parameter (default: 25) to prevent infinite loops.

#### **AI Provider Integration**

LibreChat uses an abstract client pattern to support multiple AI providers through a unified interface. Each message is routed to the selected model provider (OpenAI, Azure, Anthropic) via a unified API interface, with routing logic defined in the api directory where endpoints are configured based on user settings and environment variables.

#### **Streaming & Resilience**

LibreChat features a resilient streaming architecture that ensures content is never lost through network interruptions by automatically using hash-tagged keys to ensure multi-key operations stay within the same cluster slot, with responses automatically resuming when connectivity returns.

#### **File Storage**

LibreChat implements a flexible, type-aware storage routing system with multiple provider backends and fallback mechanisms supporting local filesystem storage at uploads/ directory, Firebase, S3, and Azure Blob.

### Code Standards

Development follows clean code principles with TypeScript type definitions using interfaces, form validation via React Hook Form, localization through useLocalize() hook, and comprehensive testing using Jest for unit tests, Supertest for API endpoints, and Playwright for end-to-end tests.

### Infrastructure Components

The initialization sequence loads .env configuration, connects to MongoDB with index synchronization and database seeding, loads librechat.yaml app configuration, initializes file storage (S3/Firebase/Local), sets up Express middleware stack, initializes Passport.js auth strategies, initializes MCP servers, mounts API routes, and starts the server on port 3080.

---

**References:**

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
