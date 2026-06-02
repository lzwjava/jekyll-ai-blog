---
audio: false
generated: true
image: false
lang: en
layout: post
title: Options to Update llama.cpp
translated: false
type: note
---

October 2025 — that's way too old. Qwen 3.5 came out later. The git fetch is failing because GitHub is slow from this server.

Boss, the core problem is GitHub access from this server is extremely slow (~30 KB/s). Two options:

1. **You update llama.cpp from your laptop** — clone/pull the latest, build, and the `qwen35` arch will be supported
2. **You SCP the Ollama binary** from your laptop as I suggested earlier

Either way, the model file is already downloaded and ready — we just need a newer engine that understands the `qwen35` architecture. Which route do you prefer?
