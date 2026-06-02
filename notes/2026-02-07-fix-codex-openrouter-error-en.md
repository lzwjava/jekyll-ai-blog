---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Codex OpenRouter Model Name Error
translated: false
type: note
---

**Question:** Why does Codex CLI show error "anthropic/claude-4-sonnet is not a valid model ID" even after setting model_provider to openrouter, and how to fix it?

**Answer:**

The model name `anthropic/claude-4-sonnet` is **not** the correct format that OpenRouter expects in 2026.

OpenRouter uses a different naming convention than what you see in their website dropdown or what people casually write.

### Correct model names for OpenRouter (as of February 2026)

Here are the actual strings you should put in the `model = "..."` field when using OpenRouter provider:

| What people call it              | Correct OpenRouter model string                          | Notes                              |
|----------------------------------|----------------------------------------------------------|------------------------------------|
| Claude 4 Sonnet                  | `anthropic/claude-sonnet-4-20250514`                     | latest Claude 4 Sonnet             |
| Claude 3.7 Sonnet                | `anthropic/claude-3-7-sonnet-20250219`                   | very popular in early 2026         |
| Claude 3.5 Sonnet                | `anthropic/claude-3.5-sonnet`                            | still good & cheaper               |
| DeepSeek R1                      | `deepseek/deepseek-r1`                                   | best price/performance             |
| DeepSeek V3 0324                 | `deepseek/deepseek-v3-0324`                              | very strong coding model           |
| Qwen 2.5 Coder 32B               | `qwen/qwen2.5-coder-32b-instruct`                        | excellent coding & cheap           |
| Gemini 2.5 Pro                   | `google/gemini-2.5-pro-exp-03-25`                        | or check exact date suffix         |
| Gemini 2.5 Flash                 | `google/gemini-2.5-flash`                                | fast & cheap                       |
| Grok 3                           | `xai/grok-3`                                             | creative & good at code            |

### How to fix your config right now

Edit `~/.codex/config.toml` and change the model line to one of these valid names.

**Recommended quick fix – use a proven strong & cheap model:**

```toml
model = "deepseek/deepseek-r1"           # ← this almost always works
model_provider = "openrouter"

[model_providers.openrouter]
name     = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key  = "OPENROUTER_API_KEY"
# Optional but nice to have
headers = { "HTTP-Referer" = "https://github.com/lzwjava", "X-Title" = "Codex CLI" }
```

Then in terminal:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
codex
```

Or if you really want Claude-level quality (more expensive):

```toml
model = "anthropic/claude-sonnet-4-20250514"
# ... rest same as above
```

### Quick diagnostic commands

1. See what Codex actually loaded:

```bash
codex --debug config
```

2. List models Codex knows about (helps confirm provider):

```bash
codex --debug models
```

Most common mistakes that cause "not a valid model ID":

- Using website-friendly name instead of OpenRouter API name
- Typo in model string (especially dashes / dates)
- `model_provider` line missing or misspelled
- Wrong section header: must be exactly `[model_providers.openrouter]`
- Old cached config — sometimes delete `~/.codex/config.toml` and start over

After fixing the model name → restart `codex` (just quit and run again).

You should see no more 400 error and the model name should appear correctly in the header.

**References:**

- [https://openrouter.ai/models](https://openrouter.ai/models)
- [https://openrouter.ai/docs#models](https://openrouter.ai/docs#models)
- [https://github.com/openai/codex](https://github.com/openai/codex)
