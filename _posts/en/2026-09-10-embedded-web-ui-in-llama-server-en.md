---
audio: false
generated: true
image: false
lang: en
layout: post
title: Embedded web UI in llama-server
translated: false
type: note
---

There's no separate `llama-web` binary in this build (b10894) - the web UI is now embedded directly in `llama-server`. So running the server *is* running the web UI.

**It's up now:** http://127.0.0.1:8080

```
model      : models/Qwen3-8B-abliterated-q4_k_m.gguf (Q4_K_M)
GPU        : 5896 MiB VRAM in use by llama-server (full offload, -ngl 99)
context    : 8192 (4 slots)
health     : {"status":"ok"}
web ui     : HTTP 200 (embedded UI served from /)
```

Verified both the API and the UI:
- `POST /v1/chat/completions` -> `{"content":"hi"}` correct
- `GET /` -> HTTP 200, serves the Svelte bundle

Don't panic if `curl http://127.0.0.1:8080/` alone returns **415** - that's expected. The UI is gzip-only; a normal browser always sends `Accept-Encoding: gzip`, so it loads fine. `curl --compressed` works too.

Manage it:
```bash
# logs
tail -f /tmp/llama-server.log
# stop
kill 3981052
# restart
cd /mnt/data/llama.cpp && ./build/bin/llama-server -m models/Qwen3-8B-abliterated-q4_k_m.gguf -ngl 99 -c 8192 --host 127.0.0.1 --port 8080
```

To reach it from another machine, bind `--host 0.0.0.0` (note: the log warns CORS is `*` with no API key - set `--api-key` before exposing it).