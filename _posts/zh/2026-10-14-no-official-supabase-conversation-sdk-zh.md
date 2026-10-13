---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无官方 Supabase 对话 SDK
translated: true
type: note
---

**Question:** Does Supabase have a conversation SDK?

**Answer:** Supabase 没有**官方的** first-party "Conversation SDK"。不过，有两件事值得了解：

**1. 第三方的 `supabase_chat_sdk`（Flutter）**

有一个名为 `supabase_chat_sdk` 的 Flutter SDK，用于构建基于 Supabase 和 PowerSync 的 **offline-first 聊天应用**。它支持 real-time messaging、channel management (direct, group, public)、message read receipts、emoji reactions、file uploads、typing indicators、user presence、push notifications 等功能。然而，这是一个 **community/third-party package**，并非 Supabase 官方产品。你可以通过以下方式安装：

```yaml
dependencies:
  supabase_chat_sdk: ^0.1.0
```

**2. 将 Supabase 用作 conversation persistence backend（常见模式）**

Supabase 本身并没有提供专门的 conversation SDK，但它被广泛用作存储 AI/LLM conversation history 的 **database layer**。典型模式是：

- 将消息存储在 Supabase PostgreSQL 表中
- 使用 `@supabase/supabase-js`（或 `supabase-py`）读写 conversation history
- 配合 Vercel AI SDK、Anthropic SDK 或 OpenAI SDK 等 AI SDK 来管理实际的 LLM 调用

这种方式意味着 conversations 存储在 `messages` 表中，当 session 恢复时重新加载，并在 history 变得过大时进行智能修剪。结果是完全可调试的——你可以直接在 Supabase 中查找任何 conversation ID。

**简而言之：** 如果你需要一个专门的 "conversation SDK"，Supabase 并不是——你需要将 Supabase（用于 storage/realtime）与 AI framework 结合。如果你正在构建 Flutter chat app，那么社区版 `supabase_chat_sdk` 值得一看。

**参考资料：**

- [supabase_chat_sdk on pub.dev](https://pub.dev/documentation/supabase_chat_sdk/latest/)
- [Database-backed conversation history with Supabase and Claude](https://www.aicodex.to/articles/supabase-conversation-history)
- [Build an AI Agent with Vercel AI SDK and Supabase](https://gautamkhorana.com/blog/build-ai-agent-vercel-supabase/)
