---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Compatibility Issues With Codex Tools
translated: false
type: note
---

I'll search for information about Kimi-k2.5 and Gemini Flash compatibility with Codex and their tool calling capabilities.Now let me search for Gemini Flash compatibility with Codex:## Yes, both have known issues with Codex:

### **Kimi-K2.5 Issues:**

Kimi K2.5 has broken tool calls when used via Kimi Code Subscription, with multiple GitHub issues reporting that the model is unable to use any tool calls despite attempted fixes.

However, the good news: Kimi K2.5 provides OpenAI/Anthropic-compatible APIs, and the Kimi API is designed to be compatible with chat-completions style workflows with strong agentic tool calling support.

**Cost consideration:** Kimi K2.5 generates extensive reasoning tokens and can execute up to 1,500 tool calls per task, but output tokens cost around $3.00 per million versus input costs of $0.50-$0.60, making it 10x more expensive per output token than some competitors.

### **Gemini Flash Issues:**

Multiple compatibility problems with Codex:

1. Gemini 3 Pro fails on multi-turn tool calls because the thought_signature is not preserved via OpenAI compatibility layer

2. Gemini 2.5 Flash multi-turn function calling fails with validation errors: "function response parts must equal function call parts" because assistant messages get 2 parts per tool call (thought signature + function call) while tool response messages only get 1 part

3. Gemini 2.5 models consistently fail to call tools for unknown reasons in some environments, while previous Gemini 2.0 executed tools normally

4. Gemini 1.5-flash's function calling doesn't work despite Gemini 1.5-pro working fine with identical configurations

## My Recommendation:

For your custom provider config.toml with cheaper options that **actually work reliably** in Codex:
- **GPT-4o Mini** (safest, proven)
- **GPT-4.1 Mini** (better performance)
- **o3-Mini** (cheapest reasoning)

Avoid Gemini Flash and Kimi-K2.5 for Codex tool calling until these compatibility issues are resolved.
