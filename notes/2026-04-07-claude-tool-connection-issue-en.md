---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Tool Connection Issue
translated: false
type: note
---

Question:
Why does `/home/lzw/projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` work with OpenClaw (AI agent), but I get the “Connect your tools to Claude… This isn't working right now” issue?

Answer:

This is **not a model problem**. Your local GGUF model works in OpenClaw, but the error comes from **Claude tool integration**, not from `llama.cpp` or the model itself.

You are seeing:

> “Connect your tools to Claude… This isn't working right now. Try again later.”

This typically happens when **OpenClaw switches to a Claude-based agent mode** but **tool server / MCP bridge is not connected**.

So:

* ✅ Local model works (`DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf`)
* ❌ Claude tool mode fails (tool connection missing)
* ❌ Not related to context window
* ❌ Not related to GGUF
* ❌ Not related to llama.cpp

---

## Why OpenClaw Works With Local Model

When you run:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

OpenClaw:

* uses **local llama.cpp server**
* no cloud tools
* no Claude integration
* no MCP required

So everything works.

---

## Why Claude Mode Fails

When OpenClaw switches to **Claude tool mode**, it expects:

* MCP tool server running
* tool registry connected
* Claude API session alive

If one fails → you see:

```
Connect your tools to Claude
This isn't working right now
```

This is a **tool connection error**, not inference.

---

## Most Common Causes

### 1. Claude tool bridge not started

You need something like:

```
openclaw tools start
```

or

```
openclaw mcp start
```

(depending on your version)

---

### 2. Using Claude agent accidentally

You may be in:

```
Agent: Claude
```

instead of:

```
Agent: Local
```

Switch back to local:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

---

### 3. Tool provider offline

Claude tools use:

* filesystem
* bash
* git
* browser

If OpenClaw can't attach them → error.

---

## Why OpenClaw Still Runs Local Model

Because OpenClaw architecture:

```
Agent layer
   ↓
Model layer (local gguf)
   ↓
Tool layer (optional)
```

Your model runs fine
But **Claude agent requires tools**
So it fails before inference

---

## Quick Fix

Use pure local agent:

```
/agent local
```

then:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

This bypasses Claude tools entirely.

---

## Another Fix

Restart OpenClaw fully:

```
pkill -f openclaw
openclaw dev
```

Then load model again.

---

## Summary

Your model works ✅
Claude tools not connected ❌
OpenClaw local mode unaffected ✅

So the issue is **Claude tool integration**, not:

* not GGUF
* not VRAM
* not context
* not llama.cpp

This is expected behavior.

If you paste:

* `openclaw logs --follow`
* or your `/agent` output

I can pinpoint exactly which layer failed.
