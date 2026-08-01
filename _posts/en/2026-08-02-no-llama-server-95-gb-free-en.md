---
audio: false
generated: true
image: false
lang: en
layout: post
title: No llama-server, 9.5 GB free
translated: false
type: note
---

**No, llama-server is not running.** Nothing matching `llama` at all. The only AI daemon is `ollama serve` (PID 3339), and it's idle — not loaded on the GPU.

Current GPU state (RTX 4070, 12 GB):

| | MiB |
| --- | --- |
| Used | 2367 |
| **Free** | **9473** |

And the 2.3 GB used is **not** AI — it's all desktop/graphics:

- Xorg: 1430 MiB (biggest)
- warp-terminal: 204 MiB
- zed-editor: 191 MiB
- browsers / gnome-shell / nautilus etc.: rest

So there's nothing to kill for your use case — you actually have **~9.5 GB free**, which is plenty. Your large-v3 fp16 transcription needs only ~3.2 GB (or ~1.1 GB with `--compute-type int8`). The `--low-memory` rewrite fits easily.

If you still want headroom, the only meaningful targets would be closing browser/zed/warp-terminal tabs (they're the desktop apps eating VRAM), but it's not necessary for the whisper run.
