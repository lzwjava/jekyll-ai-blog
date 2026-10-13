---
audio: false
generated: true
image: false
lang: en
layout: post
title: No Official Supabase Conversation SDK
translated: false
type: note
---

**Question:** Does Supabase have a conversation SDK?

**Answer:** Supabase does not have an **official** first-party "Conversation SDK." However, there are two things worth knowing:

**1. Third-party `supabase_chat_sdk` (Flutter)**

There is a Flutter SDK called `supabase_chat_sdk` for building **offline-first chat applications** built on Supabase and PowerSync. It supports real-time messaging, channel management (direct, group, public), message read receipts, emoji reactions, file uploads, typing indicators, user presence, push notifications, and more. However, this is a **community/third-party package**, not an official Supabase product. You can install it via:

```yaml
dependencies:
  supabase_chat_sdk: ^0.1.0
```

**2. Using Supabase as a conversation persistence backend (the common pattern)**

Supabase itself doesn't offer a dedicated conversation SDK, but it is widely used as the **database layer** for storing AI/LLM conversation history. The typical pattern is:

- Store messages in a Supabase PostgreSQL table
- Use `@supabase/supabase-js` (or `supabase-py`) to read/write conversation history
- Pair it with an AI SDK like Vercel AI SDK, Anthropic SDK, or OpenAI SDK to manage the actual LLM calls

This approach means conversations are stored in a `messages` table, loaded back when a session resumes, and can be pruned intelligently when history grows large. The result is fully debuggable — you can look up any conversation ID directly in Supabase.

**In short:** If you need a dedicated "conversation SDK," Supabase isn't it — you'd combine Supabase (for storage/realtime) with an AI framework. If you're building a Flutter chat app, the community `supabase_chat_sdk` may be worth checking out.

**References:**
- [supabase_chat_sdk on pub.dev](https://pub.dev/documentation/supabase_chat_sdk/latest/)
- [Database-backed conversation history with Supabase and Claude](https://www.aicodex.to/articles/supabase-conversation-history)
- [Build an AI Agent with Vercel AI SDK and Supabase](https://gautamkhorana.com/blog/build-ai-agent-vercel-supabase/)