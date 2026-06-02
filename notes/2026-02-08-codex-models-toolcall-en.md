---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Best Codex Models for Tool Calling
translated: false
type: note
---

I'll search for information about OpenAI's Codex and which models are best for tool calling.Based on the search results, here are the best OpenAI Codex models for tool calling:

## Top Models for Tool Calling in Codex

**GPT-5.2-Codex** is specifically optimized for reliable tool calling with improved factuality and better long-context understanding. It provides reliable tool calling capabilities that make it a more dependable partner for long running coding tasks while remaining token-efficient in its reasoning.

**GPT-5.3-Codex** is the latest and most capable agentic coding model for tool-using workflows. It combines frontier coding performance with stronger reasoning capabilities and runs 25% faster for Codex users.

**GPT-5-Codex-Mini** is a smaller, more cost-effective option that provides approximately 4x more usage as part of your ChatGPT subscription while maintaining good tool-calling capabilities.

## Custom Provider Configuration

Codex works best with the recommended models, but you can also point Codex at any model and provider that supports either the Chat Completions or Responses APIs to fit your specific use case in your config.toml configuration file.

For your custom provider setup in config.toml, you'll want to specify a model that supports the **Responses API** (preferred) or Chat Completions API, with priority on models designed for agentic work with strong tool-calling capabilities.

Would you like help configuring a specific model in your config.toml file?
