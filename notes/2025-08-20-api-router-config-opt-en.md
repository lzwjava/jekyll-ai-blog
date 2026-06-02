---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing API Router Model Configurations
translated: false
type: note
---

The configuration you've shared appears to be a routing setup for directing different types of tasks or queries to specific language models via an API router (possibly OpenRouter). Here's how you can optimize each field for best performance and cost-efficiency:

---

### ✅ **Recommended Configuration & Best Practices**

```json
"Router": {
  "default": "openrouter,qwen/qwen3-coder",
  // Good choice: Qwen3-Coder excels in general coding and reasoning.
  // Use for standard code generation, explanations, or mixed tasks.

  "background": "openrouter,qwen/qwen3-coder",
  // Also reasonable. If "background" means low-priority or async tasks,
  // consider a cheaper/faster model like:
  // → "openrouter:mistralai/mistral-tiny" or "google/gemini-2.5-flash-lite"

  "think": "openrouter,kimi/kimi-k2",
  // Kimi K2 is strong in long-context reasoning and Chinese/English logic.
  // However, if "think" implies step-by-step reasoning or chain-of-thought,
  // consider models better known for reasoning:
  // → "openrouter/deepseek/deepseek-chat" or "anthropic/claude-3-haiku"
  // ✅ Keep Kimi if it performs well in your tests.

  "longContext": "openrouter,google/gemini-2.5-flash",
  // ⚠️ Caution: Gemini Flash supports up to 1M tokens, but context handling may vary.
  // Better options for long-context:
  // → "openrouter:anthropic/claude-3-7-sonnet-20250129" (200K context)
  // → "openrouter:meta-llama/llama-3.1-405b-instruct" (128K)
  // → "openrouter:01-ai/yi-large" (200K+)
  // Gemini Flash is fast and cheap, but verify its accuracy on long inputs.

  "longContextThreshold": 60000,
  // This sets when to switch to the longContext model.
  // 60K tokens is reasonable for most APIs.
  // Ensure your prompt parser accurately estimates token count.
  // ✅ Keep 60000 if you're using models with 100K+ context.

  "webSearch": "openrouter,mistralai/mistral-medium-3.1"
  // Excellent choice: Mistral Medium balances quality and cost for search-based queries.
  // It handles real-time info well when combined with search results.
  // ✅ Keep this unless you need multilingual or domain-specific search.
}
```

---

### 🔍 **Suggestions by Use Case**

| Purpose        | Recommended Model |
|---------------|-------------------|
| **Default**     | `qwen/qwen3-coder` ✅ (great for code + general tasks) |
| **Background / Low Priority** | `google/gemini-2.5-flash-lite` or `mistralai/mistral-tiny` (cheaper, faster) |
| **Reasoning / Think** | `deepseek-chat` or `claude-3-haiku` (better reasoning benchmarks) |
| **Long Context (>64K)** | `anthropic/claude-3-7-sonnet` or `yi-large` (more reliable than Gemini) |
| **Web Search + Summarization** | `mistral-medium-3.1` ✅ (excellent fit) |

---

### 🛠️ Tips for Optimization

1. **Token Estimation**: Use accurate token counting (e.g., tiktoken or equivalent) to trigger `longContext` correctly.
2. **Fallbacks**: Consider adding fallback models in case of API errors or rate limits.
3. **Caching**: Cache results from `webSearch` and `longContext` to save cost.
4. **Latency Monitoring**: Track response times per model to adjust routing dynamically.
5. **Cost Tracking**: Monitor per-query cost, especially for large-context or premium models.

---

### ✅ Final Recommendation

Your config is solid, especially for coding and search workloads. Minor improvements:

```json
"Router": {
  "default": "openrouter,qwen/qwen3-coder",
  "background": "openrouter,google/gemini-2.5-flash-lite",
  "think": "openrouter,deepseek/deepseek-chat",
  "longContext": "openrouter,anthropic/claude-3-7-sonnet-20250129",
  "longContextThreshold": 60000,
  "webSearch": "openrouter,mistralai/mistral-medium-3.1"
}
```

Let me know your primary use case (e.g., coding, research, chatbots), and I can tailor it further!
