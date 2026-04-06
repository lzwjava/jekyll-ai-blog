---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Context Window Fix
translated: false
type: note
---

Question: Why does OpenClaw show “Agent failed before reply: Model context window too small (8192 tokens). Minimum is 16000” and how to fix it?

Answer:

This error means the **model you configured only supports an 8K context window**, but OpenClaw’s agent **requires at least 16K tokens** to run. So the agent stops before replying.

### Why this happens

* Your current model: **8,192 tokens max**
* OpenClaw requirement: **≥ 16,000 tokens**
* Result: agent refuses to start

This usually happens when using:

* small local GGUF models
* older Qwen / LLaMA configs
* wrong OpenRouter model variant
* llama.cpp server started with low context

---

# Fix (choose one)

## Fix 1 — Switch to a larger context model (recommended)

Use a model with **16K / 32K / 128K** context.

Examples:

* DeepSeek-R1 (32K+)
* Qwen2.5-32B (32K)
* Mistral-Large (32K)
* Claude / GPT via OpenRouter (100K+)

For example (OpenClaw slash command):

```
/model openrouter/deepseek/deepseek-r1
```

or

```
/model openrouter/qwen/qwen-2.5-32b-instruct
```

---

## Fix 2 — Increase llama.cpp context (local model)

If you're running local server:

Start with larger context:

```
--ctx-size 16384
```

or better:

```
--ctx-size 32768
```

Example:

```
llama-server \
  -m DeepSeek-R1.gguf \
  --ctx-size 32768
```

---

## Fix 3 — change OpenClaw agent requirement (not recommended)

You could lower requirement, but agent quality drops.

OpenClaw config:

```
agent:
  min_context: 8192
```

But this often breaks:

* planning
* tool calling
* long code edits

So better upgrade model.

---

## Quick diagnosis

Run:

```
openclaw model
```

or

```
openclaw doctor
```

You’ll likely see:

```
context: 8192
required: 16000
```

---

## Best practical choice

Use:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

because it supports **32K context** and works well with OpenClaw.

---

In short:

* error is normal
* your model too small
* switch to 16K+ model
* or increase ctx-size

That will immediately fix it.