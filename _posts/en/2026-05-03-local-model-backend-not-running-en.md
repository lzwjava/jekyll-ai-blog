---
audio: false
generated: true
image: false
lang: en
layout: post
title: Local Model Backend Not Running
translated: false
type: note
---

The error is clear: **the local model backend isn't running.**

The system tried to call `openai/gpt-oss-120b` at `http://localhost:1234/api/v1/chat` and got `Connection refused` — there's no model server listening on port 1234.

Per the README:
> A local OpenAI-compatible chat backend reachable at `http://localhost:1234/api/v1/chat`

You need to start a local inference server (e.g. **LM Studio**, **Ollama**, **llama.cpp server**, **vLLM**) that:
- Listens on `http://localhost:1234`
- Has the path `/api/v1/chat` (OpenAI-compatible)
- Serves the configured models (`qwen3.5-9b-mlx`, `openai/gpt-oss-120b`, etc.)

**Quick check** — do you have LM Studio or Ollama installed? If so, start it and load a model, then the session creation will work.