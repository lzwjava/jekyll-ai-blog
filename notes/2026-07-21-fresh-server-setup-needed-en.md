---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fresh Server Setup Needed
translated: false
type: note
---

The server is running but **bare** — no model files, no API server, only Jupyter Lab. Here's the full picture:

**Server Status: ✅ GPU Working**

| Test | Result |
| ------ | -------- |
| GPU Compute (HIP) | ✅ Vector add passed, 48GB VRAM, gfx1100 |
| ROCm Driver | ✅ 7.2.1 |
| Jupyter Lab | ✅ Running on port 8888 (base_url: `/instances/u-9758-811746f0/`) |
| API endpoint | ❌ "Instance unavailable" — no service on port 8000 |
| Model files | ❌ Empty cache, no Qwen3-8B downloaded |
| vLLM / API packages | ❌ Not installed |

The earlier successful API call was from a different session. This container is fresh — it starts Jupyter, but the model and API server need to be set up. Want me to install vLLM and download the Qwen3-8B model to get the API running?
