---
audio: false
date: 2025-09-06
generated: true
image: false
lang: en
layout: post
title: Optimal Model Selection for Cost and Performance
translated: false
type: note
---

Looking at your Claude Code configuration, you want to optimize for both cost and performance. Here are some recommendations for choosing "cheap and powerful" models in your router setup:

## Best Cost/Performance Models from your list

**For most tasks (default):**

- `deepseek/deepseek-chat-v3.1` - Excellent performance at very low cost
- `deepseek/deepseek-r1` - Great reasoning capabilities, still cost-effective

**For background tasks:**

- `deepseek/deepseek-chat-v3.1` - Already a good choice
- `google/gemini-2.5-flash` - Fast and inexpensive

**For thinking/reasoning:**

- `deepseek/deepseek-r1` - Specifically designed for reasoning tasks
- `z-ai/glm-4.5` - Your current choice is decent

**Updated Router suggestion:**

```json
"Router": {
  "default": "openrouter,deepseek/deepseek-chat-v3.1",
  "background": "openrouter,google/gemini-2.5-flash",
  "think": "openrouter,deepseek/deepseek-r1",
  "longContext": "openrouter,moonshotai/kimi-k2",
  "webSearch": "openrouter,google/gemini-2.5-flash"
}
```

## Key considerations

- **DeepSeek models** offer the best price/performance ratio currently
- **Gemini 2.5 Flash** is very fast and cheap for simpler tasks
- Keep **Kimi** for long context since it handles 200k+ tokens well
- **Gemini 2.5 Pro** if you need more capability than Flash

You can check current pricing on OpenRouter's website to compare exact costs, but DeepSeek models are typically 10-20x cheaper than GPT-4 level models while offering competitive performance.
