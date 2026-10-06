---
audio: false
generated: true
image: false
lang: en
layout: post
title: Everything working end to end
translated: false
type: note
---

Everything is working end-to-end now. 🎉

## ✅ Final result

| Item | Status |
|---|---|
| llama.cpp + CUDA (sm_52/MMQ) built for M40 | ✅ `~/projects/llama.cpp` |
| Qwen2.5-14B-Instruct Q5_K_M (10.5GB) downloaded | ✅ `~/projects/models/` |
| llama-server running (detached, PID 2785) | ✅ port 8080 |
| Auto-suspend permanently disabled | ✅ systemd masked + GNOME off |
| API test | ✅ `"Hi there!"` |

## 📊 Performance (real measurement)

| Metric | Speed |
|---|---|
| Prompt processing | **38.5 tok/s** |
| Generation (14B Q5_K_M) | **13.6 tok/s** |

## 🌐 How to use it from any machine on your network

**Web chat UI** (browser):
```
http://192.168.1.137:8080
```

**OpenAI-compatible API** (works with any tool expecting OpenAI):
```bash
curl http://192.168.1.137:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'
```
Endpoint: `http://192.168.1.137:8080/v1` · model name = the GGUF path

**Terminal chat** (on the machine itself):
```bash
~/projects/run-chat.sh
```

## 📁 Project layout (as requested, in `~/projects/`)
```
~/projects/
├── llama.cpp/          # source + build (binaries in build/bin/)
├── models/             # GGUF model shards
├── run-chat.sh         # interactive CLI chat
└── run-server.sh       # API + web server
```

## 🔜 Optional next steps (say the word)

1. **Auto-start on boot** — I can create a `systemd` service so llama-server starts automatically after every reboot/restart.
2. **Bigger model** — with 24GB you can run Qwen2.5-**32B**-Q4 (~20GB) at ~2–4 tok/s, or **Mixtral 8x7B Q3**.
3. **whisper.cpp** — add fast speech-to-text on the same GPU.
4. **Power-limit the M40** (`sudo nvidia-smi -pl 150`) — less stress on the old PSU, negligible speed loss.

⚠️ Note: the server currently has **no API key** and allows CORS from anywhere — fine on your LAN, but don't expose port 8080 to the internet.

Shall I set up the **systemd auto-start service** so it's always available?
