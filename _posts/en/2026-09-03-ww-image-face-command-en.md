---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww image face command
translated: false
type: note
---

Done. Here's what I added:

## New command: `ww image face`

**Module:** `ww/image/face.py` — a flexible, face-aware photo cropper that ports the logic from your employment-files scripts into the `ww` toolkit.

**What it does:**
1. Detects the largest face with macOS Vision (`VNDetectFaceRectanglesRequest`).
2. Frames a head-and-shoulders crop centered on the face, with the face center positioned at a configurable fraction from the top.
3. Clamps to image bounds, then resamples (LANCZOS) to each target pixel size.

**Default presets** (all generated when no `--size`/`--preset` given):
- `square_600x600`, `rectangle_800x1000`, `qmas_visa_1500x2000`, `1inch_id_295x413`, `2inch_id_413x579`, `passport_413x531`

**Flexibility flags:**
- `-o / --out` — custom output dir (default: `<src_stem>_face/` next to source)
- `--size WxH` (repeatable) — ad-hoc target sizes; append `= name` to name the file, e.g. `--size 600x600 = profile`
- `--preset NAME` (repeatable) — only these named presets
- `--scale / --face-scale` — crop height = N × face height (default 2.7)
- `--top / --face-top` — face-center vertical fraction from top (default 0.40)
- `--quality` — JPEG quality (default 95)
- `--dpi` — output DPI (default 300)
- `--format JPEG|PNG`

**Examples:**
```
ww image face ~/IMG_6127.JPG                          # all 6 presets
ww image face ~/IMG_6127.JPG -o ./out                 # custom dir
ww image face ~/IMG_6127.JPG --size 600x600 --size 413x531
ww image face ~/IMG_6127.JPG --scale 2.5 --top 0.45 --quality 85
```

**Wiring done:**
- `pyproject.toml`: added `pyobjc-framework-Vision>=9.0` dependency (and ran `uv sync`).
- `ww/main.py`: registered `face` in the `image` group (help text + dispatch).
- `~/.zsh/completions/_ww`: added `face` to `image_cmds`. Run `autoload -Uz compinit && compinit` to reload.

Verified against `IMG_6127.JPG` — all presets and custom sizes crop correctly.
