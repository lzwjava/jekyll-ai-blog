---
audio: false
generated: true
image: false
lang: en
layout: post
title: New Video Generator
translated: false
type: note
---

All done. Here's a summary of what was created:

**`ww gen-video <file>`** — generates a vertical short-form video (9:16) from a markdown note.

**Files changed:**

- `ww/gen_video/__init__.py` — empty package init
- `ww/gen_video/video.py` — main module (~680 lines)
- `ww/main.py` — help text + dispatch block + group lookup
- `~/.zsh/completions/_ww` — zsh completion entry

**Pipeline:**

1. **LLM script generation** — reads markdown, uses your default MODEL to create a narration script + 5-6 image prompts per scene
2. **Flux image generation** — calls `black-forest-labs/flux.2-pro` via OpenRouter for each scene, handles base64 data URLs and brand-name moderation
3. **TTS narration** — uses macOS `say` command (Samantha/Tingting voice), converts to AAC
4. **FFmpeg assembly** — stitches images into a 1080×1920 vertical video with narration audio

**Usage:**

```
ww gen-video /path/to/note.md
ww gen-video /path/to/note.md --output my_video.mp4 --voice Samantha
ww gen-video /path/to/note.md --audio existing_narration.aac
ww gen-video /path/to/note.md --image-model black-forest-labs/flux.2-pro
```

**Tested** with the Tesla P100 vs M60 article — produced a 164s, 3.9 MB, 1080×1920 video with 5 Flux-generated images and narration.
