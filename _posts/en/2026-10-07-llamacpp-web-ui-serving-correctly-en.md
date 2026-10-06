---
audio: false
generated: true
image: false
lang: en
layout: post
title: llama.cpp Web UI Serving Correctly
translated: false
type: note
---

🎉 **Fixed! The web UI is now serving correctly.** (The 415 was just curl not sending `Accept-Encoding: gzip` — real browsers always do, and the JSON error you saw earlier is replaced by the UI.)

`GET /` → **200** ✅ · static assets → **200** ✅

## Open this in your browser:

```
http://192.168.1.137:8080/
```

You'll get the llama.cpp chat UI (it auto-connects to the Qwen2.5-14B model on the M40).

## Final state — everything done ✅

| Item | Status |
|---|---|
| Tesla M40 24GB working (BIOS "Above 4G", driver 550.163.01) | ✅ |
| llama.cpp built for Maxwell (CUDA sm_52 + MMQ) | ✅ |
| Qwen2.5-14B-Instruct Q5_K_M (10.5GB) fully on GPU | ✅ |
| llama-server on :8080 (API + **web UI**) | ✅ running |
| Web UI embedded & gzipped | ✅ |
| Auto-suspend disabled (systemd + GNOME) | ✅ — stays up 24/7 |
| Speed | **~38 t/s prompt, ~13.6 t/s generation** |

## Quick reference

```bash
# terminal chat
~/projects/run-chat.sh

# restart server if needed
~/projects/run-server.sh        # web UI + OpenAI API on :8080

# OpenAI-compatible API
http://192.168.1.137:8080/v1   (model = the .gguf path)
```

⚠️ Reminder: no API key is set — keep port 8080 on your LAN only.

Still want me to set up the **systemd service** (auto-start llama-server on every boot)? Otherwise this is fully working — enjoy! 🚀
