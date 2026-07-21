---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restart AMD Instance for FLUX Fix
translated: false
type: note
---

Still down. The instance needs to be restarted from the **AMD Radeon cloud console** — the OOM crash killed the SSH daemon on port 31154.

Once you restart it, I'll:

1. **SSH in** with the fixed script (no `.to("cuda")`, uses `enable_sequential_cpu_offload()`)
2. **Remove FLUX.2-dev** (166GB, too large for 48GB VRAM)
3. **Download FLUX.1-dev** (~35GB, 12B params — fits 48GB VRAM)
4. **Generate** an image with proper memory settings

Let me know when it's back!
