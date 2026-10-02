---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restarting llama-server process
translated: false
type: note
---

The `llama-server` process (PID 7946) you saw in `nvidia-smi` is **no longer running** — it has exited, so its port is already closed.

However, I see you have the `llama.cpp` project at `~/projects/llama.cpp/`. If you want to restart it:

```bash
cd ~/projects/llama.cpp
./llama-server -m /path/to/your/model.gguf --port 8080
```

By default, `llama-server` listens on **port 8080**. Once it's running:

- **Web UI**: `http://localhost:8080`
- **OpenAI-compatible API**: `http://localhost:8080/v1/chat/completions`
- **Check if it's listening**: `lsof -i :8080`

You can also specify a different port with `--port <number>`. Want me to create a quick startup script for it?
