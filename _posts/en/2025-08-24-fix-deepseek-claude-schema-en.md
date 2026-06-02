---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix DeepSeek Claude Code Schema Mismatch
translated: false
type: note
---

Short answer: schema mismatch.

Claude Code “speaks Anthropic” (it expects Anthropic-Messages style tool use like `tool_use` / `tool_result` blocks). DeepSeek V3.1 on OpenRouter “speaks OpenAI” (it emits OpenAI-style `tool_calls` / function calling). If your Claude Code router forwards a task to DeepSeek V3.1 without transforming the request/response, the assistant’s tool-calling messages won’t parse—and you’ll see errors right when the agent tries to plan/run tools or stream output. ([Anthropic][1], [OpenRouter][2], [DeepSeek API Docs][3])

What to do (quick fixes):

1. Use the router’s transformers
   Enable the OpenRouter↔︎Anthropic request/response transformers in your Claude Code router so `tool_calls` ⇄ `tool_use` are mapped both ways. The popular community router supports this explicitly; check its “Request/Response Transformation” section and example configs. ([GitHub][4], [ClaudeLog][5])

2. Pick the correct model slug
   DeepSeek V3.1 has specific OpenRouter slugs (e.g., the V3.1/V3 family entries). A wrong or old slug can also throw errors during streaming or tool phases. Verify the exact model id shown on OpenRouter’s DeepSeek page and use that in your router mapping. ([OpenRouter][6])

3. Stay in “chat” (not “reasoner”) unless you’ve mapped its fields
   If you try a reasoning variant that streams special reasoning fields, your router must translate them—or Claude Code will choke. Prefer the standard chat model or disable extra “thinking” output until your transformer handles it. (DeepSeek’s docs emphasize OpenAI-style function calling; that’s what you should map.) ([DeepSeek API Docs][3])

4. Update to latest router build
   Recent community builds added compatibility tweaks for non-Anthropic providers; upgrade before testing. ([GitHub][4])

Why this only happens with V3.1
V3.1 added stronger agent/tool-calling by default. That increases the chance your Claude Code flow hits the un-translated tool messages, which is exactly where the schema mismatch bites. ([DeepSeek API Docs][7])

If you share the exact error text, I can point to the precise transformer snippet to drop into your config.

[1]: https://www.anthropic.com/engineering/claude-code-best-practices?utm_source=chatgpt.com "Claude Code: Best practices for agentic coding"
[2]: https://openrouter.ai/docs/features/tool-calling?utm_source=chatgpt.com "Tool & Function Calling"
[3]: https://api-docs.deepseek.com/guides/function_calling?utm_source=chatgpt.com "Function Calling"
[4]: https://github.com/musistudio/claude-code-router?utm_source=chatgpt.com "musistudio/claude-code-router"
[5]: https://claudelog.com/claude-code-mcps/claude-code-router/?utm_source=chatgpt.com "Claude Code Router"
[6]: https://openrouter.ai/models?q=deepseek&utm_source=chatgpt.com "Models: 'deepseek'"
[7]: https://api-docs.deepseek.com/news/news250821?utm_source=chatgpt.com "DeepSeek-V3.1 Release"
