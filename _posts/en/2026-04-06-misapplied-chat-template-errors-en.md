---
audio: false
generated: true
image: false
lang: en
layout: post
title: Misapplied Chat Template Causes Errors
translated: false
type: note
---

🦞 Here's the full breakdown:

## Root Cause

The GGUF model file `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` has a **Qwen3 chat template** baked into its metadata — because the base architecture is Qwen3 (note the name: "DeepSeek-R1-0528-**Qwen3**-8B"). But I started the server with `--chat-template deepseek`, which forced the **DeepSeek LLM** template format instead.

## What went wrong mechanically

Chat templates define how messages get serialized into the prompt string the model actually sees. For example.

When the DeepSeek template was applied to a Qwen3 model:

1. The prompt tokens dropped to **2** (essentially garbage) instead of **14** (properly formatted)
2. The model received an almost empty, nonsensical prompt
3. It fell back to whatever patterns it had memorized — which is why it started talking about "DeepSeek-Coder-7B-Instruct" completely unprompted
4. The web UI's input wasn't being formatted at all, so every message was garbled

## Why I made the mistake

The model name starts with "DeepSeek-R1" so I reflexively used `--chat-template deepseek`. But the architecture is **Qwen3** (a Qwen model fine-tuned by DeepSeek), not a native DeepSeek model. The name is misleading — the template should match the **architecture**, not the **fine-tuner**.

## The fix

Removed the `--chat-template deepseek` flag entirely. When no explicit template is specified, `llama-server` reads the chat template **embedded in the GGUF file itself** — which is the correct Qwen3 template. This is always the safest approach unless you have a reason to override.

## Lesson

- **Never hardcode `--chat-template`** unless you know for certain the model's architecture needs an override
- **GGUF files carry their own template metadata** — trust it by default
- **Model names ≠ architecture** — "DeepSeek-R1-Qwen3" is a Qwen3 model, not a DeepSeek model
- When something is wrong with a model's output, **check the prompt formatting first** — if `prompt_tokens` is suspiciously low (like 2), the template is almost certainly wrong
