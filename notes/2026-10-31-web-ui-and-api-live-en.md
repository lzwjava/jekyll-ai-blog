---
audio: false
generated: true
image: false
lang: en
layout: post
title: Web UI and API Live
translated: false
type: note
---

Web UI is live and the API responds. Here's how to access it:

## Access

| Where | URL |
|-------|-----|
| **This machine** | <http://localhost:8080> |
| **LAN (other devices)** | **<http://192.168.1.209:8080>** |

Just open it in a browser — llama.cpp ships a built-in chat UI at the root path. No extra frontend needed.

**API endpoints** (OpenAI-compatible):

- `POST http://192.168.1.209:8080/v1/chat/completions`
- `POST http://192.168.1.209:8080/v1/completions`
- `GET  http://192.168.1.209:8080/v1/models`

## Current status

```
model     : Qwen2.5-7B-Instruct-Q4_K_M.gguf
backend   : ROCm / gfx900 (WX 9100), ngl=99
ctx       : 32768  (4 slots, unified KV)
listening : http://0.0.0.0:8080   (/health -> ok)
```

Verified with a live chat completion → `Hello there!`

## Manage the server

```bash
# log
tail -f ~/projects/llama.cpp/server.log

# stop
pkill -f llama-server

# start again (detached, survives logout)
cd ~/projects/llama.cpp
setsid nohup ./build/bin/llama-server \
  -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 --host 0.0.0.0 --port 8080 --ctx-size 32768 \
  > server.log 2>&1 < /dev/null &
```

## ⚠️ Security note

The log warns: **no API key is set and CORS allows all origins**. Since it's bound to `0.0.0.0`, anyone on your LAN can use it. To lock it down, add `--api-key YOUR_SECRET` to the start command (clients then send `Authorization: Bearer YOUR_SECRET`). If you only need local access, use `--host 127.0.0.1` instead.
