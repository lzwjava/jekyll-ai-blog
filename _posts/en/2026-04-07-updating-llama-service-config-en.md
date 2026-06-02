---
audio: false
generated: true
image: false
lang: en
layout: post
title: Updating Llama Service Configuration
translated: false
type: note
---

Here's a summary of what we did:

**Service Setup**
- Found 2 existing llama services: `llama-server.service` (working) and `llama.service` (broken — wrong path with capital `P`, kept crash-looping)
- Updated `llama-server.service` to match the actual running process settings instead of the outdated config

**Config Change**
| | Before | After |
|---|---|---|
| Model | DeepSeek-R1-0528-Qwen3-8B-Q4_K_M | gemma-4-E4B-it-Q5_K_M |
| Port | 11435 | 8081 |
| GPU layers | 99 | 43 |
| Context | 8192 | 65536 |
| Flash attn | — | off |

**Things worth noting**
- `llama.service` is still **enabled but broken** — it'll keep failing on every boot. Worth either fixing the path or disabling it: `sudo systemctl disable llama.service`
- The service is still **enabled**, so it will auto-start on next reboot — remember to start it manually when you're ready (or when the server is further away!)
- GPU dropped from ~5.7GB used → **166MiB** after stopping, temp went idle at 35°C
